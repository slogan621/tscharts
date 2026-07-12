#!/usr/bin/env bash

#(C) Copyright Syd Logan 2026
#(C) Copyright Thousand Smiles Foundation 2026
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# Run filtered db import and monitor every 5 min for up to 12 hours.
set -euo pipefail

DOCKER_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="${LOG:-/tmp/db-import-monitor.log}"
RESULT="${RESULT:-/tmp/db-import-result.log}"
INTERVAL_SEC="${INTERVAL_SEC:-300}"
MAX_CHECKS="${MAX_CHECKS:-144}"

if [ -f "$DOCKER_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$DOCKER_DIR/.env"
  set +a
fi

echo "=== Import+monitor started $(date -Is) ===" | tee -a "$LOG"
echo "=== Import+monitor started $(date -Is) ===" > "$RESULT"

(
  "$DOCKER_DIR/scripts/import-db-excluding-logs.sh" "$@" >>"$RESULT" 2>&1
  echo "exit_code=$?" >>"$RESULT"
) &
IMPORT_PID=$!

echo "import_pid=$IMPORT_PID" | tee -a "$LOG"

for i in $(seq 1 "$MAX_CHECKS"); do
  TABLES=$(docker exec mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=\"tscharts\";" 2>/dev/null' || echo "error")

  IMPORT_RUNNING="no"
  if kill -0 "$IMPORT_PID" 2>/dev/null; then
    IMPORT_RUNNING="yes"
  fi

  echo "$(date -Is) check $i/$MAX_CHECKS tables=$TABLES import_running=$IMPORT_RUNNING" | tee -a "$LOG"

  if [ "$IMPORT_RUNNING" = "no" ]; then
    IMPORT_EXIT=0
    wait "$IMPORT_PID" || IMPORT_EXIT=$?
    echo "$(date -Is) import process ended exit_code=${IMPORT_EXIT}" | tee -a "$LOG"
    if [ "$IMPORT_EXIT" -eq 0 ]; then
      echo "IMPORT_STATUS=success $(date -Is)" | tee -a "$LOG"
    else
      echo "IMPORT_STATUS=failed exit_code=${IMPORT_EXIT} $(date -Is)" | tee -a "$LOG"
    fi
    docker exec mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" tscharts -e "
      SELECT COUNT(*) AS tables_in_db FROM information_schema.tables WHERE table_schema=\"tscharts\";
      SELECT COUNT(*) AS auth_users FROM auth_user;
      SELECT table_name FROM information_schema.tables
        WHERE table_schema=\"tscharts\" AND table_name IN (\"requestlog_requestlog\", \"django_admin_log\");
    " 2>/dev/null' | tee -a "$LOG" || true
    tail -20 "$RESULT" | tee -a "$LOG" || true
    echo "=== Import+monitor finished $(date -Is) ===" | tee -a "$LOG"
    exit "$IMPORT_EXIT"
  fi

  sleep "$INTERVAL_SEC"
done

echo "IMPORT_STATUS=timeout $(date -Is)" | tee -a "$LOG"
echo "=== Import+monitor finished (timeout) $(date -Is) ===" | tee -a "$LOG"
exit 124

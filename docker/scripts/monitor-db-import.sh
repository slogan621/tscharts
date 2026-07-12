#!/usr/bin/env bash
# Monitor db-8.sql import progress. Default: every 5 min for 12 hours (144 checks).
set -euo pipefail

INTERVAL_SEC="${INTERVAL_SEC:-300}"
MAX_CHECKS="${MAX_CHECKS:-144}"   # 144 * 5 min = 12 hours
LOG="${LOG:-/tmp/db-import-monitor.log}"
IMPORT_PID="${IMPORT_PID:-}"

echo "=== Import monitor (12h) started $(date -Is) max_checks=$MAX_CHECKS interval=${INTERVAL_SEC}s ===" | tee -a "$LOG"

for i in $(seq 1 "$MAX_CHECKS"); do
  TABLES=$(docker exec mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=\"tscharts\";" 2>/dev/null' || echo "error")

  IMPORT_RUNNING="no"
  if [ -n "$IMPORT_PID" ] && kill -0 "$IMPORT_PID" 2>/dev/null; then
    IMPORT_RUNNING="yes"
  elif docker exec mysql_db sh -c 'pgrep -f "mysql.*tscharts" >/dev/null' 2>/dev/null; then
    IMPORT_RUNNING="yes"
  fi

  echo "$(date -Is) check $i/$MAX_CHECKS tables=$TABLES import_running=$IMPORT_RUNNING" | tee -a "$LOG"

  if [ "$IMPORT_RUNNING" = "no" ]; then
    echo "$(date -Is) import process ended" | tee -a "$LOG"
    docker exec mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" tscharts -e "SHOW TABLES LIKE \"auth_user\"; SELECT COUNT(*) AS auth_users FROM auth_user;" 2>/dev/null' | tee -a "$LOG" || true
    echo "=== Import monitor finished $(date -Is) ===" | tee -a "$LOG"
    exit 0
  fi

  if [ "$i" -lt "$MAX_CHECKS" ]; then
    sleep "$INTERVAL_SEC"
  fi
done

echo "$(date -Is) reached max wait (${MAX_CHECKS} checks)" | tee -a "$LOG"
echo "=== Import monitor finished $(date -Is) ===" | tee -a "$LOG"

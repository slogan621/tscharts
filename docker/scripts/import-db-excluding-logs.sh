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

# Import a MySQL dump into the running tscharts database, skipping large log tables.
set -euo pipefail

# Usage:
#   ./import-db-excluding-logs.sh /path/to/dump.sql
#   DUMP_FILE=/path/to/dump.sql ./import-db-excluding-logs.sh
#
# The dump file must not be committed to git (it may contain private data).
#
# To create a dump suitable for this script (run on the source server):
#   mysqldump -u USER -p --databases tscharts --single-transaction \
#     --set-gtid-purged=OFF > /secure/path/outside-repo/tscharts-dump.sql
#
# This script pipes the dump through filter-db-sql.py, which omits:
#   - requestlog_requestlog  (very large API request log)
#   - django_admin_log       (Django admin action history)
#
# Skipped tables are created empty later via fake-initial-migrate.sh.

DOCKER_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FILTER="$DOCKER_DIR/scripts/filter-db-sql.py"
DUMP="${1:-${DUMP_FILE:-}}"

if [ -z "$DUMP" ]; then
  echo "Usage: $0 /path/to/dump.sql" >&2
  echo "Or set DUMP_FILE to the dump path." >&2
  exit 1
fi

if [ ! -f "$DUMP" ]; then
  echo "Dump not found: $DUMP" >&2
  exit 1
fi

if ! docker exec mysql_db mysqladmin ping -h127.0.0.1 -uroot -p"${MYSQL_ROOT_PASSWORD:-}" --silent 2>/dev/null; then
  if [ -f "$DOCKER_DIR/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    source "$DOCKER_DIR/.env"
    set +a
  fi
fi

echo "=== Importing $DUMP (excluding logging tables) ==="
echo "=== Started $(date -Is) ==="

python3 "$FILTER" "$DUMP" | docker exec -i mysql_db sh -c \
  'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" tscharts'

echo "=== Finished $(date -Is) ==="
docker exec mysql_db sh -c \
  'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" tscharts -e "
    SELECT COUNT(*) AS tables_in_db FROM information_schema.tables WHERE table_schema=\"tscharts\";
    SELECT table_name FROM information_schema.tables
      WHERE table_schema=\"tscharts\" AND table_name IN (
        \"requestlog_requestlog\", \"django_admin_log\"
      );
  "'

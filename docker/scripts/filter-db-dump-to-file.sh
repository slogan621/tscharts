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

# Filter a mysqldump on disk (omit log tables) so a smaller file can be copied
# to a deployment host. Does not require Docker or a running database.
#
# Usage:
#   ./filter-db-dump-to-file.sh /path/to/db-8.sql
#   ./filter-db-dump-to-file.sh /path/to/db-8.sql /path/to/db-8-filtered.sql
#
# Default output: same directory as the input, with -filtered inserted before
# the extension (db-8.sql -> db-8-filtered.sql).
#
# Omits the same tables as import-db-excluding-logs.sh / filter-db-sql.py:
#   - requestlog_requestlog
#   - django_admin_log
#
# On the deployment host you can then either:
#   ./import-db-excluding-logs.sh /path/to/db-8-filtered.sql
#     (filter is idempotent; already-skipped tables are simply absent)
# or load directly:
#   docker exec -i mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" tscharts' \
#     < /path/to/db-8-filtered.sql
# Then always run: ./fake-initial-migrate.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FILTER="$SCRIPT_DIR/filter-db-sql.py"

SRC="${1:-}"
DEST="${2:-}"

if [ -z "$SRC" ]; then
  echo "Usage: $0 /path/to/dump.sql [/path/to/filtered.sql]" >&2
  exit 1
fi

if [ ! -f "$SRC" ]; then
  echo "Dump not found: $SRC" >&2
  exit 1
fi

if [ -z "$DEST" ]; then
  if [[ "$SRC" == *.sql ]]; then
    DEST="${SRC%.sql}-filtered.sql"
  else
    DEST="${SRC}-filtered.sql"
  fi
fi

if [ "$SRC" -ef "$DEST" ] 2>/dev/null || [ "$SRC" = "$DEST" ]; then
  echo "Refusing to overwrite the source file: $SRC" >&2
  exit 1
fi

if [ -e "$DEST" ]; then
  echo "Output already exists (refusing to overwrite): $DEST" >&2
  echo "Remove it or pass a different output path." >&2
  exit 1
fi

echo "=== Source:  $SRC ($(du -h "$SRC" | awk '{print $1}')) ==="
echo "=== Output:  $DEST ==="
echo "=== Started $(date -Is) ==="

python3 "$FILTER" "$SRC" "$DEST"

echo "=== Finished $(date -Is) ==="
echo "=== Filtered: $DEST ($(du -h "$DEST" | awk '{print $1}')) ==="

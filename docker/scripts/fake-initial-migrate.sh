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

# Align django_migrations with a restored database schema (post-import).
# Run after import-db-excluding-logs.sh completes.
set -euo pipefail

echo "=== Waiting for SQL import to finish (if still running) ==="
while docker exec mysql_db sh -c 'pgrep -f "mysql.*tscharts" >/dev/null' 2>/dev/null; do
  TABLES=$(docker exec mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=\"tscharts\";" 2>/dev/null' || echo "?")
  echo "$(date -Is) import still running, tables=$TABLES"
  sleep 60
done

TABLES=$(docker exec mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -N -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=\"tscharts\";" 2>/dev/null')
echo "Import done (or not running). tables=$TABLES"
if [ "${TABLES:-0}" -lt 48 ]; then
  echo "WARNING: expected ~48 tables from dump (2 log tables skipped); got $TABLES. Continue anyway? (Ctrl-C to abort)"
  sleep 10
fi

echo "=== Step 1: Clear django_migrations history ==="
docker exec django_app python manage.py shell -c \
  "from django.db.migrations.recorder import MigrationRecorder; n=MigrationRecorder.Migration.objects.count(); MigrationRecorder.Migration.objects.all().delete(); print(f'Deleted {n} records')"

echo "=== Step 2: Fake all migrations (schema already in DB from import) ==="
docker exec django_app python manage.py migrate --fake

echo "=== Step 3: requestlog table (skipped in SQL import) — apply for real ==="
docker exec django_app python manage.py shell -c \
  "from django.db.migrations.recorder import MigrationRecorder; MigrationRecorder.Migration.objects.filter(app='requestlog').delete()"
docker exec django_app python manage.py migrate requestlog

echo "=== Step 4: Optional — invalidate old sessions (Django 1.x → 5.x) ==="
docker exec mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" tscharts -e "TRUNCATE TABLE django_session;"' || true

echo "=== Step 5: Verify ==="
docker exec django_app python manage.py showmigrations | tail -30
docker exec mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" tscharts -e "
  SELECT COUNT(*) AS migration_records FROM django_migrations;
  SELECT COUNT(*) AS tables_in_db FROM information_schema.tables WHERE table_schema=\"tscharts\";
  SELECT COUNT(*) AS auth_users FROM auth_user;
" 2>/dev/null'

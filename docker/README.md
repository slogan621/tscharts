# Docker development stack for tscharts

Run the full stack (MySQL, Django, nginx, phpMyAdmin) from this directory:

```bash
cp .env.example .env   # edit credentials locally; never commit .env
docker compose up -d --build
```

## URLs

| Service | URL |
|---------|-----|
| Django API (HTTPS) | https://localhost |
| phpMyAdmin (HTTPS) | https://localhost:8443 |

## SSL certificates

The `nginx*certs/` directories contain **development-only** self-signed certificates
for localhost. **Do not use these in production.**

Or, to generate your own, use openssl, as in the following example:

```bash
openssl req -x509 -newkey rsa:4096 -keyout dev_key.pem -out dev_cert.pem -sha256 -days 365 -nodes -subj "/CN=localhost"
```

## Traffic monitor (optional, off by default)

Packet capture is disabled unless you enable the `debug` profile:

```bash
docker compose --profile debug up -d traffic-monitor
```

Captures are written to `tcpdump_data/` and can grow large quickly. Do not enable
this unless you are actively debugging network traffic.

## Database & migrations

Migration files under each Django app describe the schema this codebase expects.
How you apply them depends on whether the database already has tables and data.

The `django` service does **not** run `migrate` on container start (only
`collectstatic` and gunicorn). Run migrations explicitly using one of the paths
below.

### Path A — Restore from a SQL backup (typical local development)

Use this when you have a private `mysqldump` of an existing tscharts database.
Dumps contain private data and must **never** be committed to git.

```bash
./scripts/import-db-excluding-logs.sh /secure/path/outside-repo/tscharts-dump.sql
# or:
DUMP_FILE=/secure/path/outside-repo/tscharts-dump.sql ./scripts/import-db-excluding-logs.sh
./scripts/fake-initial-migrate.sh
```

See `scripts/import-db-excluding-logs.sh` for how to produce a suitable `mysqldump`.
Scripts read MySQL credentials from `docker/.env` via the running container.

A dump alone does **not** restore patient headshots or X-ray files. After import,
copy the legacy image tree into the `chart_images` volume — see
[Patient images (headshots and X-rays)](#patient-images-headshots-and-x-rays).

To produce a smaller dump **before** copying it to another host (same log tables
omitted, no Docker required):

```bash
./scripts/filter-db-dump-to-file.sh /path/to/db-8.sql
# writes /path/to/db-8-filtered.sql — then scp that file instead
```

**Why import + fake?** The dump already contains table definitions and data. The
`django_migrations` table in an older backup may not match Django 5.2 or the
migration files in this repo. `fake-initial-migrate.sh`:

1. Waits for the import to finish (if still running).
2. Clears `django_migrations`.
3. Runs `migrate --fake` so Django records all migrations as applied without
   altering existing tables.
4. Runs a real `migrate requestlog` — that table is omitted from the import
   (large log data) and is created empty.
5. Optionally truncates `django_session` (sessions from Django 1.x are invalid
   on 5.2).
6. Prints verification queries.

The import script skips `requestlog_requestlog` and `django_admin_log` via
`filter-db-sql.py`. Expect ~48 application tables after import (two log tables
skipped).

### Path B — Empty database (greenfield / CI)

Use this when starting with an empty MySQL database and no SQL dump:

```bash
docker compose up -d --build
docker exec django_app python manage.py migrate
```

This applies all migrations for real and creates tables from scratch. You will
need to create users and seed data separately (for example
`docker exec -it django_app python manage.py createsuperuser`).

### Path C — Schema changes after the 5.2 baseline

When you change models in this repo:

```bash
# on the host, from the repository root:
docker exec django_app python manage.py makemigrations
docker exec django_app python manage.py migrate
```

Commit new migration files with your code changes. Use **real** `migrate` here —
not `--fake` — unless you are deliberately aligning migration history with an
existing schema you applied by hand.

**Do not** run `fake-initial-migrate.sh` on a database that was built with
`migrate` on an empty DB; it is only for post-restore alignment.

## Patient images (headshots and X-rays)

A SQL dump restores `image_image` rows (metadata: patient id, type, path uuid,
timestamps) but **not** the image files themselves. Those live on disk under
Django’s `CHART_IMAGES_DIR` (default `/opt/thousandsmiles/images`).

Layout on the legacy host (and inside the container after migration):

```text
/opt/thousandsmiles/images/{patient_id}/{path}
```

`path` is the uuid stored in `image_image.path`. Headshots use `imagetype='h'`;
X-rays use `imagetype='x'`. Without the files, the image API returns empty data
even when the database has thousands of rows.

### Docker volume

The `django` service mounts a named volume `chart_images` at
`/opt/thousandsmiles/images`. Docker creates it on first `compose up`. It
persists across container restarts and `docker compose down`, but is removed by
`docker compose down -v` (same caveat as `db_data`).

```bash
docker volume ls | grep chart_images
# typically: docker_chart_images  (project directory name + "_chart_images")
```

### Migrate files from a legacy / existing deployment

Do this after the stack is up (so the volume exists) and preferably after the
database restore so patient ids match.

1. **On the legacy host**, confirm the tree and approximate size:

   ```bash
   sudo ls /opt/thousandsmiles/images | head
   sudo du -sh /opt/thousandsmiles/images
   ```

2. **Copy to a staging directory on the new host** (example with `rsync`):

   ```bash
   # on the new Docker host
   mkdir -p /tmp/ts-images
   rsync -aH --info=progress2 \
     USER@LEGACY_HOST:/opt/thousandsmiles/images/ \
     /tmp/ts-images/
   ```

   Preserve directory structure (`patient_id` folders and uuid filenames). Do not
   commit these files to git; they are private patient data.

3. **Load the staging tree into the `chart_images` volume** (from this `docker/`
   directory):

   ```bash
   VOLUME=$(docker volume ls -q | grep chart_images | head -1)
   docker run --rm \
     -v "${VOLUME}:/dest" \
     -v /tmp/ts-images:/src:ro \
     alpine cp -a /src/. /dest/
   ```

4. **Verify inside the Django container**:

   ```bash
   docker exec django_app ls /opt/thousandsmiles/images | head
   # pick a patient_id that has a headshot row in image_image:
   docker exec django_app ls "/opt/thousandsmiles/images/<patient_id>" | head
   ```

   Optionally compare counts: number of headshot files on disk vs
   `SELECT COUNT(*) FROM image_image WHERE imagetype='h';` (counts need not match
   exactly if some historical files were pruned, but a large gap usually means
   the copy was incomplete).

5. **Smoke-test the API** (after login; use a patient that has a headshot):

   ```bash
   curl -sk -H "Authorization: Token $TOKEN" \
     "https://localhost/tscharts/v1/image/?patient=<patient_id>&type=Headshot&newest=true"
   ```

   A successful response includes image metadata and base64 `data` when the file
   is present. Empty or missing `data` usually means the file was not copied.

### Alternative: bind-mount a host directory

If you prefer to `rsync` directly to a host path (for example on EC2), replace
the named volume in `docker-compose.yml` with a bind mount:

```yaml
# under django.volumes — instead of chart_images:/opt/thousandsmiles/images
- /opt/thousandsmiles/images:/opt/thousandsmiles/images
```

Create the host directory, copy files there with `rsync`, then recreate the
Django service. Path inside the container must remain
`/opt/thousandsmiles/images` unless you also change `CHART_IMAGES_DIR` in
settings.

## End-to-end bring-up and verification

This is the workflow used to validate the stack (including database persistence
across container restarts). It follows **Path A** above.

### 1. Start the cluster

```bash
cd docker
cp .env.example .env          # set MYSQL_* passwords locally
docker compose up -d --build
docker compose ps             # mysql_db should be healthy, django_app running
```

### 2. Import a local dump and align migrations

```bash
./scripts/import-db-excluding-logs.sh /path/to/your-dump.sql
./scripts/fake-initial-migrate.sh
```

### 3. Verify API login and a sample query

Set credentials from a user that exists in your database. Do not commit real
values to the repository.

```bash
export TSCHARTS_USERNAME='<your username>'
export TSCHARTS_PASSWORD='<your password>'
export TSCHARTS_CLINIC_ID='<clinic id>'   # e.g. an id that exists in your dump

curl -sk -X POST https://localhost/tscharts/v1/login/ \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$TSCHARTS_USERNAME\",\"password\":\"$TSCHARTS_PASSWORD\"}"

TOKEN=$(curl -sk -X POST https://localhost/tscharts/v1/login/ \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$TSCHARTS_USERNAME\",\"password\":\"$TSCHARTS_PASSWORD\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk -H "Authorization: Token $TOKEN" \
  "https://localhost/tscharts/v1/clinic/${TSCHARTS_CLINIC_ID}/"
```

A successful clinic response looks like:

```json
{"id": 3, "start": "02/02/2019", "end": "02/02/2019", "location": "Thousand Smiles Ensenada"}
```

(field values depend on your data)

### 4. Restart and confirm persistence

```bash
docker compose down
docker compose up -d
```

Re-run the login and clinic curls from step 3. Responses should match, and
`auth_user` row counts should be unchanged (data lives in the `db_data` volume).

### 5. Optional checks

```bash
docker exec mysql_db sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" tscharts -e "
  SELECT COUNT(*) AS tables FROM information_schema.tables WHERE table_schema=\"tscharts\";
  SELECT COUNT(*) AS users FROM auth_user;
"'
docker exec django_app python -c "import django; print(django.get_version())"
```

## Requirements

- Docker and Docker Compose
- ~25 GB free disk space if restoring a large production dump locally

## License

(C) Copyright Syd Logan 2026  
(C) Copyright Thousand Smiles Foundation 2026  

Licensed under the Apache License, Version 2.0. See [LICENSE.md](../LICENSE.md).

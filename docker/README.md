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

To generate your own local certificates, use the [cert-gen](https://github.com/slogan621/cert-gen)
tool and its documentation.

## Traffic monitor (optional, off by default)

Packet capture is disabled unless you enable the `debug` profile:

```bash
docker compose --profile debug up -d traffic-monitor
```

Captures are written to `tcpdump_data/` and can grow large quickly. Do not enable
this unless you are actively debugging network traffic.

## Database restore (local development only)

Database dumps contain private data and must **never** be committed to git.
Store dumps outside this repository and pass the path explicitly:

```bash
./scripts/import-db-excluding-logs.sh /secure/path/outside-repo/tscharts-dump.sql
# or:
DUMP_FILE=/secure/path/outside-repo/tscharts-dump.sql ./scripts/import-db-excluding-logs.sh
./scripts/fake-initial-migrate.sh
```

See `scripts/import-db-excluding-logs.sh` for how to produce a suitable `mysqldump`.
Scripts read credentials from `docker/.env` via the running MySQL container.

## End-to-end bring-up and verification

This is the workflow used to validate the stack (including database persistence
across container restarts).

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

Expect ~48 tables after import (two log tables are skipped). `fake-initial-migrate.sh`
waits for import to finish if it is still running.

### 3. Verify API login and a sample query

```bash
curl -sk -X POST https://localhost/tscharts/v1/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"register","password":"register"}'

TOKEN=$(curl -sk -X POST https://localhost/tscharts/v1/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"register","password":"register"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

curl -sk -H "Authorization: Token $TOKEN" \
  https://localhost/tscharts/v1/clinic/3/
```

Expected clinic 3 response:

```json
{"id": 3, "start": "02/02/2019", "end": "02/02/2019", "location": "Thousand Smiles Ensenada"}
```

### 4. Restart and confirm persistence

```bash
docker compose down
docker compose up -d
```

Re-run the login and clinic 3 curls from step 3. Responses should match, and
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

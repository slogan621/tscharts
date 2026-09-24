# tsdashboard-web Docker deployment

Standalone container for the clinic-ops dashboard. **Not** part of
`tscharts/docker/docker-compose.yml` — deploy it on its own (same EC2 or
another host).

## Build & run (standalone)

```bash
cd webapps/tsdashboard-web/docker
cp .env.example .env
# edit TSCHARTS_BASE_URL
./gen-cert.sh <public-ip-or-dns>
docker compose up -d --build
# UI: https://<host>:<HOST_HTTPS_PORT>
```

Set `APP_PORT` and `HOST_HTTPS_PORT` in `.env` before starting. Neither has a
default in this repo.

`gen-cert.sh` writes a self-signed certificate into `docker/certs/` (gitignored).
The certificate name must match the host you type in the browser (`IP:` SAN for
an address, `DNS:` SAN for a hostname). Replace those two PEM files with a
publicly trusted certificate when you have one; nginx reads
`certs/dashboard.pem` and `certs/dashboard-key.pem`.

Port **443** on the tscharts host stays the API. The dashboard publishes HTTPS
on `HOST_HTTPS_PORT`. Plain HTTP on that port will no longer answer.

## How it reaches the tscharts API

| Mode | When | `TSCHARTS_BASE_URL` | Notes |
|------|------|---------------------|--------|
| **A. Tablet-style HTTPS** | Other host, or same host without joining compose network | `https://<ec2-ip-or-dns>` or `https://host.docker.internal` | Needs firewall allow from this host; set `TSCHARTS_TLS_INSECURE=1` if cert hostname does not match |
| **B. Internal Docker network** | Same machine as tscharts compose | `http://django:8000` | Attach to tscharts network (below); no TLS. Use the Compose **service** name `django`, not container name `django_app` (underscores are invalid in HTTP Host / Django `ALLOWED_HOSTS`) |

### Mode A — like a tablet

```bash
# .env
TSCHARTS_BASE_URL=https://<ec2-ip-or-dns>   # or host.docker.internal on same box
TSCHARTS_TLS_INSECURE=1
APP_PORT=<port>
HOST_HTTPS_PORT=<port>
docker compose up -d --build
```

`127.0.0.1` inside the container is **not** the host. Use `host.docker.internal`
(compose file already maps it) or the host’s real IP.

### Mode B — join tscharts compose network (optional)

tscharts remains its own compose project. This dashboard **optionally** joins
that network:

```bash
# find network name
docker network ls | grep app-network
# e.g. docker_app-network

# .env
TSCHARTS_BASE_URL=http://django:8000
TSCHARTS_TLS_INSECURE=0
TSCHARTS_COMPOSE_NETWORK=docker_app-network

docker compose -f docker-compose.yml -f docker-compose.tscharts-net.yml up -d --build
```

Django is reached as Compose service name `django` on port 8000 (gunicorn), not
via nginx. Ensure `ALLOWED_HOSTS` includes `django` (or rely on Mode A /
`host.docker.internal` with Host rewriting).

## Firewall

If the UI is on EC2, allow `HOST_HTTPS_PORT` from the same admin
IPs as 443. That port is now TLS, not plain HTTP. You do **not** need to open
Django’s 8000 publicly for Mode B, and you do **not** move the dashboard onto
443 (that listener is the tscharts API).

## Layout

```
webapps/tsdashboard-web/
  Dockerfile                 # multi-stage Rust build
  docker/
    docker-compose.yml       # standalone (app + nginx TLS)
    docker-compose.tscharts-net.yml   # optional network join
    gen-cert.sh              # self-signed cert into certs/
    nginx/templates/default.conf.template
    .env.example
    README.md
```

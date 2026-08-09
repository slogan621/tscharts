# tsdashboard-web Docker deployment

Standalone container for the clinic-ops dashboard. **Not** part of
`tscharts/docker/docker-compose.yml` — deploy it on its own (same EC2 or
another host).

## Build & run (standalone)

```bash
cd webapps/tsdashboard-web/docker
cp .env.example .env
# edit TSCHARTS_BASE_URL
docker compose up -d --build
# UI: http://<host>:3000
```

## How it reaches the tscharts API

| Mode | When | `TSCHARTS_BASE_URL` | Notes |
|------|------|---------------------|--------|
| **A. Tablet-style HTTPS** | Other host, or same host without joining compose network | `https://<ec2-ip-or-dns>` or `https://host.docker.internal` | Needs firewall allow from this host; set `TSCHARTS_TLS_INSECURE=1` if cert hostname does not match |
| **B. Internal Docker network** | Same machine as tscharts compose | `http://django_app:8000` | Attach to tscharts network (below); no TLS |

### Mode A — like a tablet

```bash
# .env
TSCHARTS_BASE_URL=https://52.x.x.x          # or host.docker.internal on same box
TSCHARTS_TLS_INSECURE=1
HOST_PORT=3000
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
TSCHARTS_BASE_URL=http://django_app:8000
TSCHARTS_TLS_INSECURE=0
TSCHARTS_COMPOSE_NETWORK=docker_app-network

docker compose -f docker-compose.yml -f docker-compose.tscharts-net.yml up -d --build
```

Django is reached as service name `django_app` on port 8000 (gunicorn), not via nginx.

## Firewall

If the UI is on EC2, allow `HOST_PORT` (e.g. 3000) from the same admin IPs as
443. You do **not** need to open Django’s 8000 publicly for Mode B.

## Layout

```
webapps/tsdashboard-web/
  Dockerfile                 # multi-stage Rust build
  docker/
    docker-compose.yml       # standalone
    docker-compose.tscharts-net.yml   # optional network join
    .env.example
    README.md
```

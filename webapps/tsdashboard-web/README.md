# tsdashboard-web

Rust/Axum clinic operations dashboard for Thousand Smiles. Replaces the wxPython
`apps/tsdashboard` desktop tool for clinic/patient/registration workflows.

**End-user documentation:** [docs/USER_GUIDE.md](docs/USER_GUIDE.md) — how to plan
clinics, maintain data between events, and review or correct records after
volunteers register patients with
[tscharts-register](https://github.com/slogan621/tscharts-register).

Imaging (X-ray view/upload/delete) is a **separate module** (`/imaging/...`) so
clinic ops stay independent.

## Features (v1)

**Clinics**
- Default list: past calendar year **including currently running** clinics; future hidden
- Filters: all past, future only, custom date range
- Create future clinic; delete future clinic only (mistaken entry)

**Clinic detail**
- List registered patients
- Register existing patient for **current or past** clinic (not future)
- Unregister patient from clinic

**Patients**
- Create / edit demographics (not registration)
- Search by name / CURP

**Imaging**
- Stub routes with deep links from clinic patient rows (implement next)

**Print agent**
- Optional later via `PRINT_AGENT_URL` (REST wristband microservice)

## Requirements

- Rust 1.75+ (`rustup`)
- Reachable tscharts API (`TSCHARTS_BASE_URL`)

## Run (local cargo)

```bash
cd webapps/tsdashboard-web
cp .env.example .env
# edit TSCHARTS_BASE_URL
cargo run
# open http://127.0.0.1:3000
```

## Run (Docker, standalone)

Not part of `tscharts/docker` compose. See **[docker/README.md](docker/README.md)**.

```bash
cd webapps/tsdashboard-web/docker
cp .env.example .env
docker compose up -d --build
```

Modes: tablet-style HTTPS to the API, or optional join of the tscharts Docker
network for `http://django:8000` (Compose service name).

## Layout

```
Dockerfile          # multi-stage image
docker/             # standalone compose + optional tscharts-net overlay
src/
  main.rs
  config.rs
  clinic_filter.rs
  client/
  routes/
  html.rs
  session.rs
static/style.css
```

## Tests

```bash
cargo test
```

## License

Apache-2.0 (same as Thousand Smiles / Syd Logan project licensing).

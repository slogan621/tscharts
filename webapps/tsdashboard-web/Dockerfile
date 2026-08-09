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

# Build from repository context: webapps/tsdashboard-web/
#   docker build -t tsdashboard-web .
# Or via docker/docker-compose.yml (build context is ..).

FROM rust:1.97-bookworm AS builder
WORKDIR /src
COPY Cargo.toml Cargo.lock ./
COPY src ./src
COPY static ./static
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /src/target/release/tsdashboard-web /app/tsdashboard-web
COPY --from=builder /src/static /app/static
ENV STATIC_DIR=/app/static \
    LISTEN_ADDR=0.0.0.0:3000
EXPOSE 3000
USER nobody
CMD ["/app/tsdashboard-web"]

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

# Write a self-signed cert for the dashboard nginx proxy.
# Usage: ./gen-cert.sh <public-ip-or-dns>
#        ./gen-cert.sh dashboard.example.org

set -euo pipefail

host="${1:-}"
if [[ -z "$host" ]]; then
  echo "usage: $0 <ip-or-dns>" >&2
  exit 1
fi

dir="$(cd "$(dirname "$0")" && pwd)/certs"
mkdir -p "$dir"

if [[ "$host" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  san="IP:${host},DNS:localhost"
  if [[ "$host" != "127.0.0.1" ]]; then
    san="${san},IP:127.0.0.1"
  fi
else
  san="DNS:${host},DNS:localhost,IP:127.0.0.1"
fi

openssl req -x509 -newkey rsa:2048 -sha256 -days 397 -nodes \
  -keyout "$dir/dashboard-key.pem" \
  -out "$dir/dashboard.pem" \
  -subj "/CN=${host}" \
  -addext "subjectAltName=${san}"

chmod 644 "$dir/dashboard.pem"
chmod 600 "$dir/dashboard-key.pem"

echo "wrote $dir/dashboard.pem"
echo "wrote $dir/dashboard-key.pem"
echo "SAN: ${san}"

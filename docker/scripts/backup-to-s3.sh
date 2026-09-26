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

# Weekly backup: gzipped mysqldump of tscharts, plus a tarball of the
# chart image volume. Both are uploaded to S3 and removed from the host.
#
# Configure docker/backup.env from backup.env.example. Cron installs
# docker/cron/tscharts-backup.

set -euo pipefail

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"

DOCKER_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$DOCKER_DIR/backup.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE (copy backup.env.example and set S3_PREFIX)." >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

if [[ -z "${S3_PREFIX:-}" || "$S3_PREFIX" == *YOUR_BUCKET* ]]; then
  echo "Set S3_PREFIX in $ENV_FILE." >&2
  exit 1
fi

IMAGE_VOLUME="${IMAGE_VOLUME:-docker_chart_images}"
STAMP="$(date +%F)"
WORKDIR="$(mktemp -d /var/tmp/tscharts-backup.XXXXXX)"
trap 'rm -rf "$WORKDIR"' EXIT

echo "=== Backup $STAMP started $(date -Is) ==="

DUMP="$WORKDIR/tscharts-$STAMP.sql.gz"
# MyISAM is the default engine, so lock tables for a consistent dump.
docker exec mysql_db sh -c \
  'mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" --lock-tables --routines --events tscharts' \
  | gzip > "$DUMP"
aws s3 cp "$DUMP" "$S3_PREFIX/tscharts-$STAMP.sql.gz"
echo "Uploaded database dump"

IMAGES="$(docker volume inspect "$IMAGE_VOLUME" --format '{{.Mountpoint}}')"
if [[ ! -d "$IMAGES" ]]; then
  echo "Image volume mount not found: $IMAGES" >&2
  exit 1
fi

TAR="$WORKDIR/tscharts-images-$STAMP.tar.gz"
# Archive contents are <patient_id>/<file>, which is the layout of
# /opt/thousandsmiles/images (the volume root).
tar -C "$IMAGES" -czf "$TAR" .
aws s3 cp "$TAR" "$S3_PREFIX/tscharts-images-$STAMP.tar.gz"
echo "Uploaded image tarball"

echo "=== Backup $STAMP finished $(date -Is) ==="

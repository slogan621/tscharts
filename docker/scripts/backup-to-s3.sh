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

# Weekly backup: gzipped mysqldump of tscharts, plus a tarball of chart
# images. Image backups are incremental. docker/image-backup.toc lists
# every relative path successfully uploaded since the last full archive.
# A deletion makes the next archive a full copy of the volume.
# Restore images from the newest *-full.tar.gz, then each later *-incr.tar.gz.
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

# Cron runs as root and does not see a user's ~/.aws. Use that home's
# credentials when the root environment has none of its own.
if [[ -z "${AWS_SHARED_CREDENTIALS_FILE:-}${AWS_ACCESS_KEY_ID:-}${AWS_PROFILE:-}" ]]; then
  aws_home="${AWS_CONFIG_HOME:-}"
  if [[ -z "$aws_home" && "$(id -u)" -eq 0 && -f /home/ubuntu/.aws/credentials ]]; then
    aws_home=/home/ubuntu
  fi
  if [[ -n "$aws_home" && -f "$aws_home/.aws/credentials" ]]; then
    export AWS_SHARED_CREDENTIALS_FILE="$aws_home/.aws/credentials"
    if [[ -f "$aws_home/.aws/config" ]]; then
      export AWS_CONFIG_FILE="$aws_home/.aws/config"
    fi
  fi
fi

STAMP="$(date +%F)"
WORKDIR="$(mktemp -d /var/tmp/tscharts-backup.XXXXXX)"
trap 'rm -rf "$WORKDIR"' EXIT

# Publish a streamed upload only when every pipeline stage succeeded.
# The object is stored under dest.partial first. A disk-full or quota
# error makes tar, gzip, or aws exit non-zero; the partial object is
# removed and the script stops before the image manifest is updated.
publish_stream() {
  local dest="$1"
  shift
  local failed=0 code
  for code in "$@"; do
    if [[ "$code" -ne 0 ]]; then
      failed=1
    fi
  done
  if [[ "$failed" -ne 0 ]]; then
    echo "Backup aborted (pipeline status: $*). Incomplete upload removed." >&2
    aws s3 rm "${dest}.partial" >/dev/null 2>&1 || true
    exit 1
  fi
  aws s3 mv "${dest}.partial" "$dest"
}

echo "=== Backup $STAMP started $(date -Is) ==="

# Stream to S3. A local copy of either archive can exceed the account
# disk quota (the image set already did, under /tmp).
# MyISAM is the default engine, so lock tables for a consistent dump.
sql_dest="$S3_PREFIX/tscharts-$STAMP.sql.gz"
docker exec mysql_db sh -c \
  'mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" --lock-tables --routines --events tscharts' \
  | gzip \
  | aws s3 cp - "${sql_dest}.partial"
sql_status=("${PIPESTATUS[@]}")
publish_stream "$sql_dest" "${sql_status[@]}"
echo "Uploaded database dump"

# Paths relative to the volume root, one per line. This does not read
# file contents. nginx:alpine supplies find/tar; the caller never opens
# the root-owned volume directory on the host.
list_image_files() {
  docker run --rm --entrypoint find \
    -v "${IMAGE_VOLUME}:/images:ro" \
    nginx:alpine \
    /images -type f \
    | sed 's|^/images/||' \
    | LC_ALL=C sort -u
}

TOC="$DOCKER_DIR/image-backup.toc"
TOC_S3="$S3_PREFIX/tscharts-images.toc"
CURRENT="$WORKDIR/images.current"
PREV="$WORKDIR/images.prev"
list_image_files > "$CURRENT"

if [[ -s "$TOC" ]]; then
  LC_ALL=C sort -u "$TOC" > "$PREV"
elif aws s3 cp "$TOC_S3" "$PREV"; then
  LC_ALL=C sort -u "$PREV" -o "$PREV"
  echo "Loaded image manifest from S3"
else
  : > "$PREV"
  echo "No image manifest; full image backup"
fi

DELETED="$WORKDIR/images.deleted"
NEW="$WORKDIR/images.new"
comm -23 "$PREV" "$CURRENT" > "$DELETED"
comm -13 "$PREV" "$CURRENT" > "$NEW"

KIND=""
LIST=""
if [[ -s "$DELETED" ]]; then
  KIND=full
  LIST="$CURRENT"
  echo "Image files removed ($(wc -l < "$DELETED")); full image backup"
elif [[ ! -s "$PREV" ]]; then
  KIND=full
  LIST="$CURRENT"
  echo "Full image backup ($(wc -l < "$CURRENT") files)"
elif [[ -s "$NEW" ]]; then
  KIND=incr
  LIST="$NEW"
  echo "Incremental image backup ($(wc -l < "$NEW") new files)"
else
  echo "No image changes"
fi

if [[ -n "$KIND" && -s "$LIST" ]]; then
  image_dest="$S3_PREFIX/tscharts-images-$STAMP-$KIND.tar.gz"
  docker run --rm --entrypoint tar \
    -v "${IMAGE_VOLUME}:/images:ro" \
    -v "$LIST:/filelist:ro" \
    nginx:alpine \
    -C /images -czf - -T /filelist \
    | aws s3 cp - "${image_dest}.partial"
  image_status=("${PIPESTATUS[@]}")
  publish_stream "$image_dest" "${image_status[@]}"
  echo "Uploaded image tarball"
elif [[ -n "$KIND" ]]; then
  echo "No image files remain"
fi

if [[ -n "$KIND" ]]; then
  # CURRENT is every path stored by the latest full archive plus later
  # incrementals. Record it only after the tarball upload succeeds.
  aws s3 cp "$CURRENT" "$TOC_S3"
  cp "$CURRENT" "$TOC"
  echo "Updated image manifest ($(wc -l < "$TOC") files)"
fi

echo "=== Backup $STAMP finished $(date -Is) ==="

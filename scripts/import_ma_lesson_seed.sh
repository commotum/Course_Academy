#!/usr/bin/env bash
set -euo pipefail

: "${EDB_POSTGRES_URL:?Set EDB_POSTGRES_URL to the EDB peer PostgreSQL connection.}"
edb_bin="${EDB_BIN:-/home/jake/Developer/EDB/target/release/edb}"
database="${EDB_DATABASE:-course-academy-v2}"
endpoint="${EDB_ENDPOINT:-/tmp/course-academy-edb-v2/writer.sock}"
root="$(cd "$(dirname "$0")/.." && pwd)"
input_dir="$root/.local/edb/lesson-seed"
report_dir="$root/.local/edb/lesson-reports"
mkdir -p "$report_dir"

for file in "$input_dir"/lessons-*.edn; do
    base="$(basename "$file" .edn)"
    digest="$(sha256sum "$file")"
    digest="${digest%% *}"
    printf '%s\n' "Submitting $base"
    "$edb_bin" transact --database "$database" --endpoint "$endpoint" \
        --request-key "course-academy-${base}-${digest}" --timeout-ms 180000 \
        --file "$file" > "$report_dir/${base}-${digest}.edn"
done

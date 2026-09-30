#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
edb_root="${EDB_ROOT:-/home/jake/Developer/EDB}"
pg_ctl="${PG_CTL:-/usr/local/MATLAB/R2025b/sys/postgresql/glnxa64/PostgreSQL/bin/pg_ctl}"
data_dir="$root/.local/edb/postgres"
run_dir="$root/.local/edb/run"
database="${EDB_DATABASE:-course-academy-v2}"
endpoint="${EDB_ENDPOINT:-/tmp/course-academy-edb-v2/writer.sock}"
endpoint_dir="$(dirname "$endpoint")"

if ! "$pg_ctl" -D "$data_dir" status >/dev/null 2>&1; then
    "$pg_ctl" -D "$data_dir" -l "$root/.local/edb/postgres.log" start
fi

shopt -s nullglob
libraries=("$edb_root"/target/release/deps/libedb_core-*.rlib)
if ((${#libraries[@]} != 1)); then
    echo "Expected one release edb_core library under $edb_root/target/release/deps" >&2
    exit 1
fi
rustc --edition=2024 "$root/engine/edb/transactor.rs" \
    --extern "edb_core=${libraries[0]}" \
    -L "dependency=$edb_root/target/release/deps" \
    -o "$root/.local/edb/course-academy-transactor"

mkdir -p "$endpoint_dir"
chmod 700 "$endpoint_dir"
export EDB_POSTGRES_URL="host=$run_dir dbname=course_academy user=edb_writer sslmode=disable"
exec "$root/.local/edb/course-academy-transactor" "$database" "$endpoint"

#!/usr/bin/env bash
# Compile the smoke test outside both repositories; no PostgreSQL connection.
set -euo pipefail

schema_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
edb_root="${EDB_ROOT:-/home/jake/Developer/EDB}"
rlib="${EDB_RLIB:-}"
if [[ -z "$rlib" ]]; then
  shopt -s nullglob
  candidates=("$edb_root"/target/release/deps/libedb_core-*.rlib)
  if (( ${#candidates[@]} != 1 )); then
    printf 'Expected one built release edb_core library; found %s. Set EDB_RLIB explicitly.\n' "${#candidates[@]}" >&2
    exit 1
  fi
  rlib="${candidates[0]}"
fi
if [[ ! -f "$rlib" ]]; then
  printf 'EDB library does not exist: %s\n' "$rlib" >&2
  exit 1
fi

build_dir="$(mktemp -d /tmp/course-academy-schema.XXXXXXXX)"
trap 'rm -rf -- "$build_dir"' EXIT
rustc --edition=2024 "$schema_dir/validate.rs" \
  --extern "edb_core=$rlib" \
  -L "dependency=$(dirname -- "$rlib")" \
  -o "$build_dir/validate"
"$build_dir/validate" "${1:-$schema_dir}"

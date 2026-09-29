#!/usr/bin/env bash
# Exercise the Rust engine against the sibling EDB repository's native build.
set -euo pipefail
cd "$(dirname "$0")/.."
edb_root="${EDB_ROOT:-../EDB}"
edb_deps="$edb_root/target/release/deps"
mapfile -t edb_libraries < <(compgen -G "$edb_deps/libedb_core-*.rlib")
if [ "${#edb_libraries[@]}" -ne 1 ]; then
  echo "Expected one release edb_core library in $edb_deps; build EDB first or set EDB_ROOT." >&2
  exit 1
fi
cargo build --offline
check_binary="$(mktemp /tmp/course-academy-edb-check.XXXXXX)"
trap 'rm -f "$check_binary"' EXIT
rustc --edition=2024 tests/validate_fire_schema.rs \
  --extern "edb_core=${edb_libraries[0]}" \
  --extern course_academy_engine=target/debug/libcourse_academy_engine.rlib \
  -L "dependency=$edb_deps" -L dependency=target/debug/deps \
  -o "$check_binary"
"$check_binary"

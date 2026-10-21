#!/usr/bin/env bash
# Build the writer from current EDB source before installing or restarting it.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
edb_root="${EDB_ROOT:-$root/../EDB}"
output="${1:-$root/.local/edb-build/course-academy-transactor}"
if [ "$#" -gt 1 ]; then
  echo "usage: build_local_edb_writer.sh [OUTPUT]" >&2
  exit 2
fi

# A newer transactor source or binary does not imply that its statically linked
# EDB library includes the latest fixes. Always let Cargo check that dependency.
cargo build --manifest-path "$edb_root/Cargo.toml" --target-dir "$edb_root/target" \
  --release --lib --offline --locked
edb_deps="$edb_root/target/release/deps"
mapfile -t edb_libraries < <(compgen -G "$edb_deps/libedb_core-*.rlib")
if [ "${#edb_libraries[@]}" -ne 1 ]; then
  echo "Expected one release edb_core library in $edb_deps." >&2
  exit 1
fi

mkdir -p "$(dirname "$output")"
staging="$(mktemp "$output.tmp.XXXXXX")"
trap 'rm -f "$staging"' EXIT
rustc --edition=2024 -O "$root/engine/edb/transactor.rs" \
  --extern "edb_core=${edb_libraries[0]}" \
  -L "dependency=$edb_deps" -o "$staging"
chmod 755 "$staging"
mv -f "$staging" "$output"
echo "Built $output"

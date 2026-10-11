#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
exec /usr/bin/python3 "$root/scripts/run_local_edb_service.py" "$@"

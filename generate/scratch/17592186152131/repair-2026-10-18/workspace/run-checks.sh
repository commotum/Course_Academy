#!/usr/bin/env bash
# Current author validation; prior pass commands/results remain in evidence/commands.md.
set -euo pipefail
exec bash "$(dirname "$0")/run-repair-checks.sh"

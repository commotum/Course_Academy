# Course Academy

Our FIRe implementation is in [engine/rust](engine/rust/). It combines the
published mechanisms with configurable policies chosen for Course Academy.
The goal is a reliable engine of our own, informed by the available evidence;
matching Math Academy's private numerical values is not a requirement.
Start with the [research and implementation report](reference/fire-reconstruction.md),
[history verification](reference/fire-history-analysis.md), and
[data model](reference/fire-data-model.md).

```bash
cargo run -- demo
cargo test
# Optional comparison against the preserved Python implementation:
cargo build
PYTHONDONTWRITEBYTECODE=1 python3 tests/rust_parity.py
# Native EDB boundary (requires the sibling EDB release build):
bash tests/check_rust_edb.sh
```

The Rust library and `fire` binary run without Python. The original Python files
remain as the reference implementation used by differential tests. See the
[Rust API and commands](engine/rust/README.md).

The [schema index](schema/README.md) groups curriculum and learner data separately
from instructional content. FIRe policy settings are in
[schema/engine](schema/engine/). The [reference index](reference/README.md)
links the earlier research and source material.

# Rank from column counts

Use `17592186119847.py --difficulty easy --count 5 --seed 0 --format json` with the pinned interpreter/dependencies. The package contains only the entry point, source data and requirements. No assets or external runtime files are required.

Finite semantic capacity: easy 12; moderate 91. Requests above the capacity or below zero fail explicitly with a nonzero exit and no JSON. Returned batches contain exactly the requested number of distinct semantic tasks. Hard is unsupported. Source replay is available through `generate(..., parameters=..., bank_profile=...)`.

The current repair is described in `../instructional-account.md`; validation starts with `../check_repair.py`, then `../check_variation.py` after the documented delivery commands, and `../check_inventory.py`. The old validate.py/replenish.py and historical reports remain as provenance; they are outside the package and are superseded for this repair. Do not use the historical publication workflow.

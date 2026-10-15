# Matrix-column generator

Run `.venv/bin/python generate/scratch/17592186100866/validate.py` for exact rendered-math, source-bank and native learner-grading validation. Run `.venv/bin/python generate/scratch/17592186100866.py --difficulty easy --seed 3 --count 2` for JSON previews. Unsupported levels raise an explicit error.

The scoped `replenish.py` checks the native learner pool and independently validates available source records, excludes incomplete records, and adds only a supported shortage. It registers the stable generator UUID and repository-relative path, serializes the entire durable workflow with application api.lock and retains exact requests, previews, receipts, attribution and exact-basis readback in reference/replenishment. It never repairs source content or modifies learner history.

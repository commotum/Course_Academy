# Two-point parallel-line generator

Run `python3 generate/scratch/17592186175911.py --difficulty easy --count 5 --seed 1946 --format json` (or moderate / markdown). The CLI uses the repository virtual environment if SymPy is missing. Hard is explicitly unsupported. Generation never accesses EDB.

`validate.py` exhaustively checks all bounded instances, replays both original prompts and field layouts, and tests canonical/equivalent and wrong answers through the real application grader. Source keys, solutions and difficulty labels are missing; all additions are explicitly authored. `review.md` presents original-parameter replays and variants for side-by-side inspection. `capabilities.json` records finite domains and the unfilled hard reserve.

`replenish.py` uses the existing Database adapter, native inventory reader and deployed validation preview. It locks the application's api.lock, rechecks fresh basis/lineage and source evidence, deduplicates whole mathematical lines, saves complete requests, submits guarded additive transactions with the configured application contributor, verifies exact-basis readback and every datom, and retains receipts. It does not edit original content or learner state. Repeated runs reconcile original requests before preparing new intent. Evidence is under reference/replenishment.

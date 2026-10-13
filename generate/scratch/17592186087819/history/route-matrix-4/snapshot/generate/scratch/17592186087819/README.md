# Matrices for Route Planning

Scratch generator `../17592186087819.py`, through step 7 only. No database/shared-file writes. Source: math basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186087819.py --difficulty all --seed 1 --count 2 --format json
.venv/bin/python generate/scratch/17592186087819/validate.py
```

API: `generate_easy`, `generate_moderate`, `generate_hard`, and `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Explicit parameters must include matrix, holes, row_order and col_order; invalid parameters are rejected without resampling. Source replay calls appear in `source-cases.json`; all original fields/banks are preserved.

Version `route-matrix-4` limits new graphs to at least 3 arrows, with at most 8 for three stations or 10 for four, with at most two routes per directed pair and one self-loop per station. Hard starts from five occupied cells before inserting its queried entries. Exact source replay retains the captured graph, including larger counts. These are narrower authored sampling limits, not claims about the source parameter range. Labels use the installed regular Liberation Serif font to match the source diagrams’ upright Times-style lettering; the font hash and renderer version are included in the plot cache identity.

Source-derived radio templates now default to their complete observed count banks. Hard defaults to `authored_count_window`: five consecutive nonnegative counts beginning at `max(0, correct_sum - 2)`. This preserves five distinct choices without forcing dense diagrams to satisfy omission-bank collisions. `authored_omissions` remains an explicit optional profile where sparse instances exist; `sum_139685` has no sampled variants for that profile under the new limits and reports that limitation immediately.

Previous frozen implementations and evidence are retained in `history/route-matrix-1/` `history/route-matrix-2/`, and `history/route-matrix-3/`. Existing database questions retain their original graphs and answers; this version changes future generated variants.

Seven observed templates; all three levels provided. Hard is authored four-station direct-route counting with independently reordered row/column headings, three unknown counts, and one queried loop. The complete original scalar catalogs remain available as observed replay profiles; their wrong-operation intent is unknown.

Two unrated originals lack correct refs/solutions. Easy assignment and missing solutions are explicitly authored, with correct counts independently read from diagrams. q-319429's B→C prose for a B→B blank is minimally corrected in normal output; `profile='raw_solution_319429'` replays the raw original prose for evidence. `validation.json` separates these cases from exact matched source designations/solutions.

Read `classification.md`, `template-extraction.md`, `plot-extraction.md`, `review.md` and `validation.json`. Review contains every original and at least two clearly labeled rendered variants of every observed template/bank, plus hard and authored normal-bank examples. Native fixture checks use the real `learning::grade_field` in `generate/runs/current/check-engine`. Renderer dependencies are cached read-only; all generated assets are private to this directory. Hashes in `freeze.json` identify the completed implementation/evidence snapshot for parent QA.

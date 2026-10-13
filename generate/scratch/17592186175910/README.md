# Parallel-line equation generator

Run from the repository: `python3 generate/scratch/17592186175910.py --difficulty easy --count 5 --seed 1909 --format json`. The script uses the repository .venv when the invoking Python lacks SymPy. Requirements: SymPy, NumPy, Matplotlib. The package writes local PNG previews only; replenish.py performs the separate validated EDB preparation/commit.

Read classification.md, template-extraction.md, plot-extraction.md, source-replay.json, validation.json and capabilities.json. Two incomplete, unrated sources remain unchanged. Local easy/moderate labels, missing answer keys and solutions are explicitly authored. Hard is unsupported in this bounded package and stays unfilled.

Normal bounded capacity: 36 easy tasks (one is already a source task, so at most 35 new), 182 moderate tasks. These are slope-and-marked-point tuples, not seeds or option orders. Source replay also accepts exactly the two original parameter sets. Original source and canonical tasks are excluded from generated admission. Repeated replenishment must subtract the entire current pool and account for learner exposure/reservations.

Validation exhaustively checks all 218 normal parameter tasks, plus source replays and ten visual previews. Actual native grading includes every radio option and canonical/equivalent/wrong blank entries. review.md places original, replay and variants side by side. source.json/source.edn retain basis 1909 and lineage. All ten proposed PNGs were visually checked and hashes retained in plot-review.json.

reference/replenishment stores exact EDN, contributor, basis/lineage, native preview, request journal, receipt and readback. replenish.py holds the application api.lock through inventory recheck, guarded submission and readback, and admits only reviewed previews for this job. New inventory is not learner exposure. Only new answer/field/question entities, membership additions, and this KP's generator registration are authorized.

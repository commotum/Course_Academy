All commands run from this evidence directory. They write review output here and do not publish or access the database.

- Generate source replays, seeded samples, counterfactuals and tests: `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review.py`
- Recheck saved mathematical records: `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python recheck.py`
- Run the retained strict failing case: `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine minimal-grader-input.json minimal-grader-result.json`
- Run its controls: `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine minimal-grader-controls-input.json minimal-grader-controls-result.json`
- Run the remaining main grader cases: `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-followup-input.json grader-followup-results.json`
- Probe conditional cues: `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python shortcut-followup.py`
- Delivery: `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../outputs-0 --math-root /media/jake/SSD/EDB/math`
- Independent delivery uses `samples-easy.json`, output `delivery-independent`, asset root `assets`, otherwise the same flags.
- Batch rendering: `PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root assets --asset-root ../outputs-0 --math-root /media/jake/SSD/EDB/math` (default six cases, including all five batch records).
- Controlled-pair rendering: same renderer, `--input counterfactual-records.json --output render-counterfactual --limit 10 --asset-root assets`.
- Hard/supplementary source rendering: same renderer, `--input render-hard-records.json --output render-hard --limit 5`.

The review-only ANTLR parser dependency is pinned under `review-deps` (4.11.1); package runtime dependencies were not modified. The initial independent TeX parser needed explicit pi constants and multiplication boundaries; the corrected parser is in review.py. Earlier parsing failures were reviewer-tool issues, not attributed to the generator. Final math-results.json contains no failures.

The grader stops at the first unexpected result and does not emit a result JSON on that failure. minimal-grader-execution.json preserves its exit code and exact stderr; the strict expected-accepted input remains unchanged. Controls are a separate invocation. The general exp notation failure is narrowed to the demonstrated fractional-argument cases; integral exp expressions in the main sample pass.

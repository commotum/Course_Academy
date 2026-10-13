# Identifying a Line Given a Graph

Generator `../17592186054802.py`, UUID `b429cfa3-b141-58ec-8aa2-78825cd36898`, is validated and registered for hard questions. Both source radio profiles replay their complete five-choice banks, prompts, and worked solutions, with one documented coefficient correction. The validation covers all 36 bounded profile combinations, 35 distinct graph lines, and actual learner grading: 36 correct selections accepted, 144 distractors rejected, zero unresolved checks.

```bash
python3 generate/scratch/17592186054802.py --difficulty hard --count 5 --seed 42 --format json
.venv/bin/python generate/scratch/17592186054802/validate.py
```

The generator uses the repository's Python environment automatically when required dependencies are missing from the invoking interpreter. Seeds select distinct mathematical lines within the batch; seeds and choice order do not define new content. Inventory replenishment must exclude every existing source/generated line and preserve source identities and learner history. The standalone CLI emits local previews; it does not commit to EDB.

At basis 2060, the inventory had two available hard questions. Three distinct generated hard questions were committed and read back at basis 2061, bringing availability to five. The application lock covered the fresh inventory check, basis-guarded submission and readback. Attribution is `:application/ca-engine`. All four practice source questions and the canonical example are unchanged; receipt datoms contain only permitted additive content and generator-registration facts. Exact request, preview, receipt, asset hashes and verification are retained in `reference/replenishment/basis-2060/`.

Easy and moderate remain unsupported bounded capability exceptions, each with a nominal shortage of five. The two unrated checkbox source questions remain unchanged and excluded from rated inventory. These exceptions limit the present implementation; they do not prove those bands impossible. See `classification.md`, `template-extraction.md`, `plot-extraction.md` and `capabilities.json` for evidence and constraints.

Six newly published assets passed hash readback and visual inspection, including all prompt/solution graphs for the committed instances. `validation.json` records source and boundary-graph review; `reference/replenishment/basis-2060/verification.json` records the exact database result.

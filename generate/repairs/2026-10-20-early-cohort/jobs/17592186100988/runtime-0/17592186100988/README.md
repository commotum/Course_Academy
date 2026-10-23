# Rectangular matrix entry lookup

Current generator and evidence use frozen math basis1356. Seven raw source profiles preserve all27 values,5 available correct references/solutions, and both unrated missing references/solutions/labels. Complete authored indexing-error banks supply normal practice, including both existing-entry and one-index-overflow No such entry radios at easy. Normal blanks and moderate/hard scans remain numeric and in bounds. Moderate/hard are authored larger visual scans, same row-column lookup, with no arithmetic added.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186100988/validate.py
.venv/bin/python generate/scratch/17592186100988.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186100988.py --difficulty easy --profile raw:q-13496 --format json
```

Public API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None), plus generate_easy/moderate/hard. Parameters contain matrix (integer row arrays),i,j,letter, and external scalar slots for raw profiles. See source-cases.json for reproducible original calls. Raw and completed profiles are evidence-only; correct refs remain absent in unrated raw records.

Authoritative current artifacts: source/topic/lesson.json, classification.md, template-extraction.md, source-questions.md, source-cases.json, source-replay.json, plot-extraction.md, validate.py, validation.json, native-input/grading.json, review.json/md, capabilities.json and cli-preview.json. Other files retained from the previous package are historical, including source.edn and the private engine copy; they are not current validation evidence. Validation uses the shared frozen run check-engine binary and performs no DB reads/writes. Stops after step7.

The easy no-entry family exposes26 meaningful tasks, both overflow directions, and a full four-cell indexing-error bank. Its template is inline_no_entry_radio and bank profile overflow_locations. Exactly one index is its dimension plus1; the other is in range. Validation enumerates and natively grades every one of these26 tasks, in addition to source/default checks.

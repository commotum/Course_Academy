# Arc-length integral setup generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186119743/validate.py
.venv/bin/python generate/scratch/17592186119743.py --difficulty all --seed 42 --count 2 --format json
```

API: generate_easy/moderate/hard; generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). `authored_method` is default; `observed:<template>` selects a complete explicit source replay profile; q33728 additionally offers `observed:trig2:legacy`. Exact complete parameter dictionaries are validated, never silently resampled. All layouts are five-option radios.

Eight practice questions, eight active banks plus one legacy bank, 45 complete displayed values; eight original correct refs available, one legacy designation unavailable. Normal presentation repairs q33857's incorrect generic integral bounds and q33728's duplicate legacy field. Missing hard is explicitly authored within vector differentiation, magnitude simplification and integral setup; no integration is performed. Observed underdetermined distractor intent remains a documented limitation of explicit replay profiles, not inferred default pedagogy.

Evidence: source.json and original-widget.json are raw provenance; classification/template/plot extraction explain scope; source-cases and bank-mapping retain all banks; validate.py independently parses displayed prompts, derivative/norm stages and complete integral choices then calls the real native grader; validation.json reports denominators; review.md/review.json show originals, every bank and generated peers. Local plots are parameter-dependent Matplotlib PNGs with sidecars. Stop after step 7; no EDB mutation, registration or shared edits.

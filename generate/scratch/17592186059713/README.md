# Alternative vector-notation generator

Local steps 3–7 artifact for KP 17592186059713, frozen math basis 1356. No database writes, registration, engine edits or commits. Script: `../17592186059713.py`.

```sh
.venv/bin/python generate/scratch/17592186059713.py --difficulty all --seed 27 --count 2 --format json
.venv/bin/python generate/scratch/17592186059713.py --difficulty easy --template scalar --profile raw-q-1386 --format markdown
.venv/bin/python generate/scratch/17592186059713/validate.py
```

Python API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individually documented `generate_easy`, `generate_moderate`, `generate_hard`. Explicit input errors fail without changing inputs. Example `generate_moderate(parameters={'a':[2,-3], 'b':[4,5], 'p':2, 'q':3, 's':-1})`. Supported type is radio; raw fieldless evidence intentionally omits fields. Parameters and profiles are author metadata, outside learner content.

Six rendering masks, three observed mathematical families. Normal easy samples both observed sum masks, subtraction and scalar multiplication; five complete choices follow defensible component-operation banks. Moderate and hard are authored missing-level scalar-combination extensions within the same 2D component method. All arithmetic is exact, all banks reject collisions as a whole, seed/order do not affect content identity, and fingerprints do not count letter-case/profile aliases as separate mathematical tasks.

Public `raw-q-1300`, `raw-q-1324`, `raw-q-1323`, `raw-q-1386` profiles replay original omissions. They are evidence-only, not eligible for learner practice. The q-1323 complete historical bank contains unresolved error intent; its opaque parameterized selectors remain evidence-only. Default subtraction uses a separate authored operation bank. Normal arrow syntax for historical forms is normalized to the actually observed overset-arrow notation.

Read `classification.md`, `template-extraction.md`, `plot-extraction.md`, `source-cases.json`, `review.md`/`review.json`, `raw-replay.json`, `validation.json` and `native-report.json`. `source.json` is the unchanged capture. Originals and completed originals are labeled separately in review; generated examples cover every observed bank and at least two examples per level. `native-input.json` records all native fixture inputs for audit.

Validation currently checks 4/4 original prompts, 2/2 exact available solutions, 2/2 full banks and 10/10 displayed values; missing captured correct refs are reported as 0/0 matched, 2 missing. All four raw originals are ungradeable due to omissions. Four completed originals plus 1,200 generated records are independently checked and natively graded: 1,204 accepted correct selections, 4,816 rejected wrong selections, no unresolved native checks. Runtime: Python 3.13.5, SymPy 1.14.0. Matplotlib 3.11.2 installed; no generated assessed plots. The canonical raster was inspected at full resolution for context.

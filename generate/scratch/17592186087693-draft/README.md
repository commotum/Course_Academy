# Private all-level matrix dimensions draft

Verify from repository root:

```sh
.venv/bin/python generate/scratch/17592186087693-draft/validate.py
.venv/bin/python generate/scratch/17592186087693-draft.py --difficulty all --seed 20 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186087693-draft/render_qa.py
```

API: `generate`, `generate_easy`, `generate_moderate`, `generate_hard`; `level, seed, template, field_type, parameters, profile` are supported. Raw evidence replay uses source-cases.json parameters and explicit observed profiles. Raw legacy missing attributes remain absent and those cases have no grading designation. Every observed profile is evidence-only; normal defaults use full method-derived banks and source-shaped prompts.

Easy 25, authored moderate 60, authored hard 36 meaningful ordered-count tasks: finite total 121. Moderate extends exactly one unlabelled count beyond six; hard extends both. Both remain pure row/column counting. Labels are design claims, not recovered MA classifications. Normal output cannot assess element values, index notation, one-row/column matrices, operations or matrix selection from descriptions. Hard and moderate use single-digit cells and display math, maximum 12×12; typesetting QA checks extrema separately from mathematical and native checks.

Source provenance is database math at basis 1356. Review includes eight raw original replays, every observed bank's changed-count evidence variant, and two authored examples per level. Validation exhausts all 121 shapes in both field layouts; native grades correct/wrong choices and canonical/equivalent/wrong blank entries. Raw source bank fidelity, mathematical correctness, native grading and authored difficulty rationale are distinct results.

This is private local review code. It never replaces or registers the external workflow's easy-only 17592186087693.py. No database writes or shared engine changes.

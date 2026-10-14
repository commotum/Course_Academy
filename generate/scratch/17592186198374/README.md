# Inferred-integrand change-of-variables generator

The current package is version `integrand-transform-2`. Registered identity:
`8e0d6a8f-d53a-5c00-b25f-e055df31cb01`, script
`generate/scratch/17592186198374.py`. Easy and hard are supported; moderate raises
a bounded capability error. `--difficulty all` emits only supported levels.

```bash
.venv/bin/python generate/scratch/17592186198374.py --difficulty easy --count 5 --seed 12000 --format json
.venv/bin/python generate/scratch/17592186198374.py --difficulty hard --template rational --seed 713 --format markdown
.venv/bin/python generate/scratch/17592186198374/validate-current.py
.venv/bin/python generate/scratch/17592186198374/replenish.py
```

`generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None)` uses exact matrix, shift, bounds and scale parameters. The normal
`method` profile produces one five-choice scalar radio and one concrete
five-stage solution. Choices are selected as a complete bank, reject on
collisions, and shuffle deterministically. Identities exclude seed and choice
order. Duplicate checks independently compare the actual integrand and region,
excluding field identities, answer banks and solution text.

`classification-current.md`, `template-extraction-current.md`,
`extraction-current.json`, `validation-current.json` and `capabilities.json`
supersede the old basis-1356 difficulty/completeness statements. All 12 current
practice sources are hard; q-160896 now has a complete solution and key. Its
former provisional moderate assignment has been withdrawn. Easy is still an
explicit canonical-example extension. New source backbones/banks outside the
implemented sampler are recorded without claiming fidelity for their variants.
One legacy duplicate-field source remains ungradable and unchanged.

The historical source file and extraction/validation artifacts remain for
provenance. Public `raw:q-...` profiles replay those historical banks and are
always evidence-only, ineligible for learning. Historical replay matches all
35 choices in seven complete banks; unresolved error intentions are retained.
The old `validate.py` remains the historical validator and supplies the shared
rendered-math checks; use `validate-current.py` for current scope.

`reference/replenishment/basis-2287/` retains the exact EDN, guarded request,
speculative preview, confirmed receipt and readback at basis 2288. Five distinct
easy questions were added, with native grading of all choices, content-addressed
Matplotlib diagrams, contributor `:application/ca-engine`, and no source/history
changes. Fresh supply was verified as easy 5 / hard 11. Moderate remains an
explicit nominal shortage of five. The worker holds the shared application
`api.lock` from the current-basis inventory check through submission/readback.
Re-running a saved request recovers the same receipt and verifies its result.

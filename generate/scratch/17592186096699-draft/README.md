# Basis-2275 registered revalidation draft

Only 17592186096699-draft.py and its private evidence are modified. registered-baseline.json records the entire original numeric script/evidence pathset and hashes; validation checks it unchanged. No registration, database writes, engine edits or shared QA edits.

```sh
.venv/bin/python generate/scratch/17592186096699-draft/validate.py
.venv/bin/python generate/scratch/17592186096699-draft.py --difficulty all --count 2 --seed 7 --format markdown
.venv/bin/python generate/scratch/17592186096699-draft.py --difficulty easy --template q-119078 --profile observed_raw --format json
```

API generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus three difficulty wrappers. Original public replay uses observed_raw with {scale:1}; observed_repaired preserves opaque complete banks while making explicitly authored repairs. Both are evidence-only/ineligible. Observed variants use bounded dependent-function rescaling, with no arbitrary bank offsets. Normal defaults choose every supported source-shaped easy/moderate family and authored method-derived banks, with {scale,target} slots; hard uses three familiar primitive components, one initial condition and bounded explicit parameters.

source.json is the exact math basis-2275 wrapper. source-cases.json covers all fourteen MA originals. independent-inventory.json preserves all eight independent records as separately labeled context, not observed MA templates. The validator reads the actual supplied equation, condition, all choices, formal inputs, primitive and evaluation stages, final prose, domains, branches and grading contracts. Mutation controls change math and operative structure while refreshing content hashes. Native memory-only grade_field checks cover every radio option and canonical/equivalent/wrong blank entries. Review and validation separate original fidelity, notation normalization, source errors, authored scope, mathematics, native grading and baseline preservation.

# Gradient-property local generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186124447.py --difficulty all --seed 19 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186124447.py --difficulty moderate --template poly --profile source:q-36144 --parameters '{"x0":0,"y0":0}' --format json
.venv/bin/python generate/scratch/17592186124447/validate.py
.venv/bin/python generate/scratch/17592186124447/write_evidence.py
```

The API exposes generate_easy, generate_moderate, generate_hard and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Each entrypoint is individually documented in the script. Field type is radio. All snapshots use math basis 1356 and captured lineage. This is review JSON, never transaction data.

Eight source-shaped families and eight exact raw banks; four opaque banks remain evidence only. Easy, the additional hard binomial family and the missing q-37466 solution/designation are authored. Normal defaults cover seven moderate families and the observed hard Gaussian family using whole eligible observed or method-derived banks. No plots, database writes, engine modifications, registration or commits.

Read validation.json for separate fidelity, mathematical, stage-mutation, identity, native grading, finite-domain evidence and limitations. Native tests omit the one raw missing-designation fixture while testing its authored normal completion. Exact raw attribute omissions persist through public API and CLI.

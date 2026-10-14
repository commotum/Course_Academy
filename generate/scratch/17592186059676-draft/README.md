# Basis-2275 registered-generator revalidation draft

Only 17592186059676-draft.py and its private evidence folder are modified. registered-baseline.json contains the entire 111-file original numeric script/evidence pathset with SHA-256 values; validation checks exact preservation. No DB writes, registration, engine or shared QA edits.

```sh
.venv/bin/python generate/scratch/17592186059676-draft/validate.py
.venv/bin/python generate/scratch/17592186059676-draft.py --difficulty all --count 2 --seed 7 --format markdown
.venv/bin/python generate/scratch/17592186059676-draft.py --difficulty easy --template q-30990 --profile observed_raw
.venv/bin/python generate/scratch/17592186059676-draft.py --difficulty moderate --template authored-point --field-type blank --parameters '{"a":2,"b":3,"point":0}'
```

JSON CLI output is a list of records; --difficulty all emits easy, moderate and hard records in that order. Public generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None), with easy/moderate/hard wrappers. observed_raw is exact ineligible evidence; source-pattern normal output uses the full original source recipe banks, preserving captured field shapes. Missing-source metadata is an authored repair. authored-method supplies a familiar evaluation-point moderate peer and a same-method four-term hard workload peer. Full bounded banks reject as a whole if ambiguous. Normal defaults cover all nine source families and both authored families.

source.json, topic.json and lesson.json are frozen basis-2275 snapshots. independent-inventory.json holds all three exact independent records with role and relationship_to_source_templates. source-cases.json retains every raw original and explicit full-bank recipe. source-replay.json separates attrs/omissions/raw fidelity from normal math and teaching authorship. The validator reads the actual supplied expression, actual point, full banks, every formal derivative operand, all algebraic/evaluated stages, conclusions, prime input, domains and contracts. Native grade_field checks cover all radio IDs and canonical/equivalent/wrong blank values. Structural mutations deliberately change the actual math/layout/key/domain. Review includes raw originals, normal replays, changed coefficients, point-only changes and a hard instance.

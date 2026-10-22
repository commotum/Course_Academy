# KP 17592186119806 generator

Run from the repository root:

```sh
python3 generate/scratch/17592186119806.py --difficulty easy --count 5 --seed 119806 --format json
.venv/bin/python generate/scratch/17592186119806/validate.py
.venv/bin/python generate/scratch/17592186119806/replenish.py
```

The CLI uses the project's existing .venv if the application interpreter lacks
SymPy. Python/SymPy versions and immutable source basis are saved in generation
metadata. The generator has no database writes. Replenishment validates supplied
instances, rechecks inventory and basis while holding the application's api.lock,
previews original typed EDN with native ensures, saves an exact durable request,
submits with the basis guard, and verifies exact-basis readback and provenance.
Registration alone never certifies arbitrary future generated content.

Read capabilities.json for explicit moderate/hard exceptions and finite capacity.
Review.md shows source and variant presentations for every complete profile.
Only this KP's package and generated content may be changed by this workflow.

# Parametrizing an Elliptic Cylinder

17592186175970.py is the public pure generator. Run with the repository .venv Python:

    .venv/bin/python generate/scratch/17592186175970.py --difficulty easy --count 5 --seed 2690 --format json
    .venv/bin/python generate/scratch/17592186175970/validate.py
    .venv/bin/python generate/scratch/17592186175970/replenish.py

Easy/moderate are supported. Hard remains unfilled. See classification.md,
template-extraction.md and capabilities.json. The replenisher uses the configured
EDB integration, native inventory and grader, additive validated transactions,
application api.lock, basis guard, exact retained requests and receipt readback.
It never repairs source questions or changes learner state.

# Origin-centered circular polar setups

Run `.venv/bin/python generate/scratch/17592186129199/validate.py` from the repository root. Preview: `.venv/bin/python generate/scratch/17592186129199.py --difficulty all --seed 3 --count 2 --format json`.

The public API is generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Parameters are {radius_squared: 2..36 integer, rotation: 0..3 integer}; full disks require rotation 0. Source replay uses every entry in source-cases.json and profile q-ID. Missing source keys/labels/solutions and authored hard scope are documented. Math fields have five complete integral choices and owned UUID answers.

Normal responses require the actual D, pointwise transformed integrand and Jacobian with nonnegative r. Incidental equal scalar values are reported separately in bank-collisions.json. Native grader checks radio selections; independent displayed-math checks establish setup validity. No integral evaluation, shifted circle, changing radial boundary, EDB transaction, registration or shared edit occurs.

See classification.md, template-extraction.md and plot-extraction.md for exact source/extension boundaries, review.md/review.json for originals and every template’s variants, validation.json and native-report.json for verified counts, and freeze-hashes.json for the frozen artifact hashes.

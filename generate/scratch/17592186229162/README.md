# KP17592186229162 scratch generator

Nonresonant one/two-term exponential trial particular solutions. Basis1356. No database writes.

```sh
.venv/bin/python generate/scratch/17592186229162/validate.py
.venv/bin/python generate/scratch/17592186229162.py --difficulty all --count 2 --seed 53 --format json
.venv/bin/python generate/scratch/17592186229162.py --difficulty easy --profile q-332393
```

The validator independently reads printed ODEs and every trial/derivative/substitution/distribution/collection/coefficient/final stage, compares exact complete sources, checks scope guards and content identity, and invokes the application's native grader. Review artifacts contain every raw original, each supported normal presentation and generated examples of all six presentation families plus two per level.

Eight complete source banks match exactly. Two unrated source blanks lack keys/solutions/levels: raw profiles preserve missing fields, normal output adds independently derived values and authored easy labels. Normal output also clarifies the requested trial span. The unrestricted raw source request admits homogeneous additions that the fixed-answer grader rejects; engine evidence records this limitation honestly. No resonance, general solution, or IVP tasks are generated.

Hard instances retain primitive whole-ODE leading coefficient a/gcd(a,b,*c)>=4, as well as two nonintegral normalized forcing coefficients; a common scaling cannot turn moderate work into hard. The validator checks this from actual printed equations and includes two explicit rejection controls.

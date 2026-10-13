Local step 3–7 draft for **The Cartesian Equation of an Ellipse** (KP17592186152188). No registration or database writes.

Verify with `.venv/bin/python generate/scratch/17592186152188/validate.py`.
Preview with `.venv/bin/python generate/scratch/17592186152188.py --difficulty all --seed 17 --count 2 --format markdown` (or `json`). API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Parameters are exact strings `a,b,h,k`. `source-cases.json` supplies public original-profile replays.

Original profiles `observed:q-ID` preserve all source strings and banks. Opaque hard banks and the original q-327811 parameter mismatch are explicitly evidence-only. Normal source families use defensible source method banks, while q-79375/q-79377 use separately authored complete method banks and q-327811 normalizes its parameter to theta. All source families participate in default sampling.

Easy is authored: isolation is supplied, leaving squaring and the Pythagorean identity. Moderate isolates trigonometric functions in origin equations; hard additionally removes nonzero translations in both equations. No interval elimination, traversal, graph reconstruction, rotated conics, hyperbolas, or sibling-KP material is introduced. No raster references exist in the 15 practice questions, canonical example, or any choice/solution; plotting is not required.

`review.md` labels every original and two generated examples of every mask. `validation.json` separates exact fidelity, printed-stage mathematical validation and native grading. `freeze.json` records actual Python/SymPy and artifact hashes. Historical distractor intentions for q-79375/q-79377 remain unresolved, with raw banks preserved and excluded from learning defaults.

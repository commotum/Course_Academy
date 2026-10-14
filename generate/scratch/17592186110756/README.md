# Unit-circle reciprocal generator

`../17592186110756.py` emits JSON practice records for **Moderate** only:

```sh
.venv/bin/python generate/scratch/17592186110756.py \
  --difficulty moderate --count 5 --seed 20261014 --format json
```

Use `--template` to select one of the five observed bank profiles. The default
samples profiles and removes repeated mathematical tasks across banks. Seeds
control sampling; UUIDs derive from exact mathematical content and a complete
bank profile, never from seeds or option order. Inventory deduplication uses the
supplied coordinate, its x/y role, requested ratio and first quadrant; it ignores
bank profile and representation changes. Finite domains and collision exclusions
are recorded in slot-coverage.json. Requests beyond distinct capacity fail
explicitly rather than pad with repeats.

The current bounded domain uses b=3..8, known=sqrt(r)/b, r=1 for rational input
and non-square 2<=r<b² for radical input. The complementary coordinate must
remain irrational, so all supported instances retain the rationalization stage.
The source value and requested complement are linked: y implies sec; x implies
csc. Changing theta's name or P's name establishes no new mathematical task.

Python, SymPy, NumPy and Matplotlib are required. Exact validation checks all
finite domain banks and rendered endpoint/interior cases per profile. Actual
radio grading uses the existing engine through check-engine.rs. Run:

```sh
.venv/bin/python generate/scratch/17592186110756/validate.py
```

`source.json` retains all six source questions, the canonical example, lineage,
and classification basis. `template-extraction.json` maps every choice of the
five complete source banks. Cognitive interpretations of arbitrary observed
number/radicand patterns remain unresolved; those expressions are preserved as
recipes, not explained as invented misconceptions. The unrated incomplete sixth
source remains unchanged and is excluded. Easy/Hard are not supported by this
validated package; exceptions and shortages are explicit in capabilities.json.
New complete source evidence may reopen classification.

Source and generated figures were inspected side by side in source-plots.png,
generated-plots-review.png and review.md. All axes, first-quadrant branch,
coordinate/ratio roles and ordered solution stages agree. Generated diagrams
use exact sampled coordinates rather than recycling approximate source positions.
Layout fidelity is separate from mathematical bank fidelity: captured Unicode
function rendering is normalized to standard LaTeX, and the long solution point
label is placed above the square plot to prevent clipping.

`replenish.py` rechecks current stock, validates supplied instances if present,
and produces only shortages at supported bands. It preserves source questions,
canonical example, history and all unrelated facts. The configured application
contributor owns the registration and new content. The application api.lock is
held through preparation, basis-guarded submission and exact receipt readback.
Exact EDN, source, request key, lineage, expected basis, UUIDs, connection hash,
preview, receipt and verification are retained under reference/replenishment.
Accepted assets use the existing ImageLibrary content-addressed store. Recovery
uses the original request key and body, then repeats verification. No automatic
process modifies unrelated generators, scheduling or application code.

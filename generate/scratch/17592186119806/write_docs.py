"""Persist classification/extraction evidence for this KP only."""
import importlib.util,json
from collections import defaultdict
from pathlib import Path
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
groups=defaultdict(list)
for sid in g.CASES:groups[g.template_id(sid)].append(sid)
text=f'''# Classification — Solving for a Vector in a Linear Combination

Database math, basis {g.SOURCE['basis']}, lineage {g.SOURCE['lineage']}. `source.json`
and `reference/source.edn` retain all 14 practice questions and the canonical example.
The 13 complete rated questions are easy, each with one radio field named
`selection`, five mathematical choices, and a field-owned correct designation.
There are {len(groups)} Markdown/solution/response backbones and 13 complete bank
profiles. Dimension and signed/reversed isolation stages remain separate because
they affect component work and ordered presentation. Component target locations
are eligible slots within a sum or difference backbone.

| Difficulty | Complete sources | Fields | Templates | Plot rating |
|---|---:|---|---:|---|
| Easy | 13 | One radio field; vector or scalar value | {len(groups)} | None for every template |
| Moderate | 0 | Unevidenced | 0 | Unevidenced |
| Hard | 0 | Unevidenced | 0 | Unevidenced |

Source `q-34574` is unrated, lacks a correct designation and worked solution,
and cannot contribute to inventory. Its equation would give x=(-2,1,4,2),
with x1+x2=-1, but no repair or difficulty classification is made to the source.
The canonical example is teaching evidence, not available practice. Its SVG
is standalone MathJax vector notation rather than a mathematical diagram.

'''
for name,sids in groups.items():text+='- '+name+': '+', '.join(sids)+'; plot none.\n'
text+='\nModerate/hard are bounded unsupported capabilities in this package. Their nominal\nfive-question shortages remain explicit; new source evidence reopens classification.\n'
(H/'classification.md').write_text(text)
doc='''# Template extraction

Solve p*a+c*x=b using componentwise scalar multiplication, subtraction, and
division by nonzero c. The supplied objects are a and b; x is the requested
vector, or its two named components are combined by the observed sum/difference.
The vector dimension, coefficient pair, operation, response shape, radio contract,
and ordered symbolic isolation stages remain fixed within each source profile.
Positive, signed-negative, and reverse-subtraction isolation presentations are
preserved rather than collapsed into a new solution sequence.

Observed profiles are enumerated below; original prompt, solution, field, and
every original option remain in source.json. choice-recipes.json maps every
choice to its source field, UUID, exact value, and complete observed offset recipe.
No profiles are pooled. Each profile must reproduce all five choices and the
correct designation at its original parameters.

Variable slots:

- `scale` is the uniform integer dilation k in {1,2,3} applied to a and b.
  x=(b-p*a)/c is computed first. Every supplied, intermediate, solved and choice
  vector changes coherently; integrality and source sign/zero patterns survive.
  k=1 replays the source. k=2,3 are conservative same-method generalizations.
  The upper bound keeps the same small-integer component workload; larger
  numbers are excluded by policy, not asserted mathematically impossible.
- `target` is absent for vector answers. For scalar answers it selects any two
  distinct eligible coordinates using the source operation. Sum pairs are
  unordered; difference pairs are ordered. All prompt names, final solution
  names, arithmetic and bank correct values derive from this slot. The number
  of coordinates requested and the full vector-solving stages stay fixed.
  Original target locations are retained for replay; location repetition alone
  is not a constraint. All target slots are covered exhaustively, including a
  changed-target case with all other supplied data held constant.

Bank recipe: requested_value + k*(source_option-source_correct_value).
At the source target this is exactly k*source_option. At another eligible target,
it translates the entire observed offset profile to the new correct value.
This target translation is an authored conservative extension. The underlying
mistake represented by a random-looking source offset is unresolved; no error
intent or feedback is invented. Every option is retained, and no bank mixing
occurs. Nonzero k preserves unique offsets and one correct option.

One concrete source-worded solution is rendered for each instance. All numeric
matrices are derived through the same dilation, and scalar final arithmetic
handles signed terms and parentheses. There are no branch/domain issues: finite
real integer vectors and nonzero scalar coefficients yield a unique x.

Mathematical novelty hashes the displayed supplied coefficients and relevant
coordinate data, with the operation. Scalar-query unused coordinates, target
labels, profile IDs, answer order, UUIDs and seeds cannot create new tasks.
All 156 declared tasks are distinct; 13 are source tasks, leaving 143 bounded
variants before considering learner presentations/reservations.

'''
cases=[]
for sid,old in sorted(g.CASES.items()):
 p,c,a,b,target=g.parse_problem(old[':question/problem']);x=(b-p*a)/c
 case={'source':sid,'template':g.template_id(sid),'profile':sid,'coefficients':[p,c],'a':list(map(int,a)),'b':list(map(int,b)),'x':list(map(int,x)),'dimension':len(a),'target':target,'response':'vector' if target is None else 'scalar','number_features':'exact integral vectors; mixed signs and zero components as observed; nonzero coefficient','original_parameters':{'scale':1,'target':target},'plot_rating':'none'}
 cases.append(case)
 doc+='## '+sid+'\n\n'+json.dumps(case)+'\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\n'
(H/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
(H/'template-extraction.md').write_text(doc)
(H/'plot-extraction.md').write_text('''# Plot extraction

No rated practice question contains plot assets. The canonical example contains
images/8f/8fef8bb1e88ca823b49d8c5544c5456c66b7a5beb0c9bd48f349a50bf3fa17b5.svg,
whose MathJax title/markup encodes a=(12,-11,-5) and b=(24,-9,13).
It is standalone mathematical notation and is not a plot. No generated instance
uses this asset; prompts and choices use delimiter-free LaTeX matrix values.
No plot generator, asset publication, or new raster artwork is required.
''')
(H/'README.md').write_text('''# KP 17592186119806 generator

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
''')

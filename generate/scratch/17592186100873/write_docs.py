"""Write source-backed extraction and bounded capability evidence for this KP."""
import hashlib,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).parent;sys.path.insert(0,str(HERE));import validate as v
g=v.g
rows=[]
for mid,t in g.TEMPLATES.items():
    src=g.SOURCE_BY_ID[mid];A,B=v.matrices(src);_,i,j=v.target(src);f=src[':question/answer-fields'][0]
    rows.append(f"| {mid} / {src[':db/id']} | easy | {t['field_type']} | {len(A[0])} | {len(A)}×{len(A[0])}, {len(B)}×{len(B[0])} | ({i+1},{j+1}) | {len(g.domain(mid))} | none |")
(HERE/'classification.md').write_text(f'''# Finding an Entry of the Product of Two Matrices

Captured math lineage {g.CAPTURE['lineage']}, basis {g.CAPTURE['basis']}.
All twelve practice records and the canonical example were read together.

Easy has ten complete graded sources: six single-field radio questions (five
integer choices) and four single-field integer blanks. Four mathematical/layout
families combine a two- or three-term dot product with radio or blank output.
The source-specific implementations retain each source's notation and layout;
six radio banks remain separate profiles. Blanks have no distractor profile.
Each source asks for one entry, selects one row and column, expands their dot
product, shows integer products, then sums. None requires a new plot.

| Source / db ID | Difficulty | Field | Dot length | Matrix shapes | Observed target | Eligible targets | Plots |
|---|---|---|---|---|---|---|---|
'''+ '\n'.join(rows)+'''

q-70791 and q-70792 are unrated radio records with no correct-answer links or
worked solutions. They are excluded, preserved and not counted as inventory.
They demonstrate the same matrix-entry operation, but cannot establish a new
difficulty. No source practice question is rated Moderate or Hard. Those bands
remain unsupported by this package pending new evidence; Easy is not relabeled.
The canonical example's unchanged matrix image is documented in plot-extraction.md.
''')
(HERE/'template-extraction.md').write_text('''# Source extraction and executable boundaries

`source-components.json` retains every original record, exact parameter matrices,
queried target, source field, answer ID, complete option value, and profile.
`source-fidelity.json` reports ten complete banks, 34/34 values and 24/24
incorrect values matched one-to-one, with correct designations preserved.

The shared backbone is C=AB with signed integer matrices of compatible dimensions;
the supplied objects are two complete matrices, and the requested object is one
entry of their product. A single integer is selected or entered. The solution
states which row and column to multiply, displays the two full matrices, extracts
that row and column, expands their dot product, evaluates each product and sums.
Two- and three-term workloads and radio/blank layouts remain separate families.
Each source keeps its source notation (explicit multiplication dots or implicit
parentheses). Labels, matrices, number forms, operand order, field key/type/count,
choice count, instructional wording and solution stage order stay source-fixed.

The variable slots row and column independently range over all product cells in
each source matrix pair, subject only to a radio-bank collision rejection. This
is a conservative same-method generalization of the observed target, including
rows/columns other than the original position. It preserves signed integer dot
products of the original length, without adding operations or reasoning stages.
Source matrices are a deliberate narrow sampling policy: entry randomization is
unnecessary to provide distinct target tasks and unsupported error interpretations
would not justify inventing more complex numerical policies. Original parameters
are always retained for exact source replay.

For a target (i,j), compute A*B exactly with SymPy, independently cross-check the
sum of selected scalar products, and derive every target subscript, ordinal,
row/column vector, expansion, signed intermediate sum and answer from that target.
Radio banks retain each observed incorrect integer as a fixed literal recipe;
the interpretation of those mistakes is unresolved. The source does not establish
parameter-dependent error formulas, so none are inferred. The selected profile
is chosen before constructing its complete bank. Its correct value becomes the
computed target entry, and targets equal to a fixed incorrect value are rejected.
Every normal bank is therefore one observed source profile with no pooled recipes,
no invented distractors and five unique values. Blanks retain their one canonical
integer and source equation fragment. Original question/field/answer identities
are never used for authored variants.

The exact bank and source solution are replayed only at the observed target and
marked evidence-only. Mathematical and grading checks independently read the
rendered source replay as well as every normal variant. The replay API cannot be
used to admit a source duplicate into inventory. Normal generation can produce
a source target, but preparation excludes every existing source/canonical
fingerprint and every already generated task before adding content.

Only the ordered selected row and column vectors establish mathematical content
identity. Seed, labels, unused matrix entries, IDs, answer-field type and choice
order do not. Full eligible cell enumeration yields 94 source/profile variants,
90 distinct tasks before excluding the current database. Other difficulty levels
and arbitrary matrices are outside this bounded generator. Unsupported shortages
are explicit in capabilities.json and the job result.
''')
asset=Path('/media/jake/SSD/EDB/math/images/c6/c6c7e580cfd96bc23c55742535ceb40a94635c2a44b911e0d08311c3a599c2fa.png')
assert hashlib.sha256(asset.read_bytes()).hexdigest()==asset.stem
(HERE/'plot-extraction.md').write_text('''# Plot/asset extraction

All ten rated practice questions display their matrices in LaTeX. These are
standalone mathematical notation, not plots; no new diagram is needed. Generation
uses LaTeX matrices and introduces no asset references.

The canonical example alone uses the unchanged image
images/c6/c6c7e580cfd96bc23c55742535ceb40a94635c2a44b911e0d08311c3a599c2fa.png.
It was visually inspected at its native 334×74 pixels. It displays A=[[1,2],[-2,0],
[1,2]], B=[[3,4,-1],[1,-2,2]], in black matrix notation on white. The prompt asks
for c32, so its selected vectors [1,2] and [4,-2] have dot product 0. The image
has no geometric relationships, axes or plotted data. Its bytes hash matches its
SHA-256 filename. math_reader.py records this canonical-only transcription to
exclude equivalent generated tasks. The asset and canonical question remain
unchanged. Plot requirements for every family: none; Plot Generator is inapplicable.
''')
validation=json.loads((HERE/'validation.json').read_text())
cap={'knowledge_point':g.KP_ID,'supported':{'easy':{'field_types':['radio','blank'],'mathematical_templates':4,'source_profiles':10,'radio_bank_profiles':6,'source_profile_variants':94,'distinct_task_limit':len(g.candidates('easy')),'bounded_policy':'fixed source operand matrices; all eligible target cells; fixed source incorrect values; collisions rejected'}},'unsupported':{l:{'reason':'No rated source template or validated same-workload difficulty evidence; do not relabel Easy questions','shortage_explicit':5,'reopens_on':'new source or independent difficulty evidence'} for l in ['moderate','hard']},'source_exclusions':g.EXCLUDED,'bank_limit':'Incorrect source integer constants retained verbatim; mistake interpretations unresolved; no parameter-dependent recipes inferred','plots':'none','basis':g.CAPTURE['basis'],'lineage':g.CAPTURE['lineage']}
v.write(HERE/'capabilities.json',cap)
(HERE/'README.md').write_text('''# Finding an Entry of the Product of Two Matrices

`../17592186100873.py` generates bounded Easy matrix-entry questions from fixed
source operand matrices and eligible queried cells. It supports radio and blank
fields. Moderate and Hard remain unsupported, not filled. There are 90 distinct
selected-vector tasks before excluding existing/shown/reserved content.

```
.venv/bin/python generate/scratch/17592186100873/validate.py
.venv/bin/python generate/scratch/17592186100873.py --difficulty easy --count 5 --seed 23 --format json
.venv/bin/python generate/scratch/17592186100873/replenish.py
```

`generate(level, seed=0, template=None, parameters=None, profile=None, replay=False)`
accepts parameters row/column with one-based integer indices, source question ID
as template, and its source-bank profile. `easy`, `candidates`, and Markdown/JSON
CLI previews are available. CLI counts exceeding the finite domain fail explicitly.
Source replays are evidence-only; stable generated UUIDs and field-owned answer
UUIDs never depend on seed or choice order. See classification, template extraction,
complete source-bank mapping, side-by-side review, validation and freeze evidence.

Replenishment rechecks the configured math inventory, native pool and actual grader,
excludes every historical presentation/reservation and current mathematical task,
then adds only the supported shortages. It retains exact basis-guarded EDN and
requests, previews installed specs, commits as :application/ca-engine, and verifies
source records, membership, registered generator and attribution at the receipt
basis while holding the application's api.lock. It touches no learner or engine
facts. Incomplete unrated originals remain explicit and unchanged.
''')

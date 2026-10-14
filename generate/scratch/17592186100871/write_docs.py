import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent));import validate as v
g=v.g;H=v.HERE
cap={'supported_levels':list(g.SUPPORTED),'unsupported_levels':['easy'],'finite_limits':{l:len(g.candidates(l)) for l in g.SUPPORTED},'finite_limit_scope':'Distinct ordered operand dimension triples before existing/shown/reserved exclusions; matrix entries, labels, field shape, seed, identity and choice order do not create variants.','exceptions':[{'level':'easy','scope':g.VERSION,'reason':'No rated easy source is present. Unrated q-22065 lacks correct link and solution. The observed forward templates are moderate; changing incidental entries does not justify reclassifying them easy. New source evidence or a separately validated easy design can reopen this bounded exception.','required_reserve':5,'produced':0,'filled':False},{'source_id':'q-22065','reason':g.EXCLUDED['q-22065']},{'source_id':'q-22067','reason':'Rendered A has four rows and two columns; first solution sentence says 3×2. Source remains unchanged; new source replay corrects that sentence to 4×2; observed bank and correct key already agree with 2×2. This source is excluded from the mathematically validated inventory.'}]}
v.write(H/'capabilities.json',cap)
(H/'classification.md').write_text('''# Matrix-product dimensions classification

Captured math basis '''+str(g.CAPTURE['basis'])+'; lineage '+g.CAPTURE['lineage']+'''. `source.json` and `reference/initial/kp.edn` retain all ten practice sources and canonical evidence in one pull.

| Band | Fields | Backbone templates | Source IDs | Plot rating |
|---|---|---:|---|---|
| Easy | none observed | 0 | no rated source | none |
| Moderate | radio; two blanks | 2 (forward-radio, forward-blank) | q-129492, q-77475, q-77476; q-320351, q-320389 | none |
| Hard | radio; two blanks | 2 (reverse-radio, reverse-blank) | q-22067, q-129489; q-275395, q-320371 | none |
| Unrated | radio, incomplete | excluded | q-22065 | none |

Counting rows/columns, checking inner conformity, and reporting the outer dimensions is the shared method. Hard sources require reversing the order of matrices as supplied. Blanks retain field-1 rows and field-2 columns. Three distinct radio bank patterns are preserved: outer-dimension combinations, inner/outer square combinations, and the reverse rectangular bank. `source-components.json` assigns every supported source and maps every choice to its exact recipe and field; incomplete q-22065 is explicitly excluded.

Matrices rendered as LaTeX or canonical matrix PNGs are standalone mathematical notation, not plots. q-22067 has a recorded source solution typo. No source or learner facts are repaired by replenishment. Easy absence is a bounded package exception, not a claim that the underlying skill admits no easy questions.
''')
(H/'template-extraction.md').write_text('''# Template extraction

Backbone: supply two explicit matrices; ask dimensions of their defined product; count each matrix's rows and columns; compare inner dimensions; state outer rows × columns; display the dimension multiplication diagram. Preserve supplied order, requested order, radio versus two-blank response, source labels, and the complete source-bank profile. Labels and entries are incidental and never count toward diversity.

Slots r,k,c denote the ordered left operand's rows, its columns/shared inner size, and the right operand's columns. Prompt, solution prose, boxed dimension diagram, correct answers and all distractors derive from those slots. Positive integer dimensions ensure finite matrix shapes. Matrix entries need no calculations; deterministic signed integers avoid seed-dependent incidental differences. SymPy computes an exact matrix product to check its shape before authoring answers.

Observed and proposed bounds are separate: `source-components.json` retains each original problem, solution, exact triple, field layouts, options, and full mapped bank. `domain(mid)` exposes conservative dimensions 1–4. Forward moderate radio preserves a square first operand with a nonsquare result, an inner vector product, or an outer vector product. Forward blanks preserve a vector first operand's shared inner dimension 1 with a nonsquare result, or a column-vector second operand. Reverse hard profiles preserve nonvector matrices; square-result profiles use r=c≠k, and reverse rectangular profiles use all distinct r,k,c. Normal parameters enumerate the entire declared finite domain. No undefined-product template is invented; undefined remains a wrong source choice.

Recipes use complete ordered dimensions, rather than multiplication of their numeric entries: correct=(r,c), transpose=(c,r), inner×outer-right=(k,c), outer-right-square=(c,c), outer-left-square=(r,r), outer-left×inner=(r,k), inner×outer-left=(k,r), inner-square=(k,k); undefined is text. Each bank is selected as a complete source profile. Conditions prevent collisions and additional correct options. Blanks contain one field-owned math answer per field.

`source-fidelity.json` records 33/33 complete answer values across nine source banks, including all 20 distractors and correct designations. Source prompts and operative solution wording replay exactly, except the supported q-22067 3×2→4×2 correction. No unmapped supported choices remain. Source q-22065 is missing rating, key and solution and stays unchanged outside supported generation.

Deduplication uses only ordered operand shapes (r,k,c), across bank, field layout and seed. The canonical reverse product has (2,4,2), visually verified from its original matrix assets; exclude it even though it lacks practice fields. Source q-22067 and q-320371 share this same task. Distinctness requires changed supplied operand shapes; changing entries, choice order, identities, labels or seed alone cannot replenish inventory.

`review.md` places every original alongside a dimension-changed variant. Exhaustive validation covers all 51 profile/parameter cases, every slot's allowed values, all banks, source replay and native radio and equivalent-blank grading. A same-matrix AB/BA target-swap mutation must reject stale keys and solution targets. Normal samples retain the forward/reverse roles that anchor the source difficulty.
''')
(H/'plot-extraction.md').write_text('''# Plot extraction and generation

No template requires plots. All practice matrices and dimension diagrams are LaTeX notation. The canonical prompt's two matrix PNGs were inspected: A is 4×2 and B is 2×4, so BA is 2×2. Their content-addressed references are retained in source.json. Neither matrix numbers nor standalone notation create a plotting requirement. Generated variants use LaTeX matrices and the source boxed dimension diagram; asset hashes are empty, and there is no new asset publishing stage.
''')
(H/'README.md').write_text('''# Determining the Dimension of the Product of Two Matrices

`../17592186100871.py` provides deterministic supported moderate/hard generators with 27/12 distinct bounded tasks. Easy remains explicitly unsupported in this package. Only changed operand dimensions create new tasks. Sources and learner history are preserved.

```
.venv/bin/python generate/scratch/17592186100871/validate.py
.venv/bin/python generate/scratch/17592186100871.py --difficulty hard --count 2 --seed 23 --format json
.venv/bin/python generate/scratch/17592186100871/replenish.py
```

API: generate(level, seed=0, template=None, parameters=None, profile=None, replay=False), plus moderate/hard wrappers. `replay=True` retains exact source prompts and solutions with the documented q-22067 solution correction and marks records evidence-only. Normal CLI output is a JSON array compatible with inventory_jobs.py. System Python reexecutes in the repository virtual environment when SymPy is absent. Parameters have exactly r,k,c and obey the complete profile domain.

Validation separates source-bank fidelity, exact mathematics, formatting and actual engine grading. Full source evidence, side-by-side variants and slot coverage remain local. `replenish.py` uses configured application contributor and EDB transport, holds api.lock over inventory/basis recheck through receipt/readback, previews installed native specs, retains exact basis-guarded requests, and verifies additive datoms, all source records, field ownership, generator registration, native grading and no-op repeat preparation. Outcome and shortages are recorded without calling unsupported bands filled.
''')
files=[H.with_suffix('.py'),H/'math_reader.py',H/'validate.py',H/'source.json',H/'source-components.json',H/'source-fidelity.json',H/'capabilities.json',H/'replenish.py']
v.write(H/'freeze.json',{'version':g.VERSION,'sha256':{str(p.relative_to(v.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}})

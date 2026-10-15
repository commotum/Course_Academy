from validate import *
source=g.SOURCE
components=[]
for sid,q in g.SOURCES.items():
 p,v,b=g.MODELS[sid];f=q[':question/answer-fields'][0]
 components.append({'source_id':sid,'difficulty':g.level_of(q),'template':sid,'profile':sid,'prompt':q[':question/problem'],'worked_solution':q[':question/worked-solution'],'P':p,'Q':v,'rectangle_bounds':b,'field':{'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'choice_count':5},'observed_parameters':{'scale':1},'normal_sampling_domain':{'scale':list(range(1,13))},'choices':[{'source_field':f[':answer-field/id'],'source_answer':a[':answer/id'],'exact_source_value':a[':answer/value'],'base_mathematical_object':str(g.parse_value(a[':answer/value'])),'recipe':'multiply the entire baseline integrand/expression by positive integer scale; preserve every integration variable and bound','correct':a[':answer/id']==f[':answer-field/correct'][':answer/id'],'complete_value_replayed':True,'misconception_interpretation':'No new misconception claim: preserve this exact observed expression pattern; pedagogical origin unresolved.'} for a in f[':answer-field/choices']]})
save(HERE/'template-components.json',{'database_basis':source['basis'],'lineage':source['lineage'],'components':components})
(HERE/'classification.md').write_text('''# Classification

At math basis 2651, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1,
the complete KP practice bank contains ten questions. The canonical example is
supporting evidence only and never inventory. All ten have one radio field,
key `selection`, with five bare-TeX math choices and one field-owned correct value.

| Difficulty | Sources / separate polynomial templates | Profiles | New plot rating |
|---|---|---|---|
| easy | q-127070, q-127206, q-127203, q-127226, q-127224 | one complete bank per source | none, unchanged region assets |
| moderate | q-127072, q-127229, q-127231, q-127228, q-127232 | one complete bank per source | none, unchanged region assets |
| hard | no observed practice template | none | unsupported by this package |

Easy identifies f = P_x + Q_y. The five polynomial structures distinguish
separable squares, partial cancellation of xy, a difference of squares,
combining cubic terms, and mixed linear/quadratic output. Moderate sets up a
dy dx integral on an explicitly supplied rectangle, with five distinct component
structures: x(2y+5), 3y^3(1+8x), cancellation to 5y^3,
2x(y^2+6), and 2y(2+x). These factored expressions name original instances,
not unrestricted forms. Each source retains its own complete choice profile.
No missing field, unreadable asset or unresolved source-key error was found.

The source diagrams occur only in worked solutions. Inspection of all ten
rasters in reference/source-diagrams.png confirms the stated polygons and bounds.
The narrower generator varies the field scale while holding those regions fixed,
so no new diagram is needed. This plot rating is based on asset roles, not count.
Hard has no validated workload here; absence does not prove inherent impossibility.
''')
(HERE/'template-extraction.md').write_text('''# Extraction and bounded generalization

`template-components.json` records every original prompt, worked solution,
component polynomial, field, answer, correct designation, profile, and exact
choice recipe. Every original option maps one-to-one at scale 1. No bank is pooled.

Backbone: the counterclockwise closed polygon, outward normal, flux form of
Green's theorem, supplied polynomial components, and requested object remain the
same. Easy differentiates P in x and Q in y, adds, simplifies and identifies f.
Moderate additionally reads rectangle bounds, describes the type I region, and
writes the repeated integral in dy dx order. No integral evaluation is requested.
Solutions retain the theorem statement, diagram, named components, concrete
partial derivatives, region description where applicable, substitution and final
simplification. Polynomial factoring and TeX layout are normalized independently
of mathematical source-bank fidelity.

The sole authored parameter is a positive integer scale s in 1..12. Observed
sources have s=1. Normal generation applies P=s P0 and Q=s Q0, so each derivative,
intermediate sum, correct integrand and each entire observed distractor integrand
or expression is multiplied by s. Integral bounds and differential order are
unchanged. These recipes reproduce complete observed values and do not claim
an unobserved learner misconception. The inferred generalization is explicitly
narrower than independently varying every coefficient. Nonzero positive scaling
preserves polynomial degrees, signs, cancellation structure and reasoning load;
it preserves bank inequivalence. x and y are real and all components are smooth.

Fixed components: source polygon and image (to reuse already verified geometry),
component exponents and term roles (to preserve the observed derivative method),
answer shape, five-choice contract and source-bank grouping (for fidelity), and
target f or dy dx integral (the assessed object). No positional target slot is
claimed. Independently changing bounds or target objects is outside this package.
The scale changes the assessed divergence, rather than only identity or order.
Mathematical fingerprints use expanded divergence, difficulty and moderate bounds;
they ignore source IDs, seed, field constants, option order and easy geometry.

All 120 bounded tasks were exhaustively checked; ten duplicate their original
source mathematical tasks and must not be imported again. Thus each supported
band has 60 catalog tasks, 55 mathematically new relative to the original bank.
Availability must further subtract presented/reserved tasks at the current basis.
Native grading tests every option of all variants and all source questions.
No new feedback or distractors are shown. Side-by-side originals and scales 1/7
are retained in side-by-side.json. Source mathematics and every generated derivative,
key, bound, final expression and unchanged diagram were checked separately.
''')
(HERE/'plot-extraction.md').write_text('''# Unchanged solution diagrams

The source contact sheet shows all ten figures in source-bank order. All use
black x/y axes with arrowheads, pale blue polygon fill and thin orange boundaries.
Labels mark only relevant coordinate values. Easy figures show the stated triangle
or rectangle; moderate figures show precisely the supplied axis-aligned rectangle.
The polygon is the region D and its boundary is C. The diagram is explanatory;
the prompt already supplies vertices. It does not encode field scale or answer.

The axes, ticks, polygon vertices, fill, crop and labels remain fixed for every
scale of that source. No plotting function or asset publication is required.
asset-verification.json retains each original database-relative path, source ID,
and SHA-256, checked against stored bytes and content-addressed filename.
All labels and bounds were visually read from reference/source-diagrams.png.
The rating is none for new plots, with unchanged existing mathematical diagrams.
''')
exception={'difficulty':'hard','status':'unsupported','scope':'bounded validated package, not inherent impossibility','evidence':'All ten rated practice questions: five easy divergence-identification and five moderate rectangle-integral setups; canonical example also sets up a rectangle integral. No hard template or workload validated.','reason':'Relabeling existing workload as hard is unsupported; adding evaluation or new regions would exceed these extracted templates.','reopen_on':'new source evidence or a separately validated in-scope hard template','unfilled_quantity':5,'rolling_minimum_if_supported':5,'filled':False,'shortage_explicit':True}
save(HERE/'capabilities.json',{'supported_levels':list(g.LEVELS),'unsupported_levels':['hard'],'exceptions':[exception],'finite_limits':{'easy':{'catalog':60,'original_source_aliases':5,'maximum_new_relative_to_sources':55},'moderate':{'catalog':60,'original_source_aliases':5,'maximum_new_relative_to_sources':55}},'capacity_policy':'Current unavailable, reserved, canonical and existing mathematical tasks must be subtracted; never pad with seeds, identities, or choice order.'})
(HERE/'README.md').write_text('''# Flux-form Green theorem generator

Validated source package for KP 17592186172100. Registration points to
`generate/scratch/17592186172100.py`; stable UUID is in generator-id.json.

```
python3 generate/scratch/17592186172100.py --difficulty easy --count 5 --seed 1930 --format json
.venv/bin/python generate/scratch/17592186172100/validate.py
.venv/bin/python generate/scratch/17592186172100/replenish.py
```

The public script re-execs the repository Python environment when SymPy is absent.
SymPy 1.14.0 and existing math_format helpers are required. Only easy/moderate
are supported; unsupported hard raises an explicit error. Per-template replay:
`--template q-127070 --scale 1 --count 1`. Sampling uses seeded selection without
replacement within one invocation. Across calls, consumers must compare semantic
fingerprints and existing question identities; the seed is provenance only.
Catalog capacity and hard exception remain explicit in capabilities.json.

Validation covers all original banks and the complete 120-task bounded domain,
reads displayed component fields independently, differentiates them exactly,
checks displayed solution derivatives and final objects, checks all option keys,
compares unevaluated repeated-integral structures, tests actual native grading,
checks unchanged content-addressed diagram bytes, and demonstrates that changing
only the seed preserves identities. The source bank already provides five unseen,
unreserved validated questions per supported band at basis 2651. No extra question
should be committed while those counts remain sufficient.

Durable registration/replenishment is scoped to this KP. It uses the application's
Database integration, contributor and native specs; serializes with api.lock;
checks current lineage/basis; saves exact EDN/request before submission; recovers
receipts; reads at db_after; and audits all datoms and unchanged source questions.
Evidence and receipts live under reference/. Source questions and learner data
are never retracted or changed.
''')
print('Scoped classification, extraction, plot evidence and capabilities saved')

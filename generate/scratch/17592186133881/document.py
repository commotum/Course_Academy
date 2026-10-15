"""Persist the scoped classification and source-component extraction."""
import importlib.util,json,re
from pathlib import Path
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rows=[];components=[];templates={}
for sid,q in g.SOURCES.items():
 level=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1];types=[f[':answer-field/type'][':db/ident'].split('/')[-1] for f in q[':question/answer-fields']]
 prompt=q[':question/problem'];statements=[line for line in prompt.splitlines() if re.match(r'(?:- \*\*)?(?:I|II|III|IV)\.',line)]
 backbone=(level,tuple(types),tuple(statements),len(q.get(':question/worked-solution','').split('\n\n')))
 templates.setdefault(backbone,[]).append(sid)
 rows.append(f'| {sid} ({q[":db/id"]}) | {level} | {", ".join(types)} | {g.FAMILIES[sid]} | heavy | source-bank:{sid} |')
 fields=[]
 for f in q[':question/answer-fields']:
  choices=[]
  for a in f[':answer-field/choices']:
   choices.append({'source_answer_id':a[':db/id'],'value':a[':answer/value'],'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id'],'recipe':'Boolean truth value for field proposition' if len(f[':answer-field/choices'])==2 else 'Fixed subset '+a[':answer/value']+' of I,II,III,IV; compare with actual proposition truths','complete_value_replayed':True})
  fields.append({'field_id':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'choices':choices})
 components.append({'source_id':sid,'db_id':q[':db/id'],'difficulty':level,'prompt':prompt,'worked_solution':q.get(':question/worked-solution'),'statements':statements,'fields':fields,'family':g.FAMILIES[sid],'assets':re.findall(r'!\[.*?\]\((.*?)\)',prompt+'\n'+q.get(':question/worked-solution','')),'proposed_realization':list(g.REALIZATIONS[sid]),'realization_evidence':'same qualitative diagram family; original numerical scale unobserved'})
(P/'source-components.json').write_text(json.dumps(components,indent=2)+'\n')
(P/'classification.md').write_text(f'''# Visual curl classification

Database math; captured basis {g.PROVENANCE['basis']}; lineage {g.PROVENANCE['lineage']}. All 14 practice sources, complete fields/banks, correct references, worked solutions, difficulty, plot references and canonical example were read at this basis. Canonical e-8929 supports interpretation but does not enter practice inventory. The unrated q-105103 remains unrated and is not counted.

| Source | Difficulty | Fields | Diagram family | Plot rating | Profile |
|---|---|---|---|---|---|
'''+ '\n'.join(rows)+f'''

There are {len(templates)} source Markdown/value backbones across observed field layouts and solution stages. Statement order, irrotational negation, queried positive/negative direction and radio versus checkbox layout remain distinct source templates. Every source is assigned to its complete original choice profile; Boolean checkbox banks and both five-option radio banks are fully replayed. The short unrated solution is classified separately and excluded from difficulty generation.

Heavy plots: every prompt's arrows carry the supplied mathematical object; plot generation is necessary when changing it. Source-contact.png was inspected. Sources show uniform horizontal/diagonal/vertical fields, horizontal/vertical compression, radial expansion, clockwise/counterclockwise elliptical rotation, and outward spirals of either handedness. No source uses a nonzero third component or z-dependence.

q-105664 has a contradictory clockwise sentence followed by counterclockwise/right-hand conclusions. The diagram and key support positive curl; new solutions consistently say counterclockwise. The original question and solution remain unchanged.

No easy source was observed. Within this package, easy is unsupported: there is no source difficulty boundary or response layout supporting a downgrade. This is a bounded evidence exception, not proof that an easy question can never exist. Reopen on new rated evidence.
''')
(P/'template-extraction.md').write_text('''# Template extraction

source-components.json describes each original prompt, statement, field, complete bank and solution, before generalization. It maps every answer to its exact source field, value, designation and recipe. source-fidelity.json reports complete bank coverage.

Shared pattern: infer local paddlewheel rotation from a planar vector field, decide zero versus nonzero curl, identify irrotational behavior, apply the right-hand rule, and select all true propositions or the correct subset from a radio bank. Four propositions and their exact source layout remain fixed. No calculation of an explicit derivative is requested of the learner.

Slot domain: exact affine realizations F=(ax+by+u,cx+dy+v,0) in R^3. These proposed coefficients are same-method generalizations, not claimed numerical measurements of unscaled originals. For moderate rotation, retain opposite-sign cross components and vary their absolute coefficient ratio over 1..4. For moderate or hard outward spirals, retain a=d>0 and b=-c with the original handedness, and vary radial/angular ratio over 1..4. For hard uniform diagonal flow, preserve southeast direction and vary slope over 1..4. For hard radial expansion, preserve positive diagonal entries and vary anisotropy over 1..4. Axis-only uniform/compression sources each have one qualitative variant: changing length alone cannot create fresh questions. No shifts, new targets, nonlinear fields, extra operations or z-components are introduced.

Each source template retains the supplied family and curl sign because its complete source radio/checkbox bank and explanation are conditional on those features. Numerical coefficients control arrows, qualitative truths and the concrete worked solution together. Profile selection precedes field construction. A radio bank retains all five exact observed subsets, and a checkbox field owns exactly the true and false options. The correct value must belong to the field; no choices are pooled across profiles.

Solution stages remain paddlewheel thought experiment; observed local rotation; zero/nonzero and irrotational consequences; right-hand direction; conclusions for I..IV; final subset. Replays retain original wording and original plots. New prose keeps these stages, removes the contradictory q-105664 direction sentence, and omits repeated decorative solution diagrams that add no supplied information. Wording fidelity and mathematical fidelity are reported separately. No inferred distractor explanations are shown to learners.

Stable identities include the authored source profile and normalized affine field, excluding seed/choice order. Inventory and generation deduplicate more strictly by normalized field alone, including across source templates and difficulties. Positive global field scaling is collapsed. Original source magnitudes are unmeasured; baseline realizations conservatively represent their qualitative families for duplicate suppression, so similar originals may count as one.
''')
(P/'plot-extraction.md').write_text('''# Plot extraction and rendering

source-components.json retains every original prompt and solution asset in order. source-contact.png shows all prompts side by side. Source plots use black/gray arrows on a regular square grid, x right and y up, no numerical ticks, equal geometric axes, and local velocity encoded by direction and relative length. Rotational families turn around the origin; gradient families expand or compress along the shown axes. Solution plots repeat these fields with paddlewheel illustrations; those teaching illustrations have no variable numeric labels.

General specification: 13 by 13 samples of one exact planar affine field on [-3,3]^2; x/y axes crossing at zero; black/gray quiver arrows; equal aspect; no invented numeric labels. Fixed orientation is essential to the right-hand rule. Variable coefficients change all vector components and relative lengths together. A single global scale makes the largest arrow length 1/3; per-arrow normalization is forbidden because it destroys the magnitude gradient. The zero vector has no arrow. Quiver data and normalization are retained in JSON beside each PNG. Bounds [-3.6,3.6] leave room for arrow heads and axis labels. Matplotlib generates PNGs only.

Prompt plots must be regenerated for new parameters. Source replay uses the exact original bytes, because unscaled diagrams cannot establish exact coefficients. Generated examples were compared with these originals for topology, arrow direction, local rotation, compression/expansion, readability and label bounds. The new concrete solution explains the same paddlewheel and right-hand stages in prose; no independent plot randomness or new reasoning stage is introduced.
''')
(P/'capabilities.json').write_text(json.dumps({'version':g.VERSION,'supported_levels':['moderate','hard'],'unsupported_levels':['easy'],'easy':{'filled':False,'reason':'No rated easy source or supported difficulty boundary; bounded to observed moderate/hard families.'},'sampling_attempt_bound':512,'finite_families':['axis-only uniform fields','axis-only compression'],'distinctness':'Exact affine coefficients modulo positive global scale; seed, identities, source profile and choice order ignored when counting.'},indent=2)+'\n')
(P/'README.md').write_text('''# Interpreting the Curl of a Vector Field

Generator: ../17592186133881.py. Run with the repository .venv Python, --difficulty moderate|hard --count N --seed S --format json|markdown. validate.py replays all complete source banks and validates the full declared coefficient-ratio domain through exact circulation, plotted numeric arrays, field keys and the application grader. replenish.py handles current inventory, application lock, configured attribution, schema validation, basis guard, saved exact request and verified readback. Easy remains unsupported. Original sources and learner state are preserved.
''')
print('source backbones',len(templates))

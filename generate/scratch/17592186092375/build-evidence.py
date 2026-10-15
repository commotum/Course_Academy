"""Record source classification, extraction and bounded capabilities."""
import importlib.util,json,hashlib,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
templates={
'cubic-quartic-linear':['q-123005'],
'cubic-quadratic-linear':['q-123025','q-85724'],
'linear-quadratic':['q-81377'],
'cubic-quadratic-pair':['q-15174'],
'quadratic-linear-illustrated':['q-123019'],
'cubic-linear-illustrated':['q-81380','q-123020']}
save('classification.json',{'database':'math','basis':g.SOURCE['basis'],'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','knowledgePoint':g.KP_ID,'rated_practice':8,'unrated_incomplete':2,'levels':{'easy':{'field_types':[['radio']],'field_key':'selection','choices':5,'templates':[{'id':k,'source_ids':v,'profiles':v,'plot_rating':'light' if 'illustrated' in k else 'none','new_plot_generation_supported':False} for k,v in templates.items()]},'moderate':{'observed':0,'supported':False},'hard':{'observed':0,'supported':False}},'excluded_sources':[{'source':'q-15172','reason':'missing rating, correct link and worked solution'},{'source':'q-81437','reason':'missing rating, correct link and worked solution'}],'canonical':'e-602 is supporting formula evidence only, not inventory','choice_profiles':'each of eight complete banks retained separately; no mixed banks'})
text='''# Template extraction

Captured at EDB basis 2637, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All ten original practice records and the canonical example are retained in source.json. Eight complete sources are rated easy; two legacy sources lack their key, rating and solution and are excluded.

The shared assessment is selecting the arc-length integral of a supplied polynomial parametric curve on a supplied interval. Six Markdown/value families differ in their derivative structures, factorization stage or illustration. Each of the eight source questions retains its own complete five-choice bank. Classification groups and profile membership are in classification.json. No bank pooling is used.

The fixed backbone is the supplied x(t), y(t), one radio field named selection, five integral expressions, the formula L = integral sqrt((dx/dt)^2+(dy/dt)^2), the two explicit differentiation stages and substitution/simplification in the original worked solution. The factored t in q-15174 requires nonnegative t. Every original choice, with field, answer identity, exact text, radicand, outside factor and replay result, is mapped in choice-recipes.json. Psychological interpretations are unresolved; no inferred mistakes replace observed expressions.

Only the two endpoint roles vary. The lower and upper bound must change together in the prompt, every answer and every explicit solution integral. Curves, coefficients, translations, powers, operators, choice order and answer shapes are fixed. Coefficients remain fixed as a conservative policy because their source distractor derivations are not evidenced. Bounds are a conservative same-method generalization: they alter the mathematical integral without adding differentiation or integration stages; the question still asks for an expression, not its evaluation. No seed-only, identity-only or option-order variants count. Canonical IDs never enter generated content.

Normal sampling uses integral bounds a in 2..8, b in a+1..a+4 on four nonplot source profiles; q-85724 instead uses negative intervals a in -8..-3 with a < b <= -1. Every domain cell is filtered by exact polynomial root isolation: all five integrands must be real and their squared integrands strictly pairwise ordered throughout the interval. This proves unique definite integral values, not merely distinct text. All 126 admitted cells are independently validated, rather than relying on random sampling. The endpoint domain is deliberately bounded and is not a claim of mathematical exhaustion.

Some original distractors are nonreal on part of their original intervals (exact rational witnesses in source-issues.json). Original replay preserves those banks for fidelity evidence; generated intervals avoid these defects. Original questions and learner history are never repaired or rewritten here.

## Source-specific components

'''
for sid,q in g.CASES.items():
 x,y,a,b=g.CURVES[sid];text+=f"### {sid}\n\n{x=}, {y=}; original interval [{a}, {b}].\n\n"+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\n'
(HERE/'template-extraction.md').write_text(text)
assets=[]
for q in g.SOURCE['record'][':knowledge-point/questions']+[g.SOURCE['record'][':knowledge-point/canonical-example']]:
 for ref in re.findall(r'!\[[^]]*\]\(([^)]+)\)',q.get(':question/problem','')):
  p=Path('/media/jake/SSD/EDB/math')/ref;assets.append({'source':q.get(':question/math-academy-id'),'reference':ref,'exists':p.is_file(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None})
save('plot-extraction.json',{'rating':'light for illustrated profiles; none for generated profiles','inspection':'q-123019, q-81380, q-123020: blue planar curve on black x/y axes, solid supplied parameter segment, dotted continuation, labeled endpoint parameter values, orientation arrow; endpoints/solid segment are mathematically tied to bounds','assets':assets,'specification':'for a future illustrated generator, sample curve over interval, extend dotted curve beyond endpoints, draw orientation arrow and label t=a,t=b; regenerate all segment and endpoint features together with question parameters','reuse_policy':'illustrated profiles replay only at original interval, retaining exact original asset; do not reuse a source plot under changed endpoints','generation':'no newly plotted variants are claimed; stage 7 is not needed for admitted variants'})
save('capabilities.json',{'generator_id':g.GENERATOR_UUID,'script':str(HERE.with_suffix('.py').relative_to(HERE.parents[2])),'supported_levels':['easy'],'finite_variant_count':126,'normal_profiles':sorted(set(g.CASES)-g.PLOTTED),'replay_only_profiles':sorted(g.PLOTTED),'exceptions':[{'levels':['moderate','hard'],'status':'unsupported','evidence':'No rated source examples, field contracts or difficulty-preserving templates observed at basis 2637. Relabeling easy questions is not permitted. New source evidence reopens classification.','nominal_unfilled':{'moderate':5,'hard':5}},{'profiles':sorted(g.PLOTTED),'status':'replay-only','evidence':'Illustrated endpoints tied to original interval; no new plot renderer has been validated.'},{'scope':'easy endpoint variants','status':'finite-policy-limit','count':126,'evidence':'Exhaustive slot-coverage.json; exact source coefficients retained; bounded integer endpoint policy. More than 126 unseen accepted tasks is not claimed.'}], 'source_issues':'source-issues.json records original-domain defects and variant-domain correction without modifying originals'})
(HERE/'README.md').write_text('''# Parametric arc-length integral generator

Run from the repository with `.venv/bin/python generate/scratch/17592186092375.py --difficulty easy --count 5 --seed 42 --format json`. SymPy 1.14 is required; the application uses its configured Python environment. Validate with `.venv/bin/python generate/scratch/17592186092375/validate.py`.

Easy only. There are 126 validated bounded endpoint variants across five nonplot profiles. Illustrated profiles support source replay only. Moderate and hard are unsupported; their nominal five-question reserves remain unfilled. Source evidence can reopen these restrictions. Seeds and identity changes do not add variants. Output stores stable field-owned UUIDs and complete solutions, retaining provenance separately from content.

See classification.json, template-extraction.md, choice-recipes.json, plot-extraction.json, source-replay.json, source-issues.json, slot-coverage.json, native-grading.json, validation.json and review.md. Registration and any replenishment requests/receipts/readback are retained under reference/replenishment. Original source and learner facts must remain unchanged. Current inventory is always rechecked under the application's api.lock before committing.
''')

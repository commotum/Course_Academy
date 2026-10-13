"""Retain source classification and extraction evidence, stages 3–5."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H));import validate as v
g=v.g
classified=[]
for q in g.SOURCE['record'][':knowledge-point/questions']:
 mid=q[':question/math-academy-id'];fields=q.get(':question/answer-fields',[])
 level=q.get(':question/difficulty',{}).get(':db/ident','unclassified').split('/')[-1]
 row={'source_id':mid,'db_id':q[':db/id'],'difficulty':level,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'fields':fields,'plot_rating':'none','supported':mid in g.PROFILES}
 if mid in g.PROFILES:row.update(template=g.PROFILES[mid][1],profile=mid)
 else:row['exception']='Missing fields; answer shape unresolved' if not fields else 'Unrated and missing key/solution; difficulty unresolved'
 classified.append(row)
(H/'classification.json').write_text(json.dumps({'database':'math','lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','basis':g.SOURCE['basis'],'questions':classified,'canonical_example':g.SOURCE['record'].get(':knowledge-point/canonical-example')},indent=2))
intro=f'''# Differentiating a trigonometric function using the chain rule

Captured math basis {g.SOURCE['basis']}, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. All eleven practice sources and the canonical example were pulled together. source.json/source.edn retain every source field and original wording. No plots appear in prompts, banks or solutions. The canonical example e-732 is instructional evidence only.

Moderate: four templates, two blank and two five-option radio, with one bank profile each. Hard: five prompt/solution templates, two with usable fields (one blank and one five-option radio). q-31241 (quadratic sine slope), q-48508 (affine cosine tangent) and q-48636 (cubic cosine tangent) have no fields and are explicitly excluded. Unclassified: two radio derivative templates q-1943 and q-1946 without key, solution or rating; neither establishes an easy band. Easy remains unclassified/unsupported by this package. Every source is assigned to its own observed bank; none are pooled. Plot rating none for every template, including excluded templates.

q-1943 is cos(x²), with options x sin(2x), -x sin(x²), -2x sin(x²), x² sin(2x), x² cos(x²); differentiation supports -2x sin(x²), but no source key or difficulty is asserted. q-1946 is tan(2x+2), with options 2 csc²(2x+2), 2 cot(2x+2), 2 sec²(2x+2), 2 sec(2x+2), sec²(2x+2); differentiation supports 2 sec²(2x+2), with the same unresolved rating/key/solution limitation. The three fieldless hard sources have results 2 cos(1), y=1, y=1 respectively; the missing response structures are not inferred into generated questions.

q-310182 stores a delimited text answer `$-4\\pi$`; its source bank is retained exactly as evidence. New blanks use delimiter-free mathematical values and preserve field key and fragment shape. q-310179 stores bare {{sec}} notation; generated answers use \\sec. These are generated-content corrections only. Actual source grading rejects the equivalent -4*pi entry for q-310182 because its bank is lexical text; reference/source-grading-summary.json retains that failure and all other supported original grading results. This unchanged source is excluded from validated availability. Correctness, source-bank fidelity and actual grading are checked separately.
'''
(H/'classification.md').write_text(intro+'\n\n'+ '\n\n'.join('## '+r['source_id']+' ('+r['difficulty']+')\n\n'+r['prompt']+'\n\nFields: '+', '.join(f[':answer-field/type'][':db/ident'] for f in r['fields'])+'. '+('Template '+r['template']+'; bank '+r['profile']+'.' if r['supported'] else r['exception']) for r in classified))
recipes={
'q-310179':['4t x³ sec²(t x⁴−5)'],
'q-310180':['t cos(t · π/(2t)) = 0'],
'q-31153':['3 cos(6+t)','−3 cos(6+t)','t cos(2)','t cos(6+t)','−t cos(6+t)'],
'q-31163':['−2 sin(t−2x)−9x²','−cos(t−2x)−9x²','sin(t−2x)−18x²','2 cos(t−2x)−18x²','2 sin(t−2x)−18x²'],
'q-310182':['2(t+1)π(−1)^t'],
'q-51026':['y=x−π−(t+1)','y=x+π−t','y=−t','y=−t x+tπ','y=0']}
patterns={
'q-310179':'Differentiate tan(t x⁴−5), with fixed negative shift, fourth power and blank derivative fragment. The inner derivative is 4t x³; no distractors.',
'q-310180':'Slope of sin(t x) at x=π/(2t), positive integer inner slope and exact angle π/2. Blank numeric fragment, slope 0. Distinct frequencies, rather than distinct answers, define tasks.',
'q-31153':'Slope of sin(3x+t) at x=2. Affine positive slope 3 and variable positive shift t; five-option radio. Chain rule followed by substitution gives 3 cos(6+t). t=3 rejected because coefficient-confusion options collide with the correct answer.',
'q-31163':'Differentiate cos(t−2x)−6x³. Negative affine slope and negative cubic coefficient retained. Split sum, apply chain rule to g, power rule to h, recombine. Radio expression derivative; five options preserve complete compound source patterns, including the altered cubic coefficient −9.',
'q-310182':'Slope of sin(π(t x²+2x−2)) at x=1. Variable positive quadratic coefficient, fixed linear coefficient 2 and signed constant −2. Inner derivative π(2t x+2), angle tπ, slope 2(t+1)π(−1)^t. Blank scalar math with exact π. Both parity signs tested.',
'q-51026':'Tangent to y=t cos(x−1) at (1+π,−t). Positive amplitude t, fixed negative shift −1, exact phase π. Chain rule, zero slope, point-slope equation, final y=−t. Radio full equations; every bank recipe is an entire equation.'}
extraction=[]
for p,profile in g.PROFILES.items():
 q=g.ORIGINALS[p];sf=q[':question/answer-fields'][0];f,u,at,ans,bank=g.model(p,profile[2]);correct=next(i for i,b in enumerate(bank) if v.sp.simplify(b-ans)==0)
 mapping=[]
 for i,a in enumerate(sf[':answer-field/choices']):
  parsed=v.expr(a[':answer/value'].split('=',1)[-1].strip('$'));j=next(j for j,b in enumerate(bank) if v.sp.simplify(v.sp.trigsimp(b-parsed))==0)
  mapping.append({'source_answer_id':a[':answer/id'],'source_field_key':sf[':answer-field/key'],'exact_source_value':a[':answer/value'],'recipe':recipes[p][j],'reproduces_complete_object':True,'correct':j==correct,'interpretation':'Correct result' if j==correct else 'Observed parameterized expression pattern; psychological error interpretation unresolved'})
 extraction.append({'source_id':p,'template':profile[1],'difficulty':profile[0],'source_parameters':{'t':profile[2]},'proposed_parameter_domain':list(profile[3]),'source_field_key':sf[':answer-field/key'],'source_field_type':sf[':answer-field/type'][':db/ident'],'source_choice_count':len(sf[':answer-field/choices']),'pattern':patterns[p],'fixed_vs_variable':'Only t varies; all other signs, powers, constants and evaluation conventions are fixed. Domain deliberately narrower than possible mathematical extension.','source_components':q,'choice_bank_mapping':mapping,'plot_specification':{'rating':'none','assets':[]},'solution_sequence':'Original prose and displays replay exactly at source parameters. Simultaneous expression replacements propagate t into problem, substitution, inner derivative, chain-rule expansion, evaluation and final result. Source sentences unchanged; normalization of answer notation and radio placeholder are explicit extensions.'})
(H/'template-extraction.json').write_text(json.dumps(extraction,indent=2))
(H/'template-extraction.md').write_text('# Templates and complete banks\n\nEvery source option is mapped in template-extraction.json with original field identity/value and reproducibility recipe. Original source components are retained. The psychological interpretation of unusual distractors remains unresolved; recipes are observed expressions, never learner-facing feedback. Banks are selected as complete profiles. No mixing or choice-count changes. No blank distractors added.\n\n'+ '\n\n'.join('## '+r['source_id']+'\n\n'+r['pattern']+'\n\nSource t='+str(r['source_parameters']['t'])+'; proposed bounded t domain '+str(r['proposed_parameter_domain'])+'.\n\n'+ '\n'.join('- '+m['exact_source_value']+' → '+m['recipe'] for m in r['choice_bank_mapping']) for r in extraction))
(H/'plot-extraction.md').write_text('# Plot stages 5 and 7\n\nNo source prompt, choice or solution contains graph or diagram assets. This KP uses symbolic expressions only. Every template has plot rating none; no new or reused assets require publication.\n')
(H/'README.md').write_text('''# Trigonometric chain-rule generator

Run generate/scratch/17592186064281.py with --difficulty moderate|hard --count N --seed S --format json|markdown. The script never writes to the database. Source snapshots, classification and extraction cover all eleven practice records and canonical instructional evidence. Six supported templates replay their entire source banks and exact original prompt/solution at source parameters. validation.json freezes exhaustive bounded correctness, rendered mathematics, deterministic identity and actual learner grading. review.md contains originals alongside variants. capabilities.json records the easy classification exception, excluded fieldless templates, bounded counts and narrower sampling.

replenish.py uses existing EDB integration, configured application attribution, native validation specs, api.lock, retained exact requests and basis guards. It adds only distinct content to this KP and registers its stable UUID/script via installed attributes. Existing source questions and all learner history remain unchanged. reference/replenishment retains inventory, preparation, preview, request, receipt and exact-basis readback. Unsupported levels are never claimed filled.
''')
# Keep extraction evidence for excluded templates, without authoring unsupported fields or ratings.
excluded=[]
legacy_recipes={
 'q-1943':{'parameters':{'n':2},'pattern':'Derivative of cos(x^n); original n=2, no proposed sampler until difficulty/key/solution review','recipes':['x*sin(n*x)','-x*sin(x^n)','-n*x^(n-1)*sin(x^n)','x^n*sin(n*x)','x^n*cos(x^n)'],'correct_index_inferred':2},
 'q-1946':{'parameters':{'a':2,'b':2},'pattern':'Derivative of tan(a*x+b); original positive a=2 and b=2, no proposed sampler until difficulty/key/solution review','recipes':['a*csc(a*x+b)^2','a*cot(a*x+b)','a*sec(a*x+b)^2','a*sec(a*x+b)','sec(a*x+b)^2'],'correct_index_inferred':2}}
for q in g.SOURCE['record'][':knowledge-point/questions']:
 mid=q[':question/math-academy-id']
 if mid in g.PROFILES:continue
 row={'source_id':mid,'source_components':q,'plot_rating':'none','supported':False,'sampling_domain':[],'unresolved':'Missing response field shape' if not q.get(':question/answer-fields') else 'Missing original key, fixed solution and difficulty','choice_bank_mapping':[]}
 if mid in legacy_recipes:
  spec=legacy_recipes[mid];row.update(spec)
  sf=q[':question/answer-fields'][0]
  for i,a in enumerate(sf[':answer-field/choices']):
   row['choice_bank_mapping'].append({'source_answer_id':a[':answer/id'],'source_field_key':sf[':answer-field/key'],'exact_source_value':a[':answer/value'],'recipe':spec['recipes'][i],'original_parameters':spec['parameters'],'interpretation':'Observed mathematical expression; error interpretation unresolved','correct_designation':'Mathematically correct, not source-attested' if i==2 else 'Mathematically incorrect','reproduction_at_source':'Original expressions are recorded exactly; classification remains blocked by key/solution/rating evidence'})
 excluded.append(row)
(H/'excluded-template-extraction.json').write_text(json.dumps(excluded,indent=2))

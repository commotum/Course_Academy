#!/usr/bin/env python3
"""Independent read-only review. Run with the job's Python executable."""
import sys
sys.dont_write_bytecode = True
import json, hashlib, importlib.util, re, platform, shutil
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import sympy as S

ROOT = Path(__file__).resolve().parent
JOB = ROOT.parent
PKG = JOB / 'workspace'
REPO = Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(REPO))
from scripts.question_capture.math_format import normalize_prose
def save(name, obj):
    p=ROOT/name; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, default=str)+'\n')
def load(p): return json.loads(Path(p).read_text())
def snapshot():
    return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(PKG.rglob('*')) if p.is_file()}
before=snapshot(); save('package-before.json',before)
spec=importlib.util.spec_from_file_location('reviewed_generator',PKG/'17592186229183.py')
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
source=load(JOB/'source/source.json'); inv=load(JOB/'source/inventory.json')
batch=load(JOB/'samples.json'); save('batch-records.json',batch)

def num(tex):
    m=re.search(r'\\frac\{(-?\d+)\}\{(\d+)\}',tex)
    return S.Rational(m[1],m[2]) if m else S.Rational(re.search(r'-?\d+(?:\.\d+)?',tex)[0])
def prompt_params(q):
    terms=re.findall(r'\$([^$]+)\$', q[':question/problem'])
    vals=[num(x) for x in terms[:6]]
    return dict(zip(('H','v','q','c','rin','rout'),vals))
def rounding(x):
    return str(Decimal(str(S.N(x,60))).quantize(Decimal('.1'), rounding=ROUND_HALF_UP))
def independently(q):
    p=prompt_params(q); H,v,q0,c,ri,ro=[p[k] for k in ('H','v','q','c','rin','rout')]
    t=S.Symbol('t',nonnegative=True);d=ri-ro;V=v+d*t
    # Derived independently from mass conservation, not generator data/metadata.
    Q=c*V+(q0-c*v)*(v/V)**(ro/d)
    residual=S.simplify(S.diff(Q,t)-(c*ri-ro*Q/V))
    initial=S.simplify(Q.subs(t,0)-q0);to=(H-v)/d
    result=S.simplify(Q.subs(t,to))
    return {'prompt_parameters':p,'overflow_time':to,'exact_mass':result,
            'rounded_mass':rounding(result),'ode_residual':residual,'initial_residual':initial}
def field_answers(q):
    for f in q[':question/answer-fields']:
        key=f.get(':answer-field/correct')
        key=key.get(':answer/id') if isinstance(key,dict) else key[1] if key else None
        yield f, key
def analyze(r):
    q=r['question'];calc=independently(q);f,key=next(field_answers(q))
    choices=f[':answer-field/choices'];ordered=sorted(choices,key=lambda a:num(a[':answer/value']))
    correct=next((a for a in choices if a[':answer/id']==key),None)
    return {'id':q[':question/id'],'template':r.get('generation',{}).get('template'),
            'seed':r.get('generation',{}).get('seed'),**calc,
            'correct_value':correct[':answer/value'] if correct else None,
            'correct_position':next((i+1 for i,a in enumerate(choices) if a[':answer/id']==key),None),
            'correct_numeric_rank':next((i+1 for i,a in enumerate(ordered) if a[':answer/id']==key),None),
            'sorted_choices':[a[':answer/value'] for a in ordered],
            'median_id':ordered[2][':answer/id'],'correct_id':key,
            'math_pass':correct is not None and num(correct[':answer/value'])==S.Rational(calc['rounded_mass'])
                        and calc['ode_residual']==0 and calc['initial_residual']==0}

# Small stratified sample covers each visible template; independently chosen seeds.
samples=[G.generate('easy',seed=seed,template=template)
         for template in G.MASKS for seed in (7319,7320,7321,7322)]
save('sample-records.json',samples)
minimal=G.generate('easy',seed=9041,template='q-336506',
                   parameters={'H':'20','v':'10','q':'1','c':'0.4','rin':'6','rout':'4'})
save('minimal-records.json',[minimal])
p={'H':'210','v':'90','q':'18','c':'0.5','rin':'18','rout':'12'}
cf=[G.generate('easy',seed=9041,template='q-336506',parameters=p),
    G.generate('easy',seed=9041,template='q-336506',parameters={**p,'H':'240'}),
    G.generate('easy',seed=9041,template='q-336506',parameters={**p,'rin':'9','rout':'6'}),
    G.generate('easy',seed=9041,template='q-336513',parameters=p)]
save('counterfactual-records.json',cf)
save('counterfactual-results.json',{'order':['base','capacity 210→240','flows divided by two','context coolant→flavoring'],
      'analysis':[analyze(r) for r in cf],
      'relevant_response_changed':analyze(cf[0])['correct_value']!=analyze(cf[1])['correct_value'],
      'irrelevant_flow_mass_preserved':analyze(cf[0])['correct_value']==analyze(cf[2])['correct_value'],
      'irrelevant_context_mass_preserved':analyze(cf[0])['correct_value']==analyze(cf[3])['correct_value']})
all_records=samples+batch+[minimal]+cf
math=[analyze(r) for r in all_records]
save('math-results.json',{'command':f'{sys.executable} {ROOT}/review.py','results':math,'all_pass':all(r['math_pass'] for r in math)})

# Reproduce every captured source case against current public profiles.
replays=[];replay_results=[]
for q in source['material']['kp'][':knowledge-point/questions']:
    sid=q[':question/math-academy-id'];p={k:str(v) for k,v in prompt_params(q).items()}
    row={'source_uuid':q[':question/id'],'source_id':sid,'parameters':p,'independent_math':independently(q)}
    try:
        r=G.generate('easy',seed=9041,profile='observed:'+sid,parameters=p);replays.append(r)
        actual=r['question'];src_fields=list(field_answers(q));actual_fields=list(field_answers(actual))
        bank=lambda fs:[sorted(a[':answer/value'] for a in f[':answer-field/choices']) for f,_ in fs]
        row.update(prompt_equal=actual[':question/problem']==q[':question/problem'],
                   solution_equal=actual.get(':question/worked-solution')==q.get(':question/worked-solution'),
                   field_count=[len(src_fields),len(actual_fields)],banks_equal=bank(src_fields)==bank(actual_fields),
                   source_correct_values=[next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key),None) for f,key in src_fields],
                   replay_correct_values=[next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key),None) for f,key in actual_fields])
    except Exception as e:row['error']=f'{type(e).__name__}: {e}'
    replay_results.append(row)
canonical=source['material']['kp'][':knowledge-point/canonical-example']
cp={k:str(v) for k,v in prompt_params(canonical).items()}
canonical_r=G.generate('easy',seed=9041,template='q-336506',parameters=cp)
save('source-replay-records.json',replays)
save('canonical-parameter-records.json',[canonical_r])
save('source-replay-results.json',{'cases':replay_results,'canonical':{'source_uuid':canonical[':question/id'],
    'calculation':independently(canonical),'tested_parameters':cp,'same_parameters_other_context':analyze(canonical_r),
    'limitation':'No syrup canonical prompt/solution mask or observed bank exists in package.'}})

# Exact replay, explicit physical boundaries, and actual stochastic rejection tracing.
rejects=[]
old_guard,old_bank=G.guard,G.method_bank
def traced_guard(*a,**kw):
    try:return old_guard(*a,**kw)
    except ValueError as e:rejects.append({'where':'guard','reason':str(e),'parameters':a[0]});raise
def traced_bank(*a,**kw):
    try:return old_bank(*a,**kw)
    except ValueError as e:rejects.append({'where':'bank','reason':str(e)});raise
G.guard,G.method_bank=traced_guard,traced_bank
replayed=[G.generate('easy',seed=seed) for seed in (7319,7320,7321,7322)]
G.guard,G.method_bank=old_guard,old_bank
boundary=[]
for label,delta in [('capacity equals initial',{'H':'10'}),('no filling',{'rin':'4'}),('zero initial mass',{'q':'0'}),('equilibrium concentration',{'q':'4'})]:
    params={**minimal['generation']['parameters'],**delta}
    try:G.generate('easy',seed=9041,template='q-336506',parameters=params);result='accepted'
    except Exception as e:result=type(e).__name__+': '+str(e)
    boundary.append({'case':label,'parameters':params,'result':result})
save('runtime-results.json',{'python':platform.python_version(),'sympy':S.__version__,
     'manifest_dependencies':load(PKG/'package.json')['dependencies'],
     'deterministic_replay':all(G.generate('easy',seed=r['generation']['seed'])==r for r in replayed),
     'traced_rejection_attempts':rejects,'traced_outputs':[analyze(r) for r in replayed],
     'boundaries':boundary,'minimum_admitted_case':analyze(minimal)})

# Stored generated instances are reproduced, not inferred from original source questions.
historical=load(PKG/'17592186229183/reference/replenishment/basis-2591/generated.json')
by_id={q[':question/id']:q for q in inv['questions']};affected=[];regenerated=[];inventory_results=[]
for old in historical:
    g=old['generation'];r=G.generate(g['level'],seed=g['seed'],template=g['template'],parameters=g['parameters'],profile=g['profile'])
    qid=r['question'][':question/id'];stored=by_id.get(qid)
    checks={'record_id':qid,'level':g['level'],'matches_historical_question':r['question']==old['question'],
            'generation_metadata_equal':r['generation']==old['generation'],'stored_match':stored is not None}
    if stored:
        checks['prompt_equal']=r['question'][':question/problem']==stored[':question/problem']
        checks['solution_equal']=r['question'][':question/worked-solution']==stored[':question/worked-solution']
        checks['normalized_solution_equal']=normalize_prose(r['question'][':question/worked-solution'])==stored[':question/worked-solution']
        def semantics(q):
            return [(sorted(a[':answer/value'] for a in f[':answer-field/choices']),
                next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key),None)) for f,key in field_answers(q)]
        checks['bank_and_key_equal']=semantics(r['question'])==semantics(stored)
        checks['entity_id']=stored[':db/id'];checks['analysis']=analyze(r)
        if all(checks[k] for k in ('generation_metadata_equal','prompt_equal','normalized_solution_equal','bank_and_key_equal')) and analyze(r)['correct_numeric_rank']==3:
            regenerated.append(r)
            affected.append({'question_id':qid,'entity_id':stored[':db/id'],
                'finding':'Normal method bank makes the third-smallest of five masses correct; all such stored generated questions have this incidental shortcut.',
                'reproduction':f"{sys.executable} {PKG}/17592186229183.py --difficulty {g['level']} --seed {g['seed']} --count 1 --format json (template is {g['template']}); exact parameter API replay: review.py",
                'evidence_path':'generated-records.json'})
    inventory_results.append(checks)
save('generated-records.json',regenerated)
save('affected-inventory.json',{'affected_questions':affected})
save('inventory-results.json',{'basis':inv['basis'],'questions':len(inv['questions']),
     'generated_historical_replays':inventory_results,'affected_generated':len(affected),
     'source_questions_not_marked_generated':len(source['material']['kp'][':knowledge-point/questions']),
     'limitations':'Inventory lacks generation metadata; historical generated records supply it. Replay IDs, prompts, banks and keys match stored entities; solutions match after shared normalize_prose adds scalable parentheses. Raw regenerated records are retained unchanged. All ten generated records tested; original instructional items excluded.'})

# Native grader batch: every option plus controlled old/new equivalent response tests.
grade_records=batch+cf+[minimal]+[samples[i*4] for i in range(len(G.MASKS))]
cases=[]
for i,r in enumerate(grade_records):
    f,key=next(field_answers(r['question']));cases.append({'label':f'independent radio choices {i}', 'record':r,
        'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],
                   'expected':'accepted' if a[':answer/id']==key else 'rejected',
                   'purpose':'mass independently computed from rendered prompt; test correct and every plausible distractor'} for a in f[':answer-field/choices']]})
save('grader-input.json',cases)
# Screenshots include every template, exact complete batch and both counterfactual kinds.
save('render-records.json',batch+cf+[minimal]+[samples[i*4] for i in range(len(G.MASKS))])
save('package-after.json',snapshot())
assert snapshot()==before, 'Package changed'
save('sampling-summary.json',{'sample_count':len(samples),'batch_count':len(batch),
      'by_template':{t:[analyze(r) for r in samples if r['generation']['template']==t] for t in G.MASKS},
      'batch':[analyze(r) for r in batch],'minimal':analyze(minimal),
      'mathematical_argument':'Let B=cH,D=cv-q>0,r=v/H in (0,1),n>0. Correct=B-D*r^n. B and B-D*r^(n+1) exceed correct; B-D*r^(n-1) and B-cv*r^n are below correct. Strict five-way rounded collision rejection preserves this ordering. Therefore correct always has rank 3, regardless of option shuffle, parameters, level, template, rejection or deduplication.',
      'package_unchanged':snapshot()==before})
print(json.dumps({'samples':len(samples),'math_all_pass':all(r['math_pass'] for r in math),
     'median_correct_samples':sum(analyze(r)['correct_numeric_rank']==3 for r in samples),
     'median_correct_batch':sum(analyze(r)['correct_numeric_rank']==3 for r in batch),
     'replay_missing':sum('error' in r for r in replay_results),'affected_inventory':len(affected)}))

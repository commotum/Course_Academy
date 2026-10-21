"""Independent, read-only generator review. Run with the job's venv Python.

All output paths are relative to this file. No package/database writes.
"""
import collections, hashlib, importlib.util, json, pathlib, re, shutil, subprocess, sys
import sympy as S
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor)

HERE=pathlib.Path(__file__).resolve().parent
JOB=HERE.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PKG=JOB/'workspace'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed_generator',PKG/'17592186087877.py')
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
X=S.Symbol('x',positive=True)
Y,V=S.symbols('y yp')
def save(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def snapshot():
    return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in PKG.rglob('*') if p.is_file()}

def group_at(t,i):
    assert t[i]=='{',(t,i)
    depth=1;j=i+1
    while depth:
        if t[j]=='{':depth+=1
        if t[j]=='}':depth-=1
        j+=1
    return t[i+1:j-1],j

def clean(t):
    t=t.replace('\\\\','\\').replace('\\u2061','').replace('\u2061','')
    t=t.replace('\\left','').replace('\\right','').replace('\\,','').replace('\\!','')
    t=t.replace('\\dfrac','\\frac')
    t=re.sub(r'\\(?:text|textrm)\{d\}', 'd', t)
    t=re.sub(r'\\operatorname\{(cos|sin|ln)\}',r'\\\1',t)
    return t

def scalar(t):
    t=clean(t).strip().rstrip('.')
    t=re.sub(r'\\ln\|([^|]+)\|',r'\\ln{\\abs{\1}}',t)
    t=re.sub(r'\\(cos|sin|ln)\s*x\b',r'\\\1{x}',t)
    while '\\frac' in t:
        i=t.rfind('\\frac');j=i+5
        while t[j].isspace():j+=1
        a,j=group_at(t,j)
        while t[j].isspace():j+=1
        b,j=group_at(t,j)
        t=t[:i]+'(('+str(scalar(a))+')/('+str(scalar(b))+'))'+t[j:]
    t=t.replace('\\cdot','*').replace('\\cos',' cos').replace('\\sin',' sin').replace('\\ln',' log').replace('\\abs',' Abs')
    t=t.replace('{','(').replace('}',')').replace('^','**')
    assert '\\' not in t,t
    return parse_expr(t,local_dict={'x':X,'y':Y,'yp':V,'e':S.E,'E':S.E,
        'cos':S.cos,'sin':S.sin,'log':S.log,'Abs':S.Abs},
        transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def equation(t):
    t=clean(t).strip().rstrip('.')
    left,right=t.split('=')
    if left.startswith('\\frac{d}{dx}'):
        f=scalar(left[len('\\frac{d}{dx}'):]);lhs=S.diff(f,X)+S.diff(f,Y)*V
    else:
        left=left.replace('\\frac{dy}{dx}',' (yp) ');lhs=scalar(left)
    return S.expand(lhs-scalar(right))

def normalized(r):
    c=S.expand(r).coeff(V)
    assert c!=0,r
    return S.simplify(r/c)

def prompt_equation(record):
    t=record['question'][':question/problem']
    spans=re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*?)\$',t)
    for a,b in spans:
        v=clean(a or b)
        if '\\frac{dy}{dx}' in v:
            v=v.split(',')[0]
            return v,equation(v)
    raise AssertionError(t)

def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
    c=field(r)[':answer-field/correct']
    return c[':answer/id'] if isinstance(c,dict) else c[1]
def shortcut(r):
    """Read only the answer bank; never read prompt, metadata, or key."""
    candidates=[]
    for a in field(r)[':answer-field/choices']:
        t=clean(a[':answer/value']).split('=')[0]
        m=re.search(r'e\^',t)
        if not m:continue
        h,_=group_at(t,m.end())
        h=scalar(h)
        candidates.append((a[':answer/id'],h))
    winners=[aid for aid,h in candidates if any(S.simplify(h2-2*h)==0 for _,h2 in candidates)]
    return winners[0] if len(winners)==1 else None

def math_check(r):
    text,pr=prompt_equation(r);target=normalized(pr)
    choices=[]
    for a in field(r)[':answer-field/choices']:
        ar=equation(a[':answer/value'])
        choices.append({'id':a[':answer/id'],'valid':S.simplify(normalized(ar)-target)==0})
    good=[a['id'] for a in choices if a['valid']]
    assert good==[key(r)],(r['question'][':question/id'],good,key(r))
    # Check both printed multiply/distribution rows and final product equation.
    blocks=re.findall(r'\$\$\s*([\s\S]*?)\s*\$\$',r['question'][':question/worked-solution'])
    checked=[]
    for b in blocks:
        if '\\begin{aligned}' not in b or '\\int' in b:continue
        b=b.replace('\\begin{aligned}','').replace('\\end{aligned}','')
        for row in b.split('\\\\'):
            row=row.replace('&','').strip()
            rr=equation(row)
            assert S.simplify(normalized(rr)-target)==0,(row,target)
            checked.append(row)
    assert len(checked)==3
    return {'question_id':r['question'][':question/id'],'prompt_equation':text,
            'normalized_residual':str(target),'choices':choices,'solution_rows':checked,'passed':True}

def run():
    before=snapshot();save('package-before.json',before)
    source=load(JOB/'source/source.json');inv=load(JOB/'source/inventory.json')
    save('runner-batch.json',load(JOB/'samples.json'))
    samples=[]
    # Fresh seeds, explicit template stratification, bounded regression sample.
    for i,(t,(level,_)) in enumerate(G.TEMPLATES.items()):
        for j in range(8 if level=='easy' else 2):
            samples.append(G.generate(level,seed=613901+i*101+j,template=t))
    save('samples.json',samples)
    pairs=[]
    for label,params in [('base',{'a':'1','n':2}),('relevant',{'a':'-1','n':2}),
                         ('irrelevant',{'a':'1','n':2})]:
        r=G.generate('easy',seed=8174 if label=='irrelevant' else 8173,template='signed_constant_power',parameters=params)
        pairs.append(r)
    save('counterfactual-records.json',pairs)
    pair_results=[]
    for r in pairs:
        a=next(a for a in field(r)[':answer-field/choices'] if a[':answer/id']==key(r))
        left=clean(a[':answer/value']).split('=')[0]
        factor=S.simplify(scalar(left[len('\\frac{d}{dx}'):])/Y)
        pair_results.append({'question_id':r['question'][':question/id'],'parameters':r['generation']['parameters'],
            'factor_from_printed_correct_equation':str(factor),'math':math_check(r)})
    assert pair_results[0]['factor_from_printed_correct_equation']!=pair_results[1]['factor_from_printed_correct_equation']
    assert pair_results[0]['factor_from_printed_correct_equation']==pair_results[2]['factor_from_printed_correct_equation']
    save('counterfactual-results.json',{'command':f'{sys.executable} {HERE/"audit.py"}',
        'pairs':pair_results,'irrelevance':'Changing only the shuffle seed preserves the entire prompt, solution, correct equation and owned correct answer UUID; choice order alone changes. No substantive ODE datum is irrelevant to the entire transformed equation.'})
    math_rows=[math_check(r) for r in samples+pairs+load(HERE/'runner-batch.json')]
    save('math-results.json',{'command':f'{sys.executable} {HERE/"audit.py"}','cases':math_rows})
    replays=[];replay_checks=[]
    by_ma={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
    for source_id,t,p in G.CASES:
        level=G.TEMPLATES[t][0]
        r=G.generate(level,seed=7791,template=t,parameters=p,profile='observed_raw')
        replays.append(r);q=by_ma[source_id]
        original=q[':question/answer-fields'][0][':answer-field/choices']
        unmatched=list(field(r)[':answer-field/choices']);matches=[]
        for a in original:
            if 'dx^{2}' in clean(a[':answer/value']):
                match=next(b for b in unmatched if 'dx^{2}' in b[':answer/value'])
                method='Malformed dx^2 shape preserved for evidence only, not assigned semantics.'
            else:
                ar=equation(a[':answer/value'])
                match=next(b for b in unmatched if S.simplify(normalized(equation(b[':answer/value']))-normalized(ar))==0)
                method='Independent expanded product equation equivalence'
            unmatched.remove(match);matches.append({'source_answer_id':a[':answer/id'],
                'generated_answer_id':match[':answer/id'],'method':method})
        assert not unmatched
        replay_checks.append({'source_id':q[':question/id'],'ma_id':source_id,'matches':matches,
            'source_solution_present':':question/worked-solution' in q,
            'prompt_matches_normalized_equation':S.simplify(normalized(prompt_equation(r)[1])-normalized(equation(clean(re.search(r'\$\$([\s\S]*?)\$\$|\$([^$]*\\frac\{dy\}[^$]*)\$',q[':question/problem']).group(1) or re.search(r'\$\$([\s\S]*?)\$\$|\$([^$]*\\frac\{dy\}[^$]*)\$',q[':question/problem']).group(2)).split(',')[0])))==0})
    save('source-replay-records.json',replays)
    # Canonical is not in CASES. Inspect reachable easy Q forms independently.
    canonical=source['material']['kp'][':knowledge-point/canonical-example']
    save('source-replay-results.json',{'command':f'{sys.executable} {HERE/"audit.py"}',
        'practice_cases':replay_checks,'canonical_id':canonical[':question/id'],
        'canonical_status':'unsupported: P=2,Q=2 exp(-2x) has no template. Easy Q is cos(bx) or x^n; linear_exp has nonconstant P=2ax and hard has d>=2. No admissible parameters give this canonical equation.',
        'supported_source_corrections':['Negative distributed sign in q-335278 corrected.','Positive half-line added where dividing by x or using logarithmic distractors.']})
    inventory_reproductions=[];affected=[];inventory_checks=[]
    historical=load(PKG/'17592186087877/reference/replenishment/basis-2009/generated.json')
    inv_by_id={q[':question/id']:q for q in inv['questions']}
    for old in historical:
        meta=old['generation'];level=old['question'][':question/difficulty'].split('/')[-1]
        r=G.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
        printed=normalized(prompt_equation(r)[1])
        inv_data=[S.srepr(S.simplify(printed.coeff(Y))),
                  S.srepr(S.simplify(-printed.subs({Y:0,V:0})))]
        r['generation']['inventory_fingerprint']=hashlib.sha256(json.dumps(inv_data).encode()).hexdigest()
        # replenish.py's readback compares unordered banks using ordered().
        # Metadata and every question field must match; bank order is cosmetic.
        field(r)[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
        old_ordered=json.loads(json.dumps(old))
        field(old_ordered)[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
        assert r==old_ordered
        stored=inv_by_id[r['question'][':question/id']]
        assert stored[':question/problem']==r['question'][':question/problem']
        assert stored[':question/worked-solution']==r['question'][':question/worked-solution']
        sf=stored[':question/answer-fields'][0]
        assert sf[':answer-field/correct'][':answer/id']==key(r)
        assert {a[':answer/value'] for a in sf[':answer-field/choices']}=={a[':answer/value'] for a in field(r)[':answer-field/choices']}
        inventory_reproductions.append(r)
        defect=level=='easy' and shortcut(r)==key(r)
        inventory_checks.append({'id':stored[':question/id'],'entity_id':stored[':db/id'],'reproduced':True,'easy_bank_shortcut':defect})
        if defect:affected.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],
            'finding':'Correct exponential is uniquely the one whose doubled exponent also occurs in the bank; ignore the ODE.',
            'reproduction':f'{sys.executable} {HERE/"audit.py"}; generate({level!r}, seed={meta["seed"]}, template={meta["template"]!r}, parameters={meta["parameters"]!r}, profile={meta["profile"]!r}); sort choices by :answer/value as historical delivery does',
            'evidence_path':'generated-records.json'})
    save('generated-records.json',inventory_reproductions)
    save('affected-inventory.json',{'affected_questions':affected})
    save('inventory-results.json',{'basis':inv['basis'],'questions':len(inv['questions']),
        'source_questions_excluded':8,'generated_questions_reproduced':len(inventory_reproductions),
        'checks':inventory_checks,'limits':'All 9 generated inventory records replayed with exact metadata/content/IDs modulo cosmetic bank order; all 3 stored generated easy questions demonstrate the shortcut. Original source questions are not marked generated. Other difficulty shortcut families not exhaustively audited.'})
    all_easy=[r for r in samples if r['question'][':question/difficulty'].endswith('/easy')]
    probes=[]
    for group,rows in [('fresh easy overall',all_easy)]+[(t,[r for r in all_easy if r['generation']['template']==t]) for t in ['constant_cos','scaled_constant_power','signed_constant_power']]+[('runner batch',load(HERE/'runner-batch.json'))]:
        probes.append({'subgroup':group,'correct':sum(shortcut(r)==key(r) for r in rows),'total':len(rows),
            'attempts':[{'question_id':r['question'][':question/id'],'predicted':shortcut(r),'correct':key(r)} for r in rows]})
    save('shortcut-results.json',{'command':f'{sys.executable} {HERE/"audit.py"}',
        'strategy':'From choices only, select exponential e^h for which another exponential e^(2h) appears. Ignore prompt and generation metadata.',
        'baseline':0.2,'probes':probes})
    cases=[]
    for r in samples+pairs+load(HERE/'runner-batch.json'):
        checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],
                 'expected':'accepted' if a[':answer/id']==key(r) else 'rejected',
                 'purpose':'Independently expanded equation equivalence' } for a in field(r)[':answer-field/choices']]
        if r in all_easy or r in pairs:
            checks.append({'submitted_answer_id':shortcut(r),'expected':'accepted','purpose':'Bank-only shortcut succeeds in real learner grader'})
        cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
    save('grader-input.json',cases)
    # Relevant/irrelevant pairs plus a representative of each moderate source.
    render=pairs+[next(r for r in samples if r['generation']['template']==t) for t in ['constant_cos','scaled_constant_power','scaled_reciprocal_cos','linear_sin']]
    save('render-input.json',render)
    rejection=[]
    for label,kwargs in [('zero coefficient',{'parameters':{'a':'0','b':1}}),
             ('unknown template',{'template':'constant_exp'}),('wrong field',{'field_type':'free'}),
             ('outside difficulty',{'template':'linear_sin'}),('large coefficient',{'parameters':{'a':'5','b':1}})]:
        try:G.generate('easy',seed=23,template='constant_cos',**kwargs) if 'template' not in kwargs else G.generate('easy',seed=23,**kwargs)
        except ValueError as e:rejection.append({'case':label,'rejected':True,'message':str(e)})
        else:rejection.append({'case':label,'rejected':False})
    assert all(x['rejected'] for x in rejection)
    replay=all(G.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed'],template=r['generation']['template'])==r for r in samples)
    save('packaging-results.json',{'python':sys.version.split()[0],'sympy':S.__version__,
        'manifest_dependencies':load(PKG/'package.json')['dependencies'],'deterministic_replay':replay,
        'rejection_checks':rejection,'external_outputs':'No file writes in generator; stdout JSON records. Imports only bundled source JSON plus declared sympy and standard library.',
        'package_unchanged':snapshot()==before})
    (HERE/'session-state.md').write_text('Independent source account, source-bank replay, printed math/solution checks, fresh samples, controlled pairs, shortcut probes and inventory reproductions saved. Awaiting delivery, native grader, actual UI rendering, relocation and final report. Package unchanged.\n')
    print(json.dumps({'samples':len(samples),'math_cases':len(math_rows),'source_banks':len(replay_checks),
        'affected_inventory':len(affected),'shortcut_probes':[{k:p[k] for k in ['subgroup','correct','total']} for p in probes]}))

if __name__=='__main__':run()

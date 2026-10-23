import argparse, collections, hashlib, importlib.util, json, pathlib, re, subprocess, sys
sys.dont_write_bytecode = True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
ROOT = pathlib.Path(__file__).resolve().parent
JOB = ROOT.parent
REPO = pathlib.Path('/home/jake/Developer/Course_Academy')
def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, ensure_ascii=False))
def read(p): return json.loads(pathlib.Path(p).read_text())
def load(package):
    spec=importlib.util.spec_from_file_location('reviewed',pathlib.Path(package)/'17592186064206.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def coeff(v):
    v=v.strip()
    if v in ('','-'): return s.Integer(-1 if v=='-' else 1)
    m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',v)
    if m:return (-1 if m[1] else 1)*s.Rational(m[2],m[3])
    return s.Rational(v)
def log(v):
    m=re.fullmatch(r'(.*?)\\operatorname\{ln\}\u2061?\|([^|]+)\|\+C',v)
    if not m: raise ValueError(v)
    return coeff(m[1]),m[2]
def expr(v):return parse_expr(v, transformations=standard_transformations+(implicit_multiplication_application,))
def field(r):return r['question'][':question/answer-fields'][0]
def key(f):
    v=f[':answer-field/correct'];return v[1] if isinstance(v,list) else v[':answer/id']
def shortcut(r):
    # No prompt, generation metadata, key, position or IDs consulted for the decision.
    choices=field(r)[':answer-field/choices']; parts=[log(a[':answer/value']) for a in choices]
    if len(set(arg for c,arg in parts))==1:
        if sum(bool(c<0) for c,arg in parts)==3:
            eligible=[i for i,(c,arg) in enumerate(parts) if -1<c<0];cue='same argument; three negatives: choose negative proper fraction'
        else:
            largest=max(c for c,arg in parts)
            eligible=[i for i,(c,arg) in enumerate(parts) if c==largest];cue='same argument; two negatives: choose largest positive coefficient'
    else:
        eligible=[i for i,(c,arg) in enumerate(parts) if c==1 and arg!='x'];cue='mixed arguments: choose positive unit coefficient with shifted argument'
    return (choices[eligible[0]][':answer/id'] if len(eligible)==1 else None),cue
def probe(records):
    rows=[]
    for r in records:
        chosen,cue=shortcut(r)
        rows.append({'id':r['question'][':question/id'],'template':r['generation']['template'],'cue':cue,'selected':chosen,'correct':chosen==key(field(r))})
    groups={}
    for attr in ['cue','template']:
        for value in sorted(set(row[attr] for row in rows)):
            sub=[row for row in rows if row[attr]==value]
            groups[attr+':'+value]={'correct':sum(row['correct'] for row in sub),'total':len(sub),'baseline':0.2}
    return {'correct':sum(row['correct'] for row in rows),'total':len(rows),'groups':groups,'records':rows}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--package',default=str(JOB/'workspace'));ap.add_argument('--candidate-records');args=ap.parse_args()
    if args.candidate_records:
        result=probe(read(args.candidate_records));save('candidate-shortcuts.json',result);print(json.dumps({k:v for k,v in result.items() if k!='records'}));return
    m=load(args.package)
    source=read(JOB/'source/source.json');source_rows=[];replays=[]
    for q in source['material']['kp'][':knowledge-point/questions']:
        sid=q[':question/math-academy-id']
        if sid not in m.PROFILES:
            source_rows.append({'source_id':q[':question/id'],'template':sid,'status':'unsupported','inferred_answer':r'\frac{2}{3}\ln|3x+5|+C','reason':'Captured bank present; key and solution missing. Affine positive slope is taught by canonical example.'});continue
        r=m.generate(template=sid,parameters=m.PROFILES[sid]['parameters'],seed=46391);replays.append(r)
        q2=r['question'];f=field(r)
        source_rows.append({'source_id':q[':question/id'],'template':sid,'status':'passed' if q[':question/problem']==q2[':question/problem'] and q[':question/worked-solution']==q2[':question/worked-solution'] and sorted(c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(c[':answer/value'] for c in f[':answer-field/choices']) else 'failed'})
    rejects=[]
    for sid,par in [('q-15707',[3,5,2]),('q-49511',[2,3,5]),('q-49452',[1,0,2]),('q-15707',[1,1,1]),('q-49452',[1,-10,2])]:
        try:m.generate(template=sid,parameters=par);err=None
        except Exception as e:err=type(e).__name__+': '+str(e)
        rejects.append({'template':sid,'parameters':par,'error':err})
    save('source-replay.json',{'checks':source_rows,'canonical_rejected':rejects[0],'records':replays,'rejections':rejects})
    samples=[m.generate(seed=i) for i in range(46391,46431)]
    boundaries={'q-15707':[[2,1,1],[9,1,12]],'q-49453':[[2,1,1],[9,1,12]],'q-49452':[[1,-2,1],[1,-9,12]],'q-49450':[[1,1,-1],[1,1,-12]],'q-49454':[[1,1,2],[1,1,12]]}
    for sid,pars in boundaries.items():
        samples.extend(m.generate(template=sid,parameters=p,seed=804) for p in pars)
    pair_records=[m.generate(template='q-15707',parameters=[n,1,5],seed=8301) for n in [2,3]]
    pair_records.append(m.generate(template='q-49453',parameters=[2,1,5],seed=8301))
    pair_records.extend(m.generate(template='q-49452',parameters=[1,a,5],seed=8301) for a in [-2,-3])
    save('counterfactual-records.json',pair_records)
    save('samples.json',samples);save('batch.json',read(JOB/'samples.json'))
    save('render-records.json',pair_records+[m.generate(template='q-49450',parameters=[1,1,-8],seed=8301),m.generate(template='q-49454',parameters=[1,1,8],seed=8301)])
    checks=[];grader=[]
    for r in samples+read(JOB/'samples.json')+pair_records:
        q=r['question'];f=field(r);match=re.search(r'\\frac\{(\d+)\}\{([^}]+)\}',q[':question/problem']);n=s.Integer(match[1]);d=expr(match[2]);x=s.Symbol('x');integrand=n/d
        answers=[];gchecks=[]
        for ch in f[':answer-field/choices']:
            c,arg=log(ch[':answer/value']);arg=expr(arg);residual=s.cancel(c*s.diff(arg,x)/arg-integrand);valid=residual==0
            answers.append({'value':ch[':answer/value'],'residual':str(residual),'valid':valid,'key_agrees':valid==(ch[':answer/id']==key(f))})
            gchecks.append({'submitted_answer_id':ch[':answer/id'],'expected':'accepted' if valid else 'rejected','purpose':'independent differentiation of rendered choice'})
        checks.append({'id':q[':question/id'],'prompt':q[':question/problem'],'answers':answers,'unique_correct':sum(a['valid'] for a in answers)==1,'solution_contains_expected_final':next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key(f)) in q[':question/worked-solution']})
        grader.append({'label':q[':question/id'],'record':r,'checks':gchecks})
    save('math.json',checks);save('grader-input.json',grader)
    save('shortcuts.json',{'independent_samples':probe(samples),'runner_batch':probe(read(JOB/'samples.json'))})
    a,b,c,neg2,neg3=pair_records
    val=lambda r:next(ch[':answer/value'] for ch in field(r)[':answer-field/choices'] if ch[':answer/id']==key(field(r)))
    save('counterfactuals.json',{'relevant':{'parameters_before':[2,1,5],'parameters_after':[3,1,5],'answers':[val(a),val(b)],'answer_changed':val(a)!=val(b),'prompts_changed':a['question'][':question/problem']!=b['question'][':question/problem'],'solutions_changed':a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']},'slope':{'answers':[val(neg2),val(neg3)],'expected':'-1/2 changes to -1/3'},'irrelevant':{'change':'q-15707 versus q-49453 prompt wording, identical [2,1,5]','answer_preserved':val(a)==val(c),'prompt_changed':a['question'][':question/problem']!=c['question'][':question/problem']}})
    save('packaging.json',{'python':sys.version.split()[0],'sympy':s.__version__,'manifest':read(pathlib.Path(args.package)/'package.json')['dependencies'],'deterministic':m.batch('easy',5,994860459)==m.batch('easy',5,994860459),'runner_batch_replay':m.batch('easy',5,994860459)==read(JOB/'samples.json'),'boundary_rejections':rejects,'seed':46391,'sample_count':len(samples)})
    inv=read(JOB/'source/inventory.json');original_ids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
    save('inventory-review.json',{'basis':inv['basis'],'count':len(inv['questions']),'original_source_count':sum(q[':question/id'] in original_ids for q in inv['questions']),'generated_count':sum(q[':question/id'] not in original_ids for q in inv['questions']),'result':'No stored generated records in captured inventory; all six IDs match original source. Incomplete q-49511 lacks correct key and worked solution and is not usable practice. Original source records are not marked generated or proposed for repair.','records':[{'id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in original_ids,'retired':q.get(':question/retired',False),'has_solution':bool(q.get(':question/worked-solution')),'has_key':bool(q[':question/answer-fields'][0].get(':answer-field/correct'))} for q in inv['questions']]})
    save('affected-inventory.json',{'affected_questions':[]})
    print(json.dumps({'math_records':len(checks),'math_failed':sum(not c['unique_correct'] or not all(a['key_agrees'] for a in c['answers']) for c in checks),'source':[(r['template'],r['status']) for r in source_rows],'sample_shortcut':probe(samples)['correct'],'batch_shortcut':probe(read(JOB/'samples.json'))['correct']}))
if __name__=='__main__':main()

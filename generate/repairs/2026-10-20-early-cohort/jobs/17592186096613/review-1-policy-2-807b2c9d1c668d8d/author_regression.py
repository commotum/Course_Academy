"""Retained finding 6bbaf15dc6703e79f686: current generator source coverage.

No historical batch is read. Default run generates current CLI and directed cases,
then tests them before/after the real shared delivery filter. --input reads any
prospective or accepted array with the same independent visible-math checks.
"""
import argparse, collections, importlib.util, json, os, pathlib, re, subprocess, sys
sys.dont_write_bytecode = True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
ROOT = pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186096613/workspace')
REPO = pathlib.Path('/home/jake/Developer/Course_Academy')
JOB = ROOT.parent
OUT = pathlib.Path(__file__).resolve().parent / 'author-regression'
OUT.mkdir(exist_ok=True)
x = sp.Symbol('x', positive=True)
spec = importlib.util.spec_from_file_location('candidate', ROOT/'17592186096613.py')
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

def save(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')

def parse(s):
    s = s.replace(r'\dfrac', r'\frac').replace(r'\operatorname{ln}', r'\ln').replace('\u2061', '').replace(r'\,', '').replace(r'\cdot', '*').replace(r'\left', '').replace(r'\right', '').strip().rstrip('.,')
    s = s.replace(r'\frac{\text{d}}{\text{d}x}', 'D')
    def group(i):
        assert s[i] == '{', s
        start=i+1; depth=1; i+=1
        while depth:
            depth+=(s[i]=='{')-(s[i]=='}'); i+=1
        return s[start:i-1],i
    while r'\frac' in s:
        i=s.rfind(r'\frac'); a,j=group(i+5); b,j=group(j)
        s=s[:i]+'(('+a+')/('+b+'))'+s[j:]
    s=re.sub(r'(?:\\ln|ln)\s*x', ' log(x)', s).replace('^','**').replace('{','(').replace('}',')')
    assert '\\' not in s, s
    return parse_expr(s,local_dict={'x':x,'e':sp.E,'log':sp.log,'D':lambda a:sp.diff(a,x)}, transformations=standard_transformations+(implicit_multiplication_application,))

def target(r):
    return sp.diff(parse(re.search(r'\$y\s*=\s*(.*?)\$',r['question'][':question/problem'])[1]),x)
def field(r): return r['question'][':question/answer-fields'][0]
def key(r):
    f=field(r)
    return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def equal(a,b): return sp.simplify(a-b)==0

def inspect(r):
    q=r['question']; t=target(r); f=field(r); choices=f[':answer-field/choices']
    assert equal(parse(key(r)[':answer/value']),t), q[':question/id']
    vals=[parse(a[':answer/value']) for a in choices]
    radio=f[':answer-field/type'].endswith('/radio')
    if radio:
        assert len(vals)==5 and sum(equal(a,t) for a in vals)==1
        assert all(not equal(a,b) for i,a in enumerate(vals) for b in vals[:i])
    else: assert all(equal(a,t) for a in vals)
    blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'], re.S)
    lhs,rhs=blocks[0].split('='); assert equal(parse(lhs),parse(rhs))
    aligned=re.sub(r'\\(?:begin|end)\{aligned\}', '', blocks[-1])
    rows=aligned.split(r'\\')
    for row in rows:
        assert equal(parse(row.split('=')[-1]),t), row
    quotient=bool(re.search(r'\\frac\{\\ln x\}\{\d+\}',q[':question/problem']))
    if quotient:
        assert len(rows)==5, 'Quotient rewriting step missing'
        assert 'D' in rows[1].replace(r'\frac{\text{d}}{\text{d}x}', 'D')
        assert r'\ln x' in rows[1] and r'\frac{1}{' in rows[1]
    checks=[]
    if radio:
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if equal(v,t) else 'rejected','purpose':'Independent derivative of visible prompt'} for a,v in zip(choices,vals)]
    else:
        checks=[{'submitted':s,'expected':expect,'purpose':'Equivalent derivative or incorrect signed coefficient'} for s,expect in [(str(t),'accepted'),(sp.latex(t),'accepted'),(str(t).replace('/x','*x^(-1)'),'accepted'),(str(-t),'rejected'),('0','rejected'),(str(t*x),'rejected')]]
    return {'label':q[':question/id'],'record':r,'checks':checks}

def coverage(records):
    by=collections.defaultdict(list)
    for r in records:
        q=r['question']; f=field(r)
        # Read learner-visible presentation, not metadata labels.
        text=q[':question/problem']; t=target(r)
        if re.search(r'\\frac\{\\ln x\}\{\d+\}',text): family='quotient'
        elif f[':answer-field/type'].endswith('/blank'): family='blank'
        elif 'e' in re.search(r'\$y\s*=\s*(.*?)\$',text)[1]: family='euler'
        elif r'\frac' in re.search(r'\$y\s*=\s*(.*?)\$',text)[1]: family='fraction'
        else: family='integer'
        pos=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==key(r)[':answer/id'])
        by[family].append((str(t),pos,bool(t.subs(x,1)>0)))
    return {family:{'records':len(vals),'semantic_derivatives':len(set(v[0] for v in vals)), 'key_positions':dict(collections.Counter(v[1] for v in vals)), 'positive_keys':sum(v[2] for v in vals), 'always_first_successes':sum(v[1]==0 for v in vals),'always_positive_successes':sum(v[2] for v in vals),'radio_position_baseline':0.2 if family!='blank' else None} for family,vals in by.items()}

def delivery(name):
    cmd=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(OUT/(name+'.json')),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty','easy','--output',str(OUT/('delivery-'+name)),'--asset-root',str(OUT/'assets'),'--math-root','/media/jake/SSD/EDB/math']
    result=subprocess.run(cmd,capture_output=True,text=True)
    (OUT/('delivery-'+name+'.log')).write_text(result.stdout+result.stderr)
    assert result.returncode==0, result.stdout+result.stderr
    return json.loads((OUT/('delivery-'+name)/'accepted.json').read_text())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=pathlib.Path);args=ap.parse_args()
    if args.input:
        records=json.loads(args.input.read_text())
        for r in records:inspect(r)
        print(json.dumps({'input':str(args.input),'checked':len(records),'coverage':coverage(records)}));return
    # The original minimal failure is always exercised against current code.
    inspect(g.generate_easy(seed=917,parameters={'n':1,'d':4,'k':0}))
    source=json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
    anchors={'q-11909':(7,1,0),'q-11910':(2,3,0),'q-339941':(-11,1,0),'q-70881':(2,1,0),'q-101600':(2,1,1),'q-101604':(-9,1,0),'q-308849':(8,1,0),'q-339949':(11,4,0),'q-339950':(-7,3,0),'q-70887':(1,4,0),'q-70889':(6,1,1)}
    replays=[]
    for q in source:
        sid=q[':question/math-academy-id']; n,d,k=anchors[sid]
        r=g.generate_easy(seed=917,profile='raw-'+sid,parameters=dict(n=n,d=d,k=k)); replays.append(r)
        out=r['question']
        assert q[':question/problem']==out[':question/problem'],sid
        assert q.get(':question/worked-solution')==out.get(':question/worked-solution'),sid
        assert q.get(':question/difficulty',{}).get(':db/ident')==out.get(':question/difficulty'),sid
        for a,b in zip(q.get(':question/answer-fields',[]),out.get(':question/answer-fields',[]),strict=True):
            assert a[':answer-field/type'][':db/ident']==b[':answer-field/type']
            assert a[':answer-field/key']==b[':answer-field/key']
            assert sorted(v[':answer/value'] for v in a[':answer-field/choices'])==sorted(v[':answer/value'] for v in b[':answer-field/choices']),sid
            assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
            if ':answer-field/correct' in a: assert equal(parse(a[':answer-field/correct'][':answer/value']),parse(key(r)[':answer/value']))
    save('source-replays.json',replays)
    focused=[g.generate_easy(seed=170+d+s,profile='quotient',parameters=dict(n=s,d=d,k=0)) for s in (-1,1) for d in range(2,13)]
    focused += [g.generate_easy(seed=25,profile=p,parameters=dict(n=s,d=4,k=0)) for p in ('canonical','equivalent-entry') for s in (-1,1)]
    pairs=[]
    for profile,params,changed in [('quotient',(1,4,0),(1,5,0)),('quotient',(1,4,0),(-1,4,0)),('integer',(7,1,0),(-7,1,0)),('fraction',(2,3,0),(4,3,0)),('euler',(6,1,1),(-6,1,1)),('canonical',(1,4,0),(-1,4,0)),('equivalent-entry',(1,4,0),(1,5,0))]:
        make=lambda p,seed:g.generate_easy(seed=seed,profile=profile,parameters=dict(zip(('n','d','k'),p)))
        a,b,c=make(params,53),make(changed,53),make(params,54)
        assert not equal(target(a),target(b)) and equal(target(a),target(c))
        assert key(a)[':answer/value']!=key(b)[':answer/value'] and key(a)[':answer/value']==key(c)[':answer/value']
        pairs.append({'profile':profile,'before':a,'relevant_after':b,'irrelevant_after':c})
    save('counterfactuals.json',pairs)
    cmd=[sys.executable,str(ROOT/'17592186096613.py'),'--difficulty','easy','--count','5','--seed','3129290382','--format','json']
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(OUT/'assets')}
    batch=json.loads(subprocess.check_output(cmd,env=env));save('prospective-batch.json',batch)
    assert json.loads(subprocess.check_output(cmd,env=env))==batch
    cmd[cmd.index('--count')+1]='32';cmd[cmd.index('--seed')+1]='89321'
    normal=json.loads(subprocess.check_output(cmd,env=env))
    assert 'quotient' in coverage(normal),'Normal CLI cannot reach the quotient family'
    records=focused+normal+[r for pair in pairs for k,r in pair.items() if k!='profile']
    save('focused-samples.json',records)
    cases=[inspect(r) for r in records+batch]
    accepted=delivery('focused-samples');accepted_batch=delivery('prospective-batch')
    cases.extend(inspect(r) for r in accepted+accepted_batch)
    pre,post=coverage(records),coverage(accepted)
    for c in (pre,post):
        assert c['quotient']['semantic_derivatives']>=20
        assert 0<c['quotient']['positive_keys']<c['quotient']['records']
        for fam,v in c.items():
            if fam!='blank' and v['records']>=5: assert len(v['key_positions'])>1,(fam,v)
    for pair in pairs:
        if field(pair['relevant_after'])[':answer-field/type'].endswith('/blank'):
            cases.append({'label':'stale-'+pair['profile'],'record':pair['relevant_after'],'checks':[{'submitted':key(pair['before'])[':answer/value'],'expected':'rejected','purpose':'Reject old derivative after relevant evidence changes'}]})
    save('grader-input.json',cases)
    save('render-records.json',[focused[0],focused[13],pairs[0]['before'],pairs[0]['relevant_after'],pairs[1]['relevant_after']])
    report={'finding':'6bbaf15dc6703e79f686','passed':True,'source_replays':len(replays),'complete_source_banks':sum(bool(r['question'].get(':question/answer-fields')) for r in replays),'math_records_before':len(records)+len(batch),'math_records_after':len(accepted)+len(accepted_batch),'before':pre,'after':post,'requested_batch_before':coverage(batch),'requested_batch_after':coverage(accepted_batch),'counterfactuals':len(pairs),'cli_commands':[cmd],'deterministic_replay':True,'limitations':['Delivery uses captured inventory. Actual learner history and configured weights are unavailable; no live draws are claimed.','Position/sign probes test these incidental predictors, not every possible heuristic. Identifying the reciprocal of the displayed signed constant is the intended rule.']}
    save('regression-results.json',report)
    print(json.dumps({k:report[k] for k in ('passed','source_replays','complete_source_banks','math_records_before','math_records_after','counterfactuals')}))
if __name__=='__main__':main()

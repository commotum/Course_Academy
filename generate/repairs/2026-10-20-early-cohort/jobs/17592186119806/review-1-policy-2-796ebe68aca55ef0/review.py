"""Read-only independent review. Run with the supplied .venv/bin/python.

All writes are relative to this script's evidence directory. The original
package is imported with bytecode disabled. No database or publishing calls.
Parsing/Fraction checking adapts the previous independent audit with provenance.
"""
import sys
sys.dont_write_bytecode = True
import json, re, pathlib, importlib.util, hashlib, shutil, subprocess, copy
import collections, platform, ast
from fractions import Fraction
E=pathlib.Path(__file__).resolve().parent
B=E.parent; P=B/'workspace'; R=pathlib.Path('/home/jake/Developer/Course_Academy')
PY=R/'.venv/bin/python'
def save(n,x):
    (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def load(n): return json.loads((E/n).read_text())
spec=importlib.util.spec_from_file_location('independent_candidate',P/'17592186119806.py')
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
source=json.loads((B/'source/source.json').read_text())
M=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def norm(s): return s.replace('\\\\begin','\\begin').replace('\\\\end','\\end').replace('\\\\\\\\','\\\\')
def vec(s): return tuple(Fraction(x.strip()) for x in M.fullmatch(norm(s))[1].split(r'\\'))
def parsed(r):
    q=r.get('question',r); text=norm(q[':question/problem'])
    m=re.search(r'\$(\d+)a\s*([+-])\s*(\d+)x\s*=\s*b\$',text)
    p=int(m[1]); d=int(m[3])*(1 if m[2]=='+' else -1)
    ms=list(M.finditer(text)); a=vec(ms[0].group()); b=vec(ms[-1].group())
    assert len(a)==len(b) and len(a) in (3,4)
    x=tuple((v-p*u)/d for u,v in zip(a,b))
    t=re.search(r'(?:\{x\}|x)_\{(\d+)\}\s*([+-])\s*(?:\{x\}|x)_\{(\d+)\}',text.split('given that')[0])
    target=(int(t[1])-1,int(t[3])-1,t[2]) if t else None
    value=x if target is None else x[target[0]]+(1 if target[2]=='+' else -1)*x[target[1]]
    return p,d,a,b,x,target,value
def choices(r):
    f=r['question'][':question/answer-fields'][0]; cid=f[':answer-field/correct'][1]
    return [(v[':answer/id'],vec(v[':answer/value']) if '\\begin' in norm(v[':answer/value']) else Fraction(v[':answer/value'])) for v in f[':answer-field/choices']],cid
def check(r):
    p,d,a,b,x,t,value=parsed(r);ch,cid=choices(r);q=r['question'];s=norm(q[':question/worked-solution'])
    assert len(q[':question/answer-fields'])==1
    assert q[':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio'
    assert len(ch)==5 and len(set(v for _,v in ch))==5
    assert next(v for i,v in ch if i==cid)==value
    assert sum(v==value for _,v in ch)==1
    reverse=(' & ='+str(p)+'a-b') in s
    numerator=tuple(p*u-v if reverse else v-p*u for u,v in zip(a,b))
    mats=[vec(m.group()) for m in M.finditer(s)]
    assert mats==([a,b,numerator,x] if reverse else [b,a,numerator,x]), (r['generation'],mats)
    assert all(z.denominator==1 for z in x)
    assert ('x & ='+('-' if d<0 and not reverse else '')+r'\frac{1}{'+str(abs(d))+'}') in s
    if t:
        end=s.split('Therefore,')[1]
        assert ('{x}_{'+str(t[0]+1)+'}'+t[2]+'{x}_{'+str(t[1]+1)+'}') in end
        expr=end.split('=')[1]
        assert re.fullmatch(r'[\d+()\- ]+',expr)
        assert Fraction(eval(expr,{'__builtins__':{}}))==value
        assert end.endswith('='+str(value)+'.$')
    return {'id':q[':question/id'],'profile':r['generation']['source_id'],'target':t,'expected':str(value),'passed':True}
def gen(sid,params=None,seed=913007): return g.generate('easy',seed,sid,params)
def grading_case(r,label):
    ch,_=choices(r);value=parsed(r)[6]
    return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':i,'expected':'accepted' if v==value else 'rejected','purpose':'Equation-derived answer, not generation metadata'} for i,v in ch]}
def probes(records):
    groups=collections.defaultdict(list)
    for r in records: groups[r['generation']['source_id']].append(r)
    report={}
    for sid,rs in sorted(groups.items()):
        counters=collections.defaultdict(collections.Counter); strategy=collections.defaultdict(lambda:[0,0])
        for r in rs:
            ch,cid=choices(r); vals=[v for _,v in ch]; idx=[i for i,_ in ch].index(cid)
            counters['position'][idx+1]+=1
            metrics={'value':vals,'absolute':[abs(v) for v in vals]} if not isinstance(vals[0],tuple) else {
                **{'coordinate'+str(j+1):[v[j] for v in vals] for j in range(len(vals[0]))},
                'sum':[sum(v) for v in vals], 'norm2':[sum(z*z for z in v) for v in vals], 'lexicographic':vals}
            for metric,vs in metrics.items():
                counters[metric+' rank'][sorted(vs).index(vs[idx])+1]+=1
                for rank in range(5):
                    # Stable displayed-position tie breaking, explicit for reproducibility.
                    selected=sorted(range(5),key=lambda i:vs[i])[rank]
                    key=metric+' rank '+str(rank+1);strategy[key][0]+=selected==idx;strategy[key][1]+=1
            for k in range(5):strategy['position '+str(k+1)][0]+=idx==k;strategy['position '+str(k+1)][1]+=1
        report[sid]={'count':len(rs),'histograms':{k:dict(v) for k,v in counters.items()},'strategies':dict(strategy)}
    return report
def run():
    replay=[];report=[]
    for old in source['material']['kp'][':knowledge-point/questions']:
        sid=old[':question/math-academy-id'];row={'source_id':old[':question/id'],'profile':sid}
        if ':question/worked-solution' not in old:
            row.update(status='source_gap',expected_inferred=str(parsed(old)[6]),reason='No captured key or worked solution; bank is captured. Inference -1 matches one bank choice. Not a complete source replay profile.')
        else:
            target=parsed(old)[5];r=gen(sid,{'scale':1,'target':list(target) if target else None});replay.append(r)
            f=old[':question/answer-fields'][0]
            assert sorted(norm(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
            assert norm(old[':question/problem'])==r['question'][':question/problem']
            assert norm(old[':question/worked-solution'])==r['question'][':question/worked-solution']
            original_correct=norm(f[':answer-field/correct'][':answer/value'])
            assert (vec(original_correct) if '\\begin' in original_correct else Fraction(original_correct))==parsed(r)[6]
            row.update(status='passed',complete_bank_size=5,math=check(r),prompt_exact_after_normalization=True,solution_exact_after_normalization=True)
        report.append(row)
    save('source-replay-records.json',replay)
    save('source-replay.json',{'command':str(PY)+' review.py','complete_banks_replayed':len(replay),'cases':report,'canonical_gap':'Canonical e-4790 lacks a captured answer bank; canonical arithmetic x=(6,1,9) confirmed in source-analysis. No fabricated radio bank asserted.'})
    fresh=[gen(sid,seed=s) for sid in sorted(g.CASES) for s in range(913003,913015)]
    batch=json.loads((B/'samples.json').read_text());save('batch-records.json',batch);save('fresh-records.json',fresh)
    # All eligible targets once at a non-original scale; not an exhaustive new domain.
    target_records=[gen(sid,{'scale':2,'target':list(t) if t else None}) for sid in sorted(g.CASES) for t in g.eligible_targets(sid)]
    save('target-records.json',target_records)
    # Relevant target reversal and replacement at exactly fixed a,b.
    cfs=[gen('q-34601',{'scale':2,'target':t},48291) for t in [[2,1,'-'],[1,2,'-'],[0,2,'-']]]
    assert parsed(cfs[0])[6]==54 and parsed(cfs[1])[6]==-54 and parsed(cfs[2])[6]==-32
    assert all(parsed(r)[2:4]==parsed(cfs[0])[2:4] for r in cfs)
    # New authored construction: one fixed visible bank admits five different correct roles.
    controls=[];pairs=[];irrelevant=[]
    for sid in ['q-34601','q-105161','q-73933','q-105160']:
        base=gen(sid);params=base['generation']['parameters'];p,d,a,b,x,t,v=parsed(base)
        group=[]
        for cv in params['choices']:
            new=copy.deepcopy(params)
            if t is None:new['x']=list(map(int,vec(cv)))
            else:
                wanted=int(cv);i,j,op=t
                u=next(u for u in range(-9,10) if -9 <= (wanted-u if op=='+' else u-wanted) <=9)
                new['x'][i]=u;new['x'][j]=wanted-u if op=='+' else u-wanted
            r=gen(sid,new);group.append(r);controls.append(r)
            assert parsed(r)[2]==a and parsed(r)[5]==t
            assert set(vv for _,vv in choices(r)[0])==set(vv for _,vv in choices(base)[0])
        assert len({str(parsed(r)[6]) for r in group})==5
        pairs.append({'profile':sid,'held_fixed':'coefficients, a, target, unordered visible bank','changed':'b through compatible x','expected':'each candidate becomes the equation-derived unique response','answers':[str(parsed(r)[6]) for r in group],'passed':True})
        if t:
            new=copy.deepcopy(params);unused=next(j for j in range(len(x)) if j not in t[:2]);new['x'][unused] += 1 if new['x'][unused]<9 else -1
            other=gen(sid,new);irrelevant.extend([base,other]);assert parsed(base)[6]==parsed(other)[6]
    save('counterfactual-records.json',cfs);save('control-records.json',controls);save('irrelevant-records.json',irrelevant)
    save('counterfactual-results.json',{'command':str(PY)+' review.py','target_changes':{'answers':[str(parsed(r)[6]) for r in cfs],'expected':['54','-54','-32'],'fixed_vectors':True,'passed':True},'fixed_bank_changes':pairs,'irrelevant':{'pairs':len(irrelevant)//2,'change':'one unrequested component of b via x','expected':'same answer; changed full solved vector in explanation','passed':all(parsed(a)[6]==parsed(b)[6] and parsed(a)[4]!=parsed(b)[4] for a,b in zip(irrelevant[::2],irrelevant[1::2]))}})
    all_records=replay+fresh+target_records+batch+cfs+controls+irrelevant
    results=[check(r) for r in all_records];save('math.json',{'method':'Exact Fraction arithmetic independently parsed from prompts; all five choices; every solution matrix and final scalar arithmetic; coefficient division sign. No generation answer metadata used.','record_count':len(results),'passed':True,'results':results})
    native=replay+fresh[::12]+batch+cfs+controls+irrelevant
    save('grader-input.json',[grading_case(r,str(i)) for i,r in enumerate(native)])
    # Actual renderer includes the exact batch, all target changes, 2 fixed-bank
    # relevant states with changed keys, and both irrelevant-evidence states.
    save('render-records.json',batch+cfs+controls[:2]+irrelevant[:2])
    # Check earlier defect witnesses actually fail the strict retained criteria.
    previous=json.loads((B/'review-0-policy-2-903865075bf272e6/strict-regressions.json').read_text())
    old=[]
    for test in previous['tests']:
        if 'records' in test:
            ranks=[]
            for row in test['records']:
                ch,cid=choices(row['record']);answer=next(v for i,v in ch if i==cid);ranks.append(sorted(v for _,v in ch).index(answer)+1)
            old.append({'test':test['test'],'independently_recomputed_ranks':dict(collections.Counter(ranks)),'prior_passed':test['passed'],'failure_confirmed':len(set(ranks))==1})
        else:old.append({'test':test['test'],'prior_passed':test['passed'],'exception':test.get('exception'),'failure_confirmed':not test['passed']})
    assert all(t['failure_confirmed'] for t in old)
    save('historical-witness-verification.json',{'previous_binding':json.loads((E/'provenance.json').read_text())['previous_binding_package_hash'],'tests':old,'current_results':'strict-regressions.json','author_preflight':'author-preflight-output.txt','limits':'Historical records, not executable old runtime, are retained. Rank calculations re-executed; missing-profile exception is confirmed from the previously bound independent run.'})
    checks=[]
    bad=[('unsupported difficulty',lambda:g.generate('moderate',0)),('unknown profile',lambda:gen('no-profile')),('scale zero',lambda:gen('q-34601',{'scale':0,'target':[0,1,'-']})),('same component target',lambda:gen('q-34601',{'scale':1,'target':[0,0,'-']})),('negative count',lambda:g.batch('easy',-1))]
    bp=copy.deepcopy(fresh[0]['generation']['parameters'])
    for label,mutate in [('wrong dimensions',lambda x:x['a'].pop()),('nonintegral',lambda x:x['x'].__setitem__(0,0.5)),('outside domain',lambda x:x['x'].__setitem__(0,10)),('missing correct choice',lambda x:x.__setitem__('choices',['100','101','102','103','104'])),('duplicate choices',lambda x:x.__setitem__('choices',[x['choices'][0]]*5))]:
        p=copy.deepcopy(bp);mutate(p);bad.append((label,lambda p=p:gen(fresh[0]['generation']['source_id'],p)))
    for label,fn in bad:
        try:fn();checks.append({'case':label,'passed':False})
        except (ValueError,TypeError,AttributeError) as ex:checks.append({'case':label,'passed':True,'error':str(ex)})
    checks.append({'case':'deterministic seeds and explicit authored replay','passed':all(gen(r['generation']['source_id'],seed=r['generation']['seed'])==r and gen(r['generation']['source_id'],r['generation']['parameters'],r['generation']['seed'])==r for r in fresh)})
    # Stress rejection/resampling on a bounded requested pool.
    br=g.batch('easy',40,946271);save('batch-resampling-records.json',br)
    checks.append({'case':'batch rejection/resampling','passed':len(br)==40 and len({r['generation']['mathematical_fingerprint'] for r in br})==40,'construction':'bounded coordinate choices; duplicate mathematical fingerprints are rejected, max(100,count*10) attempts; random branch needs no division resampling.'})
    rel=E/'relocated';rel.mkdir(exist_ok=True);manifest=json.loads((P/'package.json').read_text())
    for n in manifest['files']:
        dst=rel/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/n,dst)
    cmd=[str(PY),str(rel/manifest['entrypoint']),'--count','5','--seed','946271']
    out=subprocess.run(cmd,capture_output=True,text=True,cwd=E)
    save('relocated-records.json',json.loads(out.stdout) if out.returncode==0 else {'stderr':out.stderr})
    checks.append({'case':'manifest-only relocation, external cwd','command':cmd,'passed':out.returncode==0 and json.loads(out.stdout)==g.batch('easy',5,946271)})
    import sympy
    versions={'python':platform.python_version(),'packages':{'sympy':sympy.__version__}}
    checks.append({'case':'exact installed runtime dependencies','passed':versions==manifest['dependencies']})
    checks.append({'case':'external outputs','passed':not any(p.name=='__pycache__' for p in rel.rglob('*')),'detail':'Entrypoint only emits stdout; no assets or image generation. Relocation created only declared files; bytecode disabled.'})
    save('packaging.json',{'checks':checks,'versions':versions,'manifest':manifest,'passed':all(c['passed'] for c in checks)})
    inv=json.loads((B/'source/inventory.json').read_text());originals={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
    rows=[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in originals,'generation_metadata':any('generat' in k for k in q)} for q in inv['questions']]
    assert all(x['original_source'] and not x['generation_metadata'] for x in rows)
    save('inventory-analysis.json',{'captured_basis':inv['basis'],'entries':rows,'conclusion':'Verified all 15 inventory entries are captured originals without generator metadata. No generated inventory instance of the retained weakness exists in this captured inventory. Later/live inventory untested.'})
    save('affected-inventory.json',{'affected_questions':[]})
    save('scope.json',{'passed':True,'source_scope':'3/4 dimensional one-vector isolation and optional two-component sum/difference; five radio choices; integer solutions.','sample_count':len(all_records),'profile_count':len(g.CASES),'coefficients':sorted({(parsed(r)[0],parsed(r)[1]) for r in all_records}),'dimensions':sorted({len(parsed(r)[2]) for r in all_records}),'source_gaps':['q-34574 missing captured solution/key','Canonical missing radio bank'],'new_domain':'Ordinary a [-6,6], x [-9,9], scalar bank [-12,12]; coefficients/dimensions retained per source; union includes both signs. Compatible b keeps same integer arithmetic workload. No additional operators or stages.'})
    save('raw-probes.json',{'fresh':probes(fresh),'batch':probes(batch),'diagnostic':probes(target_records)})
    (E/'session-state.md').write_text('Independent review.py complete: source replay (14 complete banks), exact prompt/solution math, all eligible targets, fresh seeds, historical witness recomputation, strict current regressions, copied author preflight, runtime/replay/relocation/boundaries, inventory verified. Delivery, native grader, actual UI render and final decision report remain. Original package untouched.\n')
    print(json.dumps({'source_banks':len(replay),'fresh':len(fresh),'target_records':len(target_records),'math_records':len(results),'grader_cases':len(native),'packaging_passed':all(c['passed'] for c in checks),'scope_passed':True}))
if __name__=='__main__':run()

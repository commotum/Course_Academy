"""Offline repair regressions and independent witnesses from visible records.

No service access, database writes, or edits to runtime files. The prepare mode
writes evidence used by the shared delivery, grader, and renderer tools.
"""
import argparse
import ast
import copy
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'evidence'
EVIDENCE.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('candidate',ROOT/'17592186119806.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def write(name,value):
    (EVIDENCE/name).write_text(json.dumps(value,indent=2)+'\n')

def cells(s):
    m=MATRIX.fullmatch(s)
    assert m,s
    return tuple(int(z.strip()) for z in m[1].split(r'\\'))

def parse(q):
    p=q[':question/problem']
    equation=re.search(r'\$(\d+)a([+-])(\d+)x=b\$',p)
    assert equation,p
    c=int(equation[1]);d=int(equation[3])*(-1 if equation[2]=='-' else 1)
    ms=MATRIX.findall(p)
    a=tuple(int(z.strip()) for z in ms[0].split(r'\\'))
    b=tuple(int(z.strip()) for z in ms[-1].split(r'\\'))
    t=re.search(r'\{x\}_\{(\d+)\}([+-])\{x\}_\{(\d+)\}',p)
    target=(int(t[1])-1,int(t[3])-1,t[2]) if t else None
    solved=tuple(Fraction(bi-c*ai,d) for ai,bi in zip(a,b))
    assert len(a)==len(b) and len(a) in (3,4)
    assert all(z.denominator==1 for z in solved)
    solved=tuple(map(int,solved))
    answer=solved if target is None else solved[target[0]]+(1 if target[2]=='+' else -1)*solved[target[1]]
    return c,d,a,b,target,solved,answer

def read_bank(q):
    f=q[':question/answer-fields'][0]
    ch=f[':answer-field/choices'];target=parse(q)[4]
    vals=[cells(c[':answer/value']) if target is None else int(c[':answer/value']) for c in ch]
    key=f[':answer-field/correct'][1]
    ix=next(i for i,c in enumerate(ch) if c[':answer/id']==key)
    return vals,ix

def arithmetic(text):
    def value(n):
        if isinstance(n,ast.Expression):return value(n.body)
        if isinstance(n,ast.Constant) and type(n.value) is int:return n.value
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -value(n.operand)
        if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub)):
            return value(n.left)+(1 if isinstance(n.op,ast.Add) else -1)*value(n.right)
        raise AssertionError('Unexpected solution arithmetic')
    return value(ast.parse(text,mode='eval'))

def check(r):
    q=r['question'];p,d,a,b,t,x,answer=parse(q);vals,ix=read_bank(q)
    assert len(q[':question/answer-fields'])==1
    assert q[':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio'
    assert len(vals)==5 and len(set(vals))==5 and vals[ix]==answer
    solution=q[':question/worked-solution']
    ms=[cells(m.group()) for m in MATRIX.finditer(solution)]
    rev=(' & ='+str(p)+'a-b') in solution
    numerator=tuple(p*ai-bi if rev else bi-p*ai for ai,bi in zip(a,b))
    assert ms==([a,b,numerator,x] if rev else [b,a,numerator,x])
    assert 'x & ='+('-' if d<0 and not rev else '')+r'\frac{1}{'+str(abs(d))+'}' in solution
    if t:
        end=solution.split('Therefore,')[1]
        target='{x}_{'+str(t[0]+1)+'}'+t[2]+'{x}_{'+str(t[1]+1)+'}'
        assert target in end
        assert arithmetic(end.split('=')[1])==answer
        assert end.endswith('='+str(answer)+'.$')
    return answer

def native(r,label):
    answer=check(r);q=r['question'];vals,ix=read_bank(q)
    return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],
        'expected':'accepted' if j==ix else 'rejected','purpose':'independent visible equation and component arithmetic'}
        for j,c in enumerate(q[':question/answer-fields'][0][':answer-field/choices'])]}

def semantic(r):
    p,d,a,b,t,_,_=parse(r['question'])
    if t:
        pairs=[(a[i],b[i]) for i in t[:2]]
        if t[2]=='+':pairs.sort()
        return (p,d,t[2],tuple(pairs))
    return p,d,a,b

def shortcuts(records):
    groups=defaultdict(list)
    for r in records:groups[r['generation']['bank_profile']].append(r)
    report={}
    for sid,rs in sorted(groups.items()):
        counts=defaultdict(Counter);attempts=Counter();hits=Counter()
        for r in rs:
            vals,ix=read_bank(r['question']);ans=vals[ix]
            counts['position'][ix+1]+=1
            metrics={'value':vals,'absolute':list(map(abs,vals))} if isinstance(ans,int) else {
                **{'coordinate-'+str(i+1):[v[i] for v in vals] for i in range(len(ans))},
                'sum':[sum(v) for v in vals], 'norm2':[sum(z*z for z in v) for v in vals],
                'lexicographic':vals}
            for name,vs in metrics.items():
                rank=sorted(vs).index(vs[ix])+1;counts[name+'-rank'][rank]+=1
                for kind,fn in [('minimum',min),('maximum',max)]:
                    matches=[j for j,v in enumerate(vs) if v==fn(vs)]
                    if len(matches)==1:
                        cue=name+'-'+kind;attempts[cue]+=1;hits[cue]+=matches[0]==ix
            if isinstance(ans,int):
                for name,pred in [('positive',lambda v:v>0),('negative',lambda v:v<0),('zero',lambda v:v==0)]:
                    matches=[j for j,v in enumerate(vals) if pred(v)]
                    if len(matches)==1:attempts['only-'+name]+=1;hits['only-'+name]+=matches[0]==ix
        report[sid]={'count':len(rs),'histograms':{k:dict(v) for k,v in counts.items()},
            'unique_cues':{k:{'successes':hits[k],'attempts':n,'chance_baseline':0.2} for k,n in attempts.items()}}
    return report

def assert_no_fixed_cue(report):
    for sid,r in report.items():
        if r['count']<8:continue
        for cue,h in r['histograms'].items():
            assert len(h)>1,(sid,cue,h)
        for cue,v in r['unique_cues'].items():
            assert v['attempts']<8 or v['successes']<v['attempts'],(sid,cue,v)

def run():
    fixtures=json.loads((EVIDENCE/'source-fixtures.json').read_text())
    replay=[];replays=[];mappings=[]
    for old in fixtures:
        sid=old[':question/math-academy-id']
        if not old.get(':question/worked-solution'):continue
        _,_,_,_,target,_,answer=parse(old)
        r=g.generate('easy',48291,sid,{'scale':1,'target':list(target) if target else None});check(r)
        q=r['question'];f=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem']
        assert q[':question/worked-solution']==old[':question/worked-solution']
        assert sorted(c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(c[':answer/value'] for c in f[':answer-field/choices'])
        assert r['generation']['correct_value']==f[':answer-field/correct'][':answer/value']
        replays.append(r);replay.append({'source_id':old[':question/id'],'profile':sid,'prompt_exact':True,'solution_exact':True,'bank_matches':5,'distractors_match':4,'correct_designation_matches':True})
        for c in f[':answer-field/choices']:
            mappings.append({'profile':sid,'source_answer_id':c[':answer/id'],'value':c[':answer/value'],
                             'recipe':'literal complete captured bank on original parameters only','error_intent':'unresolved'})
    assert len(replays)==14
    # Execute the exact retained review check unchanged against the current candidate.
    subprocess.run([sys.executable,str(ROOT/'checks/retained_reviewer.py'),'--package',str(ROOT),
                    '--output',str(EVIDENCE/'retained-regressions.json')],check=True,capture_output=True,text=True)
    diagnostic=[]
    for sid in sorted(g.CASES):
        for scale in (1,2,3):
            for t in g.eligible_targets(sid):
                r=g.generate('easy',48291,sid,{'scale':scale,'target':list(t) if t else None})
                check(r);diagnostic.append(r)
    minimal=g.generate('easy',48291,'q-34601',{'scale':2,'target':[2,1,'-']})
    reversal=g.generate('easy',48291,'q-34601',{'scale':2,'target':[1,2,'-']})
    assert check(minimal)==54 and check(reversal)==-54
    write('exact-counterexamples-now.json',[minimal,reversal])
    fresh=[]
    for sid in sorted(g.CASES):
        for seed in range(20):
            r=g.generate('easy',seed+60000,sid);check(r)
            assert g.generate('easy',r['generation']['seed'],sid,r['generation']['parameters'])==r
            fresh.append(r)
    raw=shortcuts(fresh);assert_no_fixed_cue(raw)
    # At fixed bank, a, coefficients and target, each of its five values can
    # become correct by changing only the compatible x and hence b.
    controls=[];control_report=[];irrelevant=[]
    for sid in ('q-34601','q-105161','q-73933'):
        base=g.generate('easy',60000,sid);params=base['generation']['parameters']
        p,d,a,b,t,x,old_answer=parse(base['question']);xs=[]
        for choice in params['choices']:
            new=copy.deepcopy(params)
            if t is None:new['x']=list(cells(choice))
            else:
                v=int(choice);i,j,op=t
                u=next(u for u in range(-9,10) if -9 <= (v-u if op=='+' else u-v) <=9)
                new['x'][i]=u;new['x'][j]=v-u if op=='+' else u-v
            r=g.generate('easy',60000,sid,new);check(r);controls.append(r)
            pp,dd,aa,bb,tt,xx,ans=parse(r['question'])
            assert (pp,dd,aa,tt)==(p,d,a,t)
            assert sorted(read_bank(r['question'])[0])==sorted(read_bank(base['question'])[0])
            xs.append(ans)
        assert len(set(xs))==5
        control_report.append({'profile':sid,'same_bank_and_a_and_target':True,'distinct_correct_responses':5,'answers':xs})
        if t is not None:
            new=copy.deepcopy(params);unused=next(i for i in range(len(x)) if i not in t[:2])
            new['x'][unused]=new['x'][unused]+1 if new['x'][unused]<9 else new['x'][unused]-1
            changed=g.generate('easy',60000,sid,new);assert check(changed)==check(base)
            irrelevant.extend([base,changed])
    # All eligible targets are witnessed with other supplied vectors fixed.
    target_coverage={};target_controls=[]
    for sid in sorted(g.CASES):
        ts=g.eligible_targets(sid);seen=set()
        for t in ts:
            r=g.generate('easy',48291,sid,{'scale':2,'target':list(t) if t else None});check(r)
            seen.add(tuple(t) if t else None);target_controls.append(r)
        target_coverage[sid]={'eligible':ts,'observed':sorted([list(t) if t else [] for t in seen]),'missing':[]}
        assert len(seen)==len(ts)
    # Negative controls must catch wrong keys and stale worked arithmetic.
    stale=copy.deepcopy(minimal);f=stale['question'][':question/answer-fields'][0]
    f[':answer-field/correct'][1]=next(c[':answer/id'] for c in f[':answer-field/choices'] if c[':answer/id']!=f[':answer-field/correct'][1])
    try:check(stale)
    except AssertionError:pass
    else:raise AssertionError('Wrong key escaped oracle')
    stale=copy.deepcopy(minimal);stale['question'][':question/worked-solution']=reversal['question'][':question/worked-solution']
    try:check(stale)
    except AssertionError:pass
    else:raise AssertionError('Stale target escaped oracle')
    for band in ('moderate','hard','unclassified'):
        try:g.batch(band,1)
        except ValueError:pass
        else:raise AssertionError('Unsupported band generated')
    for parameters in ({'scale':0,'target':None},{'scale':4,'target':None},{'scale':2,'target':[0,0,'+']}):
        try:g.generate('easy',0,'q-34248',parameters)
        except ValueError:pass
        else:raise AssertionError('Invalid diagnostic parameters generated')
    assert g.batch('easy',0)==[]
    assert g.batch('easy',5,48291)==g.batch('easy',5,48291)
    batch=g.batch('easy',5,48291)
    for r in batch:check(r)
    write('source-replay.json',{'passed':True,'complete_banks':len(replay),'distractors':len(replay)*4,'profiles':replay,
          'missing_evidence':['q-34574 original key and worked solution','canonical answer bank']})
    write('source-replay-records.json',replays);write('source-bank-mapping.json',mappings)
    write('diagnostic-records.json',diagnostic);write('fresh-records.json',fresh);write('batch.json',batch)
    write('raw-shortcuts.json',raw);write('control-records.json',controls+irrelevant)
    write('counterfactual-results.json',{'passed':True,'same_bank_controls':control_report,
          'irrelevant_coordinate_pairs':2,'target_coverage':target_coverage,'negative_controls_caught':['wrong key','stale final target/arithmetic']})
    native_records=replays+batch+controls+irrelevant+target_controls
    write('grader-input.json',[native(r,str(i)) for i,r in enumerate(native_records)])
    # Capture inventory provenance; originals cannot be claimed as generated.
    inv=json.loads(Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119806/source/inventory.json').read_text())
    original_ids={q[':question/id'] for q in fixtures}
    inventory_rows=[]
    for q in inv['questions']:
        assert q[':question/id'] in original_ids
        assert not any('generation' in k or 'generator' in k for k in q)
        inventory_rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':True,'generation_metadata':False})
    write('inventory-audit.json',{'captured_basis':inv['basis'],'tested_entries':len(inventory_rows),'entries':inventory_rows,
        'conclusion':'All 15 captured entries are original source records. No stored generated record exists in this capture to reproduce the demonstrated generator transformation. Source rank arrangements alone are not marked generated defects. Live inventory outside the capture is untested.'})
    write('affected-inventory.json',{'affected_questions':[]})
    report={'passed':True,'source_banks':14,'source_distractors':56,'diagnostic_records':len(diagnostic),
            'fresh_records':len(fresh),'semantic_instances_in_fresh':len({semantic(r) for r in fresh}),
            'exact_retained_regressions':'passed','fresh_shortcut_profiles':len(raw),
            'same_bank_counterfactuals':len(controls),'irrelevant_records':len(irrelevant),
            'grader_cases_prepared':len(native_records),'native_grading':'pending separate native harness',
            'rendering':'pending actual UI render and visual inspection'}
    write('validation.json',report);print(json.dumps(report))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path);ap.add_argument('--report',default='delivery-shortcuts.json');args=ap.parse_args()
    if args.input:
        rs=json.loads(args.input.read_text())
        for r in rs:check(r)
        report=shortcuts(rs);assert_no_fixed_cue(report)
        write(args.report,{'passed':True,'records':len(rs),'semantic_instances':len({semantic(r) for r in rs}),'profiles':report})
        print(json.dumps({'passed':True,'records':len(rs),'profiles':len(report)}))
    else:run()

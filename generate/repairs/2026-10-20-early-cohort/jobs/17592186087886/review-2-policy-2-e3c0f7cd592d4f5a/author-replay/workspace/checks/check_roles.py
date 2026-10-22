"""Strict cross-family regression for the answer-length construction failure.

Parse the displayed mathematics, hold each bank fixed, and change only relevant
linear-coefficient or cancellation-parameter evidence. A bank-only function cannot identify the key across
each fixed-bank counterfactual group, regardless of its text-length/shape implementation.
"""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from collections import Counter, defaultdict
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load('g',ROOT/'17592186087886.py')
c=load('validator',ROOT/'17592186087886/validate.py')
from math_reader import rate,prompt_rhs,x,y,v
from check_shortcuts import size
OUT=ROOT/'evidence';REPO=Path('/home/jake/Developer/Course_Academy')
def save(name,data):(OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def choices(r):return r['question'][':question/answer-fields'][0][':answer-field/choices']
def key(r):
    f=r['question'][':question/answer-fields'][0]
    return next(a[':answer/value'] for a in choices(r) if a[':answer/id']==f[':answer-field/correct'][1])
def audit(rows,stage):
    groups=defaultdict(list)
    for r in rows:
        signature=tuple(sorted(a[':answer/value'] for a in choices(r)))
        groups[(r['generation']['template'],signature)].append(r)
    result={}
    assert len({t for t,_ in groups})==8
    for (t,signature),rs in groups.items():
        assert len(rs)>=4,(stage,t,'Insufficient controlled target assignments')
        keys=[key(r) for r in rs]
        assert len(set(keys))==len(rs),(stage,t,'fixed answer role')
        positions=Counter();probes=Counter();witnesses=[]
        for r in rs:
            q=r['question'];expected=(prompt_rhs(q[':question/problem']).subs(y,v*x)-v)/x
            aa=choices(r);actual=[rate(a[':answer/value']) for a in aa]
            matches=[i for i,a in enumerate(actual) if c.equivalent(a,expected)]
            assert len(matches)==1 and aa[matches[0]][':answer/value']==key(r)
            positions[matches[0]]+=1
            sizes=[size(a[':answer/value']) for a in aa]
            for name,fn in [('shortest',min),('longest',max)]:
                z=fn(sizes)
                if sizes.count(z)==1 and sizes[matches[0]]==z:probes[name]+=1
            witnesses.append({'parameters':r['generation']['parameters'],'question_id':q[':question/id'],'parsed_correct_rate':str(actual[matches[0]]),'lengths':sizes,'correct_position':matches[0]})
        assert max(positions.values())<len(rs),(stage,t,'fixed position shortcut')
        assert all(probes[n]<len(rs) for n in ['shortest','longest'])
        assert max(Counter(keys).values())==1
        label=t+':'+rs[0]['generation']['bank_profile']
        if 'bank_start' in rs[0]['generation']['parameters']:label+=':'+str(rs[0]['generation']['parameters']['bank_start'])
        result[label]={'records':len(rs),'identical_complete_visible_bank':True,'different_keys':len(set(keys)), 'bank_only_strategy_max_hits':1,'bank_only_strategy_max_rate':1/len(rs),'correct_positions':dict(positions),'unique_extreme_length_hits':dict(probes),'witnesses':witnesses}
    return result

def main():
    rows=[];counterfactuals=[];negative=0
    for t,k0 in g.ORIGINAL.items():
        k=next(k for k in g.DOMAINS[t] if k!=k0)
        family=[g.generate('easy',37,t,{'k':k,'shift':s}) for s in [-2,-1,0,1,2]]
        base=family[2];bq=base['question'];base_rhs=prompt_rhs(bq[':question/problem']);base_rate=rate(key(base))
        for r in family:
            s=r['generation']['parameters']['shift'];q=r['question']
            c.solution_check(q)
            assert c.equivalent(prompt_rhs(q[':question/problem'])-base_rhs,s*y/x)
            assert c.equivalent(rate(key(r))-base_rate,s*v/x)
            other=g.generate('easy',42,t,r['generation']['parameters'])
            assert sorted(a[':answer/value'] for a in choices(other))==sorted(a[':answer/value'] for a in choices(r))
            assert key(other)==key(r) and other['question'][':question/id']==q[':question/id']
            assert other['question'][':question/problem']==q[':question/problem'] and other['question'][':question/worked-solution']==q[':question/worked-solution']
            if s:
                stale=copy.deepcopy(q);stale[':question/worked-solution']=bq[':question/worked-solution']
                try:c.solution_check(stale)
                except AssertionError:negative+=1
                else:raise AssertionError('Stale role solution escaped validation')
        rows+=family
        counterfactuals.append({'template':t,'fixed_k':k,'role_values':[-2,-1,0,1,2],'visible_prompt_delta':'s*y/x','independent_correct_rate_delta':'s*v/x','all_worked_stages_checked':True,'seed_preserves_math':True})
    for t in g.CANCELLATION:
        for start in [1,2]:
            for k in range(start,start+5):
                if k==g.ORIGINAL[t]:continue
                r=g.generate('easy',37,t,{'k':k,'shift':0,'bank_start':start})
                c.solution_check(r['question']);rows.append(r)
    rows=list({r['question'][':question/id']:r for r in rows}.values())
    save('role-records.json',rows)
    save('role-grader-input.json',[{'label':'controlled '+str(i),'record':r,'checks':c.checks(r)} for i,r in enumerate(rows)])
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(OUT/'role-grader-input.json'),str(OUT/'role-grader-report.json')],check=True,capture_output=True,text=True)
    command=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(OUT/'role-records.json'),'--source',str(ROOT.parent/'source/source.json'),'--inventory',str(ROOT.parent/'source/inventory.json'),'--difficulty','easy','--output',str(OUT/'role-delivery'),'--asset-root',str(OUT),'--math-root','/media/jake/SSD/EDB/math']
    subprocess.run(command,capture_output=True,text=True,check=True)
    accepted=json.loads((OUT/'role-delivery/accepted.json').read_text())
    report={'status':'pass','before_delivery':audit(rows,'raw'),'after_delivery':audit(accepted,'delivered'),'counterfactuals':counterfactuals,'stale_solution_negative_controls':negative,'delivery_command':command,'generator_rejection':'No rejection sampler. Five mathematical role cases are chosen before k. Batch deduplicates prompt mathematics, then samples without replacement. Invalid k, shift and difficulty raise ValueError.', 'limits':'Fixed-bank proof applies to controlled authored role groups: at fixed k for nonzero linear shifts, and at fixed k-window for cancellation targets. Source replay members are excluded from authored groups. It proves absence of bank-only predictors for these cases, not universal mastery or absence of all possible prompt-based shortcuts. Learner history/reservations/live policy selection are unavailable.'}
    save('role-regression.json',report)
    print(json.dumps({'status':'pass','families':8,'raw_records':len(rows),'delivered_records':len(accepted),'negative_controls':negative,'max_bank_only_hits_per_fixed_bank':1}))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Retained 38c61a8aeadb91718959: visible records, actual delivery and grader."""
import collections,json,subprocess,sys
from pathlib import Path
import sympy as sp
import validate as v

REVIEW=v.W.parent/'review-1-policy-2-33e5a98244ac977f'

def select(r):
    # The reviewer's exact shape/sign decision rule, with an independent parser.
    f=r['question'][':question/answer-fields'][0]
    choices=[(a,v.matrix(a[':answer/value'])) for a in f[':answer-field/choices']]
    extra=[m for a,m in choices if len(m)==3 and len(m[0])==3 and m[2]==(0,0,0)]
    if len(extra)==1:
        hits=[a for a,m in choices if m==extra[0][:2]]
        if len(hits)==1:return hits[0][':answer/id']
    candidates=[(a,m) for a,m in choices if len(m)==2 and len(m[0])==3]
    if len(candidates)==4:
        for row in [0,1]:
            cnt=collections.Counter(sp.sign(m[row][0]) for a,m in candidates)
            if sorted(cnt.values())==[1,3]:
                return next(a[':answer/id'] for a,m in candidates if cnt[sp.sign(m[row][0])]==1)
    return None

def inspect(records):
    assert records
    groups=collections.defaultdict(list);profiles=collections.defaultdict(list)
    for r in records:
        target=v.witness(r);f=r['question'][':question/answer-fields'][0]
        bank=tuple(v.matrix(a[':answer/value']) for a in f[':answer-field/choices'])
        groups[bank].append((r,target))
        profiles[r['generation']['bank_profile']].append(r)
    group_reports=[]
    for bank,rs in groups.items():
        # No generator metadata is used to prove the changed-answer relationship.
        targets={t for r,t in rs}
        assert len(targets)>=2,'Delivery lost all contrasting targets from a bank'
        assert len(targets)==len(rs),'Repeated semantic target substituted for coverage'
        assert len({bank.index(t) for t in targets})==len(targets)
        successes=sum(select(r)==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r,t in rs)
        assert successes<len(rs),'Retained shortcut still solves an entire shared-bank group'
        group_reports.append({'records':len(rs),'semantic_targets':len(targets),'reviewed_selector_correct':successes,'bank_only_upper_bound':1})
    results={}
    for profile,rs in profiles.items():
        correct=sum(select(r)==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in rs)
        assert correct<len(rs),(profile,'reviewed shortcut still perfect')
        probes=collections.defaultdict(list)
        for r in rs:
            target=v.witness(r)
            vals=[v.matrix(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
            pos=vals.index(target)
            for index in range(5):probes[f'fixed_choice_{index}'].append(index==pos)
            for row in range(2):
                for col in range(3):
                    hits=[i for i,m in enumerate(vals) if len(m)==2 and len(m[0])==3 and m[row][col]==target[row][col]]
                    probes[f'match_prompt_cell_{row}_{col}'].append(hits==[pos])
                    for sign in [-1,0,1]:
                        hits=[i for i,m in enumerate(vals) if row<len(m) and col<len(m[0]) and sp.sign(m[row][col])==sign]
                        probes[f'unique_sign_{row}_{col}_{sign}'].append(hits==[pos])
            for name,score in [
                ('shape_2x3',lambda m:int(len(m)==2 and len(m[0])==3)),
                ('most_zeros',lambda m:sum(x==0 for row in m for x in row)),
                ('fewest_negatives',lambda m:-sum(bool(x<0) for row in m for x in row)),
                ('most_negatives',lambda m:sum(bool(x<0) for row in m for x in row)),
                ('largest_abs_sum',lambda m:sum(abs(x) for row in m for x in row)),
                ('smallest_abs_sum',lambda m:-sum(abs(x) for row in m for x in row))]:
                scores=[score(m) for m in vals];hits=[i for i,s in enumerate(scores) if s==max(scores)]
                probes[name].append(hits==[pos])
        for name,outcomes in probes.items():
            # A sufficient displayed cell in a single fixed bank is a valid
            # individual simplification. Two-group five-record batches must
            # vary that action as well as contradict all bank-only selectors.
            if not name.startswith('match_prompt_cell_') or len(rs)>=4:
                assert not all(outcomes),(profile,name,'perfect fixed action')
        results[profile]={'records':len(rs),'reviewed_selector_correct':correct,'cue_checks':{name:{'correct':sum(xs),'attempts':len(xs)} for name,xs in probes.items()},'single_bank_simplification_limit':'Fixed displayed-cell sufficiency is checked as a repeated action when at least two groups of this profile are delivered; individual sufficient-cell readings remain legitimate.'}
    return {'records':len(records),'semantic_instances':len({v.witness(r) for r in records}),'profiles':results,'same_order_fixed_bank_groups':group_reports}

def deliver(path,output,band='easy'):
    cmd=[v.PY,str(v.REPO/'generate/pipeline/check_delivery.py'),'--input',str(path),'--source',str(v.W.parent/'source/source.json'),'--inventory',str(v.W.parent/'source/inventory.json'),'--difficulty',band,'--output',str(output),'--asset-root',str(v.E/'assets'),'--math-root','/media/jake/SSD/EDB/math']
    run=subprocess.run(cmd,capture_output=True,text=True)
    assert run.returncode==0,run.stdout+run.stderr
    return json.loads((output/'accepted.json').read_text()),cmd

def main():
    original=json.loads((REVIEW/'delivery-batch/accepted.json').read_text())
    successes=[select(r)==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in original]
    assert len(original)==5 and all(successes),'Original counterexample no longer reproduced'
    v.save('retained-failed-batch.json',original)
    raw=json.loads((REVIEW/'batch.json').read_text())[0];meta=raw['generation']
    minimal=v.g.generate('easy',meta['seed'])
    assert minimal['question']==raw['question']
    assert select(minimal)==minimal['question'][':question/answer-fields'][0][':answer-field/correct'][1]
    # This individual is still a valid question. Its role must have contrasting
    # companions rather than being removed from the supported source family.
    companions=[]
    for item in minimal['generation']['recipes']:
        try:r=v.g.generate('easy',meta['seed'],meta['template'],meta['parameters'],meta['bank_profile'],bank_orientation=meta['bank_orientation'],target_recipe=item['recipe'])
        except ValueError:continue
        v.witness(r);companions.append(r)
    assert len({v.witness(r) for r in companions})==3
    assert sum(select(r)==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in companions)==1
    v.save('exact-counterfactual-records.json',companions)
    reports=[];native=[];render=[]
    for name,seed,profile in [('exact-batch-seed',2878966680,None)]+[(p,20261020,p) for p in v.g.EASY_SOURCES]:
        cmd=[v.PY,str(v.W/'17592186059770.py'),'--difficulty','easy','--count','5','--seed',str(seed),'--format','json']
        if profile:cmd+=['--profile',profile]
        run=subprocess.run(cmd,capture_output=True,text=True);assert run.returncode==0,run.stderr
        rs=json.loads(run.stdout);assert len(rs)==5
        before=inspect(rs)
        path=v.E/f'repair-batch-{name}.json';path.write_text(json.dumps(rs,indent=2))
        accepted,delivery_cmd=deliver(path,v.E/f'repair-delivery-{name}')
        assert len(accepted)==5,'New batch unexpectedly loses a record to captured inventory/deduplication'
        after=inspect(accepted)
        reports.append({'case':name,'command':cmd,'delivery_command':delivery_cmd,'before':before,'after':after})
        if profile:render.extend(accepted[:1])
        else:v.save('replacement-batch.json',accepted)
        for r in accepted:
            target=v.witness(r)
            native.append({'label':name,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if v.matrix(a[':answer/value'])==target else 'rejected','purpose':'changed visible system determines target after actual delivery'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
    # Small boundary sample: odd/even group partitioning, every profile, deterministic CLI API.
    boundaries=[]
    for profile in v.g.EASY_SOURCES:
        for count in [1,2,3,5,6]:
            rs=v.g.generate_batch('easy',count,42,profile=profile)
            assert rs==v.g.generate_batch('easy',count,42,profile=profile)
            assert len(rs)==count
            for r in rs:v.witness(r)
            if count>1:inspect(rs)
            boundaries.append({'profile':profile,'count':count,'status':'passed'})
    v.save('repair-render-records.json',render)
    v.save('repair-native-input.json',native)
    run=subprocess.run([str(v.REPO/'generate/runs/current/check-engine'),str(v.E/'repair-native-input.json'),str(v.E/'repair-native-report.json')],capture_output=True,text=True)
    assert run.returncode==0,run.stdout+run.stderr
    v.save('batch-regression.json',{'finding_id':'38c61a8aeadb91718959','status':'passed','original_reviewed_shortcut':'5/5 reproduced','minimal_question':minimal['question'][':question/id'],'minimal_source_role_retained':True,'minimal_fixed_bank_targets':3,'batches':reports,'boundary_cases':boundaries,'native_checks':5*len(native),'limits':'Captured inventory/difficulty/publication filtering exercised. Arbitrary live learner exclusions and future inventory may remove companions; no claim about unavailable learner state or all possible prompt-aware shortcuts.'})
    print('38c61a8aeadb91718959 passed: exact 5/5 failure reproduced; 25/25 replacements delivered; 125 native checks; all shared banks retain contrasting keys')

if __name__=='__main__':main()

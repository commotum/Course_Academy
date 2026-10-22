"""Retained e00c00847a8d35dee226: visible-rank decision influence, after delivery.

No runtime edits or network/DB access. --input is a strict negative/positive
checker. Default run tests the current sampler, exact reported prefix, native
learner grading, source replay (retained first-finding check), and same-layout
single-matrix counterfactuals. All evidence stays inside this workspace.
"""
import argparse
import copy
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
from collections import defaultdict
from unittest.mock import patch
from validate_content import ROOT, REPO, JOB, g, inspect, visible_bank
from check_batch_decisions import audit as original_audit

E=ROOT/'evidence/repair-3'

def save(name, value):
    path=E/name;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n')

def audit(records):
    groups=defaultdict(list)
    for rec in records:
        w,_=inspect(rec);bank=visible_bank(rec['question'])
        excluded=tuple(k for k,m in sorted(bank.items()) if min(len(m),len(m[0]))<w['target'])
        common=(rec['generation']['source_id'],w['target'],excluded,
                w['field_count'],rec['generation']['choice_profile'])
        for resolution,shape in [('shape-multiset',tuple(sorted((len(m),len(m[0])) for m in bank.values()))),
                                 ('label-shapes',tuple((k,len(m),len(m[0])) for k,m in sorted(bank.items())))]:
            groups[(resolution,common,shape)].append((rec,w,sorted(set(bank)-set(excluded))))
    rows=[];failures=[]
    for key,items in groups.items():
        truths=[set(w['truth']) for _,w,_ in items];eligible=items[0][2]
        row={'group':str(key),'count':len(items),'truths':[sorted(t) for t in truths],
             'ids':[r['question'][':question/id'] for r,_,_ in items],
             'correct_positions':[w['positions'] for _,w,_ in items],
             'correct_counts':sorted({len(t) for t in truths}),
             'singleton':len(items)==1,'missing_independent_decisions':[]}
        # A singular whole-matrix radio contract permits inferring the last
        # candidate. A subset contract does not specify its correct cardinality.
        subset=bool(re.search(r'matrices have',items[0][0]['question'][':question/problem'])) and len(eligible)>1
        if len(items)>1 and subset:
            for lab in eligible:
                witnesses=[(a,b) for a,b in itertools.combinations(range(len(items)),2)
                           if (truths[a]-{lab})==(truths[b]-{lab}) and (lab in truths[a])!=(lab in truths[b])]
                if not witnesses:row['missing_independent_decisions'].append(lab)
            if row['missing_independent_decisions']:failures.append(row)
        rows.append(row)
    old=original_audit(records)
    return {'passed':not failures and old['passed'],'groups':rows,'failures':failures,
            'retained_fixed_label_and_position_audit':old,
            'witness':'For every subset candidate, hold other qualifying statuses constant and change this one; read exact ranks from visible matrices.',
            'limits':['Singleton groups cannot demonstrate conditional coverage.',
                      'Singular matrix-radio permits fixed cardinality by response contract.']}

def delivery(name,records):
    save(name+'.json',records)
    command=[sys.executable,'-B',str(REPO/'generate/pipeline/check_delivery.py'),
             '--input',str(E/(name+'.json')),'--source',str(JOB/'source/source.json'),
             '--inventory',str(JOB/'source/inventory.json'),'--difficulty','easy',
             '--output',str(E/(name+'-delivery')),'--math-root','/media/jake/SSD/EDB/math']
    result=subprocess.run(command,capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    accepted=json.loads((E/(name+'-delivery/accepted.json')).read_text())
    before,after=audit(records),audit(accepted)
    assert before['passed'] and after['passed'],(name,before['failures'],after['failures'])
    assert len(records)==len(accepted),'Delivery lost decision-case coverage'
    return accepted,{'command':command,'before':before,'after':after,
                     'delivery':json.loads((E/(name+'-delivery/delivery.json')).read_text())}

def exclusive_strategy(rec,inspected='A'):
    w,_=inspect(rec);bank=visible_bank(rec['question'])
    eligible=[k for k,m in bank.items() if min(len(m),len(m[0]))>=w['target']]
    other=next(k for k in eligible if k!=inspected)
    guess={inspected} if inspected in w['truth'] else {other}
    field=rec['question'][':question/answer-fields'][0]
    choice=next(a for a in field[':answer-field/choices'] if set(re.findall(r'\$([A-E])\$',a[':answer/value']))==guess)
    outcome='accepted' if guess==set(w['truth']) else 'rejected'
    return {'label':'Inspect '+inspected+' only, assume exclusivity','record':rec,'checks':[
        {'submitted_answer_id':choice[':answer/id'],'expected':outcome,
         'purpose':'Uses one visible rank, assumes exactly one of two eligible matrices qualifies'}]},outcome

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path);p.add_argument('--report',type=Path)
    args=p.parse_args();E.mkdir(parents=True,exist_ok=True)
    if args.input:
        report=audit(json.loads(args.input.read_text()))
        if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'passed':report['passed'],'failures':len(report['failures'])}))
        raise SystemExit(0 if report['passed'] else 1)
    previous=json.loads((E/'previous-batch.json').read_text())
    old=audit(previous);assert not old['passed'] and old['failures']
    save('latest-negative-control.json',old)
    catalog=g.catalog();live={r['question'][':question/id']:r for r in catalog}
    assert catalog==json.loads((ROOT/'evidence/catalog.json').read_text()),'Unrelated catalog changed'
    # Publisher normalization can reidentify checkbox records; the exact raw
    # runner prefix is retained separately from its accepted delivery fixture.
    prefix_records=json.loads((E/'previous-raw-batch.json').read_text())
    assert all(live[r['question'][':question/id']]==r for r in prefix_records)
    ids=[r['question'][':question/id'] for r in prefix_records]
    def prefix(_rng,rows):
        indexed={r['question'][':question/id']:r for r in rows}
        rows[:]=[indexed[k] for k in ids if k in indexed]+[r for r in rows if r['question'][':question/id'] not in ids]
    with patch.object(g.random.Random,'shuffle',prefix):repaired=g.batch('easy',5,0)
    affected=[r for r in repaired if r['generation']['source_id']=='q-139965']
    assert len(affected)==3
    assert {tuple(inspect(r)[0]['truth']) for r in affected}=={('A',),('C',),('A','C')}
    shapes=[{k:(len(m),len(m[0])) for k,m in visible_bank(r['question']).items()} for r in affected]
    assert all(s==shapes[0] for s in shapes),'Label-to-shape assignment changed within block'
    accepted,exact_delivery=delivery('exact-prefix-repaired',repaired)
    affected=[r for r in accepted if r['generation']['source_id']=='q-139965']

    # Retain whole-family capacity and size-boundary coverage without a seed sweep.
    controls=[];capacity=len({r['generation']['mathematical_fingerprint'] for r in catalog})
    for seed,count in [(0,5),(1763,5),(5281,5),(14653,5),(7,0),(7,1),(7,2),(7,3),(7,4),(7,capacity-1),(5281,capacity)]:
        records=g.batch('easy',count,seed)
        assert len(records)==count
        assert len({r['generation']['mathematical_fingerprint'] for r in records})==count
        analysis=audit(records);assert analysis['passed'],(seed,count,analysis['failures'])
        control={'seed':seed,'count':count,'audit':analysis}
        # First-finding regression already covers 0,7,119848 and capacity-7 delivery.
        if (seed,count) in [(1763,5),(5281,5),(14653,5),(5281,capacity)]:
            _,control['delivery']=delivery('seed-'+str(seed)+'-'+str(count),records)
        controls.append(control)
    assert {r['generation']['mathematical_fingerprint'] for r in records}=={r['generation']['mathematical_fingerprint'] for r in catalog}

    # Both one-inspection shortcuts fail the delivered joint case in the native grader.
    native=[];shortcut=[]
    for rec in affected:
        _,checks=inspect(rec);native.append({'label':'affected delivered bank','record':rec,'checks':checks})
        for label in ('A','C'):
            case,outcome=exclusive_strategy(rec,label);native.append(case)
            shortcut.append({'id':rec['question'][':question/id'],'inspected':label,'outcome':outcome})
    assert sum(x['outcome']=='rejected' for x in shortcut)==2

    # Stronger same-layout controls: only the omitted matrix changes physically.
    controls_matrix=[g.generate('easy',0,'q-139965',{'matches':m,'assignment':['C','A','B']})
                     for m in [['A'],['A','C'],['C']]]
    banks=[visible_bank(r['question']) for r in controls_matrix]
    assert banks[0]['A']==banks[1]['A'] and banks[0]['B']==banks[1]['B'] and banks[0]['C']!=banks[1]['C']
    assert banks[1]['C']==banks[2]['C'] and banks[1]['B']==banks[2]['B'] and banks[1]['A']!=banks[2]['A']
    for before,after in [(controls_matrix[0],controls_matrix[1]),(controls_matrix[2],controls_matrix[1])]:
        for component in (':question/worked-solution',':question/answer-fields'):
            bad=copy.deepcopy(after);bad['question'][component]=before['question'][component]
            try:inspect(bad)
            except (AssertionError,StopIteration):pass
            else:raise AssertionError('Stale key/solution negative control passed')
    for i,rec in enumerate(controls_matrix):
        _,checks=inspect(rec);native.append({'label':'single-matrix counterfactual '+str(i),'record':rec,'checks':checks})
        for label in ('A','C'):
            case,_=exclusive_strategy(rec,label);native.append(case)
    irrelevant=g.generate('easy',0,'q-139965',{'matches':['A','C'],'assignment':['C','A','B'],'scale':1})
    assert inspect(irrelevant)[0]['truth']==inspect(controls_matrix[1])[0]['truth']
    assert visible_bank(irrelevant['question'])!=banks[1]
    _,checks=inspect(irrelevant);native.append({'label':'irrelevant scaling','record':irrelevant,'checks':checks})
    save('counterfactual-records.json',controls_matrix+[irrelevant])
    save('render-records.json',affected)
    save('grader-input.json',native)
    command=[str(REPO/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-results.json')]
    result=subprocess.run(command,capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    grades=json.loads((E/'grader-results.json').read_text());assert grades['documented_unresolved_checks']==0
    report={'passed':True,'finding':'e00c00847a8d35dee226','negative_control_failed':True,
            'exact_prefix_delivery':exact_delivery,'sampler_controls':controls,
            'unchanged_catalog':{'presentations':len(catalog),'semantic_instances':capacity},
            'single_matrix_counterfactuals':{'only_C_changed':[0,1],'only_A_changed':[2,1],
                'excluded_B_unchanged':True,'stale_solution_and_key_rejected':True,'irrelevant_scale_response_preserved':True},
            'native_grader_command':command,'grades':{k:grades[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
            'exclusive_shortcut_grades':shortcut,
            'limits':['Recorded candidate prefix restored explicitly; runner batch shuffle seed is unknown.',
                      'Captured inventory only. Live histories and reservations unavailable; selection may exhaust finite families.',
                      'Independent native grader used without engine changes; no services contacted.']}
    save('exclusive-regression.json',report)
    print(json.dumps({'passed':True,'negative_control_failed':True,'sampler_controls':len(controls),
                      'catalog_presentations':len(catalog),'semantic_instances':capacity,'grades':report['grades']}))

if __name__=='__main__':main()

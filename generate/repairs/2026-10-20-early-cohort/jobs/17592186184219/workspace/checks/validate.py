"""Focused repair validation. prepare -> shared delivery -> finish -> native/UI tools."""
import collections, hashlib, json, platform, shutil, subprocess, sys, tempfile
from pathlib import Path
from regressions import G, QS, SOURCE, W, math_check, read, witnesses
E=W/'evidence';REPO=Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python'
def save(name,data):
    path=E/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n')
def load(name):return json.loads((E/name).read_text())
def signature(r):
    d=read(r);v=sorted(d['values']);return d['target'],tuple(b-a for a,b in zip(v,v[1:]))
def probe(rs):
    groups=collections.defaultdict(list);positions=collections.Counter();targets=collections.Counter();shapes=collections.Counter()
    rules={signature(q):sorted(read(q)['values']).index(read(q)['c']) for q in QS}
    hits=0
    for r in rs:
        d=math_check(r);bank=sorted(d['values']);role=bank.index(d['c']);sig=signature(r)
        groups[str(sig)].append(role);positions[d['values'].index(d['c'])]+=1;targets[d['target']]+=1
        shapes['square' if d['m']==d['n'] else 'tall' if d['m']>d['n'] else 'wide']+=1
        hits+=role==rules[sig]
    return {'count':len(rs),'old_target_gap_rule_hits':hits,'display_correct_positions':dict(positions),'targets':dict(targets),'shapes':dict(shapes),'by_target_and_gaps':{k:{'count':len(v),'sorted_roles':dict(collections.Counter(v))} for k,v in groups.items()}}

def prepare():
    replay=[];summary=[]
    for q in QS:
        d=read(q);p={k:d[k] for k in ['m','n','k','target']};r=G.generate('easy',seed=61403,template=q[':question/math-academy-id'],parameters=p);math_check(r);replay.append(r)
        summary.append({'source_id':q[':question/id'],'ma_id':q[':question/math-academy-id'],'complete_bank':sorted(read(r)['values'])==sorted(d['values']),'correct':read(r)['c']==d['c'],'prompt':r['question'][':question/problem']==q[':question/problem'],'solution':r['question'][':question/worked-solution']==q[':question/worked-solution']})
    assert all(all(x[k] for k in ['complete_bank','correct','prompt','solution']) for x in summary)
    save('source-replay.json',summary);save('source-replay-records.json',replay)
    controls=witnesses();save('controls.json',controls)
    # Small sampler regression, including every profile and exact original seed interval.
    small=[G.generate('easy',seed=310+i,template=read(q)['target'],profile=q[':question/math-academy-id']) for i,q in enumerate(QS)]
    small += [G.generate('easy',seed=i,template='rank',profile='q-141220') for i in range(829001,829017)]
    for r in small:math_check(r)
    save('small-sample.json',small)
    out=subprocess.check_output([str(PY),'-B',str(W/'17592186184219.py'),'--difficulty','easy','--seed','829013','--count','5','--format','json'],cwd=W)
    batch=json.loads(out);save('batch.json',batch)
    pairs=[]
    for target,profile in [('rank','q-141220'),('nullity','q-142481')]:
        for label,m,n,k,role in [('base',12,10,5,2),('given',12,10,6,1),('columns',12,11,5,3),('rows',11,10,5,2)]:
            r=G.generate('easy',seed=31,template=target,profile=profile,parameters=dict(m=m,n=n,k=k,target=target),bank_role=role)
            d=math_check(r);assert sorted(d['values'])==[3,4,5,6,7]
            assert d['c']=={'base':5,'given':4,'columns':6,'rows':5}[label]
            pairs.append({'case':target+'/'+label,'record':r})
    save('counterfactuals.json',pairs)
    boundaries=[]
    for t in ['rank','nullity']:
        profile='q-141220' if t=='rank' else 'q-142481'
        for m,n,k in [(2,2,0),(2,2,2),(12,12,0),(12,12,12),(2,12,10)]:
            rank=n-k if t=='rank' else k;p=dict(m=m,n=n,k=k,target=t)
            try:r=G.generate('easy',seed=22,template=t,profile=profile,parameters=p)
            except ValueError:
                assert rank>min(m,n);boundaries.append({'parameters':p,'expected_infeasible':True})
            else:math_check(r);boundaries.append({'parameters':p,'record':r})
    for kwargs in [dict(level='moderate'),dict(level='hard'),dict(level='easy',field_type='blank'),dict(level='easy',template='nullity',profile='q-141220'),dict(level='easy',template='rank',parameters=dict(m=2,n=2,k=True,target='rank'))]:
        try:G.generate(**kwargs)
        except ValueError:pass
        else:raise AssertionError(('unsupported request accepted',kwargs))
    save('boundaries.json',boundaries)
    # Controlled row/column/target changes and boundaries are part of the math record set.
    all_records=controls+small+batch+[x['record'] for x in pairs]+[x['record'] for x in boundaries if 'record' in x]
    for r in all_records:math_check(r)
    save('math-and-shortcuts-raw.json',{'checked':len(all_records),'controls':probe(controls),'small':probe(small),'batch':probe(batch),'coverage':'70 controlled records: five distinct answers at a fixed whole bank, target, rows and columns for each of 14 profiles. No added random samples beyond 30 affected-family records.'})
    inventory=json.loads((W.parent/'source/inventory.json').read_text());ids={q[':question/id'] for q in QS}
    rows=[]
    for q in inventory['questions']:
        generated=[k for k in q if 'generat' in k]
        assert q[':question/id'] in ids and not generated
        rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':True,'generation_keys':generated})
    save('inventory-audit.json',{'basis':inventory['basis'],'inspected':rows,'generated_instances':0,'conclusion':'Verified captured inventory contains only the 14 original source records; none is a stored generated instance of the demonstrated defect. No original source was marked generated. Later live inventory is untested.'})
    save('affected-inventory.json',{'affected_questions':[]})
    # Exact runtime-only relocation and determinism, no repository paths required.
    manifest=json.loads((W/'package.json').read_text())
    assert manifest['dependencies']=={'python':platform.python_version(),'packages':{}}
    with tempfile.TemporaryDirectory(prefix='rank-nullity-',dir='/tmp') as tmp:
        for name in manifest['files']:
            dst=Path(tmp)/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,dst)
        cmd=[str(PY),'-B',str(Path(tmp)/manifest['entrypoint']),'--difficulty','easy','--seed','829013','--count','5','--format','json']
        assert subprocess.check_output(cmd,cwd=tmp)==out
        assert subprocess.check_output(cmd,cwd=tmp)==out
    save('packaging.json',{'relocation':'passed','seeded_cli_replay':'passed','dependencies':manifest['dependencies'],'runtime_hashes':{name:hashlib.sha256((W/name).read_bytes()).hexdigest() for name in manifest['files']}})
    print(json.dumps({'source_replay':len(replay),'controls':len(controls),'small':len(small),'batch':len(batch),'math_checked':len(all_records),'packaging':'passed','inventory_generated':0}))

def finish():
    raw=load('controls.json');delivered=load('delivery-controls/accepted.json');batch=load('delivery-batch/accepted.json');assert len(batch)==5
    # Full-bank cues and target/gap/shape cues must remain ambiguous after actual filtering.
    for records in [raw,delivered]:
        groups=collections.defaultdict(set)
        for r in records:
            d=math_check(r);bank=tuple(sorted(d['values']));groups[(d['target'],d['m'],d['n'],bank)].add(d['c'])
        assert groups and all(len(values)==5 for values in groups.values())
        p=probe(records);assert all(set(v['sorted_roles'])==set(range(5)) for v in p['by_target_and_gaps'].values())
        assert p['old_target_gap_rule_hits']<p['count']
    save('delivery-shortcuts.json',{'raw':probe(raw),'delivered':probe(delivered),'batch':probe(batch),'full_bank_with_fixed_shape_groups':'all surviving groups have all five correct values','limitations':['Normalization and captured-inventory filtering were actually run. Live learner history, future inventory and policy weights were not supplied. Arbitrary history exclusions can shrink any practice family.']})
    selected=load('source-replay-records.json')+delivered+batch+[x['record'] for x in load('counterfactuals.json')]
    small=load('small-sample.json');small_delivered=load('delivery-small/accepted.json')
    save('small-delivery-shortcuts.json',{'raw':probe(small),'delivered':probe(small_delivered)})
    semantic={}
    for name,records in [('controls',raw),('small',small),('batch',batch)]:
        ds=[read(r) for r in records]
        semantic[name]={'records':len(ds),'distinct_target_column_given_tuples':len({(d['target'],d['n'],d['k']) for d in ds}),'distinct_target_column_given_bank_tuples':len({(d['target'],d['n'],d['k'],tuple(sorted(d['values']))) for d in ds})}
    save('semantic-counts.json',semantic)
    # Native grader tests entire banks, including bank-only wrong choices after normalization.
    cases=[]
    for i,r in enumerate(selected):
        d=math_check(r);field=r['question'][':question/answer-fields'][0]
        cases.append({'label':f'repair-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if int(a[':answer/value'])==d['n']-d['k'] else 'rejected','purpose':'independent subtraction from visible prompt; every radio choice'} for a in field[':answer-field/choices']]})
    save('grader-input.json',cases)
    # Include changed correct roles and targets, the exact CLI seed, and a newly recovered source.
    previews=[delivered[0],delivered[1],next(r for r in delivered if read(r)['target']=='nullity'),batch[0],load('source-replay-records.json')[-3]]
    save('render-records.json',previews)
    save('after-seed-829013.json',[G.generate('easy',seed=829013)])
    print(json.dumps({'delivered_controls':len(delivered),'delivered_batch':len(batch),'native_records':len(cases),'native_checks':sum(len(c['checks']) for c in cases),'previews':len(previews)}))

if __name__=='__main__':
    {'prepare':prepare,'finish':finish}[sys.argv[1]]()

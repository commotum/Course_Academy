"""Small current-output regression, delivery and counterfactual audit."""
import collections, hashlib, json, os, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
from visible_math import g, s, parse, key, mathcheck, eq
from check_fractional_exp import W, REPO, ENGINE, run, save

def delivery(records,name):
    save(name+'.json',records)
    run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',W/(name+'.json'),
         '--source',W.parent/'source/source.json','--inventory',W.parent/'source/inventory.json',
         '--difficulty','easy','--output',W/('delivery-'+name),'--asset-root',W/'assets',
         '--math-root','/media/jake/SSD/EDB/math'])
    return json.loads((W/('delivery-'+name)/'accepted.json').read_text())

def metrics(records):
    groups=collections.defaultdict(list)
    for r in records:
        f=r['question'][':question/answer-fields'][0]
        if not f[':answer-field/type'].endswith('/radio'):continue
        vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']];m=parse(key(r))
        groups[r['generation']['template']].append({'id':r['question'][':question/id'],
            'position':next(i+1 for i,v in enumerate(vals) if eq(v,m)),
            'first':eq(vals[0],m),'zero':m==0,
            'smallest_nonzero':eq(min((v for v in vals if v!=0),key=lambda v:abs(float(v))),m),
            'largest':eq(max(vals,key=lambda v:abs(float(v))),m),
            'answer':str(m),'target':r['generation']['parameters']['u']})
    return {k:{'count':len(v),'positions':sorted({x['position'] for x in v}),
        'successes':{cue:sum(x[cue] for x in v) for cue in ['first','zero','smallest_nonzero','largest']},
        'records':v} for k,v in groups.items()}

def main():
    env=dict(os.environ,COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(W/'assets'),PYTHONDONTWRITEBYTECODE='1')
    cmd=[sys.executable,str(W/'generator.py'),'--difficulty','easy','--count','5','--seed','3175644378','--format','json']
    first=subprocess.run(cmd,env=env,capture_output=True,text=True,check=True)
    batch=json.loads(first.stdout);save('prospective-batch.json',batch)
    second=subprocess.run(cmd,env=env,capture_output=True,text=True,check=True)
    assert first.stdout==second.stdout
    save('cli-execution.json',{'command':cmd,'output_directory':str(W/'assets'),'count':len(batch),'deterministic_replay':True})
    accepted=delivery(batch,'prospective-batch');assert len(accepted)==5
    pairs=[]
    for name,template,p,change,same in [
        ('target sign','double_cos_radio',dict(a=2,b=3,u='pi/6'),dict(u='pi/3'),False),
        ('zero to positive','linear_trig_radio',dict(a=2,b=1,u='pi/2'),dict(u='3*pi/2'),False),
        ('translation','poly5_radio',dict(a=2,b=3,c=3,u=1),dict(c=-4),True),
        ('blank target','cubic_blank',dict(a=2,b=1,u=2),dict(u=3),False)]:
        a=g.generate('easy',8201,template,parameters=p)
        b=g.generate('easy',8201,template,parameters=dict(p,**change))
        assert eq(parse(key(a)),parse(key(b)))==same
        assert a['question'][':question/problem']!=b['question'][':question/problem']
        if not same:assert a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']
        pairs.append({'label':name,'same_answer':same,'before':a,'after':b})
    save('current-counterfactuals.json',pairs)
    probes=[r for p in pairs for r in (p['before'],p['after'])]
    # Start small. Add only a bounded follow-up when an observed cue remains perfect.
    for template,(level,kind,*_) in g.TEMPLATES.items():
        if level!='easy' or kind!='radio':continue
        group=[]
        for i in range(8):
            group.append(g.generate('easy',71003+i,template))
            report=metrics(group)[template]
            if len(group)>=2 and len(report['positions'])>1 and all(n<len(group) for n in report['successes'].values()):break
        probes.extend(group)
    delivered_probes=delivery(probes,'probes')
    before,after=metrics(probes),metrics(delivered_probes)
    for stage in [before,after]:
        for template,v in stage.items():
            assert len(v['positions'])>1,(template,'fixed key position')
            assert all(n<v['count'] for n in v['successes'].values()),(template,'perfect tested cue')
    save('current-shortcuts.json',{'batch':metrics(batch),'delivered_batch':metrics(accepted),'probes':before,'delivered_probes':after,
        'scope':'Counterexamples to first/zero/minimum nonzero magnitude/maximum magnitude cues, per easy radio template; not a proof against every possible strategy. Five-item batch metrics are descriptive, not arbitrary balance quotas.'})
    rs=batch+probes
    save('current-math.json',[mathcheck(r) for r in rs])
    cases=[]
    for r in rs+accepted+delivered_probes:
        f=r['question'][':question/answer-fields'][0]
        if f[':answer-field/type'].endswith('/radio'):
            checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
        else:checks=[{'submitted':key(r),'expected':'accepted'},{'submitted':'('+key(r)+')+1','expected':'rejected'}]
        cases.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
    for pair in pairs:
        r=pair['after'];f=r['question'][':question/answer-fields'][0]
        if f[':answer-field/type'].endswith('/blank'):
            cases.append({'label':'stale target answer','record':r,'checks':[{'submitted':key(pair['before']),'expected':'accepted' if pair['same_answer'] else 'rejected'}]})
    save('current-grader-input.json',cases);run([ENGINE,W/'current-grader-input.json',W/'current-grader-result.json'])
    hard=json.loads((W/'regression-records.json').read_text())[0]
    save('render-records.json',[next(r for r in batch if r['generation']['plots']),next(r for r in batch if not r['generation']['plots']),hard])
    old=json.loads((W/'runtime-before.json').read_text());now={f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in old};assert now==old
    save('current-validation.json',{'batch':len(batch),'delivered_batch':len(accepted),'probe_records':len(probes),'delivered_probe_records':len(delivered_probes),'runtime_unchanged':True,'result':'passed'})
    print('Current CLI, math, grading, counterfactual and shortcut checks passed;',len(probes),'probe records')
if __name__=='__main__':main()

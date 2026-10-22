"""Offline regressions: inspect visible records; never contact a service or database."""
import collections, importlib.util, json, os, re, shutil, subprocess, sys, tempfile
from check_cli_contract import decode, main as check_cli_contract
from pathlib import Path
HERE=Path(__file__).resolve().parent
E=HERE/'evidence'; E.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('rank_generator',HERE/'17592186119847.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):
    (E/name).write_text(json.dumps(value,indent=2)+'\n')
def inspect(record):
    q=record['question']; text=q[':question/problem']
    name,m,n,c=re.search(r'\$([A-Z])\$.*?\$(\d+)\s*\\(?:times|cdot)\s*(\d+)\$.*?\$(\d+)\$',text).groups()
    m,n,c=map(int,(m,n,c));rank=n-c if '**non-pivot**' in text else c
    assert 1<=rank<=min(m,n),text
    field=q[':question/answer-fields'][0];choices=field[':answer-field/choices']
    vals=[int(a[':answer/value']) for a in choices]
    assert len(choices)==len(set(vals))==5 and min(vals)>=0
    correct=field[':answer-field/correct'];cid=correct.get(':answer/id') if isinstance(correct,dict) else correct[1]
    pos=next(i for i,a in enumerate(choices) if a[':answer/id']==cid)
    assert vals[pos]==rank
    sol=q[':question/worked-solution']
    assert f'\\text{{rank}}({name})={rank}.' in sol
    assert 'number of pivot columns' in sol
    if '**non-pivot**' in text:assert f'{n}-{c}={rank}.' in sol
    else:assert f'${name}$ has ${c}$ pivot column' in sol
    return {'rank':rank,'position':pos,'numerical_order':sorted(vals).index(rank),'semantic':('non-pivot',n,c) if '**non-pivot**' in text else ('pivot',c),'rows':m,'columns':n,'count':c}
def cli(level,count,seed=0,entry=None,cwd=None):
    cmd=[sys.executable,str(entry or HERE/'17592186119847.py'),'--difficulty',level,'--count',str(count),'--seed',str(seed),'--format','json']
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
    return p,cmd

def main():
    check_cli_contract()
    counts=[];full=[]
    # Declared finite capacities; uniqueness and correctness are read from visible records.
    capacities={'easy':12,'moderate':91}
    for level,capacity in capacities.items():
        for count in [0,1,5,capacity]:
            p,cmd=cli(level,count);assert p.returncode==0,p.stderr
            rs=decode(p.stdout);assert isinstance(rs,list) and len(rs)==count
            facts=[inspect(r) for r in rs];assert len({f['semantic'] for f in facts})==count
            counts.append({'command':cmd,'requested':count,'returned':len(rs),'distinct_semantic':len(facts)})
            if count==capacity:full+=rs
        for count in [-1,capacity+1]:
            p,cmd=cli(level,count);assert p.returncode!=0 and not p.stdout and f'{capacity} distinct semantic tasks' in p.stderr
            counts.append({'command':cmd,'requested':count,'exit':p.returncode,'error':p.stderr.strip()})
    deterministic,_=cli('easy',5,91);p2,_=cli('easy',5,91);assert deterministic.stdout==p2.stdout
    save('count-regression.json',{'status':'pass','capacities':capacities,'cases':counts})
    source=json.loads((HERE.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
    replay=[];records=[]
    for q in source:
        profile=q[':question/math-academy-id'];level='moderate' if '**non-pivot**' in q[':question/problem'] else 'easy'
        r=g.generate(level,parameters=g.source_parameters(q),bank_profile=profile);inspect(r)
        got=r['question'];assert got[':question/problem']==q[':question/problem'].replace(r'\cdot',r'\times')
        old=q[':question/answer-fields'][0];new=got[':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in old[':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':answer-field/choices'])
        if ':question/worked-solution' in q:assert got[':question/worked-solution']==q[':question/worked-solution']
        if ':answer-field/correct' in old:
            assert next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value']
        replay.append({'source':profile,'source_uuid':q[':question/id'],'options_matched':5,'source_solution_present':':question/worked-solution' in q,'inferred_missing_key_and_solution':profile=='q-34825'})
        records.append(r)
    save('source-replay.json',replay)
    # Same evidence, changed presentation; same dimensions, changed decisive counts.
    controls=[]
    for level in ['easy','moderate']:
        profile='q-79405' if level=='easy' else 'q-139953'
        p={'name':'A','rows':10,'columns':12,'count':5,'kind':'pivot' if level=='easy' else 'non-pivot'}
        variants=[p,{**p,'count':4},{**p,'name':'T','rows':9}]
        if level=='moderate':variants.append({**p,'columns':13})
        rs=[g.generate(level,seed=51,parameters=x,bank_profile=profile) for x in variants]
        fs=[inspect(r) for r in rs];assert fs[0]['rank']!=fs[1]['rank'];assert fs[0]['rank']==fs[2]['rank']
        if level=='moderate':assert fs[0]['rank']!=fs[3]['rank']
        controls.append({'difficulty':level,'facts':fs});records+=rs
    save('counterfactuals.json',controls)
    # The random cue probes miss row=3; exercise it constructively in both bands.
    for level,profile,count in [('easy','q-34805',2),('moderate','q-34806',5)]:
        boundary=g.generate(level,seed=7,parameters={'name':'A','rows':3,'columns':6,'count':count,'kind':'pivot' if level=='easy' else 'non-pivot'},bank_profile=profile)
        inspect(boundary);records.append(boundary)
    save('boundary-records.json',records[-2:])
    # Exercise sign assignments and bank positions within every recognizable profile.
    probes=[]
    for level,profiles in g.PROFILES.items():
        for profile in profiles:
            group=[g.generate(level,seed=seed,bank_profile=profile) for seed in range(40)]
            facts=[inspect(r) for r in group]
            assert len({f['position'] for f in facts})>1,profile
            assert len({f['numerical_order'] for f in facts})>1,profile
            probes+=group
    save('probe-records.json',probes)
    records+=full[:5]+[full[-1]]
    save('validation-records.json',records)
    cases=[]
    for r in records:
        fact=inspect(r);f=r['question'][':question/answer-fields'][0]
        cases.append({'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if int(a[':answer/value'])==fact['rank'] else 'rejected','purpose':'Independent visible-count rank oracle, all five responses'} for a in f[':answer-field/choices']]})
    save('grader-input.json',cases)
    # Copy only declared runtime closure, then execute outside the repository.
    manifest=json.loads((HERE/'package.json').read_text())
    with tempfile.TemporaryDirectory(prefix='rank-relocation-') as tmp:
        for name in manifest['files']:
            dest=Path(tmp)/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(HERE/name,dest)
        relocated,cmd=cli('easy',5,91,Path(tmp)/manifest['entrypoint'],tmp)
        assert relocated.returncode==0,relocated.stderr
        assert relocated.stdout==deterministic.stdout
    save('relocation.json',{'status':'pass','runtime_files':manifest['files'],'five_records_match_original':True})
    save('validation.json',{'status':'pass','source_banks':len(replay),'source_options':5*len(replay),'math_full_semantic_domain':capacities,'controls':len(controls),'probe_records':len(probes),'grader_records':len(records),'history_note':'No finding IDs are present in repair-history.json. The legacy_packaging_or_sampling event is tested by count-regression.json.'})
    print(json.dumps({'status':'pass','capacities':capacities,'source_banks':len(replay),'probes':len(probes),'grader_cases':len(cases)}))
if __name__=='__main__':main()

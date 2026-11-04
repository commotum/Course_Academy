"""Check the repeated-application purpose from the displayed trig angles."""
from pathlib import Path
from fractions import Fraction
import importlib.util,json,math,random,re,subprocess,sys
HERE=Path(__file__).resolve().parent;PKG=HERE.parent
sys.path.insert(0,str(HERE));sys.path.insert(0,str(PKG))
from numeric_audit import Numeric,nodes,audit
spec=importlib.util.spec_from_file_location('candidate',PKG/'generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def standard(degrees):
    return any(abs(degrees/base-round(degrees/base))<1e-8 for base in (30,45))

def visible_intermediate(record):
    prompt=record['question'][':question/problem']
    angles=[Numeric(nodes(a),{}).evaluate()*180/math.pi for _,a in re.findall(r'\\(sin|cos|sec|csc)\\left\((.*?)\\right\)',prompt)]
    assert len(angles)>=3,prompt
    # All three served factors use the original or doubled original argument.
    intermediate=max(angles)
    assert abs(min(angles)*2-intermediate)<1e-7,(prompt,angles)
    return intermediate

def cli(band,count,seed):
    cmd=[sys.executable,str(PKG/'generator.py'),'--difficulty',band,'--count',str(count),'--seed',str(seed),'--format','json']
    return json.loads(subprocess.run(cmd,capture_output=True,text=True,check=True,cwd='/tmp').stdout)

counterexamples=[]
for family,c in [('product',8),('sec_over_pair',2)]:
    r=g.construct('easy' if family=='product' else 'hard',60,c,'degrees',family,rng=random.Random(47))
    angle=visible_intermediate(r)
    assert standard(angle) and abs(angle-30)<1e-8
    assert audit(r['question'],'historical-purpose-counterexample',PKG.name)['status']=='match'
    counterexamples.append({'family':family,'after_first_application_angle_degrees':angle,'both_remaining_functions_are_prerequisite_values':True,'conclusion':'A second identity application is optional; the candidate is rejected from ordinary evaluated sampling.','record':r})

checked=[];samples=[]
for band in ('easy','moderate','hard'):
    for seed in (47,83,109):
        data=cli(band,4 if band=='easy' else 16,seed)
        samples.extend(data)
        for r in data:
            gen=r['generation'];family=gen['template']
            angle=visible_intermediate(r)
            exempt=family=='cancellation' or gen['symbolic_terminal']
            if not exempt:assert not standard(angle),(band,seed,angle,r['question'][':question/problem'])
            if band=='hard':assert gen['parameters']['coefficient'] in ('1','2')
            checked.append({'band':band,'seed':seed,'question_id':r['question'][':question/id'],'family':family,'intermediate_degrees':angle,'intentional_exemption':exempt,'status':'passed'})
# All four easy semantic instances must appear; another unit/bank does not create a fifth.
easy=cli('easy',4,47)
assert {(Fraction(r['generation']['parameters']['end_degrees']),int(r['generation']['parameters']['coefficient'])) for r in easy}=={(Fraction(e),c) for e in (30,45) for c in (4,8)}
rejected=subprocess.run([sys.executable,str(PKG/'generator.py'),'--difficulty','easy','--count','5','--seed','47','--format','json'],capture_output=True,text=True)
assert rejected.returncode and 'four distinct' in rejected.stderr
historical=[]
for item in json.loads((PKG/'source-replay.json').read_text()):
    cmd=[sys.executable,str(PKG/'generator.py'),'--replay-source',item['id'],'--format','json']
    r=json.loads(subprocess.run(cmd,capture_output=True,text=True,check=True,cwd='/tmp').stdout)[0]
    angle=visible_intermediate(r)
    expected=item['family']!='cancellation' and standard(angle)
    assert r['generation']['historical_single_application_bypass']==expected
    historical.append({'source_id':item['id'],'intermediate_degrees':angle,'historical_single_application_bypass':expected})
assert any(x['historical_single_application_bypass'] for x in historical)
(HERE/'purpose-regression-records.json').write_text(json.dumps(samples,indent=2)+'\n')
(HERE/'purpose-regression.json').write_text(json.dumps({'status':'passed','negative_controls':counterexamples,'current_cli_checks':checked,'historical_replay_checks':historical,'easy_capacity':4,'count_5_rejected':True,'conclusion':'Ordinary evaluated products and reciprocal quotients retain nonstandard intermediate angles. Cancellation remains intentionally one-use; symbolic terminals remain supported.'},indent=2)+'\n')
print(json.dumps({'status':'passed','ordinary_cli_records':len(checked),'negative_controls':len(counterexamples),'historical_replays':len(historical),'easy_capacity':4}))

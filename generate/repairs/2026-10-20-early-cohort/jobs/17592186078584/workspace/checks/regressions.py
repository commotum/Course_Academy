"""Retained finding checks against the current generator and visible records.
Offline only. Writes evidence, never runtime files or database content.
"""
import collections,importlib.util,json,math,pathlib,re,subprocess,sys
sys.dont_write_bytecode=True
P=pathlib.Path(__file__).resolve().parents[1]; E=P/'evidence';E.mkdir(exist_ok=True)
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=module('generator',P/'17592186078584.py');v=module('display_math',P/'17592186078584/validate.py')
source=load(P.parent/'source/source.json')['material']['kp']
def info(r):
 q=r['question'];f=q[':question/answer-fields'][0];ch=f[':answer-field/choices']; cid=f[':answer-field/correct'][1]
 nums=[int(re.search(r'-?\d+',a[':answer/value'])[0]) for a in ch];pos=next(i for i,a in enumerate(ch) if a[':answer/id']==cid);a=nums[pos]
 assert len(set(nums))==5
 return dict(id=q[':question/id'],template=r['generation']['template'],answer=a,rank=sorted(nums).index(a)+1,position=pos+1,values=nums)
def math_check(r):
 # Read all numerical givens from learner-visible prompt, not metadata or helper output.
 text=r['question'][':question/problem'];level=r['question'][':question/difficulty'].split('/')[-1]
 if level=='easy':
  rate,A=re.search(r'=-([\d.]+)\(T-(\d+)\)',text).groups();A=int(A)
  I=int(re.search(r'initial temperature.*?\$\{(\d+)',text)[1]);t=int(re.search(r'after \$(\d+)\$',text)[1])
  x=A+(I-A)*math.exp(-float(rate)*t)
 elif level=='moderate':
  nums=[int(n) for n in re.findall(r'\$\{(\d+)\}\^\{∘\}[CF]',text)]
  if 'Simon measures' in text:I,O,Z,A=nums[:4]
  else:I,A,O,Z=nums[:4]
  t=int(re.search(r'After \$(\d+)\$',text)[1]);x=t*math.log((Z-A)/(I-A))/math.log((O-A)/(I-A))
 else:
  A,O,L,Z=[int(n) for n in re.findall(r'\$\{(\d+)\}\^\{∘\}',text)]
  a,b=[int(n) for n in re.findall(r'after \$(\d+)\$',text)]
  x=a+(b-a)*math.log((Z-A)/(O-A))/math.log((L-A)/(O-A))
 expected=math.floor(x+.5);assert info(r)['answer']==expected,(info(r),expected)
 return dict(id=info(r)['id'],expected=expected,passed=True)
def norm(s):return re.sub(r'\s+','',s.replace(r'\left','').replace(r'\right',''))
replays=[];replay_results=[]
for sid,(t,p) in g.ORIGINALS.items():
 original=next(q for q in source[':knowledge-point/questions'] if q[':question/math-academy-id']==sid)
 r=g.generate(g.TEMPLATES[t],84199,profile=sid);q=r['question'];sf=original[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
 expected_solution=original[':question/worked-solution']
 if t=='outside':expected_solution=expected_solution.replace(r'\text{C}',r'\text{F}').replace('}C','}F')
 assert norm(q[':question/problem'])==norm(original[':question/problem']),sid
 assert norm(q[':question/worked-solution'])==norm(expected_solution),sid
 assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']),sid
 actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 assert actual==sf[':answer-field/correct'][':answer/value'],sid
 math_check(r);v.validate(r);replays.append(r);replay_results.append(dict(profile=sid,source_id=original[':question/id'],prompt=True,solution=True,bank=True,key=True,unit_correction=t=='outside'))
assert len(replays)==len(source[':knowledge-point/questions'])==11
save('source-replay-records.json',replays);save('source-replay.json',replay_results)
# Exact rejected source examples and boundary cases remain strict acceptance checks.
restricted=[]
for template,p,answer in [('coffee',dict(ambient=23,initial=80,rate='0.25',time=4),44),('coffee',dict(ambient=21,initial=40,rate='0.06',time=4),36),('body',dict(ambient=21,initial=40,rate='0.06',time=4),36),('bulb',dict(ambient=23,initial=80,rate='0.25',time=4),44),('body',dict(ambient=80,initial=95,rate='0.25',time=15),80),('body',dict(ambient=5,initial=20,rate='0.02',time=1),20)]:
 r=g.generate('easy',84199,template,parameters=p);assert info(r)['answer']==answer;math_check(r);v.validate(r);restricted.append(r)
bulb=restricted[3];assert 'fluorescent light bulb after turning off' in bulb['question'][':question/problem'];assert 'T(4)=23+57' in bulb['question'][':question/worked-solution']
save('acceptance-records.json',restricted)
# Fresh generation uses all normal layouts; each group must refute the old fixed-rank rule.
samples=[];summary={}
for template,level in g.TEMPLATES.items():
 rs=[g.generate(level,seed,template) for seed in range(84101,84113)]
 for r in rs:math_check(r)
 ranks=collections.Counter(info(r)['rank'] for r in rs);positions=collections.Counter(info(r)['position'] for r in rs)
 assert len(ranks)>1 and len(positions)>1,(template,ranks,positions)
 if level=='easy':assert any(info(r)['rank']!=3 for r in rs)
 else:assert any(info(r)['rank']!=4 for r in rs)
 for key in ('ambient','time','target','rate','initial','observed','later','start','gap'):
  vals={str(r['generation']['parameters'][key]) for r in rs if key in r['generation']['parameters']}
  if vals and not (template=='water' and key=='initial'):assert len(vals)>1,(template,key,vals)
 v.validate(rs[0]);samples.extend(rs)
 summary[template]=dict(count=len(rs),ranks=dict(ranks),positions=dict(positions),old_shortcut_correct=sum(info(r)['rank']==(3 if level=='easy' else 4) for r in rs),attempt_counts=dict(collections.Counter(r['generation']['attempts'] for r in rs)))
save('fresh-samples.json',samples);save('raw-coverage.json',summary)
# Exact old runner seed and five runner seeds: current-generation replacement.
oldbatch=load(P.parent/'samples.json');newbatch=[g.generate('easy',r['generation']['seed']) for r in oldbatch]
assert len(newbatch)==5
# Preserve exact old mathematical cases even though the expanded layout catalog
# changes seed-to-template selection. This isolates the repaired construction rule.
oldstored=load(P/'17592186078584/reference/replenishment/basis-2501/generated.json')
historical=[]
for oldrecord in oldbatch+oldstored:
 meta=oldrecord['generation'];lv=oldrecord['question'][':question/difficulty'].split('/')[-1]
 rr=g.generate(lv,meta['seed'],meta['template'],parameters=meta['parameters'])
 math_check(rr);v.validate(rr)
 assert info(rr)['answer']==info(oldrecord)['answer']
 assert norm(rr['question'][':question/problem'])==norm(oldrecord['question'][':question/problem'])
 historical.append(rr)
assert any(info(r)['rank']!=3 for r in historical[:5])
assert any(info(r)['rank']!=4 for r in historical[5:])
save('historical-counterexamples-current.json',historical)
for r in newbatch:math_check(r)
assert any(info(r)['rank']!=3 for r in newbatch)
save('runner-replacement.json',newbatch)
# Controlled target changes and irrelevant object/bank changes at fixed numerical givens.
p=dict(ambient=25,initial=100,rate='0.05',time=6)
cf=[g.generate('easy',84161,'coffee',parameters=p),g.generate('easy',84161,'coffee',parameters={**p,'time':9}),g.generate('easy',84161,'compressor',parameters=p)]
m=dict(ambient=24,initial=150,observed=100,target=60,time=15)
cf.extend([g.generate('moderate',84161,'pork',parameters=m),g.generate('moderate',84161,'pork',parameters={**m,'target':50})])
assert [info(r)['answer'] for r in cf[:3]]==[81,73,81]
assert info(cf[3])['answer']!=info(cf[4])['answer']
for r in cf:math_check(r);v.validate(r)
assert 'after $9$ minutes' in cf[1]['question'][':question/problem'] and 'T(9)=25+75' in cf[1]['question'][':question/worked-solution']
assert '${50}^{∘}C' in cf[4]['question'][':question/problem'] and 'T({t}_{1}) & =50' in cf[4]['question'][':question/worked-solution']
fixed=[g.generate('easy',seed,'coffee',parameters=p) for seed in range(84101,84113)]
assert len({info(r)['rank'] for r in fixed})>1
assert len({info(r)['answer'] for r in fixed})==1
assert len({r['question'][':question/problem'] for r in fixed})==len({r['question'][':question/worked-solution'] for r in fixed})==1
save('counterfactual-records.json',cf+fixed)
save('counterfactual-results.json',dict(relevant_easy=[info(cf[0]),info(cf[1])],irrelevant_context=[info(cf[0]),info(cf[2])],relevant_target=[info(cf[3]),info(cf[4])],fixed_parameters=[info(r) for r in fixed]))
# Reject genuine domain violations, not distractor-induced restrictions.
for changes in [dict(time=0),dict(initial=25),dict(rate='-0.05')]:
 try:g.generate('easy',0,'coffee',parameters={**p,**changes})
 except ValueError:pass
 else:raise AssertionError(changes)
# One batched native-grader input checks every option for independent mathematical keys.
representatives=historical+newbatch+replays+restricted+cf+[r for r in samples if r['generation']['seed']==84101]+fixed[:2]
for r in representatives:math_check(r)
cases=[]
for i,r in enumerate(representatives):
 f=r['question'][':question/answer-fields'][0];answer=info(r)['answer']
 cases.append(dict(label=f'current-{i}',record=r,checks=[dict(field_index=0,submitted_answer_id=a[':answer/id'],expected='accepted' if int(re.search(r'\d+',a[':answer/value'])[0])==answer else 'rejected',purpose='Independent displayed-prompt model, rounded integer, all offered radio responses') for a in f[':answer-field/choices']]))
save('grader-input.json',cases)
save('math-results.json',dict(records=len(samples)+len(representatives),stage_counts=v.COUNTS,passed=True))
save('render-records.json',[restricted[3],next(r for r in replays if r['generation']['template']=='body'),next(r for r in replays if r['generation']['template']=='pork'),cf[1]])
# Shared actual publisher filters: the full sample and runner batch.
repo=pathlib.Path('/home/jake/Developer/Course_Academy')
for level in g.LEVELS:
 rs=[r for r in samples if r['question'][':question/difficulty'].endswith('/'+level)]
 save(f'delivery-{level}-input.json',rs)
 cmd=[sys.executable,str(repo/'generate/pipeline/check_delivery.py'),'--input',str(E/f'delivery-{level}-input.json'),'--source',str(P.parent/'source/source.json'),'--inventory',str(P.parent/'source/inventory.json'),'--difficulty',level,'--output',str(E/f'delivery-{level}'),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math']
 subprocess.run(cmd,check=True,capture_output=True,text=True)
 accepted=load(E/f'delivery-{level}/accepted.json')
 assert len(accepted)==len(rs)
 for t in {r['generation']['template'] for r in rs}:
  ars=[r for r in accepted if r['generation']['template']==t]
  assert len({info(r)['rank'] for r in ars})>1
  assert len({info(r)['position'] for r in ars})>1
cmd=[sys.executable,str(repo/'generate/pipeline/check_delivery.py'),'--input',str(E/'runner-replacement.json'),'--source',str(P.parent/'source/source.json'),'--inventory',str(P.parent/'source/inventory.json'),'--difficulty','easy','--output',str(E/'delivery-runner'),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math']
subprocess.run(cmd,check=True,capture_output=True,text=True)
assert len(load(E/'delivery-runner/accepted.json'))==5
save('regression-results.json',dict(passed=True,findings=['ac0c1cf7997b4910bec6','20d9dfcf2465e68e0ac7','e86a572838bfd263537b'],source_profiles=len(replays),bank_choices=55,distractors=44,source_acceptance_cases=len(restricted),fresh_records=len(samples),coverage=summary,runner=[info(r) for r in newbatch],delivery='All sample records survive; within-template rank and position counterexamples retained'))
print(json.dumps(dict(passed=True,source_profiles=len(replays),source_acceptance_cases=len(restricted),fresh_records=len(samples),native_cases=len(cases),ranks={k:d['ranks'] for k,d in summary.items()}),indent=2))

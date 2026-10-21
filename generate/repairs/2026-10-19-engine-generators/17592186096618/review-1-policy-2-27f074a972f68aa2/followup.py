import sys,os,json,subprocess,shutil,hashlib,collections
from pathlib import Path
sys.dont_write_bytecode=True
from audit import *
# Recheck only parser gaps; no new samples.
results=json.loads((E/'math-results.json').read_text()); lookup={r['question'][':question/id']:r for r in json.loads((E/'samples.json').read_text())+json.loads((E/'replays.json').read_text())+json.loads((E/'runner-batch.json').read_text())+json.loads((E/'counterfactual-records.json').read_text())}
for i,v in enumerate(results):
 if v['failures']:results[i]=inspect(lookup[v['id']])
save('math-results.json',results)
# Preserve the required accepted outcome against the repaired native engine.
cases=json.loads((E/'grader-input.json').read_text())
for case in cases:
 if case['label']=='valid ln4=2ln2 equivalent':
  case['checks'][0]['expected']='accepted';case['checks'][0]['purpose']+='; exact logarithm identity must be accepted'
save('grader-observed-input.json',cases)
# Replay and relocate runtime only inside evidence.
pack={};same=[]
for kw in json.loads((E/'requests.json').read_text())[:16]:same.append(g.generate(**kw)==g.generate(**kw))
pack['deterministic_replay']=all(same)
rejections=[]
for kw in [{'level':'hard'},{'template':'polynomial_log_blank','parameters':{'n':2,'h':0}},{'template':'base_log_left_blank','parameters':{'b':1,'d':7,'k':1}},{'template':'base_sin_left_blank','parameters':{'b':11}},{'template':'power_exp_radio','parameters':{'c':True,'n':2,'k':1}},{'template':'base_sin_left_blank','target':'middle'}]:
 try:g.generate(**kw);rejections.append({'parameters':kw,'outcome':'accepted'})
 except Exception as ex:rejections.append({'parameters':kw,'outcome':'rejected','reason':str(ex)})
pack['rejections']=rejections;pack['canonical_replay_supported']=g.generate(template='polynomial_log_blank',parameters={'n':2,'h':0}) is not None
dest=E/'relocated';dest.mkdir(exist_ok=True)
for name in ['generator.py','math_format.py','requirements.txt']:shutil.copyfile(W/name,dest/name)
cmd=[str(ROOT/'.venv/bin/python'),'-B',str(dest/'generator.py'),'--seed','701229','--count','5']
p=subprocess.run(cmd,cwd=E,capture_output=True,text=True);(E/'relocated-samples.json').write_text(p.stdout);(E/'relocated-stderr.txt').write_text(p.stderr or 'No stderr.\n');pack['relocation']={'command':cmd,'exit_code':p.returncode,'matches_original':[g.generate(seed=701229+i) for i in range(5)]==json.loads(p.stdout),'external_output':'stdout JSON only; no images, files, network or database code in runtime'}
pack['dependencies']=json.loads((E/'runtime.json').read_text());pack['rejection_analysis']='No rejection/resampling loop in normal generation; domain guards fail explicit invalid parameters and complete-bank ambiguity checks raise. All 128 selected fresh/boundary calls succeeded; no cases were silently resampled.'
save('packaging.json',pack)
# Surface-only probes conditional on each recognizable radio template, pre/post delivery.
probes=[];coverage={}
for stage,file in [('raw','samples.json'),('delivered','delivery/accepted.json'),('batch','batch-delivery/accepted.json')]:
 rs=json.loads((E/file).read_text());groups=collections.defaultdict(list)
 for r in rs:groups[r['generation']['template']].append(r)
 coverage[stage]={t:{'count':len(rr),'targets':dict(collections.Counter(r['generation']['target'] for r in rr)),'signs':dict(collections.Counter(str(r['generation']['parameters'].get('k')) for r in rr))} for t,rr in groups.items()}
 for t,rr in groups.items():
  if not t.endswith('radio'):continue
  for label,select in [('first position',lambda aa:0),('shortest string',lambda aa:min(range(len(aa)),key=lambda i:len(aa[i][':answer/value']))),('longest string',lambda aa:max(range(len(aa)),key=lambda i:len(aa[i][':answer/value'])))]:
   hits=sum(r['question'][':question/answer-fields'][0][':answer-field/choices'][select(r['question'][':question/answer-fields'][0][':answer-field/choices'])][':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in rr)
   probes.append({'stage':stage,'template':t,'strategy':label,'correct':hits,'total':len(rr),'baseline':0.2,'records_file':file})
save('shortcut-results.json',probes);save('coverage.json',coverage)
# The configured selector is uniform within eligible easy records; reproduce its exact digest draw over synthetic ordered IDs assigned after delivery.
rs=json.loads((E/'delivery/accepted.json').read_text());counts=collections.Counter();selected=[]
for i in range(256):
 seed='independent-review-803c-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);idx=int(u*len(rs));r=rs[idx];counts[r['generation']['template']]+=1;selected.append({'seed':seed,'synthetic_id':idx+1,'question_id':r['question'][':question/id'],'template':r['generation']['template'],'target':r['generation']['target']})
save('selection.json',{'captured_basis':3950,'source_code':'engine/rust/question_selection.rs:105-199','assumptions':['fresh accepted records given synthetic ordered IDs 1..N','configured policy with positive easy weight; all candidates easy','no live learner history or allocated database IDs available'],'unconfigured_policy':'without distribution select() chooses first sorted ID deterministically; coverage claim does not apply to that legacy configuration','counts':dict(counts),'draws':selected,'stage_counts':{'raw':len(json.loads((E/'samples.json').read_text())),'accepted':len(rs),'selected_draws':256},'limitation':'Exact hash and within-band draw faithfully reproduced read-only. Synthetic IDs demonstrate rule behavior, not actual learner sequences.'})
print('math failures',sum(bool(v['failures']) for v in results),'replay',pack['deterministic_replay'],'relocation',pack['relocation']['matches_original']);print('shortcut probes',[(v['stage'],v['template'],v['strategy'],v['correct'],v['total']) for v in probes if v['correct']==v['total']])
(E/'session-state.md').write_text('Independent source analysis, 128 fresh/boundary samples, 17 source replays, 160 independent arithmetic checks and delivery filtering complete. Native grader demonstrably cannot accept valid 4^x/(2x ln2) for 4^x/(x ln4). Original failing expected-accept input and log preserved; observed-input characterizes this gap. Renderer running. Runtime relocation and guard tests saved. Package unchanged; finish UI inspection and final variation report.\n')

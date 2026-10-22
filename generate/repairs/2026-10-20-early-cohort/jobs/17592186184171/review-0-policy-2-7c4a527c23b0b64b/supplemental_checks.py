import json,pathlib,sys,importlib.util
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent/'workspace'));sp=importlib.util.spec_from_file_location('g',R.parent/'workspace/17592186184171.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
q=json.load(open(R.parent/'source/source.json'))['material']['kp'][':knowledge-point/canonical-example'];r=g.generate('easy',seed=802103,parameters={'m':3,'n':5,'k':3},profile='small');json.dump([r],open(R/'canonical-replay-records.json','w'),indent=2);json.dump({'source_id':q[':question/id'],'parameters':{'m':3,'n':5,'k':3},'expected':2,'generated_final':'2','solution_stages':['state theorem','identify n=5 and rank=3','substitute','subtract 5-3','conclude nullity=2'],'answer_bank':'No canonical bank captured; tested bank is the identical-parameter practice profile, not asserted canonical evidence.'},open(R/'canonical-replay.json','w'),indent=2)
x=json.load(open(R/'shortcut-results.json'))
for stage,path in [('raw-moderate','moderate-samples.json'),('delivered-moderate','delivery-moderate/accepted.json')]:
 rs=json.load(open(R/path));subgroups=[('overall','overall',rs)]
 for key in ['template','profile']:
  for val in sorted(set(r['generation'][key] for r in rs)):subgroups.append((key+':'+val,'within_template' if key=='template' else 'other_recognizable_subgroup',[r for r in rs if r['generation'][key]==val]))
 for label,scope,rr in subgroups:
  def answer(r):
   f=r['question'][':question/answer-fields'][0];return int(next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1]))
  success=sum(answer(r)==1 for r in rr)
  x[stage]['probes'].append({'cue':'template identity / bank range','subgroup':stage+':'+label,'scope':scope,'strategy':'Always select integer 1 without reading the null space.','correct':success,'total':len(rr),'baseline':0.2,'disposition':'not_predictive','conclusion':f'Constant answer 1 succeeds {success}/{len(rr)}, not a deterministic cue. Baseline 0.2 is random choice among five. This does not prove absence of other shortcuts.','sample_refs':[path,'shortcut-results.json']})
json.dump(x,open(R/'shortcut-results.json','w'),indent=2)
print('Added canonical replay and moderate template/bank constant-answer probes.')

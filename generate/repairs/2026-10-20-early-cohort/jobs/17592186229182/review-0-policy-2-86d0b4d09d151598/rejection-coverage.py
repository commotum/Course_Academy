import json,pathlib,sys,importlib.util,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;P=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186229182/workspace')
s=importlib.util.spec_from_file_location('g',P/'17592186229182.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
original=g.sample;attempts=[];outputs=[]
for seed in range(8101,8141):
 def wrapped(meta,rng):
  p=original(meta,rng);full=dict(p,kind=meta['kind'])
  try:d=g.guard(full,meta,'easy');g.authored_bank(d,meta['kind']);reason='accepted'
  except Exception as e:reason=str(e)
  attempts.append({'seed':seed,'parameters':p,'outcome':reason});return p
 g.sample=wrapped;outputs.append(g.generate('easy',seed))
g.sample=original
report={'seeds':[8101,8140],'proposal_count':len(attempts),'output_count':len(outputs),'outcomes':dict(collections.Counter(p['outcome'] for p in attempts)),'proposals':attempts,'interpretation':'Instrumented sample() in memory only, recording unchanged guard/bank rejection. The normal generator resamples up to 2000 times per output. Source masks and their exponent/direction stay fixed. Outputs exactly match easy-samples.json.','output_replay_match':outputs==json.load(open(E/'easy-samples.json'))}
(E/'rejection-coverage.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='proposals'}))

"""Strict independent acceptance tests; exits 1 while demonstrated defects persist."""
import sys,pathlib,importlib.util,json,re,argparse
sys.dont_write_bytecode=True
p=argparse.ArgumentParser();p.add_argument('--package',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);args=p.parse_args()
spec=importlib.util.spec_from_file_location('tested',args.package/'17592186119806.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
results=[]
for sid,rank in [('q-34601',2),('q-105161',1)]:
 rows=[]
 for k in (1,2,3):
  for target in g.eligible_targets(sid):
   r=g.generate('easy',48291,sid,{'scale':k,'target':list(target)});f=r['question'][':question/answer-fields'][0];ch=f[':answer-field/choices'];vals=sorted(int(a[':answer/value']) for a in ch);key=next(int(a[':answer/value']) for a in ch if a[':answer/id']==f[':answer-field/correct'][1]);rows.append({'parameters':r['generation']['parameters'],'rank':vals.index(key)+1,'record':r})
 results.append({'test':'Defeat always choose scalar rank '+str(rank)+' in '+sid,'passed':any(r['rank']!=rank for r in rows),'counterexamples_to_shortcut':sum(r['rank']!=rank for r in rows),'records':rows})
try:
 r=g.generate('easy',48291,'q-105158',{'scale':1,'target':None})
 results.append({'test':'Replay complete captured source q-105158','passed':True,'record':r})
except ValueError as e:results.append({'test':'Replay complete captured source q-105158','passed':False,'exception':str(e)})
args.output.write_text(json.dumps({'command':sys.argv,'passed':all(t['passed'] for t in results),'tests':results},indent=2)+'\n')
print(json.dumps({'passed':all(t['passed'] for t in results),'tests':[{k:v for k,v in t.items() if k not in ['records','record']} for t in results]}))
sys.exit(0 if all(t['passed'] for t in results) else 1)

import json,subprocess,sys,os,re,collections
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generators.json').read_text());out=[];report=[];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':'/tmp/course-academy-kp17592186192790-checkdeps'}
probe=r'''import sys,runpy,json,inspect
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));m=runpy.run_path(str(p));o={}
for k in ['TEMPLATES','FAMILIES','SPECS','CASES','PROFILES','SUPPORTED_LEVELS','LEVELS']:
 v=m.get(k)
 if isinstance(v,dict):o[k]={str(a): (b if isinstance(b,(str,int,list,tuple,dict))else str(b)) for a,b in v.items()}
 elif isinstance(v,(list,tuple)):o[k]=v
print(json.dumps(o,default=str))'''
if (H/'generator-full-invocations.json').exists():
 report=json.loads((H/'generator-full-invocations.json').read_text());out=json.loads((H/'generator-full-samples.json').read_text())
done={x['kp']for x in report}
for g in G:
 if g['kp']in done:continue
 code=Path(g['path']).read_text();p=subprocess.run([sys.executable,'-c',probe,g['path']],capture_output=True,text=True,env=env,timeout=120)
 try:meta=json.loads(p.stdout)
 except:report.append({'kp':g['kp'],'probe_error':p.stderr});continue
 info={'kp':g['kp'],'meta':meta,'invocations':[]};jobs=[]
 if "'--template'"in code or '"--template"'in code:
  spec=meta.get('TEMPLATES')or meta.get('SPECS')or meta.get('CASES')or{}
  if isinstance(spec,list):spec={str(n):None for n in spec}
  for name,v in spec.items():
   level=v.get('level',v.get('difficulty'))if isinstance(v,dict)else v[0]if isinstance(v,(list,tuple))else v
   if level not in['easy','moderate','hard']:
    # Template has no explicit workload metadata; let CLI test each supported band.
    levels=['easy','moderate']if g['kp']==17592186147456 else['easy','moderate','hard']
   else:levels=[level]
   for level in levels:jobs.append((level,['--template',name],2))
 # Cycle complete default families and roles in every supported band, including
 # generators whose public CLI deliberately hides source-only replay profiles.
 for level in['easy','moderate','hard']:
  if g['kp']==17592186147456 and level=='hard'or g['kp']==17592186217247 and level!='easy':continue
  families=meta.get('FAMILIES',{});n=len(families.get(level,[]))if isinstance(families,dict)and isinstance(families.get(level),list)else 0
  count=max(12,min(48,4*n))
  jobs.append((level,[],count))
 for level,extra,count in jobs:
  args=[sys.executable,g['path'],'--difficulty',level,'--count',str(count),'--seed','271028','--format','json',*extra]
  try:
   p=subprocess.run(args,capture_output=True,text=True,env=env,timeout=180)
   if p.returncode:raise ValueError(p.stderr[-500:])
   records=json.loads(p.stdout);records=records if isinstance(records,list)else[records]
   for r in records:out.append({'kp':g['kp'],'band':level,'record':r,'kind':'explicit-template'if extra else'fresh-family-cycle','arguments':extra})
   info['invocations'].append({'band':level,'args':extra,'records':len(records),'passed':True})
  except Exception as ex:info['invocations'].append({'band':level,'args':extra,'passed':False,'error':str(ex)})
 report.append(info);print(g['kp'],sum(j.get('records',0)for j in info['invocations']),'records',flush=True)
 (H/'generator-full-samples.json').write_text(json.dumps(out,indent=2)+'\n');(H/'generator-full-invocations.json').write_text(json.dumps(report,indent=2)+'\n')
print('records',len(out))

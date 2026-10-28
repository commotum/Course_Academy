import importlib.util,inspect,json,os,sys,time
from pathlib import Path
sys.dont_write_bytecode=True;src=Path(sys.argv[1]);outfile=Path(sys.argv[2]);sys.path.insert(0,str(src.parent));spec=importlib.util.spec_from_file_location('template_audit',src);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
BANDS=('easy','moderate','hard');supported=json.loads(sys.argv[3]);selectors={b:set()for b in supported};poolproof=[]
def bandof(v):
 if isinstance(v,dict):
  for k in['level','difficulty',':question/difficulty']:
   z=v.get(k);z=z.get(':db/ident')if isinstance(z,dict)else z
   if isinstance(z,str)and z.split('/')[-1]in BANDS:return z.split('/')[-1]
 if isinstance(v,(tuple,list)):
  for z in v:
   if isinstance(z,str)and z in BANDS:return z
 return None
for name in['LEVELS','LEVEL','FAMILIES','TEMPLATES','CASES','SPECS','MODELS','DATA']:
 pool=getattr(m,name,None)
 if not isinstance(pool,dict)or len(pool)>300:continue
 poolproof.append({'pool':name,'keys':list(map(str,pool))})
 if set(pool)&set(BANDS):
  for b,v in pool.items():
   if b in supported and isinstance(v,(list,tuple,set)):
    selectors[b].update(z for z in v if isinstance(z,str))
 else:
  for k,v in pool.items():
   if not isinstance(k,str)or k in BANDS:continue
   b=bandof(v)
   for band in([b]if b in supported else supported):selectors[band].add(k)
results=[];records=[]
for band,names in selectors.items():
 func=getattr(m,'generate_'+band,None)
 if not callable(func):func=getattr(m,'generate',None)
 if not callable(func):results.append({'band':band,'error':'No public generate API'});continue
 for name in sorted(names or{None},key=str):
  args={'seed':983755,'template':name};args={k:v for k,v in args.items()if v is not None}
  try:
   if getattr(m,'generate_'+band,None)is func:r=func(**args)
   else:r=func(band,**args)
   rs=[r]if isinstance(r,dict)and'question'in r else r if isinstance(r,list)else[]
   if not rs:raise ValueError('API returned no question records')
   results.append({'band':band,'template':name,'passed':True,'records':len(rs)})
   records.extend({'level':band,'template_selector':name,'record':r}for r in rs)
  except Exception as ex:results.append({'band':band,'template':name,'rejected_selector':True,'error':str(ex)[:250]})
 outfile.write_text(json.dumps({'source':str(src),'pools':poolproof,'results':results,'samples':records},indent=2))
print(len(records),len(results),flush=True)

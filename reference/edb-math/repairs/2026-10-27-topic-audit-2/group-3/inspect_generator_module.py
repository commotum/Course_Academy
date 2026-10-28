import importlib.util,json,os,sys
from pathlib import Path
sys.dont_write_bytecode=True;p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));spec=importlib.util.spec_from_file_location('audit_generator',p);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
def level(v):
 if isinstance(v,dict):
  for k in ['level','difficulty',':question/difficulty']:
   x=v.get(k)
   if isinstance(x,dict):x=x.get(':db/ident')
   if isinstance(x,str):return x.split('/')[-1]
  for k in ['source','question']:
   if k in v:
    out=level(v[k])
    if out:return out
 return None
pools={}
for name in ['TEMPLATES','CASES','CASE','SOURCES','SOURCE','Q','ORIGINALS','FAMILY','LEVEL','PROFILES']:
 v=getattr(m,name,None)
 if isinstance(v,dict)and len(v)<500:
  pools[name]=[{'name':str(k),'level':level(x)or x if name=='LEVEL'and isinstance(x,str)else level(x)}for k,x in v.items()]
 elif isinstance(v,list)and len(v)<500 and v and isinstance(v[0],dict):
  rows=[]
  for x in v:
   namekey=x.get('template')or x.get(':question/math-academy-id')or x.get('name')
   if namekey:rows.append({'name':namekey,'level':level(x)})
  pools[name]=rows
supported={k:list(v)for k in ['SUPPORTED_LEVELS','LEVELS']if isinstance(v:=getattr(m,k,None),(list,tuple,set))and all(isinstance(x,str)for x in v)}
print(json.dumps({'pools':pools,'supported':supported,'version':getattr(m,'VERSION',None)}))

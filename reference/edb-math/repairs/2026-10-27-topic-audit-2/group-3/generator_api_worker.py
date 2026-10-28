import importlib.util,json,os,sys,inspect
from pathlib import Path
sys.dont_write_bytecode=True;p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));spec=importlib.util.spec_from_file_location('audit_generator',p);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);records=[];calls=[];levels=('easy','moderate','hard')
def call(label,fn,kind,*args,**kw):
 row={'label':label,'kind':kind,'args':str(args),'kwargs':kw}
 try:
  result=fn(*args,**kw);rs=result if isinstance(result,list)else[result];rs=[r for r in rs if isinstance(r,dict)and'question'in r];row['records']=len(rs)
  for r in rs:records.append({'kind':kind,'record':r,'arguments':label})
 except Exception as ex:row.update({'error':str(ex)[:500],'classification':'unsupported API/template/band or policy rejection; not a valid sample'})
 calls.append(row)
# Actual public generate() (including installed policy wrapper) covers explicit families.
templates=set()
for name in ['TEMPLATES','SPECS','FAMILY','MODELS','LEVELS']:
 v=getattr(m,name,None)
 if isinstance(v,dict):templates|={k for k in v if isinstance(k,str)and k not in levels and not k.startswith(':')}
 elif isinstance(v,(list,tuple))and all(isinstance(k,str)for k in v):templates|={k for k in v if k not in levels}
if hasattr(m,'generate'):
 for t in sorted(templates):
  for level in levels:call(level+'/'+t,m.generate,'fresh-explicit-template',level,seed=912231,template=t)
# Explicit evidence-only source replay APIs, never fed into fresh sampling.
if hasattr(m,'replay_sources'):call('replay_sources',m.replay_sources,'source-replay')
if hasattr(m,'replay_source'):
 candidates=set()
 for name in ['CASE','SOURCES','SOURCE_PARAMETERS']:
  v=getattr(m,name,None)
  if isinstance(v,dict):candidates|={k for k in v if isinstance(k,str)and not k.startswith(':')and k not in levels}
 if hasattr(m,'CANONICAL')and isinstance(m.CANONICAL,dict):
  sid=m.CANONICAL.get(':question/math-academy-id')
  if sid:candidates.add(sid)
 for sid in sorted(candidates):call('replay_source/'+sid,m.replay_source,'source-replay',sid)
if hasattr(m,'replay'):
 sig=inspect.signature(m.replay)
 if len(sig.parameters)==0:call('replay()',m.replay,'source-replay')
print(json.dumps({'records':records,'calls':calls},default=str))

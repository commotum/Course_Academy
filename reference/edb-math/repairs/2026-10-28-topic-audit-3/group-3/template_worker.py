import importlib.util,inspect,json,os,sys,time,random
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
 known={'level':band,'difficulty':band,'band':band,'count':1,'seed':983755,'output':Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']),'output_dir':Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']),'out':Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']),'outdir':Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']),'rng':random.Random(983755)}
 if callable(getattr(m,'parameters',None)):
  try:known['p']=next(iter(m.parameters(band)))
  except Exception:pass
 funcs=[getattr(m,n,None)for n in ['generate_'+band,'generate','build','batch','generate_batch','generate_one','sample_batch','sample']];func=None
 for candidate in funcs:
  if not callable(candidate):continue
  sig=inspect.signature(candidate)
  required={k for k,v in sig.parameters.items()if v.default is inspect.Parameter.empty and v.kind not in[inspect.Parameter.VAR_POSITIONAL,inspect.Parameter.VAR_KEYWORD]}
  if required<=set(known)|{'template','family'}:func=candidate;break
 if func is None:results.append({'band':band,'error':'Public API needs explicit model/parameters; CLI baseline remains covered'});continue
 sig=inspect.signature(func);params=sig.parameters;selector='template'if'template'in params else'family'if'family'in params else None
 # A batch-only API does not expose selectors; do not misclassify ignored keywords as template coverage.
 varkw=any(v.kind==inspect.Parameter.VAR_KEYWORD for v in params.values())
 if selector is None and varkw:selector='template'
 if selector is None:names={None}
 for name in sorted(names or{None},key=str):
  args={k:v for k,v in known.items()if k in params}
  if varkw:args['seed']=983755
  if name is not None:args[selector]=name
  try:
   r=func(**args);rs=[r]if isinstance(r,dict)and'question'in r else r if isinstance(r,list)else[]
   if not rs:raise ValueError('API returned no question records')
   results.append({'band':band,'template':name,'api':func.__name__,'passed':True,'records':len(rs)})
   records.extend({'level':band,'template_selector':name,'record':r}for r in rs)
  except Exception as ex:results.append({'band':band,'template':name,'api':func.__name__,'rejected_selector':True,'error':str(ex)[:250]})
outfile.write_text(json.dumps({'source':str(src),'pools':poolproof,'results':results,'samples':records},indent=2))
print(len(records),len(results),flush=True)

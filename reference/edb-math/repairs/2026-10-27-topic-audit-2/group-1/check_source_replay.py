import concurrent.futures,json,os,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];D=json.loads((H/'current.json').read_text());G=dict(D['generators']);stages={c['kp']:c for c in json.loads((H/'format-generator-stage-config.json').read_text())};tasks=[]
code=r'''
import importlib.util,json,sys
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));spec=importlib.util.spec_from_file_location('replay_probe',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);mode=sys.argv[2]
def probe(source,fn):
 try:return {'source':source,'record':fn(source)}
 except Exception as ex:return {'source':source,'error':type(ex).__name__+': '+str(ex)}
if mode=='monomial':records=[probe(k,m.replay_source)for k in m.SOURCE_SPECS]
elif mode=='radical':records=[probe(k,m.replay)for k in m.SOURCE_SPEC]
elif mode=='reciprocal':records=[probe(k,m.source_replay)for k in m.ORIGINAL_PARAMETERS]
elif mode=='sum':
 rows=json.loads(p.with_name('source_cases.json').read_text());records=[probe(r['source_name'],m.replay_source)for r in rows]
print(json.dumps(records,default=str))
'''
for k,mode in[(17592186064167,'monomial'),(17592186064168,'radical'),(17592186064169,'reciprocal'),(17592186184155,'sum')]:
 old=Path('/media/jake/SSD/EDB/math')/G[k][':question-generator/script'];new=Path(stages[k]['directory'])/stages[k]['entrypoint'];old=old.with_name('legacy.py')if mode=='sum'else old;new=new.with_name('legacy.py')if mode=='sum'else new;tasks.append((k,mode,old,new))
def run(task):
 k,mode,old,new=task;results=[]
 for p in[old,new]:
  r=subprocess.run([str(R/'.venv/bin/python'),'-c',code,str(p),mode],text=True,capture_output=True,timeout=60,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});results.append({'returncode':r.returncode,'stderr':r.stderr,'records':json.loads(r.stdout)if r.returncode==0 else[]})
 a,b=results;checks=[]
 if a['returncode']==b['returncode']==0:
  for left,right in zip(a['records'],b['records']):
   if 'error'in left or'error'in right:
    checks.append({'source':left['source'],'old_error':left.get('error'),'staged_error':right.get('error'),'same_guard':left.get('error')==right.get('error')});continue
   l,r=left['record']['question'],right['record']['question'];attrs=[':question/problem',':question/worked-solution'];checks.append({'source':left['source'], 'raw_prose_equal':all(l.get(attr)==r.get(attr)for attr in attrs),'choice_values_equal':sorted(v[':answer/value']for f in l.get(':question/answer-fields',[])for v in f.get(':answer-field/choices',[]))==sorted(v[':answer/value']for f in r.get(':question/answer-fields',[])for v in f.get(':answer-field/choices',[]))})
 return {'kp':k,'api':mode,'old':a,'staged':b,'checks':checks}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:out=list(pool.map(run,tasks))
(H/'source-replay-validation.json').write_text(json.dumps(out,indent=2));print([(r['kp'],r['old']['returncode'],r['staged']['returncode'],len(r['checks']),sum(c.get('raw_prose_equal',False)for c in r['checks']),sum(c.get('choice_values_equal',False)for c in r['checks']))for r in out])

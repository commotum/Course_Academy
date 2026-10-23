"""Current-package regression for a68a8999b8ec7f376999 (never reads old batch).
Run: .venv/bin/python -B checks/regression.py
"""
from audit_helpers import *
from shortcut_probe import probe
OUT=ROOT/'author-regression'; OUT.mkdir(exist_ok=True)
def write(name,data): (OUT/name).write_text(json.dumps(data,indent=2,default=str))
def cli(path):
 env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(OUT/'assets')}
 result=subprocess.run([sys.executable,'-B',str(PKG/'generator.py'),'--difficulty','easy','--seed','3173462200','--count','5','--format','json'],check=True,capture_output=True,text=True,env=env)
 path.write_text(result.stdout);return json.loads(result.stdout)
def delivery(path,level):
 cmd=[sys.executable,'/home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py','--input',str(path),'--source',str(PKG.parent/'source/source.json'),'--inventory',str(PKG.parent/'source/inventory.json'),'--difficulty',level,'--output',str(OUT/('delivery-'+path.stem)),'--asset-root',str(OUT/'assets'),'--math-root','/media/jake/SSD/EDB/math']
 result=subprocess.run(cmd,capture_output=True,text=True)
 (OUT/('delivery-'+path.stem+'.log')).write_text(result.stdout+result.stderr)
 if result.returncode:raise RuntimeError('FAILED COMMAND: '+ ' '.join(cmd)+'\n'+result.stdout+result.stderr)
 return json.load(open(OUT/('delivery-'+path.stem)/'accepted.json'))
def check(records):
 result=[p for r in records if (p:=probe(r)) is not None]
 assert result,'No applicable radios were actually tested'
 assert not any(p['success'] for p in result),result
 return result
if __name__=='__main__':
 batch=cli(OUT/'prospective-batch.json')
 results={'batch':check(batch)}
 # The original parameters remain a forced witness even if CLI selection changes.
 witness=g.generate('easy',3173462203,'slope_sqrt_radio',parameters={'a':7,'b':37,'t':-4})
 write('exact-counterexample-current.json',[witness]);results['exact']=check([witness])
 records=[]
 for name,spec in g.TEMPLATES.items():
  if spec['field']=='radio':
   for seed in range(20):records.append(g.generate(spec['level'],90100+seed,template=name))
 write('radio-sample.json',records)
 results['raw']=check(records)
 for level in ['easy','moderate','hard']:
  subset=[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)]
  path=OUT/('radio-'+level+'.json');write(path.name,subset)
  accepted=delivery(path,level)
  results['delivered-'+level]=check(accepted) if level!='hard' else {'count':len(accepted),'spacing_probe':'not a linear radical'}
 accepted=delivery(OUT/'prospective-batch.json','easy');results['delivered-batch']=check(accepted)
 write('spacing-regression.json',results)
 print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in results.items()}))

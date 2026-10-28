import concurrent.futures,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];cfg=json.loads((H/'generator-stage-config.json').read_text());outside=Path(tempfile.mkdtemp(prefix='ca-topic3-g1-template-'));env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('_CA_SOURCE_POLICY_CHILD',None);env['PYTHONDONTWRITEBYTECODE']='1'
child=r'''
import importlib.util,inspect,json,os,sys,copy,traceback
from pathlib import Path
entry=Path(sys.argv[1]);kp=int(sys.argv[2]);sys.path.insert(0,str(entry.parent));spec=importlib.util.spec_from_file_location('template_probe',entry);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
selectors={17592186083245:'FAMILIES',17592186083280:'TEMPLATES',17592186129267:'TEMPLATES',17592186129268:'TEMPLATES',17592186133899:'FAMILIES',17592186133900:'FAMILIES',17592186133929:'CONFIG',17592186157298:'DATA',17592186175987:'SPECS',17592186176023:'FAMILIES',17592186176024:'CONFIG',17592186198389:'TEMPLATES',17592186129200:'FAMILIES'}
cases=[]
if kp==17592186172085:
 for band in ['easy','moderate','hard']:
  base=m.generate(band,seed=28109837)['generation']['parameters']
  if band=='hard':
   for mask in range(1,7):p=copy.deepcopy(base);p['mask']=mask;cases.append((band,'hard-role-mask-'+str(mask),{'parameters':p}))
  else:
   for i,fam in enumerate(['polynomial','trig','radical','reciprocal','log']):p=copy.deepcopy(base);p['families']=[fam]*3;p['mask']=i+1;cases.append((band,fam,{'parameters':p}))
else:
 values=getattr(m,selectors[kp])
 for name,value in values.items():
  if kp==17592186129200:
   for fam in value:cases.append((name,fam,{'family':fam}))
  elif kp==17592186157298:cases.append(('moderate',name,{'template':name}))
  elif kp==17592186175987:cases.append(('moderate',name,{'template':name}))
  else:
   level=value.get('level',value.get('difficulty'))if isinstance(value,dict)else value[0]
   if level in['easy','moderate','hard']:cases.append((level,name,{'template':name}))
 if kp==17592186083245:cases.append(('easy','linear_quadratic',{'template':'linear_quadratic'}))
 if kp==17592186175987:cases.extend([('easy','easy_constant',{'template':'easy_constant'}),('hard','hard_polynomial',{'template':'hard_polynomial'})])
reports=[];records=[]
for index,(band,name,kwargs)in enumerate(cases):
 try:
  r=m.generate(band,seed=28109837+index,**kwargs);records.append(r);reports.append({'band':band,'template':name,'status':'pass','question':r['question'][':question/id'],'generation':r['generation']})
 except Exception as e:reports.append({'band':band,'template':name,'status':'rejected','error':type(e).__name__+': '+str(e),'trace':traceback.format_exc()})
print(json.dumps({'kp':kp,'cases':reports,'records':records},default=str))
'''
(outside/'probe.py').write_text(child)
def run(c):
 root=outside/str(c['kp']);root.mkdir()
 for f in c['files']:p=root/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(c['directory'])/f,p)
 assets=outside/'outputs'/str(c['kp']);assets.mkdir(parents=True)
 try:
  r=subprocess.run([str(R/'.venv/bin/python'),str(outside/'probe.py'),str(root/c['entrypoint']),str(c['kp'])],cwd=outside,env={**env,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets)},text=True,capture_output=True,timeout=240)
  return {'kp':c['kp'],'returncode':r.returncode,'stderr':r.stderr,'cwd':str(outside),'result':json.loads(r.stdout)if r.returncode==0 else None}
 except Exception as ex:return {'kp':c['kp'],'error':str(ex),'result':None}
results=[];records=[]
if len(sys.argv)>1:
 selected={int(v)for v in sys.argv[1:]};cfg=[c for c in cfg if c['kp']in selected]
 results=[r for r in json.loads((H/'stage-template-tests.json').read_text())if r['kp']not in selected]
 records=[r for r in json.loads((H/'stage-template-samples.json').read_text())if r['knowledge_point']['db_id']not in selected]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 for r in pool.map(run,cfg):
  if r.get('result'):records+=r['result'].pop('records')
  results.append(r);(H/'stage-template-tests.json').write_text(json.dumps(results,indent=2)+'\n');(H/'stage-template-samples.json').write_text(json.dumps(records,indent=2)+'\n');print(r['kp'],r.get('returncode'),len(r.get('result',{}).get('cases',[]))if r.get('result')else r.get('error'),[(c['template'],c.get('error'))for c in r.get('result',{}).get('cases',[])if c['status']!='pass']if r.get('result')else r.get('stderr'),flush=True)
print('packages',len(results),'template records',len(records),'outside',outside)

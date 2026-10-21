from audit import *
import shutil,subprocess
out={'commands':[],'determinism':[],'rejections':[],'dependencies':json.load(open('runtime.json'))}
for t,spec in g.TEMPLATES.items():
 a=g.generate(spec['level'],94179,template=t);b=g.generate(spec['level'],94179,template=t)
 out['determinism'].append({'template':t,'seed':94179,'identical':a==b})
for label,kwargs in [('wrong_level',{'level':'easy','template':'power_cos'}),('wrong_field_type',{'level':'easy','field_type':'free'}),('out_of_bounds',{'level':'easy','template':'exp_forcing','parameters':{'a':1,'b':6,'r':2}}),('resonant_wrong_family',{'level':'easy','template':'exp_forcing','parameters':{'a':3,'b':6,'r':3}}),('bad_parameter_type',{'level':'easy','template':'exp_cancel','parameters':{'a':True,'m':1}}),('observed_not_random',{'level':'easy','profile':'q-335402'}),('noninteger_count',None)]:
 if kwargs is None:continue
 try:r=g.generate(seed=94179,**kwargs);out['rejections'].append({'case':label,'rejected':False})
 except Exception as e:out['rejections'].append({'case':label,'rejected':True,'error':str(e)})
rel=ROOT/'relocated-package';rel.mkdir(exist_ok=True)
for p in PKG.iterdir():
 if p.is_file():shutil.copy2(p,rel/p.name)
cmd=[sys.executable,str(rel/'generator.py'),'--difficulty','easy','--seed','94179','--count','3']
r=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True);out['commands'].append(cmd);out['relocation']={'exit_code':r.returncode,'stderr':r.stderr,'equal_to_original':[g.generate('easy',94179+i) for i in range(3)]==json.loads(r.stdout)}
save('relocated-records.json',json.loads(r.stdout));save('packaging-results.json',out)
print('determinism',all(r['identical'] for r in out['determinism']),'relocation',out['relocation'],'rejections',len(out['rejections']))

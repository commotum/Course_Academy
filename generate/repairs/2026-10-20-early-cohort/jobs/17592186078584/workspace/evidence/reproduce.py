import importlib.util,json,sys,re
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('old',E/'old/17592186078584.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def info(r):
 f=r['question'][':question/answer-fields'][0]; ch=f[':answer-field/choices']; nums=[int(re.search(r'\d+',a[':answer/value'])[0]) for a in ch]; v=nums[[a[':answer/id'] for a in ch].index(f[':answer-field/correct'][1])]
 return dict(values=nums,answer=v,rank=sorted(nums).index(v)+1)
report={'runner_seed':info(g.generate('easy',1403253416)),'errors':[],'rank_counts':{}}
for p in [dict(ambient=23,initial=80,rate='0.25',time=4),dict(ambient=21,initial=40,rate='0.06',time=4)]:
 try:g.generate('easy',84199,'coffee',parameters=p)
 except ValueError as e:report['errors'].append(dict(parameters=p,error=str(e)))
for profile in ['q-107121','q-107123']:
 try:g.generate('easy' if profile=='q-107121' else 'moderate',84199,profile=profile)
 except ValueError as e:report['errors'].append(dict(profile=profile,error=str(e)))
for t,l in g.TEMPLATES.items():
 if l=='hard':continue
 ranks=[info(g.generate(l,seed,t))['rank'] for seed in range(84101,84106)]
 report['rank_counts'][t]=ranks
(E/'before.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

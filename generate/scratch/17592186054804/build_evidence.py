import importlib.util,json,difflib
from pathlib import Path
D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
params={
'q-40091':{'given':['1','-1'],'remaining':['-2/3','-3/4'],'scale':'12'},
'q-75795':{'given':['2','-1'],'remaining':['1/2','-3/2'],'scale':'-4'},
'q-112638':{'given':['-3','1'],'remaining':['6','-5'],'scale':'1'},
'q-270967':{'given':['1','-1'],'remaining':['2','-2'],'scale':'1'},
'q-328522':{'given':['3','-3'],'remaining':['1','-2'],'scale':'1'},
'q-337081':{'given':['-2','-3'],'remaining':['-1/3','2/3'],'scale':'9'},
'q-270970':{'given':['-3','-2'],'remaining':['1/6','3/5'],'scale':'-30'}}
cases=[]
for q in g.KP[':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];name=next(n for n,s in g.SPECS.items() if s['source']==sid)
 c={'source_id':sid,'template':name,'level':g.SPECS[name]['level'],'parameters':params[sid],'bank_profile':'raw_'+sid};cases.append(c)
 r=g.generate(c['level'],template=name,parameters=c['parameters'],profile=c['bank_profile'])
 for k in [':question/problem',':question/worked-solution']:
  if q.get(k)!=r['question'].get(k):
   print(sid,k, '\n'.join(difflib.unified_diff(q.get(k,'').splitlines(),r['question'].get(k,'').splitlines())))
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')

"""Private evidence builder; generator replay uses public parameterized API."""
import json,sys,importlib.util,difflib,re
from pathlib import Path
D=Path(__file__).resolve().parent; spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=json.loads((D/'source.json').read_text());qs=s['record'][':knowledge-point/questions'];cases=[]
for q in qs:
 ma=q[':question/math-academy-id']; profile='observed_'+ma.split('-')[1];template=g.PROFILES[profile]
 if ma=='q-106661':p={'a':150,'k':'0.5'}
 elif ma=='q-106662':p={'a':80,'k':5}
 elif ma=='q-106663':p={'a':250,'k':3,'initials':[200,400,150,50,100]}
 else:
  p={'options':[]}
  for o in q[':question/answer-fields'][0][':answer-field/choices']:
   st=o[':answer/value'].replace(r'\,',''); rhs=st.split('=')[1].split(',')[0];n=st.split('P(0)=')[1]
   if 'P-' in rhs:b,c=rhs.split('P-');c='-'+c
   else:c,b=rhs.split('-');b='-'+b[:-1]
   p['options'].append({'c':c,'b':b,'initial':n})
 cases.append({'source_id':ma,'source_db_id':q[':db/id'],'template':template,'level':g.TEMPLATES[template],'bank_profile':profile,'parameters':p})
 r=g.generate(g.TEMPLATES[template],template=template,parameters=p,profile=profile)
 print(ma)
 for key in (':question/problem',':question/worked-solution'):
  if q.get(key)!=r['question'].get(key):print(key,'DIFF\n'+''.join(difflib.unified_diff(q.get(key,'').splitlines(keepends=True),r['question'].get(key,'').splitlines(keepends=True))))
 for sf,gf in zip(q[':question/answer-fields'],r['question'][':question/answer-fields']):
  sv=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);gv=sorted(a[':answer/value'] for a in gf[':answer-field/choices']);print('BANK EXACT',sv==gv)
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')

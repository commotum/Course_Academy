import json,sys,re
from pathlib import Path
from bs4 import BeautifulSoup
from propose_controls import norm
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
s=(H/'import_historical_question_content.py').read_text();ns={'__file__':str(R/'scripts/import_historical_question_content.py')};exec(compile(s.split('def prepare():')[0],str(H/'import_historical_question_content.py'),'exec'),ns)
D=json.loads((H/'current.json').read_text());Q={q.get(':question/math-academy-id'):q for q in D['questions']};out={};review=[]
for source in json.loads((H/'sources.json').read_text()):
 if source['attribute']!='question/problem'or'selectList'not in source['html']:continue
 q=Q.get(source['identity'])
 if not q:continue
 r=ns['Renderer'](None)
 for control in BeautifulSoup(source['html'],'html.parser').select('.selectList'):
  marker=re.search(r'-(\d+)$',control.get('id',''))
  if not marker:continue
  key='field-'+str(int(marker[1])+1);fs=[f for f in q[':question/answer-fields']if f[':answer-field/key']==key]
  if len(fs)!=1:continue
  f=fs[0]
  for option in control.select('.selectListOption'):
   try:v=r.text(option)
   except:continue
   kind='answer.type/math'if re.fullmatch(r'\$[^$]+\$',v,re.S)else'answer.type/text';value=v[1:-1]if kind.endswith('/math')else v
   for a in f[':answer-field/choices']:
    before=a[':answer/type'][':db/ident'].lstrip(':')
    if norm(a[':answer/value'])!=norm(value)or before==kind:continue
    # Only source-owned actual dropdown options, never foreign historical extras.
    out[a[':db/id']]={'entity':a[':db/id'],'attribute':'answer/type','before':before,'after':kind,'reason':'Restore source-proved prose-vs-math option type using exact source DOM control index and option value; historical importer forced all dropdown options to math','evidence':{'question':q[':db/id'],'identity':source['identity'],'field':f[':db/id'],'key':key,'value':a[':answer/value'],'source':source['path'],'original_option_html':str(option)},'confidence':'high'}
(H/'type-proposals.json').write_text(json.dumps(list(out.values()),indent=2)+'\n');print('types',len(out));print([(x['evidence']['identity'],x['evidence']['key'],x['evidence']['value'])for x in out.values()])

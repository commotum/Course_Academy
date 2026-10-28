import json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
s=(H/'import_historical_question_content.py').read_text();ns={'__file__':str(R/'scripts/import_historical_question_content.py')};exec(compile(s.split('def prepare():')[0],str(H/'import_historical_question_content.py'),'exec'),ns)
Renderer=ns['Renderer'];sources=json.loads((H/'sources.json').read_text());fixtures=H/'historical-control-fixtures';fixtures.mkdir(exist_ok=True);checks=[]
for ident in ['q-337133','q-318660','q-333756','q-333727','q-337707']:
 a=next(x for x in sources if x['identity']==ident and x['attribute']=='question/problem'and x['path'].endswith('-after.json'))
 soup=BeautifulSoup(a['html'],'html.parser');r=Renderer(6353);out=r.text(soup,True)
 keys=[f['key']for f in r.fields];used=re.findall(r'\{\{([^}]+)\}\}',out)
 assert sorted(keys)==sorted(used),(ident,keys,used)
 assert not r.errors,(ident,r.errors)
 assert not any('(S'+str(i)+')'in out for i in range(10))
 assert all(c['type']=='text' for f in r.fields for c in f['choices']if c['value']in['is',"isn't",'is not'])
 (fixtures/(ident+'-after.html')).write_text(a['html'])
 checks.append({'identity':ident,'source':a['path'],'problem':out,'fields':r.fields,'errors':r.errors})
a=next(x for x in sources if x['identity']=='q-318659'and x['attribute']=='question/problem');soup=BeautifulSoup(a['html'],'html.parser')
try:Renderer(6353).text(soup,True)
except AssertionError as e:assert 'Unverified historical dropdown'in str(e)
else:raise AssertionError('source-before default must not become canonical')
(fixtures/'q-318659-before.html').write_text(a['html']);checks.append({'identity':'q-318659','source':a['path'],'unverified_before_rejected':True})
(H/'historical-controls-verification.json').write_text(json.dumps(checks,indent=2)+'\n');print('passed',len(checks))

import json,sys
from pathlib import Path
from bs4 import BeautifulSoup
sys.path.insert(0,'scripts');from question_capture.html_tables import source_table_html
H=Path(__file__).resolve().parent;R=Path.cwd();D=json.loads((H/'snapshot.json').read_text());M=json.loads((H/'source-manifest.json').read_text());p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';s=p.read_text();ns={'__file__':str(p)};exec(compile(s.split('parents=json.loads')[0]+s[s.index('def roots(s):'):s.index('def visible(tex):')],str(p),'exec'),ns);props={(r['entity'],r['attribute']):r for r in json.loads((H/'proposals.json').read_text())};evidence=[]
for eid in [17592186373003,17592186235482]:
 q=next(q for q in D['questions']if q[':db/id']==eid);sid=q[':question/math-academy-id'];path=next(p for p in M[sid]if p.endswith('-before.json'));raw=json.loads(Path(path).read_text());table=BeautifulSoup(raw['html'],'html.parser').find('table');original=str(table);r=ns['CompleteSourceRenderer'](None);r.extract_fields=True;fields={f['dom_id']:f['key']for f in raw['fields']}
 for i,node in enumerate(table.select('.mq-editable-field')):
  if not node.find_parent(id=lambda v:v in fields):
   node['id']='__source-blank-'+str(i);fields[node['id']]=raw['fields'][i]['key']
 for node in table.find_all(id=True):
  if node['id']in fields:node['class']=list(node.get('class',[]))+['freeResponseTextbox']
 def leaf(n):return'{{'+fields[n['id']]+'}}'if n.get('id')in fields else r.render(n)
 rendered=source_table_html(table,leaf).strip();before=q[':question/problem'];start=before.index('|');after=before[:start].rstrip()+'\n\n'+rendered
 ev={'source_identity':sid,'source_path':path,'raw_source_table':original,'normalized_table':rendered,'field_ids_keys_values_unchanged':True,'source_roles':'actual top/bottom border fraction cells, original row/column and vertical alignment'}
 if eid==17592186373003:ev.update({'independent_ODE_residual':0,'initial_condition':'y(2)=-1','maximal_IVP_interval':'((sqrt(17)-1)/2,infinity)'})
 else:ev.update({'multistep_context_entity':17592186235296,'functions':'f(u)=e^u/2,h(x)=-4sinx','independent_chain_rule':'fprime(h(x))*hprime(x)=-2cos(x)*exp(-4sin(x))','owned_numerator':'2cosx'})
 props[eid,'question/problem']={'entity':eid,'attribute':'question/problem','before':before,'after':after,'reason':'Recover original answer fraction cell roles from the retained source table, preserving the blank in its original numerator/denominator position.','evidence':ev,'confidence':'high'};evidence.append({'entity':eid,**ev});(H/(sid+'-original-table.html')).write_text(original);(H/(sid+'-normalized-table.html')).write_text(rendered)
(H/'proposals.json').write_text(json.dumps(list(props.values()),indent=2));(H/'source-fraction-table-evidence.json').write_text(json.dumps(evidence,indent=2));print('fraction tables',len(evidence),'props',len(props))

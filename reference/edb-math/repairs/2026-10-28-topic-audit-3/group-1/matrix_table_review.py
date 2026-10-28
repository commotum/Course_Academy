import json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import matrix_answer,validate_math_structure
D=json.loads((H/'current.json').read_text());by={q[':db/id']:q for q in D['questions']};sources=json.loads((H/'sources.json').read_text());props=json.loads((H/'source-reviewed-proposals.json').read_text());pby={(p['entity'],p['attribute']):p for p in props};checks=[]
for candidate in json.loads((H/'html-answer-table-candidates.json').read_text()):
 e=candidate['entity'];q=by[e];table=BeautifulSoup(candidate['table'],'html.parser').find('table')
 if table.get('aria-label')=='Answer matrix':checks.append({'question':e,'identity':candidate['identity'],'resolution':'Existing native matrix_answer table within matrix-answer-brackets; retain.'});continue
 ss=[s for s in sources if s['identity']==candidate['identity']and s['attribute']=='question/problem'and s.get('observed_controls')];assert ss,(e,'No original actual input table')
 s=ss[0];raw=BeautifulSoup(s['html'],'html.parser').find('table');assert raw is not None;rawrows=raw.find_all('tr');rendered=BeautifulSoup(s['observed_control_text'],'html.parser').find('table');assert rendered is not None;rows=rendered.find_all('tr');assert len(rows)==len(rawrows)==2
 first=rows[0].find_all('td',recursive=False);assert len(first)==4 and first[0].get('rowspan')=='2';label=first[0].get_text('',strip=True);m=re.fullmatch(r'\$([\s\S]*?)\$',label);assert m,label;expression=re.sub(r'=\s*(?:\\,\s*)*$','',m[1]).strip();data=[]
 for i,(row,rawrow)in enumerate(zip(rows,rawrows)):
  cells=row.find_all('td',recursive=False);rawcells=rawrow.find_all('td',recursive=False)
  if i==0:cells=cells[1:];rawcells=rawcells[1:]
  assert len(cells)==len(rawcells)==3
  assert not rawcells[0].get_text('',strip=True)and not rawcells[2].get_text('',strip=True)
  assert 'border-right:hidden'in rawcells[0].get('style','')and 'border-left:hidden'in rawcells[2].get('style','')
  assert rawcells[1].find(class_='freeResponseTextbox')is not None
  value=cells[1].get_text('',strip=True);assert re.fullmatch(r'\{\{[^{}]+\}\}',value);data.append([value])
 assert [v[0][2:-2]for v in data]==candidate['keys'];replacement=matrix_answer(expression,data);k=(e,'question/problem');p=pby.get(k)
 if p is None:p={'entity':e,'attribute':'question/problem','before':q[':question/problem'],'after':q[':question/problem'],'reason':'Restore original matrix bracket geometry and row-major input positions.','evidence':{'basis_t':9837,'identity':candidate['identity'],'source_path':s['path']},'confidence':'high'};props.append(p);pby[k]=p
 current_table=BeautifulSoup(p['after'],'html.parser').find('table');assert current_table is not None
 # Match the complete current HTML table span without changing other source formulas.
 pattern=r'<table\b[\s\S]*?</table>';matches=list(re.finditer(pattern,p['after']));assert len(matches)==1;match=matches[0];p['after']=p['after'][:match.start()]+replacement+p['after'][match.end():];validate_math_structure(p['after']);proof={'source_path':s['path'],'raw_source_table':str(raw),'observed_control_keys':candidate['keys'],'row_major_after':data,'source_label':expression,'current_and_after_field_ids':[f[':db/id']for f in q[':question/answer-fields']],'independent_check':'Original narrow border cells are matrix brackets, not data columns. Hidden cell borders and rowspan establish two entries in a single column. No numeric/given/answer value changed.','current_engine_after':'native matrix_answer uses external brackets, borderless entries, and exact original placeholder order.'};p['evidence']['matrix_table_restoration']=proof;checks.append({'question':e,'identity':candidate['identity'],'resolution':'Restore proven source bracket frame using native matrix_answer.','proof':proof})
(H/'source-reviewed-proposals.json').write_text(json.dumps(props,indent=2)+'\n');(H/'matrix-table-review.json').write_text(json.dumps(checks,indent=2)+'\n');print('response tables',len(checks),'source bracket repairs',sum('proof'in c for c in checks))

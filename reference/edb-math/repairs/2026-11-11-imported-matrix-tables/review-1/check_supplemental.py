#!/usr/bin/env python3
"""Cross-check source geometry and fresh field ownership for Newton supplements."""
import collections, json, re
from pathlib import Path
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
proposals=json.loads((HERE/'supplemental-proposals.json').read_text())
qs={q[':db/id']:q for q in json.loads((BASE/'capture/questions.json').read_text())}
qs.update({q[':db/id']:q for q in json.loads((BASE/'supplemental-capture/questions.json').read_text())})
sources={topic:BeautifulSoup(Path(f'/home/jake/Developer/MA/DATA/Lessons/{topic}/Source/{topic}.html').read_text(),'html.parser') for topic in [5377,5379]}
checks=[]
for p in proposals:
 q=qs[p['entity']];assert q[':question/problem']==p['before']
 expected=p['evidence']['matrix_rows'];replacement=p['replacements'][0]['after'];soup=BeautifulSoup(replacement,'html.parser')
 table=soup.find('table',attrs={'aria-label':'Answer matrix'})
 actual=[[c.get_text(strip=True) for c in row.find_all('td',recursive=False)] for row in table.find_all('tr')]
 expected_display=[[v if re.fullmatch(r'\{\{[^{}]+\}\}',v) else '$'+v+'$' for v in row] for row in expected]
 assert actual==expected_display and len(actual)==2 and all(len(row)==1 for row in actual)
 label=soup.find('span',class_='matrix-answer-label').get_text(strip=True)
 assert label=='$'+p['evidence']['equation_label']+'$'
 fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};mapping=[]
 for rownum,row in enumerate(expected,1):
  value=row[0];m=re.fullmatch(r'\{\{([^{}]+)\}\}',value)
  if not m:mapping.append({'row':rownum,'supplied_tex':value});continue
  field=fields[m[1]];correct=field[':answer-field/correct'];answers=field[':answer-field/choices']
  assert any(a[':db/id']==correct[':db/id'] and a[':answer/value']==correct[':answer/value'] for a in answers)
  mapping.append({'row':rownum,'field_key':m[1],'field_entity':field[':db/id'],
                  'correct_answer_entity':correct[':db/id'],'correct_value':correct[':answer/value'],
                  'correct_owned_by_same_field':True})
 topic=5377 if p['evidence']['source_topic_ids']==[17592186048637] else 5379
 source_q=sources[topic].find(id='question-'+q[':question/math-academy-id'].removeprefix('q-'))
 source_tables=source_q.find_all('table') if source_q else []
 # The source has a spanning left label and a spanning right bracket, with one
 # true component cell in each row. Current source may show a different family.
 exact=[]
 for source_table in source_tables:
  rows=[r for r in source_table.find_all('tr') if r.find_parent('table')==source_table]
  if len(rows)!=2:continue
  cells=[r.find_all(['td','th'],recursive=False) for r in rows]
  if [len(r) for r in cells]==[3,1] and cells[0][0].get('rowspan')=='2' and cells[0][2].get('rowspan')=='2':
   exact.append({'row_cell_counts':[3,1],'left_label_rowspan':2,'right_bracket_rowspan':2,
                 'cell_styles':[[c.get('style') for c in row] for row in cells]})
 checks.append({'entity':p['entity'],'imported_id':q[':question/math-academy-id'],'fresh_exact_before':True,
                'rendered_geometry':'2 rows × 1 column','label_preserved':True,'components':mapping,
                'source_exact_question_iterate_tables':exact,
                'source_evidence_scope':'exact current source geometry' if exact else 'stored shape plus exact same-family source rowspan pattern; no claim of exact current question match'})
summary={'questions':len(checks),'exact_current_source_geometry_count':sum(bool(c['source_exact_question_iterate_tables']) for c in checks),
         'fresh_capture_matches':len(checks),'marker_orphan_count':0,'missing_correct_ref_count':0,
         'supplied_components':sum('supplied_tex' in cell for c in checks for cell in c['components']),
         'marker_components':sum('field_key' in cell for c in checks for cell in c['components']),
         'label_operator_counts':dict(collections.Counter('approximate' if '≈' in p['evidence']['equation_label'] else 'equals' for p in proposals)),
         'checks':checks}
(HERE/'supplemental-cross-review.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='checks'},indent=2))

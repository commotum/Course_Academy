from pathlib import Path
import json,hashlib
from html.parser import HTMLParser
import jsonschema
E=Path(__file__).resolve().parent
load=lambda n:json.loads((E/n).read_text())
class Radios(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='input' and a.get('type')=='radio':self.ids.append(a['value'])
rows=[]
recs=load('render-more/input.json')
for i,r in enumerate(recs):
 f=r['question'][':question/answer-fields'][0]
 if i<7 or not f[':answer-field/type'].endswith('/radio'):continue
 p=Radios();p.feed((E/f'render-more/question-{i+1:03d}.html').read_text());cid=f[':answer-field/correct'][1]
 rows.append({'question_id':r['question'][':question/id'],'html':f'render-more/question-{i+1:03d}.html','actual_rendered_answer_ids':p.ids,'correct_zero_based_position':p.ids.index(cid)})
(E/'rendered-position-probe.json').write_text(json.dumps({'strategy':'choose first actual rendered radio option','correct':sum(r['correct_zero_based_position']==0 for r in rows),'total':len(rows),'baseline':0.2,'ordering':'ui/learning.js choiceOrder uses deterministic FNV-style sort seeded by itemId and field.id, so stored bank order is not displayed order. This probe uses saved actual UI DOM.','records':rows},indent=2)+'\n')
v=load('pedagogical-variation.json')
for p in v['shortcut_probes']:
 if p['cue']=='First displayed radio option':
  p['correct']=sum(r['correct_zero_based_position']==0 for r in rows)
  p['total']=len(rows)
  if 'rendered-position-probe.json' not in p['sample_refs']:p['sample_refs'].append('rendered-position-probe.json')
(E/'pedagogical-variation.json').write_text(json.dumps(v,indent=2)+'\n')
jsonschema.validate(v,json.loads(Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json').read_text()))
result=load('result.json');paths=[]
paths+=result['source_analysis']['evidence_paths']
for check in result['checks'].values():paths+=check['evidence_paths']
for key in ['coverage','counterfactuals','shortcut_probes']:
 for x in v[key]:paths+=x['sample_refs']
paths+=v['delivery']['sample_refs']
for n in paths:
 p=E/n;assert p.is_file() and p.stat().st_size>0,n;assert p.resolve().is_relative_to(E),n
assert len(result['checks'])==8 and result['checks']['decision_variation']['status']=='failed'
assert load('package-final.json')['unchanged']
assert load('render/rendering.json')['passed'] and load('render-more/rendering.json')['passed']
assert all(not r['errors'] for r in load('math-results.json')['results'])
checks={'variation_schema_valid':True,'nonempty_evidence_references':len(set(paths)),'eight_checks':True,'rendered_first_option_successes':sum(r['correct_zero_based_position']==0 for r in rows),'rendered_radio_records':len(rows),'package_unchanged':True,'result':'revise: demonstrated batch selection failure'}
(E/'evidence-contract.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))

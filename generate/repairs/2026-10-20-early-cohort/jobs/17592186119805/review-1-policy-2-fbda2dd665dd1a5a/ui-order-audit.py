"""Check real UI display ordering and simple visible-position strategies."""
import importlib.util,sys
sys.dont_write_bytecode=True
from pathlib import Path
s=importlib.util.spec_from_file_location('independent',Path(__file__).with_name('revision-audit.py'));a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
from html.parser import HTMLParser
class Radios(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='input' and d.get('type')=='radio':self.ids.append(d['value'])
def fnv(t):
 n=2166136261
 for c in t:n=((n^ord(c))*16777619)&0xffffffff
 return n
def ordered(r,item_id):
 f=r['question'][':question/answer-fields'][0]
 return sorted(a.choices(r['question']),key=lambda opt:fnv(f"{item_id}:{f[':answer-field/id']}:{opt[':answer/id']}"))
validated=[]
for prefix,filename in [('render','render-records.json'),('render-followup','render-followup-records.json')]:
 rs=a.load(a.ROOT/filename);report=a.load(a.ROOT/prefix/'rendering.json')
 for c in report['cases']:
  i=c['index'];r=rs[i];p=Radios();p.feed((a.ROOT/prefix/f'question-{i+1:03d}.html').read_text());expected=[x[':answer/id'] for x in ordered(r,i+1)];assert p.ids==expected,(prefix,i,p.ids,expected)
  validated.append({'file':f'{prefix}/question-{i+1:03d}.html','question_id':r['question'][':question/id'],'ordered_ids':p.ids,'correct_display_position':expected.index(r['question'][':question/answer-fields'][0][':answer-field/correct'][1]),'order_matches_real_UI':True})
measure=[]
for name in ['normal-records.json','runner-batch.json']:
 rs=a.load(a.ROOT/name)
 for item_id in [1,107,1007]:
  groups={'overall':rs}
  for r in rs:groups.setdefault(r['generation']['bank_profile'],[]).append(r)
  for group,sub in groups.items():
   for position in range(5):
    correct=sum(a.value(ordered(r,item_id)[position][':answer/value'])==a.verify(r) for r in sub)
    measure.append({'input':name,'task_item_id_assumption':item_id,'subgroup':group,'position':position,'correct':correct,'total':len(sub),'baseline':0.2})
a.save('ui-order-results.json',{'implementation':'ui/learning.js choiceOrder FNV1a seed itemId:field.id, checked against actual rendered radio input order','html_matches':validated,'position_probes':measure,'limitations':['Future task-item IDs are not captured. Three explicit item-ID scenarios are measured; real HTML validates all 29 previews. Value/rank/label probes do not depend on display shuffling.']})
print({'HTML_matches':len(validated),'position_probes':len(measure),'perfect_nontrivial_groups':[x for x in measure if x['correct']==x['total'] and x['total']>=5]})

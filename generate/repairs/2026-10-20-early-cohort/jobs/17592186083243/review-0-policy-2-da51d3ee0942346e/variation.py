from review import *
import collections
from html.parser import HTMLParser
class Radios(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='input' and a.get('type')=='radio':self.ids.append(a.get('value'))

def metrics(records):
 groups=collections.defaultdict(list)
 for r in records:
  f=r['question'][':question/answer-fields'][0]
  if not f[':answer-field/type'].endswith('/radio'): continue
  vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']];m=parse(key(r))
  data={'id':r['question'][':question/id'],'first_option':eq(vals[0],m),'zero':m==0,'smallest_nonzero_magnitude':eq(min((v for v in vals if v!=0),key=lambda v:abs(float(v))),m),'largest_magnitude':eq(max(vals,key=lambda v:abs(float(v))),m),'template':r['generation']['template'],'parameters':r['generation']['parameters'],'key':key(r)}
  groups[r['generation']['template']].append(data)
 return {k:{'total':len(v),'successes':{s:sum(x[s] for x in v) for s in ['first_option','zero','smallest_nonzero_magnitude','largest_magnitude']},'cases':v} for k,v in groups.items()}
rs=json.load(open('samples-independent.json'));batch=json.load(open('batch.json'));accepted=json.load(open('delivery-batch/accepted.json'));indaccepted=json.load(open('delivery-independent/accepted.json'))
report={'independent':metrics(rs),'batch':metrics(batch),'accepted_batch':metrics(accepted),'accepted_independent':metrics(indaccepted)}
# Actual UI order, not raw package order, for rendered batches and controlled pairs.
ui=[]
for dirname,filename in [('render','render-records.json'),('render-counterfactual','counterfactual-records.json')]:
 records=json.load(open(filename));n=len(json.load(open(dirname+'/rendering.json'))['cases'])
 for i,r in enumerate(records[:n]):
  f=r['question'][':question/answer-fields'][0]
  if not f[':answer-field/type'].endswith('/radio'):continue
  p=Radios();p.feed(Path(dirname+f'/question-{i+1:03}.html').read_text());ids=p.ids
  ui.append({'directory':dirname,'index':i,'question_id':r['question'][':question/id'],'choice_ids':ids,'correct_position':ids.index(f[':answer-field/correct'][1])+1 if f[':answer-field/correct'][1] in ids else None})
report['actual_ui_positions']=ui
save('shortcut-results.json',report)
print(json.dumps({k:{t:{a:b for a,b in data.items() if a!='cases'} for t,data in v.items()} for k,v in report.items() if k!='actual_ui_positions'},indent=2))
print('UI positions',[x['correct_position'] for x in ui])

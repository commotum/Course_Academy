from audit import *
from html.parser import HTMLParser
from collections import Counter
class Inputs(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='input' and d.get('type')=='radio' and 'data-answer-input' in d:self.ids.append(d['value'])
def h(s):
 n=2166136261
 for c in s:n=((n^ord(c))*16777619)&0xffffffff
 return n

def main():
 evidence=[];ps=json.load(open(OUT/'shortcut-results.json'))
 for directory,filename in [('render-all','render-records.json'),('render-delivered','delivery-batch/accepted.json')]:
  records=json.load(open(OUT/filename));positions={}
  for idx,r in enumerate(records):
   parser=Inputs();parser.feed((OUT/directory/f'question-{idx+1:03}.html').read_text());f=r['question'][':question/answer-fields'][0]
   ordered=sorted(f[':answer-field/choices'],key=lambda c:h(f"{idx+1}:{f[':answer-field/id']}:{c[':answer/id']}"))
   assert parser.ids==[c[':answer/id'] for c in ordered]
   pos=parser.ids.index(key(r['question']))+1
   evidence.append({'renderer':directory,'index':idx,'record_file':filename,'question_id':r['question'][':question/id'],'rendered_choice_ids':parser.ids,'correct_display_position':pos,'matched_actual_ui_hash_order':True})
   positions[idx]=pos
  for t in ['swap','scale']:
   sub=[idx for idx,r in enumerate(records) if r['generation']['template']==t]
   for pos in range(1,6):
    hits=sum(positions[idx]==pos for idx in sub)
    ps.append({'cue':'Actual UI position '+str(pos),'subgroup':directory+':'+t,'scope':'within_template','strategy':'Always select UI option '+str(pos)+' after learning.js choiceOrder','correct':hits,'total':len(sub),'baseline':.2,'disposition':'not_predictive','conclusion':'Uniform five-choice guessing baseline 0.2. Fixture content IDs and actual question-field IDs determine the visible ordering. No fixed UI position answers all tested questions in this template. Production task/item IDs are not yet allocated, so no exact future layout is claimed.','sample_refs':[filename,'ui-order-results.json']})
   assert max(Counter(positions[i] for i in sub).values())<len(sub),(directory,t,positions)
 save('ui-order-results.json',{'cases':evidence,'source':'ui/learning.js:choiceOrder lines 690-701; preview supplies contentId=index+1','scope':'Verified rendered DOM ordering, including all 5 normalized accepted batch records. Actual production item IDs are not supplied; the hash reorder does not fix a correct position across arbitrary item IDs.'})
 save('shortcut-results.json',ps)
 print('Actual rendered choice ordering verified',len(evidence),'delivered positions',[e['correct_display_position'] for e in evidence if e['renderer']=='render-delivered'])
if __name__=='__main__':main()

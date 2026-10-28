import copy,collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,validate_prose,validate_tex
D=json.loads((H/'current.json').read_text());objects={}
def index(x):
 if isinstance(x,dict):
  if ':db/id'in x:objects.setdefault(x[':db/id'],x)
  for v in x.values():index(v)
 elif isinstance(x,list):
  for v in x:index(v)
index(D);props={};merge=[]
def add(p):
 p=copy.deepcopy(p);p['attribute']=':'+p['attribute'].lstrip(':');k=p['entity'],p['attribute'];prior=props.get(k)
 if prior:
  old=prior['before'];current=prior['after'];after=p['after']
  if old is not None and isinstance(after,str)and old in after:after=after.replace(old,current)
  elif after!=current:merge.append({'entity':k[0],'attribute':k[1],'resolution':'Later authored standalone task/solution takes precedence over source-only annotation reconstruction. Both evidence records retained.','earlier':prior['reason'],'later':p['reason']})
  p['before']=old;p['after']=after;p['evidence']={'combined':[prior['evidence'],p['evidence']]};p['reason']=prior['reason']+' '+p['reason']
 props[k]=p
for file in['source-formula-proposals.json','answer-format-proposals.json','context-proposals.json','completion-solution-proposals.json','extra-context-proposals.json']:
 for p in json.loads((H/file).read_text()):add(p)
topics={t['entity']:t['ma_id']for t in D['topics']};tq={q:topics[t]for t,k,q in D['links']};display=[]
for q in D['questions']:
 if tq[q[':db/id']]not in[285,308,1112,3769]:continue
 k=q[':db/id'],':question/problem';before=props[k]['after']if k in props else q[':question/problem'];changes=[]
 for m in MATH.finditer(before):
  if m[0].startswith(('$$',r'\[',r'\('))or r'\int'not in m[0]:continue
  if re.match(r'\s*(?:Given|Let)\b',before)and not re.search(r'calculate|evaluate|find|complete|what is',before,re.I):continue
  changes.append((m.start(),m.end(),'\n\n$$\n'+m[0][1:-1].strip()+'\n$$\n\n'))
 if not changes:continue
 after=before
 for a,b,v in reversed(changes):after=after[:a]+v+after[b:]
 after=re.sub(r'\n{3,}','\n\n',after).strip();p=dict(entity=q[':db/id'],attribute=':question/problem',before=before,after=after,reason='Show standalone integral calculations in display math, preserving mathematical expressions and blank fragments.',evidence={'basis_t':9122,'identity':q.get(':question/math-academy-id'),'review':'Each promoted formula is an integral calculation in the task problem, not a solution reference, assumption or answer bank.'},confidence='high');display.append(p)
 if k in props:
  props[k]['after']=after;props[k]['reason']+=' '+p['reason'];props[k]['evidence']={'combined':[props[k]['evidence'],p['evidence']]}
 else:add(p)
out=list(props.values());validation=[]
for p in out:
 assert objects[p['entity']].get(p['attribute'])==p['before'],(p['entity'],p['attribute'])
 try:(validate_tex if p['attribute']==':answer/value'and objects[p['entity']].get(':answer/type',{}).get(':db/ident')==':answer.type/math'else validate_prose)(p['after'])
 except Exception as ex:validation.append({'entity':p['entity'],'attribute':p['attribute'],'error':str(ex)})
proposed=copy.deepcopy(D)
def patch(x):
 if isinstance(x,dict):
  e=x.get(':db/id')
  for(eid,a),p in props.items():
   if e==eid:x[a]=p['after']
  for v in x.values():patch(v)
 elif isinstance(x,list):
  for v in x:patch(v)
patch(proposed)
keys=json.loads((H/'key-proposals.json').read_text());ans={a[':db/id']:a for q in proposed['questions']for f in q.get(':question/answer-fields',[])for a in f.get(':answer-field/choices',[])}
for q in proposed['questions']:
 for f in q.get(':question/answer-fields',[]):
  ps=[p for p in keys if p['entity']==f[':db/id']]
  if ps:f[':answer-field/correct']=copy.deepcopy(ans[ps[0]['after']])
(H/'proposals.json').write_text(json.dumps(out,indent=2));(H/'proposed.json').write_text(json.dumps(proposed,indent=2));(H/'display-proposals.json').write_text(json.dumps(display,indent=2));(H/'merge-review.json').write_text(json.dumps(merge,indent=2));(H/'proposed-structure-validation.json').write_text(json.dumps(validation,indent=2));print('content',len(out),collections.Counter(p['attribute']for p in out),'display',len(display),'merges',len(merge),'errors',validation)
# Separate explicit ownership/history-preserving duplicate detach recommendation.
dups=[]
for qid,stale in[(17592186115783,17592186113665),(17592186115785,17592186113667),(17592186125222,17592186123932),(17592186125224,17592186123944)]:
 q=objects[qid];old=[f[':db/id']for f in q[':question/answer-fields']];dups.append(dict(entity=qid,attribute=':question/answer-fields',before=old,after=[f for f in old if f!=stale],reason='Detach stale duplicate-key membership, retaining all question/field/answer entities and history. Current renderer otherwise overwrites one field. Independently solved old radio keys staged separately so archived old banks become valid.',evidence={'basis_t':9122,'incoming':'history-refs.json','stale_field':stale,'proof':'Only incoming reference at captured basis is question membership; no task response references. Replacement field bank/canonical independently verified.'},confidence='high'))
(H/'duplicate-membership-proposals.json').write_text(json.dumps(dups,indent=2))

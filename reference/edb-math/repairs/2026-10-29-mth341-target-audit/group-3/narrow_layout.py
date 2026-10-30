import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());ps=json.loads((H/'proposals.json').read_text());changes={(p['entity'],p['attribute']):p for p in ps};evidence=[];pat=re.compile(r'\$\$([\s\S]*?)\$\$|(?<!\$)\$([^$]*?)\$(?!\$)')
def wrap(v):
 if r'\begin'in v:return v
 m=re.search(r'([ABC]\s*=\s*)\\\{(.*):(.*)\\\}',v,re.S)
 if not m:return v
 replacement=r'\begin{gathered}'+m[1]+r'\left\{\begin{gathered}'+m[2]+r':\\'+m[3]+r'\end{gathered}\right\}\end{gathered}'
 return v[:m.start()]+replacement+v[m.end():]
def add(eid,attr,before,cur):
 if before==cur and (eid,attr)not in changes:return
 if(eid,attr)in changes:changes[eid,attr]['after']=cur;changes[eid,attr]['reason']+=' Preserve source content while wrapping complete set/line formulas at mathematical boundaries so they remain visible at320px.'
 else:changes[eid,attr]={'entity':eid,'attribute':attr,'before':before,'after':cur,'reason':'Preserve complete source content while wrapping long mathematical formulas at their logical boundaries for320px player presentation.'}
 evidence.append({'entity':eid,'attribute':attr,'source_math_values_and_symbols_preserved':True,'purpose':'avoid demonstrated320px clipping'})
for q in S['questions']:
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/ident']!=':answer-field.type/checkbox' or not f[':answer-field/key'].startswith('$'):continue
  before=f[':answer-field/key'];cur=changes.get((f[':db/id'],'answer-field/key'),{}).get('after',before);after='$'+wrap(cur[1:-1])+'$'
  if cur!=after:add(f[':db/id'],'answer-field/key',before,after)
 if q[':db/id']in[17592186192505,17592186193313,17592186193318,17592186479092,17592186596006]:
  before=q[':question/problem'];cur=changes.get((q[':db/id'],'question/problem'),{}).get('after',before);after=cur
  for m in list(pat.finditer(cur))[::-1]:
   body=m[1]if m[1]is not None else m[2];v=wrap(body)
   if v!=body:after=after[:m.start()]+('$$'+v+'$$'if m[1]is not None else'$'+v+'$')+after[m.end():]
  if q[':db/id']==17592186192505:after=re.sub(r'B\s*=\s*\\left',lambda m:r'B=\\\left',after)
  if cur!=after:add(q[':db/id'],'question/problem',before,after)
 if q[':db/id']==17592186119648:
  before=q[':question/problem'];cur=changes.get((q[':db/id'],'question/problem'),{}).get('after',before);after=cur
  for m in list(pat.finditer(cur))[::-1]:
   body=m[1]if m[1]is not None else m[2]
   if r'\mathbf{r}='in body:
    split=re.search(r'\+\s*([st])',body)
    if split:v=r'\begin{aligned}'+body[:split.start()].replace('=','&=',1)+r'\\&+'+body[split.start()+1:]+r'\end{aligned}';after=after[:m.start()]+'\n\n$$\n'+v+'\n$$\n\n'+after[m.end():]
  if cur!=after:add(q[':db/id'],'question/problem',before,after)
(H/'proposals.json').write_text(json.dumps(list(changes.values()),indent=2)+'\n');(H/'narrow-layout-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('Wrapped',len(evidence),'clipping-prone source formulas; total proposals',len(changes))

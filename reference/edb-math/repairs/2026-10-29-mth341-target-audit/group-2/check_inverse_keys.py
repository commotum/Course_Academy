import json,re,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from algebra import matrices,scalar,symbols
from check_algebra import expr
# Load helpers without rerunning the family audit.
import ast
code=ast.parse((H/'family_audit.py').read_text());exec(compile(ast.Module(body=[n for n in code.body if isinstance(n,ast.FunctionDef)and n.name in['normalized_ops','operation']],type_ignores=[]),'family_helpers','exec'))
from question_capture.math_format import MATH
S=json.loads((H/'proposed-snapshot.json').read_text());topics={q:t for t,k,q in S['links']};checks=[];review=[]
def ops(t):
 out=[]
 for v in ([m[0]for m in MATH.finditer(t)]or[t]):
  edge=2 if v.startswith('$$')else 1 if v.startswith('$')else 0;v=v[edge:-edge]if edge else v;v=re.sub(r'(?:\\[,;! ]|[?,.])+$','',v)
  for p in re.split(r'\band\b|,\s*\\,|,|\\qquad\s*,?',v):
   if re.search(r'R.*?(?::=|↔|\\leftrightarrow)',p):out.append(p.rstrip('?,.'))
 return out
for q in S['questions']:
 if topics[q[':db/id']]not in[17592186048920,17592186050900]:continue
 prompt=q[':question/problem'];fs=q.get(':question/answer-fields',[]);ms=matrices(prompt);pp=ops(prompt);r={'question':q[':db/id'],'choice_checks':[]}
 for f in fs:
  typ=f[':answer-field/type'][':db/ident'];right=f[':answer-field/correct'][':db/id'];good=[];reason=None
  if typ==':answer-field.type/blank':continue
  if 'transformed into the'in prompt:
   if typ==':answer-field.type/checkbox':a=matrices(f[':answer-field/key'])[0]['matrix'];candidate=[(None,a)]
   else:candidate=list(zip('ABC', [m['matrix']for m in ms]))
   selected=[]
   for label,a in candidate:
    b=a
    for op in pp:
     b,_=operation(op,b);assert b is not None,(q[':db/id'],op)
    if b==sp.eye(a.rows):selected.append(label)
   for c in f[':answer-field/choices']:
    ok=(c[':answer/value']==str(bool(selected)).lower())if typ==':answer-field.type/checkbox'else set(re.findall(r'\b[A-C]\b',c[':answer/value']))==set(selected)
    if ok:good.append(c[':db/id'])
   reason='Apply each specified operation in order to every candidate; compare with I.'
  elif 'Find the row operation'in prompt:
   a=ms[0]['matrix']
   for c in f[':answer-field/choices']:
    b=a;oo=ops(c[':answer/value'])
    for op in oo:
     b,_=operation(op,b)
     if b is None:break
    if oo and b==sp.eye(a.rows):good.append(c[':db/id'])
   reason='Apply every offered operation sequence to the supplied matrix and test I.'
  elif ms and ('inverse'in prompt.lower()):
   a=ms[0]['matrix'];a=a[:,:a.rows]if a.cols==2*a.rows else a;inv=a.inv()
   subs=re.findall(r'\{?b\}?_\{(\d)(\d)\}',prompt)
   if subs:
    expected=sum(inv[int(i)-1,int(j)-1]for i,j in subs)
    for c in f[':answer-field/choices']:
     if scalar(c[':answer/value'])==expected:good.append(c[':db/id'])
    reason='Compute A^-1 exactly and the requested sum of indexed inverse entries.'
   elif any(matrices(c[':answer/value'])for c in f[':answer-field/choices']):
    for c in f[':answer-field/choices']:
     v=re.sub(r'^.*?=','',c[':answer/value'],count=1)
     try:
      if expr(v)==inv:good.append(c[':db/id'])
     except Exception:pass
    reason='Compute A^-1 exactly, including external scalar factors.'
   elif a.cols==a.rows or 'corresponding row operations'in prompt.lower()or'row operations corresponding'in prompt.lower():
    # Each listed sequence must reproduce the successive displayed matrices.
    targets=[(u['matrix'],v['matrix'])for u,v in zip(ms,ms[1:])if operation(prompt[u['end']:v['start']],u['matrix'])[0]is None]
    for c in f[':answer-field/choices']:
     oo=ops(c[':answer/value']);valid=len(oo)==len(targets)
     for op,(before,after)in zip(oo,targets):
      b,_=operation(op,before)
      if b is None or b!=after:valid=False;break
     if valid:good.append(c[':db/id'])
    reason='Compare every offered row-operation sequence with each required intermediate.'
  if reason:
   ok=good==[right];r['choice_checks'].append({'field':f[':db/id'],'method':reason,'matching_owned_choices':good,'correct':right,'ok':ok})
   if not ok:review.append(r['choice_checks'][-1]|{'question':q[':db/id']})
  else:review.append({'question':q[':db/id'],'field':f[':db/id'],'reason':'Need explicit operation-choice review'})
 checks.append(r)
(H/'inverse-key-verification.json').write_text(json.dumps({'passed':not review,'checks':checks,'review':review},default=str,indent=2)+'\n');print('Questions',len(checks),'key checks',sum(len(r['choice_checks'])for r in checks),'review',len(review));print(review)

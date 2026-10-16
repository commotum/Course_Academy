"""Solve the 18 questions independently; propose no database mutations."""
import collections,json,re,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'))
from math_format import ENV,MATH,environment,cells
from edn import loads
TRANS=standard_transformations+(implicit_multiplication_application,)
SYMS={n:sp.Symbol(n) for n in ['x','y','z','x1','x2','x3']+[f'{a}{i}' for a in 'RC' for i in range(1,5)]}
def seed(text):
 # Some old imported math strings are uniformly double-escaped.
 if r'\\begin' in text and not re.search(r'(?<!\\)\\begin',text):text=text.replace('\\\\','\\')
 return text

def clean(text):
 text=seed(text).replace('$','').replace('−','-').strip().rstrip('.')
 text=re.sub(r'\\(?:left|right)\b','',text)
 text=re.sub(r'\\+(?:,|;|quad\b|qquad\b)','',text)
 text=re.sub(r'\{?([RCxyz])\}?_\{?(\d)\}?',r'\1\2',text)
 text=re.sub(r'\\color\{[^}]*\}','',text)
 while re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',text):text=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',text)
 return text.replace('{','(').replace('}',')').strip().rstrip(',')
def expr(t):return sp.expand(parse_expr(clean(t),local_dict=SYMS,transformations=TRANS))
def matrices(text):
 text=seed(text);out=[]
 for t in ENV.finditer(text):
  if t[1]!='begin' or t[2] not in ['array','bmatrix']:continue
  span=environment(text,t.start());body=text[span[0]:span[1]]
  if t[2]=='array':body=re.sub(r'^\s*\{[^{}]*\}','',body)
  out.append(sp.Matrix([[expr(v) for v in row] for row in cells(body)]))
 return out

def ops(text):
 pieces=[m[0] for m in MATH.finditer(text)] if '$' in text else [text];out=[]
 for p in pieces:
  t=clean(p).replace(' ','')
  swap=re.fullmatch(r'([RC])(\d)(?:↔|\\leftrightarrow)(?:[RC])(\d)',t)
  if swap:out.append(('swap',swap[1],int(swap[2])-1,int(swap[3])-1));continue
  m=re.fullmatch(r'([RC])(\d):?=(.+)',t)
  if not m or '…' in t or 'ldots' in t:continue
  
  try:e=expr(m[3])
  except Exception as err:raise ValueError({'original':p,'cleaned':t,'expression':m[3]}) from err
  axis=m[1];coeffs=[e.coeff(SYMS[axis+str(i)]) for i in range(1,5)]
  assert e==sum(c*SYMS[axis+str(i+1)] for i,c in enumerate(coeffs)),t
  out.append(('linear',axis,int(m[2])-1,coeffs))
 return out

def apply(mat,operations):
 mat=mat.copy()
 for kind,axis,i,data in operations:
  if kind=='swap':
   if axis=='R':mat.row_swap(i,data)
   else:mat.col_swap(i,data)
   continue
  if axis=='R':mat[i,:]=sum((c*mat.row(j) for j,c in enumerate(data[:mat.rows])),sp.zeros(1,mat.cols))
  else:mat[:,i]=sum((c*mat.col(j) for j,c in enumerate(data[:mat.cols])),sp.zeros(mat.rows,1))
 return mat

def ref(mat):
 piv=[next((j for j,v in enumerate(mat.row(i)) if v),None) for i in range(mat.rows)];p=[v for v in piv if v is not None]
 return piv==p+[None]*(len(piv)-len(p)) and all(a<b for a,b in zip(p,p[1:]))

def signature(a):
 mm=matrices(a[':answer/value'])
 if mm:return ('matrices',tuple(tuple(map(str,m)) for m in mm))
 oo=ops(a[':answer/value'])
 return ('ops',repr(oo)) if oo else ('text',re.sub(r'\s+','',a[':answer/value']))

report=[]
for q in json.loads((H/'questions.json').read_text()):
 eid=q[':db/id'];mid=q[':question/math-academy-id'];prompt=q[':question/problem'];ms=matrices(prompt);fields=q[':question/answer-fields'];formula=[];matches=[]
 if mid in ['q-42362','q-42363']:
  rows=[int(n)-1 for n in re.findall(r'\$(\d)\$(?:st|nd|rd|th)',prompt.split('rows')[0])]
  answer=sum(next(v for v in ms[0].row(i) if v) for i in rows);formula=[f'Leading entries in rows {[r+1 for r in rows]} sum to {answer}']
  predicate=lambda a:expr(a[':answer/value'])==answer
 elif mid in ['q-42026','q-42369']:
  bad=[chr(65+i) for i,m in enumerate(ms) if not ref(m)];formula=['Non-echelon matrices: '+', '.join(bad)]
  predicate=lambda a:re.findall(r'\$([ABC])\$',a[':answer/value'])==bad
 elif mid in ['q-10202','q-20451']:
  if mid=='q-10202':mat=ms[0];answer=mat[:,:-1].inv()*mat[:,-1]
  else:
   body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',prompt,re.S)[1];eqs=[expr(l)-expr(r) for l,r in [row.replace('&','').split('=') for row in body.split(r'\\')]]
   A,b=sp.linear_eq_to_matrix(eqs,[SYMS['x1'],SYMS['x2'],SYMS['x3']]);answer=A.inv()*b
  formula=['Solution column: '+str(list(answer))];predicate=lambda a:matrices(a[':answer/value'])==[answer]
 elif mid in ['q-10321','q-1076']:
  m=ms[0];answer=m[:,:-1].inv()*m[:,-1];formula=['System solution '+str(list(answer))+'; compare complete matrix/solution choices']
  def predicate(a):
   candidates=matrices(a[':answer/value'])
   if len(candidates)!=1 or not ref(candidates[0]) or candidates[0].rref()[0]!=m.rref()[0]:return False
   if mid=='q-1076':
    scalars={m[1]:expr(m[2]) for m in re.finditer(r'\$\s*([xy])\s*=([^$]+)\$',a[':answer/value'])}
    return scalars==dict(zip(['x','y'],answer))
   return True
 elif mid in ['q-20240','q-20389','q-20392']:
  formula=['Apply every offered row operation to the entire matrix; '+('test the new (2,1) entry is zero' if mid=='q-20392' else 'compare all resulting entries with the target matrix')]
  def predicate(a):
   oo=ops(a[':answer/value']);assert oo,a
   out=apply(ms[0],oo);return out[1,0]==0 if mid=='q-20392' else out==ms[1]
 elif mid in ['q-10252','q-10248']:
  given=ops(prompt);assert len(given)==1;answer=apply(ms[0],given);formula=['Computed row-operation result: '+str(answer.tolist())];predicate=lambda a:matrices(a[':answer/value'])==[answer]
 else:
  given=ops(prompt);formula=['Compare every target matrix entry after applying the stated operation and both offered missing operations.','Fixed operations: '+repr(given)]
  def predicate(a):
   oo=ops(a[':answer/value']);assert len(oo)==2,(mid,a,oo)
   return apply(ms[0],given+oo)==ms[1]
 for f in fields:
  valid=[a for a in f[':answer-field/choices'] if predicate(a)]
  correct=f.get(':answer-field/correct')
  if correct:assert len(valid)==1 and valid[0][':db/id']==correct[':db/id'],(mid,'existing key does not match',valid,correct)
  matches.append({'field':f[':db/id'],'key_present':bool(correct),'matching_options':[{'answer':a[':db/id'],'value':a[':answer/value']} for a in valid],'unique':len(valid)==1})
 entry={'question':eid,'ma_id':mid,'difficulty':q.get(':question/difficulty',{}).get(':db/ident'),'kp':q[':knowledge-point/_questions'][0][':knowledge-point/title'],'worked_solution_present':bool(q.get(':question/worked-solution')),'derivation':formula,'fields':matches}
 if len(fields)==2:
  entry['banks_mathematically_equal']=collections.Counter(map(signature,fields[0][':answer-field/choices']))==collections.Counter(map(signature,fields[1][':answer-field/choices']))
 report.append(entry)
# Inspect every existing solution matrix stage, not just the final key.
for q,entry in zip(json.loads((H/'questions.json').read_text()),report):
 if not q.get(':question/worked-solution'):continue
 sol=q[':question/worked-solution'];stages=matrices(sol);findings=[]
 if entry['ma_id']=='q-10248':
  expected=apply(matrices(q[':question/problem'])[0],ops(q[':question/problem']))
  assert stages[0]==matrices(q[':question/problem'])[0] and stages[-1]==expected
  if stages[1]!=expected:
   findings.append({'kind':'incorrect intermediate matrix','stage':2,'displayed_first_row':list(map(str,stages[1].row(0))),'required_first_row':list(map(str,expected.row(0))),'explanation':'R3:=R3+3R1 changes only row 3; row 1 was wrongly negated in the intermediate display. Final matrix and answer key are correct.'})
 else:
  printed=[]
  for body in re.findall(r'\\begin\{aligned\}((?:\{?[RC]\}?_\{[1-4]\}).*?)\\end\{aligned\}',sol,re.S):
   printed+=ops('$'+body.replace('&','')+'$')
  assert len(stages)==len(printed)+1,(entry['ma_id'],len(stages),printed)
  for i,op in enumerate(printed):
   assert apply(stages[i],[op])==stages[i+1],(entry['ma_id'],'Incorrect printed stage',i)
 entry['existing_solution_matrix_stages_checked']=len(stages)
 entry['existing_solution_findings']=findings
(H/'answer-analysis.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print(json.dumps({'questions':len(report),'unique_correct_in_all_fields':sum(all(f['unique'] for f in r['fields']) for r in report),'existing_keyed_questions_verified':sum(any(f['key_present'] for f in r['fields']) for r in report),'ambiguous':[r['ma_id'] for r in report if not all(f['unique'] for f in r['fields'])],'same_banks':[r['ma_id'] for r in report if r.get('banks_mathematically_equal')]}))

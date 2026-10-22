"""Independent visible-content oracle, source replay, decision probes, native inputs.

Run with --accepted FILE to audit the actual delivery survivor batch.
"""
import argparse, collections, importlib.util, json, re, sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('imt',ROOT/'17592186124511.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
OUT=ROOT/'evidence'
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
LABELS=('I','II','III')
def save(name,data):(OUT/name).write_text(json.dumps(data,indent=2)+'\n')
def plain(text):
 text=text.replace(r'\text','').replace(r'\textrm','').replace(r'\ne','!=').replace(r'\mathbb','').replace('**','')
 return re.sub(r'[\s${}\\]','',text)
def correct(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def visible(q):
 prompt=q[':question/problem'];n=int(re.search(r'(\d+)\s*\\times\s*(\d+)',prompt)[1])
 numbered=re.findall(r'(?:^|\n)(III|II|I)\. ([^\n]+)',prompt)
 head=prompt.split('\n\nI.')[0];m=MATRIX.findall(head);basis=None
 if m:
  expr=[sp.sympify(re.sub(r'(\d)(x)',r'\1*\2',re.sub(r'\{x\}_\{([12])\}',r'x\1',r.strip()))) for r in m[0].split(r'\\')]
  assert len(expr)==n
  xs=sorted(set().union(*(x.free_symbols for x in expr)),key=str)
  if xs:
   basis=sp.Matrix([[v.coeff(x) for x in xs] for v in expr]);k=basis.rank();assert k==len(xs)
   assert all(v==sum(basis[i,j]*x for j,x in enumerate(xs)) for i,v in enumerate(expr))
   ranks=[n-k];kind='nullspace'
  else:
   v=sp.Matrix(expr);assert any(v);kind='vector';ranks=[0,n-1]
   # Independent matrix witnesses for underdetermination: zero and projection off span(v).
   witness=sp.eye(n)-v*v.T/(v.T*v)[0];assert witness*v==sp.zeros(n,1) and witness.rank()==n-1
 elif (d:=re.search(r'det\(A\)=(-?\d+)',head)):
  kind='det';ranks=[n] if int(d[1]) else list(range(n))
 elif re.search(r'\\text\{rank\}\(A\)='+str(n),head):kind='rank';ranks=[n]
 else:
  assert 'Col' in head and re.search(r'R\}\^\{'+str(n)+r'\}',head);kind='col';ranks=[n]
 if numbered:assert [x[0] for x in numbered]==list(LABELS);claims=[x[1] for x in numbered]
 else:claims=[f[':answer-field/key'] for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above']
 assert len(claims)==3
 def eval_at(c,r):
  s=plain(c);inv=r==n;k=n-r
  if s=='Aisinvertible':return inv
  if s=='Aisnotinvertible':return not inv
  if 'pivotcolumns' in s:
   j=int(re.search(r'(\d+)pivotcolumns',s)[1]);return (r!=j) if 'doesnothave' in s else (r==j)
  m=re.fullmatch(r'(Null|Col)\(A\)(=|!=)(.*)',s)
  if m:
   obj,op,rhs=m.groups()
   eq=(k==0 if obj=='Null' else r==0) if rhs=='0' else (r==n if obj=='Col' and rhs=='R^'+str(n) else None)
   assert eq is not None,(s,n)
   return eq if op=='=' else not eq
  m=re.fullmatch(r'(rank|dim\(Null|dim\(Col|nullity)\(A\)\)?(=|!=|<)(\d+)',s);assert m,s
  obj,op,value=m.groups();actual=r if obj in ('rank','dim(Col') else k;value=int(value)
  return {'=':actual==value,'!=':actual!=value,'<':actual<value}[op]
 mask=[]
 for c in claims:
  possible={eval_at(c,r) for r in ranks};assert len(possible)==1,('undetermined claim',c,ranks)
  mask.append(possible.pop())
 return kind,n,claims,mask,basis

def inspect(rec):
 q=rec['question'];kind,n,claims,mask,basis=visible(q);fields=q[':question/answer-fields'];sol=q[':question/worked-solution'];replay=rec['generation']['replay']
 if fields[0][':answer-field/type'].endswith('/radio'):
  target=' and '.join(k for k,b in zip(LABELS,mask) if b)+' only'
  assert correct(fields[0])==target
  position=next(i for i,a in enumerate(fields[0][':answer-field/choices']) if a[':answer/id']==fields[0][':answer-field/correct'][1])
 else:
  assert any(correct(f)=='true' for f in fields)
  expected={c:str(b).lower() for c,b in zip(claims,mask)}
  for f in fields:assert correct(f)==(str(not any(mask)).lower() if f[':answer-field/key']=='None of the above' else expected[f[':answer-field/key']])
  position=None
 if not replay:
  if not fields[0][':answer-field/type'].endswith('/radio'):
   truth_by_claim={c.strip('$'):b for c,b in zip(claims,mask)}
   claims=[c for c,b in re.findall(r'- Statement \$(.*?)\$ is (true|false)\.',sol)]
   mask=[truth_by_claim[c] for c in claims]
  if fields[0][':answer-field/type'].endswith('/radio'):
   judgments=re.findall(r'- Statement (III|II|I) is (true|false): \$(.*?)\$\.',sol)
   assert judgments==[(label,str(b).lower(),c.strip('$')) for label,b,c in zip(LABELS,mask,claims)]
  else:
   judgments=re.findall(r'- Statement \$(.*?)\$ is (true|false)\.',sol)
   assert dict(judgments)=={c.strip('$'):str(b).lower() for c,b in zip(claims,mask)}
  if basis is not None:
   cols=[sp.Matrix([int(x.strip()) for x in v.split(r'\\')]) for v in MATRIX.findall(sol)]
   assert sp.Matrix.hstack(*cols)==basis
  if not fields[0][':answer-field/type'].endswith('/radio'):
   conclusion=sol.split('Therefore, the correct answer is ')[1]
   for c,b in zip(claims,mask):
    if b:assert '$'+c+'$' in conclusion
   if not any(mask):assert 'None of the above' in conclusion
  # The theorem's dimension and evidence match the visible given.
  assert r'\text{rank}(A)&='+str(n) in sol
  if kind=='det':assert re.search(r'det\(A\)=(-?\d+)',q[':question/problem'])[0] in sol
 assert str(q[':question/id']) and len({a[':answer/id'] for f in fields for a in f[':answer-field/choices']})==sum(len(f[':answer-field/choices']) for f in fields)
 return tuple(mask),position

def native(rec,label):
 return {'label':label,'record':rec,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently verified complete bank'} for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]}

def summarize(records,require=False):
 groups=collections.defaultdict(list)
 for rec in records:
  mask,pos=inspect(rec);p=rec['generation']['parameters'];t=rec['generation']['template'];groups[t].append((mask,pos))
  if 'det' in p:groups[t+':det-'+('nonzero' if p['det'] else 'zero')].append((mask,pos))
 result={}
 for t,rows in groups.items():
  masks=collections.Counter(''.join(str(int(x)) for x in m) for m,p in rows);positions=collections.Counter(str(p) for m,p in rows if p is not None)
  result[t]={'count':len(rows),'truth_masks':dict(masks),'radio_positions':dict(positions),'best_constant_subset_successes':max(masks.values()),'trials':len(rows),'best_fixed_position_successes':max(positions.values(),default=None),'uniform_position_baseline':0.2 if positions else None}
  if require:
   assert len(masks)>1,('fixed subset',t)
   for i in range(3):assert {m[i] for m,p in rows}=={True,False},('fixed statement truth',t,i)
   if positions:
    assert len(positions)>1,('fixed position',t,positions)
    if ':det-' not in t:assert set(positions)==set(map(str,range(5))),('positions missing',t,positions)
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--accepted',type=Path);args=ap.parse_args()
 if args.accepted:
  records=json.loads(args.accepted.read_text());save('delivery-variation.json',{'passed':True,'coverage':summarize(records,True),'semantic_instances':len({g.fingerprint(r['question']) for r in records})});print('Accepted batch independent content and shortcut checks passed:',len(records));return
 replays=[];replay_report=[]
 for t in g.TEMPLATES:
  r=g.generate(template=t,replay=True);inspect(r);src=g.SOURCES[t];q=r['question']
  assert q[':question/problem']==src[':question/problem'] and q[':question/worked-solution']==src[':question/worked-solution']
  for a,b in zip(src[':question/answer-fields'],q[':question/answer-fields']):
   assert a[':answer-field/key']==b[':answer-field/key']
   expected=[('II only' if t=='q-142367' and v[':answer/value']=='lI only' else v[':answer/value']) for v in a[':answer-field/choices']]
   assert expected==[v[':answer/value'] for v in b[':answer-field/choices']]
   assert a[':answer-field/correct'][':answer/value']==correct(b)
  replays.append(r);replay_report.append({'source':t,'complete_bank':True,'choice_count':sum(len(f[':answer-field/choices']) for f in q[':question/answer-fields']),'exact_prompt_and_solution':True})
 records=[]
 # Small targeted sample retained per profile until decisions, positions and determinant subgroups occur.
 for t in g.TEMPLATES:
  rows=[]
  for seed in range(120):
   r=g.generate(template=t,seed=seed);inspect(r);rows.append(r)
   if len(rows)<12:continue
   try:
    summarize(rows,True)
    source=g.SOURCES[t];none=any(f[':answer-field/key']=='None of the above' for f in source[':question/answer-fields'])
    observed={inspect(x)[0] for x in rows}
    expected={tuple(bool(bits&(1<<j)) for j in range(3)) for bits in range(0 if none else 1,8)}
    if source[':question/answer-fields'][0][':answer-field/type'][':db/ident'].endswith('/radio'):
     values=[('II only' if t=='q-142367' and a[':answer/value']=='lI only' else a[':answer/value']) for a in source[':question/answer-fields'][0][':answer-field/choices']]
     expected={tuple(label in value.split(' only')[0].split(' and ') for label in LABELS) for value in values}
    assert observed==expected
    if 'det' in r['generation']['parameters']:assert {bool(x['generation']['parameters']['det']) for x in rows}=={True,False}
    break
   except AssertionError:pass
  else:raise AssertionError(('coverage failed',t,len(rows)))
  records+=rows
 # Relevant evidence counterfactual: determinant changes, identical claims and dimension.
 t='q-141200';p={'n':6,'det':1,'claims':[r'A\text{ is invertible}',r'\text{Null}(A)=\{0\}',r'\text{dim(Null}(A))\ne 0']}
 a=g.generate(template=t,parameters=p);p['det']=0;b=g.generate(template=t,parameters=p)
 assert inspect(a)[0]==(True,True,False) and inspect(b)[0]==(False,False,True)
 # Same givens, changed claim polarity: a different decision and worked judgment.
 p['claims'][0]=r'A\text{ is not invertible}';c=g.generate(template=t,parameters=p);assert inspect(c)[0]==(True,False,True)
 # Irrelevant magnitude/sign and vector scaling preserve the decision.
 p=a['generation']['parameters'].copy();p['det']=-4;d=g.generate(template=t,parameters=p);assert inspect(a)[0]==inspect(d)[0];assert g.fingerprint(a['question'])==g.fingerprint(d['question'])
 e=g.generate(template='q-34929',seed=4);p=json.loads(json.dumps(e['generation']['parameters']));p['matrix']=[[-v for v in row] for row in p['matrix']];f=g.generate(template='q-34929',parameters=p);assert inspect(e)[0]==inspect(f)[0];assert g.fingerprint(e['question'])==g.fingerprint(f['question'])
 counter=[a,b,c,d,e,f]
 for level in ('easy','hard'):
  try:g.batch(level,5,0)
  except ValueError:pass
  else:raise AssertionError(level)
 # Explicit empty selection without source None must fail, not be silently rewritten.
 p={'n':6,'det':1,'claims':[r'A\text{ is not invertible}',r'\text{Null}(A)\ne \{0\}',r'\text{dim(Null}(A))\ne 0']}
 try:g.generate(template='q-141200',parameters=p)
 except ValueError:pass
 else:raise AssertionError('empty selectable subset accepted')
 assert g.batch('moderate',5,99)==g.batch('moderate',5,99)
 report={'passed':True,'source_profiles':replay_report,'replay_choice_count':sum(r['choice_count'] for r in replay_report),'sample_count':len(records),'semantic_instances':len({g.fingerprint(r['question']) for r in records}),'coverage':summarize(records,True),'controlled_pairs':['determinant zero/nonzero with claims fixed','claim polarity with givens fixed','irrelevant determinant sign/magnitude','irrelevant vector scaling'],'excluded_sources':g.EXCLUDED}
 save('source-replays.json',replays);save('content-validation.json',report);save('probe-records.json',records);save('counterfactual-records.json',counter)
 save('native-input.json',[native(r,'replay-'+r['generation']['template']) for r in replays]+[native(r,'sample-'+str(i)) for i,r in enumerate(records)]+[native(r,'counterfactual-'+str(i)) for i,r in enumerate(counter)])
 save('render-records.json',[replays[0],records[0],a,b,next(r for r in records if r['generation']['template']=='q-141196'),next(r for r in records if r['generation']['template']=='q-34834' and not any(inspect(r)[0]))])
 print('Passed:',len(replays),'source banks;',len(records),'targeted samples; 4 controlled pairs. Native and render inputs saved.')
if __name__=='__main__':main()

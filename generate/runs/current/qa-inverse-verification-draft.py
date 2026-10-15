"""Root reads actual supplied matrices, ordered product cells, witnesses and selection predicates."""
import re,json,hashlib,sys,importlib.util,copy
from pathlib import Path
from fractions import Fraction as F
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2];D=ROOT/'generate/scratch/17592186087699-draft'
z=importlib.util.spec_from_file_location('root_inverse_gen',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
from scripts.question_capture.math_format import normalize_prose
count=dict(records=0,supplied_cells=0,operand_cells=0,concrete_product_cells=0,nonidentity_witnesses=0,statements=0,choices=0,prose_truths=0,source_values=0,source_keys=0,source_solutions=0)
def scalar(t):
 t=t.strip();t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'\1/\2',t);return F(t.replace(' ',''))
def matrix(t):
 rr=[[None if c.strip()=='∗' else scalar(c) for c in row.split('&')] for row in t.split(r'\\')];assert len(rr)==2 and [len(r) for r in rr]==[2,2];return rr
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
I=[[F(1),F(0)],[F(0),F(1)]]
def check(record):
 q=record['question'];pr=q[':question/problem'];named={m[1]:matrix(m[2]) for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',pr,re.S)};assert len(named) in (2,3)
 statements=re.findall(r'(?<!\$)\$(?!\$)([^$]+)(?<!\$)\$(?!\$)',pr)[-3:];truth=[]
 if len(named)==3:
  for raw in statements:
   t=raw.replace(' ','').replace('{','').replace('}','');m=re.fullmatch(r'([A-Z])([A-Z])=([A-Z])([A-Z])=I_2',t)
   if m:
    a,b,c,d=m.groups();assert (a,b)==(d,c);truth.append(mul(named[a],named[b])==I and mul(named[c],named[d])==I)
   else:
    m=re.fullmatch(r'([A-Z])(=|\\ne)([A-Z])\^-1',t);assert m,t;a,op,b=m.groups();eq=mul(named[a],named[b])==I and mul(named[b],named[a])==I;truth.append(eq if op=='=' else not eq)
  count['statements']+=3
 sol=q.get(':question/worked-solution','');blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 for block in blocks:
  pair=re.match(r'\s*([A-Z])([A-Z])',block);assert pair,block
  objects=[matrix(m) for m in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',block,re.S)];assert len(objects)==3
  a,b,shown=objects;assert a==named[pair[1]] and b==named[pair[2]];actual=mul(a,b);showncells=[]
  for i in range(2):
   for j in range(2):
    if shown[i][j] is not None:assert shown[i][j]==actual[i][j];showncells.append((i,j));count['concrete_product_cells']+=1
  if len(showncells)==1:
   i,j=showncells[0];assert actual[i][j]!=I[i][j] and re.search(r'\\n(?:eq|e)\s*\{?I\}?_\{?2\}?',block);count['nonidentity_witnesses']+=1
  else:
   assert len(showncells)==4 and shown==actual
   if actual!=I:assert record['generation']['template']=='q-7908' or re.search(r'\\n(?:eq|e)\s*\{?I\}?_\{?2\}?',block),block
  count['operand_cells']+=8
 for roman,word in re.findall(r'[Ss]tatement (I|II|III) is (true|false)',sol):assert truth[('I','II','III').index(roman)]==(word=='true');count['prose_truths']+=1
 for f in q.get(':question/answer-fields',[]):
  values=f[':answer-field/choices'];correct=f.get(':answer-field/correct');got=None if correct is None else next(a[':answer/value'] for a in values if a[':answer/id']==correct[1])
  if f[':answer-field/type'].endswith('/checkbox'):
   assert sorted(a[':answer/value'] for a in values)==['false','true'];assert got==str(truth[('I','II','III').index(f[':answer-field/key'])]).lower()
  else:
   banks=[frozenset(re.findall(r'(?<!I)(?:III|II|I)(?!I)',a[':answer/value'])) for a in values];want=frozenset(v for v,b in zip(('I','II','III'),truth) if b);assert len(banks)==len(set(banks))==5 and banks.count(want)==1
   if got is not None:assert frozenset(re.findall(r'(?<!I)(?:III|II|I)(?!I)',got))==want
  count['choices']+=len(values)
 if blocks and truth:
  ending=sol.rsplit('Therefore,',1)[-1];assert set(re.findall(r'(?<!I)(?:III|II|I)(?!I)',ending))=={v for v,b in zip(('I','II','III'),truth) if b},ending
 count['supplied_cells']+=4*len(named);count['records']+=1
sources=json.loads((D/'source-cases.json').read_text())
for c in sources:
 sid=c['source_id'];r=g.generate('easy',template=sid,profile='raw-source',parameters=g.original_parameters(sid));q=r['question'];o=c['record'];assert q[':question/problem']==normalize_prose(o[':question/problem'])
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==normalize_prose(o[':question/worked-solution']);count['source_solutions']+=1
 for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
  assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);count['source_values']+=len(of[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];count['source_keys']+=1
 check(r)
for item in json.loads((D/'review.json').read_text()):check(item['record'])
for level in ('easy','moderate','hard'):
 for sid in g.DEFAULT_TEMPLATES:
  r=g.generate(level,seed=927,template=sid);check(r)
  ms=[v for m in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',r['question'][':question/problem'],re.S) for row in matrix(m) for v in row]
  if level=='easy':assert all(v.denominator<=3 for v in ms)
  elif level=='moderate':assert sum(v.denominator==4 for v in ms)>=2 and all(v.denominator==1 for v in ms[:4])
  else:assert sum(v.denominator>1 for v in ms[:4])>=2 and sum(v.denominator>1 for v in ms)>=5
saved=dict(count);bad=copy.deepcopy(g.generate('easy',seed=37,template='q-11640'));sol=bad['question'][':question/worked-solution'];m=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',sol,re.S);assert m;bad['question'][':question/worked-solution']=sol[:m.start(1)]+'99 & 0 \\\\ 0 & 99'+sol[m.end(1):]
try:check(bad)
except AssertionError:pass
else:raise AssertionError('wrong initial matrix operand with unchanged finalkey escaped')
count=saved;out=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),independent_readback=count,unchanged_finalkey_controls=1,scope='direct2x2 product verification, all levels same supplied-object method; no determinant/adjugate/row-reduction. Moderate/hard arithmetic domains authored and uncalibrated',limits='Source masks retain relation roles; zero source q7908 key denominator; canonical remains separate incomplete raw evidence.')
(R/'qa/17592186087699-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

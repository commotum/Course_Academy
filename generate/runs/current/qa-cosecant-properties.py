"""Root derives statement truth from printed claims, independently of masks."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186176053
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','csc_p');H=load(R/'qa-sinusoidal-properties.py','csc_source');g=load(ROOT/f'generate/scratch/{K}.py','csc_g');n=s.Symbol('n',integer=True);p.locals_['t']=n
p.functions['csc']=s.Function('UnevaluatedCosecant')
def read(v):return p.scalar(re.sub(r'(?<![A-Za-z])n(?![A-Za-z])','t',v.strip().strip('$').rstrip('.,')))
def claims(prompt):
 out=re.findall(r'^\s*(?:[IVX]+\.|[123]\.|-)\s+(.*)$',prompt,re.M);assert len(out)==3,(prompt,out);return out
def truth(z):
 if 'not on the graph' in z or 'is on the graph' in z:
  pair=re.search(r'\$\((.*?),(.*?)\)\$',z);assert pair;angle=read(pair[1]);ordinate=read(pair[2]);sine=s.simplify(s.sin(angle));actual=sine!=0 and s.simplify(1/sine-ordinate)==0
  return not actual if 'not on' in z else actual
 if 'vertical asymptote' in z:
  expr=read(re.search(r'\$x\s*=\s*(.*?)\$',z)[1]);return (s.simplify(expr/s.pi)).is_integer is True
 if 'takes the value' in z:
  m=re.search(r'value \$(.*?)\$ at \$x\s*=\s*(.*?)\$',z);assert m,z;value=read(m[1]);angle=read(m[2]);sin=s.simplify(s.sin(angle));return sin!=0 and s.simplify(1/sin-value)==0
 if 'in the domain' in z:
  angle=read(re.search(r'\$x\s*=\s*(.*?)\$',z)[1]);return s.simplify(s.sin(angle))!=0
 if 'in the range' in z:
  val=read(re.search(r'\$y\s*=\s*(.*?)\$',z)[1]);return abs(val)>=1
 if 'domain' in z:return 'except' in z and ('integer multiples' in z or 'nπ' in z)
 if 'range' in z:return 'cup' in z and '-1]' in z and '[1,' in z
 if 'minimum' in z or 'maximum' in z:return 'no global' in z
 if 'zero' in z:return 'no zero' in z
 if 'intersect' in z:return "doesn't intersect" in z or 'does not intersect' in z
 if '=' in z and ('csc' in z or 'operatorname{csc}' in z):
  expr=z.strip().strip('$').rstrip('.');a,b=map(read,expr.split('='));assert a.func==b.func==p.functions['csc'];delta=s.simplify((a.args[0]-b.args[0])/(2*s.pi));return delta.is_integer is True
 raise AssertionError(('Unrecognized printed statement',z))
def bits(value):
 if value in ('None','None of the listed'):return 0
 tokens=re.findall(r'\b(?:III|II|I)\b',value);assert tokens;return sum({'I':1,'II':2,'III':4}[x] for x in tokens)
source=H.source(g,K);sources=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];source_math=[]
for q in sources:
 vals=list(map(truth,claims(q[':question/problem'])));mask=sum(1<<i for i,v in enumerate(vals) if v);key=q[':question/answer-fields'][0].get(':answer-field/correct');assert key is None or bits(key[':answer/value'])==mask;source_math.append(dict(source_id=q[':question/math-academy-id'],truths=list(map(bool,vals)),supplied_key=key is not None))
records=json.loads((R/f'qa/{K}-sampled.json').read_text())+[g.generate('moderate',seed=51+i,template=t) for i,t in enumerate(g.SOURCES)]
count=0;choices=0
for rec in records:
 q=rec['question'];vals=list(map(truth,claims(q[':question/problem'])));mask=sum(1<<i for i,v in enumerate(vals) if v);f=q[':question/answer-fields'][0];bank=[bits(v[':answer/value']) for v in f[':answer-field/choices']];assert len(set(bank))==5 and mask in bank
 for v in f[':answer-field/choices']:assert (bits(v[':answer/value'])==mask)==(v[':answer/id']==f[':answer-field/correct'][1]);choices+=1
 if rec['generation']['template'] not in g.SOURCES:assert set(bank)=={mask^e for e in [0,1,2,4,7]}
 sol=q[':question/worked-solution']
 for i,want in enumerate(vals):
  label=['I','II','III'][i]
  m=re.search(r'(?:the )?statement '+label+r' is (true|false)',sol,re.I)
  if m:assert (m[1]=='true')==want
  else:assert i in (0,1) and 'statements I and II are both false' in sol and not want
  count+=1
 # Actual hard value/domain prose is independently read from its printed objects.
 if rec['generation']['template']=='indexed_properties':
  m=re.search(r'cosecant takes the value \$(.*?)\$ at \$x=(.*?)\$',sol);assert m and s.simplify(read(m[1])-1/s.sin(read(m[2])))==0
  claim=claims(q[':question/problem'])[2];angle=read(re.search(r'\$x=(.*?)\$',claim)[1]);prose=re.search(r'The number \$(.*?)\$ is (not )?an integer multiple',sol);assert prose and read(prose[1])==angle and bool(prose[2])==(not (angle/s.pi).is_integer)
report=dict(status='passed',kp_id=K,source=source,source_truth_readback=source_math,normal_records=len(records),independent_statement_truths=count,full_choice_subsets=choices,fixed_graphs='Four original untransformed graphs inspected individually at full resolution; no changed geometry is needed.',script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='source_truth_readback'}))

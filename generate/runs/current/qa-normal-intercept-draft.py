"""Root actual normal-line/intercept process, source banks and changed targets."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186092385;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_ni_gen',D.with_suffix('.py'));P=load('root_ni_math',R/'direct-derivative-readback.py');x,y=P.x,P.P.y
POSITIVE=False
N=dict(records=0,points=0,derivative_operands=0,derivative_targets=0,derivative_rows=0,slope_rows=0,normal_rows=0,line_rows=0,intercept_rows=0,conclusions=0,values=0,pairs=0,banks=0,blanks=0,axes=0,domains=0)
def clean(text):
 text=P.clean(text)
 while r'\sqrt[' in text:
  m=re.search(r'\\sqrt\[(\d+)\]',text);assert m;arg,end=P.group(text,m.end());text=text[:m.start()]+'('+arg+r')^{\frac{1}{'+m[1]+'}}'+text[end:]
 return text
def scalar(text):
 value=P.scalar(clean(text))
 if POSITIVE:
  xp=s.Symbol('root_positive_x',positive=True)
  value=s.powdenest(value.subs(x,xp),force=True).subs(xp,x)
 return value
def eq(a,b):
 if P.eq(a,b):return True
 if POSITIVE:
  xp=s.Symbol('root_positive_x',positive=True);return s.simplify((a-b).subs(x,xp))==0
 return False
def point(text):
 z=clean(text).replace(r'\,','').strip().strip('()');parts=z.split(',');assert len(parts)==2;return tuple(scalar(z) for z in parts)
def value(raw,fun,at,m):
 raw=clean(raw);raw=re.sub(r'\{m\}', 'm',raw)
 for arg in re.findall(r"\{?f\}?(?:\^\{\x27\}|\x27)\((.*?)\)",raw):
  target=scalar(arg);assert target==x or eq(target,at),(target,at);N['derivative_targets']+=1
 for operator in P.DERS:
  while operator in raw:
   start=raw.index(operator);pos=start+len(operator)
   while raw[pos].isspace():pos+=1
   arg,end=P.group(raw,pos);f=scalar(arg);raw=raw[:start]+'('+s.latex(s.diff(f,x),root_notation=False)+')'+raw[end:];N['derivative_operands']+=1
 def formal(matched):
  target=scalar(matched[1]) if matched[1] is not None else x
  return '('+s.latex(s.diff(fun,x).subs(x,target),root_notation=False)+')'
 raw=re.sub(r"\{?f\}?(?:\^\{\x27\}|\x27)(?:\((.*?)\))?",formal,raw)
 raw=re.sub(r"m(?:\^\{\x27\}|\x27)",lambda _: '('+s.latex(-1/m)+')',raw);raw=re.sub(r'\bm\b',lambda _: '('+s.latex(m)+')',raw)
 return scalar(raw)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));fidelity=dict(prompts=0,solutions=0,values=0,refs=0,missing_refs=0)
for tid,o in G.ROWS.items():
 if ':question/math-academy-id' not in o:continue
 raw=G.source_replay(tid);assert raw['question']==o and raw['generation']['evidence_only'];fidelity['prompts']+=1;fidelity['solutions']+=(':question/worked-solution' in o)
 for f in o.get(':question/answer-fields',[]):fidelity['values']+=len(f.get(':answer-field/choices',[]));fidelity['refs']+=(':answer-field/correct' in f);fidelity['missing_refs']+=(':answer-field/correct' not in f)
def check(r):
 global POSITIVE
 q,meta=r['question'],r['generation'];tid=meta['template'];prompt=q[':question/problem'];p=meta['parameters'];POSITIVE=(meta.get('domain')=='x>0' or tid in ('q-11124','q-104073','q-104075','q-342222','hard-canonical'))
 match=re.search(r'\$(?:f\(x\)|y)\s*=\s*(.*?)\$',prompt);assert match;fun=scalar(match[1]);match=re.search(r'point \$(.*?)\$',prompt);assert match;at,y0=point(match[1]);assert eq(fun.subs(x,at),y0);N['points']+=1
 axis=re.search(r'intersects the \$([xy])\$-axis',prompt);assert axis;axis=axis[1];N['axes']+=1
 df=s.diff(fun,x);m=s.simplify(df.subs(x,at));assert m.is_finite and m!=0;n=-1/m;b=s.simplify(y0-n*at);line=n*x+b;answer=s.simplify(-b/n) if axis=='x' else b;correctpoint=(answer,s.Integer(0)) if axis=='x' else (s.Integer(0),answer)
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==5,(tid,len(blocks))
 first=clean(blocks[0]);operator=next(v for v in P.DERS if v in first);pos=first.index(operator)+len(operator)
 while first[pos].isspace():pos+=1
 operand,_=P.group(first,pos);assert eq(scalar(operand),fun)
 for i,block in enumerate(blocks):
  block=re.sub(r'\\(?:begin|end)\{aligned\}','',block);carry=None
  for row in block.split(r'\\'):
   parts=row.replace('&','').split('=');assert len(parts)>=2
   if parts[0].strip():carry=parts[0]
   else:assert carry is not None;parts[0]=carry
   vals=[value(z,fun,at,m) for z in parts]
   if i<3:assert all(eq(z,(df,m,n)[i]) for z in vals),(tid,i,row,vals)
   elif i==3:vals=[z.subs(y,line) for z in vals];assert all(eq(z,vals[0]) for z in vals),(tid,row,vals)
   else:vals=[z.subs({x:answer,y:0} if axis=='x' else {x:0,y:answer}) for z in vals];assert all(eq(z,vals[0]) for z in vals),(tid,row,vals)
   N[('derivative_rows','slope_rows','normal_rows','line_rows','intercept_rows')[i]]+=len(vals)
 for actualaxis in re.findall(r'(?:intersects|intersection with) the \$([xy])\$-axis',sol):assert actualaxis==axis
 conclusion=re.search(r'intersects the\s+\$[xy]\$-axis at\s*(?:\$\s*)?(\(.*?\))',sol);assert conclusion,sol;assert all(eq(z,w) for z,w in zip(point(conclusion[1]),correctpoint));N['conclusions']+=1
 fs=q[':question/answer-fields'];isradio=fs[0][':answer-field/type'].endswith('/radio')
 if isradio:
  assert len(fs)==1;f=fs[0];vals=[point(z[':answer/value']) for z in f[':answer-field/choices']];ispoint=lambda a,b:all(eq(z,w) for z,w in zip(a,b))
  assert sum(ispoint(z,correctpoint) for z in vals)==1 and ispoint(next(z for z,v in zip(vals,f[':answer-field/choices']) if v[':answer/id']==f[':answer-field/correct'][1]),correctpoint)
  for a,c in itertools.combinations(vals,2):assert not ispoint(a,c);N['pairs']+=1
  if meta['profile'] in ('source_bank','observed_served'):
   if tid=='q-10871':expected=[-at,at,m,answer,answer/m]
   elif tid=='q-11124':expected=[1/m,y0,y0+1/(2*m),1/(2*m),answer]
   elif tid=='q-104073':expected=[-answer,answer,-at,y0-at,-(y0-at)]
   elif tid=='q-104075':expected=[m,1/answer,1/m,at,answer]
   else:raise AssertionError(tid)
  else:
   intercept=lambda rate,ordinate,abscissa:s.simplify(abscissa-ordinate/rate) if axis=='x' else s.simplify(ordinate-rate*abscissa)
   expected=[answer,intercept(m,y0,at),intercept(1/m,y0,at),intercept(n,y0,0),intercept(n,0,at)]
  expectedpoints=[(z,0) if axis=='x' else (0,z) for z in expected];assert len(vals)==len(expectedpoints) and all(sum(ispoint(z,w) for z in vals)==1 for w in expectedpoints),(tid,vals,expectedpoints);N['banks']+=1;N['values']+=len(vals)
 else:
  assert len(fs)==2 and {f[':answer-field/key'] for f in fs}=={'field-1','field-2'}
  for f in fs:
   wanted=correctpoint[0 if f[':answer-field/key']=='field-1' else 1];assert len(f[':answer-field/choices'])==1;v=f[':answer-field/choices'][0];assert eq(scalar(v[':answer/value']),wanted) and f[':answer-field/correct']==[':answer/id',v[':answer/id']];assert '{{'+f[':answer-field/key']+'}}' in prompt;N['blanks']+=1;N['values']+=1
 if POSITIVE:assert at>0
 if tid=='q-308823':assert at!=0
 N['domains']+=1;N['records']+=1
if __name__=='__main__':
 for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
 for level,ts in G.NORMAL_TEMPLATES.items():
  for tid in ts:
   ps=[{'scale':scale,'point':pt,'axis':axis} for scale in (1,8) for pt in G.points(tid) for axis in ('x','y')]
   for p in ps:
    for ft in ('blank','radio'):
     try:r=G.generate(level,template=tid,parameters=p,field_type=ft)
     except ValueError:continue
     check(r)
 for tid in ('q-10871','q-11124','q-104073','q-104075'):
  for scale in (1,8):
   try:r=G.generate(G.SPECS[tid][3],template=tid,parameters={'scale':scale,'point':G.SPECS[tid][1],'axis':G.SPECS[tid][2]},profile='source_bank')
   except ValueError:continue
   check(r)
 for tid in G.ROWS:
  if tid.startswith('nonMA-') or tid in ('q-10878','q-71542'):continue
  check(G.source_replay(tid,'observed_served'))
 result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

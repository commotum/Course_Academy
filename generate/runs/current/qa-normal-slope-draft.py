"""Root normal slope: actual curve points, formal derivatives, all stages/banks."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186092384;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
POSITIVE=False
def eq(a,b):
 if P.eq(a,b):return True
 if POSITIVE:
  xp=s.Symbol('root_x_positive',positive=True);return s.simplify((a-b).subs(x,xp))==0
 return False
G=load('root_normal_gen',D.with_suffix('.py'));P=load('root_normal_math',R/'direct-derivative-readback.py');x=P.x
N=dict(records=0,curve_points=0,bindings=0,formal_operands=0,formal_targets=0,derivative_equalities=0,slope_equalities=0,normal_equalities=0,values=0,pairs=0,banks=0,blanks=0,domains=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));originals={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fidelity=dict(prompts=0,solutions=0,values=0,refs=0,missing_refs=0,unrated=0)
for tid,o in originals.items():
 raw=G.generate('easy',template=tid,parameters={'scale':1} if tid in G.SPECS else {},profile='raw');assert raw['question']==o and raw['generation']['evidence_only'];fidelity['prompts']+=1;fidelity['solutions']+=(':question/worked-solution' in o);fidelity['unrated']+=(':question/difficulty' not in o)
 for f in o.get(':question/answer-fields',[]):fidelity['values']+=len(f.get(':answer-field/choices',[]));fidelity['refs']+=(':answer-field/correct' in f);fidelity['missing_refs']+=(':answer-field/correct' not in f)
def coord(text):
 m=re.search(r'point \$\((.*?)\)(?:[.:]?)\$',text);assert m,text;parts=m[1].split(',');assert len(parts)==2;return tuple(P.scalar(z) for z in parts)
def value(raw,fun,at,m):
 raw=P.clean(raw);raw=re.sub(r'\{m\}', 'm',raw)
 for arg in re.findall(r"\{?f\}?(?:\^\{\x27\}|\x27)\((.*?)\)",raw):
  target=P.scalar(arg);assert target==x or eq(target,at),(arg,at);N['formal_targets']+=1
 for der in P.DERS:
  start=0
  while der in raw[start:]:
   pos=raw.index(der,start)+len(der)
   while raw[pos].isspace():pos+=1
   arg,end=P.group(raw,pos);assert eq(P.scalar(arg),fun);N['formal_operands']+=1;start=end
 raw=re.sub(r"m(?:\^\{\x27\}|\x27)",lambda _: '('+s.latex(-1/m)+')',raw)
 raw=re.sub(r'\bm\b',lambda _: '('+s.latex(m)+')',raw)
 return P.value(raw,fun,'f',dict(formal_derivative_inputs=0))
def check(r):
 global POSITIVE
 q,meta=r['question'],r['generation'];POSITIVE=meta['domain']=='x>0';tid=meta['template'];prompt=q[':question/problem'];fun=P.given(prompt)[0];at,y0=coord(prompt);assert eq(fun.subs(x,at),y0);N['curve_points']+=1;df=s.diff(fun,x);m=s.simplify(df.subs(x,at));assert m.is_finite and m!=0;normal=-1/m
 sol=q[':question/worked-solution'];binding=re.search(r'\$f\(x\)=(.*?)\$',sol);assert binding and eq(P.scalar(binding[1]),fun);N['bindings']+=1
 for pt in re.findall(r'point \$(.*?)\$',sol):
  z=pt.rstrip(':').strip();assert z[0]=='(' and z[-1]==')';a,b=map(P.scalar,z[1:-1].split(','));assert eq(a,at) and eq(b,y0);N['curve_points']+=1
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==3
 for i,block in enumerate(blocks):
  block=re.sub(r'\\(?:begin|end)\{aligned\}','',block);wanted=(df,m,normal)[i]
  for row in block.split(r'\\'):
   pieces=[z for z in row.replace('&','').split('=') if z.strip()];assert pieces and all(eq(value(z,fun,at,m),wanted) for z in pieces),(tid,row,wanted);N[('derivative_equalities','slope_equalities','normal_equalities')[i]]+=len(pieces)
 field=q[':question/answer-fields'][0];vals=[P.scalar(z[':answer/value']) for z in field[':answer-field/choices']];scale=meta['parameters'].get('scale',1)
 if tid=='q-103531':expected=[m,-s.Rational(5,2)*scale,2/(s.Integer(5)*scale),normal,-2/(s.Integer(5)*scale)]
 elif tid=='q-103532':expected=[-s.Integer(1),1/m,-m,m,normal]
 elif tid=='q-103543':expected=[s.Integer(1),1/m,normal,m,-m]
 elif tid=='q-47449':expected=[1/m,-s.Integer(1),1/(s.Integer(2)*scale),-1/(s.Integer(2)*scale),normal]
 elif tid=='q-71524':expected=[normal,s.Rational(4,5),m,-2*scale,1/m]
 else:expected=[normal]
 assert len(vals)==len(expected) and all(sum(eq(v,e) for v in vals)==1 for e in expected),(tid,vals,expected)
 assert sum(eq(v,normal) for v in vals)==1 and eq(next(v for v,z in zip(vals,field[':answer-field/choices']) if z[':answer/id']==field[':answer-field/correct'][1]),normal)
 for a,b in itertools.combinations(vals,2):assert not eq(a,b);N['pairs']+=1
 if field[':answer-field/type'].endswith('/blank'):assert '{{'+field[':answer-field/key']+'}}' in prompt and len(vals)==1;N['blanks']+=1
 domain=meta['domain'];assert domain==('x>0' if tid in ('q-342153','q-103531','q-103532') else 'x!=0' if tid in ('q-342152','q-103543') else 'real x')
 if domain=='x>0':assert at>0
 if domain=='x!=0':assert at!=0
 N['values']+=len(vals);N['banks']+=1;N['domains']+=1;N['records']+=1
for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
for tid in list(G.SPECS)+list(G.AUTHORED):
 ps=G.parameters_for(tid);l='easy' if tid in G.SPECS else G.AUTHORED[tid][0]
 for p in (ps[0],ps[len(ps)//2],ps[-1]):
  try:r=G.generate(l,template=tid,parameters=p)
  except ValueError:continue
  check(r)
 if tid in G.SPECS:check(G.generate('easy',template=tid,parameters={'scale':1}))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

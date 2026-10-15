"""Root log-chain review from actual prompts, composite bindings and all stages."""
import sys,json,hashlib,importlib.util,re,copy
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186092265;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_general_log_gen',D.with_suffix('.py'));H=load('root_general_log_scalar',R/'log-chain-scalar-readback.py');x,u=H.x,H.u;W=s.Symbol('root_log_positive_w',positive=True)
def clean(t):return t.replace(r'\left.','').replace(r'\mathrm{d}',r'\text{d}').replace(r'\left','').replace(r'\right','').replace(r'\big','').replace(r'\,','').replace(r'\cancel','').strip().rstrip('.,')
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fid=dict(records=0,banks=0,values=0,keys=0,solutions=0,fieldless=0,incomplete_fields=0)
for sid,o in olds.items():
 q=G.raw_replay(sid)['question'];assert q==o;fid['records']+=1;fid['solutions']+=':question/worked-solution'in o
 if not o.get(':question/answer-fields'):fid['fieldless']+=1
 for f in o.get(':question/answer-fields',[]):
  if not f.get(':answer-field/choices'):fid['incomplete_fields']+=1;continue
  fid['banks']+=1;fid['values']+=len(f[':answer-field/choices']);fid['keys']+=':answer-field/correct'in f
N=dict(records=0,bindings=0,partial_derivatives=0,chain_stages=0,points=0,canceled_factors=0,values=0,pairs=0);tasks={l:set()for l in G.SUPPORTED_LEVELS};semantic=dict(banks=0,values=0,keys=0)

def check(r,anchor=False):
 q,m=r['question'],r['generation'];sid=m['template'];prompt=q[':question/problem'];given=re.search(r'\$(?:f\(x\)|y)=(.*?)\$',prompt);assert given;F=H.scalar(given[1]);df=s.diff(F,x);point=re.search(r'where \$x=(.*?)\$',prompt);at=H.scalar(point[1])if point else None
 if at is not None:assert F.subs(x,at).is_finite;N['points']+=1
 bb=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(bb)==(4 if at is not None else 3)
 composite=clean(bb[0]);left,inner=re.split(r',?\\quad\s*u=',composite);U=H.scalar(inner);outerparts=left.split('=');assert re.fullmatch(r'(?:f\(x\)|y)',outerparts[0]);outers=[H.scalar(z)for z in outerparts[1:]];assert outers
 # Radical instances use their actual connected real branch, without force.
 coord=None
 if any(p.exp==s.Rational(1,2)and p.base.has(x)for p in U.atoms(s.Pow)):
  squared=s.expand(U**2);a=s.diff(squared,x);assert a!=0 and not a.has(x)and squared.subs(x,0)==0;coord=W if a>0 else -W
 def eq(a,b):return H.eq(a.subs(x,coord)if coord is not None else a,b.subs(x,coord)if coord is not None else b)
 assert all(eq(o.subs(u,U),F)for o in outers);outer=outers[-1];N['bindings']+=1
 partial=clean(bb[1]);parts=re.split(r',?\\quad',partial);assert len(parts)==2;seen=set()
 DER=r'\\frac\{\\text\{d\}([fyu])\}\{\\text\{d\}([xu])\}'
 expected_map={('f','u'):s.diff(outer,u),('y','u'):s.diff(outer,u),('u','x'):s.diff(U,x),('f','x'):df,('y','x'):df}
 for part in parts:
  sides=part.rstrip('.,').split('=');leftop=re.fullmatch(DER,sides[0].strip());assert leftop,(sid,repr(part),repr(sides[0]));key=(leftop[1],leftop[2]);assert key in expected_map;seen.add(key)
  for raw in sides[1:]:assert eq(H.scalar(raw),expected_map[key]),('actual partial derivative',sid,raw,key);N['partial_derivatives']+=1
 assert ('u','x')in seen and (('f','u')in seen or('y','u')in seen)
 def value(raw):
  t=clean(raw);evalpoint=None
  match=re.search(r'(?:\{\|\}|\|)_\{',t)
  if match:
   arg,end=H.group(t,match.end()-1);assert arg.startswith('x=')and at is not None;evalpoint=H.scalar(arg[2:]);assert eq(evalpoint,at);t=t[:match.start()]+t[end:]
  replacements={}
  def formal(mm):
   key=(mm[1],mm[2]);assert key in expected_map;token=('i','j','k')[len(replacements)];replacements[H.P.locals_[token]]=expected_map[key];return '('+token+')'
  t=re.sub(DER,formal,t);result=H.scalar(t).subs(replacements).subs(u,U);return result.subs(x,evalpoint)if evalpoint is not None else result
 for bi,b in enumerate(bb[2:]):
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',b);rows=[row.split('&',1)[1].strip().removeprefix('=').strip()for row in text.split(r'\\')if row.strip()];want=df if bi==0 else df.subs(x,at)
  if bi==0:
   first=clean(rows[0]);assert re.fullmatch(DER+r'\\cdot '+DER,first),('ordered formal chain factors',sid,first)
  for raw in rows:assert eq(value(raw),want),('actual chain/evaluation stage',sid,raw,value(raw),want);N['chain_stages']+=1
  for cc in re.finditer(r'\\cancel\{',b):
   factor,end=H.group(b,cc.end()-1);v=H.scalar(factor);assert v!=0;N['canceled_factors']+=1
 f=q[':question/answer-fields'][0];vals=[H.scalar(a[':answer/value'])for a in f[':answer-field/choices']];want=df if at is None else df.subs(x,at);assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if eq(v,want)]==[f[':answer-field/correct'][1]]
 for i,v in enumerate(vals):
  for vv in vals[:i]:assert not eq(v,vv);N['pairs']+=1
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in prompt
 if anchor:
  for of in olds[sid].get(':question/answer-fields',[]):
   if not of.get(':answer-field/choices'):continue
   original=[H.scalar(a[':answer/value'])for a in of[':answer-field/choices']];assert len(original)==len(vals)and all(sum(eq(v,w)for w in vals)==1 for v in original)and all(sum(eq(w,v)for v in original)==1 for w in vals);semantic['banks']+=1;semantic['values']+=len(vals)
   if ':answer-field/correct'in of:assert eq(H.scalar(of[':answer-field/correct'][':answer/value']),next(v for a,v in zip(f[':answer-field/choices'],vals)if a[':answer/id']==f[':answer-field/correct'][1]));semantic['keys']+=1
 N['records']+=1;N['values']+=len(vals);tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(F),str(at)))
for sid in G.TEMPLATES:check(G.generate(G.SPECS[sid][1],template=sid,parameters=G.original(sid)),True)
for level in G.SUPPORTED_LEVELS:
 for seed in range(60):check(G.generate(level,seed))
result=dict(status='passed',source=fid,source_parameterized_banks=semantic,readback=N,sampled_actual_tasks={l:len(v)for l,v in tasks.items()},scope='Source affine easy, polynomial/tangent-slope moderate and radical hard same chain factors with retained cancellation/evaluation stages; actual negative radical and monomial domains read without positive-x narrowing. Unrated completions explicitly authored; raw omissions retained.',native_limitations='See frozen validation and expanded valid-equivalent probes; canonical answers separately tested.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

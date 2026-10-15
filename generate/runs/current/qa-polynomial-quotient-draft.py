"""Root complete polynomial quotients, ordered operands and domain identity."""
import sys,json,hashlib,importlib.util,re,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096620;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_polyquot_gen',D.with_suffix('.py'));H=load('root_polyquot_scalar',R/'ode-scalar-parser.py');B=load('root_polyquot_group',R/'direct-derivative-readback.py');x=H.x
parse=lambda z:H.scalar(z.replace('[','(').replace(']',')'))
def eq(a,b):return s.cancel(a-b)==0
def group(t,i):return B.group(t,i)
def fraction(raw):
 raw=raw.strip().rstrip('.,');i=raw.index(r'\frac')+5;nu,j=group(raw,i);de,j=group(raw,j);assert j==len(raw.strip());return parse(nu),parse(de)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fid=dict(records=0,banks=0,values=0,keys=0,solutions=0,fieldless=0)
for sid,o in olds.items():
 q=G.generate('easy',template=sid,profile='raw')['question'];fid['records']+=1
 for key in(':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert(key in q)==(key in o)
 assert q[':question/problem']==o[':question/problem']
 if ':question/worked-solution'in o:assert q[':question/worked-solution']==o[':question/worked-solution'];fid['solutions']+=1
 if not o.get(':question/answer-fields'):fid['fieldless']+=1
 for f,of in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
  assert f[':answer-field/key']==of[':answer-field/key']and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fid['banks']+=1;fid['values']+=len(f[':answer-field/choices']);assert(':answer-field/correct'in f)==(':answer-field/correct'in of)
  if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fid['keys']+=1
N=dict(records=0,defined_polynomials=0,derivatives=0,substituted_factors=0,stages=0,values=0,pairs=0,domain_checks=0);tasks={l:set()for l in G.SUPPORTED_LEVELS}
PRIME=lambda letter:r'\{?'+letter+r'\}?\^\{(?:′|\x27|\\prime)\}\(x\)'
def prose(t):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','[M]',t,flags=re.S)).replace('[M],','[M]').strip()
def check(r,capacity=False):
 q=r['question'];m=r['generation'];assert m['profile']!='raw';sid=m['template'];prompt=q[':question/problem'];given=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',prompt);assert given;U,V=fraction(given[1]);F=U/V;df=s.diff(F,x);sol=q[':question/worked-solution'];u=parse(re.search(r'\$u\(x\)\s*=\s*(.*?)\$',sol)[1]);v=parse(re.search(r'\$v\(x\)\s*=\s*(.*?)\$',sol)[1]);assert eq(u,U)and eq(v,V);du,dv=s.diff(u,x),s.diff(v,x);N['defined_polynomials']+=2
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 if len(blocks)==2:
  derivs=[row.split('&=',1)[1]for row in blocks[0].split(r'\\')];assert len(derivs)==2
 else:
  mm=re.search(r'\$\$\s*u\^\{\\prime\}\(x\)=(.*?),\\,v\^\{\\prime\}\(x\)=(.*?)\$\$',sol,re.S);assert mm;derivs=list(mm.groups())
 assert eq(parse(derivs[0]),du)and eq(parse(derivs[1]),dv);N['derivatives']+=2
 rows=[row.split('&=',1)[1].strip().rstrip('.')for row in blocks[-1].split(r'\\')];assert len(rows)=={'q-11955':3,'q-104305':3,'q-104309':5}.get(sid,4)
 assert rows[0]==r'\frac{u^{\prime}(x)\cdot v(x)-u(x)\cdot v^{\prime}(x)}{[v(x)]^{2}}'
 num,j=group(rows[1],5);den,j=group(rows[1],j);ops=re.fullmatch(r'\((.*?)\)\\cdot \((.*?)\)-\((.*?)\)\\cdot \((.*?)\)',num);assert ops
 for actual,want in zip(ops.groups(),(du,v,u,dv)):assert eq(parse(actual),want);N['substituted_factors']+=1
 assert eq(parse(den),v*v)
 for row in rows[1:]:assert eq(parse(row),df);N['stages']+=1
 if sid=='q-128235':assert re.fullmatch(r'\(.*\)-\(.*\)',group(rows[2],5)[0])
 if sid=='q-128335':assert r'\cdot'in group(rows[-1],5)[0]
 if sid=='q-104309':assert len(re.findall(r'[-+]',group(rows[2],5)[0]))>=3
 if sid in olds and ':question/worked-solution'in olds[sid]:assert prose(sol)==prose(olds[sid][':question/worked-solution'])
 f=q[':question/answer-fields'][0];vals=[parse(a[':answer/value'])for a in f[':answer-field/choices']];assert[a[':answer/id']for a,vv in zip(f[':answer-field/choices'],vals)if eq(vv,df)]==[f[':answer-field/correct'][1]]
 for i,vv in enumerate(vals):
  for w in vals[:i]:assert not eq(vv,w);N['pairs']+=1
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in prompt
 # Content simplification must keep every original excluded denominator root.
 correct=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);dd=s.Poly(v,x).sqf_part().monic().as_expr();N['domain_checks']+=1
 # The displayed fraction, before SymPy cancellation, retains removable holes.
 if correct.startswith(r'\frac'):
  _,printed_den=fraction(correct);assert s.Poly(printed_den,x).sqf_part().monic().as_expr()==dd
 if capacity:tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(s.cancel(F)),s.srepr(dd)))
 N['records']+=1;N['values']+=len(vals)
for e in json.load(open(D/'engine-input.json')):check(e['record'])
for level in G.SUPPORTED_LEVELS:
 for seed in range(18):check(G.generate(level,seed))
# Independent complete supplied-task enumeration of authored slot domains.
for level,bound in(('moderate',4),('hard',3)):
 for c,e,a,d in itertools.product([v for v in range(-bound,bound+1)if v],repeat=4):
  check(G.generate(level,template='authored-'+level,parameters=dict(c=c,e=e,a=a,d=d)),True)
 assert len(tasks[level])=={'moderate':1912,'hard':632}[level]
result=dict(status='passed',source=fid,readback=N,capacity={l:len(v)for l,v in tasks.items()if v},scope='Missing moderate affine/two-term-quadratic has fixed4 products; missing hard two-termquadratic pair fixed6products, degrees2 and no new differentiation method. Actual first-step→next route keeps other-function quotients and Leibniz following this KP; authored scope anchored canonical e3637. Source easy chains/prose retained separately.',native_limitations='591accepted1024rejected165intentional invalidradio transports; genuine unreduced blank quotient-rule equivalents accepted. Generic54freshaccepted8wrongreject0unresolved. No engine changes.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

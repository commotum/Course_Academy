"""Root independent readback of all cosecant derivative/evaluation families."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186115190;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_csc_gen',D.with_suffix('.py'));H=load('root_csc_direct',R/'direct-derivative-readback.py');x=H.x
@lru_cache(maxsize=10000)
def eq(a,b):
 delta=s.expand(a-b)
 if delta==0:return True
 for point in(s.pi/4,s.Integer(1)):
  v=delta.subs(x,point)
  if v.is_finite and v.is_zero is False:return False
 return s.trigsimp(delta,method='fu')==0 or s.simplify(delta)==0
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fid=dict(records=0,banks=0,values=0,keys=0,solutions=0,fieldless=0)
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];q=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question'];fid['records']+=1
 for key in(':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert(key in q)==(key in o)
 assert q[':question/problem']==o[':question/problem']
 if ':question/difficulty'in o:assert q[':question/difficulty']==o[':question/difficulty'][':db/ident']
 if ':question/worked-solution'in o:assert q[':question/worked-solution']==o[':question/worked-solution'];fid['solutions']+=1
 if not o.get(':question/answer-fields'):fid['fieldless']+=1
 for f,of in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
  assert f[':answer-field/key']==of[':answer-field/key']and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fid['banks']+=1;fid['values']+=len(f[':answer-field/choices']);assert(':answer-field/correct'in f)==(':answer-field/correct'in of)
  if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fid['keys']+=1
N=dict(records=0,formal_operands=0,stages=0,values=0,pairs=0,blanks=0,evaluation_points=0);tasks={l:set()for l in('easy','moderate','hard')}
def check(r):
 q=r['question'];m=r['generation'];assert not m['evidence_only']and m['eligible_for_learning'];sid=m['template'];prompt=q[':question/problem'];given=re.search(r'\$([fgh])\(x\)\s*=\s*(.*?)\$',prompt);assert given;name=given[1];F=H.scalar(given[2]);requested=prompt.split('$')[1].replace('′',"'");target=re.fullmatch(r"\{?([fgh])\}?(?:\^\{'\}|')\((.*)\)",requested);assert target and target[1]==name;point=None if target[2]=='x'else H.scalar(target[2]);df=s.diff(F,x);want=df if point is None else s.simplify(df.subs(x,point))
 if point is not None:assert point.is_real and s.sin(point)!=0 and F.subs(x,point).is_finite;N['evaluation_points']+=1
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==(1 if point is None else 2)
 for bi,b in enumerate(blocks):
  rows=[v for v in b.split(r'\\')if v.strip()];assert len(rows)==(3 if bi==0 else 4 if name=='g'else 3)
  rhs=[]
  for ri,row in enumerate(rows):
   left,raw=row.replace('&','').split('=');raw=H.clean(raw).replace(r'\,','');rhs.append(raw)
   if left.strip():
    label=re.fullmatch(r"\{?([fgh])\}?(?:\^\{'\}|')\((.*)\)",left.strip().replace('′',"'"));assert label and label[1]==name;assert eq(H.scalar(label[2]),x if bi==0 else point)
   if bi==0 and ri==0:
    op=next(d for d in H.DERS if d in raw);arg,end=H.group(raw,len(op));assert eq(H.scalar(arg),F);value=s.diff(H.scalar(arg),x);N['formal_operands']+=1
   else:value=H.scalar(raw)
   assert eq(value,df if bi==0 else want),('actual printed derivative stage',sid,raw,value,want);N['stages']+=1
  if bi==0:assert '(-'in rhs[1]
 if point is not None:
  points=re.findall(r'substitute \$x=(.*?)\$',sol);assert len(points)==1 and eq(H.scalar(points[0]),point)
 f=q[':question/answer-fields'][0];vals=[H.scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if eq(v,want)]==[f[':answer-field/correct'][1]]
 for i,v in enumerate(vals):
  for w in vals[:i]:assert not eq(v,w);N['pairs']+=1
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in prompt;N['blanks']+=1
 N['records']+=1;N['values']+=len(vals)
 if not(sid=='q-105298'and m['profile']=='observed'):tasks[q[':question/difficulty'].split('/')[-1]].add(s.srepr(F)+'|'+str(point))
for r in json.load(open(D/'bounded-records.json')):check(r)
for level in('easy','moderate','hard'):
 for seed in range(18):check(G.generate(level,seed))
assert {l:len(v)for l,v in tasks.items()}==dict(easy=48,moderate=83,hard=168)
result=dict(status='passed',source=fid,readback=N,capacity={l:len(v)for l,v in tasks.items()},scope='Easy source sums; moderate one source product; hard source derivative then familiar-angle substitution/evaluation with unchanged 3+3 or3+4 stages. Authored six familiar angles exclude zero csc derivative bank degeneracy; opaque original pi/2 bank retained observed profile. Source q313723 wrong sign formal operand repaired only normal. Missing key/solution q1889 and field q104316 minimally authored, raw absent attrs retained.',native_limitations='490accepted1000rejected774intentional foreign/malformed/text-radio unresolved;3 retained true broad hyperbolic/double-angle equivalents unresolved; supported scope-preserving equivalents additionally passed; no normal parameter removed for grader.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

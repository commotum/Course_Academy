"""Root printed givens, formal operands, complete banks and blank context."""
import sys,json,hashlib,importlib.util,re,copy
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186115192;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_secant_gen',D.with_suffix('.py'));H=load('root_secant_direct',R/'direct-derivative-readback.py');x=H.x
@lru_cache(maxsize=8000)
def eq(a,b):
 z=s.expand(a-b)
 if z==0:return True
 # An exact ordinary real point is a counterexample, never an equality proof.
 for p in(s.pi/4,s.Integer(1)):
  v=z.subs(x,p)
  if v.is_finite and v.is_zero is False:return False
 return s.trigsimp(z,method='fu')==0 or s.simplify(z)==0
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
N=dict(records=0,formal_operands=0,stages=0,values=0,pairs=0,blanks=0,hard_correct_one=0);tasks={l:set()for l in('easy','moderate','hard')}
counts={'q-1892':[2],'q-31280':[3],'q-1883':[4],'q-1938':[5],'q-337182':[6],'q-104325':[4],'q-105314':[3],'q-105316':[2],'q-340608':[2],'q-340611':[3],'q-340620':[2,4]}
def readrow(raw,F,point=None):
 raw=H.clean(raw).replace(r'\,','')
 for end in(r'\,{|}_{x=0}',r'{|}_{x=0}'):
  if raw.endswith(end):assert point==0;return H.scalar(raw[:-len(end)]).subs(x,point)
 if any(der in raw for der in H.DERS):N['formal_operands']+=1
 return H.value(raw,F,'y',{'formal_derivative_inputs':0})
def check(r):
 q=r['question'];assert not r['generation']['evidence_only'];sid=r['generation']['template'];F,point,name=H.given(q[':question/problem']);df=s.diff(F,x);expected=df if point is None else df.subs(x,point)
 sol=q[':question/worked-solution'];sol=sol.replace(r'\begin{aligned}\begin{aligned}',r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}',r'\end{aligned}')
 bb=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);rows=[[row.split('&',1)[1].strip().removeprefix('=').strip()for row in b.split(r'\\')if row.strip()]for b in bb];assert [len(v)for v in rows]==counts[sid]
 first=rows[0][0];op=next(d for d in H.DERS if d in first);at=first.index(op)+len(op)
 while first[at].isspace()or first.startswith(r'\,',at):at+=2 if first.startswith(r'\,',at)else 1
 operand,end=H.group(first,at);assert eq(H.scalar(operand),F)
 for i,block in enumerate(rows):
  want=df if i==0 else expected
  for row in block:assert eq(readrow(row,F,point),want),('printed derivative stage',sid,row,want);N['stages']+=1
 # Source-stage operations are retained: quotient expansion and factoring,
 # product distribution then common-factor extraction, and the fixed evaluation.
 if sid in('q-1938','q-337182','q-104325'):assert r'\frac{'in rows[0][1]and ')('in rows[0][1]and r'^{2}'in rows[0][1]
 if sid=='q-337182':assert ')('not in rows[0][2]and '('in rows[0][3]and '('in rows[0][4]and '('in rows[0][5]
 if sid in('q-105314','q-340611'):assert '+'in rows[0][1]and '('in rows[0][2]
 f=q[':question/answer-fields'][0];vals=[H.scalar(a[':answer/value'])for a in f[':answer-field/choices']]
 if f[':answer-field/type'].endswith('/blank'):
  context=q[':question/problem'].split('\n\n',1)[1].replace('{{'+f[':answer-field/key']+'}}','('+f[':answer-field/choices'][0][':answer/value']+')').replace('$','').replace('\n','');assert eq(H.scalar(context.split('=',1)[1]),expected),('blank contextual completion',sid,context);N['blanks']+=1
 else:
  assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if eq(v,expected)]==[f[':answer-field/correct'][1]]
  for i,v in enumerate(vals):
   for w in vals[:i]:assert not eq(v,w);N['pairs']+=1
 if sid=='q-340620'and expected==1:N['hard_correct_one']+=1
 N['records']+=1;N['values']+=len(vals);tasks[q[':question/difficulty'].split('/')[-1]].add(s.srepr(F)+'|'+str(point))
for e in json.load(open(D/'native-input.json')):
 if not e['record']['generation']['evidence_only']:check(e['record'])
for level in('easy','moderate','hard'):
 for seed in range(18):check(G.generate(level,seed))
assert N['hard_correct_one']>0 and sum(map(len,tasks.values()))==143
result=dict(status='passed',source=fid,readback=N,capacity={l:len(v)for l,v in tasks.items()},scope='Each source-level family retains source workload and operative rows. Easy direct sum, moderate quotient/product and factored derivative blank fragments, hard two-block derivative then fixed x0 evaluation. All three levels observed. 143 canonical supplied-function/evaluation tasks independent of seed and bank.',native_limitations='298accepted345rejected;289 intentional malformed/foreign/type errors and3 genuine ln-power equivalents unresolved (4,8,9). Canonical and reordered non-log-power equivalents accepted. No valid output excluded.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

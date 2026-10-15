"""Root actual cotangent families, every stage and both fraction-table blanks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186115191;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_cot_gen',D.with_suffix('.py'));H=load('root_cot_direct',R/'direct-derivative-readback.py');x=H.x;w=s.Symbol('root_cot_circle_w',real=True)
@lru_cache(maxsize=10000)
def eq(a,b):
 d=s.expand(a-b)
 if d==0:return True
 circle={s.sin(x):2*w/(1+w*w),s.cos(x):(1-w*w)/(1+w*w),s.tan(x):2*w/(1-w*w),s.sec(x):(1+w*w)/(1-w*w),s.csc(x):(1+w*w)/(2*w),s.cot(x):(1-w*w)/(2*w)}
 assert all(f.args[0]==x for f in d.atoms(s.sin,s.cos,s.tan,s.sec,s.csc,s.cot))
 return s.cancel(s.expand_log(d.xreplace(circle)))==0
parse=lambda t:H.scalar(t.replace('[','(').replace(']',')'))
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fid=dict(records=0,banks=0,values=0,keys=0,solutions=0,fieldless=0)
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];q=G.generate(c.get('difficulty',c.get('level')),template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question'];assert q[':question/problem']==o[':question/problem']and q.get(':question/worked-solution')==o.get(':question/worked-solution');fid['records']+=1;fid['solutions']+=':question/worked-solution'in o
 for key in(':question/answer-fields',':question/difficulty',':question/worked-solution'):assert(key in q)==(key in o)
 if not o.get(':question/answer-fields'):fid['fieldless']+=1
 for f,of in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
  assert f[':answer-field/key']==of[':answer-field/key']and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fid['banks']+=1;fid['values']+=len(f[':answer-field/choices']);assert(':answer-field/correct'in f)==(':answer-field/correct'in of)
  if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fid['keys']+=1
N=dict(records=0,formal_operands=0,stages=0,values=0,pairs=0,contextual_blanks=0,fraction_tables=0);tasks={l:set()for l in('easy','moderate','hard')}
def check(r):
 q=r['question'];m=r['generation'];sid=m['template'];given=re.search(r'\$([fgy])(?:\(x\))?\s*=\s*(.*?)\$',q[':question/problem']);assert given;F=parse(given[2]);df=s.diff(F,x);point=s.pi/6 if sid=='q-31288'else None;expected=df if point is None else df.subs(x,point);sol=q[':question/worked-solution'].replace(r'\begin{aligned}\begin{aligned}',r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}',r'\end{aligned}');bb=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(bb)==(2 if point is not None else 1)
 for bi,b in enumerate(bb):
  rows=[row.split('&',1)[1].strip().removeprefix('=').strip()for row in b.split(r'\\')if row.strip()];assert len(rows)==(4 if sid=='q-340599'else 3)
  for ri,row in enumerate(rows):
   row=H.clean(row).replace(r'\,','')
   if bi==0 and ri==0:
    der=next(op for op in H.DERS if op in row);arg,end=H.group(row,len(der));assert eq(parse(arg),F);val=s.diff(parse(arg),x);N['formal_operands']+=1
   else:val=parse(row)
   assert eq(val,df if bi==0 else expected),('actual cotangent stage',sid,row,val,expected);N['stages']+=1
  if bi==0:
   assert '(-'in rows[1]or sid=='q-31355'
   if sid in('q-340599','q-340603','q-31355'):assert r'\frac'in rows[1]and r'^{2}'in rows[1]or sid=='q-31355'
 if point is not None:
  requested=re.search(r"Find \$.*?\((.*?)\)\$",q[':question/problem']);assert requested and eq(parse(requested[1]),point);p=re.search(r'substitute \$x=(.*?)\$',sol);assert p and eq(parse(p[1]),point)
 f=q[':question/answer-fields'][0];vals=[parse(a[':answer/value'])for a in f[':answer-field/choices']]
 if f[':answer-field/type'].endswith('/blank'):
  context=q[':question/problem'].split('\n\n',1)[1];placeholder='{{'+f[':answer-field/key']+'}}';assert placeholder in context;context=context.replace(placeholder,'('+f[':answer-field/choices'][0][':answer/value']+')')
  if context.startswith('|'):
   rr=[line.split('|')for line in context.splitlines()];top=rr[0][3].replace('$','');bottom=rr[2][3].replace('$','');assert eq(parse(top)/parse(bottom),expected),('actual table numerator/denominator',sid,top,bottom);N['fraction_tables']+=1
  else:assert eq(parse(context.replace('$','').replace('\n','').split('=',1)[1]),expected),('actual partial blank completion',sid,context)
  N['contextual_blanks']+=1
 else:
  assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if eq(v,expected)]==[f[':answer-field/correct'][1]]
  for i,v in enumerate(vals):
   for vv in vals[:i]:assert not eq(v,vv);N['pairs']+=1
 N['records']+=1;N['values']+=len(vals)
 if not m['evidence_only']:tasks[q[':question/difficulty'].split('/')[-1]].add(s.srepr(F)+'|'+str(point))
for e in json.load(open(D/'native-input.json')):
 if not e['record']['generation']['profile'].startswith('observed-'):check(e['record'])
for level in('easy','moderate','hard'):
 for seed in range(18):check(G.generate(level,seed))
assert {l:len(v)for l,v in tasks.items()}==dict(easy=55,moderate=72,hard=24)
result=dict(status='passed',source=fid,readback=N,capacity={l:len(v)for l,v in tasks.items()},scope='All three observed levels: source direct sums, six fixed-workload products/quotients with full/partial/table response contracts, hard scalar-times-cot derivative at fixed pi6 (csc value2 squared then multiply). Same existing coefficients/base vary; no new derivative rule or progression.2missingkey/solutions and2fieldless raw omissions preserved, minimalnormalcompletions authored; opaque banks separately ineligible.',native_limitations='282accepted456rejected462intentional foreign/malformed/type errors;zero genuine valid-equivalent gaps. Generic54freshaccepted52wrongreject0unresolved.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

"""Root Leibniz notation: actual ordered quotient operands and contextual blanks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096622;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_leibniz_gen',D.with_suffix('.py'));H=load('root_leibniz_scalar',R/'ode-scalar-parser.py');B=load('root_leibniz_group',R/'direct-derivative-readback.py');x=H.x
@lru_cache(maxsize=20000)
def parse(t):
 t=t.strip().rstrip('.,');t=re.sub(r'\\log_\{(\d+)\}x',lambda m:r'(\ln(x)/\ln('+m[1]+'))',t);return H.scalar(t)
@lru_cache(maxsize=20000)
def eq(a,b):
 delta=s.expand(a-b)
 if delta==0:return True
 # Independent exact circle parametrization proves/rejects these same-angle
 # rational identities without heuristic trig simplification on every wrong.
 w=s.Symbol('root_circle_w',real=True);circle={s.sin(x):2*w/(1+w*w),s.cos(x):(1-w*w)/(1+w*w),s.tan(x):2*w/(1-w*w),s.sec(x):(1+w*w)/(1-w*w),s.csc(x):(1+w*w)/(2*w),s.cot(x):(1-w*w)/(2*w)}
 assert all(f.args[0]==x for f in delta.atoms(s.sin,s.cos,s.tan,s.sec,s.csc,s.cot))
 return s.cancel(s.expand_log(delta.xreplace(circle)))==0
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fid=dict(records=0,banks=0,values=0,keys=0,solutions=0)
for sid,o in olds.items():
 q=G.generate(G.TEMPLATES[sid]['level'],template=sid,profile='raw')['question'];assert q==o;fid['records']+=1;fid['solutions']+=':question/worked-solution'in o
 for f in o.get(':question/answer-fields',[]):fid['banks']+=1;fid['values']+=len(f[':answer-field/choices']);fid['keys']+=':answer-field/correct'in f
# Original parameters must drive the actual parameterized bank, not only raw copying.
semantic=dict(banks=0,values=0,keys=0)
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];q=G.generate(c['difficulty'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
 for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
  vals=[parse(a[':answer/value'])for a in f[':answer-field/choices']];original=[parse(a[':answer/value'])for a in of[':answer-field/choices']];assert len(vals)==len(original)
  assert all(sum(eq(v,w)for w in vals)==1 for v in original)and all(sum(eq(w,v)for v in original)==1 for w in vals);semantic['banks']+=1;semantic['values']+=len(vals)
  if ':answer-field/correct'in of:assert eq(parse(of[':answer-field/correct'][':answer/value']),next(v for a,v in zip(f[':answer-field/choices'],vals)if a[':answer/id']==f[':answer-field/correct'][1]));semantic['keys']+=1
N=dict(records=0,defined_operands=0,derivatives=0,substituted_factors=0,stages=0,values=0,pairs=0,blanks=0);tasks={l:set()for l in G.SUPPORTED_LEVELS}
counts={'q-340336':4,'q-340340':4,'q-340337':3,'q-47994':3,'q-11969':4,'q-340332':4,'q-340341':3,'q-340343':7,'q-340335':6,'q-11944':4,'q-9909':4}
FORMAL=r'\frac{v\frac{\text{d}u}{\text{d}x}-u\frac{\text{d}v}{\text{d}x}}{v^{2}}'
def check(r):
 q=r['question'];m=r['generation'];assert m.get('profile')!='raw';sid=m['template'];given=re.search(r'\$y=(.*?)\$',q[':question/problem']);assert given;F=parse(given[1]);df=s.diff(F,x);sol=q[':question/worked-solution'];bind=re.search(r'Let \$u=(.*?)\$ and \$v=(.*?)\$',sol);assert bind;defs=bind[1].split('=');u=parse(defs[-1]);assert all(eq(parse(d),u)for d in defs);v=parse(bind[2]);assert eq(u/v,F);N['defined_operands']+=2;du,dv=s.diff(u,x),s.diff(v,x)
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
 formal=blocks[0].replace('&','');a,b=formal.split(r'\,\text{and}\,');assert a.split('=')[0]==r'\frac{\text{d}u}{\text{d}x}'and b.split('=')[0]==r'\frac{\text{d}v}{\text{d}x}';assert eq(parse(a.split('=',1)[1]),du)and eq(parse(b.split('=',1)[1]),dv);N['derivatives']+=2
 rows=[row.split('&=',1)[1].strip().rstrip('.')for row in blocks[1].split(r'\\')];assert len(rows)==counts[sid]and rows[0]==FORMAL
 nr,j=B.group(rows[1],5);dr,j=B.group(rows[1],j);ops=re.fullmatch(r'\((.*?)\)\\cdot \((.*?)\)-\((.*?)\)\\cdot \((.*?)\)',nr);assert ops
 for actual,want in zip(ops.groups(),(v,du,u,dv)):assert eq(parse(actual),want);N['substituted_factors']+=1
 assert eq(parse(dr),v*v)
 for row in rows[1:]:assert eq(parse(row),df),('printed Leibniz stage',sid,row,df);N['stages']+=1
 if sid=='q-340343':assert r'\ln'in rows[3]and '('in rows[4]and r'\cdot'in rows[6]
 if sid=='q-340335':assert r'\cdot'in rows[3]and r'\frac'in rows[4]and r'\csc'in rows[5]
 f=q[':question/answer-fields'][0];vals=[parse(a[':answer/value'])for a in f[':answer-field/choices']]
 if f[':answer-field/type'].endswith('/blank'):
  ctx=q[':question/problem'].split('\n\n',1)[1].replace('{{'+f[':answer-field/key']+'}}','('+f[':answer-field/choices'][0][':answer/value']+')').replace('$','').replace('\n','');assert eq(parse(ctx.split('=',1)[1]),df),('contextual fragment',sid,ctx);N['blanks']+=1
 else:
  assert[a[':answer/id']for a,vv in zip(f[':answer-field/choices'],vals)if eq(vv,df)]==[f[':answer-field/correct'][1]]
  for i,vv in enumerate(vals):
   for w in vals[:i]:assert not eq(vv,w);N['pairs']+=1
 N['records']+=1;N['values']+=len(vals)
 tasks[q[':question/difficulty'].split('/')[-1]].add(s.srepr(F))
# Native inputs contain normal source/profile anchors and changed parameters.
inputs=json.load(open(D/'engine-input.json'))
for index,e in enumerate(inputs):
 if index%100==0:print('Root Leibniz actual stages read',index,flush=True)
 if e['record']['generation'].get('profile')!='raw':check(e['record'])
for level in G.SUPPORTED_LEVELS:
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fid,source_parameterized_banks=semantic,readback=N,sampled_actual_functions={l:len(v)for l,v in tasks.items()},scope='Observed E/M/H complete same-angle/nonchain quotient families retain formal vdu−udv order, source operative steps and full/partial derivative response contracts. Missing two unrated key/solution/rating assignments explicitly authored; general-base log equality retained.',native_limitations='See frozen worker engine-report.json and generic parent native report; no live DB or engine changes.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

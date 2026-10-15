"""Root real log-chain bindings, negative branches, complete tangent-line banks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186092264;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_natural_log_gen',D.with_suffix('.py'));H=load('root_natural_log_scalar',R/'log-chain-scalar-readback.py');x,u,y=H.x,H.u,H.P.y
clean=lambda t:t.replace(r'\mathrm{d}',r'\text{d}').replace(r'\left.','').replace(r'\left','').replace(r'\right','').replace(r'\big','').replace(r'\,','').replace(r'\cancel','').strip().rstrip('.,')
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fid=dict(records=0,banks=0,values=0,keys=0,solutions=0,fieldless=0)
for sid,o in olds.items():
 q=G.raw_replay(sid)['raw_question'];assert q==o;fid['records']+=1;fid['solutions']+=':question/worked-solution'in o
 if not o.get(':question/answer-fields'):fid['fieldless']+=1
 for f in o.get(':question/answer-fields',[]):fid['banks']+=1;fid['values']+=len(f[':answer-field/choices']);fid['keys']+=':answer-field/correct'in f
N=dict(records=0,bindings=0,partial_derivatives=0,chain_stages=0,canceled_factors=0,points=0,whole_line_checks=0,values=0,pairs=0,negative_branch_power_instances=0);tasks={l:set()for l in G.SUPPORTED_LEVELS};semantic=dict(banks=0,values=0,keys=0)
def line(raw):
 left,right=raw.split('=');residual=s.expand(H.scalar(left)-H.scalar(right));assert residual.is_polynomial(x,y)and s.Poly(residual,x,y).total_degree()==1;co=residual.coeff(y);assert co!=0;answer=s.expand(y-residual/co);assert not answer.has(y);return answer

def check(r,source_id=None):
 q,m=r['question'],r['generation'];prompt=q[':question/problem'];given=re.search(r'\$([fg])\(x\)=(.*?)\$',prompt);assert given;name=given[1];F=H.scalar(given[2]);df=s.diff(F,x);point=None;yp=None;line_target='Find the equation of the tangent'in prompt
 if line_target:
  coordinates=re.search(r'at the point \$(.*?)\$',prompt);assert coordinates;coords=coordinates[1].rstrip('.');assert coords[0]=='('and coords[-1]==')';a,b=coords[1:-1].split(',');point,yp=H.scalar(a),H.scalar(b);assert H.eq(F.subs(x,point),yp)
 else:
  p=re.search(r'where \$x=(.*?)\$',prompt)
  if p:point=H.scalar(p[1])
 if point is not None:assert F.subs(x,point).is_finite;N['points']+=1
 bb=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);assert len(bb)==(5 if line_target else 4 if point is not None else 3)
 composite=clean(bb[0]);first,inner=re.split(r',\s*u=',composite);left,outer=first.split('=',1);assert left==name;U=H.scalar(inner);O=H.scalar(outer);assert H.eq(O.subs(u,U),F);N['bindings']+=1
 if U.is_Pow and U.base==x and U.exp.is_even:
  assert H.eq(F.subs(x,-s.Integer(2)),O.subs(u,U.subs(x,-s.Integer(2))));N['negative_branch_power_instances']+=1
 DER=r'\\frac\{\\text\{d\}([fgyu])\}\{\\text\{d\}([xu])\}';expected_map={(name,'u'):s.diff(O,u),('u','x'):s.diff(U,x),(name,'x'):df}
 parts=clean(bb[1]).split(',');assert len(parts)==2
 for part in parts:
  sides=part.split('=');op=re.fullmatch(DER,sides[0].strip());assert op and(op[1],op[2])in expected_map
  for rhs in sides[1:]:assert H.eq(H.scalar(rhs),expected_map[(op[1],op[2])]);N['partial_derivatives']+=1
 def value(raw):
  t=clean(raw);at=None;bar=re.search(r'(?:\{\|\}|\|)_\{',t)
  if bar:
   actual,end=H.group(t,bar.end()-1);assert actual.startswith('x=')and point is not None;at=H.scalar(actual[2:]);assert H.eq(at,point);t=t[:bar.start()]+t[end:]
  replacements={}
  def formal(mm):
   key=(mm[1],mm[2]);assert key in expected_map;token=('i','j','k')[len(replacements)];replacements[H.P.locals_[token]]=expected_map[key];return '('+token+')'
  t=re.sub(DER,formal,t);v=H.scalar(t).subs(replacements).subs(u,U);return v.subs(x,at)if at is not None else v
 for bi,b in enumerate(bb[2:4]if point is not None else bb[2:3]):
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',b);rr=[row.split('&',1)[1].strip().removeprefix('=').strip()for row in text.split(r'\\')if row.strip()];want=df if bi==0 else df.subs(x,point)
  if bi==0:assert re.fullmatch(DER+r'\\cdot '+DER,clean(rr[0]))
  for raw in rr:assert H.eq(value(raw),want),('actual natural-log chain stage',m['source_id'],raw,value(raw),want);N['chain_stages']+=1
  for cc in re.finditer(r'\\cancel\{',b):arg,end=H.group(b,cc.end()-1);assert H.scalar(arg)!=0;N['canceled_factors']+=1
 target=s.expand(df.subs(x,point)*(x-point)+yp)if line_target else df.subs(x,point)if point is not None else df
 if line_target:
  b=re.sub(r'\\(?:begin|end)\{aligned\}','',bb[-1]);rows=[row.strip()for row in b.split(r'\\')];assert len(rows)==3 and rows[0].replace(' ','')==r'y-y_1&=m(x-x_1)'
  for row in rows[1:]:assert H.eq(line(row.replace('&','')),target),('point-slope line stage',row,target);N['whole_line_checks']+=1
 f=q[':question/answer-fields'][0];values=[line(a[':answer/value'])if line_target else H.scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if H.eq(v,target)]==[f[':answer-field/correct'][1]]
 for i,v in enumerate(values):
  for vv in values[:i]:assert not H.eq(v,vv);N['pairs']+=1
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}'in prompt
 if source_id is not None:
  for of in olds[source_id].get(':question/answer-fields',[]):
   original=[line(a[':answer/value'])if line_target else H.scalar(a[':answer/value'])for a in of[':answer-field/choices']];assert len(original)==len(values)and all(sum(H.eq(v,w)for w in values)==1 for v in original)and all(sum(H.eq(w,v)for v in original)==1 for w in values);semantic['banks']+=1;semantic['values']+=len(values)
   if ':answer-field/correct'in of:old=line(of[':answer-field/correct'][':answer/value'])if line_target else H.scalar(of[':answer-field/correct'][':answer/value']);assert H.eq(old,next(v for a,v in zip(f[':answer-field/choices'],values)if a[':answer/id']==f[':answer-field/correct'][1]));semantic['keys']+=1
 N['records']+=1;N['values']+=len(values);tasks[q[':question/difficulty'].split('/')[-1]].add((s.srepr(F),str(point),'line'if line_target else'derivative'if point is None else'slope'))
for sid in olds:check(G.source_case(sid),sid)
for level in G.SUPPORTED_LEVELS:
 for seed in range(40):check(G.generate(level,seed=seed))
assert N['negative_branch_power_instances']>0
result=dict(status='passed',source=fid,source_parameterized_banks=semantic,readback=N,sampled_actual_tasks={l:len(v)for l,v in tasks.items()},scope='MA practice labels preserved; authored missing easy affine-chain family stays within introductory method. Real ln(x^even) keeps both signs. Hard full tangent equations satisfy actual point and derivative slope; equality compares complete lines up to nonzero scale. Two nonMA inventory rows separated from source evidence.',native_limitations='See frozen native-validation evidence and generic parent report.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

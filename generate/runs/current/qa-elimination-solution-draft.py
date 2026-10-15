"""Parent full solution: actual equations, every stage and complete method-error tuples."""
import importlib.util,json,re,hashlib,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2];letters={c:s.Symbol(c,real=True) for c in 'xystabuvwz'}
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
def scalar(raw):
 raw=re.sub(r'\\cancel\{([^{}]*)\}',r'\1',raw);raw=raw.strip().rstrip('.,').replace('&','').replace(r'\left','').replace(r'\right','');raw=re.sub(r'-\s+\\frac',r'-\\frac',raw);raw=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',raw);assert re.fullmatch(r'[xystabuvwz0-9()\s+*/.\-]+',raw),raw;return s.expand(parse_expr(raw,local_dict=letters,transformations=standard_transformations+(implicit_multiplication_application,)))
def equation(raw):a,b=raw.split('=',1);return scalar(a),scalar(b)
def pair(raw):return tuple(scalar(v) for v in raw.strip()[1:-1].split(','))
def same(a,b):return s.simplify(a-b)==0
def check(k,provided=None,write=True):
 g=load(ROOT/f'generate/scratch/{k}-draft.py','fullsystem'+str(k));source={'originals':3};D=ROOT/f'generate/scratch/{k}-draft';records=provided if provided is not None else json.loads((R/f'qa/{k}-sampled.json').read_text());C=dict(records=0,marked_operations=0,distributed_rows=0,ordered_grouped_components=0,collected_rows=0,back_substitution_stages=0,prose_conclusions=0,choice_reinsertions=0,whole_banks=0,primitive_workload_checks=0)
 for r in records:
  q=r['question'];text=q[':question/problem'];m=re.search(r'solution \$\(([xystabuvwz]), ?([xystabuvwz])\)\$',text);assert m;textvars=m.groups();u,v=map(letters.get,textvars);target=u if k==17592186192656 else v;backvar=v if target==u else u;body=re.search(r'\n\$(?:\\)?\{(.*?)\$',text)
  if body:rows=[equation(row) for row in body[1].split('; ')]
  else:
   body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S);assert body;rows=[equation(z) for z in body[1].split(r'\\')]
  assert len(rows)==2;solution=s.solve([a-b for a,b in rows],(u,v));assert set(solution)=={u,v};X,Y=solution[u],solution[v];point=(X,Y);coeff=[a.coeff(target) for a,b in rows];row=0 if abs(coeff[0])<abs(coeff[1]) else 1;m=-coeff[1-row]/coeff[row];assert m.q==1;scaled=[(s.expand(m*a),s.expand(m*b)) if i==row else (a,b) for i,(a,b) in enumerate(rows)];A,B=scaled[0][0]+scaled[1][0],scaled[0][1]+scaled[1][1];assert A.coeff(target)==0 and A.coeff(backvar)!=0
  level=q[':question/difficulty'].split('/')[-1];assert all(z.q==1 and 1<=abs(z)<=5 for z in point);small=min(map(abs,coeff));assert (small==1 if level=='easy' else 2<=small<=3);assert (2<=abs(m)<=7 if level=='easy' else 2<=abs(m)<=4 if level=='moderate' else 5<=abs(m)<=7)
  primitive_coeff=[abs(a.coeff(target))/s.igcd(*(int(a.coeff(w)) for w in (u,v)),int(b)) for a,b in rows];small0=min(primitive_coeff);ratio0=max(primitive_coeff)/small0
  assert (small0==1 if level=='easy' else 2<=small0<=3) and ratio0.q==1 and (2<=ratio0<=7 if level=='easy' else 2<=ratio0<=4 if level=='moderate' else 5<=ratio0<=7);C['primitive_workload_checks']+=1
  sol=q[':question/worked-solution'];op=re.search(r'multiply the (first|second) equation by \$([^$]+)\$',sol);assert op and (0 if op[1]=='first' else 1)==row and scalar(op[2])==m;bs=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(bs)==(3 if k==17592186192656 else 4)
  inner=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',bs[0],re.S);assert len(inner)==2
  before=inner[0].split(r'\\')
  for i,z in enumerate(before):
   z=z.replace(r'\bigl','').replace(r'\bigr','').replace(r'\left','').replace(r'\right','').replace('&','').replace(r'\,','');z=re.sub(r'\s+','',z)
   if i==row:
    zz=re.fullmatch(r'\((.*?)\)\\times\((-?\d+)\)',z);assert zz and s.Rational(zz[2])==m and equation(zz[1])==rows[i];C['marked_operations']+=1
   else:assert equation(z)==rows[i]
  assert [equation(z) for z in inner[1].split(r'\\')]==scaled;C['distributed_rows']+=2
  stages=bs[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\');assert len(stages)==(4 if A.coeff(backvar)==1 else 5)
  for stage,want in zip(stages[:2],scaled):assert equation(stage)==want;C['distributed_rows']+=1
  left,right=stages[2].split('=',1);left=re.sub(r'\s+','',left.replace('&',''));right=re.sub(r'\s+','',right);assert left.startswith('(') and left.endswith(')') and right.startswith('(') and right.endswith(')');parts=re.findall(r'([+-]?\d*)'+str(backvar),left);got=[s.Integer(1 if z in ('','+') else -1 if z=='-' else z) for z in parts];assert got==[a.coeff(backvar) for a,b in scaled];nums=list(map(s.Integer,re.findall(r'[+-]?\d+',right)));assert nums==[b for a,b in scaled];C['ordered_grouped_components']+=4
  assert equation(stages[-1])==(backvar,solution[backvar]);assert len(stages)==4 or equation(stages[3])==(s.expand(A),s.expand(B));C['collected_rows']+=len(stages)-3
  backrow=0 if r['generation']['template'] in ('radio_solution','moderate_blank_solution') else row
  back=bs[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\');assert len(back)==(4 if coeff[backrow]==1 else 5);assert equation(back[0])==rows[backrow];a,b=rows[backrow];co=a.coeff(target);remain=a.coeff(backvar);expected=s.expand(co*target+remain*solution[backvar])-b
  for stage in back[1:]:
   L,R0=equation(stage);poly=s.expand(L-R0);assert same(poly.subs(target,solution[target]),0) and poly.has(target);ratio=s.simplify(poly/expected);assert not ratio.has(target) and ratio!=0,(stage,expected);C['back_substitution_stages']+=1
  # Check separately substituted/evaluated remaining-variable components.
  lhs=back[1].split('=',1)[0].replace('&','');assert '('+str(solution[backvar])+')' in lhs;lhs2=scalar(back[2].split('=',1)[0]);assert lhs2.coeff(target)==co and lhs2.subs(target,0)==remain*solution[backvar]
  for key,want in ((str(u),X),(str(v),Y)):
   ending=sol.split('Therefore,',1)[1];assert re.search(r'(?<![a-z])'+key+r'\s*=\s*'+re.escape(str(want)),ending)
  endpair=re.search(r'which can be expressed as \$\((.*?)\)\.?\$',sol);assert endpair and pair('('+endpair[1]+')')==point;C['prose_conclusions']+=1
  for f in q[':question/answer-fields']:
   vals=[]
   for a in f[':answer-field/choices']:
    V=pair(a[':answer/value']) if f[':answer-field/type'].endswith('/radio') else (scalar(a[':answer/value']),);want=point if len(V)==2 else (X,) if f[':answer-field/key']=='field-1' else (Y,);assert (V==want)==(a[':answer/id']==f[':answer-field/correct'][1]);assert V not in vals;vals.append(V);C['choice_reinsertions']+=len(V)
    if len(V)==2:assert all(same((L-R0).subs({u:V[0],v:V[1]}),0) for L,R0 in rows)==(V==point)
   if len(vals)==5:
    if k==17592186192656:assert sum(all(z.q==1 for z in V) for V in vals)>=2,('sole integer correct shortcut',r['generation'])
    # Independently reconstruct every full wrong pair from printed row data.
    a,b=rows[row];c=rows[1-row][0];d=rows[1-row][1];ai=a.coeff(target);bi=a.coeff(backvar);Bi=c.coeff(backvar);ci=b;Ci=d;wrong=[(Ci+ci)/(Bi+m*bi),(Ci+m*ci)/(Bi+bi),(Ci-m*ci)/(Bi+m*bi)];make=lambda w:tuple((s.simplify((ci-bi*w)/ai),w) if target==u else (w,s.simplify((ci-bi*w)/ai)));expectedbank=[point]+[make(w) for w in wrong];last=s.simplify((ci+bi*solution[backvar])/ai);expectedbank.append((last,solution[backvar]) if target==u else (solution[backvar],last))
    if k==17592186192657:
     aa=a.coeff(u);bb=a.coeff(v);cc=c.coeff(u);hh=cc+m*aa;nn=Ci+m*ci;back=lambda w:(s.simplify(w),s.simplify((ci-aa*w)/bb));omitted=back((Ci+ci)/hh);sign=back((Ci-m*ci)/hh);add=(X,s.simplify((ci+aa*X)/bb));profile=r['generation']['profile'];expectedbank=[point,omitted,sign,add,(X,-Y)] if profile=='signed_substitution' else [point,back(nn/(cc+aa)),omitted,add,(X,ci-aa*X)]
     assert all(s.igcd(*(int(L.coeff(w)) for w in (u,v)),int(R0))==1 for L,R0 in rows) and abs(A.coeff(u))>=2
    assert set(vals)==set(expectedbank);C['whole_banks']+=1
  C['records']+=1
 source={'originals':0,'values':0,'keys':0,'parameterized_source_solutions':0}
 for row0 in json.loads((D/'source-cases.json').read_text()):
  sid=row0['source_id'];o=row0['record'];r0=g.replay_source(sid,True);q0=r0['question'];source['originals']+=1
  if sid!='q-208816':
   pr,worked=g.observed_backbone(g.ANCHORS[sid],sid);assert pr==o[':question/problem'] and worked==o[':question/worked-solution'];source['parameterized_source_solutions']+=1
  for of,f in zip(sorted(o[':question/answer-fields'],key=lambda z:z[':answer-field/key']),sorted(q0[':question/answer-fields'],key=lambda z:z[':answer-field/key'])):
   if ':answer-field/choices' in of:
    assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']);source['values']+=len(of[':answer-field/choices'])
   if ':answer-field/correct' in of:assert of[':answer-field/correct'][':answer/id']==f[':answer-field/correct'][1];source['keys']+=1
 out=dict(status='passed',kp_id=k,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}-draft.py').read_bytes()).hexdigest())
 if write:(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

import copy
records=json.loads((R/'qa/17592186192656-sampled.json').read_text());bad=copy.deepcopy(records[0]);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('multiply the first equation by $','multiply the first equation by $9',1) if 'multiply the first equation' in bad['question'][':question/worked-solution'] else bad['question'][':question/worked-solution'].replace('multiply the second equation by $','multiply the second equation by $9',1)
try:check(17592186192656,[bad],False)
except AssertionError:pass
else:raise AssertionError('unchanged-final-key wrong scaling prose escaped root reader')
check(17592186192656)


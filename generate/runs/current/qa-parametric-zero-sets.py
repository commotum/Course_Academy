"""Parent complete horizontal/vertical parameter sets from actual printed curves/domains."""
import importlib.util,json,re,hashlib,sys
from functools import lru_cache
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186083278
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
b=load(R/'qa-parametric-lines.py','zerosetparentparser');t=b.t
def scalar(v):return b.scalar(v.replace(r'\times','*'))
def roots_value(v):
 v=v.strip().rstrip('.,').replace('$','').replace(r'\,','').replace(' only','').replace(' and ', ',');v=re.sub(r't\s*=\s*','',v)
 if r'\pm' in v:
  a=scalar(v.replace(r'\pm',''));return tuple(sorted((-a,a),key=float))
 return tuple(sorted([scalar(z) for z in v.split(',')],key=lambda z:float(s.N(z))))
def seteq(A,B):return len(A)==len(B) and all(b.eq(a,c) for a,c in zip(sorted(A,key=lambda z:float(s.N(z))),sorted(B,key=lambda z:float(s.N(z)))))
def bound(v):return -s.oo if '-\\infty' in v or '- ∞' in v or '-∞' in v else s.oo if '\\infty' in v or '∞' in v else scalar(v)
@lru_cache(maxsize=1000)
def zeros(F,domain):
 Z=s.solveset(F,t,domain=domain);assert isinstance(Z,s.FiniteSet),(F,domain,Z);return tuple(sorted(Z,key=lambda z:float(s.N(z))))
def task(q):
 raw=next(z for z in b.blocks(q[':question/problem']) if re.match(r'\s*x\s*=',z));raw=raw.replace(r'\qquad','').replace(r'\quad','').replace(r'\,','');m=re.match(r'\s*x\s*=(.*?),\s*y\s*=(.*?),\s*(.*?)\.?\s*$',raw,re.S)
 if m:
  F,G=map(scalar,m.groups()[:2]);domaintext=m[3].replace(r'\leq','≤').replace(r'\le','≤');d=re.match(r'\s*(.*?)(≤|<)\s*t\s*(≤|<)(.*?)\s*\.?$',domaintext);assert d,domaintext;L,U=bound(d[1]),bound(d[4]);domain=s.Interval(L,U,left_open=d[2]=='<',right_open=d[3]=='<')
 else:
  m=re.match(r'\s*x\s*=(.*?),\s*y\s*=(.*?)\.?\s*$',raw,re.S);assert m,raw;F,G=map(scalar,m.groups());domain=s.S.Reals
 dx,dy=s.diff(F,t),s.diff(G,t);requested_vertical='vertical' in q[':question/problem'];orientation=('horizontal' if requested_vertical else 'vertical') if K==17592186083280 else ('vertical' if requested_vertical else 'horizontal');target=dx if orientation=='vertical' else dy;companion=dy if orientation=='vertical' else dx;Z=zeros(target,domain);assert len(Z) in (1,2,4);assert all(not b.eq(companion.subs(t,z),0) for z in Z);return F,G,dx,dy,target,companion,Z,domain,orientation
def raw(g):
 qs=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,solutions=0,fields=0,values=0,literal_values=0,keys=0,unrated=0)
 for c in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  old=next(q for q in qs if c['source_id']==q[':question/math-academy-id']);q=g.generate(c.get('difficulty',c.get('level')),template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in old)
   if key in q and key!=':question/answer-fields':assert q[key]==(old[key][':db/ident'] if isinstance(old[key],dict) else old[key]),(c,key)
  C['prompts']+=1;C['solutions']+=(':question/worked-solution' in old);C['unrated']+=(':question/difficulty' not in old);assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],old[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];vals=[a[':answer/value'] for a in f[':answer-field/choices']];prev=[a[':answer/value'] for a in f0[':answer-field/choices']];remaining=list(map(roots_value,prev));C['literal_values']+=sum(v in prev for v in vals)
   for val in vals:
    V=roots_value(val);i=next((i for i,W in enumerate(remaining) if seteq(V,W)),None);assert i is not None;remaining.pop(i)
   assert not remaining and (':answer-field/correct' in f)==(':answer-field/correct' in f0);C['fields']+=1;C['values']+=len(vals)
   if ':answer-field/correct' in f:assert seteq(roots_value(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])),roots_value(f0[':answer-field/correct'][':answer/value']));C['keys']+=1
 return C
def bank(name,F,G,target,roots,domain):
 Z=list(roots)
 if K==17592186083280:
  if name=='exponential':a=s.expand(G).coeff(t,2);c=-s.expand(G).coeff(t);return [(c/(2*a),),(c/a,),(-c/(2*a),),(a/(2*c),),(s.sqrt(c/a),)]
  if name=='logarithmic':k=-s.expand(F).coeff(t);return [(1/k,),(k,),(-1/k,),(s.pi/k,),(1/(s.pi*k),)]
  if name=='cubic':n=-s.expand(G).coeff(t)/(3*s.expand(G).coeff(t,3));z=s.sqrt(n);return [(-z,z),(-s.sqrt(3*n),s.sqrt(3*n)),(z,),(-z,),(0,)]
  if name in ('frequency_trig','legacy_trig'):
   arg=next(iter(F.atoms(s.cos))).args[0];k=s.diff(arg,t);r=s.pi/k
   return [(0,r),(0,),(0,2*r),(r,),(2*r,)] if name=='legacy_trig' else [(0,r),(r/2,3*r/2),(0,),(r,),(0,2*r)]
  return None
 if name=='line_quadratic':a=s.diff(F,t);h=F.subs(t,0)/a;c=s.diff(G,t,2)/2;return [(Z[0],),(-h,),(h,),(c,),(2*c,)]
 if name=='line_cubic':a=s.diff(F,t);h=F.subs(t,0)/a;c=s.diff(G,t,3)/6;return [(Z[0],),(-h,),(-3*c,),(h,),(3*c,)]
 if name=='power_line':n=s.degree(F,t);z=Z[0];return [(z,),(z+1,),(z-1,),(n-1,),(n,)]
 L=domain.start
 if name=='circle_horizontal':return [(L,L+s.pi/2),(L+s.pi/4,L+s.pi/2),(L,L+s.pi),(L+s.pi/4,L+s.pi),(L+s.pi/2,L+s.pi)]
 if name=='circle_vertical':return [(L+3*s.pi/2,),(L+s.pi/2,L+3*s.pi/2),(L+s.pi/4,),(L+s.pi/4,L+3*s.pi/4),(L+s.pi/2,)]
 return None
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','zerosetgenerator');source=raw(g);rs=json.loads((R/f'qa/{K}-sampled.json').read_text());seen={r['generation']['template'] for r in rs}
 for c in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  if c['template'] not in seen:rs.append(g.generate(c.get('difficulty',c.get('level')),seed=93,template=c['template']));seen.add(c['template'])
 C=dict(records=0,derivatives=0,complete_zero_sets=0,zero_equation_stages=0,nonzero_substitution_stages=0,concluding_parameters=0,choices=0,complete_banks=0)
 for r in rs:
  q=r['question'];F,G,dx,dy,target,companion,Z,domain,o=task(q);sol=q[':question/worked-solution'];bs=b.blocks(sol);body=next(z for z in bs if (re.search(r"x(?:'|\\prime)\(t\)=",z) or '{x}^{′}(t)=' in z) and ',' in z);parts=re.split(r',\\(?:,|quad|qquad)\s*',body);assert len(parts)==2,(r['generation']['template'],body,parts)
  for part,d in zip(parts,(dx,dy)):assert b.eq(scalar(part.split('=',1)[1].replace(r'\end{aligned}','')),d);C['derivatives']+=1
  derivative_block=body
  for body in bs:
   if body==derivative_block:continue
   body=body.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
   for row in body.split(r'\\'):
    m=re.search(r'(?:\{[xy]\}\^\{′\}|[xy]\'|[xy]\\prime)\((.*?)\)\s*&?\s*=',row)
    if m:
     if m[1]=='t':continue
     z=scalar(m[1]);assert any(b.eq(z,w) for w in Z);side=row[m.end():].split(r'\ne')[0];assert r'\ne' in row
     for expr in side.split('='):assert b.eq(scalar(expr),companion.subs(t,z)) and not b.eq(scalar(expr),0),(r['generation']['template'],row,companion);C['nonzero_substitution_stages']+=1
     continue
    if '=' not in row or '′' in row or "'" in row or r'\prime' in row or row.lstrip().startswith('m='):continue
    row=row.replace('&','')
    for component in re.split(r'(?:⟹|\\implies|\\Longrightarrow)',row):
     if '=' not in component:continue
     lhs,rhs=component.replace(r'\,','').split('=',1)
     if lhs.strip()=='t':
      values=roots_value(rhs)
      assert seteq(values,Z) if body in [z.replace(r'\begin{aligned}','').replace(r'\end{aligned}','') for z in re.findall(r'\$\$(.*?)\$\$',sol,re.S)] else all(any(b.eq(v,w) for w in Z) for v in values),(component,Z)
      C['complete_zero_sets']+=1
     elif b.eq(scalar(rhs),0):assert seteq(zeros(scalar(lhs),domain),Z),(component,Z);C['zero_equation_stages']+=1
     else:assert seteq(zeros(scalar(lhs)-scalar(rhs),domain),Z),(component,Z);C['zero_equation_stages']+=1
  for span in re.findall(r'\$t=(.*?)\$',sol):assert all(any(b.eq(v,z) for z in Z) for v in roots_value(span)),(span,Z);C['concluding_parameters']+=1
  vals=[];keys=re.findall(r'\{\{(field-\d)\}\}',q[':question/problem'])
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    v=roots_value(a[':answer/value']);want=(Z[keys.index(f[':answer-field/key'])],) if f[':answer-field/type'].endswith('/blank') else Z;assert seteq(v,want)==(a[':answer/id']==f[':answer-field/correct'][1]),(r['generation']['template'],a,Z);C['choices']+=1;vals.append(v)
  expected=bank(r['generation']['template'],F,G,target,Z,domain)
  if expected is not None:assert len(vals)==5 and all(sum(seteq(v,w) for v in vals)==1 for w in expected);C['complete_banks']+=1
  C['records']+=1
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 if len(sys.argv)>1:K=int(sys.argv[1])
 check()

"""Root derives identity conditions and banks from actual displayed equations."""
import importlib.util,json,re,sys,math
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_unknown_scalar',P/'ode-scalar-parser.py');g=module('root_unknown_gen',D.with_suffix('.py'));x,u,v=p.x,p.u,p.v
C=dict(records=0,actual_equations=0,choices=0,whole_banks=0,solution_equalities=0,prose_parameter_values=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def scalar(text,names):
 text=text.strip().rstrip('.,').replace('&','')
 text=re.sub(r'\\[A-Za-z]+|[A-Za-z]',lambda m:m[0] if m[0].startswith('\\') else names.get(m[0],m[0]),text)
 return s.expand(p.scalar(text))
def check(r):
 q=r['question'];meta=r['generation'];name=meta['template'];profile=meta.get('profile',meta.get('bank_profile'));prompt=q[':question/problem'];blocks=re.findall(r'\$\$(.*?)\$\$',prompt,re.S);inline=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S)
 equations=[z for z in blocks+inline if '=' in z and 'x' in z];assert len(equations)==1
 raw=equations[0];letters=set(re.findall(r'[a-z]',re.sub(r'\\[A-Za-z]+','',raw)))-{'x'};assert len(letters)==(1 if K==17592186110720 else 2)
 # Determine parameter ordering from actual coefficient dependence, not metadata.
 ns={z:('u' if i==0 else 'v') for i,z in enumerate(sorted(letters))};L,R=map(lambda z:scalar(z,ns),raw.split('='));poly=s.Poly(L-R,x);assert poly.degree()==1
 coeff=poly.nth(1);const=poly.nth(0)
 if K==17592186110721 and v in coeff.free_symbols:
  ns={k:('v' if z=='u' else 'u') for k,z in ns.items()};L,R=map(lambda z:scalar(z,ns),raw.split('='));poly=s.Poly(L-R,x);coeff=poly.nth(1);const=poly.nth(0)
 U=s.solve(coeff,u);assert len(U)==1 and U[0].is_Rational;U=U[0];a=s.diff(coeff,u);b=coeff.subs(u,0)+s.Poly(R,x).nth(1);c=s.Poly(R,x).nth(1)
 if K==17592186110720:
  assert const==0;roots={u:U};correct=U
 else:
  assert coeff.free_symbols=={u} and const.free_symbols=={v};V=s.solve(const,v);assert len(V)==1 and V[0].is_Rational;V=V[0];roots={u:U,v:V};correct=U+V;d=s.diff(const,v);f=s.Poly(R,x).nth(0);e=const.subs(v,0)+f
 field=q[':question/answer-fields'][0];vals=[scalar(z[':answer/value'],{}) for z in field.get(':answer-field/choices',[])];assert len(set(vals))==len(vals) and all(z.is_Rational for z in vals);opaque=profile.startswith(('observed_','raw:'))
 if ':answer-field/correct' in field:
  good=next(z for z in field[':answer-field/choices'] if z[':answer/id']==field[':answer-field/correct'][1]);assert scalar(good[':answer/value'],{})==correct and vals.count(correct)==1
  sol=q[':question/worked-solution'];stages=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
  # First universal rule blocks describe a different arbitrary equation.
  actual=stages[1:] if K==17592186110720 else stages[2:]
  for block in actual:
   body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
   for row in body.split(r'\\'):
    row=row.strip().rstrip('.,');parts=row.split('=');assert len(parts)>=2
    if K==17592186110720 and row.startswith('a='):
     bits=row.split(r',\,');assert len(bits)==2 and scalar(bits[0][2:],ns)==s.Poly(L,x).nth(1);assert scalar(bits[1][2:],ns)==s.Poly(R,x).nth(1);C['solution_equalities']+=2;continue
    actuals=[scalar(z,ns) for z in parts];assert all(s.expand(z.subs(roots)-actuals[0].subs(roots))==0 for z in actuals[1:]),(row,roots);C['solution_equalities']+=len(actuals)-1
    # Equation constraints involving one parameter must uniquely determine it.
    diff=s.expand(actuals[0]-actuals[-1]);syms=diff.free_symbols
    if len(syms)==1 and syms<={u,v}:var=next(iter(syms));assert s.solve(diff,var)==[roots[var]],row
  for span in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S):
   for z in span.split(','):
    if '=' in z and z.split('=',1)[0].strip() in ns:
     lhs,rhs=z.split('=',1);assert scalar(rhs,ns)==roots[scalar(lhs,ns)];C['prose_parameter_values']+=1
 else:assert opaque and ':question/difficulty' not in q and ':question/worked-solution' not in q;C['raw_missing_assessments']+=1
 if K==17592186110720:
  banks={'authored_scale':[U,1/U,-U,c,a*c],'authored_shift':[U,c+b,c/(-b),(-b)/c,c],'observed_ratio':[U,1/U,-1/U,1,0],'observed_scale':[U,1,a,a/U,c],'observed_signed':[U,-U,1/U,0,-a],'observed_shift':[U,c/(-b),(-b)/c,c,-b],'blank':[U]};expected=banks[profile]
  assert meta['evidence_only']==opaque and meta['eligible_for_learning']==(not opaque)
  if not opaque:
   level=q[':question/difficulty'].split('/')[-1]
   if level=='easy':assert (b==0 and a.q==c.q==1 and 2<=abs(a)<=8 and 2<=abs(c)<=16) or (a==1 and b.q==c.q==1 and 2<=abs(b)<=8 and 2<=abs(c)<=12)
   if level=='moderate':assert a.q==b.q==c.q==1 and 2<=abs(a)<=8 and 1<=abs(b)<=9 and 1<=abs(c)<=24 and math.gcd(int(a),int(b),int(c))==1 and U.q<=4 and 0<abs(U)<=12
   if level=='hard':assert all(2<=z.q<=5 and 1<=abs(z.p)<=12 and abs(z)<=4 for z in (a,b,c)) and b.q!=c.q and 2<=(c-b).q<=10 and 2<=U.q<=6 and 1<=abs(U.p)<=12
 else:
  expected={'method-sum':[correct,U,V,c+f,U-V],'method-components':[correct,c/a+V,U+f/d,a*(c-b)+V,U+d*(f-e)],'blank':[correct]}.get(profile)
  if expected is None:
   sid=profile.split(':',1)[1]
   expected={'q-287978':[U,-b,U+2*V,correct,c],'q-287985':[],'q-288583':[correct],'q-288584':[correct],'q-288622':[f,correct,U,2*V,c],'q-288623':[a*c,U,U+f-a,f*a*a,correct],'q-288627':[c+f,correct,correct/2,f,3*f/2]}[sid]
  assert meta['eligible_for_normal_practice']==(not opaque)
  if q.get(':question/difficulty')==':question.difficulty/hard':assert all(z.q==1 for z in (a,b,c,d,e,f)) and 2<=abs(a)<=6 and 2<=abs(d)<=6 and 1<=abs(b)<=8 and 1<=abs(e)<=8 and math.gcd(int(a),int(b),int(c))==math.gcd(int(d),int(e),int(f))==1 and (U.q>1 or V.q>1)
 assert set(vals)==set(expected),(profile,vals,expected);C['whole_banks']+=1;C['choices']+=len(vals);C['records']+=1;C['actual_equations']+=1;return q
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old);of,fld=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in fld.get(':answer-field/choices',[]))==sorted(z[':answer/value'] for z in of.get(':answer-field/choices',[]));C['source_values']+=len(of.get(':answer-field/choices',[]));C['source_banks']+=1
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in fld[':answer-field/choices'] if z[':answer/id']==fld[':answer-field/correct'][1]);C['source_keys']+=1
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(24):check(g.generate(level,seed+10700))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)

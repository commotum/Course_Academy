"""Root reads actual rational functions, whole real-root banks and discriminant stages."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=P.parents[2]/f'generate/scratch/{K}';common=K==17592186087845

def mod(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=mod('root_complex_rational',P/'rational-asymptote-readback.py');g=mod('root_complex_generator',D.with_suffix('.py'));X=p.X
C=dict(records=0,choices=0,complete_operation_banks=0,solution_equalities=0,denominator_zero_conditions=0,partial_factor_conditions=0,discriminant_stages=0,prose_root_statements=0,source_prompts=0,source_values=0,available_source_solutions=0,original_designations=0,raw_omission_profiles=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def check(r):
 q=r['question'];meta=r['generation'];z=p.function(q[':question/problem']);poles=z['poles'];holes=z['domain']-poles;reduced_den=s.fraction(s.cancel(z['value']))[1]
 if common:assert not poles and s.degree(s.gcd(z['numerator'],z['denominator']),X)>0 and holes
 else:assert not holes and s.degree(s.gcd(z['numerator'],z['denominator']),X)==0
 quadratics=[s.Poly(f,X) for f,n in s.factor_list(reduced_den,X)[1] if s.degree(f,X)==2 and s.discriminant(f,X)<0];assert len(quadratics)==1;quad=quadratics[0];a,b,c=quad.all_coeffs();disc=b*b-4*a*c
 assert meta['eligible_for_learning']==(not meta['evidence_only'])
 for f in q.get(':question/answer-fields',[]):
  vals=[p.rootset(v[':answer/value']) for v in f[':answer-field/choices']];C['choices']+=len(vals)
  correct=f.get(':answer-field/correct')
  if f[':answer-field/type'].endswith('/radio'):
   assert len(vals)==5 and len(set(vals))==5 and vals.count(poles)==1
   if correct:assert next(v for ans,v in zip(f[':answer-field/choices'],vals) if ans[':answer/id']==correct[1])==poles
   if common and not meta['evidence_only']:
    monic=quad.monic();aa,bb,cc=monic.all_coeffs();multiplier=2 if meta['template'] in ('quartic','q-4695','q-113547','q-113554','q-39936') else 1;assert meta['operation_profile_multiplier']==multiplier;wrong=p.real_roots(aa*X**2+bb*X-multiplier*cc);expected={frozenset(),holes,wrong,holes|wrong};extra=set(vals)-expected;assert len(expected)==4 and len(extra)==1 and len(next(iter(extra)))==1 and next(iter(extra))<wrong;assert set(vals)==expected|extra;C['complete_operation_banks']+=1
   if not common and meta.get('bank_operations'):
    ops=meta['bank_operations'];assert len(ops)==5;assert {p.real_roots(p.expression(op['zeros_of'])) for op in ops}==set(vals);assert p.real_roots(p.expression(ops[0]['zeros_of']))==poles;C['complete_operation_banks']+=1
  else:
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'];assert len(vals)==1 and len(poles)==1 and vals[0]==poles
 if ':question/worked-solution' in q:
  text=q[':question/worked-solution']
  # Read the actual stated quadratic: rational cancellation may extract a
  # scalar GCF, while the source discriminant uses unreduced coefficients.
  for span in re.finditer(r'\$\$(.*?)\$\$|\$([^$]+)\$',text,re.S):
   raw=p.clean(span[1] if span[1] is not None else span[2])
   if raw.endswith('=0') and 'x' in raw and '=' not in raw[:-2] and r'\\' not in raw:
    candidate=p.expression(raw[:-2])
    if s.degree(candidate,X)==2 and s.discriminant(candidate,X)<0:
     actual=s.Poly(candidate,X);assert actual.monic()==quad.monic();quad=actual;a,b,c=quad.all_coeffs();disc=b*b-4*a*c
  def expr(raw):
   raw=p.clean(raw)
   if re.fullmatch(r'[fgh]\(x\)',raw):assert raw==z['name']+'(x)';return z['value']
   if raw=='D':return disc
   # Only bare coefficient letters are replaced, protecting command names.
   raw=re.sub(r'\\[A-Za-z]+|[abc]',lambda m:m[0] if m[0].startswith('\\') else '('+s.latex({'a':a,'b':b,'c':c}[m[0]])+')',raw)
   return p.expression(raw)
  for block in re.findall(r'\$\$(.*?)\$\$',text,re.S):
   prev=None;isdisc=bool(re.search(r'\bD\s*&?\s*=',block))
   for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
    parts=row.strip().split('=');assert len(parts)>=2;values=[]
    for i,raw in enumerate(parts):
     if not p.clean(raw):assert prev is not None;value=prev
     else:value=expr(raw)
     values.append(value)
    if len(values)==2 and values[-1]==0 and values[0].has(X):assert p.real_roots(values[0])==poles;C['denominator_zero_conditions']+=1
    else:assert all(s.cancel(v-values[0])==0 for v in values[1:]),(row,values,z);C['solution_equalities']+=len(values)-1
    prev=values[-1]
    if isdisc:assert s.simplify(prev-disc)==0;C['discriminant_stages']+=1
  for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',text,re.S):
   inline=p.clean(inline)
   if re.fullmatch(r'x\s*=.+',inline):
    rhs=p.expression(inline.split('=',1)[1]);assert rhs in poles;C['prose_root_statements']+=1
   elif inline.endswith('=0') and 'x' in inline:
    condition=p.expression(inline[:-2]);roots=p.real_roots(condition);assert roots<=poles
    # The no-real-root equation must use the actual remaining irreducible quadratic.
    if s.degree(condition,X)==2 and not roots:assert s.Poly(condition,X).monic()==quad.monic()
    else:assert s.simplify(s.rem(reduced_den,condition,X))==0 or roots==poles
    C['partial_factor_conditions']+=1
 C['records']+=1;return q
cases=json.loads((D/'source-cases.json').read_text())
for case in cases:
 profile=case.get('raw_profile') or ('original' if not common else case['bank_profile']);r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=profile);q=check(r);old=sources[case.get('source_math_academy_id',case['source_id'])];assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in old)
 if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
 if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];C['available_source_solutions']+=1
 oldf={f[':answer-field/key']:f for f in old.get(':question/answer-fields',[])};newf={f[':answer-field/key']:f for f in q.get(':question/answer-fields',[])};assert set(oldf)==set(newf)
 for key,f in oldf.items():
  n=newf[key];assert n[':answer-field/type']==f[':answer-field/type'][':db/ident'];assert sorted((a[':answer/type'],a[':answer/value']) for a in n[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in f[':answer-field/choices']);C['source_values']+=len(f[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in n)
  if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in n[':answer-field/choices'] if a[':answer/id']==n[':answer-field/correct'][1])==f[':answer-field/correct'][':answer/value'];C['original_designations']+=1
 C['raw_omission_profiles']+=1
for r in json.loads((D/'review.json').read_text())+json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(30):check(g.generate(level,seed+84445))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)

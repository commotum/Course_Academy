"""Root independently verifies printed ODE, complete families and integration stages."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186096696;D=P.parents[2]/f'generate/scratch/{K}'
def mod(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=mod('root_direct_reader',P/'direct-integration-readback.py');g=mod('root_direct_generator',D.with_suffix('.py'));X=p.X;C=p.CONST;F=p.F;DF=p.DF
T=dict(records=0,choices=0,whole_operation_banks=0,evidence_banks=0,displayed_solution_equalities=0,source_prompts=0,source_values=0,available_source_solutions=0,original_designations=0,raw_omissions=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def check(r):
 q=r['question'];meta=r['generation'];G=p.forcing(q[':question/problem']);assert meta['eligible_for_learning']==(not meta['evidence_only']);field=q[':question/answer-fields'][0];values=[p.family(a[':answer/value']) for a in field[':answer-field/choices']]
 def valid(v):return s.cancel(p.derivative(v)-G)==0 and s.diff(v,C)!=0 and not s.diff(v,C).has(X,C)
 assert sum(valid(v) for v in values)==1
 # Complete families are equivalent iff they have equal derivatives and
 # independent additive constants; a particular solution is not a general one.
 for i,v in enumerate(values):
  for w in values[:i]:assert s.cancel(p.derivative(v-w))!=0 or v.has(C)!=w.has(C)
 correct=field.get(':answer-field/correct')
 if correct:assert valid(next(v for a,v in zip(field[':answer-field/choices'],values) if a[':answer/id']==correct[1]))
 else:assert meta['evidence_only'] and ':question/worked-solution' not in q and ':question/difficulty' not in q;T['raw_omissions']+=1
 if not meta['evidence_only']:
  d=s.Rational(meta['parameters']['d']);components=[]
  printed=next(z for z in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S) if '=' in z);left,right=printed.split('=',1);actual_d=s.expand(p.expression(left)-p.expression(right)).coeff(DF);assert actual_d==d
  opening=('First, notice that the derivative term is already isolated on the left:' if actual_d==1 else 'First, we rearrange the equation to isolate the derivative term:');assert q[':question/worked-solution'].startswith(opening)
  # The actual displayed derivative supplies the reference, then documented
  # component operations are checked as a complete bank, independently of term().
  for kind,a,b in meta['parameters']['terms']:
   a=s.Rational(a)
   if kind=='poly':h=a*X**b;f=a*X**(b+1)/(b+1);inner=b+1
   elif kind=='exp':h=a*s.exp(b*X);f=a*s.exp(b*X)/b;inner=b
   elif kind=='sin':h=a*s.sin(b*X);f=-a*s.cos(b*X)/b;inner=b
   elif kind=='cos':h=a*s.cos(b*X);f=a*s.sin(b*X)/b;inner=b
   elif kind=='reciprocal':h=a/(X-b);f=a*s.log(s.Abs(X-b));inner=1
   else:raise AssertionError(kind)
   components.append((h,f,inner,kind,a))
  assert s.cancel(sum(h for h,f,j,k,a in components)/d-G)==0
  prims=[f/d for h,f,j,k,a in components];base=sum(prims);wrong=[-base,G,sum(f*j*j/d if k!='reciprocal' else f/(d*a*a) for h,f,j,k,a in components),sum(prims[:-1]) if len(prims)>1 else base/components[0][4]]
  derivs=[p.derivative(v) for v in values];expected=[p.derivative(v) for v in [base]+wrong];assert len(derivs)==len(expected)==5
  assert all(sum(s.cancel(v-w)==0 for w in expected)==1 for v in derivs);T['whole_operation_banks']+=1
 else:T['evidence_banks']+=1
 if ':question/worked-solution' in q:
  primitive=sum(s.integrate(term,X) for term in s.Add.make_args(s.expand(G)))
  for block in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
   prev=None
   for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
    parts=row.split('=');assert len(parts)>=2;vals=[]
    for i,raw in enumerate(parts):
     if not p.normalize(raw):assert i==0 and prev is not None;v=prev
     else:v=p.expression(raw)
     vals.append(v)
    if any(v.has(DF) for v in vals):assert all(s.cancel((v-vals[0]).subs(DF,G))==0 for v in vals[1:]),(row,vals,G)
    else:assert all(s.cancel(p.derivative((v-vals[0]).subs(F,primitive)))==0 for v in vals[1:]),(row,vals,G)
    prev=vals[-1];T['displayed_solution_equalities']+=len(vals)-1
 T['records']+=1;T['choices']+=5;return q
for case in json.loads((D/'source-cases.json').read_text()):
 level=g.TEMPLATES[case['template']];r=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=check(r);old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];T['source_prompts']+=1
 for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (key in old)==(key in q)
 if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];T['available_source_solutions']+=1
 f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0];assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);T['source_values']+=5
 assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
 if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];T['original_designations']+=1
 for scale in (2,'-3/2'):check(g.generate(level,template=case['template'],parameters={'dependent_scale':scale},profile=case['bank_profile']))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for template,level in g.TEMPLATES.items():
 for seed in range(8):check(g.generate(level,seed+96696,template=template))
T['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(T,indent=2)+'\n');print(T)

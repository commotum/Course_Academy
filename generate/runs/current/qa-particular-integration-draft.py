"""Root actual full-bank, integration/condition-stage and supplied-fragment QA."""
import sys,importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096699;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=mod('root_particular_reader',R/'particular-integration-readback.py');g=mod('root_particular_generator',D.with_suffix('.py'));Fid=mod('root_particular_fidelity',R/'root-source-fidelity.py');X=p.X;C=p.C
originals,fidelity=Fid.check(g,K,D)
T=dict(records=0,choices=0,whole_operation_banks=0,evidence_banks=0,displayed_solution_equalities=0,initial_condition_equalities=0,documented_source_error_rows=0,arbitrary_C_general_solutions=0)
tasks={l:set() for l in ('easy','moderate','hard')}
def check(r):
 q=r['question'];meta=r['generation'];G,t,v,name=p.problem(q[':question/problem']);vals,full=p.responses(q,name);valid=lambda z:p.equal(p.derivative(z),G,t) and p.equal(z.subs(X,t),v,t);assert sum(valid(z) for z in full)==1;assert meta['evidence_only']==(not meta['eligible_for_learning']);field=q[':question/answer-fields'][0];ref=field.get(':answer-field/correct')
 if ref:assert valid(next(z for a,z in zip(field[':answer-field/choices'],full) if a[':answer/id']==ref[1]))
 else:assert meta['evidence_only'] and ':question/difficulty' not in q and ':question/worked-solution' not in q
 for i,z in enumerate(vals):
  for w in vals[:i]:assert not p.equal(z,w,t)
 P=p.primitive(G);constant=s.simplify(v-P.subs(X,t));F=s.simplify(P+constant)
 if not meta['evidence_only']:
  level=q[':question/difficulty'].split('/')[-1];tasks[level].add(s.srepr(G)+'|'+str(t)+'|'+str(v))
  if field[':answer-field/type'].endswith('radio'):
   template=meta['template'];params=meta['parameters']
   if template=='three':wrong=3*s.integrate(s.expand(G).coeff(X,2)*X**2,X)+p.primitive(G-s.expand(G).coeff(X,2)*X**2)
   elif template in ('q-119078','q-352066','q-49942'):wrong=P+v+P.subs(X,t)
   elif template in ('q-119045','q-352075'):
    scale=s.Rational(params['scale']);base=P/scale;amp=base.as_coeff_Mul()[0];wrongprim=(base/amp)/(scale*amp);wrong=wrongprim+v-wrongprim.subs(X,t)
   elif template in ('q-119075','q-119083'):
    k=-2 if template=='q-119075' else s.Rational(1,2);e=next(z for z in s.Add.make_args(s.expand(G)) if z.has(s.exp));h=p.primitive(G-e)+e*k;wrong=h+v-h.subs(X,t)
   elif template=='q-50159':h=2*P;wrong=h+v-h.subs(X,t)
   elif template=='q-8311':h=G*X**2/2;wrong=h+v-h.subs(X,t)
   else:h=sum(z*X for z in s.Add.make_args(s.expand(G)));wrong=h+v-h.subs(X,t)
   if template=='three':wrong=wrong+v-wrong.subs(X,t)
   bad_primitive=2*P if template=='q-49942' else G
   expected=[F,P-P.subs(X,t),-P+v+P.subs(X,t),bad_primitive+v-bad_primitive.subs(X,t),wrong]
   assert len(vals)==5 and all(sum(p.equal(z,w,t) for w in expected)==1 for z in vals);T['whole_operation_banks']+=1
 else:T['evidence_banks']+=1
 sol=q.get(':question/worked-solution')
 if sol:
  # Check actual variable roles before normalization, retaining only documented
  # raw teaching-label errors; repaired and default records may not contain them.
  for m in re.finditer(r'(f\(x\)|g\(x\)|(?<![A-Za-z])y)\s*(?:&\s*)?=',sol):
   expected_name='y' if name=='y' else name+'(x)'
   if m[1]!=expected_name:assert meta['profile']=='observed_raw' and meta['template'] in ('q-119045','q-50044')
  if not meta['evidence_only']:
   general=re.search(r'general solution is \$[^$]*?=(.*?)\$',sol);assert general,(meta,sol)
   formula=p.expression(general[1]);assert s.diff(formula,C)==1 and p.equal(p.derivative(formula),G,t);T['arbitrary_C_general_solutions']+=1
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);last_aligned=max(i for i,b in enumerate(blocks) if r'\begin{aligned}' in b);submatch=re.search(r'Let \$u=(.*?)\.\$',sol);sub=p.expression(submatch[1]) if submatch else None
  def resolve(z):
   if sub is not None:z=z.subs(p.SUB,sub)
   return p.interval(z.subs({p.DF:G,p.F:F,C:constant}),t)
  for i,b in enumerate(blocks):
   if r'\begin{aligned}' not in b:
    left,right=b.split('=',1);a=p.expression(left);z=p.expression(right)
    if a==p.F:assert valid(z)
    else:assert p.equal(resolve(a),resolve(z),t)
    T['displayed_solution_equalities']+=1;continue
   prev=None
   for row in b.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\'):
    if meta['profile']=='observed_raw' and meta['template']=='q-50044' and r'6(\frac{{x}^{3}}{3})\,\text{d}x' in row:T['documented_source_error_rows']+=1;prev=p.F;continue
    left,right=row.split('=',1);a=p.expression(left) if p.normalize(left) else prev;z=p.expression(right);assert a is not None;aa=resolve(a);zz=resolve(z)
    if i==last_aligned:assert p.equal(aa,zz,t),(meta,row,aa,zz);T['initial_condition_equalities']+=1
    else:assert p.equal(p.derivative(aa-zz),0,t),(meta,row,aa,zz)
    prev=z;T['displayed_solution_equalities']+=1
  # Every prose condition uses the actual given point, including changed targets.
  for m in re.finditer(r'[fgy]\(([-\d]+)\)\s*=\s*(-?\d+)',sol):assert s.Integer(m[1])==t and s.Integer(m[2])==v
 T['records']+=1;T['choices']+=len(vals);return q
for c in json.loads((D/'source-cases.json').read_text()):
 for scale in (1,-2,3):
  for profile in ('observed_raw','observed_repaired'):check(g.generate(c['level'],template=c['template'],parameters={'scale':scale},profile=profile))
 for scale,target in ((1,5),(-2,-3),(3,7)):
  try:rec=g.generate(c['level'],template=c['template'],parameters={'scale':scale,'target':target})
  except AssertionError:continue
  check(rec)
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for k in (-2,-1,1,2):
 for kind in ('blank','radio'):
  check(g.generate('hard',template='three',field_type=kind,parameters={'a':2,'b':-2,'d':3,'k':k,'t':0,'v':4,'name':'g','family':'three'}))
report=dict(status='passed',source=fidelity,readback=T,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(report)

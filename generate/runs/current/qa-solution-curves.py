"""Root mathematical readback of plotted complete families and fixed solution steps."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186096698;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=mod('root_curve_reader',R/'direct-integration-readback.py');g=mod('root_curve_generator',D.with_suffix('.py'));X=p.X;C=p.CONST;F=p.F;DF=p.DF
T=dict(records=0,displayed_curves=0,whole_operation_banks=0,evidence_banks=0,rendered_sidecars=0,displayed_solution_equalities=0,source_prompts=0,source_solutions=0,source_asset_values=0,present_source_keys=0,missing_source_keys=0,empirical_source_options=4,root_original_choices_visually_reviewed=55,root_original_solution_plots_visually_reviewed=11,root_generated_banks_visually_reviewed=6)
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']};tasks={l:set() for l in ('easy','moderate','hard')}
def ex(z):return s.sympify(z,locals={'x':X})
def forcing(prompt):
 eq=next(z for z in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S) if '=' in z);left,right=eq.split('=',1);res=s.expand(p.expression(left)-p.expression(right));coef=res.coeff(DF);assert coef!=0 and not coef.has(F,DF,C);G=s.cancel(-(res-coef*DF)/coef);assert not G.has(F,DF,C);return G
def check(r):
 q=r['question'];meta=r['generation'];G=forcing(q[':question/problem'].replace('?',''));assert meta['evidence_only']==(not meta['eligible_for_learning']);field=q[':question/answer-fields'][-1];paths=[a[':answer/value'] for a in field[':answer-field/choices']];banks=[]
 for path in paths:
  if Path(path).is_absolute():
   png=Path(path);payload=json.loads(png.with_suffix('.json').read_text());assert png.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n';spec=payload['spec'];assert spec==meta['plot_geometry'][path] and spec['curves']==meta['curves'][path];T['rendered_sidecars']+=1
   if meta['domain']=='x>0':assert all(v is not None and v>=0 for v in spec['domain_minima'])
  else:assert meta['evidence_only'];spec=meta['plot_geometry'][path]
  curves=[ex(v) for v in spec['curves']];assert len(curves)==3;assert len(spec['colors'])==3;banks.append(curves);T['displayed_curves']+=3
 eligible=[all(s.simplify(s.diff(v,X)-G)==0 for v in vs) for vs in banks];assert sum(eligible)==1;assert eligible[next(i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1])]
 if not meta['evidence_only']:
  family=meta['parameters']['family'];a=s.Rational(meta['parameters']['a']);h=s.Rational(meta['parameters']['h']);k=s.Rational(meta['parameters']['k']);u=X-h
  if family=='linear':base=a*X;expected=[base,-base,2*base,base/2,(a+s.sign(a))*X]
  elif family=='logarithmic':base=a*s.log(X);expected=[base,-base,a/X,a*X,a*s.sqrt(X)]
  elif family=='reciprocal':base=a/X;expected=[base,-base,a*X,a*X**2,-a*s.sqrt(X)]
  elif family=='quadratic':base=a*u**2;expected=[base,-base,s.diff(base,X),a*u**3,base.subs(X,X+1)]
  elif family=='cubic':
   base=a*u**3;expected=[base,-base,2*base,base/2,base.subs(X,X+1)] if q[':question/difficulty'].endswith('/hard') else [base,-base,s.diff(base,X),-s.diff(base,X),base.subs(X,X+1)]
  elif family=='exponential':base=a*s.exp(k*X);expected=[base,-base,s.diff(base,X),base.subs(X,-X),base/k]
  else:raise AssertionError(family)
  assert s.simplify(s.diff(base,X)-G)==0
  for vs in banks:assert all(s.simplify(s.diff(v-vs[0],X))==0 for v in vs[1:]);assert all(s.simplify(v-vs[0])==j for v,j in zip(vs,(0,2,4)))
  actual=[s.diff(vs[0],X) for vs in banks];want=[s.diff(v,X) for v in expected];assert all(sum(s.simplify(v-w)==0 for w in want)==1 for v in actual);T['whole_operation_banks']+=1;tasks[q[':question/difficulty'].split('/')[-1]].add(s.srepr(G)+'|'+meta['domain'])
 else:T['evidence_banks']+=1
 primitive=sum(s.integrate(v,X) for v in s.Add.make_args(s.expand(G)))
 for block in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
  prev=None
  for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
   left,right=row.split('=',1);right=right.split(',\\,x>0')[0];aa=p.expression(left) if p.normalize(left) else prev;bb=p.expression(right);assert aa is not None
   if aa.has(DF) or bb.has(DF):assert s.simplify((aa-bb).subs(DF,G))==0
   else:assert s.simplify(p.derivative((aa-bb).subs(F,primitive)))==0,(meta,row,aa,bb,G)
   prev=bb;T['displayed_solution_equalities']+=1
 # Plot-label constants must be the actual sampled constants in both prose and
 # sidecar curve offsets; source plot color order may differ but remains replayed.
 assert 'C='+','.join(meta['parameters']['constants']) in q[':question/worked-solution']
 T['records']+=1;return q
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['template']];assert q[':question/problem']==old[':question/problem'];assert q[':question/worked-solution']==old[':question/worked-solution'];T['source_prompts']+=1;T['source_solutions']+=1;assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
 for f,of in zip(q[':question/answer-fields'],old[':question/answer-fields']):
  assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);T['source_asset_values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];T['present_source_keys']+=1
  else:T['missing_source_keys']+=1
for r in json.loads((D/'review.json').read_text()):check(r)
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
T['meaningful_printed_tasks']={l:len(v) for l,v in tasks.items()};assert min(T['meaningful_printed_tasks'].values())>=6;T['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(T,indent=2)+'\n');print(T)

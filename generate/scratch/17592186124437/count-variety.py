from pathlib import Path
import importlib.util,itertools,json
import sympy as s
D=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
domains={
'linear':{'x':[-3,-2,-1,1,2,3],'y':[-4,-3,-2,1,2,3,4],'a':range(2,7)},
'polynomial':{'x':[-3,-2,-1,1,2,3],'y':[-4,-3,-2,1,2,3,4],'a':range(2,7),'b':range(2,7)},
'monomial':{'x':[-3,-2,-1,1,2,3],'y':[-4,-3,-2,1,2,3,4],'a':range(2,7)},
'sin_product':{'x':[k*s.pi/2 for k in (-3,-1,1,3)],'y':[-4,-3,-2,2,3,4]},
'cos_sum':{'x':[k*s.pi/2 for k in (-3,-1,1,3)],'y':[0,s.pi,2*s.pi]},
'rational_radical':{'x':[1,4,9],'y':[-4,-3,-2,2,3,4]},
'log_exp':{'x':[s.E,s.E**2,s.E**3],'y':[1,2,3]},
'exp_cos':{'x':[-3,-2,-1,1,2,3],'y':[s.pi,-s.pi,2*s.pi]},
'base_exp':{'x':[0],'y':[1,2,3],'a':[2,3,4]},
'canonical_rational':{'x':[-3,-2,2,3],'y':[-4,-3,3,4],'a':[2,3,4,5]},
'canonical_trig':{'x':[-3,-2,2,3],'y':[-4,-3,3,4],'a':[2,3,4,5],'b':[2,3,4]},
}
counts={}
for t in g.TEMPLATES:
 if t=='cos_shift':tasks=[{'x':X,'y':Y} for X in [-3,-2,-1,1,2,3] for Y in [0,s.pi/(2*X),s.pi/X]]
 elif t=='radical_ratio':tasks=[dict(zip(('x','y'),v)) for v in [(3,2),(-3,2),(3,-2),(-3,-2),(6,4),(-6,4),(6,-4),(-6,-4)]]
 else:
  dom=domains[t];tasks=[dict(zip(dom,v)) for v in itertools.product(*dom.values())]
 ok=set()
 for item in tasks:
  pa={k:g.val(v) for k,v in g.CONFIG[t][3].items()};pa.update({k:g.val(v) for k,v in item.items()})
  try:g.guards(t,pa)
  except ValueError:continue
  d,parts,answer,wrong,hist=g.math_data(t,pa);opts=[answer]+wrong
  if any(s.simplify(v-w)==0 for i,v in enumerate(opts) for w in opts[:i]):continue
  ok.add((s.srepr(d),s.srepr(pa['x']),s.srepr(pa['y']),g.CONFIG[t][1]))
 counts[t]={'eligible_mathematical_tasks_in_default_domain':len(ok),'candidate_tasks':len(tasks),'exclude':'ancillary z, option order, blank/radio and profile aliases'}
 print(t,len(ok),flush=True)
(D/'variety.json').write_text(json.dumps(counts,indent=2)+'\n')

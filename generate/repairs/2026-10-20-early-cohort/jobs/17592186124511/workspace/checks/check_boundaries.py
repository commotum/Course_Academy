"""Supported domains and independently checked parameter coverage."""
import importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('content',ROOT/'checks/check_content.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
rows=json.loads((ROOT/'evidence/probe-records.json').read_text());coverage={}
for t in g.TEMPLATES:
 params=[r['generation']['parameters'] for r in rows if r['generation']['template']==t];kind,n,k=g.SPEC[t]
 sizes=sorted({p['n'] for p in params});c={'dimensions':sizes}
 if kind in ('det','rank','col'):assert sizes==list(range(3,8)),(t,sizes)
 if kind=='det':
  c['determinants']=sorted({p['det'] for p in params});assert 0 in c['determinants'] and any(x!=0 for x in c['determinants'])
 if kind in ('vector','nullspace'):
  c['coefficients']=sorted({x for p in params for row in p['matrix'] for x in row})
  c['coordinate_supports']=sorted({str([i for i,row in enumerate(p['matrix']) if any(row)]) for p in params})
 coverage[t]=c
bad=[]
for t in ('q-141199','q-142358'):
 r=g.generate(template=t);p=r['generation']['parameters'];p['matrix']=[[0]*len(row) for row in p['matrix']];bad.append((t,p,'zero/nonindependent given'))
p=g.generate(template='q-141200')['generation']['parameters'];p['det']=5;bad.append(('q-141200',p,'determinant outside declared bounds'))
p=g.generate(template='q-141201')['generation']['parameters'];p['n']=2;bad.append(('q-141201',p,'dimension outside declared bounds'))
for t,p,purpose in bad:
 try:g.generate(template=t,parameters=p)
 except (ValueError,AssertionError):pass
 else:raise AssertionError(purpose)
for t in g.EXCLUDED:
 try:g.generate(template=t)
 except ValueError:pass
 else:raise AssertionError(t)
v.save('boundaries.json',{'passed':True,'coverage':coverage,'invalid_parameter_rejections':[purpose for t,p,purpose in bad],'source_exclusions':g.EXCLUDED})
print(f'Boundary checks passed: scalar dimensions 3–7 in all profiles, both determinant cases, four invalid-parameter rejections, {len(g.EXCLUDED)} evidence exclusions.')

"""Root recovers A's radius/angle from actual prompts and reads every stage."""
import importlib.util,json,re,hashlib,subprocess
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186092219
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','other_point_p');H=load(R/'qa-vector-line-stages.py','other_point_source');g=load(ROOT/f'generate/scratch/{K}.py','other_point_g')
def read(v,env=None):
 v=v.strip().strip('$').rstrip('.,').replace(r'{\theta }_{R}','k').replace(r'\theta','v').replace('θ','v').replace(r'\dfrac',r'\frac');v=re.sub(r'(?<![A-Za-z])r(?![A-Za-z])','u',v);out=p.scalar(v);return out.subs(env) if env else out
def pair(raw,env=None):
 raw=raw.replace(r'\left','').replace(r'\right','').strip().strip('$').rstrip('.');assert raw[0]=='(' and raw[-1]==')';parts=raw[1:-1].split(',');assert len(parts)==2;return tuple(read(v,env) for v in parts)
def same(a,b):return s.simplify(a-b)==0
def physics(prompt):
 ap=re.search(r'point \$A\$ has polar coordinates \$(.*?)\$',prompt)[1];bp=re.search(r'point \$B\$ has polar coordinates \$(.*?)\$',prompt)[1];ac=re.search(r'Cartesian coordinates of \$A\$ are \$(.*?)\$',prompt)[1];ax,ay=pair(ac);ar=s.sqrt(ax*ax+ay*ay);theta=s.atan2(ay,ax)
 if theta<0:theta+=2*s.pi
 radius,angle=pair(ap);env={p.u:ar,p.v:theta,p.x:ax,p.y:ay,p.k:s.atan(abs(ay/ax)) if ax else s.pi/2};assert same(radius.subs(env),ar) and same(s.cos(angle.subs(env)),ax/ar) and same(s.sin(angle.subs(env)),ay/ar)
 br,ba=pair(bp,env);assert br.is_positive;xy=(s.simplify(br*s.cos(ba)),s.simplify(br*s.sin(ba)));return env,br,ba,xy
source=H.source(g,K);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
source_key_checks=0
for original in g.Q.values():
 _,_,_,expected=physics(original[':question/problem'])
 for f in original[':question/answer-fields']:
  correct=f.get(':answer-field/correct')
  if correct is None:continue
  if f[':answer-field/type'][':db/ident'].endswith('/radio'):assert pair(correct[':answer/value'])==expected
  else:assert read(correct[':answer/value'])==expected[0 if f[':answer-field/key']=='field-1' else 1]
  source_key_checks+=1
# Include every observed normal family even if a random batch misses one.
for sid,spec in g.SPEC.items():records.append(g.generate(spec[-1],seed=73,template=sid))
counts=dict(records=0,radius_reference_equalities=0,converted_polar_pairs=0,coordinate_equalities=0,tuple_conclusions=0,choices=0,blank_components=0);native=[]
for rec in records:
 q=rec['question'];env,br,ba,xy=physics(q[':question/problem']);sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(aligned)==3
 first=aligned[0];lhs=None
 for row in first.split(r'\\'):
  a,b=row.replace('&','').split('=',1);lhs=a.strip() or lhs;assert same(read(lhs,env),read(b,env));counts['radius_reference_equalities']+=1
 coords=re.search(r'polar coordinates of \$B\$ are\s*\$\$(.*?)\$\$',sol,re.S) or re.search(r'polar coordinates of \$B\$ are\s*\$([^$]+)\$',sol);assert coords
 for part in coords[1].strip().rstrip('.').split('='):
  pr,pa=pair(part,env);assert same(pr,br) and same(s.sin(pa),s.sin(ba)) and same(s.cos(pa),s.cos(ba));counts['converted_polar_pairs']+=1
 b_env=env|{p.u:br,p.v:ba,p.x:xy[0],p.y:xy[1]}
 for ix,block in enumerate(aligned[1:]):
  lhs=None
  for row in block.split(r'\\'):
   a,b=row.replace('&','').split('=',1);lhs=a.strip() or lhs;assert lhs==('x','y')[ix] and same(read(b,b_env),xy[ix]);counts['coordinate_equalities']+=1
 end=re.search(r'Cartesian coordinates of \$B\$ are \$(.*?)\$',sol);assert end and pair(end[1])==xy;counts['tuple_conclusions']+=1
 # Every explicit inferred-quadrant theta in the prose must equal A's angle.
 for angle in re.findall(r'\$\\theta\s*=\s*(.*?)\$',sol):
  for term in angle.split('='):assert same(read(term).subs(env),env[p.v])
 checks=[]
 for fi,f in enumerate(q[':question/answer-fields']):
  if f[':answer-field/type'].endswith('/blank'):
   ix=0 if f[':answer-field/key']=='field-1' else 1;assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'];assert read(f[':answer-field/choices'][0][':answer/value'])==xy[ix];counts['blank_components']+=1
   ratio=(s.cos(ba),s.sin(ba))[ix];checks += [dict(field_index=fi,submitted=s.sstr(br)+'*('+s.sstr(ratio)+')',expected='accepted',purpose='unreduced recovered B radius times trig component'),dict(field_index=fi,submitted=s.sstr(xy[ix]+1),expected='rejected',purpose='wrong component')]
  else:
   values=[pair(v[':answer/value']) for v in f[':answer-field/choices']];ar=env[p.u];aa=env[p.v];x,y=xy
   if rec['generation']['template']=='axis_radius' or pair(re.search(r'point \$A\$ has polar coordinates \$(.*?)\$',q[':question/problem'])[1])[0].has(p.u):
    expected=[xy,(y,x),(s.simplify(ar*s.cos(ba)),s.simplify(ar*s.sin(ba))),(-x,y),(x,-y)]
   elif s.simplify((ba-aa)/s.pi)%2==1:
    expected=[xy,(s.simplify(br*s.cos(aa)),s.simplify(br*s.sin(aa))),(s.simplify(ar*s.cos(ba)),s.simplify(ar*s.sin(ba))),(-x,y),(x,-y)]
   else:expected=[xy,(s.simplify(br*s.cos(aa)),s.simplify(br*s.sin(aa))),(s.simplify(br*s.cos(2*aa-ba)),s.simplify(br*s.sin(2*aa-ba))),(-x,-y),(y,x)]
   assert set(values)==set(expected) and len(set(values))==5,(rec['generation']['template'],values,expected)
   for v,a in zip(values,f[':answer-field/choices']):assert (v==xy)==(a[':answer/id']==f[':answer-field/correct'][1]);counts['choices']+=1
 if checks:native.append(dict(label=q[':question/id'],record=rec,checks=checks))
 counts['records']+=1
ip=R/f'qa/{K}-root-equivalent-input.json';op=R/f'qa/{K}-root-equivalent-report.json';ip.write_text(json.dumps(native,indent=2)+'\n');subprocess.run([str(R/'check-engine'),str(ip),str(op)],check=True)
report=dict(status='passed',kp_id=K,source=source,source_correct_designations_independently_derived=source_key_checks,readback=counts,native_typed_equivalents=str(op),script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

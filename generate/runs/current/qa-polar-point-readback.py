"""Root reads displayed polar tuples, both components and every solution row."""
import importlib.util,json,re,hashlib,subprocess,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','polar_parent_parser');H=load(R/'qa-sinusoidal-properties.py','polar_source_checks')
def read(z,env=None):
 z=z.strip().strip('$').rstrip('.,').replace(r'\theta','v')
 z=re.sub(r'\{?(-?\d+)\}?\^\{∘\}',lambda m:'('+m[1]+'*pi/180)',z)
 z=re.sub(r'(?<![A-Za-z])r(?![A-Za-z])','u',z)
 out=p.scalar(z)
 return out.subs(env) if env else out
def pair(z):
 z=z.strip().strip('$').rstrip('.').strip('()');parts=z.split(',');assert len(parts)==2;return tuple(read(x) for x in parts)
def physics(prompt):
 m=re.search(r'polar coordinates \$\((.*?),(.*?)\)',prompt)
 if m:radius=read(m[1]);theta=read(m[2])
 else:
  radius=read(re.search(r'to the origin is \$(.*?)\$',prompt)[1]);theta=read(re.search(r'makes an angle of \$(.*?)\$',prompt)[1]);assert 'positive $x$-axis' in prompt
 assert radius.is_positive and 0<=theta<2*s.pi
 c=s.cos(theta);d=s.sin(theta);xy=(s.simplify(radius*c),s.simplify(radius*d))
 return radius,theta,c,d,xy

def main(k=17592186092217):
 g=load(ROOT/f'generate/scratch/{k}.py','polar_gen');src=H.source(g,k)
 records=json.loads((R/f'qa/{k}-sampled.json').read_text())
 if k==17592186092218:
  records += [g.generate(level,100+idx,template=template) for level,templates in g.FAMILIES.items() for idx,template in enumerate(templates)]
 n=dict(records=0,coordinate_components=0,full_radio_options=0,solution_equalities=0,tuple_conclusions=0)
 native=[];families=set()
 for r in records:
  q=r['question'];radius,theta,c,d,xy=physics(q[':question/problem']);env={p.u:radius,p.v:theta,p.x:xy[0],p.y:xy[1]};families.add((r['generation']['level'],r['generation']['template']));n['records']+=1
  fields=q[':question/answer-fields'];checks=[]
  for ix,f in enumerate(fields):
   choices=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
   if f[':answer-field/type'].endswith('/radio'):
    vals=[pair(a[':answer/value']) for a in choices];expected=[xy,(-xy[0],xy[1]),(xy[0],-xy[1]),(-xy[0],-xy[1]),(c,d)]
    profile=r['generation']['profile']
    if k==17592186092218:
     X,Y=xy
     if radius==1:expected=[xy,(-X,Y),(X,-Y),(-X,-Y),(Y,X) if X!=Y and X!=-Y else (2*X,2*Y)]
     elif profile=='source-sign-root':expected=[(-X,-Y),(X,-Y),(X,-radius*s.sqrt(3)/2),(-X,Y),xy]
     elif profile=='source-sign-half':expected=[(-X,Y),(X,-Y/2),(-X,-Y/2),xy,(-X,-Y)]
     elif profile=='source-axis-down':expected=[(0,radius),(0,1),(0,-radius),(radius,0),(-radius,0)]
     elif profile=='source-axis-right':expected=[(0,radius),(radius,1),(radius,0),(1,0),(-radius,0)]
    assert set(vals)==set(expected) and len(set(vals))==5
    for a,v in zip(choices,vals):assert (v==xy)==(a[':answer/id']==correct);n['full_radio_options']+=1
   else:
    coord=0 if f[':answer-field/key']=='field-1' else 1;assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'];assert len(choices)==1 and read(choices[0][':answer/value'])==xy[coord];n['coordinate_components']+=1
    # Retain the actual radius-times-unit-circle product as a typed equivalent,
    # rather than simplifying it back to the stored canonical expression.
    equivalent=s.sstr(radius)+'*('+s.sstr((c,d)[coord])+')'
    checks.extend([dict(field_index=ix,submitted=equivalent,expected='accepted',purpose='unreduced radius times unit-circle component'),dict(field_index=ix,submitted=s.sstr(xy[coord]+1),expected='rejected',purpose='wrong coordinate')])
  if checks:native.append(dict(label=q[':question/id'],record=r,checks=checks))
  sol=q[':question/worked-solution'];assert 'First, we calculate the $x$-coordinate' in sol and re.search(r'Then,? we calculate the \$y\$-coordinate',sol)
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
  generic=next(block for block in blocks if block.strip().startswith('x=r'))
  if k==17592186092218:
   interpreted=blocks[0].strip();rs,ts=interpreted.split(r'\,');assert rs.strip().startswith('r=') and ts.strip().startswith(r'\theta =')
   assert read(rs.split('=',1)[1].rstrip(','))==radius and read(ts.split('=',1)[1])==theta;n['solution_equalities']+=2
  for eq in generic.split(r'\,'):
   eq=eq.strip().rstrip(',');a,b=eq.split('=');assert s.simplify(read(a,env)-read(b,env))==0;n['solution_equalities']+=1
  aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(aligned)==2
  for coordinate,block in enumerate(aligned):
   rows=block.split(r'\\');assert len(rows)==4
   lhs=None
   for row in rows:
    left,right=row.replace('&','').split('=');lhs=left.strip() or lhs;assert lhs==('x','y')[coordinate];assert s.simplify(read(right,env)-xy[coordinate])==0;n['solution_equalities']+=1
  end=re.search(r'Cartesian coordinates of \$P\$ are \$(.*?)\$',sol);assert end and pair(end[1])==xy;n['tuple_conclusions']+=1
 ip=R/f'qa/{k}-root-equivalent-input.json';op=R/f'qa/{k}-root-equivalent-report.json';ip.write_text(json.dumps(native,indent=2)+'\n');subprocess.run([str(R/'check-engine'),str(ip),str(op)],check=True)
 report=dict(status='passed',kp_id=k,source=src,readback=n,families=sorted(families),native_equivalents=str(op),script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest())
 (R/f'qa/{k}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 17592186092217)

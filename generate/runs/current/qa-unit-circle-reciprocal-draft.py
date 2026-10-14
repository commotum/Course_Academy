"""Root reads actual reciprocal identities, every scalar relation and calibrated rasters."""
import hashlib,importlib.util,itertools,json,math,re,sys
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186110756;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
G=mod('root_recip_generator',D.with_suffix('.py'));P=mod('root_recip_scalar',R/'ode-scalar-parser.py');F=mod('root_recip_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
C=dict(records=0,actual_given_coordinates=0,displayed_relations=0,inline_substitutions=0,positive_branch_assertions=0,values=0,bank_pairs=0,complete_method_banks=0,scope_checks=0,raster_markers=0,raster_circle_probes=0,raster_rays=0,raster_wedges=0,prose_masks=0)
def scalar(v,x,y):
 z=P.scalar(v.strip().rstrip('.,').replace(r'\pm','').replace(r'\theta','t').replace('θ','t'))
 z=z.subs({s.sec(P.t):1/x,s.csc(P.t):1/y,s.sin(P.t):y,s.cos(P.t):x,P.x:x,P.y:y});assert not z.free_symbols;return s.simplify(z)
def mask(v):
 v=re.sub(r'!\[.*?\]\(.*?\)','@IMAGE@',v);v=re.sub(r'\$\$.*?\$\$','@DISPLAY@',v,flags=re.S);return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',v)).strip()
def near(im,x,y,predicate,radius=3):
 return any(predicate(im.getpixel((xx,yy))) for xx in range(max(0,round(x)-radius),min(im.width,round(x)+radius+1)) for yy in range(max(0,round(y)-radius),min(im.height,round(y)+radius+1)))
blue=lambda p:p[2]>p[0]+50 and p[2]>p[1]+20
black=lambda p:max(p[:3])<70
orange=lambda p:p[0]>180 and p[1]>90 and p[2]<60

def check(r,raw=False):
 q,m=r['question'],r['generation'];prompt=q[':question/problem'];mt=re.search(r'\$(x|y)\$-coordinate .*? is \$(.*?)\$',prompt);assert mt;axis,given=mt.groups();known=P.scalar(given.strip().rstrip('.,'));assert not known.free_symbols and 0<known<1;missing=s.sqrt(1-known*known);x,y=(missing,known) if axis=='y' else (known,missing)
 target=re.search(r'find \$(.*?)\$',prompt,re.I)[1];assert ('sec' in target if axis=='y' else 'csc' in target);answer=scalar(target,x,y);assert answer==(1/x if axis=='y' else 1/y);C['actual_given_coordinates']+=1
 if not raw:
  assert m['eligible_for_learning'] and not m.get('diagnostic_only');level=q[':question/difficulty'].split('/')[-1];a,n=known.as_coeff_Mul();n=s.simplify(n*n);b=math.isqrt(int((known*known).as_numer_denom()[1]));coefficient=s.simplify(a*b)
  # Recovered primitive parameter data are checked against actual printed values;
  # unlike the coordinate KP, source-shaped square rows retain unsimplified b².
  pb=m['parameters']['b'];pr=m['parameters']['r'];assert known==s.sqrt(pr)/pb and math.gcd(int(s.sqrt(pr).as_coeff_Mul()[0]),pb)==1 and .14<=float(known)<=.97
  inputcoef,inputrad=s.sqrt(pr).as_coeff_Mul();inputrad=s.simplify(inputrad**2)
  if level=='easy':assert missing.is_Rational and inputrad<=15
  elif level=='moderate':assert not missing.is_Rational and inputcoef==1 and inputrad<=15
  else:assert not missing.is_Rational and 1<inputcoef<=4 and 1<inputrad<=15
  C['scope_checks']+=1
  for role,asset in m['assets'].items():
   path=Path(asset['path']);assert hashlib.sha256(path.read_bytes()).hexdigest()==asset['sha256'];assert list(map(s.sympify,asset['point']))==[x,y]
   im=Image.open(path).convert('RGB');assert im.size==(585,585)
   coords=[(xx,yy) for yy in range(im.height) for xx in range(im.width) if blue(im.getpixel((xx,yy)))];assert coords
   xmin,xmax=min(a for a,b in coords),max(a for a,b in coords);ymin,ymax=min(b for a,b in coords),max(b for a,b in coords);cx=(xmin+xmax)/2;cy=(ymin+ymax)/2;rx=(xmax-xmin)/2;ry=(ymax-ymin)/2;assert abs(rx-ry)<=1 and near(im,cx,cy,black)
   assert near(im,cx+rx*float(x),cy-ry*float(y),black);C['raster_markers']+=1
   for angle in (30,60,120,150,210,240,300,330):
    theta=math.radians(angle);assert near(im,cx+rx*math.cos(theta),cy-ry*math.sin(theta),blue,4);C['raster_circle_probes']+=1
   assert near(im,cx+rx*.72*float(x),cy-ry*.72*float(y),black);C['raster_rays']+=1
   theta=math.atan2(float(y),float(x))/2;assert near(im,cx+rx*.22*math.cos(theta),cy-ry*.22*math.sin(theta),orange,2);C['raster_wedges']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks) in (5,6)
  for block in blocks:
   block=block.strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
   active=None
   for row in block.split(chr(92)*2):
    # The first coordinate-identification display contains a comma-separated pair.
    for relation in re.split(r',\s*(?:\\,)?\s*(?=y=)',row):
     chain=[z.replace('&','').strip() for z in relation.split('=')];assert len(chain)>=2
     left=active if not chain[0] else None
     for z in chain:
      if not z:continue
      val=scalar(z,x,y)
      if left is None:left=val;active=val
      else:assert s.simplify(val-left)==0,(m['template'],row,val,left);C['displayed_relations']+=1
  # Every inline substitution, reciprocal definition and signed chosen conclusion
  # is read independently, including repeated final math outside displays.
  for token in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S):
   if '=' in token:
    lhs,rhs=token.split('=');assert s.simplify(scalar(lhs,x,y)-scalar(rhs,x,y))==0;C['inline_substitutions']+=1
  assert 'positive' in sol and 'first quadrant' in sol;C['positive_branch_assertions']+=1
  old=originals[m['template']]
  if ':question/worked-solution' not in old:old=originals['q-124750']
  if not raw and missing.is_Rational:old=originals['q-124750' if axis=='y' else 'q-124743'];oldtext=old[':question/worked-solution'].split('\n\nFinally, we rationalize')[0]
  else:oldtext=old[':question/worked-solution']
  assert mask(sol)==mask(oldtext);C['prose_masks']+=1
 f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value'],x,y) for a in f[':answer-field/choices']];assert len(vals)==5 and all(v.is_real and v.is_finite for v in vals) and sum(s.simplify(v-answer)==0 for v in vals)==1
 for v,w in itertools.combinations(vals,2):assert s.simplify(v-w)!=0;C['bank_pairs']+=1
 if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if s.simplify(v-answer)==0]==[f[':answer-field/correct'][1]]
 if not raw:
  profile=m['bank_profile'];expected=[answer,missing,1/known,1/(1-known*known),known/missing] if profile=='method-reciprocal' else [answer,-answer,missing,1/known,1/(1-known*known)];assert profile in ('method-reciprocal','method-sign') and all(sum(s.simplify(v-e)==0 for v in vals)==1 for e in expected);C['complete_method_banks']+=1
 C['values']+=5;C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c.get('level','moderate'),template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile'))),True)
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

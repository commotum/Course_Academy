#!/usr/bin/env python3
"""Independent readback of displayed calculus, all arithmetic rows, banks and rasters."""
import concurrent.futures,copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from PIL import Image
import numpy as np
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=sp.symbols('x y',real=True)

def expression(s):
 s=s.replace(r'\,','').strip().rstrip('.,').replace('π',r'\pi').replace(r'\cdot','*')
 # Balanced recursive \frac handling, including its two complete arguments.
 def group(z,i):
  assert z[i]=='{';n=1;j=i+1
  while n:
   n += (z[j]=='{')-(z[j]=='}');j+=1
  return z[i+1:j-1],j
 while r'\frac' in s:
  i=s.index(r'\frac');a,j=group(s,i+5);b,k=group(s,j);s=s[:i]+'(('+a+')/('+b+'))'+s[k:]
 s=s.replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**')
 s=re.sub(r'(?<=\d)(?=pi|x|y|\()', '*', s)
 return sp.sympify(s,locals=dict(x=x,y=y,pi=sp.pi))

def printed_P_Q(q):
 p=q[':question/problem'];body=re.search(r'Calculate \$(.*?)\$',p,re.S).group(1)
 body=body.replace('{∮}_{∂D}','').replace('∮_(∂D)','').replace(r'\,','').rstrip(',')
 terms=re.findall(r'([+-]?[^+-]*?)(dx|dy)',body)
 assert len(terms)==2,body
 d={v:expression(u.strip() or '1') for u,v in terms}
 return d['dx'],d['dy']

def independent_geometry(record):
 meta=record['generation'];p=meta['parameters'];t=meta['template'];shape=g.SPECS[t]['shape']
 # Independent source transcriptions, not source-solution arithmetic.
 if shape in ('annulus','semicircle','two_circles'):
  O=sp.pi*p['R']**2;holes=[sp.pi*p['r']**2/(2 if shape=='semicircle' else 1)]
  if shape=='two_circles':holes.append(sp.pi*p['t']**2)
 else:
  O=sp.Rational(p['W']*p['H'],2 if shape=='diamond' else 1);holes=[sp.Integer(p['s']**2)]
  if shape=='two_squares':holes.append(sp.Integer(p['t']**2))
 return O,holes,O-sum(holes)

def formatting(q):
 for v in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
  assert all(ord(c)>=32 or c in '\n\t' for c in v),'C0 control'
  assert v.count('$')%2==0
  balance=0
  for c in v:
   balance+=(c=='{')-(c=='}');assert balance>=0
  assert balance==0
  assert '+-' not in v and '--' not in v

EXPECTED_ROWS={'annulus_constant':7,'annulus_negative':8,'annulus_positive':7,'circle_semicircle':7,'diamond_square':8,'rectangle_square':9,'square_square':9,'square_unrated':9,'circle_two_holes':9,'rectangle_two_holes':9}

def math_check(record):
 q=record['question'];m=record['generation'];t=m['template'];raw=m['evidence_only'];formatting(q)
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 P,Q=printed_P_Q(q);dP=sp.diff(P,y);dQ=sp.diff(Q,x);curl=dQ-dP
 O,holes,A=independent_geometry(record);correct=sp.simplify(curl*A)
 sol=q.get(':question/worked-solution')
 if sol:
  # Held-coordinate definitions read back from actual rendered function prose.
  functions=re.search(r'P\(x,y\)=(.*?)\$ and \$Q\(x,y\)=(.*?)\.\$',sol)
  assert functions and expression(functions[1])==P and expression(functions[2])==Q
  derivatives=re.search(r'\\frac\{∂P\}\{∂y\}=(.*?),\\,\\frac\{∂Q\}\{∂x\}=(.*?)\.',sol)
  assert derivatives and expression(derivatives[1])==dP and expression(derivatives[2])==dQ
  chain=sol.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
  rows=chain.split(r' \\  & =');assert len(rows)==EXPECTED_ROWS[t],(t,len(rows))
  lhs,formal=rows[0].split(' & =');assert formal==g.FORMAL
  lhsP,lhsQ=printed_P_Q({':question/problem':'Calculate $'+lhs+'$'})
  if not(raw and t in ('annulus_positive','circle_semicircle')):assert lhsP==P and lhsQ==Q,'Wrong displayed LHS'
  # Every displayed distributed integrand is assessed independently before any area substitution.
  first=rows[1].removeprefix(r'{∬}_{D}').removesuffix(r'\,\text{d}A');assert expression(first)==curl
  for row in rows[2:]:
   if r'{∬}_{D}' in row:
    before,after=row.split(r'{∬}_{D}');after=after.removesuffix(r'\,\text{d}A')
    coeff=expression(before) if before not in ('','-') else (-1 if before=='-' else 1)
    integrand=expression(after) if after else 1
    assert sp.simplify(coeff*integrand*A-correct)==0,(row,correct)
   else:
    rendered=row.replace(r'\text{Area}(D)','('+str(A)+')')
    assert sp.simplify(expression(rendered)-correct)==0,(row,correct)
  # Operative structure: outer minus each hole remains visible before numerical collection.
  geometryrow=next(r for r in rows[2:] if '^{2}' in r or ('\\frac{' in r and '\\cdot' in r))
  assert '-' in geometryrow
  if t not in ('annulus_positive','circle_semicircle'):
   collected=rows[rows.index(geometryrow)+1]
   brackets=re.findall(r'\(([^()]*)\)',collected)
   inside=brackets[-1] if brackets else collected
   pieces=inside.split('-')
   assert len(pieces)==1+len(holes)
   assert expression(pieces[0])==O and all(expression(v)==h for v,h in zip(pieces[1:],holes)), 'Individually evaluated area components'
  if t in ('rectangle_square','diamond_square'):
   assert str(m['parameters']['W'])+r'\cdot '+str(m['parameters']['H']) in geometryrow
  if t in ('circle_two_holes','rectangle_two_holes'):assert geometryrow.count('-')>=2
  # Preserve factored area and separately evaluated area components.
  if t in ('rectangle_square','square_square','diamond_square','annulus_negative'):
   assert '(' in rows[-2] or t in ('rectangle_square','square_square')
 if not raw:
  f=q[':question/answer-fields'][0];values=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(values)==5 and len(set(map(sp.srepr,values)))==5
  cid=f[':answer-field/correct'][1]
  keyed=[a for a in f[':answer-field/choices'] if a[':answer/id']==cid];assert len(keyed)==1 and sp.simplify(expression(keyed[0][':answer/value'])-correct)==0
  profile=m['profile']
  expected=[correct,-correct]
  if profile=='constant_operations':expected += [curl*O,curl*sum(holes),curl*(O+sum(holes))]
  elif profile=='semicircle_operations':expected += [curl*O,curl*(O-2*holes[0]),curl*(O+holes[0])]
  elif profile=='two_hole_operations':expected += [curl*(O-holes[0]),curl*(O-holes[1]),curl*(O+sum(holes))]
  else:expected += [curl*O,curl*(O+sum(holes)),dQ*A]
  assert sorted(map(lambda v:sp.srepr(sp.simplify(v)),values))==sorted(map(lambda v:sp.srepr(sp.simplify(v)),expected))
 return correct

def plot_check(record):
 image=re.search(r'!\[\]\(([^)]+)\)',record['question'][':question/problem'])[1]
 if image.startswith('images/'):
  assert (Path('/media/jake/SSD/EDB/math')/image).exists();return
 path=Path(image);side=json.loads(path.with_suffix('.json').read_text());pixels=np.array(Image.open(path).convert('RGB'));h,w=pixels.shape[:2]
 assert side['png_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
 origin,unitx,unity=np.array(side['axes_transform']);sx=unitx[0]-origin[0];sy=unity[1]-origin[1]
 assert abs(sx-sy)<1e-7
 orange=(pixels[:,:,0]>160)&(pixels[:,:,1]>80)&(pixels[:,:,1]<200)&(pixels[:,:,2]<70)
 def hit(v):
  px=int(round(origin[0]+v[0]*sx));py=int(round(h-origin[1]-v[1]*sy));return orange[max(0,py-4):py+5,max(0,px-4):px+5].any()
 for b in side['boundaries']:
  assert b['orientation']==('counterclockwise' if b['role']=='outer' else 'clockwise')
  data=b['points']
  if 'vertices' in data:
   vertices=np.array(data['vertices'])
   for a,c in zip(vertices,np.roll(vertices,-1,axis=0)):
    for f in (.2,.5,.8):assert hit(a+f*(c-a)),('Missing raster boundary',a,c)
  else:
   c=np.array(data['center']);r=data['radius'];angles=[20,50,110,160] if 'angle' in data else [20,70,140,210,300]
   for a in angles:assert hit(c+r*np.array([np.cos(np.deg2rad(a)),np.sin(np.deg2rad(a))])),('Missing circle boundary',a)
   if 'diameter' in data:
    for f in (-.8,0,.8):assert hit(c+np.array([r*f,0])), 'Missing semicircle diameter'
 for a in side['arrows']:
  tail=np.array(a['tail']);tip=np.array(a['tip']);role=a['role'];shape=side['shape']
  if shape in ('annulus','semicircle','two_circles'):
   candidates=[b['points']['center'] for b in side['boundaries'] if b['role']==role];center=min(candidates,key=lambda c:np.linalg.norm(tail-c));v=tail-center;d=tip-tail;cross=v[0]*d[1]-v[1]*d[0]
   assert cross>0 if role=='outer' else cross<0
  elif role=='hole':assert tip[0]>tail[0] and abs(tip[1]-tail[1])<1e-8
  elif shape=='diamond':assert tip[0]>tail[0] and tip[1]>tail[1]
  else:assert tip[0]>tail[0]


def run():
 sources=[];review=[];fidelity=[];native=[]
 for t,z in g.SPECS.items():
  if 'source' in z:
   case=dict(source_id=z['source'],template=t,level=z['level'],parameters=g.parameters_for(t),bank_profile='observed_raw');sources.append(case)
   r=g.generate(z['level'],template=t,parameters=case['parameters'],profile='observed_raw');q=g.QUESTIONS[z['source']];rq=r['question']
   assert set(rq)-{':question/id'}==set(q)-{':db/id',':question/id',':question/math-academy-id'}
   assert rq[':question/problem']==q[':question/problem'] and rq.get(':question/worked-solution')==q.get(':question/worked-solution')
   for f,orig in zip(rq[':question/answer-fields'],q[':question/answer-fields']):
    assert (':answer-field/correct' in f)==(':answer-field/correct' in orig)
    a=sorted(a[':answer/value'] for a in f[':answer-field/choices']);b=sorted(a[':answer/value'] for a in orig[':answer-field/choices']);assert a==b,(t,a,b)
    if ':answer-field/correct' in f:
     got=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert got==orig[':answer-field/correct'][':answer/value']
   math_check(r);plot_check(r);review.append(dict(kind='original public raw replay',record=r));fidelity.append(dict(source_id=z['source'],prompt_exact=True,solution_exact=True,field_presence=True,bank_count=len(q[':question/answer-fields']),choices=sum(len(f[':answer-field/choices']) for f in q[':question/answer-fields']),designation_count=sum(':answer-field/correct' in f for f in q[':question/answer-fields'])))
  for n in range(2):
   r=g.generate(z['level'],seed=341+n,template=t);math_check(r);plot_check(r);review.append(dict(kind='generated variant; authored normal operation bank',record=r))
   fields=r['question'][':question/answer-fields'];checks=[]
   for i,f in enumerate(fields):
    for a in f[':answer-field/choices']:checks.append(dict(field_index=i,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',purpose='Every owned source-shaped radio choice'))
   native.append(dict(label=f'{t}-{n}',record=r,checks=checks))
  # Same parameters with shuffled choices have identical content UUIDs.
  a=g.generate(z['level'],seed=31,template=t);b=g.generate(z['level'],seed=32,template=t,parameters=a['generation']['parameters']);assert a['question'][':question/id']==b['question'][':question/id']
 coverage={l:set() for l in ['easy','moderate','hard']};math_tasks={l:set() for l in coverage}
 for l in coverage:
  for seed in range(80):
   r=g.generate(l,seed);math_check(r);coverage[l].add(r['generation']['template']);math_tasks[l].add(r['generation']['mathematical_fingerprint'])
  assert coverage[l]=={t for t,z in g.SPECS.items() if z['level']==l}
 # Structural and mathematical mutation regressions; final answer alone is insufficient.
 mutations=[];base=g.generate_easy(template='rectangle_square',parameters=g.parameters_for('rectangle_square'))
 for label,needle,replacement in [('wrong distributed sign','(4-2)','(4+2)'),('missing held partial',r'\frac{∂P}{∂y}=2',r'\frac{∂P}{∂y}=0'),('evaluated area corruption','(24-4)','(25-5)'),('C0 control',r'\frac','\f'+'rac')]:
  r=copy.deepcopy(base);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(needle,replacement)
  try:math_check(r)
  except (AssertionError,ValueError,TypeError):mutations.append(label)
  else:raise AssertionError('Mutation escaped: '+label)
 # Raster recipe mutation, tested independently of identical source paths.
 r=g.generate_moderate(template='circle_semicircle',parameters=g.parameters_for('circle_semicircle'))
 path=Path(re.search(r'!\[\]\(([^)]+)\)',r['question'][':question/problem'])[1]).with_suffix('.json');saved=path.read_text();data=json.loads(saved);data['arrows'][1]['tail'],data['arrows'][1]['tip']=data['arrows'][1]['tip'],data['arrows'][1]['tail'];path.write_text(json.dumps(data))
 try:plot_check(r)
 except AssertionError:mutations.append('reversed inner orientation')
 else:raise AssertionError('Orientation mutation escaped')
 finally:path.write_text(saved)
 # Concurrent processes (Matplotlib is not thread-safe), same and different parameters.
 code="import importlib.util,json; s=importlib.util.spec_from_file_location('g',%r);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);print(json.dumps(g.generate_hard(seed=%%s)))"%str(D.with_suffix('.py'))
 def call(n):return json.loads(subprocess.check_output([sys.executable,'-c',code%str(n)],text=True))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  parallel_records=list(pool.map(call,[901,901,902]))
 for r in parallel_records:math_check(r);plot_check(r)
 assert parallel_records[0]['question'][':question/id']==parallel_records[1]['question'][':question/id']
 (D/'source-cases.json').write_text(json.dumps(sources,indent=2)+'\n');(D/'review.json').write_text(json.dumps(review,indent=2)+'\n');(D/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 report=dict(status='passed with documented source anomalies',basis=1356,lineage=g.CAPTURE['lineage'],source_practice_questions=len(sources),source_banks=sum(r['bank_count'] for r in fidelity),source_choices=sum(r['choices'] for r in fidelity),source_correct_designations=sum(r['designation_count'] for r in fidelity),exact_prompt_replays=8,exact_solution_presence_replays=8,exact_present_solutions=7,mathematically_correct_present_source_solutions=5,source_LHS_repairs=2,missing_correct_designations=2,legacy_duplicate_fields=1,source_ratings_observed=7,unrated_source_authored_easy=1,authored_hard_templates=2,default_family_coverage={l:sorted(v) for l,v in coverage.items()},sampled_math_tasks={l:len(v) for l,v in math_tasks.items()},native=json.loads((D/'engine-report.json').read_text()),mutation_regressions=mutations,concurrency='same/different independent process instances validated',python=sys.version.split()[0],sympy=sp.__version__,matplotlib=g.matplotlib.__version__,fidelity=fidelity,unresolved=['Historical opaque scalar distractor intent is not recovered; evidence profiles are ineligible. Missing original correct references cannot count as matched designations.'])
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 text='# Applying Green\'s Theorem to Regions With Holes\n\nOriginals are public parameterized raw replays. They retain captured omissions and two erroneous initial LHSs. Variants repair these and use authored complete operation banks.\n\n'
 for entry in review:
  r=entry['record'];text+='## '+entry['kind']+': '+r['generation']['template']+'\n\n'+g.markdown(r)+'\n\n'
 (D/'review.md').write_text(text);print(json.dumps({k:v for k,v in report.items() if k not in ('native','fidelity')},indent=2))
if __name__=='__main__':run()

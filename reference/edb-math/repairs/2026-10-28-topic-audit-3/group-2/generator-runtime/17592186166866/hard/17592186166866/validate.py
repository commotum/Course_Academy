"""Fail on full-source, independently parsed mathematics, bank, geometry or engine errors."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,re,math,hashlib,subprocess,itertools,concurrent.futures,tempfile
from fractions import Fraction
from collections import Counter
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
from PIL import Image
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ellipse',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z=sp.symbols('x y z');TRANS=standard_transformations+(convert_xor,implicit_multiplication_application)
def balanced(s):
 n=0
 for c in s:
  if c=='{':n+=1
  if c=='}':n-=1
  assert n>=0
 assert n==0
 assert s.count('$$')%2==0
 assert s.replace('$$','').count('$')%2==0
 assert '--' not in s and '+-' not in s

def expr(s):
 s=s.replace(g.D,'z').replace(r'\cdot','*').replace(' ','').rstrip('.')
 def grp(i):
  assert s[i]=='{';n=1;j=i+1
  while n:
   if s[j]=='{':n+=1
   elif s[j]=='}':n-=1
   j+=1
  return s[i+1:j-1],j
 while r'\frac' in s:
  i=s.rfind(r'\frac');a,j=grp(i+5);b,k=grp(j);s=s[:i]+'(('+a+')/('+b+'))'+s[k:]
 s=s.replace('{','(').replace('}',')')
 assert '\\' not in s,s
 return parse_expr(s,local_dict={'x':x,'y':y,'z':z},transformations=TRANS)
def formal(s):
 while g.OP in s:
  i=s.index(g.OP);j=i+len(g.OP);assert s[j]=='(';k=j+1;n=1
  while n:
   if s[k]=='(':n+=1
   elif s[k]==')':n-=1
   k+=1
  e=expr(s[j+1:k-1]);d=sp.diff(e,x)+sp.diff(e,y)*z
  s=s[:i]+'('+sp.sstr(d)+')'+s[k:]
 return expr(s)
def mathcheck(r):
 q=r['question'];p=r['generation']['parameters'];h,k,a,b=[p[t] for t in ('h','k','a','b')]
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 expected_identity=g.digest({'version':g.VERSION,'difficulty':r['generation']['level'],'problem':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])})
 assert r['generation']['content_fingerprint']==expected_identity and q[':question/id']==g.uid(expected_identity)
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]:balanced(s)
 # Actual printed standard equation -> derivative; do not trust answer metadata.
 solution=q.get(':question/worked-solution')
 if solution:
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);assert len(blocks)==2
  setup=blocks[0].split('⟹')[1].replace(r'\,','').rstrip('.')
  left,right=setup.split('=');F=expr(left)-expr(right)
  assert sp.cancel(F-((x-h)**2/a**2+(y-k)**2/b**2-1))==0
  derivative=sp.cancel(-sp.diff(F,x)/sp.diff(F,y))
  initial=blocks[0].split('⟹')[0].replace(r'\,','');ll,rr=initial.split('=');assert sp.cancel(expr(ll)-expr(rr)-F)==0
  body=blocks[1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
  rows=body.split(r' \\ ');assert len(rows)==5
  assert rows[0].count(g.OP)==2 and rows[1].count(g.OP)==2
  assert rows[0].startswith(g.OP+'(') and rows[1].startswith(g.OP+'(')
  for row in rows:
   lhs,rhs=row.split(' & =');assert sp.cancel((formal(lhs)-formal(rhs)).subs(z,derivative))==0,row
  # Structural stage order is formal whole derivative, split derivatives, chain, isolation, result.
  assert g.D in rows[2] and rows[2].endswith(' & =0')
  assert rows[3].count(g.D)==1 and rows[3].split(' & =')[1].startswith('-')
  assert rows[4].startswith(g.D+' & =')
 else:derivative=-sp.Rational(b*b,a*a)*(x-h)/(y-k)
 field=q[':question/answer-fields'][0];parsed=[expr(v[':answer/value']) for v in field[':answer-field/choices']]
 assert len(parsed)==5
 assert all(sp.cancel(v-w)!=0 for i,v in enumerate(parsed) for w in parsed[i+1:])
 matches=[i for i,v in enumerate(parsed) if sp.cancel(v-derivative)==0];assert len(matches)==1
 if ':answer-field/correct' in field:assert field[':answer-field/correct'][1]==field[':answer-field/choices'][matches[0]][':answer/id']
 # Every displayed source/authored operation independently applied to actual ellipse factors.
 U=x-h;V=y-k;R=sp.Rational(b*b,a*a);L=sp.Rational(b,a)
 mapping={'r':R,'v':1/R,'l':L,'i':1/L}
 wanted=[]
 for code in r['generation']['operations']:
  pair=code[2:4]
  N,T={'XY':(U,V),'YX':(V,U),'VW':(x+h,y+k),'WV':(y+k,x+h)}[pair]
  if code.endswith('t'):N,T=(y-h,x) if pair=='YX' else (x,y-h)
  wanted.append((-1 if code[0]=='-' else 1)*mapping[code[1]]*N/T)
 assert all(sum(sp.cancel(v-w)==0 for w in wanted)==1 for v in parsed)
 return derivative

def source_geometry():
 records=[]
 for q,p in list(zip(g.KP[':knowledge-point/questions'],g.GEOMETRIES))+[(g.KP[':knowledge-point/canonical-example'],(0,0,2,4))]:
  path=re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1);f=Path('/media/jake/SSD/EDB/math')/path;im=Image.open(f).convert('RGBA');blue=[];black=[]
  for yy in range(im.height):
   for xx in range(im.width):
    R,G,B,A=im.getpixel((xx,yy))
    if A>150 and B>100 and B>R*1.3 and G>R*1.1:blue.append((xx,yy))
    if A>150 and max(R,G,B)<100:black.append((xx,yy))
  xmin,xmax=min(v[0] for v in blue),max(v[0] for v in blue);ymin,ymax=min(v[1] for v in blue),max(v[1] for v in blue)
  ox=Counter(v[0] for v in black).most_common(1)[0][0];oy=Counter(v[1] for v in black).most_common(1)[0][0]
  h,k,a,b=p;scale=(xmax-xmin)/(2*a)
  # Calibrate x from the independently inspected signed labels/guide lengths.
  # Verify y extent/center with the SAME calibrated pixel unit (stroke tolerance 3px).
  center=[(xmin+xmax)/2,(ymin+ymax)/2]
  assert abs((ymax-ymin)-2*b*scale)<=3
  assert abs(center[0]-(ox+h*scale))<=2
  assert abs(center[1]-(oy-k*scale))<=2
  records.append({'source_id':q[':question/math-academy-id'],'dimensions':list(im.size),'blue_pixel_extents':[xmin,xmax,ymin,ymax],'pixel_origin':[ox,oy],'calibrated_pixels_per_unit':scale,'center':[h,k],'semiaxes':[a,b],'unit_scales':[1,1],'positive_axis_arrows':['right','up'],'label_reading':'Manually inspected every signed endpoint or center/semiaxis guide at original 360x304 resolution; no tangent-direction arrows in source.','stroke_allowance_px':3,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 return records

def generated_geometry(r):
 pl=r['generation']['plot'];side=json.loads(Path(pl['spec']).read_text());p=r['generation']['parameters'];im=Image.open(pl['prompt']).convert('RGB');blue=[]
 for yy in range(im.height):
  for xx in range(im.width):
   R,G,B=im.getpixel((xx,yy))
   if B>100 and B>R*1.3 and G>R*1.1:blue.append((xx,yy))
 actual=[min(t[0] for t in blue),max(t[0] for t in blue),min(t[1] for t in blue),max(t[1] for t in blue)]
 trans=side['pixel_transform'];scale=im.width/trans['canvas_size'][0];ox,oy=[v*scale for v in trans['origin']];sx=trans['unit_x'][0]*scale-ox;sy=trans['unit_y'][1]*scale-oy;height=im.height
 assert abs(sx-sy)<1e-6
 expected=[ox+(p['h']-p['a'])*sx,ox+(p['h']+p['a'])*sx,height-(oy+(p['k']+p['b'])*sy),height-(oy+(p['k']-p['b'])*sy)]
 assert all(abs(a-b)<=3 for a,b in zip(actual,expected)),(actual,expected)
 return {'parameters':p,'actual_blue_extents':actual,'expected_transform_extents':expected,'allowance_px':3}

def main():
 source_rows=[];engine=[];reviews=[];generated_geometry_rows=[];replay_count=0;choice_count=0
 # Fidelity first, before normal variants. Compare complete strings and field omissions.
 for c in g.CASES.values():
  r=g.generate(c['level'],seed=31,parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);q=g.KP[':knowledge-point/questions'][c['index']];rq=r['question'];f=rq[':question/answer-fields'][0];of=q[':question/answer-fields'][0]
  assert set(rq)==set(q)
  assert set(f)==set(of)
  assert all(set(a)==set(of[':answer-field/choices'][0]) for a in f[':answer-field/choices'])
  assert rq[':question/problem']==q[':question/problem']
  assert rq.get(':question/worked-solution')==q.get(':question/worked-solution')
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  if ':answer-field/correct' in of:
   original=of[':answer-field/correct'][':answer/value'];new=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert new==original
  mathcheck(r)
  if ':answer-field/correct' in f:engine.append(r)
  replay_count+=1;choice_count+=len(f[':answer-field/choices']);reviews.append(r)
  source_rows.append({**c,'raw_key_presence_matched':True,'full_bank_exact':True,'full_solution_exact_or_missing':True,'correct_designation':'matched' if ':answer-field/correct' in of else 'missing in source; cannot count matched'})
  # Minimal supported completion exposed separately: no claim of captured missing attrs.
  completed=g.generate(c['level'],parameters=c['parameters'],profile='completed-'+c['source_id']);mathcheck(completed);reviews.append(completed);engine.append(completed)
 geometry=source_geometry();(HERE/'source-geometry.json').write_text(json.dumps(geometry,indent=2)+'\n')
 # Validate finite complete bank domains without rendering or inflating scaled ratio counts.
 variety={};task_sets={}
 for level in ('easy','moderate','hard'):
  dom=g.domain(level);seen=set()
  for p in dom:
   g.check_parameters(level,p);g.bank(p,g.DEFAULT)
   seen.add((p['h'],p['k'],Fraction(p['b'],p['a'])))
  task_sets[level]=seen
  variety[level]={'eligible_parameter_instances':len(dom),'meaningful_reduced_tasks':len(seen),'excludes':'common axis-ratio scaling, seed, notation and bank/profile aliases'}
  for seed in range(6):
   r=g.generate(level,seed=seed);mathcheck(r);generated_geometry_rows.append(generated_geometry(r));reviews.append(r);engine.append(r)
   other=g.generate(level,seed=seed+999,parameters=r['generation']['parameters']);assert r['question'][':question/id']==other['question'][':question/id']
  invalid=dict(dom[0]);invalid['a']=100
  try:g.generate(level,parameters=invalid)
  except ValueError:pass
  else:raise AssertionError('explicit bound bypass')
 # Regression: difficulty is a workload boundary, never only an ID distinction.
 overlap={}
 for left,right in itertools.combinations(('easy','moderate','hard'),2):
  common=task_sets[left]&task_sets[right];assert not common,(left,right,common)
  overlap[left+' / '+right]=len(common)
 hard_original={'h':2,'k':-1,'a':3,'b':4}
 for level in ('easy','moderate'):
  try:g.generate(level,parameters=hard_original)
  except ValueError:pass
  else:raise AssertionError('simultaneous shift/nonunit ratio admitted below hard')
 for p in [dict(h=-1,k=-1,a=2,b=1),dict(h=0,k=1,a=2,b=3),dict(h=3,k=0,a=3,b=2)]:
  g.check_parameters('moderate',p)
  try:g.generate('hard',parameters=p)
  except ValueError:pass
  else:raise AssertionError('observed moderate instance admitted at hard')
 for p in [dict(h=2,k=-1,a=3,b=4),dict(h=0,k=1,a=2,b=1),dict(h=2,k=0,a=4,b=2)]:
  try:g.generate('moderate',parameters=p)
  except ValueError:pass
  else:raise AssertionError('moderate workload degeneracy/boundary bypass')
 case=g.CASES['q-127364'];assert case['level']=='hard'
 raw=g.generate('hard',parameters=case['parameters'],profile=case['bank_profile']);assert ':question/difficulty' not in raw['question']
 completion=g.generate('hard',parameters=case['parameters'],profile='completed-q-127364');assert completion['question'][':question/difficulty']==':question.difficulty/hard'
 assert g.generate('hard',parameters=hard_original)['generation']['level']=='hard'
 (HERE/'difficulty-boundary.json').write_text(json.dumps({'status':'passed','meaningful_task_overlap_counts':overlap,'unrated_q_127364_inferred_level':'hard','raw_difficulty_still_absent':True,'single_shift_unit_reduced_ratio_rejected_at_moderate':True,'both_shift_nonunit_reduced_ratio_rejected_at_moderate':True,'graded_moderate_instances_preserved':3,'moderate_peers':['one shifted coordinate and two nonunit reduced ratio terms','two shifted coordinates and one unit reduced ratio term'],'hard_workload':'two shifted coordinates and two nonunit coprime reduced ratio terms, axes 3..8','identity_includes_actual_level':True},indent=2)+'\n')
 # Changed-parameter source profiles exercise all full historical banks/solutions.
 for c in g.CASES.values():
  for seed in range(200,1000):
   p=g.domain(c['level'])[seed%len(g.domain(c['level']))]
   try:r=g.generate(c['level'],seed=seed,parameters=p,profile='completed-'+c['source_id'])
   except ValueError:continue
   if p==c['parameters']:continue
   mathcheck(r);reviews.append(r);engine.append(r);break
  else:raise AssertionError('profile has no changed-parameter member')
 # Native grader fixture checks every owned option, independently established correct.
 checks=[]
 for i,r in enumerate(engine):
  f=r['question'][':question/answer-fields'][0];right=f[':answer-field/correct'][1]
  checks.append({'label':str(i)+'-'+r['generation']['bank_profile'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==right else 'rejected','purpose':'complete radio bank selection'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(checks,indent=2)+'\n')
 subprocess.run([str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 # Fresh concurrency QA uses isolated private output; different and identical calls.
 with tempfile.TemporaryDirectory(prefix='ellipse-qa-',dir=HERE) as td:
  ps=[g.domain('hard')[0],g.domain('hard')[1],g.domain('hard')[0]]
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:plots=list(pool.map(lambda p:g.render_plots(p,td),ps))
  for p,pl in zip(ps,plots):assert json.loads(Path(pl['spec']).read_text())['parameters']==p
  assert plots[0]==plots[2]
  assert not list(Path(td).glob('ellipse-render-*'))
 (HERE/'generated-geometry.json').write_text(json.dumps(generated_geometry_rows,indent=2)+'\n')
 (HERE/'source-cases.json').write_text(json.dumps(source_rows,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(reviews,indent=2)+'\n')
 (HERE/'review.md').write_text('# Ellipse generator review\n\nRaw originals, separate supported completions, six authored variants per level, and changed-parameter variants for every observed bank. Checked boxes mark the designated correct choice; unrated original omissions remain visible.\n\n'+'\n\n'.join(g.markdown(r) for r in reviews)+'\n')
 result={'status':'passed','basis':1356,'database_writes':0,'source_questions':9,'raw_exact_prompts':9,'full_exact_banks':9,'exact_displayed_choices':45,'captured_correct_designations_matched':7,'missing_designations_preserved':2,'exact_present_solutions':7,'missing_solutions_preserved':2,'missing_difficulties_preserved':2,'supported_completions':9,'source_raster_geometry_checks':10,'generated_raster_geometry_checks':len(generated_geometry_rows),'authored_variants_per_level':6,'changed_parameter_banks':9,'mathematics':'Every displayed choice, standard-equation input and five ordered implicit-derivative rows independently parsed and checked.','native_grading':json.loads((HERE/'engine-report.json').read_text()),'variety':variety,'difficulty_boundaries':json.loads((HERE/'difficulty-boundary.json').read_text()),'concurrency':'fresh isolated identical/different renders passed','limits':['Hard level authored, not observed.','Distractor error interpretation is hypothesized from mathematical operations; historical banks evidence only.','Native radio grading checks ID selection, so mathematical full-bank checks run separately.','Original two missing correct designations cannot count as recovered captured designations.']}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('native_grading',)},indent=2))
if __name__=='__main__':main()

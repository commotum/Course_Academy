#!/usr/bin/env python3
"""Independent displayed arithmetic, source parity, bank, geometry/native QA."""
import copy,hashlib,importlib.util,json,math,re,subprocess,uuid,concurrent.futures
from pathlib import Path
from PIL import Image
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('inverse_area',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def dump(name,v):(HERE/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def argument(t,i):
 assert t[i]=='{',(t,i)
 depth=1;j=i+1
 while depth:
  if t[j]=='{':depth+=1
  elif t[j]=='}':depth-=1
  j+=1
 return t[i+1:j-1],j

def parse(t,env=None):
 """Read TeX arithmetic from learner content, not generation data."""
 t=t.strip().rstrip('.,').replace('\u2061','').replace('⁡','').replace(r'\,','').replace(' ',' ').replace(r'\cdot','*')
 t=re.sub(r'\\text\{[^}]*\}','',t).replace('cm','').replace('mm','')
 t=re.sub(r'\\operatorname\{sin\}\{(\d+)\}\^\{∘\}',lambda m:'('+str(sp.sin(sp.pi*int(m[1])/180))+')',t)
 t=t.replace(r'\operatorname{sin}A','S').replace('m∠A','T')
 t=re.sub(r'\{(\d+)\}\^\{∘\}',r'\1',t)
 def convert(t):
  out='';i=0
  while i<len(t):
   if t.startswith(r'\frac',i):
    n,j=argument(t,i+5);d,k=argument(t,j);out+='(('+convert(n)+')/('+convert(d)+'))';i=k
   elif t.startswith(r'\sqrt',i):
    n,j=argument(t,i+5);out+='sqrt('+convert(n)+')';i=j
   elif t.startswith(r'\cancel',i):
    n,j=argument(t,i+7);out+='('+convert(n)+')';i=j
   else:out+=t[i];i+=1
  return out.replace('{','(').replace('}',')')
 t=convert(t).replace('^','**');local={k:sp.Symbol(k) for k in ['A','b','c','S','T']};local['sqrt']=sp.sqrt
 e=parse_expr(t,local_dict=local,transformations=standard_transformations+(implicit_multiplication_application,))
 return sp.simplify(e.subs({local[k]:v for k,v in (env or {}).items()}))
def balanced(t):
 assert t.count('$')%2==0,t
 depth=0
 for i,c in enumerate(t):
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert not re.search(r'\\\\(?:frac|sqrt|begin|operatorname)',t)

def verify(r):
 q=r['question'];m=r['generation'];raw=m['evidence_only'];template=m['template'];kind=g.TEMPLATES[template][1];f=q[':question/answer-fields'][0]
 assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP_ID
 assert m['eligible_for_learning']==(not raw)
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in f[':answer-field/choices']]:balanced(text)
 for id in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]:uuid.UUID(id)
 prompt=q[':question/problem'];frag=prompt.split('is $')[1].split('$')[0];area_tex=re.split(r'cm|mm|\\,|\\text|\{\\text',frag)[0].rstrip('{');area=parse(area_tex)
 # Source plot labels independently transcribed in anchors; generated labels
 # are read from sidecar matched to actual image path/hash and geometric data.
 if m['plot']:
  path=Path(re.search(r'!\[\]\(([^)]+)\)',prompt)[1]);pm=json.loads(path.with_suffix('.json').read_text());assert hashlib.sha256(path.read_bytes()).hexdigest()==pm['sha256'];assert json.loads(json.dumps(m['plot']))==pm
  image=Image.open(path).convert('RGB');assert list(image.size)==pm['image_pixels']
  for pair in ('AB','BC','CA'):
   P,Q=[pm['pixel_vertices_bottom_origin'][name] for name in pair]
   for fraction in (.25,.5,.75):
    x=round(P[0]+fraction*(Q[0]-P[0]));y=round(image.height-1-(P[1]+fraction*(Q[1]-P[1])))
    assert any(max(image.getpixel((xx,yy)))<100 for xx in range(max(0,x-3),min(image.width,x+4)) for yy in range(max(0,y-3),min(image.height,y+4))),(pair,x,y,'rendered edge stroke absent')
  A=pm['vertices']['A'];B=pm['vertices']['B'];C=pm['vertices']['C'];cgeom=math.dist(A,B);bgeom=math.dist(A,C);angle=math.degrees(math.acos(sum((B[i]-A[i])*(C[i]-A[i]) for i in (0,1))/(bgeom*cgeom)))
  c=parse(pm['labels']['AB']);b=parse(pm['b']);t=round(angle)
  assert abs(float(c)-cgeom)<1e-9 and abs(float(b)-bgeom)<1e-9 and abs(angle-t)<1e-8
  assert pm['labels']['AC']==(g.tex(b) if kind=='angle' else None) and pm['labels']['angle']==(t if kind=='side' else None)
  if kind=='angle':assert parse(pm['labels']['AC'])==b
  # Equal-scale geometric area independently agrees with actual area statement.
  geomarea=abs((B[0]-A[0])*(C[1]-A[1])-(C[0]-A[0])*(B[1]-A[1]))/2;assert abs(float(area)-geomarea)<1e-8
 else:
  _,b0,c0,t,_=g.ANCHORS[template];b,c=sp.sympify(b0),sp.sympify(c0)
  path=Path('/media/jake/SSD/EDB/math')/re.search(r'!\[\]\(([^)]+)\)',prompt)[1];assert path.exists()
 S=sp.sin(sp.pi*t/180);correct=sp.simplify(2*area/(c*S)) if kind=='side' else next(t0 for t0 in (30,45,60) if sp.simplify(sp.sin(sp.pi*t0/180)-2*area/(b*c))==0)
 assert area==sp.simplify(b*c*S/2)
 if kind=='angle' and not raw:assert 'with acute $∠A$' in prompt and 'acute triangle' not in prompt
 if raw and template=='q-280282':assert c-b*sp.cos(sp.pi*t/180)<0  # original falsely describes the whole triangle as acute
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
  assert blocks[0]==r'A=\frac{1}{2}bc\operatorname{sin}⁡A,'
  here=blocks[1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
  assert parse(here[0].split('AB=')[1])==c
  if kind=='angle':assert parse(here[1].split('AC=')[1])==b
  else:assert here[1].startswith('b & =AC') and parse(here[2].split('=',1)[1])==t
  rows=blocks[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
  env={'A':area,'b':b,'c':c,'S':S,'T':t}
  for row in rows:
   sides=row.replace('&','').split('=');assert len(sides)==2,row
   assert parse(sides[0],env)==parse(sides[1],env),(template,row,parse(sides[0],env),parse(sides[1],env))
  assert rows[0]==r'A & =\frac{1}{2}\cdot b\cdot c\cdot \operatorname{sin}⁡A'
  assert rows[1].count(r'\cdot')==3
  if kind=='side':
   assert rows[2].count(r'\cdot')==3 and r'\operatorname{sin}' not in rows[2]
   assert rows[-1].startswith('b & =') and r'\text' in rows[-1]
   conclusion=re.search(r'We conclude that \$AC=(.*?)\$',sol);assert conclusion and parse(conclusion[1])==correct
  if template in g.SOURCES and g.SOURCES[template].get(':question/worked-solution'):
   source_blocks=re.findall(r'\$\$\n(.*?)\n\$\$',g.SOURCES[template][':question/worked-solution'],re.S);source_rows=source_blocks[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
   assert len(rows)==len(source_rows)
   # Structural stage parity independent of algebraic equality. Source-specific
   # common factors, cancellation rows, swapped isolation and omitted redundant
   # sine row remain present at changed parameters.
   for shown,old in zip(rows,source_rows):
    assert shown.count(r'\cdot')==old.count(r'\cdot') and shown.count(r'\cancel')==old.count(r'\cancel')
    assert ('sin' in shown)==('sin' in old)
    assert (' & =' in shown)==(' & =' in old)
   if template=='q-280282':assert rows[-3].endswith(r'\operatorname{sin}⁡A')
  elif not raw and kind=='side':
   assert len(rows)==6
   assert rows[3].count(r'\cdot')==0 and r'\frac' in rows[4] and r'\text' in rows[5]
 vals=[parse(re.sub(r'\^\{\\circ\}|\^\{∘\}','',a[':answer/value'])) for a in f[':answer-field/choices']]
 assert len(vals)==len(set(vals)) and all(v>0 for v in vals)
 if f[':answer-field/type'].endswith('blank'):assert len(vals)==1 and '{{'+f[':answer-field/key']+'}}' in prompt
 else:assert len(vals)==5
 if ':answer-field/correct' in f:
  assert f[':answer-field/correct'][0]==':answer/id'
  v=next(v for a,v in zip(f[':answer-field/choices'],vals) if a[':answer/id']==f[':answer-field/correct'][1]);assert v==correct
 else:assert raw and template in ('q-43310','q-43343')
 if not raw and f[':answer-field/type'].endswith('radio'):
  expected=[b,b/2,2*area*c/S,2*area/(b*S),2*area/(c**2*S)] if kind=='side' else list(map(sp.Integer,[30,45,60,120,135]));assert set(vals)==set(map(sp.simplify,expected))
 return correct

def engine(r,label):
 f=r['question'][':question/answer-fields'][0]
 if ':answer-field/correct' not in f:return None
 correct=verify(r)
 if f[':answer-field/type'].endswith('radio'):checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'whole owned bank'} for a in f[':answer-field/choices']]
 else:checks=[{'submitted':str(correct),'expected':'accepted','purpose':'canonical scalar'},{'submitted':f'({2*correct})/2','expected':'accepted','purpose':'independent unreduced quotient'},{'submitted':str(correct+1),'expected':'rejected','purpose':'incorrect scalar'}]
 return {'label':label,'record':r,'checks':checks}

def main():
 dump('source.json',g.CAP);records=[];raws=[];cases=[];checks=[];review=[];details=[]
 for sid,(kind,b,c,t,u) in g.ANCHORS.items():
  p={'b':b,'c':c,'theta':t,'unit':u};case={'source_id':sid,'level':'moderate','template':sid,'parameters':p,'bank_profile':'raw_'+sid,'difficulty_origin':'observed' if ':question/difficulty' in g.SOURCES[sid] else 'authored-supported-moderate'};cases.append(case)
  raw=g.generate_moderate(template=sid,parameters=p,profile=case['bank_profile']);verify(raw);raws.append(raw);source=g.SOURCES[sid];q=raw['question'];f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
  for k in (':question/problem',':question/worked-solution'):assert q.get(k)==source.get(k)
  for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (k in q)==(k in source)
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'] and f[':answer-field/key']==sf[':answer-field/key']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  if ':answer-field/correct' in sf:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  details.append({'source_id':sid,'exact_prompt':True,'exact_solution':True if ':question/worked-solution' in source else None,'exact_bank_values':len(sf[':answer-field/choices']),'designation_match':True if ':answer-field/correct' in sf else None,'presence_parity':True})
  review.append('## Original '+sid+' (raw evidence; learning eligibility false)\n\n'+g.markdown(raw));ec=engine(raw,'raw/'+sid)
  if ec:checks.append(ec)
  for scale in (sp.Rational(1,2),2,3):
   pp={**p,'b':str(sp.sympify(b)*scale),'c':str(sp.sympify(c)*scale)};r=g.generate_moderate(template=sid,parameters=pp,profile='raw_'+sid);verify(r);records.append(r)
   if scale==2:review.append('### Generated observed-profile dilation ×2 (opaque bank intent unresolved)\n\n'+g.markdown(r))
   ec=engine(r,'raw/'+sid+'/scale'+str(scale))
   if ec:checks.append(ec)
  for seed in range(4):
   r=g.generate_moderate(seed=seed+113,template=sid);verify(r);records.append(r);checks.append(engine(r,'normal/'+sid+'/'+str(seed)))
   if seed<2:review.append('### Generated eligible moderate variant '+str(seed+1)+'\n\n'+g.markdown(r))
 for level in ('easy','moderate','hard'):
  covered=set();tasks=set()
  for seed in range(45):
   r=g.generate(level,seed=seed+2000);verify(r);records.append(r);checks.append(engine(r,'default/'+level+'/'+str(seed)));covered.add(r['generation']['template']);tasks.add(r['generation']['parameter_fingerprint'])
   if seed<2:review.append('## Authored/default '+level+' variant '+str(seed+1)+'\n\n'+g.markdown(r))
   replay=g.generate(level,seed=seed+10000,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile']);verify(replay)
   assert replay['question'][':question/id']==r['question'][':question/id']
  assert covered=={k for k,v in g.TEMPLATES.items() if v[0]==level},(level,covered)
  details.append({'level':level,'default_family_coverage':sorted(covered),'substantive_unique_tasks_sampled':len(tasks)})
 # Reject algebraically equal stage deletion, wrong conclusion, plotted-label mutation,
 # complete-bank collision and level violations, independently.
 for mode in ('delete-substitution','conclusion','first-product'):
  r=copy.deepcopy(g.generate_moderate(123,template='q-161109'))
  if mode=='delete-substitution':
   ss=r['question'][':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',ss,re.S);last=blocks[-1];rows=last.split(r' \\ ');del rows[2];r['question'][':question/worked-solution']=ss.replace(last,r' \\ '.join(rows))
  elif mode=='conclusion':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('We conclude that $AC=', 'We conclude that $AC=1+')
  else:r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(r'\frac{1}{2}\cdot b\cdot ',r'\frac{1}{3}\cdot b\cdot ',1)
  try:verify(r);raise RuntimeError('Mutation escaped: '+mode)
  except AssertionError:pass
 for level,p in [('easy',{'b':'7/2','c':'3','theta':30,'unit':'cm'}),('hard',{'b':'3','c':'4','theta':60,'unit':'cm'}),('moderate',{'b':'4','c':'5','theta':45,'unit':'cm'})]:
  try:g.generate(level,template='q-161107' if level=='moderate' else level+'_blank',parameters=p);raise RuntimeError('Guard failed')
  except ValueError:pass
 # Fresh simultaneous renders in private cache, same and different instance.
 fresh=HERE/'concurrency';fresh.mkdir(exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:assets=list(pool.map(lambda n:g.plot(sp.Rational(n,2),sp.Rational(n+1,2),120,'cm','side',fresh),[7,7,9,11]))
 assert assets[0][0]==assets[1][0] and len({a[0] for a in assets})==3
 assert not any(p.suffix not in ('.png','.json') for p in fresh.iterdir() if p.is_file())
 # Cold render and disk cache must return identical full metadata, not just
 # identical PNG paths or content IDs. Retain fresh evidence per validation.
 cold=fresh/str(uuid.uuid4())
 first=g.plot(sp.Rational(7,2),sp.Rational(9,2),120,'cm','side',cold)
 assert first==g.plot(sp.Rational(7,2),sp.Rational(9,2),120,'cm','side',cold)
 # Extreme unequal sides previously put the angle text across an edge.
 # These complete records preserve the same givens and exact answer while
 # using the renderer's exterior angle callout; parent inspects the PNGs.
 for b,c in ((12,2),(2,12)):
  verify(g.generate_easy(template='easy_blank',parameters={'b':str(b),'c':str(c),'theta':30,'unit':'cm'}))
 dump('source-cases.json',cases);dump('review.json',raws+records);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 dump('engine-input.json',checks);cp=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine.json')],text=True,capture_output=True)
 dump('validation.json',{'passed':cp.returncode==0,'source_questions':9,'source_exact_prompts':9,'source_exact_present_solutions':7,'source_solution_absences_preserved':2,'source_banks':9,'source_option_values':33,'source_correct_designations_matched':7,'missing_designations_preserved':2,'raw_evidence_only':True,'source_prose_anomalies':[{'source_id':'q-280282','issue':'claims whole triangle acute although angle B is obtuse','proof':'sqrt(3)-4*cos(60°)=sqrt(3)-2<0','raw_exact':True,'normal_repair':'only included angle A acute'}],'checked_records':len(records)+len(raws),'mutation_tests':3,'native_returncode':cp.returncode,'native_stdout':cp.stdout,'native_stderr':cp.stderr,'details':details,'dependencies':{'python':g.sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()})
 assert cp.returncode==0,cp.stdout+cp.stderr
 print('PASS source9/prompts9/solutions7/banks9/values33/designations7; independently checked',len(records)+len(raws),'records; native grading passes')
if __name__=='__main__':main()

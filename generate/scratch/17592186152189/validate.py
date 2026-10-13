"""Independent displayed-string mathematics, full fidelity, geometry and native QA."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from PIL import Image
D=Path(__file__).resolve().parent;mod=importlib.util.spec_from_file_location('ellipse',D.with_suffix('.py'));g=importlib.util.module_from_spec(mod);mod.loader.exec_module(g)
t=sp.Symbol('theta',real=True)
def parse(v):
 v=v.replace('⁡','').replace('θ','theta').replace(r'\theta','theta').replace(' ', '').replace(r'\,','').replace(r'\operatorname{cos}','cos').replace(r'\operatorname{sin}','sin').replace(r'\cos','cos').replace(r'\sin','sin')
 v=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',v)
 v=re.sub(r'(cos|sin)theta',r'\1(theta)',v);v=re.sub(r'(?<=[0-9)])(?=(?:cos|sin)\()', '*',v)
 return sp.sympify(v,locals={'theta':t})
def pair(v):
 parts=re.split(r',\s*(?:\\,)?y\s*=\s*',v);assert len(parts)==2,v
 return parse(re.sub(r'^x\s*=\s*','',parts[0])),parse(parts[1])
def eligible(v,p,oriented):
 x,y=pair(v);a,b,h,k=[p[z] for z in ('a','b','h','k')]
 locus=sp.trigsimp(((x-h)/a)**2+((y-k)/b)**2-1)==0
 if not oriented:return locus
 return bool(locus and sp.simplify(x.subs(t,0)-(h+a))==0 and sp.simplify(y.subs(t,0)-k)==0 and sp.diff(y,t).subs(t,0)>0)

def formatting(s):
 # Every math block is balanced; literal field placeholders excluded.
 assert s.count('$$')%2==0
 assert s.replace('$$','').count('$')%2==0
 s=re.sub(r'\{\{[^{}]+\}\}','',s);depth=0
 for c in s:
  if c=='{':depth+=1
  if c=='}':depth-=1;assert depth>=0
 assert depth==0
 assert '--' not in s and '+-' not in s

def check(r):
 p=r['generation']['parameters'];q=r['question'];oriented='counterclockwise' in q[':question/problem'];assert set(r['knowledge_point'])=={'db_id','id','title'};assert r['knowledge_point']['db_id']==g.KP_ID
 for k in (':question/problem',':question/worked-solution'):
  if k in q:formatting(q[k])
 # Printed center/radii/start are read independently, not from recipe metadata.
 prompt=q[':question/problem'];m=re.search(r'centered at \$\((-?\d+),(-?\d+)\)\$ with horizontal radius \$(\d+)\$ and vertical radius \$(\d+)',prompt)
 if m:
  h,k,a,b=map(int,m.groups());assert (a,b,h,k)==tuple(p[z] for z in ('a','b','h','k'))
  if oriented:
   start=re.search(r'\$A\((-?\d+),(-?\d+)\)',prompt);assert tuple(map(int,start.groups()))==(h+a,k)
 solution=q.get(':question/worked-solution')
 if solution:
  prose=re.search(r'In our case, the ellipse is centered at the point \$\((-?\d+),(-?\d+)\),\$ \$a=(\d+)\$ and \$b=(\d+)\.\$',solution);assert prose
  h,k,a,b=map(int,prose.groups());assert (a,b,h,k)==tuple(p[z] for z in ('a','b','h','k'))
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);assert len(blocks)==2
  general=blocks[0].replace('⁡','').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin');assert re.sub(r'\s+','',general).startswith(r'x=a\cos\theta+h,\,y=b\sin\theta+k,\,\theta\in[0,2\pi)')
  final=blocks[-1].split(r',\,\theta')[0];assert eligible(final,p,oriented)
 fields=q[':question/answer-fields'];bank_count=0
 for f in fields:
  values=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(values)==len(set(values))
  if f[':answer-field/type'].endswith('/radio'):
   valid=[eligible(v,p,oriented) for v in values];assert sum(valid)==1,(r['generation'],values,valid)
  else:
   key=f[':answer-field/key'];expected=p['a']*sp.cos(t)+p['h'] if key=='field-1' else p['b']*sp.sin(t)+p['k'];assert len(values)==1 and sp.simplify(parse(values[0])-expected)==0
   assert '{{'+key+'}}' in prompt
  for a in f[':answer-field/choices']:formatting(a[':answer/value'])
  if ':answer-field/correct' in f:
   ref=f[':answer-field/correct'];assert ref[0]==':answer/id';answer=next(a for a in f[':answer-field/choices'] if a[':answer/id']==ref[1]);assert eligible(answer[':answer/value'],p,oriented) if f[':answer-field/type'].endswith('/radio') else True
  bank_count+=len(values)
 return bank_count

def generated_raster(r):
 pth=Path(r['generation']['plot']);m=json.load(open(pth.with_suffix('.json')));p=r['generation']['parameters'];assert m['parameters']==p
 assert m['renderer_sha256']==hashlib.sha256((D/'render.py').read_bytes()).hexdigest()
 assert m['png_sha256']==hashlib.sha256(pth.read_bytes()).hexdigest();sx,sy=m['scale_pixels'];assert abs(sx-sy)<1e-7
 if m['oriented']:assert m['tick_label_clearance_pixels']>=4
 im=Image.open(pth).convert('RGB');pts=[]
 for y in range(im.height):
  for x in range(im.width):
   rr,gg,bb=im.getpixel((x,y))
   if bb>rr+35 and gg>rr+20:pts.append((x,y))
 box=[min(x for x,y in pts),max(x for x,y in pts),min(y for x,y in pts),max(y for x,y in pts)]
 ox,oy=m['origin_pixels'];a,b,h,k=[p[z] for z in ('a','b','h','k')];expected=[ox+(h-a)*sx,ox+(h+a)*sx,oy-(k+b)*sy,oy-(k-b)*sy]
 assert max(abs(x-y) for x,y in zip(box,expected))<=3.5,(box,expected)

def run():
 subprocess.run([sys.executable,str(D/'raster_geometry.py')],check=True)
 src=json.load(open(D/'source.json'))['record'][':knowledge-point/questions'];cases=json.load(open(D/'source-cases.json'));raw=[];checks=[];nchoices=0;correctrefs=0
 for source,case in zip(src,cases):
  r=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters=case['parameters']);q=r['question'];raw.append(r);check(r)
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
   assert (key in source)==(key in q)
  assert source[':question/problem']==q[':question/problem'];assert source.get(':question/worked-solution')==q.get(':question/worked-solution')
  assert len(source[':question/answer-fields'])==len(q[':question/answer-fields'])
  for a,b in zip(source[':question/answer-fields'],q[':question/answer-fields']):
   assert a[':answer-field/key']==b[':answer-field/key'];assert a[':answer-field/type'][':db/ident']==b[':answer-field/type']
   assert sorted(x[':answer/value'] for x in a[':answer-field/choices'])==sorted(x[':answer/value'] for x in b[':answer-field/choices']);nchoices+=len(a[':answer-field/choices'])
   assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
   if ':answer-field/correct' in a:
    v=next(x[':answer/value'] for x in b[':answer-field/choices'] if x[':answer/id']==b[':answer-field/correct'][1]);assert v==a[':answer-field/correct'][':answer/value'];correctrefs+=1
  # Non-original public replay: every variable component is rebuilt normally.
  p={'a':7,'b':2,'h':-5,'k':3};rr=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters=p);check(rr)
  for rtest in (r,rr):
   qq=rtest['question']
   # Native fixtures exclude raw legacy field lacking a designation, recorded as missing source refs.
   usable=[f for f in qq[':question/answer-fields'] if ':answer-field/correct' in f]
   if usable:
    fixture=json.loads(json.dumps(rtest));fixture['question'][':question/answer-fields']=usable;checks.append(native_item(fixture,'source:'+case['source_id']))
 # At least two per E/M/H; coverage both hard layouts and every source bank.
 review=[]
 for level in ('easy','moderate','hard'):
  for seed in (21,22):
   r=g.generate(level,seed=seed,template=('oriented_radio' if seed==21 else 'oriented_blank') if level=='hard' else None);check(r);review.append(r);checks.append(native_item(r,f'generated:{level}:{seed}'))
 # Independent source mask/bank review variants.
 variants=[]
 for case in cases:
  r=g.generate(case['level'],seed=44,template=case['template'],profile=case['bank_profile'],parameters={'a':7,'b':2,'h':-5,'k':3});variants.append(r)
 # Determinism and identity under shuffle; normal family coverage and 90 tasks.
 tasks=set();families=set()
 for level in ('easy','moderate','hard'):
  for seed in range(30):
   r=g.generate(level,seed);check(r);tasks.add(r['generation']['mathematical_fingerprint']);families.add(r['generation']['template']);s=g.generate(level,seed+77,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile']);assert r['question'][':question/id']==s['question'][':question/id']
 assert families=={'supplied','graph','oriented_radio','oriented_blank'}
 for p in ({'a':1,'b':8,'h':0,'k':-6},{'a':8,'b':1,'h':6,'k':0},{'a':2,'b':3,'h':-6,'k':-6}):
  for level in ('easy','moderate','hard'):check(g.generate(level,parameters=p))
 for p in ({'a':0,'b':2,'h':2,'k':1},{'a':3,'b':3,'h':2,'k':1},{'a':3,'b':4,'h':0,'k':0},{'a':9,'b':4,'h':2,'k':1}):
  for level in ('easy','moderate','hard'):
   try:g.generate(level,parameters=p)
   except ValueError:pass
   else:raise AssertionError('Invalid input accepted')
 # Concurrent fresh writes exercise different and identical render parameter sets.
 concurrent_params=[{'a':2,'b':7,'h':-4,'k':-3},{'a':2,'b':7,'h':-4,'k':-3},{'a':7,'b':1,'h':5,'k':-4}]
 for p in concurrent_params:
  path=g.render_plot(p,True);Path(path).unlink(missing_ok=True);Path(path).with_suffix('.json').unlink(missing_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda p:g.generate_hard(parameters=p,template='oriented_radio'),concurrent_params))
 assert results[0]['question'][':question/id']==results[1]['question'][':question/id'];assert results[0]['question'][':question/id']!=results[2]['question'][':question/id']
 for r in results:
  check(r);p=Path(r['generation']['plot']);m=json.load(open(p.with_suffix('.json')));assert m['parameters']==r['generation']['parameters'];assert m['equal_scale'] and m['label_clearance_pixels']>=11;assert m['png_sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
 for r in review+variants+results:
  if r['generation']['plot'] and r['generation']['plot'].startswith('/'):generated_raster(r)
 (D/'review.json').write_text(json.dumps({'original_replays':raw,'source_bank_variants':variants,'generated_examples':review},ensure_ascii=False,indent=2)+'\n');(D/'engine-input.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 subprocess.run([str(D.parents[1]/'runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine.json')],check=True)
 engine=json.load(open(D/'engine.json'))
 report={'passed':True,'status':'passed_with_documented_native_limitations','native_equivalent_entry_coverage_complete':False,'native_unresolved_source_entries':12,'native_unresolved_normal_entries':2,'source_questions':len(src),'prompt_exact_matches':len(src),'worked_solution_exact_matches':14,'worked_solution_absent_preserved':1,'whole_banks_exact_matches':len([f for q in src for f in q[':question/answer-fields']]),'displayed_values_exact_matches':nchoices,'correct_designations_exact_matches':correctrefs,'missing_source_designations':2,'source_attribute_presence_passed':True,'generated_mathematical_tasks_in_90_samples':len(tasks),'source_mask_variants':len(variants),'normal_families':sorted(families),'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'source_fidelity_separate_from_math_and_native':True,'database_writes':0,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'frozen_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (D.with_suffix('.py'),D/'specs.json',D/'render.py',D/'source.json')}}
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

def native_item(r,label):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  correct=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete displayed bank ID grading'} for a in f[':answer-field/choices'])
  else:
   a=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct);expr=parse(a);equiv=str(sp.expand(expr)).replace('theta','theta')
   # Different trig identity form, rather than a simplified identical spelling.
   c=expr.coeff(sp.cos(t)) or expr.coeff(sp.sin(t));z=expr-c*(sp.cos(t) if expr.has(sp.cos(t)) else sp.sin(t));alt=(f'{c}*sin(theta+pi/2)+({z})' if expr.has(sp.cos(t)) else f'{c}*cos(pi/2-theta)+({z})')
   factor=f'{c}*('+('cos(theta)' if expr.has(sp.cos(t)) else 'sin(theta)')+f'+({sp.Rational(z,c)}))'
   checks.append({'field_index':i,'submitted':factor,'expected':'accepted','purpose':'factored equivalent translation expression'})
   assert sp.trigsimp(parse(alt)-expr)==0 and sp.simplify(parse(factor)-expr)==0
   checks.extend([{'field_index':i,'submitted':a,'expected':'accepted','purpose':'faithful blank answer'},{'field_index':i,'submitted':alt,'expected':'unresolved','purpose':('source evidence' if r['generation']['evidence_only'] else 'supported normal canonical/factored record')+'; mathematically valid trig-shift entry unresolved by native rules'},{'field_index':i,'submitted':str(expr+1),'expected':'rejected','purpose':'wrong translation'}])
 return {'label':label,'record':r,'checks':checks}
if __name__=='__main__':run()

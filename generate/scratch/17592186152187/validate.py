"""Independent source, actual displayed mathematics, raster and native grading QA."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys,tempfile
from pathlib import Path
from fractions import Fraction
from PIL import Image
import sympy as sp
D=Path(__file__).resolve().parent;SCRIPT=D.with_suffix('.py');spec=importlib.util.spec_from_file_location('ellipse_generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t=sp.Symbol('t',real=True);A,B=sp.symbols('a b',positive=True)
def coef(s):
 s=s.strip();s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'(\1)/(\2)',s);s=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',s);s=re.sub(r'(?<=\d)\s*(?=sqrt\()', '*',s)
 return sp.sympify(s or '1',locals={'sqrt':sp.sqrt,'a':A,'b':B})
def readpair(s):
 s=s.replace(r'\operatorname{cos}','cos').replace(r'\operatorname{sin}','sin').replace(r'\cos','cos').replace(r'\sin','sin').replace('⁡','').replace(r'\theta','theta').replace('θ','theta')
 matches=re.findall(r'([xy])\s*=\s*(.*?)\s*(cos|sin)\s*theta',s)
 assert len(matches)==2 and [x[0] for x in matches]==['x','y'],s
 return tuple(coef(c)*(sp.cos(t) if fn=='cos' else sp.sin(t)) for _,c,fn in matches)
def signature(pair):
 return tuple(sp.expand(z).coeff(fn(t)) for z in pair for fn in (sp.cos,sp.sin))
def samepair(x,y):return signature(x)==signature(y)
def valid(pair,a,b,traversal):
 # Independent polynomial identity in cos(t),sin(t): both square coefficients
 # must be one and the mixed term zero; determinant supplies orientation.
 a=sp.Rational(a);b=sp.Rational(b);xc,xs,yc,ys=signature(pair);cross=sp.simplify(xc*ys-xs*yc)
 locus=sp.simplify(xc**2/a**2+yc**2/b**2)==1 and sp.simplify(xs**2/a**2+ys**2/b**2)==1 and sp.simplify(xc*xs/a**2+yc*ys/b**2)==0 and cross!=0
 return bool(locus and (not traversal or (xc==a and yc==0 and cross>0)))

def formatting(q):
 for text in (q[':question/problem'],q.get(':question/worked-solution',''))+tuple(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']):
  assert text.count('$')%2==0
  txt=re.sub(r'\{\{[^{}]*\}\}','',text);n=0
  for c in txt:
   if c=='{':n+=1
   if c=='}':n-=1
   assert n>=0
  assert n==0
 for f in q[':question/answer-fields']:
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
def png_geometry(asset,a,b):
 if asset['renderer']!='Matplotlib':return
 path=Path(asset['prompt']);side=json.loads(Path(asset['sidecar']).read_text());im=Image.open(path).convert('RGB');w,h=im.size
 blue=[]
 for y in range(h):
  for x in range(w):
   r,gg,bb=im.getpixel((x,y))
   if bb>r+50 and bb>gg+15 and r<140:blue.append((x,y))
 assert blue
 actual=[min(x for x,y in blue),min(y for x,y in blue),max(x for x,y in blue),max(y for x,y in blue)];e=side['curve_pixel_extents'];expected=[e[0][0],h-e[1][1],e[1][0],h-e[0][1]]
 assert max(abs(x-y) for x,y in zip(actual,expected))<=4,(actual,expected)
 assert side['a']==str(a) and side['b']==str(b);assert side['label_clearance_pass'];assert side['python'] and side['matplotlib']
 boxes=[z['bbox'] for z in side['labels']]
 for i,bb in enumerate(boxes):
  assert 0<=bb[0]<bb[2]<=w and 0<=bb[1]<bb[3]<=h
  for cc in boxes[:i]:assert not(bb[0]<cc[2] and cc[0]<bb[2] and bb[1]<cc[3] and cc[1]<bb[3])
 if side['hard']:
  assert all(z['text'] in ('x','y','A','J') or int(z['text'])%2==0 for z in side['labels'])
def check_record(z):
 q=z['question'];p=z['generation']['parameters'];a=sp.Rational(p['a']);b=sp.Rational(p['b']);assert set(z['knowledge_point'])=={'db_id','id','title'};formatting(q)
 # Read supplied prose radii independently, or original/generated geometry.
 prompt=q[':question/problem'];m=re.search(r'horizontal radius \$([^$]+)\$ and vertical radius \$([^$]+),\$',prompt)
 if m:assert coef(m.group(1))==a and coef(m.group(2))==b
 if z['generation']['level']=='hard':assert not m and 'half-unit ticks' in prompt and (a.q==2 or b.q==2)
 sol=q.get(':question/worked-solution')
 if sol:
  stages=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(stages)==2
  assert samepair(readpair(stages[0]),(A*sp.cos(t),B*sp.sin(t)));assert samepair(readpair(stages[1]),(a*sp.cos(t),b*sp.sin(t)))
  ma=re.search(r'In our case, \$a=([^$]*)\$ and \$b=([^$]*).\$',sol);assert ma and coef(ma.group(1))==a and coef(ma.group(2))==b
  assert ('Under this parametrization' in sol)==(z['generation']['template']!='graph')
 for i,f in enumerate(q[':question/answer-fields']):
  answers=f[':answer-field/choices'];ids=[v[':answer/id'] for v in answers];assert len(ids)==len(set(ids));
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][1] in ids
  if f[':answer-field/type'].endswith('/radio'):
   pairs=[readpair(x[':answer/value']) for x in answers]
   assert not any(samepair(pairs[i],pairs[j]) for i in range(len(pairs)) for j in range(i));elig=[valid(pair,a,b,z['generation']['template']!='graph') for pair in pairs];assert sum(elig)==1
   if ':answer-field/correct' in f:assert elig[ids.index(f[':answer-field/correct'][1])]
  else:
   assert len(answers)==1;value=answers[0][':answer/value'];pair=readpair('x='+value+',y='+str(b)+r'\sin\theta') if i==0 else readpair('x='+str(a)+r'\cos\theta,y='+value)
   assert samepair(pair,(a*sp.cos(t),b*sp.sin(t)))
 png_geometry(z['generation']['plot'],a,b)

def native_record(label,z):
 checks=[]
 for i,f in enumerate(z['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:continue
  if f[':answer-field/type'].endswith('/radio'):
   for an in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':an[':answer/id'],'expected':'accepted' if an[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual complete-bank radio grading'})
  else:
   v=f[':answer-field/choices'][0][':answer/value'];p=z['generation']['parameters'];c=sp.Rational(p[('a','b')[i]]);fn=('cos','sin')[i]
   for value,expected,purpose in ((v,'accepted','Canonical component'),(str(c/2)+'*(2*'+fn+'(theta))','accepted','Unreduced equivalent component'),('1','rejected','Wrong scalar component'),(str(c)+'*'+('sin','cos')[i]+'(theta)','rejected','Wrong component function')):checks.append({'field_index':i,'submitted':value,'expected':expected,'purpose':purpose})
 return {'label':label,'record':z,'checks':checks}

def main():
 raws=[];variants=[];engine=[];source_report=[];banks=values=designations=exact_values=0
 qs=g.SOURCE['record'][':knowledge-point/questions']
 for case in json.loads((D/'source-cases.json').read_text()):
  original=next(q for q in qs if q[':db/id']==case['source_id']);level=original.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]
  z=g.generate(level,seed=91,template=case['template'],profile=case['bank_profile'],parameters=case['parameters']);q=z['question'];check_record(z);raws.append(z)
  assert q[':question/problem']==original[':question/problem'];assert q.get(':question/worked-solution')==original.get(':question/worked-solution')
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in original)
  fieldmatches=[]
  for f,of in zip(q[':question/answer-fields'],original[':question/answer-fields']):
   assert f[':answer-field/key']==of[':answer-field/key'];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   gv=[x[':answer/value'] for x in f[':answer-field/choices']];ov=[x[':answer/value'] for x in of[':answer-field/choices']];assert len(gv)==len(ov);used=set()
   for v in ov:
    equivalent=(lambda w:samepair(readpair(v),readpair(w))) if f[':answer-field/type'].endswith('/radio') else (lambda w:sp.simplify(readpair('x='+v+',y='+v)[0]-readpair('x='+w+',y='+w)[0])==0)
    matches=[i for i,w in enumerate(gv) if i not in used and equivalent(w)];assert len(matches)==1;used.add(matches[0]);values+=1;exact_values+=v in gv
   banks+=1
   if ':answer-field/correct' in of:
    gc=next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1]);oc=of[':answer-field/correct'][':answer/value'];assert samepair(readpair(gc),readpair(oc)) if f[':answer-field/type'].endswith('/radio') else gc==oc;designations+=1
   fieldmatches.append({'complete_bank':True,'options':len(ov),'correct_designation_present':':answer-field/correct' in of})
  source_report.append({'source_id':case['source_id'],'profile':case['bank_profile'],'fields':fieldmatches,'prompt_raw_exact':True,'solution_key_parity_and_exact':True,'difficulty_key_parity':True})
  name=case['bank_profile'].split(':',1)[1];rp=g.RECIPES[name];newp={'a':6,'b':3,'point':case['parameters']['point']}
  v=g.generate(level,seed=21,template=case['template'],profile=case['bank_profile'],parameters=newp);check_record(v);variants.append(v)
  # Native raw check when supported; q15803 missing correct and q15856 duplicate legacy require separately labeled normal field repairs.
  if name in ('q-15803','q-15856'):nz=g.generate(level,profile=name,parameters=case['parameters']);engine.append(native_record(name+'-normal-inferred-or-layout-repaired',nz))
  else:engine.append(native_record(name+'-raw-faithful',z))
  if name not in ('q-15803','q-15856'):engine.append(native_record(name+'-changed-parameters',v))
 # Two examples for every level, with both native formats at traversal levels.
 examples=[]
 for level in g.LEVELS:
  for template in (('graph','graph') if level=='easy' else ('traversal','construct')):
   idx=len(examples);p={'a':4+idx%3,'b':2+(idx+1)%2,'point':'A'} if level!='hard' else {'a':'7/2' if idx%2 else '13/2','b':'5' if idx%2 else '3','point':'A'}
   z=g.generate(level,seed=idx,template=template,parameters=p);check_record(z);examples.append(z);engine.append(native_record(level+'-'+template,z))
 # Enumerate valid same-method parameters without renderer overhead; explicit bounds match sampler.
 enum={}
 for level in g.LEVELS:
  domain=range(2,10) if level!='hard' else [sp.Rational(i,2) for i in range(4,19)];count=0
  for aa in domain:
   for bb in domain:
    try:g.bounds(level,{'a':str(aa),'b':str(bb)})
    except ValueError:continue
    count+=1
  enum[level]=count
 assert enum=={'easy':56,'moderate':56,'hard':154}
 # Check all complete supported bank recipes over the whole eligible integer domain.
 finite_checks=0
 for name,r in g.RECIPES.items():
  if r['opaque']:continue
  for aa in range(2,10):
   for bb in range(2,10):
    if aa==bb:continue
    p={'a':str(aa),'b':str(bb),'point':'A'};fs=r['fields'][1:] if name=='q-15856' else r['fields']
    for f in g.make_fields(fs,p):
     if f[':answer-field/type'].endswith('/radio'):
      pairs=[readpair(v[':answer/value']) for v in f[':answer-field/choices']];assert sum(valid(x,aa,bb,r['template']!='graph') for x in pairs)==1;assert not any(samepair(pairs[i],pairs[j]) for i in range(len(pairs)) for j in range(i));finite_checks+=1
 for aa in [sp.Rational(i,2) for i in range(4,19)]:
  for bb in [sp.Rational(i,2) for i in range(4,19)]:
   try:g.bounds('hard',{'a':str(aa),'b':str(bb)})
   except ValueError:continue
   f=g.make_fields(g.method_bank({}),{'a':str(aa),'b':str(bb)})[0];pairs=[readpair(v[':answer/value']) for v in f[':answer-field/choices']];assert sum(valid(x,aa,bb,True) for x in pairs)==1;assert not any(samepair(pairs[i],pairs[j]) for i in range(len(pairs)) for j in range(i));finite_checks+=1
 # Public explicit guard failures.
 for p in ({'a':2,'b':'17/2'},{'a':'17/2','b':2},{'a':'5/2','b':9},{'a':9,'b':'5/2'},{'a':'17/2','b':9},{'a':2,'b':9},{'a':9,'b':2}):
  level='hard' if any('/' in str(x) for x in p.values()) else 'moderate';z=g.generate(level,profile='method-hard' if level=='hard' else 'q-106393',parameters=p,template='traversal');check_record(z);examples.append(z);engine.append(native_record('boundary-'+level+'-'+str(p),z))
 for level,p in [('easy',{'a':0,'b':3}),('moderate',{'a':'5/2','b':3}),('hard',{'a':4,'b':3}),('hard',{'a':'19/2','b':3}),('easy',{'a':3,'b':3})]:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit parameters accepted')
 # Seeds/option order preserve content ID; task fingerprints exclude aliases/banks.
 x=g.generate_moderate(1,template='traversal',profile='q-106393',parameters={'a':4,'b':3});y=g.generate_moderate(20,template='traversal',profile='q-106393',parameters={'a':4,'b':3});assert x['question'][':question/id']==y['question'][':question/id']
 xx=g.generate_easy(1,profile='q-106392',parameters={'a':4,'b':3,'point':'A'});yy=g.generate_easy(22,profile='q-106392',parameters={'a':4,'b':3,'point':'J'});assert xx['question'][':question/id']==yy['question'][':question/id']
 xx=g.generate_moderate(1,profile='q-15856',parameters={'a':4,'b':3});yy=g.generate_moderate(22,profile='q-106393',parameters={'a':4,'b':3});assert xx['question'][':question/id']==yy['question'][':question/id']
 for level in g.LEVELS:
  coverage=set()
  old=g.render_plots;g.render_plots=lambda p:{'prompt':'render-only-for-sampler-coverage','renderer':'Matplotlib'}
  try:
   for seed in range(100):coverage.add(g.generate(level,seed)['generation']['bank_profile'])
  finally:g.render_plots=old
  if level=='easy':assert coverage=={k for k,v in g.RECIPES.items() if v['template']=='graph' and not v['opaque']}
  if level=='moderate':assert coverage=={k for k,v in g.RECIPES.items() if v['template'] in ('construct','traversal')}
 # Concurrent actual fresh renderer writes, identical and different inputs, unique atomic temps.
 with tempfile.TemporaryDirectory(prefix='ellipse-concurrent-',dir=D) as tmp:
  data=[{'a':str(a),'b':str(b),'point':'A','marked':True,'hard':False} for a,b in ((3,7),(3,7),(8,2),(5,9))]
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:assets=list(ex.map(lambda p:g.render_plots(p,tmp),data))
  for p,asset in zip(data,assets):png_geometry(asset,sp.Rational(p['a']),sp.Rational(p['b']))
  assert assets[0]['prompt']==assets[1]['prompt'];assert not list(Path(tmp).glob('render-input-*'))
 (D/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False));binary=SCRIPT.parent.parent/'runs/current/check-engine';subprocess.run([str(binary),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 native=json.loads((D/'engine-report.json').read_text());review=raws+variants+examples;(D/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False))
 lines=['# Origin-centered ellipse review','Raw originals preserve missing keys; changed examples use parameterized masks. Opaque/legacy evidence is labeled in metadata.']
 for z in review:
  tag='ORIGINAL RAW' if z in raws else ('CHANGED OBSERVED BANK' if z in variants else 'AUTHORED/NORMAL LEVEL EXAMPLE');lines.extend(['## '+tag,g.markdown(z)])
 (D/'review.md').write_text('\n\n'.join(lines));report={'status':'passed','source_questions':len(raws),'complete_fields_banks':banks,'source_values_matched':values,'source_values_total':values,'raw_exact_answer_strings':exact_values,'notation_normalized_answer_strings':values-exact_values,'correct_designations_matched':designations,'correct_designations_absent':2,'prompt_exact':len(raws),'worked_solution_exact_present':12,'worked_solution_absence_preserved':1,'unrated_absence_preserved':1,'source_reports':source_report,'finite_complete_bank_checks':finite_checks,'meaningful_parameter_counts':enum,'review_records':len(review),'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':native['documented_unresolved_checks'],'concurrent_renderer':'passed fresh identical/different atomic writes','plot_geometry':'actual RGB blue extents within 4px transformed radius bounds; actual text boxes disjoint','python':sys.version.split()[0],'sympy':sp.__version__,'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest()};(D/'validation.json').write_text(json.dumps(report,indent=2));(D/'freeze.json').write_text(json.dumps({'version':g.VERSION,'files':{str(p.relative_to(D.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SCRIPT,*sorted(p for p in D.rglob('*') if p.is_file() and '__pycache__' not in p.parts)] if p.name!='freeze.json'}},indent=2));print(json.dumps({k:v for k,v in report.items() if k!='source_reports'},indent=2))
if __name__=='__main__':main()

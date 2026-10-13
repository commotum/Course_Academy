"""Root checks actual offered fields, every plot vector and explanatory predicate."""
import importlib.util,json,re,hashlib,itertools
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186172084;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_field_reader',R/'planar-field-readback.py');g=module('root_field_identification',D.with_suffix('.py'));s=p.s;x,y=p.x,p.y
# Independently verified against all nine captured diagrams, not generator data.
ORIGINAL={'q-122296':(x,-1),'q-122463':(-1,1),'q-122629':(1,x),'q-122631':(0,-y),'q-122632':(0,x),'q-122633':(y,0),'q-122634':(1,0),'q-122637':(0,-5),'q-122630':(-2,y)}
ORIGINAL={name:tuple(s.sympify(v) for v in pair) for name,pair in ORIGINAL.items()}
C=dict(instances=0,displayed_formulas=0,plot_vector_checks=0,explanation_predicates=0,elimination_checks=0,source_questions=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs=0,source_raw_exact_solutions=0,source_repaired_solutions=0)
meaningful={};fingerprints={}
def check(r):
 q=r['question'];f=q[':question/answer-fields'][0];offer={};ids={}
 for a in f[':answer-field/choices']:
  if a[':answer/value']=='None of the listed':continue
  name,pair=p.formula(a[':answer/value']);offer[name]=pair;ids[name]=a[':answer/id']
 assert len(offer)==4 and len(set(offer.values()))==4
 correct=next(name for name in offer if ids[name]==f[':answer-field/correct'][1]);pair=offer[correct];meta=r['generation'];plot=meta['plots'];actual_path=Path(re.search(r'!\[\]\(([^)]+)\)',q[':question/problem'])[1]);assert actual_path==Path(plot['prompt'])
 if plot['renderer']=='captured-source':
  source_id=meta['bank_profile'];assert pair==ORIGINAL[source_id];old=g.QUESTIONS[source_id];ref=re.search(r'!\[\]\(([^)]+)\)',old[':question/problem'])[1];assert hashlib.sha256(actual_path.read_bytes()).digest()==hashlib.sha256((Path('/media/jake/SSD/EDB/math')/ref).read_bytes()).digest()
 else:
  side=json.loads(Path(plot['sidecar']).read_text());assert side['renderer']=='Matplotlib';assert 0<side['display_scale']<=1
  matches=[]
  for name,field in offer.items():
   good=True
   for a,b,u,v in side['points']:
    a,b,u,v=map(s.Rational,(a,b,u,v));good &= all(s.expand(expr.subs({x:a,y:b})-want)==0 for expr,want in zip(field,(u,v)));C['plot_vector_checks']+=2
   if good:matches.append(name)
  assert matches==[correct],matches
 worked=q[':question/worked-solution'];all_printed=p.formulas(worked);assert len(all_printed)==4,(worked,all_printed)
 assert all(offer[name]==field for name,field in all_printed) and all_printed[-1]==(correct,pair)
 bullets=re.findall(r'- ([\s\S]*?)\n\n\$\$\n([\s\S]*?)\n\$\$',worked);assert len(bullets)==2
 eliminated=[]
 for prose,formula_block in bullets:
  predicates=p.prose_predicates(prose);assert all(test(pair) for test in predicates),(prose,pair)
  C['explanation_predicates']+=len(predicates)
  for name,field in p.formulas('$$'+formula_block+'$$'):
   assert not all(test(field) for test in predicates),(prose,name,field);eliminated.append(name);C['elimination_checks']+=1
 assert sorted(eliminated)==sorted(set(offer)-{correct})
 # Root-normalized actual qualitative shape; align task identity across source aliases.
 coefficients=[z for e in pair for z in s.Poly(e,x,y).coeffs() if z];common=abs(s.gcd_list(coefficients));shape=tuple(s.expand(e/common) for e in pair);level=q[':question/difficulty'].split('/')[-1];meaningful.setdefault(level,set()).add(shape)
 fingerprint=meta['mathematical_fingerprint'];assert fingerprints.setdefault(shape,fingerprint)==fingerprint,(shape,'cross-profile common-scale identity mismatch')
 if level=='hard':assert all(e.free_symbols and s.Poly(e,x,y).total_degree()==1 for e in pair)
 C['instances']+=1;C['displayed_formulas']+=len(offer);return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
cases=json.loads((D/'source-cases.json').read_text());case_by_source={case['source_id']:case for case in cases}
for case in cases:
 old=sources[case['source_id']];q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));C['source_questions']+=1
 assert re.sub(r'!\[\]\([^)]*\)','IMAGE',q[':question/problem'])==re.sub(r'!\[\]\([^)]*\)','IMAGE',old[':question/problem'])
 sf=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in sf[':answer-field/choices'])==sorted(z[':answer/value'] for z in nf[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(sf[':answer-field/choices'])
 if sf.get(':answer-field/correct'):
  val=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert val==sf[':answer-field/correct'][':answer/value'];C['source_existing_refs']+=1
 else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):
  expected=old[':question/worked-solution']
  if case['source_id']=='q-122629':expected=expected.replace(r'F(x,y)=-i+x\,j',r'F(x,y)=-i-j');C['source_repaired_solutions']+=1
  else:C['source_raw_exact_solutions']+=1
  assert q[':question/worked-solution']==expected
review=json.loads((D/'review.json').read_text())
for item in review['generated']:check(item)
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
# Exhaust every actual supported transform, including signed common magnitude.
for sid,definition in g.PROFILES.items():
 for sx,sy,swap,a in itertools.product((-1,1),(-1,1),(False,True),(-1,1)):
  check(g.generate(definition[0],template=case_by_source[sid]['template'],profile=sid,parameters=dict(sx=sx,sy=sy,swap=swap,a=a)))
for sx,sy,swap in itertools.product((-1,1),(-1,1),(False,True)):check(g.generate('hard',parameters=dict(sx=sx,sy=sy,swap=swap,a=1)))
C['finite_actual_qualitative_tasks']={level:len(vals) for level,vals in meaningful.items()};C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)

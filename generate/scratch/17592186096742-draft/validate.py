"""Private validation reading actual nested givens, component labels and all rows."""
import copy, hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'draft');P=load(HERE/'math_parser.py','independent_parser')
x=P.x;u=s.Symbol('u',real=True);v=s.Symbol('v',real=True)
def save(name,o):(HERE/name).write_text(json.dumps(o,indent=2,ensure_ascii=False,default=str)+'\n')
def scalar(t):return P.scalar(t.strip().rstrip('.,'))
def equal(a,b):return P.equal(a,b)
def label(t):return re.sub(r'\s+','',t)
def differential(symbol,variable):return r'\frac{\text{d}'+symbol+r'}{\text{d}'+variable+'}'
def equivalent(a,b):return equal(a,b)
def read(rec,determinism=True):
 q=rec['question'];md=rec['generation'];m=md['template'];p=md['parameters'];raw=md['evidence_only']
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 assert md['source_basis']==2275 and md['source_lineage']=='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
 assert md['eligible_for_learning']==(not raw)
 prompt=q[':question/problem'];fun,point=P.given(prompt);derivative=s.diff(fun,x)
 a=p.get('a');b=p.get('b')
 documented={'q-48569':s.cos(a*x)**3 if a else None,'q-48570':s.sin(a*x)**3 if a else None,'q-312907':s.cos(a*x**3)**8 if a else None,'q-2397':s.sin(a*x**2-1)**3 if a else None,'q-31352':s.cot((x+b)**2) if b else None,'q-31361':s.cot(a*x-b)**4 if a and b else None,'q-16699':s.cos(a*x**2+b)**3 if a and b else None,'q-28655':s.Integer(a)**s.log(s.cos(x)) if a else None,'q-342927':s.sqrt(s.cos(2*x-b)) if b else None}
 assert equal(fun,documented[m]),'Actual given is stale relative to bounded slots'
 prose_only=lambda t:re.sub(r'\$\$.*?\$\$|\$[^$]*\$','@MATH@',t,flags=re.S)
 assert prose_only(prompt)==prose_only(g.SOURCES[m][':question/problem'])
 # Independently bind each function from the actual printed nested definition.
 symbol=re.search(r'\$([fhy])(?:\(x\))?\s*=',prompt)[1]
 assessed=derivative.subs(x,point) if point is not None else derivative
 if m=='q-312907':
  tail=prompt.split('{{field-1}}',1)[1];frag=scalar(re.search(r'\$([^$]+)\$',tail)[1]);assessed=s.simplify(derivative/frag)
  assert assessed.is_polynomial(x) and s.degree(assessed,x)==2
 elif m=='q-342927':
  denominator=scalar(re.findall(r'\$([^$]+)\$',prompt)[-1]);assessed=s.simplify(derivative*denominator)
 fields=q.get(':question/answer-fields',[])
 if m=='q-16699':assert not fields and raw
 else:
  assert len(fields)==1;f=fields[0];ft=f[':answer-field/type'];key=f[':answer-field/key']
  assert key==('field-1' if m in ('q-312907','q-342927') else 'selection')
  assert ft==(':answer-field.type/blank' if m in ('q-312907','q-342927') else ':answer-field.type/radio')
  assert prompt.count('{{'+key+'}}')==(1 if ft.endswith('/blank') else 0)
  values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(values)==(1 if ft.endswith('/blank') else 5)
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(values)
  if ':answer-field/correct' in f:
   correct=next(scalar(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(correct,assessed),(m,p,'wrong correct fragment',correct,assessed)
  else:assert raw and m in ('q-48569','q-48570')
  assert sum(equal(val,assessed) for val in values)==1,(m,p,'correct designation count')
  assert all(not equal(a,b) for i,a in enumerate(values) for b in values[i+1:]),(m,p,'bank ambiguity')
  # Independent complete-bank formulas derive all arguments/scales from actual
  # given composition, including compound errors and intentionally omitted factors.
  if m in ('q-48569','q-48570'):
   trig=s.cos if m=='q-48569' else s.sin
   z=next(iter(fun.atoms(trig))).args[0];a=s.diff(z,x)
   expected=[assessed,-3*a*s.cos(x)**2*s.sin(x),-3*s.sin(z)**2,3*a*s.sin(z)**2*s.cos(z),3*s.cos(z)**2*s.sin(z)] if m=='q-48569' else [assessed,3*s.sin(z)**2*s.cos(z),3*a*s.sin(x)**2*s.cos(x),3*a*s.sin(z)*s.cos(z),3*s.sin(x)*s.cos(x)]
  elif m=='q-2397':
   z=next(iter(fun.atoms(s.sin))).args[0];a=s.Poly(z,x).coeff_monomial(x**2)
   expected=[assessed,3*x*s.sin(z)**2*s.cos(z)**2,2*a*x*s.sin(z)**2*s.cos(z)**2,2*a*x*s.sin(z)**2*s.cos(z),6*a*x*s.sin(z)**3*s.cos(z)**3]
  elif m=='q-31352':
   z=next(iter(fun.atoms(s.cot))).args[0];b=s.Poly(s.expand(z),x).coeff_monomial(x)/2
   expected=[assessed,-s.csc(z)**2,2*x*s.csc(z)**2,-2*(x+b)*s.csc(x+b),4*(x+b)]
  elif m=='q-31361':
   z=next(iter(fun.atoms(s.cot))).args[0];a=s.diff(z,x);b=-z.subs(x,0)
   expected=[assessed,a*s.cot(b)**3*s.sec(b)**2,-4*s.cot(b)**2*s.csc(b)**2,4*a*s.cot(b)*s.sec(b)**2,-4*s.cot(b)**3*s.csc(b)**2]
  elif m=='q-28655':
   base=next(z for z in fun.atoms(s.Pow) if z.exp.has(s.log)).base;expected=[assessed,-1,-base,base,1]
  else:expected=[assessed]
  assert all(sum(equal(a,b) for b in values)==1 for a in expected),'Incomplete original bank recipe reconstruction'
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==(4 if point is not None else 3)
  # Parse every composition-layer binding; the first row's source typo omits
  # one comma only in q28655 and is independently made parseable without math edit.
  decomposition=blocks[0].replace(r'v\,v=',r'v,\,v=')
  parts=re.split(r',\\(?:,|quad|qquad)',decomposition.strip());assert len(parts)==3
  bindings=[t.split('=',1) for t in parts];assert [label(a) for a,b in bindings]==[symbol,'u','v']
  objects=[scalar(b) for a,b in bindings];outer,middle,inner=objects
  assert outer.free_symbols<= {u} and middle.free_symbols<= {v} and inner.free_symbols<= {x}
  assert equal(fun,outer.subs(u,middle).subs(v,inner)),'Wrong function layer input'
  # Operator numerator/denominator labels themselves are assessed, not skipped.
  rows=re.split(r',\\(?:,|quad|qquad)',blocks[1].strip());assert len(rows)==3
  expected_ops=[differential(symbol,'u'),differential('u','v'),differential('v','x')]
  ders=[]
  for row,op,expected in zip(rows,expected_ops,[s.diff(outer,u),s.diff(middle,v),s.diff(inner,x)]):
   lhs,rhs=row.split('=',1);assert label(lhs)==label(op),(m,'formal derivative input',lhs,op)
   obj=scalar(rhs);assert equal(obj,expected),(m,p,'wrong component derivative',obj,expected);ders.append(obj)
  # Ordered formal chain operators and ALL numerical/substituted factors/rows.
  aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(aligned)==(2 if point is not None else 1)
  chain_rows=re.split(r'\\\\',aligned[0]);assert len(chain_rows)>=4
  lhs,rhs=chain_rows[0].split('&',1);assert label(lhs)==label(differential(symbol,'x'))
  formal=[differential(symbol,'u')+r'\cdot '+differential('u','x'),differential(symbol,'u')+r'\cdot '+differential('u','v')+r'\cdot '+differential('v','x')]
  for row,expected in zip(chain_rows[:2],formal):assert label(row.split('&',1)[1].lstrip().removeprefix('='))==label(expected),'Formal factor chain inputs wrong'
  # Explicit three-factor product is required before substitution.
  first_values=chain_rows[2].split('&',1)[1].strip().removeprefix('=');factors=first_values.split(r'\cdot');assert len(factors)==3
  for factor,expected in zip(factors,ders):assert equal(scalar(factor),expected),'Wrong assessed chain factor'
  for row in chain_rows[2:]:
   lhs,rhs=row.split('&',1);assert not lhs.strip();obj=scalar(rhs.strip().removeprefix('='));obj=obj.subs(u,middle).subs(v,inner)
   assert equal(obj,derivative),(m,p,'wrong intermediate stage',rhs,obj,derivative)
  if point is not None:
   # Read the target independently from prose and each displayed evaluation.
   prose=sol.split('Now we compute',1)[1];inline=re.search(r'\$([^$]+)\$',prose)[1]
   assert re.search(r'\('+str(point)+r'\)',inline)
   eval_rows=re.split(r'\\\\',aligned[1]);lhs=eval_rows[0].split('&',1)[0]
   assert re.search(r'\{'+symbol+r'\}\^\{(?:′|\x27)\}\('+str(point)+r'\)',lhs)
   for row in eval_rows:
    val=scalar(row.split('&',1)[1].strip().removeprefix('='));assert equal(val,derivative.subs(x,point)),(m,p,'evaluation stage',row)
  # Preserve every source instructional sentence/ordered stage outside math.
  source=g.SOURCES[m]
  if ':question/worked-solution' in source:
   prose_only=lambda t:re.sub(r'\$\$.*?\$\$|\$[^$]*\$','@MATH@',t,flags=re.S)
   assert prose_only(sol)==prose_only(source[':question/worked-solution'])
 if m in ('q-31352','q-31361'):
  arg=next(iter(fun.atoms(s.cot))).args[0];assert md['domain']['restriction']==g.tex(arg)+r'\notin\pi\mathbb{Z}'
 elif m=='q-28655':assert md['domain']['restriction']==r'\cos(x)>0'
 elif m=='q-342927':
  arg=next(iter(fun.atoms(s.cos))).args[0];assert md['domain']['restriction']==r'\cos('+g.tex(arg)+')>0'
 else:assert md['domain']['restriction']=='all real x'
 for text in [prompt]+([q[':question/worked-solution']] if ':question/worked-solution' in q else [])+[a[':answer/value'] for f in fields for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0 and all(ord(c)>=32 or c in '\n\t' for c in text)
 if determinism:assert rec==g.generate(md['level'],md['seed'],m,p,md['profile'])
 return fun,assessed

def raw_fidelity(rec,src):
 q=rec['question']
 for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
  assert (key in src)==(key in q),(src[':question/math-academy-id'],key,'presence')
  if key in src and key not in (':question/answer-fields',':question/difficulty'):assert q[key]==src[key]
 if ':question/difficulty' in src:assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
 fs=q.get(':question/answer-fields',[]);old=src.get(':question/answer-fields',[]);assert len(fs)==len(old)
 for f,o in zip(fs,old):
  assert f[':answer-field/key']==o[':answer-field/key'] and f[':answer-field/type']==o[':answer-field/type'][':db/ident']
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in o[':answer-field/choices']]
  assert (':answer-field/correct' in f)==(':answer-field/correct' in o)
  if ':answer-field/correct' in o:
   ca=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ca==o[':answer-field/correct'][':answer/value']

def checks(rec):
 fs=rec['question'].get(':question/answer-fields',[])
 if not fs or ':answer-field/correct' not in fs[0]:return []
 f=fs[0]
 if f[':answer-field/type'].endswith('/radio'):return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Native ID grading of every complete source-bank option'} for a in f[':answer-field/choices']]
 a=f[':answer-field/choices'][0][':answer/value'];return [{'field_index':0,'submitted':val,'expected':e,'purpose':'Canonical / unreduced equivalent / ordinary incorrect blank fragment'} for val,e in ((a,'accepted'),('2('+a+')/2','accepted'),('0','rejected'),('1','rejected'),('('+a+')+1','rejected'))]
def must_fail(fn):
 try:fn()
 except (AssertionError,ValueError,StopIteration):return
 raise AssertionError('Negative control accepted')

def main():
 frozen=json.loads((ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186096742.json').read_text());assert frozen==json.loads((HERE/'source.json').read_text())
 manifest=json.loads((ROOT/'generate/runs/current/manifest.json').read_text());job=next(j for j in manifest['jobs'] if j['kp_id']==g.KP_ID);assert job['source_basis']==2275 and job['source_snapshot_root']=='generate/runs/current/refresh-2026-10-14';assert manifest['source_snapshot_roots']['2275']=='refresh-2026-10-14'
 raw=[];cases=[]
 for m,src in g.SOURCES.items():
  print('Original',m,flush=True);r=g.generate(g.DIFFICULTIES[m],template=m,parameters=g.DEFAULTS[m],profile='observed_raw');raw_fidelity(r,src);read(r);raw.append(r)
  cases.append({'source_id':m,'level':g.DIFFICULTIES[m],'template':m,'parameters':g.DEFAULTS[m],'profile':'observed_raw','authored_level':g.DIFFICULTIES[m] if ':question/difficulty' not in src else None})
 save('source-cases.json',cases)
 normal=[];reviews=[]
 for m in g.SOURCES:
  print('Finite family',m,flush=True)
  if m=='q-28655':
   family=[g.generate('hard',template=m,parameters={'a':5},profile='source-compatibility')];read(family[0]);normal+=family;reviews+=family
  elif m not in g.RAW_ONLY:
   family=[g.generate(g.DIFFICULTIES[m],i,m,p) for i,p in enumerate(g.parameters_for(m))]
   for r in family:read(r)
   normal+=family;reviews += [family[0],family[-1]]
  # Changed-bound raw evidence uses the identical parameterized source backbone.
  for p in (g.parameters_for(m,True)[0],g.parameters_for(m,True)[-1]):
   r=g.generate(g.DIFFICULTIES[m],template=m,parameters=p,profile='observed_raw');read(r);reviews.append(r)
 default_coverage={};counts={}
 for lv in g.LEVELS:
  default=[g.generate(lv,i) for i in range(80)]
  assert {r['generation']['template'] for r in default}=={m for m in g.SOURCES if g.DIFFICULTIES[m]==lv and m not in g.RAW_ONLY and m!='q-28655'}
  for r in default:read(r)
  default_coverage[lv]=sorted({r['generation']['template'] for r in default});counts[lv]=len({r['generation']['mathematical_fingerprint'] for r in normal if r['generation']['level']==lv})
 negatives=0
 for m in g.SOURCES:
  invalid={k:99 for k in g.DEFAULTS[m]};must_fail(lambda:g.generate(g.DIFFICULTIES[m],template=m,parameters=invalid,profile='observed_raw'));negatives+=1
  must_fail(lambda:g.generate(next(l for l in g.LEVELS if l!=g.DIFFICULTIES[m]),template=m,profile='observed_raw'));negatives+=1
  if m in g.RAW_ONLY or m=='q-28655':must_fail(lambda:g.generate(g.DIFFICULTIES[m],template=m));negatives+=1
  else:
   for profile in (None,'default'):
    a=g.generate(g.DIFFICULTIES[m],0,m,g.DEFAULTS[m],profile);b=g.generate(g.DIFFICULTIES[m],91,m,g.DEFAULTS[m],profile);assert a['question'][':question/id']==b['question'][':question/id']
 for b in (25,31):must_fail(lambda:g.generate('moderate',template='q-342927',parameters={'b':b}));negatives+=1
 for args in ({'level':'easy','template':'q-48569','parameters':{'a':1}}, {'level':'easy','template':'q-48569','parameters':{'a':True}},{'level':'hard','template':'q-31361','parameters':{'a':1,'b':0}}, {'level':'moderate','template':'q-312907','field_type':'radio'},{'level':'easy','profile':'random'}):must_fail(lambda:g.generate(**args));negatives+=1
 # Independent reader mutation controls: no regeneration shortcut necessary.
 base=g.generate('hard',template='q-31361',parameters={'a':5,'b':2})
 for name in ('prompt','binding','operator','factor','stage','target','bank','designation','domain','prose','control'):
  r=copy.deepcopy(base);q=r['question'];sol=q[':question/worked-solution']
  if name=='prompt':q[':question/problem']=q[':question/problem'].replace('5x-2','5x-3')
  if name=='binding':q[':question/worked-solution']=sol.replace('v=5x-2','v=5x-3')
  if name=='operator':q[':question/worked-solution']=sol.replace(r'\frac{\text{d}u}{\text{d}v}',r'\frac{\text{d}u}{\text{d}x}',1)
  if name=='factor':q[':question/worked-solution']=sol.replace(r'\cdot 5',r'\cdot 4',1)
  if name=='stage':q[':question/worked-solution']=sol.replace('=-20{','=-21{',1)
  if name=='target':q[':question/worked-solution']=sol.replace('Now we compute ${f}^{′}(0)','Now we compute ${f}^{′}(1)')
  if name=='bank':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='0'
  if name=='designation':q[':question/answer-fields'][0][':answer-field/correct'][1]=str(uuid.uuid4())
  if name=='domain':r['generation']['domain']['restriction']='all real x'
  if name=='prose':q[':question/worked-solution']=sol.replace('Applying now the chain rule twice','Applying the product rule')
  if name=='control':q[':question/worked-solution']+='\x0c'
  must_fail(lambda:read(r,False));negatives+=1
 # Slot changes hold the other hard parameter constant and read ALL labels.
 for p in ({'a':5,'b':1},{'a':5,'b':3},{'a':7,'b':1}):read(g.generate('hard',template='q-31361',parameters=p))
 cli=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','all','--count','1','--format','json'],capture_output=True,text=True,check=True);assert len(json.loads(cli.stdout))==3
 save('review.json',{'original_replays':raw,'generated_variants':reviews})
 (HERE/'review.md').write_text('# Repeated chain rule private draft\n\nRaw replay preserves omissions and is evidence-only. Easy is tentatively authored from unrated MA trig cubics. Fieldless source excluded from normal API; q342927 normal shifts bounded1..24, raw-only expanded bounds expose engine gap.\n\n'+'\n\n'.join('## '+('MA original' if r in raw else 'Changed parameter')+' '+r['generation']['template']+' / '+r['generation']['profile']+'\n\n'+g.markdown(r) for r in raw+reviews)+'\n')
 save('previews.json',normal)
 engine=[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(raw+normal) if checks(r)]
 save('native-input.json',engine);binary=ROOT/'generate/runs/current/check-engine';assert hashlib.sha256(binary.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 run=subprocess.run([str(binary),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],capture_output=True,text=True);(HERE/'native.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
 native=json.loads((HERE/'native-grading.json').read_text());assert native['documented_unresolved_checks']==0
 # Changed-shift RAW evidence outside every normal bound documents engine gap.
 exclusion=g.generate('moderate',template='q-342927',parameters={'b':31},profile='observed_raw');probe=checks(exclusion)
 for check in probe:
  fixture=[{'label':'excluded-raw-q-342927','record':exclusion,'checks':[check]}];save('raw-exclusion-input.json',fixture)
  result=subprocess.run([str(binary),str(HERE/'raw-exclusion-input.json'),str(HERE/'raw-exclusion-output.json')],capture_output=True,text=True)
  if result.returncode:
   assert 'got unresolved' in result.stderr,result.stderr;check['expected']='unresolved';check['purpose']='Changed-shift raw evidence outside ALL normal bounds: native engine cannot resolve ordinary incorrect nested-trig entry'
 save('raw-exclusion-input.json',[{'label':'excluded-raw-q-342927','record':exclusion,'checks':probe}]);run=subprocess.run([str(binary),str(HERE/'raw-exclusion-input.json'),str(HERE/'raw-exclusion-grading.json')],capture_output=True,text=True);assert run.returncode==0,run.stderr
 baseline=json.loads((HERE/'registered-baseline.json').read_text());paths=[ROOT/'generate/scratch/17592186096742.py']+sorted(p for p in (ROOT/'generate/scratch/17592186096742').rglob('*') if p.is_file());assert {str(p) for p in paths}==set(baseline);assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline.items())
 inv=json.loads((HERE/'independent-inventory.json').read_text());assert inv['basis']==2275 and inv['lineage']==frozen['lineage'];assert [q['record'] for q in inv['questions']]==[q for q in frozen['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 report={'status':'pass','draft_only':True,'basis':2275,'original_MA_count':len(raw),'independent_inventory_exact':len(inv['questions']),'source_coverage':{'prompts':9,'solutions':7,'fields':8,'values':32,'refs':6,'missing_refs':2,'unrated':2,'fieldless':1},'exhaustive_normal_records':len(normal),'meaningful_tasks_per_level':counts,'default_family_coverage':default_coverage,'negative_and_mutation_checks':negatives,'raw_only_exclusions':g.RAW_ONLY,'all_normal_API_parameter_bounds_native_tested':True,'raw_nested_trig_engine_report':'raw-exclusion-grading.json','native_grading':{k:native[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'registered_baseline_unchanged':True,'complete_bank_coverage':{'original_choices':32,'matched_choices':32,'original_radio_banks':6,'matched_radio_banks':6,'raw_original_bank_correct_refs':4,'authored_missing_key_banks':2},'limits':['Easy ratings are tentative authored assignments; original source grade/key/solution omissions remain exact in raw evidence.','q342927 normal b1..24 bounds are exhaustively native tested; all normal calls reject b25..31, whose raw probes retain unresolved wrong0 evidence.','Fieldless q16699 is raw-only; q28655 has faithful fixed-base normal compatibility profile. The 15 raw base values collapse to one semantic task and are not counted as inventory.','Hard offset slot b is a conservative same-workload extension; all composition derivatives/evaluation rows/complete compound banks use that argument.'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',HERE/'math_parser.py',HERE/'math_format.py',binary]}}
 save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()

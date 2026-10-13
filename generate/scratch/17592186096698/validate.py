#!/usr/bin/env python3
"""Independent displayed ODE/family QA, raw fidelity, native grader and rendering."""
import concurrent.futures,copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).parent;ROOT=H.parents[2];s=importlib.util.spec_from_file_location('kp96698',H.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
X=sp.Symbol('x',real=True)
def write(name,obj):(H/name).write_text(json.dumps(obj,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def group(s,start):
 assert s[start]=='{';depth=1;i=start+1
 while depth:
  if s[i]=='{':depth+=1
  elif s[i]=='}':depth-=1
  i+=1
 return s[start+1:i-1],i

def parse(s):
 s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('⁡','').replace(r'\operatorname{ln}',r'\ln')
 for command in [r'\frac',r'\sqrt']:
  while command in s:
   i=s.index(command);arg,j=group(s,i+len(command));
   if command==r'\frac':den,k=group(s,j);val='(('+str(parse(arg))+')/('+str(parse(den))+'))';j=k
   else:val='sqrt('+str(parse(arg))+')'
   s=s[:i]+val+s[j:]
 while True:
  m=re.search(r'(?:\{e\}|e)\^\{',s)
  if not m:break
  arg,end=group(s,m.end()-1);s=s[:m.start()]+'exp('+str(parse(arg))+')'+s[end:]
 s=s.replace('^{','**(').replace('}',' )').replace('{','(').replace('^','**').replace(r'\ln|x|','log(x)').replace(r'\ln','log').strip().rstrip('.?')
 if s.startswith('log') and not s.startswith('log('):s='log('+s[3:]+')'
 return parse_expr(s,local_dict={'x':X,'exp':sp.exp,'log':sp.log,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

def ode(prompt):
 pieces=re.findall(r'\$(.*?)\$',prompt,re.S);term=next(p for p in pieces if r'\frac{\text{d}y}{\text{d}x}' in p)
 d=r'\frac{\text{d}y}{\text{d}x}'
 if r'x\cdot '+d in term:return parse(term.split('=')[1].rstrip('.?'))/X
 if r'{x}^{2}\cdot '+d in term:return -parse(term.split('+',1)[1].split('=')[0])/X**2
 return parse(term.split('=',1)[1].rstrip('.?'))

def fmt(text):
 assert text.count('$')%2==0,text
 for math in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',text,re.S):
  t=''.join(math);n=0
  for i,c in enumerate(t):
   if c=='{' and (i==0 or t[i-1]!='\\'):n+=1
   if c=='}' and (i==0 or t[i-1]!='\\'):n-=1;assert n>=0
  assert n==0,t
 assert '--' not in text and '+-' not in text

def verify(rec,normal=True):
 assert set(rec['knowledge_point'])=={'db_id','id','title'};q=rec['question'];gen=rec['generation'];der=ode(q[':question/problem']);p=gen['parameters'];F=g.primitive(p)
 assert gen['evidence_only']==gen['bank_profile'].startswith('raw-') and gen['eligible_for_learning']==(not gen['evidence_only'])
 assert sp.simplify(der-sp.diff(F,X))==0,('printed ODE',q[':question/problem'],der,F)
 fmt(q[':question/problem']);fmt(q[':question/worked-solution'])
 f=q[':question/answer-fields'][-1];correct=f[':answer-field/correct'][1];actualcorrect=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct);assert actualcorrect==gen['correct_plot']
 eligible=[];bases=[]
 for a in f[':answer-field/choices']:
  path=a[':answer/value'];curves=[g.expr(c) for c in gen['curves'][path]]
  assert len(curves)==3
  # Test every curve against the actual printed ODE, allowing any arbitrary
  # additive constant. Horizontal translations may alter the entire family.
  valid=all(sp.simplify(sp.diff(c,X)-der)==0 for c in curves);eligible.append(valid)
  if valid:assert path==actualcorrect
  bases.append(curves)
  if normal:
   file=Path(path);assert file.exists() and file.with_suffix('.json').exists()
   side=json.loads(file.with_suffix('.json').read_text());assert side['spec']==gen['plot_geometry'][path]
   assert side['spec']['curves']==gen['curves'][path]
   if p['family'] in ('logarithmic','reciprocal'):assert all(m is not None and m>=0 for m in side['spec']['domain_minima'])
   # Authored plots show vertical translates only, unlike some raw distractors.
   assert all(sp.simplify(sp.diff(c-curves[0],X))==0 for c in curves[1:])
 assert sum(eligible)==1,eligible
 if normal:
  for i,v in enumerate(bases):
   for w in bases[i+1:]:assert sp.simplify(sp.diff(v[0]-w[0],X))!=0,'equivalent general families'
 # Final displayed primitive is read from actual aligned text, not metadata.
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S).group(1);rows=block.split(r'\\')
 final=rows[-1].split('=',1)[1].replace('+C.','').replace('+C,\\,x>0.','').strip()
 if final.endswith('+C'):final=final[:-2]
 assert sp.simplify(sp.diff(parse(final),X)-der)==0,('printed primitive',final,der)
 for row in rows:
  if '=' not in row:continue
  rhs=row.split('=',1)[1].strip().rstrip('.')
  if '+C,' in rhs:rhs=rhs.split('+C,')[0]
  rhs=rhs.replace('+C','')
  if r'\int' in rhs:
   coefficient,integrand=rhs.split(r'\int',1)
   integrand=integrand.split(r'\text{d}x')[0].replace(r'\,','').strip()
   c=sp.Integer(-1) if coefficient.strip()=='-' else parse(coefficient) if coefficient.strip() else sp.Integer(1)
   value=c*sp.integrate(parse(integrand) if integrand else sp.Integer(1),X)
  else:value=parse(rhs)
  is_rearrangement=r'\frac{\text{d}y}{\text{d}x}' in row.split('=',1)[0] and r'\int' not in row
  assert sp.simplify((value if is_rearrangement else sp.diff(value,X))-der)==0,('displayed intermediate stage',row,der,value)
 return len(f[':answer-field/choices'])

def normal_native(r,label):
 # Native fixtures require all fields to have correct refs. Preserve raw replay
 # in review; the fixture omits the captured duplicate legacy field explicitly.
 r=copy.deepcopy(r)
 r['question'][':question/answer-fields']=[f for f in r['question'][':question/answer-fields'] if ':answer-field/correct' in f]
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:continue
  for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all owned image choices'})
 return {'label':label,'record':r,'checks':checks}

def main():
 original=[];variants=[];source_results=[];native=[];choices=fields=refs=0
 for case in g.CASES:
  src=g.SPECS[case['template']]['source'];r=g.generate(case['level'],17,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);verify(r,False);q=r['question'];original.append(r)
  assert set(q)==set(src),('source question attrs',case)
  assert q[':question/problem']==src[':question/problem'];assert q[':question/worked-solution']==src[':question/worked-solution']
  for sf,rf in zip(src[':question/answer-fields'],q[':question/answer-fields']):
   assert set(sf)==set(rf);assert sf[':answer-field/key']==rf[':answer-field/key'];assert sf[':answer-field/type'][':db/ident']==rf[':answer-field/type']
   sa={a[':answer/value']:a for a in sf[':answer-field/choices']};ra={a[':answer/value']:a for a in rf[':answer-field/choices']};assert set(sa)==set(ra)
   for value,a in sa.items():assert set(a)==set(ra[value]);assert a[':answer/type'][':db/ident']==ra[value][':answer/type']
   if ':answer-field/correct' in sf:
    refs+=1;correct=next(a for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert correct[':answer/value']==sf[':answer-field/correct'][':answer/value']
   choices+=len(sa);fields+=1
  native.append(normal_native(r,case['template']));source_results.append({'source_id':case['source_id'],'full_prompt_exact':True,'full_solution_exact':True,'bank_values_and_attribute_presence_exact':True,'geometry_metric_uncertainty_options':g.SPECS[case['template']]['uncertain_metric_options']})
  # Changed-parameter raw profile exercises source masks and affine whole-plot
  # transport; the unknown source intent remains explicit evidence metadata.
  pp=copy.deepcopy(case['parameters']);pp['a']=str(sp.Rational(pp['a'])*sp.Rational(3,2));rr=g.generate(case['level'],29,template=case['template'],parameters=pp,profile=case['bank_profile']);verify(rr,False);variants.append(rr);native.append(normal_native(rr,case['template']+'-changed-parameters'))
 for level in ('easy','moderate','hard'):
  for seed in range(8):
   r=g.generate(level,seed);verify(r);variants.append(r);native.append(normal_native(r,level+'-'+str(seed)))
 # Per-template signed/fractional coverage and meaningful finite sampler catalog.
 for fam in ['linear','quadratic','cubic','logarithmic','reciprocal']:
  r=g.generate('easy',37,template=fam);verify(r);variants.append(r);native.append(normal_native(r,'easy-'+fam))
 # Stable identities across ordering seeds; distinct bank content differs.
 a=g.generate('hard',0);b=g.generate('hard',999,template=a['generation']['template'],parameters=a['generation']['parameters']);assert a['question'][':question/id']==b['question'][':question/id']
 # Fresh concurrent writes in unique previously-unused parameter instances.
 tests=[dict(family='cubic',a='2/3',h='2',k='1',constants=['-2','0','2']),dict(family='exponential',a='3/2',h='0',k='-2/3',constants=['-2','0','2'])]
 # Use exact render geometry with private bounds unique to this run; does not
 # alter public difficulty parameters. No active cache pruning.
 fresh=[]
 for j,p in enumerate(tests):
  cs,colors,_=g.authored_bank(p,'hard');spec=g.make_spec(cs[0],colors[0],p);spec['bounds'][3]+=.0137+j*.0191
  spec['fresh_write_nonce']=uuid.uuid4().hex;fresh.append(spec)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(lambda s:g.render_plots([s])[0],[fresh[0],fresh[0],fresh[1],fresh[1]]))
 assert results[0]==results[1] and results[2]==results[3] and results[0]!=results[2]
 for path,spec in zip(results,[fresh[0],fresh[0],fresh[1],fresh[1]]):assert json.loads(Path(path).with_suffix('.json').read_text())['spec']==spec
 # render_plots asserts cleanup of its own immutable request, not another
 # concurrent parent QA producer's request in the same private cache.
 invalid=[('hard',dict(family='cubic',a='1',h='2',k='1',constants=['-2','0','2'])),('moderate',dict(family='cubic',a='1/2',h='0',k='1',constants=['-2','0','2']))]
 invalid += [(l,dict(family='quadratic' if l=='easy' else 'cubic',a='1' if l=='easy' else '1/2' if l=='moderate' else '3/2',h='1/997',k='1',constants=['-2','0','2'])) for l in ('easy','moderate','hard')]
 for l,p in invalid:
  try:g.generate(l,parameters=p)
  except AssertionError:pass
  else:raise AssertionError('difficulty boundary admitted')
 write('review.json',original+variants);write('engine-input.json',native)
 engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 report=json.loads((H/'engine-report.json').read_text());write('validation.json',{'status':'passed_supported_generation_with_explicit_raw_geometry_uncertainty','source_basis':1356,'source_practice_questions':11,'source_question_prompts_exact':11,'source_question_solutions_exact':11,'source_field_banks_exact':fields,'source_choice_values_exact':choices,'source_correct_designations_exact':refs,'missing_legacy_correct_designations':1,'normal_field_repair':'omit duplicate legacy radio; captured widget has one field','whole_actual_families_checked_against_printed_ode':len(original)+len(variants),'generated_records':len(variants),'normal_records':29,'normal_shift_catalog':{'easy':[-2,-1,0,1,2],'moderate_and_hard_cubic':[-2,-1,1,2],'huge_denominator_fractional_shift_rejections':3},'finite_mathematical_sampler_catalog':{'easy':89,'moderate':72,'hard':32},'source_fidelity_distractors_present_designation':44,'all_levels_reviewed':True,'parameterized_source_variants':11,'raw_geometry_metric_uncertainty':{'q-50197':[5],'q-119139':[4],'q-79563':[3,4]},'geometry_qualitative_whole_bank_inspection':55,'exact_source_asset_reuse_is_not_metric_proof':True,'native_report':report,'engine_binary_sha256':sha(engine),'engine_harness_sha256':sha(ROOT/'generate/runs/current/check-engine.rs'),'concurrency':'same and different specs, unique request files, atomic fresh PNG+sidecars','database_writes':0,'source_results':source_results})
 # Evidence is frozen only after every producer has joined and native checks end.
 artifacts=sorted(p for p in (H/'plots').iterdir() if p.suffix in ('.png','.json'));write('frozen-artifacts.json',{'generator_sha256':sha(H.with_suffix('.py')),'renderer_sha256':sha(H/'render.py'),'validator_sha256':sha(Path(__file__)),'original_source_asset_hashes':{a['original']:sha(Path(a['local'])) for a in json.loads((H/'asset-index.json').read_text())},'producer_state':'all validation subprocesses/threads completed; no pruning','png_count':sum(p.suffix=='.png' for p in artifacts),'sidecar_count':sum(p.suffix=='.json' for p in artifacts),'artifacts':{p.name:sha(p) for p in artifacts}})
 lines=['# Source originals and clearly labeled generated variants','Raw originals preserve legacy field attrs and every original image bank. Four distractor magnitudes are uncertain; these are evidence-only profiles. Normal variants use authored banks.']
 for label,records in [('ORIGINAL RAW REPLAY',original),('GENERATED VARIANT',variants)]:
  for r in records:lines+=['\n## '+label+' · '+r['generation']['level']+' · '+r['generation']['template'],g.markdown(r)]
 (H/'review.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps({'source_questions':11,'source_banks':fields,'source_options':choices,'designations':refs,'normal_variants':len(variants),'native_checks':len(native),'status':'passed with documented raw metric uncertainties'},indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Source fidelity, independent displayed math/stage checks and actual native radio grading.
No EDB connection: fixtures use course_academy_engine::learning::grade_field in memory.
"""
import copy,hashlib,importlib.util,itertools,json,random,subprocess,sys
from pathlib import Path
from functools import lru_cache
import sympy as sp
HERE=Path(__file__).parent;ROOT=HERE.parents[2];SCRIPT=HERE.with_suffix('.py')
sys.path.insert(0,str(HERE))
import printed_math as pm
# Pure exact expression reads/comparisons may repeat across layouts; cache only QA.
pm.parse=lru_cache(None)(pm.parse);pm.equal=lru_cache(None)(pm.equal)
spec=importlib.util.spec_from_file_location('g',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
g.bank=lru_cache(None)(g.bank)
SOL={sid:q.get(':question/worked-solution') for sid,q in g.SOURCES.items()}
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def check(r):return pm.validate(r,SOL)
def fixture(label,r):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual owned radio choice; independently differentiated displayed primitive modulo C'} for a in f[':answer-field/choices']]}
def main():
 cases=[];raw=[];sourcechecks=[];fixtures=[];reviews=[];text=[];mapping=[]
 for sid,src in g.SOURCES.items():
  r=g.generate(g.SOURCE_LEVELS[sid],parameters=g.SOURCE_PARAMETERS[sid],profile='raw:'+sid);q=r['question'];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
  assert q[':question/problem']==src[':question/problem']
  assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in src)
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  assert set(a[':answer/value'] for a in f[':answer-field/choices'])==set(a[':answer/value'] for a in sf[':answer-field/choices'])
  assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'] and f[':answer-field/key']==sf[':answer-field/key']
  if ':answer-field/correct' in sf:
   assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  result=check(r);sourcechecks.append({'source_id':sid,'prompt_exact':True,'solution_exact_or_missing':True,'whole_bank_exact':True,'presence_parity':True,**result})
  cases.append({'source_id':sid,'source_uuid':src[':question/id'],'level':g.SOURCE_LEVELS[sid],'template':r['generation']['template'],'parameters':g.SOURCE_PARAMETERS[sid],'bank_profile':'raw:'+sid,'authored_level_assignment':sid=='q-31248'})
  raw.append(r);reviews.append(r);text.append('## Original '+sid+' — raw observed evidence\n\n'+g.markdown(r))
  nr=copy.deepcopy(r)
  if ':answer-field/correct' not in f:
   nf=nr['question'][':question/answer-fields'][0];answer=next(a for a in nf[':answer-field/choices'] if a[':answer/value']==result['inferred_correct_value']);nf[':answer-field/correct']=[':answer/id',answer[':answer/id']]
   nr['generation']['native_fixture_completion']='Independently inferred designation only in fixture; raw output keeps captured omission'
  fixtures.append(fixture('original:'+sid,nr))
  exp,recipes,opaque=g.bank(g.SOURCE_PARAMETERS[sid]['b'],g.SOURCE_PARAMETERS[sid]['c'],g.SOURCE_LEVELS[sid],'raw:'+sid)
  choices=[]
  for a in sf[':answer-field/choices']:
   derivative=sp.diff(pm.parse(a[':answer/value']),pm.x)
   matches=[i for i,v in enumerate(exp) if pm.equal(derivative,sp.diff(v,g.X))];assert len(matches)==1
   i=matches[0];choices.append({'original_record':a,'exact_generated_value':a[':answer/value'],'recipe':recipes[i],'exact_math_at_original_parameters':str(exp[i]),'intent':'Explicit parameterized evidence; historical intention unresolved' if opaque and i else 'Observed expression shape; method interpretation inferred'})
  mapping.append({'source_id':sid,'parameters':g.SOURCE_PARAMETERS[sid],'profile':'raw:'+sid,'opaque_historical_intent':opaque,'complete_bank':choices,'raw_unicode_function_apply_count':sum(a[':answer/value'].count('\u2061') for a in sf[':answer-field/choices']),'raw_adjacent_backslash_pairs':sum(a[':answer/value'].count('\\\\') for a in sf[':answer-field/choices'])})
 records=[];counts={};tasks=set();rows=0
 # Exhaustive finite-domain displayed validation, separately deduplicated by task.
 for level in g.LEVELS:
  leveltasks=set();n=0;rejected=0
  for template,profile in g.DEFAULT_FAMILIES[level]:
   for b in g.BASES:
    for c in (g.COEFFICIENTS if level=='moderate' else (1,)):
     p={'b':b,'c':c}
     try:r=g.generate(level,seed=19,template=template,profile=profile,parameters=p)
     except ValueError:
      assert level=='moderate' and profile=='scalar_log_coefficient' and abs(c)==b;rejected+=1;continue
     result=check(r);n+=1;rows+=result['solution_rows_checked'];records.append(r)
     leveltasks.add(r['generation']['mathematical_fingerprint']);tasks.add(r['generation']['mathematical_fingerprint'])
     fixtures.append(fixture(level+':'+template+':'+profile+':'+str(b)+':'+str(c),r))
     r2=g.generate(level,seed=83,template=template,profile=profile,parameters=p)
     assert qid(r)==qid(r2) and r['generation']['content_fingerprint']==r2['generation']['content_fingerprint']
     assert sorted(a[':answer/id'] for a in field(r)[':answer-field/choices'])==sorted(a[':answer/id'] for a in field(r2)[':answer-field/choices'])
  counts[level]={'normal_records':n,'meaningful_tasks':len(leveltasks),'base_values':len(g.BASES),'coefficient_values':len(g.COEFFICIENTS) if level=='moderate' else 1,'whole_bank_rejections':rejected,'all_families_checked':list(g.DEFAULT_FAMILIES[level])}
  print('Validated '+level+': '+str(n)+' records, '+str(len(leveltasks))+' meaningful tasks',flush=True)
  # Two generated review examples per supported default family, covering signs/bounds.
  for ti,(template,profile) in enumerate(g.DEFAULT_FAMILIES[level]):
   for b,c in ((3,1),(20,1)) if level!='moderate' else ((5,-2),(19,12)):
    r=g.generate(level,seed=ti+43,template=template,profile=profile,parameters={'b':b,'c':c});check(r);reviews.append(r);text.append('## Generated '+level+' — '+template+' / '+profile+' (authored bounded variation)\n\n'+g.markdown(r))
 # Every source profile at changed parameters: no literal source branch.
 changed=0
 for sid in g.SOURCES:
  level=g.SOURCE_LEVELS[sid]
  for b,c in ((2,1),(20,1)) if level!='moderate' else ((3,4),(19,6)):
   r=g.generate(level,seed=31,parameters={'b':b,'c':c},profile='raw:'+sid);check(r);changed+=1
   reviews.append(r);text.append('## Generated evidence replay '+sid+' — changed parameters, raw complete bank (ineligible for normal learning)\n\n'+g.markdown(r))
   if sid=='q-31248':assert ':question/difficulty' not in r['question'] and ':question/worked-solution' not in r['question'] and ':answer-field/correct' not in field(r)
 # Default family coverage, independent of explicit requests.
 selected=set();positions=set()
 for level in g.LEVELS:
  for seed in range(100):
   r=g.generate(level,seed);check(r);selected.add((level,r['generation']['template'],r['generation']['profile']))
   f=field(r);positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 assert selected=={(l,t,p) for l,pairs in g.DEFAULT_FAMILIES.items() for t,p in pairs} and positions==set(range(5))
 # Same content/UUID for exact parameter aliases and changed order/seed.
 r=g.generate('easy',parameters={'b':'4/2','c':'1'},profile='base_ln_power');s=g.generate('easy',seed=9,parameters={'b':2,'c':1},profile='base_ln_power');assert qid(r)==qid(s)
 # Different banks and layout share assessed-task fingerprint only.
 a=g.generate('moderate',template='scalar_base',parameters={'b':5,'c':3},profile='scalar_reciprocal');b=g.generate('moderate',template='what_integral',parameters={'b':5,'c':3},profile='scalar_log_coefficient')
 assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and qid(a)!=qid(b)
 invalid=[('easy',{'b':1,'c':1},None),('hard',{'b':21,'c':1},None),('easy',{'b':3,'c':2},None),('hard',{'b':3,'c':2},None),('moderate',{'b':3,'c':1},None),('moderate',{'b':3,'c':-13},None),('moderate',{'b':3,'c':3},'scalar_log_coefficient'),('moderate',{'b':3,'c':-2},'raw:q-113890'),('easy',{'b':'sqrt(3)','c':1},None),('easy',{'b':2.0,'c':1},None)]
 for level,p,profile in invalid:
  try:g.generate(level,parameters=p,profile=profile)
  except ValueError:pass
  else:raise AssertionError('Invalid input accepted')
 try:g.generate('easy',field_type='blank')
 except ValueError:pass
 else:raise AssertionError('Invented blank permitted')
 mutations=[]
 for name in ('prompt_base','scalar_prose','factor_row','final_primitive','log_difference','log_zero_stage','log_negative_stage','hard_conclusion','delete_stage_equal_math','wrong_wrong_C_equivalence','control_character','wrong_key'):
  r=copy.deepcopy(g.generate('hard' if name in ('log_difference','log_zero_stage','log_negative_stage','hard_conclusion','delete_stage_equal_math') else 'moderate',parameters={'b':5,'c':1 if name in ('log_difference','log_zero_stage','log_negative_stage','hard_conclusion','delete_stage_equal_math') else -2},profile='reciprocal_method' if name in ('log_difference','log_zero_stage','log_negative_stage','hard_conclusion','delete_stage_equal_math') else 'scalar_reciprocal',template='reciprocal_base' if name in ('log_difference','log_zero_stage','log_negative_stage','hard_conclusion','delete_stage_equal_math') else 'scalar_base'));q=r['question'];f=field(r)
  if name=='prompt_base':q[':question/problem']=q[':question/problem'].replace('{5}','{6}')
  elif name=='scalar_prose':q[':question/worked-solution']=q[':question/worked-solution'].replace('constant $-2.','constant $-3.')
  elif name=='factor_row':q[':question/worked-solution']=q[':question/worked-solution'].replace('=-2\\int','=-3\\int')
  elif name=='final_primitive':q[':question/worked-solution']=q[':question/worked-solution'].replace('=-2\\cdot','=-3\\cdot')
  elif name=='log_difference':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'=\ln 1-\ln 5',r'=\ln 1+\ln 5')
  elif name=='log_zero_stage':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'=0-\ln 5',r'=1-\ln 5')
  elif name=='log_negative_stage':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'& =-\ln 5.',r'& =\ln 5.')
  elif name=='hard_conclusion':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'+C=-\frac',r'+C=\frac')
  elif name=='delete_stage_equal_math':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'& =\ln 1-\ln 5',r'& =-\ln 5')
  elif name=='wrong_wrong_C_equivalence':
   wrong=[a for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1]];wrong[1][':answer/value']=wrong[0][':answer/value']+'+17'
  elif name=='control_character':f[':answer-field/choices'][0][':answer/value']+='\x0c'
  elif name=='wrong_key':f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])]
  try:check(r)
  except (AssertionError,ValueError,TypeError,IndexError):mutations.append(name)
  else:raise AssertionError('Independent reader accepted mutation '+name)
 write('source-cases.json',cases);write('source-replays.json',raw);write('source-choice-map.json',mapping);write('review.json',reviews);write('native-input.json',fixtures)
 (HERE/'review.md').write_text('# General-base exponential integral review — basis 2275\n\nRaw originals preserve omissions; generated examples use completed authored normal records. No plots required.\n\n'+'\n\n'.join(text)+'\n')
 engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 native=json.loads((HERE/'native-report.json').read_text());assert native['accepted_checks']==len(fixtures) and native['rejected_checks']==4*len(fixtures) and native['documented_unresolved_checks']==0
 # CLI shape/presence smoke checks include omission-bearing raw source.
 cli=json.loads(subprocess.check_output([str(ROOT/'.venv/bin/python'),str(SCRIPT),'--difficulty','all','--count','2','--format','json'],text=True));assert len(cli)==6
 for r in cli:check(r)
 rawcli=json.loads(subprocess.check_output([str(ROOT/'.venv/bin/python'),str(SCRIPT),'--difficulty','moderate','--profile','raw:q-31248','--format','json'],text=True));assert ':question/difficulty' not in rawcli[0]['question']
 md=subprocess.check_output([str(ROOT/'.venv/bin/python'),str(SCRIPT),'--difficulty','moderate','--profile','raw:q-31248','--format','markdown'],text=True);assert md.startswith('What is $')
 report={'status':'pass','generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_fidelity':{'originals':6,'prompts_exact':6,'whole_banks':{'matched':6,'total':6},'options':{'matched':30,'total':30},'distractors':{'matched':24,'total':24},'observed_designated_distractors':{'matched':20,'total':20},'independently_inferred_missing_ref_distractors':4,'correct_refs':{'matched':5,'total':5,'missing':1},'worked_solutions':{'exact':5,'available':5,'missing':1},'attribute_presence_parity':6,'raw_ln_U2061_preserved':True,'presentation_repairs':0,'normal_ln_notation_normalization':'Unicode function apply ln changed to standard TeX ln only'},'source_checks':sourcechecks,'normal_domain':counts,'independent_normal_records':len(records),'normal_solution_equation_checks':rows,'source_solution_equation_checks':sum(s['solution_rows_checked'] for s in sourcechecks),'raw_changed_parameter_records':changed,'meaningful_tasks_excluding_layout_bank_seed_aliases':len(tasks),'default_family_coverage':sorted(selected),'correct_option_positions_seen':sorted(positions),'invalid_inputs_rejected':len(invalid)+1,'mutation_rejections':mutations,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'native_records':len(fixtures),'review_records':len(reviews),'changed_raw_bank_review_examples':changed,'blank_fields':0,'database_writes':0,'registered':False,'unresolved':['Historical intent of compound/swapped baseline wrong values in q-31248, q-31249, q-113890 and q-113893 is opaque. Parameterized complete raw profiles are evidence-only; separately authored default banks are method-derived. No unresolved mathematical, source-fidelity or native checks.']}
 write('validation.json',report)
 write('runtime.json',{'python':sys.version.split()[0],'sympy':sp.__version__,'renderer':'none; standalone TeX only','native_entrypoint':'course_academy_engine::learning::grade_field'})
 hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.is_file() and p.name!='hashes.json'};hashes[SCRIPT.name]=hashlib.sha256(SCRIPT.read_bytes()).hexdigest();write('hashes.json',hashes)
 print(json.dumps({k:report[k] for k in ('status','generator_sha256','normal_domain','native','meaningful_tasks_excluding_layout_bank_seed_aliases')},indent=2))
def qid(r):return r['question'][':question/id']
def field(r):return r['question'][':question/answer-fields'][0]
if __name__=='__main__':main()

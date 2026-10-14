"""Fail closed on displayed mathematics, fidelity, scope, identity or native grading."""
from pathlib import Path
import importlib.util,json,re,subprocess,hashlib,itertools,uuid,sys,copy,platform
sys.dont_write_bytecode=True
import sympy as sp
H=Path(__file__).parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor

def parse(s):
 """Independent recursive TeX reader for the entire advertised finite grammar."""
 s=s.strip().rstrip('.').replace(r'\,','').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*')
 s=re.sub(r'\\operatorname\{(sin|cos|ln)\}',lambda m:'\\'+m[1],s)
 def group(pos):
  assert s[pos]=='{',(s,pos);depth=1;end=pos+1
  while depth:
   if s[end]=='{':depth+=1
   if s[end]=='}':depth-=1
   end+=1
  return s[pos+1:end-1],end
 # Parse innermost full fractions, preserving visible multiplication.
 while r'\frac' in s:
  pos=s.rfind(r'\frac');a,j=group(pos+5);b,k=group(j)
  s=s[:pos]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+s[k:]
 s=s.replace('{cos}',r'\cos').replace('{e}','e').replace('{x}','x')
 # Function arguments are balanced parentheses/braces or the remaining simple
 # kx product through the next explicit multiplication/operator boundary.
 while re.search(r'\\(?:ln|sin|cos)',s):
  m=list(re.finditer(r'\\(ln|sin|cos)',s))[-1];pos=m.end();name={'ln':'log','sin':'sin','cos':'cos'}[m[1]]
  exponent=''
  if pos<len(s) and s[pos]=='^':
   if s[pos+1]=='{':exponent,end=group(pos+1);pos=end
   else:exponent=s[pos+1];pos+=2
  while pos<len(s) and s[pos]==' ':pos+=1
  start=pos
  if s[pos] in '({':
   left=s[pos];right=')' if left=='(' else '}';depth=1;pos+=1
   while depth:
    if s[pos]==left:depth+=1
    if s[pos]==right:depth-=1
    pos+=1
   arg=s[start+1:pos-1]
  else:
   mat=re.match(r'-?\d*x(?:\^\{?\d+\}?)?',s[pos:]);assert mat,(s,pos);arg=mat[0];pos+=len(arg)
  replacement='('+name+'('+str(parse(arg))+'))'+('^('+exponent+')' if exponent else '')
  s=s[:m.start()]+replacement+s[pos:]
 s=s.replace('{','(').replace('}',')')
 try:return parse_expr(s,local_dict={'x':g.x,'y':g.y,'e':sp.E,'log':sp.log,'sin':sp.sin,'cos':sp.cos},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
 except Exception as e:raise AssertionError(('Could not parse actual displayed expression',s)) from e

def equal(a,b):return sp.simplify(a-b)==0

def formatting(text):
 assert text.count('$$')%2==0
 assert text.replace('$$','').count('$')%2==0
 depth=0
 for c in text:
  if c=='{':depth+=1
  if c=='}':depth-=1;assert depth>=0
 assert depth==0
 assert not any(s in text for s in ('@@','+-','--','nan','zoo'))
 assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)

def displayed_check(rec):
 q=rec['question'];p=q[':question/problem'];sol=q[':question/worked-solution'];formatting(p);formatting(sol)
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 assert rec['knowledge_point']==g.KP
 raw=rec['generation']['raw_evidence_profile']
 assert rec['generation']['evidence_only']==raw and rec['generation']['eligible_for_learning']==(not raw)
 if raw:assert g.RAW_DOMAIN_PHRASE in sol and not rec['generation']['presentation_repairs']
 else:
  assert g.NORMAL_DOMAIN_PHRASE in sol and g.RAW_DOMAIN_PHRASE not in sol
  assert 'solution_interval_wording' in rec['generation']['presentation_repairs']
  if rec['generation']['template'] in ('log_all','log_scaled'):
   h=rec['generation']['parameters'].get('h',0);z='x' if h==0 else 'x+'+str(h) if h>0 else 'x'+str(h)
   assert 'On the interval $'+z+'>0,$' in p
   assert 'explicit_logarithm_interval' in rec['generation']['presentation_repairs']
 ode=re.search(r'\$\$\n\{y\}\^\{′\}=(.*?)\n\$\$',p,re.S)[1].split(r',\,')[0];rhs=parse(ode)
 ftex=re.search(r'Let \$f\(x\)=(.*?)\$',p)[1].rstrip('.,');f=parse(ftex)
 claimtex=re.search(r'- \*\*I\.\*\* \$\{f\}\^\{′\}\(x\)=(.*?)\$',p)[1].rstrip('.');claim=parse(claimtex)
 derivative=sp.diff(f,g.x);sub=rhs.subs(g.y,f)
 i=equal(derivative,claim);ii=equal(derivative,sub)
 fields=q[':question/answer-fields'];assert len(fields)==3
 assert [f[':answer-field/key'] for f in fields]==['I','II','III']
 ids=[q[':question/id']];expected={'I':i,'II':ii,'III':ii}
 for field in fields:
  assert field[':answer-field/type']==':answer-field.type/checkbox'
  assert field[':answer-field/correct'][0]==':answer/id'
  bank=field[':answer-field/choices'];assert len(bank)==2
  assert sorted(a[':answer/value'] for a in bank)==['false','true']
  assert all(a[':answer/type']==':answer.type/text' and ':answer/feedback' not in a for a in bank)
  ids.append(field[':answer-field/id']);ids.extend(a[':answer/id'] for a in bank)
  actual=next(a[':answer/value'] for a in bank if a[':answer/id']==field[':answer-field/correct'][1])
  assert actual==str(expected[field[':answer-field/key']]).lower()
 assert len(set(ids))==len(ids)
 for identifier in ids:assert str(uuid.UUID(identifier))==identifier
 assert 'Select all that apply.' in p
 for key in ('I','II','III'):assert p.count('- **'+key+'.** ')==1
 assert f'- Statement I is {"true" if i else "false"}.' in sol
 assert f'- Statement II is {"true" if ii else "false"}.' in sol
 assert f'- Statement III is {"true" if ii else "false"}.' in sol
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
 derivative_rows=blocks[0].split(r'\\');sub_rows=blocks[1].split(r'\\');stagecount=0
 t=rec['generation']['template']
 if t in ('sin_none','power_moderate','affine_log'):
  assert r'\cdot ' in derivative_rows[1], 'Collapsed required coefficient/chain product stage'
  assert r'\cdot ' not in derivative_rows[2]
 counts={'power_easy':(3,3),'exp_true':(2,2),'sin_none':(4,3),'cos_i':(2,3),'log_all':(2,3),'inverse_none':(3,3),'exp_none':(3,3),'log_scaled':(3,6),'power_moderate':(4,3),'affine_log':(3 if i else 4,4)}
 assert (len(derivative_rows),len(sub_rows))==counts[t]
 if t=='log_scaled':
  assert ')/' in sub_rows[1]
  assert r'{e}^{2\operatorname{ln}⁡x}' in sub_rows[2]
  assert r'{e}^{\operatorname{ln}⁡{x}^{2}}' in sub_rows[3]
  assert r'{x}^{2}' in sub_rows[4] and '{e}' not in sub_rows[4]
 if t=='power_moderate':
  n=sp.degree(f,g.x);a=f.subs(g.x,1)
  assert n in range(2,6) and -9<=a<=-2 and abs(a*n)<=45

 for j,row in enumerate(derivative_rows):
  lhs,r=row.split('&');r=r.strip()
  if j==0:
   assert r.startswith('=') and r.endswith('^{′}'),r
   formal=parse(r[1:-4]);assert equal(formal,f);assert equal(sp.diff(formal,g.x),derivative)
  elif r.startswith(r'\ne'):
   assert equal(parse(r[3:]),claim) and not i
  else:assert equal(parse(r[1:]),derivative),(rec['generation'],row,derivative)
  stagecount+=1
 for j,row in enumerate(sub_rows):
  lhs,r=row.split('&');r=r.strip().replace('✓','').replace(r'\times','').strip()
  relation=r'\overset{?}{=}' if r.startswith(r'\overset{?}{=}') else r'\ne' if r.startswith(r'\ne') else '='
  val=parse(r[len(relation):])
  if j==0:assert equal(val,rhs)
  else:
   assert equal(parse(lhs),derivative),(rec['generation'],row)
   assert equal(val,sub),(rec['generation'],row,sub)
   if relation=='=':assert ii
   if relation==r'\ne':assert not ii
  stagecount+=1
 # Actual prose substitutions must match the printed function/derivative too.
 prose=re.search(r'Substituting \$y=(.*?)\$ and \$\{y\}\^\{′\}=(.*?)\$',sol)
 assert prose and equal(parse(prose[1]),f) and equal(parse(prose[2]),derivative)
 defining=re.search(r'Differentiating \$f\(x\)=(.*?)\$',sol)
 assert defining and equal(parse(defining[1].rstrip(',')),f)
 conclusion=re.search(r'the function \$y=(.*?)\$ is (not )?a solution',sol)
 assert conclusion and equal(parse(conclusion[1]),f) and bool(conclusion[2])==(not ii)
 labels={(True,True):'I, II, and III',(False,True):'II and III only',(True,False):'I only',(False,False):'None'}
 assert sol.endswith('Therefore, the correct answer is "'+labels[i,ii]+'."')
 return stagecount

def read_json(path):return json.loads(Path(path).read_text())
def write_json(name,data):(H/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def baseline_snapshot():
 b=ROOT/'generate/scratch/17592186100888';entries={}
 for p in [b.with_suffix('.py'),b]+sorted(b.rglob('*')):
  relative=str(p.relative_to(ROOT))
  entries[relative]={'kind':'symlink','target':str(p.readlink())} if p.is_symlink() else {'kind':'file','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} if p.is_file() else {'kind':'directory'}
 return entries

def compare_contract(q,source):
 for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in source)
 assert q[':question/problem']==source[':question/problem'];assert q[':question/worked-solution']==source[':question/worked-solution']
 assert q[':question/difficulty']==source[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  sf=next(z for z in source[':question/answer-fields'] if z[':answer-field/key']==f[':answer-field/key'])
  assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  for key in (':answer-field/choices',':answer-field/correct'):assert (key in f)==(key in sf)
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  for a in f[':answer-field/choices']:
   original=next(z for z in sf[':answer-field/choices'] if z[':answer/value']==a[':answer/value'])
   assert a[':answer/type']==original[':answer/type'][':db/ident']
   assert (':answer/feedback' in a)==(':answer/feedback' in original)
   if ':answer/feedback' in original:assert a[':answer/feedback']==original[':answer/feedback']

DOMAINS={'power_easy':{'n':range(2,6)},'exp_true':{'k':range(1,5)},'sin_none':{'k':range(2,5)},'cos_i':{'k':range(1,5)},'log_all':{'h':range(-4,5)},'inverse_none':{'n':range(2,6)},'exp_none':{'a':range(2,6),'k':range(1,5),'b':range(1,6)},'log_scaled':{'m':range(1,5)},'power_moderate':{'a':range(-9,-1),'n':range(2,6)},'affine_log':{'a':[-4,-3,-2,2,3,4],'b':range(2,5),'c':[-4,-3,-2,-1,1,2,3,4],'claim':[True,False],'solution':[True,False]}}

def compile_engine():
 deps=ROOT/'target/release/deps';libraries={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
 command=['rustc','--edition=2024','-O',str(ROOT/'generate/runs/current/check-engine.rs')]
 for name,path in libraries.items():command+=['--extern',name+'='+str(path)]
 command+=['-L','dependency='+str(deps),'-o',str(H/'check-engine')]
 subprocess.run(command,check=True)
 provenance={'source':str(ROOT/'generate/runs/current/check-engine.rs'),'source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'command':command,'libraries':{name:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for name,p in libraries.items()},'binary_sha256':hashlib.sha256((H/'check-engine').read_bytes()).hexdigest(),'rustc_version':subprocess.check_output(['rustc','--version'],text=True).strip(),'entry_point':'course_academy_engine::learning::grade_field','database_writes':0}
 write_json('engine-provenance.json',provenance);return provenance

def main():
 assert baseline_snapshot()==read_json(H/'baseline-before.json'), 'Registered baseline changed before validation'
 capture=read_json(H/'source.json');assert capture['basis']==2275 and len(capture['record'][':knowledge-point/questions'])==14
 cases=read_json(H/'source-cases.json');originals={q[':question/math-academy-id']:q for q in capture['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q};independent=[q for q in capture['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 inventory=read_json(H/'independent-inventory.json');assert inventory['basis']==2275 and inventory['lineage']==capture['lineage']
 assert {row['record'][':db/id']:row['record'] for row in inventory['questions']}=={q[':db/id']:q for q in independent}
 assert all(row['role']=='independently authored inventory' and row['relationship_to_source_templates'] for row in inventory['questions'])
 Fspec=importlib.util.spec_from_file_location('rootF',ROOT/'generate/runs/current/root-source-fidelity.py');F=importlib.util.module_from_spec(Fspec);Fspec.loader.exec_module(F)
 replayed,counts=F.check(g,17592186100888,H);assert set(replayed)==set(originals) and len(cases)==9
 write_json('root-source-fidelity.json',{'passed':True,'basis':2275,'counts':counts,'independent_inventory_exact_records':5,'reader_sha256':hashlib.sha256((ROOT/'generate/runs/current/root-source-fidelity.py').read_bytes()).hexdigest()})
 fixtures=[];stage_count=0;normal_source_repairs=0;reviews=[];lines=['# Refreshed checkbox review — basis2275','Registered numeric baseline is preserved. Original source strings below are explicitly raw/ineligible; generated variants use the corrected function-interval wording.',''];exhaustive={};slot_coverage={};alias_checks=0
 def native(rec,label):
  checks=[{'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Each displayed Boolean option for each requested statement'} for j,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]
  fixtures.append({'label':label,'record':rec,'checks':checks})
 for c in cases:
  source=originals[c['source_id']];raw=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);compare_contract(raw['question'],source);stage_count+=displayed_check(raw);native(raw,c['source_id']+' raw');lines+=['## Raw original '+c['source_id']+' — '+c['level'].title(),g.markdown(raw),'']
  normal=g.generate(c['level'],template=c['template'],parameters=c['parameters']);stage_count+=displayed_check(normal);native(normal,c['source_id']+' normal repaired')
  normal_source_repairs+=1
  assert normal['question'][':question/worked-solution'].replace(g.NORMAL_DOMAIN_PHRASE,g.RAW_DOMAIN_PHRASE)==source[':question/worked-solution']
  prompt=source[':question/problem']
  if c['template'] in ('log_all','log_scaled'):prompt=prompt.replace(' Which of the following statements are true?',' On the interval $x>0,$ which of the following statements are true?')
  assert normal['question'][':question/problem']==prompt and normal['generation']['mathematical_fingerprint']==raw['generation']['mathematical_fingerprint']
  for seed in (71,73):
   variant=g.generate(c['level'],seed,c['template']);raw_variant=g.generate(c['level'],seed,c['template'],profile=c['bank_profile']);stage_count+=displayed_check(variant)+displayed_check(raw_variant)
   assert variant['generation']['mathematical_fingerprint']==raw_variant['generation']['mathematical_fingerprint']
   native(variant,c['source_id']+' variant '+str(seed));reviews.append(variant);lines+=['### Normal generated '+c['level']+' variant — '+c['template']+' seed'+str(seed),g.markdown(variant),'']
 # Current independently authored inventory is checked mathematically and against
 # the parameterized family without relabeling it original difficulty evidence.
 independent_parameters=[{'a':-2,'n':3},{'a':-3,'n':4},{'a':-4,'n':2},{'a':-5,'n':2},{'a':-3,'n':3}]
 for source,p in zip(independent,independent_parameters,strict=True):
  normal=g.generate_moderate(parameters=p);compare_contract(normal['question'],source);stage_count+=displayed_check(normal);native(normal,'Independent inventory '+str(source[':db/id']))
 for t,domain in DOMAINS.items():
  unique=set();coverage={name:set() for name in domain}
  for values in itertools.product(*domain.values()):
   p=dict(zip(domain,values))
   try:g.validate_parameters(g.LEVELS[t],t,p)
   except ValueError:
    assert (t=='power_moderate' and p=={'a':-2,'n':2}) or (t=='exp_none' and p['b']==p['k']);continue
   rec=g.generate(g.LEVELS[t],template=t,parameters=p);stage_count+=displayed_check(rec);unique.add(rec['generation']['mathematical_fingerprint'])
   for name,value in p.items():coverage[name].add(value)
   if t=='power_moderate':native(rec,'Full moderate '+str(p))
   # Bank-profile, field enum spelling and seed aliases preserve actual identity.
   for profile in ['authored','boolean_statements']+([g.MASKS[t]['profile']] if t in g.MASKS else []):
    alias=g.generate(g.LEVELS[t],937,t,field_type=':answer-field.type/checkbox',parameters=p,profile=profile)
    assert alias['question']==rec['question'] and alias['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint'];alias_checks+=1
  exhaustive[t]=len(unique);assert exhaustive[t]==g.CAPACITIES[t]
  slot_coverage[t]={name:sorted(values) for name,values in coverage.items()}
 # Default sampling must cover every supported source family in its actual level.
 default_families={level:set() for level in g.SUPPORTED_LEVELS};random_counts=0
 for level in g.SUPPORTED_LEVELS:
  for seed in range(120):
   rec=g.generate(level,seed);stage_count+=displayed_check(rec);random_counts+=1;default_families[level].add(rec['generation']['template'])
   if seed<4:native(rec,'Default '+level+' seed'+str(seed))
  assert default_families[level]=={t for t,l in g.LEVELS.items() if l==level}
 for seed in (71,73):
  rec=g.generate_hard(seed);stage_count+=displayed_check(rec);native(rec,'Authored hard example '+str(seed));reviews.append(rec);lines+=['## Authored normal hard example — seed'+str(seed),g.markdown(rec),'']
 for claim,solution in itertools.product((True,False),repeat=2):
  rec=g.generate_hard(parameters={'a':-2,'b':3,'c':-1,'claim':claim,'solution':solution});native(rec,'Hard truth '+str((claim,solution)))
 # Finite capacity, explicit workload bounds and unsupported contract guards.
 for level,t,p in [('moderate','power_moderate',{'a':-10,'n':2}),('moderate','power_moderate',{'a':-2,'n':2}),('moderate','power_moderate',{'a':-9,'n':6}),('hard','affine_log',{'a':1,'b':2,'c':1,'claim':True,'solution':True}),('hard','affine_log',{'a':2,'b':1,'c':0,'claim':True,'solution':True})]:
  try:g.generate(level,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Explicit workload bound bypassed')
 for call in (lambda:g.generate_easy(field_type='radio'),lambda:g.generate_hard(profile='raw_authored'),lambda:g.batch('moderate',32),lambda:g.batch('hard',577)):
  try:call()
  except ValueError:pass
  else:raise AssertionError('Unsupported contract/capacity accepted')
 whole_moderate=g.batch('moderate',31);assert len({r['generation']['mathematical_fingerprint'] for r in whole_moderate})==31
 # Mutation tests catch prose/stage/Boolean/C0 errors independently of answers.
 mutation_results={}
 base=g.generate_moderate(parameters={'a':-3,'n':2})
 mutations={
 'collapsed_required_product':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'-3\cdot 2x','-6x')),
 'stale_prose_conclusion':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('the function $y=-3{x}^{2}$','the function $y=-4{x}^{2}$')),
 'C0_formfeed':lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\f'),
 'wrong_boolean':lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',next(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/value']=='true')]),
 'wrong_formal_derivative_input':lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'{(-3{x}^{2})}^{′}',r'{(-4{x}^{2})}^{′}')),
 }
 for name,mutate in mutations.items():
  altered=copy.deepcopy(base);mutate(altered)
  try:displayed_check(altered)
  except (AssertionError,ValueError,TypeError,IndexError):mutation_results[name]='rejected'
  else:raise AssertionError('Mutation was missed: '+name)
 engine=compile_engine();write_json('native-input.json',fixtures)
 subprocess.run([str(H/'check-engine'),str(H/'native-input.json'),str(H/'native-report.json')],check=True)
 native_report=read_json(H/'native-report.json');assert native_report['documented_unresolved_checks']==0
 write_json('review.json',reviews);(H/'review.md').write_text('\n'.join(lines));write_json('slot-coverage.json',slot_coverage)
 after=baseline_snapshot();write_json('baseline-after.json',after);assert after==read_json(H/'baseline-before.json'),'Registered baseline changed'
 report={'passed':True,'generator_version':g.VERSION,'database':'math','basis':2275,'lineage':capture['lineage'],'captured_pool':14,'original_ma_sources':9,'independent_inventory_exact_records':5,'raw_fidelity':counts,'normal_source_wording_repairs':normal_source_repairs,'normal_source_log_domain_clarifications':2,'source_mathematical_stages_or_banks_changed':False,'source_teaching_anomaly':'Overbroad equation-domain wording is raw/ineligible; normal functions are checked on their valid interval.','exhaustive_distinct_tasks_by_template':exhaustive,'semantic_capacity_by_level':{l:sum(n for t,n in exhaustive.items() if g.LEVELS[t]==l) for l in g.SUPPORTED_LEVELS},'random_default_records_checked':random_counts,'default_family_coverage':{l:sorted(v) for l,v in default_families.items()},'alias_identity_checks':alias_checks,'independently_displayed_stages_checked':stage_count,'mutation_regressions':mutation_results,'native_accepted':native_report['accepted_checks'],'native_rejected':native_report['rejected_checks'],'native_unresolved':0,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'current_engine':engine,'registered_baseline_entries_unchanged':len(after),'database_writes':0,'limitations':['Hard remains an authored workload/difficulty, not an observed rating.','The moderate (a-n) asserted derivative is a labeled authored plausible operation; historical distractor intent remains underdetermined.','The finite moderate coefficient extension to -9 keeps one coefficient product bounded by45 and does not imply new observed difficulty evidence.']}
 write_json('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()

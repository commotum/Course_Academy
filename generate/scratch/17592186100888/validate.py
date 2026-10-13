"""Fail closed on displayed mathematics, fidelity, scope, identity or native grading."""
from pathlib import Path
import importlib.util,json,re,subprocess,hashlib,itertools,uuid
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
 claimtex=re.search(r'- \$\{f\}\^\{′\}\(x\)=(.*?)\$',p)[1].rstrip('.');claim=parse(claimtex)
 derivative=sp.diff(f,g.x);sub=rhs.subs(g.y,f)
 i=equal(derivative,claim);ii=equal(derivative,sub)
 field=q[':question/answer-fields'][0];bank=field[':answer-field/choices'];assert len(bank)==5
 assert len(q[':question/answer-fields'])==1 and field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection'
 assert field[':answer-field/correct'][0]==':answer/id'
 assert all(a[':answer/type']==':answer.type/text' for a in bank)
 ids=[q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in bank]
 assert len(set(ids))==len(ids)
 for identifier in ids:assert str(uuid.UUID(identifier))==identifier
 assert len({a[':answer/value'] for a in bank})==5
 sets={'None':set(),'I only':{1},'II only':{2},'III only':{3},'I and II only':{1,2},'I and III only':{1,3},'II and III only':{2,3},'I, II, and III':{1,2,3}}
 actual_truth={n for n,v in enumerate((i,ii,ii),1) if v}
 assert sum(sets[a[':answer/value']]==actual_truth for a in bank)==1
 actual=next(a[':answer/value'] for a in bank if a[':answer/id']==field[':answer-field/correct'][1]);assert actual==g.ANSWERS[i,ii]
 assert f'- Statement I is {"true" if i else "false"}.' in sol
 assert f'- Statement II is {"true" if ii else "false"}.' in sol
 assert f'- Statement III is {"true" if ii else "false"}.' in sol
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
 derivative_rows=blocks[0].split(r'\\');sub_rows=blocks[1].split(r'\\');stagecount=0
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
 return stagecount

def main():
 sources=json.loads((H/'source.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((H/'source-cases.json').read_text());fixtures=[];reviews=[];lines=['# Review — original sources and labeled generated variants','']
 total_stages=0
 def native(rec,label):
  fld=rec['question'][':question/answer-fields'][0]
  fixtures.append({'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==fld[':answer-field/correct'][1] else 'rejected','purpose':'Every owned displayed option'} for a in fld[':answer-field/choices']]})
 for case,source in zip(cases,sources,strict=True):
  rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=rec['question']
  for key in (':question/problem',':question/worked-solution'):assert q[key]==source[key],(case,key)
  for key in (':question/difficulty',':question/answer-fields',':question/worked-solution'):
   assert (key in q)==(key in source)
  assert q[':question/difficulty']==source[':question/difficulty'][':db/ident']
  a=q[':question/answer-fields'][0];b=source[':question/answer-fields'][0]
  assert a[':answer-field/type']==b[':answer-field/type'][':db/ident'];assert a[':answer-field/key']==b[':answer-field/key']
  assert sorted(i[':answer/value'] for i in a[':answer-field/choices'])==sorted(i[':answer/value'] for i in b[':answer-field/choices'])
  assert next(i[':answer/value'] for i in a[':answer-field/choices'] if i[':answer/id']==a[':answer-field/correct'][1])==b[':answer-field/correct'][':answer/value']
  assert rec['generation']['raw_evidence_profile'] and rec['generation']['evidence_only'] and not rec['generation']['eligible_for_learning']
  normal_profile=case['bank_profile'][4:]
  normal=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=normal_profile)
  assert normal['question'][':question/worked-solution'].replace(g.NORMAL_DOMAIN_PHRASE,g.RAW_DOMAIN_PHRASE)==source[':question/worked-solution']
  expected_prompt=source[':question/problem']
  if case['template'] in ('log_all','log_scaled'):
   expected_prompt=expected_prompt.replace(' Which of the following statements are true?', ' On the interval $x>0,$ which of the following statements are true?')
  assert normal['question'][':question/problem']==expected_prompt
  assert normal['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
  assert normal['question'][':question/id']!=rec['question'][':question/id']
  total_stages+=displayed_check(normal);native(normal,case['source_id']+' normal domain wording')
  total_stages+=displayed_check(rec);native(rec,case['source_id']);lines+=['## Raw original evidence '+case['source_id']+' — '+case['level'].title(),'',g.markdown(rec),'']
  for seed in (71,73):
   raw_variant=g.generate(case['level'],seed,case['template'],profile=case['bank_profile']);total_stages+=displayed_check(raw_variant)
   assert raw_variant['generation']['evidence_only']
   variant=g.generate(case['level'],seed,case['template'],profile=normal_profile);
   assert raw_variant['generation']['mathematical_fingerprint']==variant['generation']['mathematical_fingerprint']
   total_stages+=displayed_check(variant);native(variant,case['source_id']+' variant '+str(seed));reviews.append(variant);lines+=['### Generated '+case['level']+' variant — '+case['template']+' seed '+str(seed),'',g.markdown(variant),'']
 records=0;fingerprints={l:set() for l in ('easy','moderate','hard')}
 for t,level in g.LEVELS.items():
  for seed in range(70):
   rec=g.generate(level,seed,t);total_stages+=displayed_check(rec);records+=1;fingerprints[level].add(rec['generation']['mathematical_fingerprint'])
   if seed<3:native(rec,t+' random '+str(seed))
   other=g.generate(level,seed+919,t,parameters=rec['generation']['parameters'],profile=rec['generation']['bank_profile'])
   assert rec['question'][':question/id']==other['question'][':question/id'];assert rec['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
 for case in cases:
  authored=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile='authored')
  total_stages+=displayed_check(authored);native(authored,case['source_id']+' authored bank')
  observed=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'][4:])
  if sorted(a[':answer/value'] for a in authored['question'][':question/answer-fields'][0][':answer-field/choices'])!=sorted(a[':answer/value'] for a in observed['question'][':question/answer-fields'][0][':answer-field/choices']):
   assert authored['question'][':question/id']!=observed['question'][':question/id']
 for claim,solution in itertools.product((True,False),repeat=2):
  rec=g.generate_hard(parameters={'a':2,'b':3,'c':1,'claim':claim,'solution':solution});total_stages+=displayed_check(rec);native(rec,'hard truth '+str((claim,solution)))
 for seed in (71,73):
  rec=g.generate_hard(seed);reviews.append(rec);lines+=['## Authored hard variant — seed '+str(seed),'',g.markdown(rec),'']
 # Exhaustively enumerate the whole finite mathematical domain.
 exhaustive_counts={}
 domains={'power_easy':{'n':range(2,6)},'exp_true':{'k':range(1,5)},'sin_none':{'k':range(2,5)},'cos_i':{'k':range(1,5)},'log_all':{'h':range(-4,5)},'inverse_none':{'n':range(2,6)},'exp_none':{'a':range(2,6),'k':range(1,5),'b':range(1,6)},'log_scaled':{'m':range(1,5)},'power_moderate':{'a':range(-5,-1),'n':range(2,6)},'affine_log':{'a':[-4,-3,-2,2,3,4],'b':range(2,5),'c':[-4,-3,-2,-1,1,2,3,4],'claim':[True,False],'solution':[True,False]}}
 for t,domain in domains.items():
  unique=set()
  for values in itertools.product(*domain.values()):
   p=dict(zip(domain,values))
   try:g.validate_parameters(g.LEVELS[t],t,p)
   except ValueError:continue
   rec=g.generate(g.LEVELS[t],template=t,parameters=p);total_stages+=displayed_check(rec);unique.add(rec['generation']['mathematical_fingerprint'])
  exhaustive_counts[t]=len(unique)
 assert sum(exhaustive_counts[t] for t in domains if g.LEVELS[t]=='easy')==96
 assert exhaustive_counts['power_moderate']==15 and exhaustive_counts['affine_log']==576
 try:g.generate_hard(profile='raw_authored')
 except ValueError:pass
 else:raise AssertionError('Uncaptured raw authored profile accepted')
 # Every meaningful hard truth combination and all signed boundaries.
 for a in (-4,-2,2,4):
  for b in (2,4):
   for c in (-4,-1,1,4):
    for i in (True,False):
     for ii in (True,False):total_stages+=displayed_check(g.generate_hard(parameters={'a':a,'b':b,'c':c,'claim':i,'solution':ii}))
 for t,p in [('power_easy',{'n':1}),('sin_none',{'k':1}),('power_moderate',{'a':-2,'n':2}),('exp_none',{'a':2,'k':2,'b':2}),('affine_log',{'a':1,'b':2,'c':1,'claim':True,'solution':True})]:
  try:g.generate(g.LEVELS[t],template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit parameters accepted')
 (H/'native-input.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'native-input.json'),str(H/'native-report.json')],check=True)
 native_report=json.loads((H/'native-report.json').read_text())
 (H/'review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n');(H/'review.md').write_text('\n'.join(lines))
 report={'passed':True,'database':'math','basis':1356,'source_prompts_raw_exact':9,'source_prompts_exact':9,'source_solutions_raw_exact':9,'source_solutions_exact':9,'normal_interval_wording_repaired_sources':9,'normal_explicit_log_domain_prompts':2,'mathematical_workload_repairs':0,'source_banks_complete':9,'source_choices_matched':45,'source_correct_designations_matched':9,'source_difficulty_presence_parity':9,'source_errors':[{'type':'teaching_domain_wording','evidence':'Common opening requires every x in equation domain, although logarithmic candidates have a smaller interval of definition.','normal_repair':'Check all x in an interval where the proposed function is defined and the equation is valid; state logarithmic interval explicitly.','raw_replay':'All nine original strings retained through raw_<source-id>_bank profiles, evidence_only=true, eligible_for_learning=false.','mathematical_stages_and_banks_changed':False}],'authored_missing_levels':['hard'],'exhaustive_distinct_tasks_by_template':exhaustive_counts,'random_display_records_checked':records,'independent_display_stages_checked':total_stages,'sample_distinct_math_tasks':{k:len(v) for k,v in fingerprints.items()},'native_accepted':native_report['accepted_checks'],'native_rejected':native_report['rejected_checks'],'native_unresolved':native_report['documented_unresolved_checks'],'grading_engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'limitations':['Observed categorical banks reproduce exact combinations; intent behind impossible II-only/III-only distractors is not inferred.','Raw logarithmic sources omit an explicit x>0 clause and retain the original overly broad domain sentence as ineligible evidence; normal questions repair both.','Hard difficulty is authored, not an observed rating.','Moderate wrong derivative uses coefficient-minus-exponent, one plausible operation matching the single observed scalar; historical error intent is underdetermined.'],'sympy_version':sp.__version__,'database_writes':0}
 (H/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()

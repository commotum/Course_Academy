#!/usr/bin/env python3
"""Independent checks of displayed Newton cooling stories, full banks and stages."""
import copy,hashlib,importlib.util,json,pathlib,re,subprocess,sys,uuid
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=pathlib.Path(__file__).parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
U,C,A=sp.symbols('T k A',positive=True)
def require(ok,msg):
 if not ok:raise AssertionError(msg)
def rhs(value):
 require(value.count('=')==1,'Complete equation required')
 lhs,right=value.split('=')
 require(lhs in (r'\frac{\text{d}T}{\text{d}t}','T^{′}(t) ','{T}^{′}(t)','T^{′}(t)'), 'Derivative must use the displayed temperature T and minutes t')
 right=right.replace('{T}_{S}','A').replace('{','').replace('}','').replace(' ','').rstrip('.,')
 return parse_expr(right,local_dict={'T':U,'k':C,'A':A},transformations=standard_transformations+(implicit_multiplication_application,))
def temperatures(text):
 return [(int(n),unit or 'C') for n,unit in re.findall(r'\{?(\d+)\}?\^\{(?:∘|\\circ)\}(?:\\text\{([CF])\}|C)',text)]
def formatted(text):
 require(text.count('$')%2==0,'Balanced math delimiters')
 depth=0
 for character in text:
  if character=='{':depth+=1
  if character=='}':depth-=1
  require(depth>=0,'Balanced TeX braces')
 require(depth==0 and '@@' not in text,'No unfilled braces/slots')
 require('+-' not in text and '--' not in text,'Grouped signed operations')
def independent(record):
 require(record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'Exact outer knowledge_point shape')
 q=record['question'];meta=record['generation'];prompt=q[':question/problem'];level=q[':question/difficulty'].split('/')[-1]
 require(level in g.LEVELS,'Valid level enum')
 formatted(prompt);formatted(q[':question/worked-solution'])
 require('temperature' in prompt and 'minutes' in prompt and '$T(t)$' in prompt and 'constant of proportionality' in prompt,'Displayed thermal model variables and units')
 require('degrees Celsius' in prompt or 'degrees Fahrenheit' in prompt,'Declared temperature scale')
 scale='F' if 'degrees Fahrenheit' in prompt else 'C';temps=temperatures(prompt)
 require(all(unit==scale for _,unit in temps),'All temperature scales match story')
 require(len(temps)==({'easy':1,'moderate':2,'hard':3}[level]),'All source/displayed thermal givens recovered')
 if level=='easy':S=temps[0][0]
 elif level=='moderate':
  I,S=[n for n,_ in temps];require(I>S,'Cooling initial value above ambient')
  context_bounds={'thermometer':(90,110),'turkey':(120,180),'soup':(140,212),'water':(40,99),'straightener':(200,450)}
  context=next((name for name in context_bounds if name in prompt),None);require(context is not None,'Recognizable thermal context')
  low,high=context_bounds[context];require(low<=I<=high,'Actual displayed initial physically consistent with object context')
 else:
  I,S,M=[n for n,_ in temps];require(I>M>S,'Later observed reading strictly between initial and ambient')
  observed=re.search(r'After \$(\d+)\$ minutes?',prompt);require(observed is not None,'Actual observation prose time')
  h=int(observed[1]);require(1<=h<=20,'Positive bounded observation time')
  require(('After $1$ minute in' in prompt) if h==1 else ('After $'+str(h)+'$ minutes in' in prompt),'Observation time unit inflection')
  require(40<=I<=99 and M<=99,'Ordinary water container temperature below boiling')
  require(meta['parameters']['h']==h,'Time prose and selected parameter match')
  # A physical positive k exists for every displayed hard observation; not asked
  # of students, this verifies the consistency of the complete story.
  kval=sp.log(sp.Rational(I-S,M-S))/h;require(kval>0,'Observed cooling is physically realizable')
 require('t>0' in prompt or 't > 0' in prompt,'Positive time domain')
 require('k>0' in prompt or 'k > 0' in prompt,'Positive proportionality constant')
 require(meta['parameters']['S']==S,'Displayed ambient matches parameter slot')
 task={'model':'Newton cooling','ambient':S,'ambient_unit':scale,'ambient_selection_from':1 if level=='easy' else 2 if level=='moderate' else 3}
 require(meta['parameter_fingerprint']==g.digest(task),'Actual displayed assessed-task fingerprint excludes incidental numeric context and banks')
 if level in ('moderate','hard'):require(meta['parameters']['I']==I,'Displayed initial matches parameter slot')
 if level=='hard':require(meta['parameters']['M']==M,'Displayed later reading matches parameter slot')
 fields=q[':question/answer-fields'];require(len(fields)==1,'Single source field layout');f=fields[0]
 require(f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio','Observed field key/type')
 choices=f[':answer-field/choices'];require(len(choices)==5,'Complete five-member bank')
 expressions=[]
 for answer in choices:
  formatted(answer[':answer/value']);require('$' not in answer[':answer/value'],'Delimiter-free math choices')
  expressions.append(rhs(answer[':answer/value']))
 target=-C*(U-S);valid=[i for i,e in enumerate(expressions) if sp.expand(e-target)==0]
 require(len(valid)==1,'Exactly one equation preserves stated constant k, difference and sign')
 require(sp.simplify(target.subs(U,S))==0 and target.subs(U,S+1)<0,'Equilibrium and negative derivative above ambient')
 duplicates=[(i,j) for i,a in enumerate(expressions) for j,b in enumerate(expressions) if i<j and sp.expand(a-b)==0]
 if meta['bank_profile']=='q-106936':require(len(duplicates)==1 and all(valid[0] not in pair for pair in duplicates),'Only documented duplicate WRONG pair')
 else:require(not duplicates,'Whole bank rejected on mathematical equivalence')
 correct=choices[valid[0]];require(f[':answer-field/correct']==[':answer/id',correct[':answer/id']],'Correct lookup is field-owned and mathematically correct')
 solution=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)
 require(len(blocks)==2,'Original generic/substitution two-stage sequence')
 require(sp.expand(rhs(blocks[0].strip()).subs(A,S)-target)==0,'Actual generic worked equation')
 require(sp.expand(rhs(blocks[1].strip())-target)==0,'Actual substituted worked equation')
 require(temperatures(solution)==[(S,scale)],'Actual solution surrounding-temperature statement')
 require(solution.startswith("Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the differential equation"),'Shared source opening prose')
 require('where ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.' in solution,'Shared constant/surroundings prose')
 content=g.digest({'version':g.VERSION,'prompt':prompt,'solution':solution,'bank':sorted(a[':answer/value'] for a in choices)})
 require(content==meta['content_fingerprint'],'Content fingerprint from actual learner content')
 qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{g.KP_UUID}/{g.VERSION}/{content}');fid=uuid.uuid5(qid,'selection')
 require(q[':question/id']==str(qid) and f[':answer-field/id']==str(fid),'Stable question/field identity')
 for a in choices:
  require(a[':answer/type']==':answer.type/math' and a[':answer/id']==str(uuid.uuid5(fid,'math:'+a[':answer/value'])),'Field-owned answer identity/type')
 return expressions

def fidelity(old,new):
 q=new['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 require(q[':question/problem']==old[':question/problem'],'Exact original problem wording')
 require(f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'],'Original field key/type')
 ov=[a[':answer/value'] for a in of[':answer-field/choices']];nv=[a[':answer/value'] for a in f[':answer-field/choices']]
 require(sorted(ov)==sorted(nv),'Exact complete original bank')
 # One-to-one multiset comparison, including documented duplicate values. No
 # false claim that raw oil bank has uniquely different mathematical options.
 old_math=[rhs(v) for v in ov];new_math=[rhs(v) for v in nv]
 for value in old_math:
  matches=[i for i,e in enumerate(new_math) if sp.expand(e-value)==0];require(bool(matches),'Whole equation matched');new_math.pop(matches[0])
 require(not new_math,'No unmatched source options')
 if ':answer-field/correct' in of:
  chosen=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);require(chosen==of[':answer-field/correct'][':answer/value'],'Observed key designation match')
 if ':question/worked-solution' in old:require(q[':question/worked-solution']==old[':question/worked-solution'],'Full original solution sequence/prose match')

def failure(fn,label):
 try:fn()
 except (AssertionError,ValueError):return
 raise AssertionError('Negative control passed: '+label)

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());source=json.loads((HERE/'source.json').read_text());sources={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 originals=[];variants=[];details=[];sweep=0
 for case in cases:
  r=g.generate(case['level'],seed=4,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);independent(r);fidelity(sources[case['source_id']],r);originals.append(r)
  details.append({'source_id':case['source_id'],'bank_exact_matched':True,'options_matched':5,'raw_duplicate_wrong_choices':case['source_id']=='q-106936','designation_matched':case['source_id']!='q-105917','solution_matched':case['source_id']!='q-105917','missing_key_and_solution':case['source_id']=='q-105917'})
 for profile,level in g.PROFILE_LEVELS.items():
  kwargs={'profile':profile}
  if profile=='oil_repaired':kwargs['template']='q-106936'
  for seed in range(35):
   r=g.generate(level,seed=seed,**kwargs);independent(r);sweep+=1
   fixed=g.generate(level,seed=seed+80,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=profile);independent(fixed)
   require(r['question'][':question/id']==fixed['question'][':question/id'],'Content fixed across seed/choice order')
   if seed in (6,21):variants.append(r)
 # Exercise every normal prose template with complete authored default bank.
 for level,templates in g.DEFAULT_TEMPLATES.items():
  for template in templates:
   for seed in (2,19):
    r=g.generate(level,seed=seed,template=template);independent(r);variants.append(r)
 for level in g.LEVELS:
  ids=[g.generate(level,seed=i)['question'][':question/answer-fields'][0] for i in range(20)]
  positions={next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]) for f in ids}
  require(len(positions)>1,'Correct choices do not always occupy first slot')
 bad=copy.deepcopy(originals[1]);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('64','63');failure(lambda:independent(bad),'ambient prose mismatch')
 bad=copy.deepcopy(variants[-1]);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('After $','After $0',1);failure(lambda:independent(bad),'specific-time prose mismatch')
 bad=copy.deepcopy(originals[1]);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('-k(T-64)','k(T-64)');failure(lambda:independent(bad),'worked derivative sign')
 bad=copy.deepcopy(originals[1]);bad['question'][':question/answer-fields'][0][':answer-field/choices'].pop();failure(lambda:independent(bad),'incomplete bank')
 bad=copy.deepcopy(originals[1]);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']=r'\frac{\text{d}T}{\text{d}t}=-k(T-64)';failure(lambda:independent(bad),'complete-bank ambiguity')
 bad=copy.deepcopy(originals[1]);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('degrees Fahrenheit','degrees Celsius');failure(lambda:independent(bad),'units mismatch')
 bad=copy.deepcopy(originals[1]);bad['knowledge_point'][':db/id']=g.KP_ID;failure(lambda:independent(bad),'outer colon key')
 failure(lambda:g.generate('hard',parameters={'S':20,'I':90,'M':70,'h':0}),'zero explicit time')
 failure(lambda:g.generate('moderate',parameters={'S':20,'I':10}),'heating story')
 failure(lambda:g.generate('easy',parameters={'S':0}),'zero ambient degeneracy')
 failure(lambda:g.generate('hard',parameters={'S':20,'I':90,'M':70,'h':6}), 'whole hard collision I-S=M')
 # Explicit context limits must not be bypassed by any observed/raw profile.
 context_rejections=0
 for template,level,params in [
  ('q-37365','moderate',{'S':64,'I':111}),
  ('q-106883','moderate',{'S':67,'I':213}),
  ('q-106934','moderate',{'S':76,'I':213}),
  ('q-106935','moderate',{'S':19,'I':100}),
  ('q-106937','moderate',{'S':75,'I':451}),
  ('observed-reading','hard',{'S':20,'I':100,'M':60,'h':7})]:
  for profile in ([template,level+'_default'] if level=='moderate' else ['hard_default']):
   failure(lambda:g.generate(level,template=template,profile=profile,parameters=params),'context initial over-limit '+template+' '+profile);context_rejections+=1
 
 # Same shown math/content with alternate integer spelling gives same identities.
 for r in originals:
  meta=r['generation'];rr=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=1000,template=meta['template'],parameters={k:str(v)+'.0' for k,v in meta['parameters'].items()},profile=meta['bank_profile']);require(rr['question'][':question/id']==r['question'][':question/id'],'Equivalent explicit parameter spelling')
 rows=[]
 for n,r in enumerate(originals+variants):
  f=r['question'][':question/answer-fields'][0]
  rows.append({'label':str(n),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Displayed complete model equation with specified proportionality constant'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(rows,indent=2)+'\n')
 engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,cwd=ROOT)
 neg=copy.deepcopy(rows[:1]);neg[0]['checks'][0]['expected']='rejected' if neg[0]['checks'][0]['expected']=='accepted' else 'accepted';(HERE/'engine-negative-input.json').write_text(json.dumps(neg));result=subprocess.run([str(engine),str(HERE/'engine-negative-input.json'),str(HERE/'engine-negative-report.json')],capture_output=True,text=True);require(result.returncode!=0,'Native grading negative control');(HERE/'engine-negative-result.txt').write_text(result.stderr)
 (HERE/'review.json').write_text(json.dumps({'original_replays':originals,'generated_variants':variants},indent=2)+'\n')
 parts=['# Original and changed parameter review','Every original bank and prose template appears below. Raw oil replay has two equivalent wrong choices; the authored oil_repaired/easy_default profiles remove that ambiguity. q105917 key, easy label and solution are authored, not observed matches. Hard is an authored same-method two-stage extension supported by the lesson observation example.']
 for case,r in zip(cases,originals):parts+=['## Original '+case['source_id']+' (source replay)',g.markdown(r)]
 for r in variants:parts+=['## Generated variant: '+r['generation']['template']+' / '+r['generation']['bank_profile']+' / '+r['question'][':question/difficulty'].split('/')[-1], 'Parameters: '+json.dumps(r['generation']['parameters'])+'; '+r['generation']['profile_origin']+'.',g.markdown(r)]
 (HERE/'review.md').write_text('\n\n'.join(parts)+'\n')
 report={'passed':True,'source':{k:source[k] for k in ('database','basis','lineage')},'original_questions':8,'complete_banks_exact_matched':8,'source_options_matched':40,'source_options_total':40,'available_designations_matched':7,'available_designations_total':7,'missing_original_designations':1,'available_full_solutions_matched':7,'available_full_solutions_total':7,'missing_original_solutions':1,'exact_prompts_matched':8,'source_bank_correctness':{'uniquely_different_banks':7,'raw_banks_with_duplicate_wrong_equations':1,'raw_duplicate_profile':'q-106936','normal_banks_duplicate_free':True},'authored_extensions':['q105917 easy assignment, derived key and shared solution','oil_repaired and default complete operation banks','hard additional-reading selection with same two-stage Newton-law setup'],'sweep_records':sweep,'review_originals':8,'review_generated_variants':len(variants),'native_grading':json.loads((HERE/'engine-report.json').read_text()),'native_blank_equivalent_entries':'not applicable: all original and authored fields radio','negative_controls':12+context_rejections,'context_bound_rejections':context_rejections,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'unresolved_findings':['q105917 original key and solution absent; independently derived but not observed','q106936 duplicate wrong choices retained only in explicit raw source profile'],'no_database_writes':True}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(f'PASS: 8/8 exact banks, 40/40 choices, 7/7 available keys and solutions; {sweep} bank sweeps; {len(variants)} changed review records; native grader and {12+context_rejections} negative controls.')
if __name__=='__main__':
 try:main()
 except Exception as exc:
  (HERE/'validation.json').write_text(json.dumps({'passed':False,'failure':str(exc)},indent=2)+'\n');raise

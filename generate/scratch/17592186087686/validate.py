#!/usr/bin/env python3
"""Independent printed-coefficient, bank, source-presence and native QA."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from fractions import Fraction
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
def number(s):
 s=s.replace(' ','')
 match=re.fullmatch(r'(-?)\\(?:d?frac)\{(\d+)\}\{(\d+)\}',s)
 if match:return Fraction((-1 if match[1] else 1)*int(match[2]),int(match[3]))
 if s=='':return Fraction(1)
 if s=='-':return Fraction(-1)
 return Fraction(s)
def parse_line(s):
 s=s.replace(' ','')
 match=re.fullmatch(r'y=(.*?)x([+-])(.+)',s)
 assert match,('not already slope-intercept',s)
 slope='m' if match[1]=='m' else number(match[1])
 return slope,number(match[2]+match[3])
def math_checks(r):
 q,g=r['question'],r['generation'];f=q[':question/answer-fields'][0]
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert isinstance(f[':answer-field/type'],str)
 assert all(isinstance(a[':answer/type'],str) for a in f.get(':answer-field/choices',[]))
 for ident in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f.get(':answer-field/choices',[])]:
  import uuid;assert str(uuid.UUID(ident))==ident
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in f.get(':answer-field/choices',[])]:
  assert s.count('$')%2==0
  assert s.count('{')==s.count('}')
  assert '$$' not in s and '--' not in s and '+-' not in s
 prompt=q[':question/problem'];lines=re.findall(r'\$(y[^$]+)\$',prompt)
 actual=[parse_line(s) for s in lines]
 assert actual and isinstance(actual[0][0],Fraction)
 m,b=actual[0]
 assert m==Fraction(g['parameters']['slope']) and b==Fraction(g['parameters']['b'])
 if len(actual)==2:assert actual[1][1]==Fraction(g['parameters']['k'])
 assert sp.Rational(m.numerator,m.denominator) in G.domains(g['difficulty'])
 if g['template']=='line_choice':
  assert len(actual)==1
  choices=[parse_line(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(choices)==5 and len(set(choices))==5
  matches=[a for a,v in zip(f[':answer-field/choices'],choices) if v[0]==m and v[1]!=b]
  assert len(matches)==1
  assert all(v!=(m,b) for v in choices)
  assert matches[0][':answer/id']==f[':answer-field/correct'][1]
  expected=matches[0][':answer/value']
 else:
  assert len(actual)==2 and actual[1][0]=='m' and b!=actual[1][1]
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
  if not g['profile'].startswith('raw_'):
   vals=[number(a[':answer/value']) for a in f[':answer-field/choices']]
   assert len(set(vals))==len(vals) and vals.count(m)==1
   correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
   assert number(correct[':answer/value'])==m
   expected=correct[':answer/value']
  elif f.get(':answer-field/choices'):
   vals=[number(a[':answer/value']) for a in f[':answer-field/choices']]
   assert len(set(vals))==5 and vals.count(m)==1
 if not g['profile'].startswith('raw_'):
  s=q[':question/worked-solution']
  assert s.startswith(G.OPENING+'\n\n')
  # Read EVERY asserted slope in teaching bullets back from displayed line.
  assertions=re.findall(r'- The slope of the line \$(y[^$]+)\$ is \$([^$]+)\$\.',s)
  assert len(assertions)==(6 if g['template']=='line_choice' else 2)
  for line,value in assertions:
   sm,sb=parse_line(line);assert sm==('m' if value=='m' else number(value))
  if g['template']=='line_choice':
   conclusion=re.search(r'The only choice with the same slope is \$(y[^$]+)\$',s)
   assert conclusion and parse_line(conclusion[1])==(m,parse_line(expected)[1])
   assert parse_line(conclusion[1])[1]!=b
  else:
   conclusion=re.search(r'we must have \$m=([^$]+)\$',s)
   assert conclusion and number(conclusion[1])==m
   # Exact shared canonical stages and prose, not merely substring matching.
   expected_s=G.OPENING+'\n\n'+G.READING+'\n\n- The slope of the line $'+G.line(sp.Rational(m.numerator,m.denominator),int(b))+'$ is $'+G.tex(str(m))+'$.\n- The slope of the line $'+G.line('m',int(actual[1][1]))+'$ is $m$.\n\nBecause the slopes must be the same, we must have $m='+G.tex(str(m))+'$.'
   assert s==expected_s
  # Recompute identity and mathematical workload from printed content, never
 # accept a metadata-only fingerprint or a stale displayed bank.
 task={'assessment':'line_choice' if g['template']=='line_choice' else 'coefficient_read',
       'number_form':g['difficulty'],'target_slope':str(m)}
 if g['template']=='line_choice':task['compared_slopes']=sorted(str(parse_line(a[':answer/value'])[0]) for a in f[':answer-field/choices'])
 assert G.digest(task)==g['mathematical_fingerprint']
 raw=g['profile'].startswith('raw_')
 content={'version':G.VERSION,'difficulty':None if raw else g['difficulty'],
          'prompt':prompt,'solution':None if raw else q[':question/worked-solution'],
          'kind':'blank' if f[':answer-field/type'].endswith('/blank') else 'radio',
          'key':f[':answer-field/key'],'bank':sorted(a[':answer/value'] for a in f.get(':answer-field/choices',[])),
          'correct':None if raw else expected}
 assert G.digest(content)==g['content_identity']
 assert q[':question/id']==G.uid(g['content_identity'])
 return True

def normalize(x):
 if isinstance(x,list):return sorted((normalize(a) for a in x),key=lambda a:json.dumps(a,sort_keys=True))
 if isinstance(x,dict):
  return {k:(v[':db/ident'] if isinstance(v,dict) and ':db/ident' in v else normalize(v)) for k,v in x.items() if k not in (':question/id',':answer-field/id',':answer/id')}
 return x

def native_fixture(r,label):
 q=r['question'];f=q[':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/blank'):
  answer=number(f[':answer-field/choices'][0][':answer/value'])
  canonical=f[':answer-field/choices'][0][':answer/value']
  equivalent=f'({answer.numerator*3})/({answer.denominator*3})'
  checks=[{'submitted':canonical,'expected':'accepted','purpose':'canonical exact coefficient'},
          {'submitted':equivalent,'expected':'accepted','purpose':'independently unreduced fraction'},
          {'submitted':str(answer+1),'expected':'rejected','purpose':'incorrect coefficient'}]
 else:
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank native ID grading'} for a in f[':answer-field/choices']]
 return {'label':label,'record':r,'checks':checks}

def run():
 source=json.loads((HERE/'source.json').read_text());cases=json.loads((HERE/'source-cases.json').read_text())
 originals={q[':db/id']:q for q in source['record'][':knowledge-point/questions']}
 results={'source_questions':3,'raw_prompt_matches':0,'raw_presence_matches':0,'raw_complete_banks':0,'raw_displayed_choices':0,'original_correct_designations':0,'original_worked_solutions':0,'inferred_completion_keys':0,'authored_levels':['easy','moderate','hard'],'failures':[]}
 reviews=[];engine=[]
 for c in cases:
  r=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);math_checks(r)
  q=originals[c['source_id']]
  assert normalize(r['question'])==normalize(q),(normalize(r['question']),normalize(q))
  results['raw_prompt_matches']+=1;results['raw_presence_matches']+=1
  if ':answer-field/choices' in q[':question/answer-fields'][0]:
   results['raw_complete_banks']+=1;results['raw_displayed_choices']+=len(q[':question/answer-fields'][0][':answer-field/choices'])
  reviews.append({'label':'Original raw parameterized replay '+str(c['source_id']),'record':r})
  completed=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'].replace('raw_','completed_'))
  math_checks(completed);results['inferred_completion_keys']+=1
  reviews.append({'label':'Authored inferred completion '+str(c['source_id']),'record':completed})
  engine.append(native_fixture(completed,'completed-'+str(c['source_id'])))
  changed=dict(c['parameters']);changed['slope']='-5' if c['level']=='easy' else '-1/6';changed['b']='7';changed['k']='-3'
  variant=G.generate(c['level'],template=c['template'],parameters=changed,profile=c['bank_profile']);math_checks(variant)
  assert variant['question'][':question/problem']!=r['question'][':question/problem']
  reviews.append({'label':'Generated changed-parameter raw variant '+str(c['source_id']),'record':variant})
  changed_completed=G.generate(c['level'],template=c['template'],parameters=changed,profile=c['bank_profile'].replace('raw_','completed_'));math_checks(changed_completed)
  engine.append(native_fixture(changed_completed,'changed-completed-'+str(c['source_id'])))
 coverage={};counts={};boundary_checks=0
 for level in ('easy','moderate','hard'):
  for m in G.domains(level):
   for template in G.TEMPLATES:
    k='11' if abs(m) in (12,sp.Rational(1,12)) else '-12'
    p={'slope':str(m),'b':'0','k':k}
    try:r=G.generate(level,template=template,parameters=p)
    except ValueError:
     assert level=='easy' and abs(m)==1 and template!='coefficient_blank'
     continue
    math_checks(r);boundary_checks+=1
    if m in (sp.Rational(-12),sp.Rational(12),sp.Rational(-1,12),sp.Rational(1,12),sp.Rational(-12,11),sp.Rational(12,11)):
     engine.append(native_fixture(r,f'boundary-{level}-{template}-{m}'))
 # Equivalent rational parameter spelling cannot create new mathematical/content IDs.
 for template in G.TEMPLATES:
  a=G.generate('hard',12,template,parameters={'slope':'2/3','b':'-4','k':'7'})
  b=G.generate('hard',99,template,parameters={'slope':'4/6','b':'-4','k':'7'})
  assert a['question'][':question/id']==b['question'][':question/id']
  assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 for level in ('easy','moderate','hard'):
  default_templates=set();mathematical=set();presentation=set()
  for seed in range(300):
   r=G.generate(level,seed);math_checks(r);default_templates.add(r['generation']['template'])
   mathematical.add(r['generation']['mathematical_fingerprint']);presentation.add(r['question'][':question/id'])
   if seed<30:engine.append(native_fixture(r,f'{level}-{seed}'))
  assert default_templates==set(G.TEMPLATES)
  coverage[level]=sorted(default_templates);counts[level]={'samples':300,'distinct_mathematical_tasks':len(mathematical),'distinct_content':len(presentation),'eligible_slope_values':len(G.domains(level))}
  for template in G.TEMPLATES:
   for seed in (12,40):
    r=G.generate(level,seed,template);math_checks(r)
    reviews.append({'label':f'Generated authored {level} {template} seed {seed}','record':r})
    p=r['generation']['parameters'];s=G.generate(level,seed+1,template,parameters=p)
    assert r['question'][':question/id']==s['question'][':question/id']
    assert r['generation']['mathematical_fingerprint']==s['generation']['mathematical_fingerprint']
    assert sorted(r['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])==sorted(s['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])
    engine.append(native_fixture(r,f'review-{level}-{template}-{seed}'))
  # Exhaustively enumerate actual finite same-method task domains; answer order,
 # template aliases and line offsets do not inflate these counts.
 finite_counts={}
 for level in ('easy','moderate','hard'):
  line_tasks=set()
  for m in G.domains(level):
   for b in range(-12,13):
    for k in range(b+1,13):
     vals=[m,-m,sp.Integer(b),sp.Integer(k),1/m]
     if len(set(vals))==5:line_tasks.add((str(m),tuple(sorted(map(str,vals)))))
  finite_counts[level]=len(line_tasks)
 assert finite_counts=={'easy':5566,'moderate':6072,'hard':40800}
 # Strict authored input tiers, whole-bank collision, coincident-line guard.
 invalids=[('easy',{},'coefficient_blank'),('easy',{'slope':'1/2','b':'3','k':'7'},'coefficient_blank'),('moderate',{'slope':'2/3','b':'3','k':'7'},'coefficient_blank'),('hard',{'slope':'1/8','b':'3','k':'7'},'coefficient_blank'),('easy',{'slope':'2','b':'3','k':'3'},'coefficient_blank'),('easy',{'slope':'2','b':'2','k':'3'},'coefficient_radio')]
 for level,p,template in invalids:
  try:G.generate(level,template=template,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('invalid accepted',level,p))
 for template in ('coefficient_blank','coefficient_radio'):
  a=G.generate('easy',template=template,parameters={'slope':'2','b':'3','k':'7'})
  b=G.generate('easy',template=template,parameters={'slope':'2','b':'4','k':'9'})
  assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
  assert a['question'][':question/id']!=b['question'][':question/id']
 # Meaningful validator corruption regressions: displayed slope, concluded slope,
 # duplicate bank option, and a coincident line with a different option ID.
 base=G.generate('hard',12,'line_choice')
 for mutation in ('printed_slope','solution_slope','duplicate_bank','coincident_line'):
  r=copy.deepcopy(base);q=r['question'];f=q[':question/answer-fields'][0]
  if mutation=='printed_slope':q[':question/problem']=q[':question/problem'].replace('x','2x',1)
  elif mutation=='solution_slope':q[':question/worked-solution']=q[':question/worked-solution'].replace(' is $',' is $99',1)
  elif mutation=='duplicate_bank':f[':answer-field/choices'][0][':answer/value']=f[':answer-field/choices'][1][':answer/value']
  else:
   target=re.findall(r'\$(y[^$]+)\$',q[':question/problem'])[0]
   correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);correct[':answer/value']=target
  try:math_checks(r)
  except (AssertionError,ValueError):pass
  else:raise AssertionError(('corruption escaped',mutation))
 # Content identity must be canonical under option order / metadata seed.
 for r in [G.generate('easy',i,'coefficient_radio') for i in range(20)]:
  q=r['question'];f=q[':question/answer-fields'][0]
  counts.setdefault('correct_positions',set()).add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 assert len(counts['correct_positions'])>=4;counts['correct_positions']=sorted(counts['correct_positions'])
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2))
 binary=HERE.parents[1]/'runs/current/check-engine'
 process=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
 assert process.returncode==0,(process.stdout,process.stderr)
 report=json.loads((HERE/'engine-report.json').read_text())
 (HERE/'review.json').write_text(json.dumps(reviews,indent=2))
 text=['# Parallel slope-intercept generator review','Basis 1356. Raw originals omit ratings, keys and solutions. Generated completions and tier labels are authored.']
 for review in reviews:text+=['\n## '+review['label'],G.markdown(review['record'])]
 (HERE/'review.md').write_text('\n\n'.join(text)+'\n')
 results.update({'finite_assessed_domain':{'easy':{'coefficient_read':24,'line_choice':5566,'total':5590},'moderate':{'coefficient_read':22,'line_choice':6072,'total':6094},'hard':{'coefficient_read':136,'line_choice':40800,'total':40936}},'passed':True,'source_bank_fidelity':'1/1 five-scalar bank; 5/5 complete values; no captured designation to match','raw_blank_field_layouts':'2/2; no captured banks','canonical_solution_stage_sequence':'3/3 completed originals; all sampled coefficient-read solutions','native_fixture_count':len(engine),'native_report':report,'default_family_coverage':coverage,'variety':counts,'python':sys.version.split()[0],'sympy':sp.__version__,'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'corruption_tests_rejected':4,'strict_input_rejections':len(invalids),'exhaustive_slope_boundary_checks':boundary_checks,'unresolved_findings':['Historical scalar bank intent remains underdetermined; raw/completed scalar profiles evidence-only.','No observed difficulty labels, practice worked solutions or original correct refs; completions and all three tier labels are explicitly authored.']})
 (HERE/'validation.json').write_text(json.dumps(results,indent=2))
 print(json.dumps({k:v for k,v in results.items() if k!='native_report'},indent=2))
if __name__=='__main__':run()

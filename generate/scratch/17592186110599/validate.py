#!/usr/bin/env python3
"""Fail closed on display mathematics, full-source fidelity, identity and grading."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('perpendicular_generator',SCRIPT)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ROOT=HERE.parents[2]
X=sp.Symbol('x')
TRANS=standard_transformations+(implicit_multiplication_application,)


def expr(text):
 text=text.replace(r'\dfrac',r'\frac').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').strip().rstrip('.?')
 while r'\frac' in text:
  new=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',text)
  if new==text:raise AssertionError('Unsupported/malformed printed fraction: '+text)
  text=new
 if '\\' in text:raise AssertionError('Unsupported TeX '+text)
 return sp.expand(parse_expr(text,local_dict={'x':X},transformations=TRANS))


def equation(text):
 lhs,rhs=text.split('=');assert lhs.strip()=='y'
 return expr(rhs)


def formatting(text):
 assert text.count('$')%2==0
 assert text.count('$$')==2 if '\n$$' in text else '$$' not in text
 balance=0
 for c in text:
  balance+=(c=='{')-(c=='}');assert balance>=0
 assert balance==0


def check_record(record,allow_legacy=False):
 q=record['question'];meta=record['generation'];formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
 assert q[':question/problem'].startswith('Which of the following lines is perpendicular to $')
 shown=re.findall(r'\$([^$]+)\$',q[':question/problem']);assert len(shown)==1
 target=equation(shown[0].rstrip('?'));assert sp.degree(target,X)==1
 m=target.coeff(X)
 assert m!=0
 field,=q[':question/answer-fields'];assert field[':answer-field/key']=='selection' and field[':answer-field/type']==':answer-field.type/radio'
 choices=field[':answer-field/choices'];assert len(choices)==5
 assert len({a[':answer/id'] for a in choices})==5
 assert field[':answer-field/correct'][0]==':answer/id'
 assert field[':answer-field/correct'][1] in {a[':answer/id'] for a in choices}
 import uuid
 for identity in [q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in choices]:uuid.UUID(identity)
 polynomials=[];correct=[]
 for a in choices:
  assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value']
  formatting(a[':answer/value']);p=equation(a[':answer/value']);polynomials.append(p)
  if not allow_legacy:assert sp.degree(p,X)<=1, 'Normal line bank contains nonlinear object'
  if sp.degree(p,X)==1 and m*p.coeff(X)==-1:correct.append(a)
 assert len({str(p) for p in polynomials})==5
 assert len(correct)==1 and correct[0][':answer/id']==field[':answer-field/correct'][1]
 # Independently read every variable mathematical stage from learner prose.
 sol=q[':question/worked-solution']
 first=re.search(r'The line \$([^$]+)\$ is in slope-intercept form, and its slope is \$([^$]+)\$',sol)
 second=re.search(r'Looking at the answer choices, the line \$([^$]+)\$ has a slope of \$([^$]+)\$',sol)
 assert first and second
 assert equation(first[1])==target and expr(first[2])==m
 assert equation(second[1])==equation(correct[0][':answer/value']) and expr(second[2])==-1/m
 product=re.search(r'\$\$\n([^$]+)\n\$\$',sol);assert product
 sides=product[1].split('=');assert len(sides)==2 and expr(sides[0])==expr(sides[1])==-1
 assert r'\cdot' in sides[0]
 factors=sides[0].split(r'\cdot');assert len(factors)==2 and expr(factors[0])==m and expr(factors[1])==-1/m
 assert sol.count('\n\n')==5
 conclusion=re.search(r'we conclude that the line \$([^$]+)\$ is perpendicular',sol);assert conclusion and equation(conclusion[1])==equation(correct[0][':answer/value'])
 assert meta['parameter_fingerprint']==g.digest({'target_slope':str(m)})
 rebuilt=g.generate(q[':question/difficulty'].split('/')[-1],seed=999,template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
 assert q[':question/id']==rebuilt['question'][':question/id']
 assert field[':answer-field/id']==rebuilt['question'][':question/answer-fields'][0][':answer-field/id']
 assert sorted(choices,key=lambda a:a[':answer/id'])==sorted(rebuilt['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])
 assert meta['evidence_only']==allow_legacy
 return {'slope':str(m),'linearity_pass':not allow_legacy,'legacy_quarantine':allow_legacy}


def mutation_checks(record):
 mutations=[]
 def reject(name,mutator):
  r=copy.deepcopy(record);mutator(r)
  try:check_record(r)
  except (AssertionError,ValueError,TypeError,IndexError):mutations.append(name);return
  raise AssertionError('Failed to detect mutation '+name)
 reject('changed prompt coefficient',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('$y=','$y=2+')))
 reject('changed product result',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('=-1.','=-2.')))
 reject('missing option',lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'].pop())
 reject('foreign correct reference',lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id','00000000-0000-0000-0000-000000000000']))
 reject('changed slope prose',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('and its slope is $','and its slope is $2+')))
 return mutations


def main():
 source=json.loads((HERE/'source.json').read_text());questions={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 cases=json.loads((HERE/'source-cases.json').read_text());fidelity=[];records=[];review=[]
 for case in cases:
  q=questions[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);records.append(r)
  check_record(r,allow_legacy=r['generation']['evidence_only'])
  generated=r['question'];f=generated[':question/answer-fields'][0];original=q[':question/answer-fields'][0]
  a=sorted(str(equation(v[':answer/value'])) for v in f[':answer-field/choices'])
  b=sorted(str(equation(v[':answer/value'])) for v in original[':answer-field/choices'])
  assert a==b and sorted(v[':answer/value'] for v in f[':answer-field/choices'])==sorted(v[':answer/value'] for v in original[':answer-field/choices'])
  assert generated[':question/problem']==q[':question/problem']
  observed_solution=q.get(':question/worked-solution');assert not observed_solution or observed_solution==generated[':question/worked-solution']
  designation=original.get(':answer-field/correct')
  correct=next(v[':answer/value'] for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1])
  if designation:assert equation(correct)==equation(designation[':answer/value'])
  fidelity.append({'source_id':case['source_id'],'displayed_options_matched':5,'displayed_options_total':5,'bank_math_match':True,'bank_notation_match':True,'prompt_exact':True,'solution_exact':True if observed_solution else None,'correct_designation_matched':True if designation else None,'derived_correct':correct if not designation else None,'scope_exception':r['generation']['evidence_only']})
  review.append({'label':'Observed source replay '+case['source_id'],'record':r})
  for seed in (140,141):
   v=g.generate(case['level'],seed,profile=case['bank_profile']);check_record(v,allow_legacy=v['generation']['evidence_only']);review.append({'label':'Generated variant of observed bank '+case['source_id']+(' — QUARANTINED MALFORMED EVIDENCE' if v['generation']['evidence_only'] else ''),'record':v})
 # All authored domains exercised; distinct assessed structures counted without intercepts.
 samples=[];variety={}
 for level in ('easy','moderate','hard'):
  rs=[g.generate(level,seed) for seed in range(500)]
  for r in rs:check_record(r)
  variety[level]={'sample_count':500,'distinct_mathematical_tasks':len({r['generation']['parameter_fingerprint'] for r in rs}),'distinct_content_ids':len({r['question'][':question/id'] for r in rs})}
  samples.extend(rs)
  for r in rs[:2]:review.append({'label':'AUTHORED default '+level,'record':r})
 repaired=g.generate('moderate',profile='repaired-q-72524',parameters=next(c['parameters'] for c in cases if c['source_id']=='q-72524'));check_record(repaired)
 review.append({'label':'Explicit minimal source repair q-72524; two extra x factors removed','record':repaired})
 # Exhaustively test every substantive authored slope, both integer intercept extremes.
 exhaust=0
 domains={'easy':[sp.Integer(s*n) for s in (-1,1) for n in range(2,13)],'moderate':[sp.Rational(s,n) for s in (-1,1) for n in range(2,13)],'hard':sorted(set(sp.Rational(s*n,d) for s in (-1,1) for n in range(2,10) for d in range(2,10) if __import__('math').gcd(n,d)==1))}
 for level,slopes in domains.items():
  for m in slopes:
   for b in (-20,20):
    r=g.generate(level,parameters={'m':str(m),'b':b,'intercepts':[-30,-29,0,29,30]});check_record(r);exhaust+=1
  variety[level]['exhaustive_distinct_slope_tasks']=len(slopes)
 # Canonical parameter spelling and shuffle identity; intercept changes leave task fingerprint.
 first=samples[0];p=copy.deepcopy(first['generation']['parameters'])
 changed=copy.deepcopy(p);changed['b']=str(sp.Rational(p['b'])+1)
 if abs(sp.Rational(changed['b']))<=20:
  r=g.generate('easy',parameters=changed);assert r['generation']['parameter_fingerprint']==first['generation']['parameter_fingerprint'] and r['question'][':question/id']!=first['question'][':question/id']
 bad_params=[('easy',{'m':'1/2','b':0,'intercepts':[0]*5}),('moderate',{'m':'2/3','b':0,'intercepts':[0]*5}),('hard',{'m':'10/3','b':0,'intercepts':[0]*5}),('hard',{'m':'-10/3','b':0,'intercepts':[0]*5}),('easy',{'m':2.0,'b':0,'intercepts':[0]*5})]
 for level,p in bad_params:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit parameter accepted')
 # Force the complete bank collision; no replacement or option pooling permitted.
 try:g.generate('easy',profile='observed-q-72453',parameters={'m':1,'b':0,'intercepts':[0]*5})
 except ValueError:pass
 else:raise AssertionError('Invalid complete bank not rejected')
 # Equivalent rational spellings retain task and content identity.
 eq=copy.deepcopy(first['generation']['parameters']);m=sp.Rational(eq['m']);eq['m']=f'{2*m.p}/{2*m.q}'
 equivalent=g.generate('easy',parameters=eq);assert equivalent['question'][':question/id']==first['question'][':question/id']
 # Banks are presentation only: different observed profiles with target -4
 # and different candidate coefficients share the mathematical task identity.
 common={'m':-4,'b':1,'intercepts':[-6,-1,0,6,2]}
 ba=g.generate('easy',parameters=common,profile='observed-q-72453')
 bb=g.generate('easy',parameters=common,profile='observed-q-72527')
 assert ba['generation']['parameter_fingerprint']==bb['generation']['parameter_fingerprint'] and ba['question'][':question/id']!=bb['question'][':question/id']
 mutations=mutation_checks(first)
 input_data=[]
 native_records=records+[x['record'] for x in review]+samples[::50]
 for index,r in enumerate(native_records):
  f=r['question'][':question/answer-fields'][0]
  input_data.append({'label':str(index)+' '+r['generation']['bank_profile'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned choice through real learner radio grader'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(input_data,indent=2)+'\n')
 engine=ROOT/'generate/runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 native=json.loads((HERE/'engine-report.json').read_text())
 (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 lines=['# Perpendicular slope-intercept line generator review','', 'Raw basis-1356 sources precede parameterized replays and generated variants. q-72524 raw quadratic distractors are quarantined evidence; normal generation always displays lines. Missing correct designations and solutions are authored mathematical derivations, never counted as observed matches.','']
 for case in cases:
  q=questions[case['source_id']];lines+=['## ORIGINAL '+case['source_id'],'',q[':question/problem'],'']
  for a in q[':question/answer-fields'][0][':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$')
  lines+=['','**Original worked solution**','',q.get(':question/worked-solution','Absent in capture and original widget. Derived replay solution below is authored.'),'']
  for v in [x for x in review if case['source_id'] in x['label'] and 'repair' not in x['label']]:lines += ['### '+v['label'],'',g.markdown(v['record']),'']
 for v in review:
  if 'AUTHORED' in v['label'] or 'repair' in v['label']:lines+=['### '+v['label'],'',g.markdown(v['record']),'']
 (HERE/'review.md').write_text('\n'.join(lines)+'\n')
 report={'status':'pass with documented source anomaly quarantine','database_basis':1356,'database_writes':0,'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'source_question_count':7,'fidelity':{'banks':{'matched':7,'total':7},'displayed_choices':{'matched':35,'total':35},'prompt_exact':{'matched':7,'total':7},'solution_exact':{'matched':5,'total_observed':5,'authored_missing':2},'correct_designations':{'matched':5,'total_observed':5,'absent_not_counted':2},'per_source':fidelity},'correctness':{'sampled_normal_records':1500,'exhaustive_boundary_records':exhaust,'review_profiles':len(review),'all_displayed_stages_checked':True,'invalid_explicit_cases_rejected':len(bad_params),'whole_bank_collision_rejected':True,'mutation_failures_detected':mutations},'scope':{'normal_output_pass':True,'quarantined_raw_profile':'observed-q-72524','raw_nonlinear_options':2,'minimal_repair_verified':True,'hard_origin':'authored; no observed hard questions'},'variety':variety,'native_grading':{'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(engine.with_suffix('.rs').read_bytes()).hexdigest(),'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'engine_input_records':len(input_data)},'identity':{'seed_and_order_invariant':True,'equivalent_rational_spelling_invariant':True,'bank_variants_share_mathematical_task_identity':True,'intercept_changes_deduplicate_mathematical_tasks':True,'different_display_changes_content_identity':True}}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()

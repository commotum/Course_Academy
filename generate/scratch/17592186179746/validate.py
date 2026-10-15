"""Exact, rendered-value, replay, finite-domain and actual application grading QA."""
import copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,t=g.x,g.y,g.t
# Independent integration oracle: source path and independently evaluated flux.
ORACLE={
'q-126940':(t,t**2,0,1,s.Rational(1,3)),
'q-127151':(t**2,t,0,1,s.Integer(2)),
'q-127153':(1/t,t,s.Rational(1,2),2,2*s.log(2)+s.Rational(3,2)),
'q-127223':(t/2,1/(2*t),s.Rational(1,2),2,-s.Rational(9,2)),
'q-127227':(s.log(t),t,1,s.E,s.Integer(1)),
'q-127233':(t,t,0,1,s.Integer(-1)),
'q-126943':(t**2/4,t,0,2,s.Integer(8)),
'q-127244':(t,t**3,0,1,-s.Rational(14,5)),
'q-127253':(t,1-t,0,1,s.Integer(-2)),
'q-127254':(-s.log(t),t,1/s.E,1,1-s.exp(-2)),
'q-127256':(s.exp(t),t,0,1,-s.Rational(2,3)),
'q-127235':(t,1/t,s.Rational(1,2),2,s.Integer(0)),
}

def independent(r):
 meta=r['generation'];template=meta['template'];scale=meta['parameters']['scale'];src=g.SOURCES[template];question=r['question']
 assert r['knowledge_point']['db_id']==g.KP_ID and str(r['knowledge_point']['id'])==str(g.NAMESPACE)
 assert meta['profile']=='observed-scaled:'+template and scale in (1,)+g.SCALES
 prompt=question[':question/problem'];solution=question[':question/worked-solution']
 start=prompt.index('F(x,y)=')+len('F(x,y)=');end=prompt.index('$',start)
 field=prompt[start:end]
 if scale==1:
  # In source notation a missing i coefficient means zero; every supported
  # source still explicitly contains i except q-127254 (only j).
  pass
 if scale!=1:
  match=re.fullmatch(r'\((.*?)\)\\,i\+\((.*?)\)\\,j',field);assert match,field
  p,q=map(g.parse,match.groups())
 else:
  # Parse the original field, including implicit unit/zero components.
  if r'\,i' in field:
   atext,rest=field.split(r'\,i');p=g.parse(atext or '1')
   assert rest.endswith(r'\,j');qtext=rest[:-3]
   q=g.parse(qtext if qtext not in ('','+','-') else qtext+'1')
  else:
   assert field.endswith(r'\,j');p=s.Integer(0);q=g.parse(field[:-3])
 a,b,lo,hi,oracle=ORACLE[template]
 u=s.simplify(p.subs({x:a,y:b},simultaneous=True));v=s.simplify(q.subs({x:a,y:b},simultaneous=True))
 # Integrate contributions independently, rather than using generator's
 # combined integrand/antiderivative routine.
 first=s.integrate(u*s.diff(b,t),(t,lo,hi));second=s.integrate(v*s.diff(a,t),(t,lo,hi));answer=s.simplify(first-second)
 assert s.simplify(answer-scale*oracle)==0,(template,answer,oracle)
 f=question[':question/answer-fields'][0];assert len(question[':question/answer-fields'])==1
 assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 choices=f[':answer-field/choices'];assert len(choices)==5 and len({a[':answer/id'] for a in choices})==5
 values=[g.parse(a[':answer/value']) for a in choices];expected=[scale*g.parse(a[':answer/value']) for a in src[':question/answer-fields'][0][':answer-field/choices']]
 assert all(sum(s.simplify(v-w)==0 for w in values)==1 for v in expected)
 assert all(sum(s.simplify(v-w)==0 for w in values)==1 for v in values)
 correct=next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);assert s.simplify(g.parse(correct[':answer/value'])-answer)==0
 assert all('$' not in a[':answer/value'] for a in choices)
 assert question[':question/difficulty']==':question.difficulty/'+g.DATA[template][-1]
 assert meta['mathematical_signature']==g.signature(template,scale)
 assert question[':question/id']==g.generate(g.DATA[template][-1],template=template,parameters={'scale':scale})['question'][':question/id']
 # Source geometry and normal-direction cue stay fixed. Only the field is
 # replaced; deliberate corruption of a path/normal cue must fail this check.
 old=src[':question/problem'];i=old.index('F(x,y)=')+len('F(x,y)=');j=old.index('$',i)
 assert prompt[:start]==old[:i] and prompt[end:]==old[j:]
 assert re.findall(r'!\[.*?\]\((.*?)\)',solution)==re.findall(r'!\[.*?\]\((.*?)\)',src[':question/worked-solution'])
 if scale!=1:
  # Read each displayed substitution and derivative independently.
  substitution=re.search(r'P\(x,y\)&=(.*?)=(.*?), \\\\ Q\(x,y\)&=(.*?)=(.*?)\.\\end',solution)
  assert substitution,template
  for actual,want in zip(substitution.groups(),(p,u,q,v)):assert s.simplify(g.parse(actual)-want)==0,(template,actual,want)
  deriv=re.search(r'\\frac\{\\mathrm\{d\}x\}\{\\mathrm\{d\}t\}&=\\frac\{\\mathrm\{d\}\}\{\\mathrm\{d\}t\}\((.*?)\)=(.*?), \\\\ \\frac\{\\mathrm\{d\}y\}\{\\mathrm\{d\}t\}&=\\frac\{\\mathrm\{d\}\}\{\\mathrm\{d\}t\}\((.*?)\)=(.*?)\.\\end',solution)
  assert deriv,template
  for actual,want in zip(deriv.groups(),(a,s.diff(a,t),b,s.diff(b,t))):assert s.simplify(g.parse(actual)-want)==0
  final=solution.rsplit('&=',1)[1].split(r'.\end')[0];assert s.simplify(g.parse(final)-answer)==0
  # Read integrand and primitive out of the displayed final integration chain.
  z=re.findall(r'\}\((.*?)\)\\,\\mathrm\{d\}t',solution)[-1]
  assert s.simplify(g.parse(z)-(u*s.diff(b,t)-v*s.diff(a,t)))==0
  anti=re.findall(r'\\left\[(.*?)\\right\]',solution)[-1];assert s.simplify(s.diff(g.parse(anti),t)-g.parse(z))==0
 for text in (prompt,solution):assert text.count('$')%2==0 and text.count('{')==text.count('}')
 return answer

def checks(r):
 independent(r);f=r['question'][':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each complete profile radio option'} for a in f[':answer-field/choices']]

def main():
 replay=[];records=[];mapping=[]
 for template in g.DATA:
  src=g.SOURCES[template];level=g.DATA[template][-1];r=g.generate(level,template=template,parameters={'scale':1});independent(r)
  assert r['question'][':question/problem']==src[':question/problem'] and r['question'][':question/worked-solution']==src[':question/worked-solution']
  sf=src[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
  assert sf[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
  replay.append({'source':template,'db_id':src[':db/id'],'complete_bank':'5/5','distractors':'4/4','exact_prompt_solution':True,'correct_key':True})
  records.append(r)
  for a in sf[':answer-field/choices']:
   value=g.parse(a[':answer/value']);mapping.append({'source':template,'profile':'observed-scaled:'+template,'field':'selection','answer_id':a[':answer/id'],'original':a[':answer/value'],'recipe':'scale * ('+str(value)+')','expression':str(value),'correct':a[':answer/id']==sf[':answer-field/correct'][':answer/id'],'replay':True,'error_interpretation':'observed expression, mechanism unresolved; no invented learner feedback'})
  for scale in g.SCALES:
   r=g.generate(level,template=template,parameters={'scale':scale});independent(r);records.append(r)
 # Check seeds exercise every declared family and every positive scale.
 for level in g.SUPPORTED_LEVELS:
  sampled=[g.generate(level,seed) for seed in range(180)]
  assert {r['generation']['template'] for r in sampled}=={k for k,d in g.DATA.items() if d[-1]==level}
  assert {r['generation']['parameters']['scale'] for r in sampled}==set(g.SCALES)
 r=g.generate('moderate',template='q-126940',parameters={'scale':2});r2=g.generate('moderate',template='q-126940',parameters={'scale':3});assert independent(r)!=independent(r2)
 bad=copy.deepcopy(r2);bad['question'][':question/worked-solution']=r['question'][':question/worked-solution']
 bad2=copy.deepcopy(r2);f=bad2['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
 bad3=copy.deepcopy(r2);bad3['question'][':question/problem']=bad3['question'][':question/problem'].replace('[0,1]','[0,2]')
 for broken in (bad,bad2,bad3):
  try:independent(broken)
  except AssertionError:pass
  else:raise AssertionError('stale solution/key/geometry survived')
 for level in ('easy','unclassified'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('unsupported level accepted')
 assert len({r['generation']['mathematical_signature'] for r in records})==108
 assert g.generate('hard',17)==g.generate('hard',17)
 fixtures=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]
 (HERE/'engine-input.json').write_text(json.dumps(fixtures))
 subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 (HERE/'source-choice-mapping.json').write_text(json.dumps(mapping,indent=2))
 review=[g.generate(level,template=template,parameters={'scale':scale}) for level,template in [('moderate','q-126940'),('moderate','q-127153'),('hard','q-126943'),('hard','q-127254')] for scale in (1,2,5)]
 (HERE/'review.json').write_text(json.dumps(review,indent=2));(HERE/'review.md').write_text('\n\n---\n\n'.join(map(g.markdown,review)))
 report={'status':'pass','source_basis':g.SNAPSHOT['basis'],'source_replays':replay,'source_distractors':'48/48','source_complete_banks':'12/12','source_exclusions':g.EXCLUDED,'exact_independent_records':108,'normal_sample_variants':96,'slot_coverage':{'positive_common_scale':list(g.SCALES),'templates':list(g.DATA),'fixed_curve_limits_and_right_normal':True},'stale_value_mutations_rejected':3,'native':json.loads((HERE/'engine-report.json').read_text()),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='native'},indent=2))
if __name__=='__main__':main()

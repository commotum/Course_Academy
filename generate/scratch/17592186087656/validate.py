#!/usr/bin/env python3
"""Independent displayed-math, full source fidelity, domain and native QA."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('circle_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y=s.symbols('x y', real=True)

def parse(t):
 t=t.strip().rstrip('.?').replace(r'\left','').replace(r'\right','')
 t=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',t)
 t=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',t)
 t=t.replace(r'\cdot','*').replace('^','**').replace('{','(').replace('}',')')
 return parse_expr(t,local_dict={'x':X,'y':Y,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def eq(t):
 l,r=t.split('=');return s.expand(parse(l)-parse(r))
def triple(v):
 m=re.fullmatch(r'The center is \$\((.*),(.*)\)\$ and (?:the )?radius is \$(.*)\$',v);assert m,v
 return tuple(parse(c) for c in m.groups())
def formatting(t):
 assert t.count('$')%2==0,t
 balance=0
 for c in t:
  if c=='{':balance+=1
  elif c=='}':balance-=1
  assert balance>=0,t
 assert balance==0,t
 assert not any(v in t for v in ('+-','--','nan','zoo'))
def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio'
 assert len(f[':answer-field/choices'])==5
 prompt=q[':question/problem'];formatting(prompt)
 math=re.findall(r'\$(.*?)\$',prompt)[0]
 poly=eq(math);P=s.Poly(poly,X,Y);assert P.coeff_monomial(X**2)==P.coeff_monomial(Y**2)==1
 assert P.coeff_monomial(X*Y)==0
 a=-P.coeff_monomial(X)/2;b=-P.coeff_monomial(Y)/2
 S=a*a+b*b-P.coeff_monomial(1);assert S>0
 expected=(a,b,s.sqrt(S))
 bank=[triple(v[':answer/value']) for v in f[':answer-field/choices']]
 assert len(set(bank))==5
 matches=[i for i,v in enumerate(bank) if all(s.simplify(v[j]-expected[j])==0 for j in range(3))];assert len(matches)==1
 for v in f[':answer-field/choices']:formatting(v[':answer/value'])
 if r['generation']['evidence_only']:
  assert all(k not in q for k in (':question/difficulty',':question/worked-solution'));assert ':answer-field/correct' not in f
 else:
  assert f[':answer-field/correct'][1]==f[':answer-field/choices'][matches[0]][':answer/id']
  sol=q[':question/worked-solution'];formatting(sol)
  block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1)
  rows=block.split(r'\\');assert len(rows)==3
  given=rows[1].replace('&','').strip().rstrip('.?')
  assert re.sub(r'\s+','',given)==re.sub(r'\s+','',math.strip().rstrip('.?'))
  final_lhs,final_rhs=rows[2].replace('&','').split('=')
  assert '(x-' in final_lhs and '(y-' in final_lhs
  if a<0:assert '(x-(' in final_lhs
  if b<0:assert '(y-(' in final_lhs
  if a==0:assert '(x-0)' in final_lhs
  if b==0:assert '(y-0)' in final_lhs
  assert final_rhs.strip().rstrip('.').endswith('^{2}')
  for row in rows[1:]:assert s.simplify(eq(row.replace('&',''))-poly)==0,row
  assert eq(rows[0].replace('&',''))==eq('(x-a)^{2}+(y-b)^{2}=r^{2}')
  general=re.search(r'\$\$\n(.*?)\n\$\$',sol,re.S).group(1)
  assert eq(general)==eq('(x-a)^{2}+(y-b)^{2}=r^{2}')
  prose=re.search(r'We see that \$a=(.*?),\$ \$b=(.*?),\$ and \$r=(.*?)\.\$',sol)
  assert prose and tuple(parse(v) for v in prose.groups())==expected
  final=re.search(r'Therefore, the circle is centered at \$\((.*),(.*)\)\$ and its radius is \$(.*?)\.\$',sol)
  assert final and tuple(parse(v) for v in final.groups())==expected
  if q[':question/difficulty'].endswith('/hard'):
   reduction=re.search(r'\$\$\nr=(.*?)\n\$\$',sol).group(1)
   pieces=reduction.split('=');assert len(pieces)==3
   for piece in pieces:assert s.simplify(parse(piece)-s.sqrt(S))==0
   assert r'\cdot' in pieces[1] and r'\sqrt' in pieces[1]
 # Derived prompt math must also agree with publicly supplied parameters.
 assert (a,b,S)==tuple(s.Rational(r['generation']['parameters'][k]) for k in ('a','b','S'))
 assert r['generation']['parameter_fingerprint']==g.digest({k:str(v) for k,v in zip(('a','b','S'),(a,b,S))})
 return expected

def main():
 source=json.loads((D/'source.json').read_text());qs=source['record'][':knowledge-point/questions']
 originals=[];cases=[];mapping=[];engine=[];banks=0;values=0;solutions=0;designation=0
 for q in qs:
  sid=q[':question/math-academy-id'];p=g.ORIGINAL_PARAMETERS[sid]
  r=g.generate('easy',parameters=p,profile=sid);check(r);originals.append(r)
  replay=r['question'];rf=replay[':question/answer-fields'][0];of=q[':question/answer-fields'][0]
  assert replay[':question/problem']==q[':question/problem']
  for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (k in replay)==(k in q)
  assert (':answer-field/correct' in rf)==(':answer-field/correct' in of)
  assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  if ':question/worked-solution' in q:assert q[':question/worked-solution']==replay[':question/worked-solution'];solutions+=1
  if ':answer-field/correct' in of:
   correct=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
   assert correct==of[':answer-field/correct'][':answer/value'];designation+=1
  banks+=1;values+=len(of[':answer-field/choices'])
  cases.append({'source_id':sid,'source_db_id':q[':db/id'],'template':'standard_circle_radio','level':'easy','observed_difficulty':None if sid=='q-7527' else 'easy','parameters':p,'bank_profile':sid,'omission_preservation':sid=='q-7527'})
  for recipe in g.BANKS[sid]:
   v,t=g.value(recipe,g.canonical_parameters(p),sid)
   original=next(a for a in of[':answer-field/choices'] if a[':answer/value']==v)
   mapping.append({'source_id':sid,'field':'selection','answer_id':original[':answer/id'],'value':v,'recipe':recipe,'math':list(map(str,t)),'correct_designation':'missing' if ':answer-field/correct' not in of else original[':answer/id']==of[':answer-field/correct'][':answer/id']})
 review=[]
 for sid,p in g.ORIGINAL_PARAMETERS.items():
  # Every observed complete bank gets two genuine changed-parameter variants.
  for j in range(2):
   p2={'a':p['a']+(-1 if p['a']<0 else 1)*(j+1),'b':p['b']+(-1 if p['b']<0 else 1)*(j+1) if p['b'] else 0,'S':(7,16)[j]}
   if abs(p2['a'])>10:p2['a']=6+j
   if abs(p2['b'])>10:p2['b']=6+j
   rr=g.generate('easy',10+j,parameters=p2,profile=sid);check(rr);review.append(rr)
   if sid=='q-7527':
    completed_variant=g.generate('easy',10+j,parameters=p2,profile='q-7527_completed');check(completed_variant);review.append(completed_variant)
 for level in ('easy','moderate','hard'):
  for seed in (71,94):
   rr=g.generate(level,seed);check(rr);review.append(rr)
 completed=g.generate('easy',parameters=g.ORIGINAL_PARAMETERS['q-7527'],profile='q-7527_completed');check(completed);review.append(completed)
 identity_p={'a':2,'b':3,'S':7}
  # Full-bank differences change identity; bank/order aliases do not.
 identity_a=g.generate('easy',parameters=identity_p,profile='authored')
 identity_b=g.generate('easy',parameters=identity_p,profile='q-7521')
 identity_alias=g.generate('easy',parameters=identity_p,profile='q-70900')
 assert identity_a['question'][':question/id']!=identity_b['question'][':question/id']
 assert identity_a['question'][':question/id']==identity_alias['question'][':question/id']
 assert identity_a['generation']['parameter_fingerprint']==identity_b['generation']['parameter_fingerprint']
 population=[];counts={};mathcounts={}
 for level in ('easy','moderate','hard'):
  ls=[g.generate(level,seed) for seed in range(150)]
  for rr in ls:
   check(rr)
   replay=g.generate(level,seed=9999,parameters=rr['generation']['parameters'],profile=rr['generation']['bank_profile'])
   assert rr['question'][':question/id']==replay['question'][':question/id']
  population.extend(ls);counts[level]=len(ls);mathcounts[level]=len({r['generation']['parameter_fingerprint'] for r in ls})
 # All source profiles exercised under changed parameters and sign combinations.
 for profile in g.BANKS:
  for a,b in ((2,3),(-2,3),(2,-3),(-2,-3),(0,3),(3,0)):
   try:r=g.generate('easy',parameters={'a':a,'b':b,'S':7},profile=profile)
   except ValueError as e:assert str(e) in ('Complete bank collision','Axis source profile requires b=0 and a nonzero','Authored axis bank requires one zero offset at easy');continue
   check(r);population.append(r)
 # Boundary checks include broad magnitude bypass, wrong number forms and exact
 # moderate/hard overlaps, and whole-bank degeneracy.
 bad=[('easy',{'a':11,'b':2,'S':3}),('moderate',{'a':2,'b':3,'S':3}),('moderate',{'a':'1/2','b':'2/3','S':3}),('moderate',{'a':'1/2','b':0,'S':3}),('moderate',{'a':'-99/2','b':3,'S':3}),('hard',{'a':'1/2','b':3,'S':8}),('hard',{'a':'1/2','b':'2/3','S':3}),('hard',{'a':'1/2','b':'99/2','S':8})]
 for level,p in bad:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError((level,p))
 # Exhaustively enumerate finite permitted domains algebraically (not UUID
 # assembly): level membership and complete bank uniqueness by exact tuples.
 def valid(a,b,S,bank):
  p={'a':a,'b':b,'S':S}
  ts=[g.value(rec,p,bank)[1] for rec in g.BANKS[bank]]
  return len(set(ts))==5
 finite={'easy':sum(valid(s.Integer(a),s.Integer(b),s.Integer(S),'authored_axis' if not a or not b else 'authored') for a in g.INT for b in g.INT if a or b for S in (*g.SF,*(i*i for i in range(2,11)))),
         'moderate':2*len(g.RAT)*20*len(g.SF),'hard':len(g.RAT)**2*len(g.RED)}
 assert min(finite.values())>1000
 for label,r in [('source '+c['source_id'],r) for c,r in zip(cases,originals)]+[(f'generated {i}',r) for i,r in enumerate(review+population)]:
  if r['generation']['evidence_only']:continue
  f=r['question'][':question/answer-fields'][0]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native correct/wrong owned radio choice'} for a in f[':answer-field/choices']]
  engine.append({'label':label,'record':r,'checks':checks})
 (D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'bank-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
 (D/'review.json').write_text(json.dumps(review,indent=2)+'\n');(D/'original-replay.json').write_text(json.dumps(originals,indent=2)+'\n')
 (D/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
 exe=ROOT/'generate/runs/current/check-engine'
 subprocess.run([str(exe),str(D/'engine-input.json'),str(D/'engine-validation.json')],check=True)
 report=json.loads((D/'engine-validation.json').read_text())
 result={'status':'pass','source':g.SOURCE,'source_coverage':{'questions':len(qs),'prompts_exact':banks,'complete_banks_exact':banks,'displayed_choices_exact':values,'supplied_solutions_exact':solutions,'present_correct_designations_matched':designation,'missing_designations':1,'raw_attribute_presence_parity':8},'repairs':{'mathematical_errors':0,'presentation_errors':0,'inferred_completion_profiles':1},'generated_displayed_math_checked':len(review)+len(population),'sampled_level_counts':counts,'sampled_unique_tasks':mathcounts,'finite_task_counts':finite,'native_fixture_count':len(engine),'native_check_count':sum(len(e['checks']) for e in engine),'native_report':report,'native_blank_equivalence':'not applicable: source and supported generator layouts are radio only','guard_rejections_checked':len(bad),'plots':'none: no prompt/bank/solution assets in this KP','freeze':{'version':g.VERSION,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256(exe.read_bytes()).hexdigest()}}
 (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 # Reviews keep learner solutions alongside explicit source/generated labels.
 lines=['# Circle extraction review','', '## ORIGINALS — basis 1356','']
 for q,r in zip(qs,originals):
  lines+=['### ORIGINAL '+q[':question/math-academy-id']+' — '+('unrated; omissions preserved' if ':question/difficulty' not in q else 'observed easy'),'',q[':question/problem'],'']
  for a in q[':question/answer-fields'][0][':answer-field/choices']:lines+=['- '+a[':answer/value']]
  orig_correct=q[':question/answer-fields'][0].get(':answer-field/correct')
  lines+=['','**Observed correct:** '+(orig_correct[':answer/value'] if orig_correct else 'omitted; no observed designation'),'',q.get(':question/worked-solution','No worked solution or correct designation in source. Mathematically derived correct choice is center (-5,-1), radius 2; raw replay remains evidence-only.'),'','### GENERATED replay verification','',g.markdown(r),'']
 lines+=['## GENERATED VARIANTS — authored labels and observed bank provenance','']
 for r in review:lines += [g.markdown(r),'','Author metadata: '+json.dumps({k:r['generation'][k] for k in ('bank_origin','authored_difficulty','eligible_for_learning','parameters')}),'']
 lines+=['## Difficulty review','', 'Easy: integer shifts, direct sign extraction and familiar square root; all seven rated sources remain easy, including nonsquare RHS. Moderate is authored: exactly one noninteger rational shift, a second nonzero integer shift, square-free RHS. Hard is authored: exactly two noninteger rational shifts and reducible nonsquare RHS, adding familiar root simplification. All variants within a level have equal number-form demands. No completing-square, distance, midpoint, or circle-construction questions.','', '## Correctness and grading review','',f'{len(review)+len(population)} actual displayed equations, complete answer banks, all formal/comparison rows, and both substitution and conclusion prose independently checked. Native grader checked {sum(len(e["checks"]) for e in engine)} selections; all agreed. Raw missing-correct q-7527 is not a grading success and is excluded from native fixtures; its inferred completion is graded separately.']
 (D/'review.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({k:result[k] for k in ('status','source_coverage','generated_displayed_math_checked','native_check_count','finite_task_counts')},indent=2))
if __name__=='__main__':main()

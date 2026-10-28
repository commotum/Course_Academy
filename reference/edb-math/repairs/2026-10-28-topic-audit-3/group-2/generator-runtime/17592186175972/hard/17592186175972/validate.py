#!/usr/bin/env python3
"""Private QA: independently parse rendered vectors, relations and solutions.
Native grader fixtures use the real memory-only application engine. No DB writes.
"""
import copy, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('parabolic_generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
AXES='xyz'; SYMBOLS={x:sp.Symbol(x,real=True) for x in AXES}

def parse(text):
 text=text.strip().replace(r'\,','').replace('{','').replace('}','').replace('^','**').replace(r'\sin','sin')
 # Generated fractions use integer numerator/denominator complete TeX components.
 text=re.sub(r'\\frac(-?\d+)(\d+)',r'(\1/\2)*',text)
 return parse_expr(text,local_dict={**SYMBOLS,'sin':sp.sin},transformations=standard_transformations+(implicit_multiplication_application,))

def expr(text):
 text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)*',text)
 return parse(text)

def parsed(record):
 q=record['question'];prompt=q[':question/problem']
 match=re.search(r'([fgh])\(([^)]*)\)\s*=\s*⟨([^⟩]+)⟩',prompt);assert match,'Actual shown formula absent'
 fn,args,body=match.groups();args=[x.strip() for x in args.split(',')]
 assert len(args)==2 and set(args)<=set(AXES)
 vector=body.replace(r'\,','').split(',');assert len(vector)==3
 target=re.search(r'What is the (first|second|third) component',prompt).group(1);target=['first','second','third'].index(target)
 assert '?' in vector[target] or '___' in vector[target]
 relation=re.search(r'Cartesian coordinates as \$([^$]+)\$',prompt).group(1).rstrip('.')
 lhs,rhs=relation.split('=');poly=sp.Poly(expr(lhs)-expr(rhs),*[SYMBOLS[x] for x in AXES])
 degree={x:poly.degree(SYMBOLS[x]) for x in AXES};assert sorted(degree.values())==[0,1,2]
 base=next(x for x in AXES if degree[x]==2);dep=next(x for x in AXES if degree[x]==1);free=next(x for x in AXES if degree[x]==0)
 assert set(args)=={base,free},'Actual shown parameter coverage wrong'
 solved=sp.solve(poly.as_expr(),SYMBOLS[dep]);assert len(solved)==1
 assert solved[0].is_polynomial(SYMBOLS[base])
 assert sp.Poly(solved[0],SYMBOLS[base]).monoms()==[(2,)],'Only one quadratic monomial allowed'
 assert AXES[target] in (dep,free),'Role changed to base computation'
 given=[None if i==target else expr(v) for i,v in enumerate(vector)]
 expected=[solved[0] if x==dep else SYMBOLS[x] for x in AXES]
 for i,v in enumerate(given):
  if v is not None:assert sp.simplify(v-expected[i])==0,'Incorrect supplied coordinate'
 # Independent check of every actual prose function mention, excluding flagged raw inline mismatch.
 mentions=re.findall(r'\$([fgh])\(([^)]*)\)\$',prompt)
 for name,a in mentions:
  if not(record['generation']['evidence_only'] and record['generation']['profile']=='q-103992_raw'):
   assert name==fn and [x.strip() for x in a.split(',')]==args,'Stale prose function arguments'
 return fn,args,target,base,dep,free,given,expected,poly.as_expr()

def candidates(record):
 fn,args,t,u,d,v,given,expected,relation=parsed(record)
 rows=[]
 for f in record['question'][':question/answer-fields']:
  options=[]
  for choice in f[':answer-field/choices']:
   inserted=given.copy();inserted[t]=expr(choice[':answer/value'])
   constraint=sp.simplify(relation.subs(dict(zip(SYMBOLS.values(),inserted)),simultaneous=True))==0
   base_direct=sp.simplify(inserted[AXES.index(u)]-SYMBOLS[u])==0
   image_free=inserted[AXES.index(v)]
   # Exact global fiber coverage for the complete supported banks, independently
   # distinguishing even-square half-axis, bounded sine and absent free parameter.
   coverage=False
   if image_free.is_polynomial(SYMBOLS[v]):
    pol=sp.Poly(image_free,SYMBOLS[v]);coverage=pol.degree()==1 and pol.LC()!=0
   geometric=constraint and base_direct and coverage
   direct=all(sp.simplify(x-y)==0 for x,y in zip(inserted,expected))
   options.append({'id':choice[':answer/id'],'value':choice[':answer/value'],'inserted':inserted,
                   'relation':bool(constraint),'free_coverage':bool(coverage),'geometrically_valid':bool(geometric),'direct_eligible':bool(direct)})
  # Compare all pairs as complete inserted maps. Geometric surface equivalence
  # is also recorded for the two unrestricted free-axis linear parametrizations.
  aliases=[]
  for a,b in itertools.combinations(options,2):
   assert not all(sp.simplify(x-y)==0 for x,y in zip(a['inserted'],b['inserted'])),'Duplicate complete map'
   if a['geometrically_valid'] and b['geometrically_valid']:aliases.append([a['value'],b['value']])
  rows.append((f,options,aliases))
 return rows

def normal_math(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert not record['generation']['evidence_only'] and record['generation']['eligible_for_learning']
 q=record['question'];assert '?' in q[':question/problem'] and '{{selection}}' not in q[':question/problem']
 fn,args,t,u,d,v,given,expected,relation=parsed(record)
 for f,opts,aliases in candidates(record):
  assert len(opts)==5
  assert sum(o['direct_eligible'] for o in opts)==1
  correct=f[':answer-field/correct'][1]
  assert next(o for o in opts if o['id']==correct)['direct_eligible']
  if AXES[t]==v:
   assert 'Use the named parameters directly' in q[':question/problem']
   assert 'free-axis coordinate is $'+v+'.$' in q[':question/worked-solution']
  else:assert not aliases,'Multiple covering choices for dependent role'
 solution=q[':question/worked-solution']
 assert solution.count('For any point $(x,y,z)$ on our surface')==1
 vecs=re.findall(r'⟨([^⟩]*)⟩',solution);assert len(vecs)==2
 assert vecs[0]=='x,y,z','Cartesian basis order changed'
 solved=[expr(x) for x in vecs[1].replace(r'\,','').split(',')]
 assert all(sp.simplify(x-y)==0 for x,y in zip(solved,expected)),'Wrong displayed completed solution vector'
 solution_fn=re.search(r'([fgh])\(([^)]*)\)\s*&',solution)
 assert solution_fn and solution_fn[1]==fn and solution_fn[2].split(',')==args
 conclusion=re.search(r'Therefore, the (first|second|third) component of \$([fgh])\$ is \$([^$]*)\$',solution)
 assert conclusion and ['first','second','third'].index(conclusion[1])==t and conclusion[2]==fn
 assert sp.simplify(expr(conclusion[3].rstrip('.'))-expected[t])==0,'Stale solution conclusion'
 for arg in args:assert '$'+arg+r'\in (-\infty ,\infty )$' in solution or '$'+arg+r'\in (-\infty ,\infty ).$' in solution
 if q[':question/difficulty']==':question.difficulty/hard':
  norm=re.search(r'\$\$\n([^\n]+)\\quad\\Longrightarrow\\quad ([^\n]+)',solution)
  assert norm,'Missing coefficient-isolation stage'
  for equality in norm.groups():
   a,b=equality.split('=');assert sp.simplify((expr(a)-expr(b)).subs(SYMBOLS[d],expected[AXES.index(d)]))==0
 for text in [q[':question/problem'],solution]+[o[':answer/value'] for f in q[':question/answer-fields'] for o in f[':answer-field/choices']]:
  assert not any(ord(x)<32 and x not in '\n\t\r' for x in text),'C0 control character'
 g.checked_normal(copy.deepcopy(record))
 return True

def source_compare(source,record):
 q=record['question'];s=source
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
  assert (key in s)==(key in q),'Raw source attribute presence drift '+key
 if ':question/difficulty' in s:assert s[':question/difficulty'][':db/ident']==q[':question/difficulty']
 assert s[':question/problem']==q[':question/problem'],'Full source prompt drift'
 if ':question/worked-solution' in s:assert s[':question/worked-solution']==q[':question/worked-solution'],'Full worked solution stage/prose drift'
 sf=s[':question/answer-fields'];gf=q[':question/answer-fields'];assert len(sf)==len(gf)
 for a,b in zip(sf,gf):
  for key in (':answer-field/key',':answer-field/correct'):
   assert (key in a)==(key in b),'Field attribute presence drift'
  assert a[':answer-field/type'][':db/ident']==b[':answer-field/type']
  assert a[':answer-field/key']==b[':answer-field/key']
  assert sorted(c[':answer/value'] for c in a[':answer-field/choices'])==sorted(c[':answer/value'] for c in b[':answer-field/choices']),'Exact complete source bank drift'
  if ':answer-field/correct' in a:
   val=next(c[':answer/value'] for c in b[':answer-field/choices'] if c[':answer/id']==b[':answer-field/correct'][1])
   assert val==a[':answer-field/correct'][':answer/value']
 return True

def run():
 wrapper=json.loads((HERE/'source.json').read_text());sources=wrapper['record'][':knowledge-point/questions']
 assert wrapper==json.loads((ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186175972.json').read_text())
 cases=[];raws=[];norms=[];source_geometry=[]
 for s in sources:
  sid=s[':question/math-academy-id'];level='moderate' if sid=='q-164450' else 'easy'
  case={'source_id':sid,'template':g.PROFILES[sid][0],'level':level,'parameters':g.OBSERVED_PARAMETERS[sid], 'profile':sid+'_raw','bank_profile':sid+'_raw'}
  r=g.generate(level,parameters=case['parameters'],template=case['template'],profile=case['profile']);source_compare(s,r);candidates(r)
  cases.append(case);raws.append(r)
  n=g.generate(level,parameters=case['parameters'],profile=sid);normal_math(n);norms.append(n)
  geometry=[]
  for i,(f,opts,aliases) in enumerate(candidates(r)):
   geometry.append({'field_index':i,'geometric_aliases':aliases,'choices':[{k:o[k] for k in ('value','relation','free_coverage','geometrically_valid','direct_eligible')} for o in opts]})
  source_geometry.append({'source_id':sid,'fields':geometry})
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 (HERE/'source-geometric-audit.json').write_text(json.dumps(source_geometry,indent=2)+'\n')
 review=[]
 # Show all source templates/banks in normal changed-parameter output, plus two/level.
 for i,c in enumerate(cases):
  n=g.generate(c['level'],seed=31+i,profile=c['source_id']);normal_math(n);review.append(n)
 for level in g.SUPPORTED_LEVELS:
  for seed in (102,205):
   n=g.generate(level,seed=seed);normal_math(n);review.append(n)
 (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 (HERE/'source-replays.json').write_text(json.dumps(raws,indent=2,ensure_ascii=False)+'\n')
 (HERE/'review-original-parameters.json').write_text(json.dumps(norms,indent=2,ensure_ascii=False)+'\n')
 # Full finite sampler capacity, not number-of-seeds uniqueness.
 identities={x:set() for x in g.SUPPORTED_LEVELS};slots={x:set() for x in identities};full=[]
 pairs=[(a,b) for a in range(2,13) for b in range(2,6) if sp.gcd(a,b)==1]
 for level in identities:
  profiles=['normalized'] if level=='hard' else ['q-164450'] if level=='moderate' else ['q-103986','q-164443','q-164441','q-164440','q-103992']
  for profile in profiles:
   role=g.TEMPLATES[g.PROFILES[profile][0]]['role']
   for u,d in itertools.permutations(AXES,2):
    v=next(x for x in AXES if x not in (u,d))
    coeffs=pairs if level=='hard' else [(a,1) for a in range(2,13)]
    for a,b in coeffs:
     p={'base':u,'dependent':d,'a':a,'b':b,'target':d if role=='dependent' else v,
        'argument_order':'free_first' if level=='moderate' or profile=='q-103992' else 'base_first',
        'relation_order':'quadratic_first' if level=='moderate' or profile=='q-103992' else 'dependent_first'}
     n=g.generate(level,parameters=p,profile=profile);normal_math(n);full.append(n)
     identities[level].add(n['generation']['task_fingerprint']);slots[level].add((u,d,p['target'],role))
 # Default family coverage and actual name/argument permutations at fixed math.
 default_profiles={level:{g.generate(level,seed=i)['generation']['profile'] for i in range(120)} for level in identities}
 assert default_profiles['easy']=={'q-103986','q-164443','q-164441','q-164440','q-103992'}
 for profile in ('q-103986','q-164440','q-103992'):
  level='hard' if profile=='normalized' else 'easy'
  p=dict(g.OBSERVED_PARAMETERS['q-164443'] if profile=='normalized' else g.OBSERVED_PARAMETERS[profile]);p['b']=2 if level=='hard' else 1
  if level=='hard':p['a']=3
  for name in ('f','g','h'):
   for order in ('base_first','free_first'):
    p.update(function=name,argument_order=order)
    normal_math(g.generate(level,parameters=p,profile=profile))
 # Read changed requested role from actual prompt/solution with fixed surface data.
 fixed_role=dict(g.OBSERVED_PARAMETERS['q-164440'])
 first=g.generate_easy(parameters=fixed_role,profile='q-164440');normal_math(first)
 fixed_role['target']='y'
 second=g.generate_easy(parameters=fixed_role,profile='q-164441');normal_math(second)
 assert parsed(first)[2]!=parsed(second)[2] and parsed(first)[-1]==parsed(second)[-1]
 # Identity and incidental-parameter regressions.
 fixed=dict(g.OBSERVED_PARAMETERS['q-164440']);a=g.generate_easy(parameters=fixed,profile='q-164440');b=g.generate_easy(seed=52,parameters=fixed,profile='q-164440')
 assert a['question'][':question/id']==b['question'][':question/id']
 fixed['a']=11;c=g.generate_easy(parameters=fixed,profile='q-164440')
 assert a['generation']['task_fingerprint']==c['generation']['task_fingerprint'] and a['question'][':question/id']!=c['question'][':question/id']
 # Mutation regressions: printed-vector, arguments, target, relation, conclusion,
 # stale basis, coverage ambiguity and controls must actually fail independent QA.
 mutation_count=0
 def rejects(record,mutate):
  nonlocal mutation_count
  x=copy.deepcopy(record);mutate(x)
  try:normal_math(x)
  except (AssertionError,ValueError,TypeError,AttributeError):mutation_count+=1;return
  raise AssertionError('Mutation accepted')
 baseline=norms[0]
 rejects(baseline,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('f(x,z)','f(x,y)',1)))
 rejects(baseline,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('second component','first component')))
 rejects(baseline,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('4{x}^{2}','5{x}^{2}')))
 rejects(baseline,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('⟨x,y,z⟩','⟨z,y,x⟩')))
 rejects(baseline,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('is $4{x}^{2}.$','is $4{z}^{2}.$')))
 rejects(baseline,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution']+'\f'))
 rejects(norms[2],lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace(' Use the named parameters directly as their corresponding Cartesian coordinates.','')))
 # Explicit scope/level/role boundaries must reject, not resample.
 guards=0
 for level,profile,changes in [('hard','normalized',{'a':4,'b':2}),('hard','normalized',{'a':13,'b':3}),('easy','q-164443',{'a':-3}),('moderate','q-164450',{'argument_order':'base_first'}),('easy','q-164440',{'target':'y'}),('easy','q-164443',{'function':'sin'}),('easy','q-164443',{'b':2})]:
  p=dict(g.OBSERVED_PARAMETERS['q-164443'] if profile=='normalized' else g.OBSERVED_PARAMETERS[profile]);p.update(changes)
  try:g.generate(level,parameters=p,profile=profile)
  except ValueError:guards+=1
  else:raise AssertionError('Invalid explicit parameters accepted')
 # Engine checks ALL whole choices on every selected source normal/changed bank,
 # including the authored completion and two hard examples. Radio IDs stay source type.
 fixtures=[]
 for index,n in enumerate(norms+review):
  checks=[]
  for f in n['question'][':question/answer-fields']:
   for option in f[':answer-field/choices']:
    checks.append({'submitted_answer_id':option[':answer/id'],'expected':'accepted' if option[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio choice; independent complete inserted map checked'})
  fixtures.append({'label':'normal-'+str(index),'record':n,'checks':checks})
 (HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True)
 engine=json.loads((HERE/'engine.json').read_text())
 bank_count=sum(len(s[':question/answer-fields']) for s in sources);choice_count=sum(len(f[':answer-field/choices']) for s in sources for f in s[':question/answer-fields'])
 report={'status':'passed', 'passed':True, 'supported_levels':list(g.SUPPORTED_LEVELS), 'unsupported_levels':['hard'],'source':g.SOURCE,'script_sha256':__import__('hashlib').sha256(SCRIPT.read_bytes()).hexdigest(),'source_wrapper_sha256':__import__('hashlib').sha256((HERE/'source.json').read_bytes()).hexdigest(),
 'source_questions':{'matched':6,'total':6},'source_banks':{'matched':bank_count,'total':bank_count},'source_choices':{'matched':choice_count,'total':choice_count},
 'source_distractors':{'matched':28,'total':28},'source_present_correct_designations':{'matched':5,'total':5},'source_missing_correct_designations':2,
 'source_exact_prompts':6,'source_exact_present_solutions':5,'source_absent_solution_preserved':1,'source_absent_difficulty_preserved':1,
 'normal_minimal_repairs':{'duplicate_field_removed':1,'keyed_placeholders':6,'prose_argument_mismatch':1,'authored_missing_solution':1,'inferred_correct':1,'unrated_easy_assignment':1,'free_direct_convention':2,'authored_q103986_complete_bank':1},
 'source_errors':['q103986 duplicate legacy field has no correct key','q103992 prose arguments conflict with actual shown vector; missing correct/solution/difficulty','q164440 z and 6z both geometrically cover cylinder; normal direct-coordinate convention repairs response criterion'],
 'exhaustive_generated_instances':len(full),'meaningful_task_capacity':{x:len(v) for x,v in identities.items()},'global_distinct_tasks':len(set.union(*identities.values())),
 'axis_role_slots':{x:[list(s) for s in sorted(v)] for x,v in slots.items()},'default_profile_coverage':{x:sorted(v) for x,v in default_profiles.items()},
 'hard_difficulty_claim':'unsupported: no source-backed same-stage hard template; public API rejects hard',
 'independent_math':'actual displayed formula/arguments/Cartesian basis/relation/target/whole inserted maps, global free-fiber coverage, every pair, completed solution vector, conclusion, coefficient-normalization row',
 'mutation_regressions':mutation_count,'invalid_parameter_guards':guards,'native_grading':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},
 'plots':'none','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'unresolved':['historical half-linear q103986 distractor intent underidentified; expression mask explicit','hard remains unsupported; draft normalization stage excluded'],
 'approval':'source replay and independent displayed-math checks passed; selected instances require fresh native grading and exact-basis readback'}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 write_review(sources,raws,norms,review,report)
 print(json.dumps({'source_banks':bank_count,'choices':choice_count,'capacity':report['meaningful_task_capacity'],'exhaustive':len(full),'native':report['native_grading']},indent=2))
 return report

def write_review(sources,raws,norms,review,report):
 lines=['# Parabolic-cylinder review','', 'Source evidence at math basis 2275; easy/moderate supported, hard rejected.','']
 for s,r,n in zip(sources,raws,norms):
  lines += ['## Original '+s[':question/math-academy-id'],'','Captured original / parameterized public raw replay:','',g.markdown(r),'','Raw correct presence: '+str([(':answer-field/correct' in f) for f in r['question'][':question/answer-fields']]),'','Normal presentation at original parameters (documented repairs):','',g.markdown(n),'']
 for i,r in enumerate(review):
  lines += ['## Generated variant '+str(i+1)+' — '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['profile'],'','Conservative parameter/axis extension within the observed graph-copy stages.','',g.markdown(r),'']
 lines += ['## Counts','',json.dumps({k:report[k] for k in ('source_questions','source_banks','source_choices','meaningful_task_capacity','global_distinct_tasks','native_grading','unresolved')},indent=2)]
 (HERE/'review.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':run()

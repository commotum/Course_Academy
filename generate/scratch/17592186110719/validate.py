"""Independent displayed mathematics, checkbox fidelity and native Boolean QA."""
import importlib.util, itertools, json, random, re, subprocess, hashlib
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('identity_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x',real=True)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def expr(s):
 s=s.strip().rstrip('.').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*')
 while r'\frac' in s:
  updated=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
  assert updated!=s,('unparsed fraction',s);s=updated
 assert '\\' not in s,('unsupported mathematical command',s)
 return sp.expand(parse_expr(s,local_dict={'x':X},transformations=standard_transformations+(implicit_multiplication_application,)))
def residual(e):
 l,r=e.split('=');return sp.expand(expr(l)-expr(r))
def normalized(poly):
 if poly==0:return sp.Integer(0)
 p=sp.Poly(poly,X);return sp.expand(poly/p.LC())
def validate(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=record['question'];level=q[':question/difficulty'].split('/')[-1]
 equations=re.findall(r'^- \*\*(I|II|III)\.\*\* \$([^$]+)\$',q[':question/problem'],re.M)
 assert [label for label,_ in equations]==list(g.ROMAN)
 assert q[':question/problem'].startswith('Which of the following equations has infinitely many solutions?\n\nSelect all that apply.\n\n')
 equations=[equation for _,equation in equations]
 residuals=[residual(e) for e in equations];identities=[p==0 for p in residuals]
 fields=q[':question/answer-fields'];assert len(fields)==3
 assert [f[':answer-field/key'] for f in fields]==list(g.ROMAN)
 ids=[q[':question/id']]
 for f,truth in zip(fields,identities):
  assert f[':answer-field/type']==':answer-field.type/checkbox'
  bank=f[':answer-field/choices'];values=[a[':answer/value'] for a in bank]
  assert len(bank)==2 and set(values)=={'false','true'}
  assert all(a[':answer/type']==':answer.type/text' for a in bank)
  assert f[':answer-field/correct'][0]==':answer/id'
  assert next(a[':answer/value'] for a in bank if a[':answer/id']==f[':answer-field/correct'][1])==str(bool(truth)).lower()
  ids += [f[':answer-field/id']]+[a[':answer/id'] for a in bank]
 assert len(ids)==len(set(ids)), 'question, field and answer identities must be distinct'
 for identity in ids:g.uuid.UUID(identity)
 solution=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert len(blocks)==3
 for i,(equation,p,block) in enumerate(zip(equations,residuals,blocks)):
  rows=block.rstrip('.').split(r' \\ ')
  assert residual(rows[0].replace(' & ',''))==p
  for row in rows:
   assert normalized(residual(row.replace(' & ','')))==normalized(p),(equation,row)
  if p==0:assert 'This equation is true for all values of $x.$' in solution
  elif sp.degree(p,X)==1:
   # Validate the actual displayed unique-solution conclusion against prompt.
   conclusions=re.findall(r'has the unique solution \$x=([^$]+)\.\$',solution)
   answer=sp.solve(p,X)[0];assert any(sp.simplify(expr(a)-answer)==0 for a in conclusions)
  if level=='moderate':
   assert len(re.findall(r'\\left\(',equation))==1
   assert rows[1].count(r'\cdot')==2
   left,right=equation.split('=');assert sp.degree(expr(left),X)==1 and expr(left).coeff(X) not in (0,1,-1)
  if level=='hard':
   assert equation.count(r'\left(')==2 and rows[1].count(r'\cdot')==4
   assert rows[2].count('x')==4 # individually evaluated variable products/tails
   a,b,c,d=expr(equation.split('=')[0]).coeff(X),expr(equation.split('=')[0]).subs(X,0),expr(equation.split('=')[1]).coeff(X),expr(equation.split('=')[1]).subs(X,0)
   assert all(z and abs(z)<=15 for z in (a,b,c,d))
 for text in (q[':question/problem'],solution):
  assert text.count('$')%2==0 and text.count('$$')%2==0
  depth=0
  for c in text:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0
  assert depth==0
  assert '--' not in text and '+-' not in text
 return record

def selected(record):
 return tuple(f[':answer-field/key'] for f in record['question'][':question/answer-fields'] if next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='true')

def native(rec,label):
 return {'label':label,'record':rec,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each checkbox owned Boolean, including unchecked false'} for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]}

def question_index(value):
 found={}
 def visit(v):
  if isinstance(v,dict):
   if ':question/math-academy-id' in v and ':question/problem' in v:found[v[':question/math-academy-id']]=v
   for child in v.values():visit(child)
  elif isinstance(v,list):
   for child in v:visit(child)
 visit(value)
 return found

def comparison_prompt(value):
 # The earlier five checkbox migrations used single newlines between bullets.
 return re.sub(r'\n+', '\n', value)

def counterfactual_pairs(level):
 if level=='easy':return [([2,1,2,1],[2,1,2,2]),([3,2,3,2],[3,2,3,3]),([4,3,4,3],[4,3,4,4])]
 if level=='moderate':return [([2,1,2,2],[2,1,2,3]),([-3,2,-3,-6],[-3,2,-3,-5]),([4,-1,4,-4],[4,-1,4,-3])]
 rng=random.Random(8417);pairs=[]
 while len(pairs)<3:
  identity=g.sample_row('hard','identity',rng)
  for v in (-4,-3,-2,-1,1,2,3,4):
   changed=identity[:-1]+[v]
   try:reduced=g.guard(list(map(sp.Integer,changed)),'hard')
   except ValueError:continue
   if g.kind(reduced)=='empty' and identity not in [a for a,b in pairs]:
    pairs.append((identity,changed));break
 return pairs

def main():
 source=json.loads((HERE/'source.json').read_text())
 migration=ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056'
 snapshot=json.loads((migration/'snapshot.json').read_text());migrated=question_index(snapshot)
 plan={q['ma_id']:q for q in json.loads((migration/'plan.json').read_text())['questions']}
 questions=source['record'][':knowledge-point/questions'];replays=[];review=[];engine=[];cases=[]
 source_cases=dict(g.SOURCE_CASES)
 source_cases.update({'q-288426':([[4,2,4,2],[-2,-1,-2,-1],[3,5,3,9]],'observed_c'),'q-288431':([[3,4,3,4],[1,-5,1,-2],[2,3,1,3]],'observed_c')})
 originals={q[':question/math-academy-id']:q for q in questions}
 originals.update({mid:migrated[mid] for mid in plan})
 for mid,(parameters,profile) in source_cases.items():
  original=originals[mid]
  rec=validate(g.generate('easy',0,'direct',parameters={'equations':parameters},profile=profile));q=rec['question']
  assert q[':question/worked-solution']==original[':question/worked-solution'],mid
  old_field=original[':question/answer-fields'][0]
  expected=tuple(re.findall(r'\b(?:III|II|I)\b',old_field[':answer-field/correct'][':answer/value']))
  assert selected(rec)==expected,(mid,selected(rec),expected)
  current=migrated[mid]
  target_prompt=plan[mid]['problem_after'] if mid in plan else current[':question/problem']
  assert comparison_prompt(q[':question/problem'])==comparison_prompt(target_prompt),mid
  if mid not in plan:
   assert {f[':answer-field/key'] for f in current[':question/answer-fields']}==set(g.ROMAN)
   for f in current[':question/answer-fields']:
    assert f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'
    assert set(a[':answer/value'] for a in f[':answer-field/choices'])=={'false','true'}
    assert (f[':answer-field/correct'][':answer/value']=='true')==(f[':answer-field/key'] in selected(rec))
  else:assert list(selected(rec))==plan[mid]['correct']
  cases.append({'source_id':mid,'template':'direct','parameters':{'equations':parameters},'sampling_profile':profile})
  replays.append({'source_id':mid,'equations_preserved':True,'shared_solution_exact':True,'migrated_prompt_matches_ignoring_blank_line_spacing':True,'checkbox_keys':['I','II','III'],'selected':list(selected(rec)),'correct_designation_preserved':True})
  review.append({'label':'Original and checkbox replay '+mid,'original':original,'record':rec});engine.append(native(rec,mid))
 generated=0;fingerprints={l:set() for l in ('easy','moderate','hard')};profile_summary={}
 for level in ('easy','moderate','hard'):
  for profile in g.BANKS:
   seen_masks=set()
   for seed in range(120):
    rec=validate(g.generate(level,seed,profile=profile));generated+=1;fingerprints[level].add(rec['generation']['mathematical_fingerprint']);seen_masks.add(selected(rec))
    assert rec==g.generate(level,seed,profile=profile)
    other=g.generate(level,seed+1,parameters=rec['generation']['parameters'],profile=profile)
    assert rec['question']==other['question']
    assert rec['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
    if seed<4:engine.append(native(rec,f'{level}/{profile}/{seed}'))
    if seed<2:review.append({'label':f'Generated {level} {profile} seed {seed}','record':rec})
   expected_masks={tuple(re.findall(r'\b(?:III|II|I)\b',value)) for value in g.BANKS[profile]}
   assert seen_masks==expected_masks
   profile_summary[level+'/'+profile]={'instances':120,'eligible_correct_subsets':[list(mask) for mask in sorted(seen_masks)]}
 # Every subset is expressible under every explicit profile. Each counterfactual
 # changes only one equation's constant, preserving the remaining arithmetic.
 mask_summary={};counterfactuals=[]
 for level in ('easy','moderate','hard'):
  pairs=counterfactual_pairs(level);records={}
  for mask in itertools.product((False,True),repeat=3):
   params={'equations':[pair[0] if truth else pair[1] for pair,truth in zip(pairs,mask)]}
   variants=[validate(g.generate(level,88,parameters=params,profile=profile)) for profile in g.BANKS]
   rec=variants[0];records[mask]=rec
   assert selected(rec)==tuple(label for label,truth in zip(g.ROMAN,mask) if truth)
   assert all(v['question']==rec['question'] for v in variants), 'historical sampling profile must not change checkbox content'
   engine.append(native(rec,level+'/explicit/'+''.join(str(int(t)) for t in mask)))
   if mask in ((False,False,False),(True,True,True)):review.append({'label':f'{level}: explicit '+('all selected' if all(mask) else 'none selected'),'record':rec})
  for mask,rec in records.items():
   for i in range(3):
    alternate=tuple(not v if j==i else v for j,v in enumerate(mask));changed=records[alternate]
    assert sum(a!=b for a,b in zip(rec['generation']['parameters']['equations'],changed['generation']['parameters']['equations']))==1
    assert set(selected(rec))^set(selected(changed))=={g.ROMAN[i]}
  mask_summary[level]={'explicit_masks':8,'profiles_per_mask':4,'single_constant_counterfactuals':24}
  counterfactuals.extend({'difficulty':level,'mask':list(mask),'record':rec} for mask,rec in records.items())
 invalid=[('easy',{'equations':[[3,0,1,1],[2,1,2,1],[2,1,2,3]]}),('moderate',{'equations':[[1,2,1,2],[2,2,3,3],[2,2,2,3]]}),('hard',{'equations':[[4,4,4,4,4,4,4,4,4,4]]*3})]
 for level,p in invalid:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid explicit parameter accepted')
 for level in ('easy','moderate','hard'):
  for field_type in ('radio',':answer-field.type/radio','blank'):
   try:g.generate(level,field_type=field_type)
   except ValueError:pass
   else:raise AssertionError('non-checkbox field type accepted')
  for field_type in ('checkbox',':answer-field.type/checkbox'):validate(g.generate(level,field_type=field_type))
 save('source-cases.json',cases);save('source-replay.json',replays);save('engine-input.json',engine)
 binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'native-grading.json')],check=True)
 save('review.json',review);save('checkbox-cases.json',counterfactuals)
 sections=[]
 for item in review:
  text=item['label']+'\n\n'
  if 'original' in item:text+='Original\n\n'+item['original'][':question/problem']+'\n\n'+item['original'][':question/worked-solution']+'\n\nCheckbox replay\n\n'
  text+=g.markdown(item['record']);sections.append(text)
 (HERE/'review.md').write_text('\n\n---\n\n'.join(sections)+'\n')
 result={'passed':True,'generator_version':g.VERSION,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'historical_source_basis':source['basis'],'migration_source_basis':snapshot['basis'],'source_questions':7,'source_equations_preserved':7,'source_solutions_exact':7,'migrated_prompts_matched_ignoring_blank_line_spacing':7,'source_correct_designations_preserved':7,'field_type':'checkbox','fields_per_question':3,'boolean_answers_per_field':2,'source_errors':[],'authored_levels':['moderate','hard'],'observed_levels':['easy'],'profiles':profile_summary,'explicit_subset_coverage':mask_summary,'generated_displayed_instances_validated':generated,'unique_sampled_mathematical_tasks':{l:len(v) for l,v in fingerprints.items()},'native_grading':json.loads((HERE/'native-grading.json').read_text()),'checks':['independent printed equation classification','each printed worked-solution equation stage','nonunit and reduced workload bounds','retained historical-profile sampled subsets','all eight explicit subsets under each profile and difficulty','single-constant changes flip exactly one checkbox','field-owned true and false answers through native grade_field','stable seed-independent identities','profile-independent checkbox content identities','explicit guard and field-type failures'],'unresolved':[]}
 save('validation.json',result)
 print(f'PASS: 7 source replays; {generated} sampled instances; all 8 subsets at each difficulty; native Boolean grading verified.')
if __name__=='__main__':main()

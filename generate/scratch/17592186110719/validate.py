"""Independent displayed equation/stage, exact fidelity, scope and native radio QA."""
import importlib.util, json, re, subprocess, hashlib
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
 equations=re.findall(r'^- \$([^$]+)\$',q[':question/problem'],re.M);assert len(equations)==3
 residuals=[residual(e) for e in equations];identities=[p==0 for p in residuals]
 label=g.subset(['identity' if z else 'empty' for z in identities])
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 bank=f[':answer-field/choices'];values=[a[':answer/value'] for a in bank]
 assert len(bank)==5 and len(set(values))==5 and set(values)==set(g.BANKS[record['generation']['profile']])
 assert len({tuple(g.truths(v)) for v in values})==5
 assert sum(g.truths(v)==tuple(r for r,t in zip(g.ROMAN,identities) if t) for v in values)==1
 assert next(a[':answer/value'] for a in bank if a[':answer/id']==f[':answer-field/correct'][1])==label
 for obj,key in [(q,':question/id'),(f,':answer-field/id')]+[(a,':answer/id') for a in bank]:g.uuid.UUID(obj[key])
 assert all(a[':answer/type']==':answer.type/text' for a in bank)
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

def native(rec,label):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete displayed radio bank'} for a in f[':answer-field/choices']]}

def main():
 source=json.loads((ROOT/'generate/runs/current/sources/17592186110719.json').read_text());save('source.json',source)
 questions=source['record'][':knowledge-point/questions'];replays=[];review=[];engine=[];cases=[]
 for original in questions:
  mid=original[':question/math-academy-id'];parameters,profile=g.SOURCE_CASES[mid]
  rec=validate(g.generate('easy',0,'direct',parameters={'equations':parameters},profile=profile));q=rec['question'];f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
  assert q[':question/problem']==original[':question/problem'],mid
  assert q[':question/worked-solution']==original[':question/worked-solution'],mid
  assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'] and f[':answer-field/key']==of[':answer-field/key']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  case={'source_id':mid,'template':'direct','parameters':{'equations':parameters},'bank_profile':profile};cases.append(case)
  replays.append({'source_id':mid,'prompt_exact':True,'shared_solution_exact':True,'field_layout_exact':True,'choices_matched':5,'distractors_matched':4,'correct_designation_matched':True})
  review.append({'label':'Original and replay '+mid,'original':original,'record':rec});engine.append(native(rec,mid))
 generated=0;fingerprints={l:set() for l in ('easy','moderate','hard')};profile_summary={};positions=set()
 for level in ('easy','moderate','hard'):
  for profile in g.BANKS:
   seen_masks=set()
   for seed in range(120):
    rec=validate(g.generate(level,seed,profile=profile));generated+=1;fingerprints[level].add(rec['generation']['mathematical_fingerprint'])
    f=rec['question'][':question/answer-fields'][0];correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);seen_masks.add(correct)
    positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    assert rec==g.generate(level,seed,profile=profile)
    other=g.generate(level,seed+1,parameters=rec['generation']['parameters'],profile=profile)
    assert rec['question'][':question/id']==other['question'][':question/id']
    assert rec['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
    assert sorted(f[':answer-field/choices'],key=lambda a:a[':answer/id'])==sorted(other['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])
    if seed<4:engine.append(native(rec,f'{level}/{profile}/{seed}'))
    if seed<2:review.append({'label':f'Generated {level} {profile} seed {seed} (authored template)' if level!='easy' else f'Generated easy {profile} seed {seed}','record':rec})
   assert seen_masks==set(g.BANKS[profile]);profile_summary[level+'/'+profile]={'instances':120,'eligible_correct_subsets':sorted(seen_masks)}
 assert positions==set(range(5))
 # Explicit calls obey every level guard and complete-bank eligibility.
 invalid=[('easy',{'equations':[[3,0,1,1],[2,1,2,1],[2,1,2,3]]},'observed_a'),('moderate',{'equations':[[1,2,1,2],[2,2,3,3],[2,2,2,3]]},'observed_c'),('hard',{'equations':[[4,4,4,4,4,4,4,4,4,4]]*3},'observed_a')]
 for level,p,profile in invalid:
  try:g.generate(level,parameters=p,profile=profile)
  except ValueError:pass
  else:raise AssertionError('invalid explicit parameter accepted')
 # Changing a complete bank changes content identity, not mathematical identity.
 p={'equations':g.SOURCE_CASES['q-287966'][0]};a=g.generate('easy',parameters=p,profile='observed_a');b=g.generate('easy',parameters=p,profile='observed_b')
 assert a['question'][':question/id']!=b['question'][':question/id'] and a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 save('source-cases.json',cases);save('source-replay.json',replays);save('engine-input.json',engine)
 binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'native-grading.json')],check=True)
 save('review.json',review)
 sections=[]
 for item in review:
  text=item['label']+'\n\n'
  if 'original' in item:text+='Original\n\n'+item['original'][':question/problem']+'\n\n'+item['original'][':question/worked-solution']+'\n\nReplay\n\n'
  text+=g.markdown(item['record']);sections.append(text)
 (HERE/'review.md').write_text('\n\n---\n\n'.join(sections)+'\n')
 result={'passed':True,'source_basis':1356,'source_questions':5,'source_prompts_exact':5,'source_solutions_exact':5,'complete_original_banks_matched':5,'source_choices_matched':25,'source_distractors_matched':20,'source_correct_designations_matched':5,'source_errors':[],'presentation_repairs':0,'mathematical_repairs':0,'authored_levels':['moderate','hard'],'observed_levels':['easy'],'profiles':profile_summary,'generated_displayed_instances_validated':generated,'unique_sampled_mathematical_tasks':{l:len(v) for l,v in fingerprints.items()},'native_grading':json.loads((HERE/'native-grading.json').read_text()),'checks':['printed equation classification','every complete displayed categorical bank','every printed worked-solution equation stage','nonunit and reduced workload bounds','every bank correct-subset eligibility','correct choice shuffled across all five positions','stable seed-independent identities','explicit guard failures'],'unresolved':[]}
 save('validation.json',result)
 print(f'PASS: 5 exact sources, 25 choices, 20 distractors; {generated} displayed instances; native grading verified.')
if __name__=='__main__':main()

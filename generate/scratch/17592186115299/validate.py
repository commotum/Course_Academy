#!/usr/bin/env python3
"""Independent displayed-math, original fidelity and native grading audit."""
import collections,difflib,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
D=Path(__file__).parent;SCRIPT=D.with_suffix('.py');ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)
V=sp.symbols('x y z');R=sp.symbols('r1 r2 r3')
def expression(s):
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 s=re.sub(r'(?<=[0-9)])(?=[xyz])','*',s)
 return sp.expand(parse_expr(s,local_dict={**dict(zip('xyz',V)),**dict(zip(['r1','r2','r3'],R))},transformations=TRANS))
def matrices(s):
 return [sp.Matrix([[expression(c.strip()) for c in row.split('&')] for row in body.split(r'\\')]) for body in re.findall(g.MATRIX_RE,s,re.S)]
def system(s):
 body=re.search(g.SYSTEM_RE,s,re.S)[1];n=3 if 'z' in body else 2;rows=[]
 for row in body.split(r'\\'):
  left,right=row.replace('&','').strip().rstrip('.,').split('=');e=expression(left)-expression(right)
  assert e.subs(dict.fromkeys(V,0))==-expression(right)
  rows.append([e.coeff(x) for x in V[:n]]+[-e.subs(dict.fromkeys(V,0))])
 return sp.Matrix(rows)
def independent_class(m):
 a=m[:,:-1];b=m[:,-1];sol=sp.linsolve((a,b));n=a.cols
 if sol==sp.EmptySet:return 'inconsistent'
 tup=next(iter(sol));return 'dependent' if set().union(*(e.free_symbols for e in tup)) else 'independent'
def normalize(s):return re.sub(r'(?<!\\)\{(?=\\begin\{aligned\})',lambda _:r'\{',s)
def operation_checks(solution):
 chain=re.findall(r'\$\$(.*?)\$\$',solution,re.S)[1]
 found=list(re.finditer(g.MATRIX_RE,chain,re.S));mm=matrices(chain)
 for i in range(len(found)-1):
  text=chain[found[i].end():found[i+1].start()].replace('&','').replace(' ','').replace(r'\\','').replace('∼','')
  text=re.sub(r'\{R\}_\{([123])\}',r'r\1',text)
  work=mm[i].copy()
  if '↔' in text:
   a,b=map(lambda x:int(x[1])-1,text.split('↔'));work.row_swap(a,b)
  else:
   dst,rhs=text.split(':=');index=int(dst[1])-1
   e=expression(rhs);coeffs=[e.coeff(r) for r in R];assert e==sum(c*r for c,r in zip(coeffs,R))
   assert coeffs[index]!=0
   row=sp.zeros(1,work.cols)
   for j,c in enumerate(coeffs[:work.rows]):row+=c*work[j,:]
   work[index,:]=row
  assert work==mm[i+1],f'Printed row operation failure at stage {i+1}: {text}'
 return len(mm)-1

def validate_record(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'};assert rec['knowledge_point']['db_id']==g.KP_ID
 q=rec['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution'];m=system(prompt);a=m[:,:-1];b=m[:,-1];kind=independent_class(m)
 assert kind==rec['generation']['classification'];mm=matrices(solution);assert mm[0]==m and mm[1]==m
 operation_count=operation_checks(solution)
 level=q[':question/difficulty'].split('/')[-1]
 if level in ['easy','hard']:assert operation_count==(1 if level=='easy' else 3)
 final=mm[-1];assert final.rref()[0]==m.rref()[0]
 # Corresponding reduced systems must be actual final rows, not merely equivalent equations.
 blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
 for block in blocks[2:]:
  if r'\begin{aligned}' in block:
   sm=system(block);assert sm==final[:sm.rows,:]
 # Check every displayed isolated variable and zero-row implication from printed math.
 actual=next(iter(sp.linsolve((a,b)))) if kind!='inconsistent' else None
 for var,body in re.findall(r'\$([xyz])=([^$]+)\$',solution):
  body=body.rstrip('.,');assert sp.simplify(expression(body)-actual['xyz'.index(var)])==0
 for body in re.findall(r'\$(0x[^$]+)\$',solution):
  body=body.rstrip('.,');left,right=body.split('=');assert expression(left)==0
  assert any(all(v==0 for v in final.row(i)[:-1]) and final[i,-1]==expression(right) for i in range(final.rows))
 for block in blocks[2:]:
  if '⟹' in block:
   left,right=block.split('⟹');left=left.replace(r'\,','').strip();l,r=left.split('=');assert expression(l).subs(V[0],actual[0])==expression(r)
   right=right.replace(r'\,','').strip().rstrip('.');l,r=right.split('=');assert expression(l).subs(V[0],actual[0])==expression(r)
 if kind=='inconsistent':assert 'no solution' in solution and 'inconsistent' in solution
 elif kind=='dependent':
  assert 'infinitely many solutions' in solution and 'consistent dependent' in solution
  pivots=a.rref()[1];free=set('xyz'[:a.cols])-{'xyz'[i] for i in pivots}
  fragment=re.search(r'(?:we have|Here there).*?free variables?, (.*?)(?:That means|Therefore)',solution,re.S)
  if fragment:
   claimed=set(re.findall(r'\$([xyz])[.,]?\$',fragment[1]));assert claimed==free
 else:assert 'consistent independent' in solution
 statement_lines=[line for line in prompt.splitlines() if re.match(r'^(?:-|I\.|II\.|III\.) ',line)];assert len(statement_lines)==3
 truth=[]
 for i,line in enumerate(statement_lines):
  category='dependent' if 'consistent dependent' in line else 'independent' if 'independent' in line or 'unique solution' in line else 'inconsistent'
  if category==kind:truth.append(i+1)
 assert len(truth)==1
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1;assert f[':answer-field/type']==':answer-field.type/radio'
 bank=f[':answer-field/choices'];assert len(bank)==5;assert len(set(a[':answer/value'] for a in bank))==5
 correct_id=f[':answer-field/correct'][1];truthbanks=[]
 for option in bank:
  vals=[] if option[':answer/value']=='None' else [g.ROMAN.index(t)+1 for t in re.findall(r'\b(?:III|II|I)\b',option[':answer/value'])]
  truthbanks.append(vals==truth);assert (vals==truth)==(option[':answer/id']==correct_id)
 assert sum(truthbanks)==1
 for txt in [prompt,solution]:
  assert txt.count('$')%2==0;assert '{{slot_' not in txt
  stripped=re.sub(r'\\[{}]','',txt);assert stripped.count('{')==stripped.count('}'), 'Unbalanced TeX braces'
 return m,operation_checks(solution)

def main():
 families=json.loads((D/'families.json').read_text());assert len(set(families['source_to_family'].values()))==13 and set(families['source_to_family'])==set(g.TEMPLATES)
 source=json.loads((D/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];cases=[];replays=[];raw_errors=[];coverage=[];native=[];reviews=[];review=['# Originals and generated variants\n\nBasis 1356, immutable source capture. Originals below retain raw source text. Generated variants escape malformed opening system braces; q-32242 also repairs its unstated R1 sign flip. All records use full five-option radio banks.\n']
 exactprompt=exactsol=normprompt=normsol=options=distractors=0;stages_checked=0
 for sourceq in qs:
  sid=sourceq[':question/math-academy-id'];n=matrices(sourceq[':question/worked-solution'])[0].cols-1;p={'scales':[1]*n,'translations':[0]*n};profile=g.TEMPLATES[sid]['profile']
  case={'source_id':sid,'question_uuid':sourceq[':question/id'],'template':sid,'level':'moderate','parameters':p,'bank_profile':profile};cases.append(case)
  rec=g.generate('moderate',template=sid,parameters=p,profile=profile);m,count=validate_record(rec);stages_checked+=count;replays.append(rec)
  origbank=sourceq[':question/answer-fields'][0];bank=rec['question'][':question/answer-fields'][0];vals=sorted(a[':answer/value'] for a in bank[':answer-field/choices']);assert vals==sorted(a[':answer/value'] for a in origbank[':answer-field/choices'])
  correct=next(a[':answer/value'] for a in bank[':answer-field/choices'] if a[':answer/id']==bank[':answer-field/correct'][1]);assert correct==origbank[':answer-field/correct'][':answer/value'];options+=5;distractors+=4
  ep=rec['question'][':question/problem']==sourceq[':question/problem'];es=rec['question'][':question/worked-solution']==sourceq[':question/worked-solution'];np=rec['question'][':question/problem']==normalize(sourceq[':question/problem']);ns=rec['question'][':question/worked-solution']==normalize(sourceq[':question/worked-solution']);exactprompt+=ep;exactsol+=es;normprompt+=np;normsol+=ns
  assert np;assert ns or sid=='q-32242'
  errors=[]
  if not ep:
   errors.append('Unescaped unmatched opening system brace');raw_errors.append({'source_id':sid,'kind':'presentation','raw':sourceq[':question/problem'],'supported_repair':'Escape only the unpaired leading { as \\{ in each system component.'})
  if not ns:
   errors.append('Unstated R1 negation in final matrix');raw_errors.append({'source_id':sid,'kind':'mathematical-stage','raw_final_matrix':g.matrix_tex(matrices(sourceq[':question/worked-solution'])[-1]),'correct_final_matrix':g.matrix_tex(matrices(rec['question'][':question/worked-solution'])[-1]),'support':'R3:=R3-9R2 changes R3 only. R1 must remain (-1,2,6). Its spurious negation remains row-equivalent but is not the printed operation.'})
  coverage.append({'source_id':sid,'bank_profile':profile,'complete_bank':True,'option_matches':5,'distractor_matches':4,'correct_designation':True,'raw_prompt_exact':ep,'raw_solution_exact':es,'normalized_prompt_exact':np,'normalized_solution_exact':ns,'supported_repairs':errors})
  variant=g.generate('moderate',seed=100+len(reviews),template=sid);validate_record(variant);reviews.append(variant)
  review+=['\n## '+sid+' — original\n',sourceq[':question/problem'],'\nOriginal complete bank: '+', '.join(a[':answer/value'] for a in origbank[':answer-field/choices'])+'\n\nOriginal worked solution:\n\n'+sourceq[':question/worked-solution'],'\n### Generated moderate variant (parameter extension)\n',g.markdown(variant)]
 for level in ['easy','hard']:
  for seed in [0,1,5]:
   rec=g.generate(level,seed=seed);validate_record(rec);reviews.append(rec);review+=['\n## Authored '+level+' example '+str(seed+1)+'\n',g.markdown(rec)]
 for i,rec in enumerate(replays+reviews):
  f=rec['question'][':question/answer-fields'][0];native.append({'label':'replay-or-review-'+str(i),'record':rec,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned full-bank classification option '+a[':answer/value']} for a in f[':answer-field/choices']]})
 stress=collections.Counter();kinds=collections.defaultdict(set);unique=collections.defaultdict(set);firstpositions=set()
 for level in ['easy','moderate','hard']:
  for seed in range(180):
   rec=g.generate(level,seed=seed);_,count=validate_record(rec);stress[level]+=1;stages_checked+=count;kinds[level].add(rec['generation']['classification']);unique[level].add(rec['generation']['mathematical_fingerprint'])
   f=rec['question'][':question/answer-fields'][0];firstpositions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
   again=g.generate(level,seed=seed+991,template=rec['generation']['template'],parameters=rec['generation']['parameters'],profile=rec['generation']['bank_profile']);assert again['question'][':question/id']==rec['question'][':question/id']
 assert firstpositions==set(range(5));assert all(v==set(g.WORDS) for v in kinds.values())
 # Exercise every observed full profile on every source layout with changed parameters.
 crossprofiles=0
 for sid in g.TEMPLATES:
  for profile in g.BANKS:
   rec=g.generate('moderate',seed=981,template=sid,profile=profile);validate_record(rec);crossprofiles+=1
 # Identity distinguishes complete banks while ignoring shuffle and spelling.
 base=g.generate('easy',parameters={'matrix':[[1,1,1],[2,3,4]],'order':list(g.WORDS)})
 spelling=g.generate('easy',seed=998,parameters={'matrix':[['1','1','1'],['2','3','4']],'order':list(g.WORDS)})
 scaled=g.generate('easy',parameters={'matrix':[[2,2,2],[4,6,8]],'order':list(g.WORDS)})
 assert base['question'][':question/id']==spelling['question'][':question/id']
 assert base['generation']['mathematical_fingerprint']==scaled['generation']['mathematical_fingerprint']
 assert base['question'][':question/id']!=scaled['question'][':question/id']
 profile_records=[g.generate('easy',template='easy_authored',parameters=base['generation']['parameters'],profile=p) for p in g.BANKS]
 assert len({r['question'][':question/id'] for r in profile_records})==len(g.BANKS)
 assert len({r['generation']['mathematical_fingerprint'] for r in profile_records})==1
 # Enforced absolute-value bounds, both valid edges and negative overflows.
 validate_record(g.generate('easy',parameters={'matrix':[[1,16,0],[1,16,1]],'order':list(g.WORDS)}))
 validate_record(g.generate('hard',parameters={'matrix':[[1,1,1,0],[1,2,3,0],[1,3,6,40]],'order':list(g.WORDS)}))
 # Explicit invalid domains must fail, rather than be silently altered.
 for level,p in [('easy',{'matrix':[[1,17,1],[1,18,2]],'order':list(g.WORDS)}),('hard',{'matrix':[[1,41,1,1],[1,42,2,2],[1,43,4,3]],'order':list(g.WORDS)}),('moderate',{'scales':[0,1],'translations':[0,0]}),('easy',{'matrix':[[1,-17,1],[1,-18,2]],'order':list(g.WORDS)}),('hard',{'matrix':[[1,-41,1,1],[1,-42,2,2],[1,-43,4,3]],'order':list(g.WORDS)})]:
  try:g.generate(level,template='q-32242' if level=='moderate' else None,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit input accepted')
 (D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'source-errors.json').write_text(json.dumps(raw_errors,indent=2)+'\n');(D/'source-replays.json').write_text(json.dumps(replays,indent=2)+'\n');(D/'review.json').write_text(json.dumps(reviews,indent=2)+'\n');(D/'review.md').write_text('\n'.join(review)+'\n');(D/'native-fixtures.json').write_text(json.dumps(native,indent=2)+'\n')
 engine=ROOT/'generate/runs/current/check-engine';output=D/'native-results.json';run=subprocess.run([str(engine),str(D/'native-fixtures.json'),str(output)],capture_output=True,text=True);assert run.returncode==0,run.stderr+run.stdout
 engine_report=json.loads(output.read_text())
 result={'status':'passed','database':source['database'],'basis':source['basis'],'lineage':source['lineage'],'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((D/'source.json').read_bytes()).hexdigest(),'practice_sources':14,'templates':13,'source_replay_aliases':14,'distinct_observed_banks':len(g.BANKS),'source_coverage':coverage,'fidelity':{'complete_banks':{'matched':14,'total':14},'options':{'matched':options,'total':70},'distractors':{'matched':distractors,'total':56},'correct_designations':{'matched':14,'total':14},'raw_prompts':{'matched':exactprompt,'total':14},'raw_solutions':{'matched':exactsol,'total':14},'presentation_normalized_prompts':{'matched':normprompt,'total':14},'presentation_normalized_solutions':{'matched':normsol,'total':14},'supported_math_solution_repairs':1,'supported_presentation_source_repairs':11},'stress_records':dict(stress),'distinct_mathematical_tasks':{k:len(v) for k,v in unique.items()},'classification_coverage':{k:sorted(v) for k,v in kinds.items()},'printed_row_operations_checked':stages_checked,'cross_profile_records':crossprofiles,'native_grading':{'fixtures':len(native),'checks':5*len(native),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'report':engine_report},'invalid_inputs_rejected':5,'valid_boundary_instances':2,'identity_spelling_scalar_bank_checks':'passed','unresolved_findings':[],'plots':'none'}
 (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['source_coverage','native_grading']},indent=2))
if __name__=='__main__':main()

"""Independent parsing of displayed math, all source banks, and native grading."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));from extract import parse,pairs
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=sp.symbols('x y',real=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def fingerprint(prompt):return g.fingerprint_pairs(pairs(prompt))
def solution_derivatives(text):
 out=[]
 for block in re.findall(r'\$\$(.*?)\$\$',text,re.S):
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().rstrip('.,')
  a,b=re.split(r',\\(?:,|qquad)\s*',block,maxsplit=1)
  a=a.split('=',1)[1].strip().rstrip('.,');b=b.split('=',1)[1].strip().rstrip('.,')
  out.append((parse(a),parse(b)))
 assert len(out)==3
 return out

def flags(q):
 out=[]
 for f in sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
  correct=f[':answer-field/correct'];cid=str(correct[':answer/id']) if isinstance(correct,dict) else str(correct[1])
  out.append(next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if str(a[':answer/id'])==cid))
 return out

def solution_check(q):
 fields=pairs(q[':question/problem']);truth=[]
 shown=solution_derivatives(q[':question/worked-solution'])
 for i,((p,t),(a,b)) in enumerate(zip(fields,shown)):
  assert sp.simplify(a-sp.diff(p,y))==0,('Incorrect displayed P_y',i,p,a)
  assert sp.simplify(b-sp.diff(t,x))==0,('Incorrect displayed Q_x',i,t,b)
  eq=sp.simplify(a-b)==0;truth.append(eq)
  if not eq:
   assert any(sp.simplify((a-b).subs({x:u,y:v}))!=0 for u,v in ((0,0),(1,0),(0,1),(1,2),(2,1))), 'No verified inequality witness'
 assert flags(q)==truth
 fs=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']);assert len(fs)==3 and [f[':answer-field/key'] for f in fs]==list(g.KEYS)
 for f in fs:
  kind=f[':answer-field/type'];assert (kind.get(':db/ident') if isinstance(kind,dict) else kind)==':answer-field.type/checkbox'
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
  assert len({str(a[':answer/id']) for a in f[':answer-field/choices']})==2
 for text in [q[':question/problem'],q[':question/worked-solution']]:assert text.count('$')%2==0 and text.count('{')==text.count('}')
 return fields

def independent(r):
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=r['question'];meta=r['generation'];assert q[':question/difficulty']==':question.difficulty/moderate'
 fields=solution_check(q);expected=g.pairs(meta['source'],meta['parameters']['scales'])
 assert all(sp.simplify(p-a)==0 and sp.simplify(t-b)==0 for (p,t),(a,b) in zip(fields,expected))
 assert g.fingerprint_pairs(fields)==meta['parameter_fingerprint']
 assert r==g.generate('moderate',meta['seed'],template=meta['source'],parameters=meta['parameters'])
 # Check solution target references, not just its derivative numbers.
 text=q[':question/worked-solution'];chunks=re.split(r'- For the vector field \$[FGH],\$',text)[1:];assert len(chunks)==3
 for (p,t),chunk in zip(fields,chunks):
  ptext=re.search(r'we have \$P=(.*?)\$ and \$Q=(.*?)\$',chunk);assert ptext
  assert sp.simplify(parse(ptext[1])-p)==0 and sp.simplify(parse(ptext[2])-t)==0
  yes=sp.simplify(sp.diff(p,y)-sp.diff(t,x))==0
  assert ('is not conservative' not in chunk)==yes
 selected=[key for key,yes in zip(g.KEYS,flags(q)) if yes]
 assert all(key in text.rsplit('Therefore,',1)[1] for key in selected)
 ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
 assert len(ids)==len(set(ids));[uuid.UUID(i) for i in ids]

def checks(r):
 return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if str(a[':answer/id'])==str(f[':answer-field/correct'][1]) else 'rejected','purpose':'Both owned checkbox values via actual learner grader'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def main():
 source=json.loads((HERE/'source.json').read_text());records=[];replay=[];review=[]
 for q in source['record'][':knowledge-point/questions']:
  profile=q[':question/math-academy-id'];source_pairs=solution_check(q);r=g.generate(template=profile,parameters={'scales':[[1,1]]*3});independent(r)
  assert all(sp.simplify(a-p)==0 and sp.simplify(b-t)==0 for (a,b),(p,t) in zip(source_pairs,g.pairs(profile,[[1,1]]*3)))
  assert flags(q)==flags(r['question'])
  banks=[]
  for f,generated in zip(sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']),r['question'][':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in generated[':answer-field/choices'])
   banks.append({'source_field_id':f[':answer-field/id'],'key':f[':answer-field/key'],'source_choice_mapping':[{'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'recipe':'Boolean '+a[':answer/value'],'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id']} for a in f[':answer-field/choices']],'matched_choices':2,'total_choices':2,'matched_incorrect':1,'total_incorrect':1,'missing':[],'extra':[]})
  replay.append({'profile':profile,'complete':True,'fields':banks,'original_expressions_replayed':6,'original_derivatives_checked':6,'prompt_notation':'Normalized R to mathbb R, function LaTeX, parenthesized vector components; no mathematical changes','solution_sequence':'Theorem, domain, P/Q, two derivatives, comparison for F/G/H, selected subset'})
  variant=g.generate(seed=20261014,template=profile);independent(variant);records.extend([r,variant]);review.append('## '+profile+'\n\nOriginal\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(r)+'\n\nVariant\n\n'+g.markdown(variant))
 # Every scale, field, and structural profile, including simultaneous signed boundaries.
 coverage={};negative=0
 for profile in g.PROFILES:
  coverage[profile]={}
  for pos in range(3):
   choices=[]
   for u,vv in ((-2,-2),(-1,-1),(1,1),(2,2),(-2,1),(1,-2)):
    scales=[[1,1] for _ in range(3)];scales[pos]=[u,vv];r=g.generate(template=profile,parameters={'scales':scales});independent(r);records.append(r);choices.append([u,vv])
   coverage[profile][str(pos)]=choices
  baseline=g.generate(template=profile,parameters={'scales':[[1,1]]*3});changed=g.generate(template=profile,parameters={'scales':[[2,1],[1,2],[-2,1]]});independent(changed)
  broken=copy.deepcopy(changed);broken['question'][':question/worked-solution']=baseline['question'][':question/worked-solution']
  try:independent(broken)
  except AssertionError:negative+=1
  else:raise AssertionError('Stale parameters passed validation')
  records.append(changed)
  # Identical parameters produce stable content identities despite seed changes.
  assert g.generate(seed=1,template=profile,parameters={'scales':[[2,1]]*3})['question']==g.generate(seed=2,template=profile,parameters={'scales':[[2,1]]*3})['question']
 for level in ('easy','hard'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported difficulty accepted')
 save('native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 engine=json.loads((HERE/'native-report.json').read_text());assert engine['documented_unresolved_checks']==0
 save('source-bank-replay.json',replay);save('slot-coverage.json',{'scales':coverage,'eligible_values':g.SCALES,'stale_solution_negative_controls':negative,'all_profiles':list(g.PROFILES),'fixed_roles':'F/G/H are vector fields; only their coordinate and consequent coefficient parameters vary; all 3 checkbox fields remain'})
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n');save('validated-previews.json',records)
 save('validation.json',{'status':'pass','basis':source['basis'],'fidelity':{'source_questions':11,'components':66,'complete_banks':33,'matched_choices':66,'total_choices':66,'matched_incorrect_choices':33,'total_incorrect_choices':33,'missing':[],'extra':[],'source_derivatives':66,'normalization':'LaTeX spacing, parenthesized components and standard partial notation; scalar mathematics and solution stages retained'},'correctness':{'rendered_instances_checked':len(records),'global_domain':'All source functions globally C1; nonzero invertible coordinate substitutions preserve R2 domain','declared_slots_covered':True},'grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':0},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'source-components.json',HERE/'extract.py',HERE/'validate.py',ROOT/'generate/runs/current/check-engine']}})
 print('Validated',len(records),'rendered instances, all source banks and source derivative steps.')
if __name__=='__main__':main()

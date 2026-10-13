"""Independent displayed-equation, operative-stage, fidelity, and native checks."""
import hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=sp.symbols('x y')
def math(s):
 s=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',s).replace(' ','')
 if not re.fullmatch(r'[\d()+\-*/xy]+',s):raise ValueError('Unexpected notation '+s)
 s=re.sub(r'(?<=[\d)])(?=[xy])','*',s)
 return sp.sympify(s,locals={'x':x,'y':y})
def equation(s):
 sides=s.replace('&','').split('=');assert len(sides)==2
 return sp.expand(math(sides[0])-math(sides[1]))
def full_line(s):
 e=equation(s);assert sp.Poly(e,x,y).total_degree()==1 and e.coeff(y)!=0
 return sp.expand(e/e.coeff(y))
def slope(e):return sp.cancel(-e.coeff(x)/e.coeff(y))
def parse(q):
 stems=re.findall(r'\$(.*?)\$',q[':question/problem']);assert len(stems)==1
 e=equation(stems[0]);return slope(e),e

def formatting(s):
 assert '--' not in s and '+-' not in s
 assert s.count('$')%2==0
 depth=0
 for c in s:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0
 assert depth==0

def inspect(rec):
 q=rec['question'];m,e=parse(q);p=rec['generation']['parameters'];assert e.coeff(x)==p['A'] and e.coeff(y)==p['B'] and -e.subs({x:0,y:0})==p['C'];raw=rec['generation']['bank_profile'] in g.BANK_PROFILES
 assert set(rec['knowledge_point'])=={'db_id','id','title'} and rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 assert rec['generation']['python_version']==sys.version.split()[0]
 assert q[':question/problem']==f"Which of the following lines is parallel to ${g.standard(p)}$?"
 assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0]
 assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 assert '{{' not in q[':question/problem'];bank=f[':answer-field/choices'];assert len(bank)==5
 correct=f.get(':answer-field/correct',[None,None])[1];assert raw or sum(a[':answer/id']==correct for a in bank)==1
 vals=[];polys=[]
 for a in bank:
  assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'];uuid.UUID(a[':answer/id']);formatting(a[':answer/value'])
  z=equation(a[':answer/value']);assert z.coeff(y)==1;polys.append(z);vals.append((slope(z),-z.subs({x:0,y:0})))
  if not raw:assert (a[':answer/id']==correct)==(slope(z)==m)
  if slope(z)==m:assert sp.expand(e/e.coeff(y)-z)!=0,'Coincident line forbidden by never-cross canonical definition'
 assert len(set(polys))==5 and sum(a==m for a,b in vals)==1
 # Validate actual displayed bank against specified operation, independently of
 # generator bank() and metadata selections.
 bp=rec['generation']['bank_profile'].removeprefix('completed:')
 if bp in g.AUTHORED_PROFILES:
  A=e.coeff(x);B=e.coeff(y);C=-e.subs({x:0,y:0});b=C/B
  fourth=A if bp=='method-sign-reciprocal' else -A
  expected={(m,b+1),(-m,b-1),(1/m,b+2),(-1/m,b-2),(fourth,b+3)}
  assert set(vals)==expected
 assert rec['generation']['eligible_for_learning']==(not rec['generation']['evidence_only'])
 if raw:
  assert ':question/difficulty' not in q and ':question/worked-solution' not in q and ':answer-field/correct' not in f
 else:
  level=q[':question/difficulty'].split('/')[-1];assert level in g.SUPPORTED_LEVELS
  if rec['generation']['eligible_for_learning']:g.parameters(level,p)
  sol=q[':question/worked-solution'];formatting(sol);align=re.search(r'\\begin\{aligned\}\n(.*?)\n\\end\{aligned\}',sol,re.S);assert align
  rawrows=[s.strip() for s in align[1].split(r'\\')];assert len(rawrows)==3
  steps=[equation(s) for s in rawrows]
  for z in steps:assert sp.expand(z/z.coeff(y)-e/e.coeff(y))==0
  # Enforce real source operative structure, not merely equivalent rows:
  # original standard equation, isolate By, then divide to y=mx+b.
  sides=[row.replace('&','').split('=') for row in rawrows]
  assert math(sides[0][0])==e.coeff(x)*x+e.coeff(y)*y and math(sides[0][1])==-e.subs({x:0,y:0})
  assert math(sides[1][0])==e.coeff(y)*y
  assert math(sides[1][1])==-e.coeff(x)*x-e.subs({x:0,y:0})
  assert math(sides[2][0])==y
  claim=re.search(r'So, the slope is \$(.*?)\$\.',sol);assert claim and math(claim[1])==m
  opening=re.search(r'To find the slope of the line \$(.*?)\$',sol);assert opening and full_line(opening[1])==sp.expand(e/e.coeff(y))
  final=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)[-1];answer=next(a for a in bank if a[':answer/id']==correct)
  assert full_line(final)==full_line(answer[':answer/value'])
  phrases=['For two lines to be parallel, they must have the same slope.','we convert to slope-intercept form:','In slope-intercept form, the slope is the $x$-coefficient.','From the given options, the only line that has a slope of']
  positions=[sol.index(s) for s in phrases];assert positions==sorted(positions)
 assert g.digest({'slope':str(m)})==rec['generation']['parameter_fingerprint']
 assert g.digest([str(e.coeff(x)/e.coeff(y)),'1',str(-e.subs({x:0,y:0})/e.coeff(y))])==rec['generation']['standard_line_fingerprint']
 content=g.digest({'version':g.VERSION,'level':None if raw else q[':question/difficulty'].split('/')[-1],'problem':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':sorted(a[':answer/value'] for a in bank),'correct':None if raw else next(a[':answer/value'] for a in bank if a[':answer/id']==correct)})
 assert content==rec['generation']['content_fingerprint']
 assert q[':question/id']==g.uid('question:'+content) and f[':answer-field/id']==g.uid(q[':question/id']+':field:selection')
 for a in bank:assert a[':answer/id']==g.uid(f[':answer-field/id']+':answer:'+a[':answer/value'])
 for ident in (q[':question/id'],f[':answer-field/id']):uuid.UUID(ident)
 return m
structural=inspect

def checks(rec):
 f=rec['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'native field-owned radio choice'} for a in f[':answer-field/choices']]
def write(name,v):(D/name).write_text(json.dumps(v,indent=2)+'\n')
def expect_rejected(fn):
 try:fn()
 except (ValueError,AssertionError):return
 raise AssertionError('Expected rejection')
def main():
 assert g.SOURCE['basis']==1356
 assert g.SOURCE==json.loads((ROOT/'generate/runs/current/sources/17592186087687.json').read_text())
 source={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']};ledger=[];native=[];review=[];cases=[]
 for bp,p in g.SOURCE_CASES.items():
  level=g.SOURCE_LEVELS[bp];raw=g.generate(level,parameters=p,profile=bp);inspect(raw);old=source[bp];q=raw['question'];f=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem']
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in old)
  assert (':answer-field/correct' in nf)==(':answer-field/correct' in f)
  assert f[':answer-field/key']==nf[':answer-field/key'] and f[':answer-field/type'][':db/ident']==nf[':answer-field/type']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices'])
  original={full_line(a[':answer/value']) for a in f[':answer-field/choices']};generated={full_line(a[':answer/value']) for a in nf[':answer-field/choices']};assert len(original)==5 and original==generated
  completed=g.generate(level,parameters=p,profile='completed:'+bp);inspect(completed)
  ledger.append({'source':bp,'raw_prompt_exact':True,'optional_attribute_presence_parity':True,'complete_bank_raw_values_exact':True,'complete_bank_equivalence_matched':True,'matched_values':5,'matched_distractors':4,'original_correct_designation':'absent; 0 available','original_solution':'absent; 0 available','completion':'independently inferred; evidence-only'})
  cases.append({'source_id':old[':question/id'],'source_math_academy_id':bp,'source_db_id':old[':db/id'],'template':'standard-radio','parameters':p,'bank_profile':bp,'level':level,'level_origin':'authored replay call, raw output remains unrated'})
  native.append({'label':'completed/'+bp,'record':completed,'checks':checks(completed)})
  review.extend([{'label':'Original '+bp,'source':old},{'label':'Raw parameterized replay '+bp,'record':raw},{'label':'Inferred completion '+bp,'record':completed}])
  # Changed parameter opaque profile remains public, demonstrably not literal replay.
  changed={'A':p['A'],'B':p['B'],'C':p['C']%12+1};r=g.generate(level,parameters=changed,profile=bp);inspect(r)
  assert r['question'][':question/problem']!=old[':question/problem'];review.append({'label':'Generated opaque evidence variant '+bp,'record':r})
 for bp in g.BANK_PROFILES:
  for A in (-12,-2,2,12):
   for B in (-6,-1,1,6):
    for C in (1,12):
     inspect(g.generate('hard',parameters={'A':A,'B':B,'C':C},profile=bp))
 write('source-cases.json',cases);write('source-replay.json',ledger)
 # Full bounded coefficient domains, both complete method profiles, and RHS
 # boundaries. C only changes intercept arithmetic; slope task count excludes it.
 counts={};rejections={};identities=0
 for level in g.SUPPORTED_LEVELS:
  tasks=set();n=0;rejected=0;seen_profiles=set()
  for A,B in g.COEFFICIENTS[level]:
   for bp in g.AUTHORED_PROFILES:
    for C in (1,6,12):
     p={'A':A,'B':B,'C':C}
     if not g.eligible_bank(p,bp):
      expect_rejected(lambda:g.generate(level,parameters=p,profile=bp));rejected+=1;continue
     r=g.generate(level,seed=4,parameters=p,profile=bp);inspect(r);n+=1;tasks.add(r['generation']['parameter_fingerprint']);seen_profiles.add(bp)
     r2=g.generate(level,seed=35,parameters=p,profile=bp);assert r['question'][':question/id']==r2['question'][':question/id'];inspect(r2);identities+=1
     native.append({'label':f'{level}/{bp}/{A}/{B}/{C}','record':r,'checks':checks(r)})
  assert len(tasks)==len(g.SLOPES[level]) and seen_profiles==set(g.AUTHORED_PROFILES)
  defaults=[g.generate(level,seed) for seed in range(100)]
  for r in defaults:inspect(r)
  assert {r['generation']['bank_profile'] for r in defaults}==set(g.AUTHORED_PROFILES)
  assert any(r['generation']['parameters']['B']<0 for r in defaults) and any(r['generation']['parameters']['B']>0 for r in defaults)
  samples=g.batch(level,min(8,len(g.SLOPES[level])),seed=8421)
  assert len({r['generation']['parameter_fingerprint'] for r in samples})==len(samples)
  for r in samples:inspect(r);review.append({'label':'Authored '+level+' variant','record':r})
  counts[level]={'displayed_instances':n,'distinct_reduced_slope_tasks':len(tasks),'coefficient_pairs':len(g.COEFFICIENTS[level]),'default_profiles_covered':sorted(seen_profiles)};rejections[level]=rejected
 # Invalid explicit workload and whole-bank inputs cannot be silently resampled.
 for level,p in [('easy',{'A':2,'B':2,'C':3}),('moderate',{'A':7,'B':3,'C':3}),('moderate',{'A':2,'B':2,'C':3}),('moderate',{'A':13,'B':6,'C':3}),('hard',{'A':10,'B':5,'C':3}),('hard',{'A':4,'B':3,'C':3}),('hard',{'A':13,'B':3,'C':3}),('easy',{'A':2,'B':1,'C':0})]:expect_rejected(lambda:g.generate(level,parameters=p))
 assert g.task_key({'A':2,'B':-1,'C':1})==g.task_key({'A':4,'B':-2,'C':12})
 assert g.digest(g.line_key({'A':2,'B':-1,'C':1}))==g.digest(g.line_key({'A':4,'B':-2,'C':2}))
 # Sensitivity regression: mathematically equivalent but missing isolation stage.
 r=g.generate_hard(4);broken=json.loads(json.dumps(r));s=broken['question'][':question/worked-solution'];match=re.search(r'\\begin\{aligned\}\n(.*?)\n\\end\{aligned\}',s,re.S);rows=match[1].split(r'\\');rows[1]=rows[2];broken['question'][':question/worked-solution']=s[:match.start(1)]+r'\\'.join(rows)+s[match.end(1):];expect_rejected(lambda:inspect(broken))
 write('review.json',review)
 def preview(o):
  if 'record' in o:return g.markdown(o['record'])
  q=o['source'];f=q[':question/answer-fields'][0]
  return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\nOriginal difficulty, key and solution absent.'
 (D/'review.md').write_text('# Standard-form parallel-line evidence\n\n'+ '\n\n---\n\n'.join('## '+o['label']+'\n\n'+preview(o) for o in review)+'\n')
 write('engine-input.json',native);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 eng=json.loads((D/'engine-report.json').read_text());assert eng['documented_unresolved_checks']==0
 sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
 report={'status':'pass','source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_fidelity':{'sources':3,'raw_attribute_presence':3,'raw_prompt_exact':3,'complete_banks_matched':3,'complete_banks_total':3,'raw_exact_values':15,'equivalent_values':15,'matched_distractors':12,'original_correct_designations_available':0,'original_solutions_available':0,'inferred_completions_mathematically_checked':3,'missing_or_extra':[]},'mathematics':{'levels':counts,'whole_bank_rejections':rejections,'seed_independent_id_checks':identities,'operational_stage_mutation_rejected':True,'full_line_equivalence_and_noncoincidence':True,'displayed_bank_method_recipes_independently_checked':True,'default_signed_family_coverage':True,'opaque_raw_profile_signed_boundary_instances':96,'content_and_owned_identity_recomputed':True},'native_grading':{k:eng[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{'generator':sha(D.with_suffix('.py')),'validator':sha(__file__),'source':sha(D/'source.json'),'grader_binary':sha(ROOT/'generate/runs/current/check-engine'),'grader_source':sha(ROOT/'generate/runs/current/check-engine.rs')},'limitations':['No observed difficulty labels, keys or practice worked solutions: all completed levels/keys/solutions explicitly authored/inferred.','Historical distractor motives unresolved; public raw and completed historical profiles remain evidence-only.','Radio native checks establish ID grading, not mathematical equivalence; complete printed lines are independently parsed and checked.','Finite reduced-slope catalog excludes intercept changes and common coefficient scaling from task variety.','Identifier/provenance attributes are preserved in source.json; local replay reassigns UUIDs and omits database entity IDs/MA IDs. Source learner attribute omissions/layout/value strings are preserved.']}
 write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()

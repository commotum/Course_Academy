"""Independent repaired-tangent audit. Run with repository .venv/bin/python.

The small TeX arithmetic parser below is adapted from ../verify.py after review;
it is cross-checked on explicit valid and invalid arithmetic here. No author
verdict, probe count or solution metadata is used as a correctness oracle.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import hashlib, importlib.util, json, platform, random, re, shutil, subprocess, sys
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
REPO=ROOT.parents[3]
sys.path[:0]=[str(ROOT/'package'),str(REPO/'scripts')]
from generator_packages import package_digest, check_dependencies
spec=importlib.util.spec_from_file_location('reviewed_candidate',ROOT/'package/generator.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x): (OUT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def read(path):return json.loads(path.read_text())
def rawhash(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def field(r):return r['question'][':question/answer-fields'][0]
def choices(r):return field(r)[':answer-field/choices']
def key(r):return next(c for c in choices(r) if c[':answer/id']==field(r)[':answer-field/correct'][1])

@lru_cache(None)
def tex(text):
 t=text.replace('π',r'\pi').replace('∘',r'\circ')
 for part in [r'\left',r'\right',r'\displaystyle',r'\,',r'\!']:t=t.replace(part,'')
 t=t.replace(r'\dfrac',r'\frac').replace(r'\cdot','*')
 def group(start):
  assert t[start]=='{';depth=1;end=start+1
  while depth:
   if t[end]=='{':depth+=1
   if t[end]=='}':depth-=1
   end+=1
  return t[start+1:end-1],end
 while r'\frac' in t:
  i=t.index(r'\frac');a,j=group(i+5);b,k=group(j);t=t[:i]+'(('+str(tex(a))+')/('+str(tex(b))+'))'+t[k:]
 while r'\sqrt' in t:
  i=t.index(r'\sqrt');a,j=group(i+5);t=t[:i]+'sqrt('+str(tex(a))+')'+t[j:]
 while r'\tan' in t:
  i=t.index(r'\tan');j=i+4
  while t[j].isspace():j+=1
  assert t[j]=='(';k=j+1;depth=1
  while depth:
   if t[k]=='(':depth+=1
   if t[k]==')':depth-=1
   k+=1
  arg=t[j+1:k-1].replace(r'^\circ','*pi/180').replace(r'^{\circ}','*pi/180')
  t=t[:i]+'('+str(S.tan(tex(arg)))+')'+t[k:]
 t=t.replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**')
 return S.simplify(parse_expr(t,transformations=standard_transformations+(implicit_multiplication_application,)))

def target(r):
 t=re.search(r'\$(.*?)\$',r['question'][':question/problem'])[1]
 a=t.split(r'\tan\left(')[1].split(r'\right)')[0]
 return int(a.split('^')[0]) if r'\circ' in a else int(S.simplify(tex(a)*180/S.pi))
def bounds(v):return (bool(v>0),bool(abs(v)<1))
def shape(text):
 # Pure bank syntax. This uses no target, key, generation metadata or catalog.
 t=re.sub(r'\s+','',text)
 return bool(re.fullmatch(r'-?2[+-]\\sqrt\{3\}',t) or re.fullmatch(r'-?\\sqrt\{3\}[+-]2',t))
def probe(r):
 a=target(r)%180
 bucket=(a<90,a<45 or a>135) # quadrant and comparison with 45 degrees only
 iv=[c for c in choices(r) if bounds(tex(c[':answer/value']))==bucket]
 sh=[c for c in choices(r) if shape(c[':answer/value'])]
 both=[c for c in iv if shape(c[':answer/value'])]
 return {'target':target(r),'key':key(r)[':answer/value'],'key_position':choices(r).index(key(r)),
         'interval_candidates':len(iv),'shape_candidates':len(sh),
         'fraction_free_interval_candidates':sum(r'\frac' not in c[':answer/value'] for c in iv),
         'shape_plus_bounds_candidates':len(both)}
def math_check(r):
 expected=S.trigsimp(S.tan(S.pi*target(r)/180))
 vals=[tex(c[':answer/value']) for c in choices(r)]
 assert len(vals)==5 and len(set(vals))==5
 assert sum(S.simplify(v-expected)==0 for v in vals)==1
 assert S.simplify(tex(key(r)[':answer/value'])-expected)==0
 count=0
 for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',r['question'][':question/worked-solution'],re.S):
  for row in block.split(r'\\'):
   rhs=row.strip().split('&=')[1]
   assert S.simplify(tex(rhs)-expected)==0,(target(r),row)
   count+=1
 hint=r['question'][':question/problem'].split('fact that $')[1].split('$')[0]
 lhs,rhs=hint.split('=')
 if r'\circ' in lhs:lhs=lhs.replace(r'^\circ','');rhs=rhs.replace(r'^\circ','')
 assert S.simplify(tex(lhs)-tex(rhs))==0
 return count

def main():
 manifest=read(ROOT/'package/package.json')
 ph=package_digest(ROOT/'package',manifest['entrypoint'],manifest['files'],dependencies=manifest['dependencies'])
 assert ph=='e7b15035bab20db925c7ca95b4898285773fae170428ca83c375a3bf94a3bd8e'
 source=read(ROOT/'fresh-source/source.json');inventory=read(ROOT/'fresh-source/inventory.json')
 save('source-excerpts.json',{'basis':source['basis'],'kp':source['material']['kp'],'tutorial_2561':source['material']['lessons'][0][':activity/steps'][0][':step/content'],'eligibility':source['material']['source_eligibility'],'inventory_question_ids':[[q[':db/id'],q[':question/id']] for q in inventory['questions']]})
 assert source['material']['source_eligibility']['excluded_questions']==[]
 assert source['material']==read(ROOT/'source/source.json')['material']
 batch=read(ROOT/'evidence/requested.json');assert batch==g.generate(5,3750266970)
 save('requested.json',batch)
 fresh=g.generate(8,92857);save('fresh.json',fresh)
 # Independent catalog enumeration, not the author's declared slots.
 angles=[30,45,60,120,135,150,210,225,240,300,315,330]
 allowed=[15,75,105,165,195,255,285,345]
 params=[(a,b,op,unit) for a in angles for b in angles for op in ('+','-')
         if a+(b if op=='+' else -b) in allowed for unit in ('degrees','radians')]
 assert set(params)==set(g.catalog()) and len(params)==128
 catalog=[g.make(*args,rng=random.Random(81001+i)) for i,args in enumerate(params)]
 save('catalog.json',catalog)
 # Distinct quadrants, both operations/units, clear-thirds and no-clear-thirds.
 representatives=[];seen=set()
 for r in catalog:
  p=r['generation']['parameters'];signature=(target(r)%180,p['operation'],p['unit'],r['generation']['derivation']['clears_thirds'])
  if signature not in seen:representatives.append(r);seen.add(signature)
 save('boundary-samples.json',representatives)
 # Complete observed answer banks are checked against original material directly.
 replay=[];replay_checks=[]
 explicit={'q-1759':(45,30,'+','radians'),'q-43382':(240,45,'+','degrees')}
 for q in source['material']['kp'][':knowledge-point/questions']:
  name=q[':question/math-academy-id'];r=g.make(*explicit[name],profile=name)
  original=q[':question/answer-fields'][0][':answer-field/choices']
  assert sorted(tex(c[':answer/value']) for c in choices(r))==sorted(tex(c[':answer/value']) for c in original)
  assert sorted(g.normalize_tex(c[':answer/value']) for c in choices(r))==sorted(g.normalize_tex(c[':answer/value']) for c in original)
  replay.append(r);replay_checks.append({'source':name,'source_id':q[':db/id'],'complete_choice_bank_equal':True,'probe':probe(r)})
 canonical=g.make(60,45,'-','radians',rng=random.Random(12003));replay.append(canonical)
 save('source-replays.json',replay)
 save('source-replay-results.json',{'cases':replay_checks,'canonical':'e-3521 uses pi/3-pi/4 and exact 2-sqrt(3), complete rationalization; canonical has no bank to reproduce.','normalization':'Prompt prose and malformed captured math delimiters normalized; semantic target and hint preserved. Missing original worked solutions are authored from canonical/tutorial method, not claimed verbatim replay.','lineage':'All referenced source IDs are eligible; inventory contains only the two eligible original standalone questions, no generated descendants.'})
 # Relevant counterfactual: literally identical choices in identical order, changed
 # target. Irrelevant counterfactual: only angle units change, same value and bank.
 pairs=[];counter_rows=[]
 for base in [batch[0],next(r for r in catalog if r['generation']['parameters']['operation']=='+')]:
  vals=[c[':answer/value'] for c in choices(base)]
  alternative=next(tex(t) for t in vals if shape(t) and tex(t)!=tex(key(base)[':answer/value']))
  args=next(a for a in params if S.simplify(S.tan(S.pi*(a[0]+(a[1] if a[2]=='+' else -a[1]))/180)-alternative)==0)
  relevant=g.make(*args,bank_values=vals,rng=random.Random(229))
  p=base['generation']['parameters'];unit='radians' if p['unit']=='degrees' else 'degrees'
  irrelevant=g.make(p['x'],p['y'],p['operation'],unit,bank_values=vals,rng=random.Random(229))
  # Reorder controls to identical displayed order using their actual answer IDs.
  for r in [relevant,irrelevant]:
   field(r)[':answer-field/choices'].sort(key=lambda c:vals.index(c[':answer/value']))
  assert tex(key(relevant)[':answer/value'])!=tex(key(base)[':answer/value'])
  assert tex(key(irrelevant)[':answer/value'])==tex(key(base)[':answer/value'])
  assert [c[':answer/value'] for c in choices(relevant)]==vals
  pairs.append({'original':base,'relevant':relevant,'irrelevant':irrelevant})
  counter_rows.extend([base,relevant,irrelevant])
 save('counterfactuals.json',pairs);save('counterfactual-records.json',counter_rows)
 # Defect-specific regressions; old examples must fail before current passes.
 probes={}
 for name,rows in [('old_interval',read(ROOT/'original/review-1-batch.json')),('old_shape',read(ROOT/'original/review-2-batch.json')),('requested',batch),('fresh',fresh),('catalog',catalog)]:
  pp=[probe(r) for r in rows]
  probes[name]={'count':len(rows),'unique_interval':sum(p['interval_candidates']==1 for p in pp),'unique_shape':sum(p['shape_candidates']==1 for p in pp),'unique_fraction_free_interval':sum(p['fraction_free_interval_candidates']==1 for p in pp),'combined':sum(p['shape_plus_bounds_candidates']==1 for p in pp),'cases':pp}
 assert probes['old_interval']['unique_interval']>0 and probes['old_shape']['unique_shape']>0
 for name in ['requested','fresh','catalog']:
  assert probes[name]['unique_interval']==probes[name]['unique_shape']==probes[name]['unique_fraction_free_interval']==0
 save('shortcut-regressions.json',probes)
 # A same-bank pair directly falsifies any deterministic bank-only key claim.
 # Bounds + exact family still determines a unique result; derive it independently.
 exact_results=sorted(set(S.simplify(S.tan(S.pi*a/180)) for a in allowed),key=str)
 assert len(exact_results)==4 and len(set(bounds(v) for v in exact_results))==4
 save('finite-family-analysis.json',{'angles':allowed,'exact_tangents':{str(a):str(S.simplify(S.tan(S.pi*a/180))) for a in allowed},'four_disjoint_intervals':{str(v):bounds(v) for v in exact_results},'source_bank_combined_probe':[p['probe'] for p in replay_checks],'reasoning':'The combined shape-and-bounds rule uses the exact answer family {2±sqrt(3), -2±sqrt(3)}. Each member occupies a different sign/absolute-size interval. Any unique-key bank containing the correct value has exactly one member of that family in the correct interval. Another distinct value cannot both belong to that family and occupy the same interval. This also solves both complete original banks. Therefore that conjunction is not a repairable new bank-format leak while retaining the finite exact-answer task. The separate bank-only singleton and bounds-only singleton defects remain avoidable and are independently regressed.','limitation':'Learners who memorize the four exact outcomes can combine that knowledge with quadrant/reference-angle bounds; final-answer radio questions cannot force the formula once those outcomes are known.'})
 # Parser controls and independently checked displayed-row equalities.
 assert tex(r'\frac{1}{2+\sqrt{3}}')==2-S.sqrt(3)
 assert tex(r'\tan\left(15^\circ\right)')==2-S.sqrt(3)
 assert tex(r'\frac{3+\sqrt{3}}{3-\sqrt{3}}')==2+S.sqrt(3)
 assert S.simplify(tex(r'\frac{3+\sqrt{3}}{3-\sqrt{3}}')-(2-S.sqrt(3)))!=0
 math_rows=[]
 checked=batch+fresh+representatives+replay+counter_rows
 for i,r in enumerate(checked):math_rows.append({'index':i,'target':target(r),'key':key(r)[':answer/value'],'displayed_equalities_checked':math_check(r)})
 save('math-samples.json',checked);save('math-results.json',{'passed':True,'records':len(checked),'cases':math_rows,'parser_negative_control':'2+sqrt(3) differs from 2-sqrt(3); denominator rationalization and degree parsing independently controlled.'})
 # UI's native choice grader: independently derive expected answer by exact math.
 grader=[]
 for i,r in enumerate(batch+fresh+replay+counter_rows):
  expected=S.simplify(S.tan(S.pi*target(r)/180))
  grader.append({'label':str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if S.simplify(tex(c[':answer/value'])-expected)==0 else 'rejected','purpose':'independent exact-math classification of each radio option'} for c in choices(r)]})
 save('grader-input.json',grader)
 # Bindings and CLI relocation/dependency/rejection contracts.
 relocation=OUT/'relocated-package';relocation.mkdir(exist_ok=True)
 for name in manifest['files']:shutil.copyfile(ROOT/'package'/name,relocation/name)
 cmd=[sys.executable,str(relocation/'generator.py'),'--difficulty','moderate','--count','5','--seed','3750266970','--format','json']
 cli=subprocess.run(cmd,check=True,text=True,capture_output=True,cwd='/tmp')
 assert json.loads(cli.stdout)==batch
 reject=[]
 for difficulty,count in [('hard',5),('moderate',129),('moderate',-1)]:
  c=cmd.copy();c[c.index('--difficulty')+1]=difficulty;c[c.index('--count')+1]=str(count)
  result=subprocess.run(c,text=True,capture_output=True,cwd='/tmp');assert result.returncode!=0
  reject.append({'difficulty':difficulty,'count':count,'exit_code':result.returncode,'stderr':result.stderr})
 assert g.generate(0,129)==[]
 save('packaging.json',{'package_sha256':ph,'dependencies':check_dependencies(manifest['dependencies'],sys.executable),'relocation_equal':True,'deterministic_requested_replay':True,'rejections':reject,'empty_count':[],'code_review':'Runtime imports are standard library plus declared math_format.py; source-banks.json is located relative to __file__. Output is JSON only. Catalog is finite and cycles all four result classes; no content rejection/resampling removes a class.'})
 save('bindings.json',{'package_sha256':ph,'source_sha256':source['source_sha256'],'basis':source['basis'],'inventory_basis':inventory['basis'],'batch_digest':digest(batch),'batch_count':len(batch),'seed':3750266970,'difficulty':'moderate','source_file_sha256':rawhash(ROOT/'fresh-source/source.json'),'inventory_file_sha256':rawhash(ROOT/'fresh-source/inventory.json'),'batch_file_sha256':rawhash(ROOT/'evidence/requested.json'),'review_script_sha256':rawhash(Path(__file__))})
 # A representative sum, both difference signs, and identical-bank target pair.
 render=[batch[0],replay[0],replay[1],pairs[0]['relevant']]
 save('render-input.json',render)
 save('coverage.json',{'catalog_count':len(catalog),'independent_catalog_equal':True,'targets':dict(Counter(target(r) for r in catalog)),'unit_operation_groups':dict(Counter(r['generation']['parameters']['unit']+'/'+r['generation']['parameters']['operation'] for r in catalog)),'requested_keys':[key(r)[':answer/value'] for r in batch],'requested_positions':[choices(r).index(key(r)) for r in batch],'fresh_keys':[key(r)[':answer/value'] for r in fresh],'boundary_sample_count':len(representatives),'choice_positions_by_unit_operation':{unit+'/'+op:dict(Counter(choices(r).index(key(r)) for r in catalog if r['generation']['parameters']['unit']==unit and r['generation']['parameters']['operation']==op)) for unit in ['degrees','radians'] for op in ['+','-']}})
 (OUT/'session-state.md').write_text('Independent source account complete. Candidate digest pinned. Exact displayed math, original-bank replay, defect-specific before/after probes, paired controls and package relocation checked. Await native grader, shared delivery and actual UI render.\n')
 print(json.dumps({'package':ph,'math_records':len(checked),'catalog':len(catalog),'old_interval':probes['old_interval']['unique_interval'],'old_shape':probes['old_shape']['unique_shape'],'requested_interval':probes['requested']['unique_interval'],'requested_shape':probes['requested']['unique_shape'],'boundaries':len(representatives)}))

if __name__=='__main__':main()

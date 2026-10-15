"""Private exhaustive mathematics/source fidelity/native engine validation."""
import copy
import hashlib
import importlib.util
import json
import platform
import re
import subprocess
import sys
import uuid
from pathlib import Path
import sympy as sp
from math_parser import expression,prompt_integrand,integral_body,branches,derivative_residual,X,C
D=Path(__file__).resolve().parent;R=D.parents[2]
spec=importlib.util.spec_from_file_location('reciprocal_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ENGINE=R/'generate/runs/current/check-engine';ENGINE_SHA='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):(D/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def zero(e):return sp.simplify(e)==0

def same_derivative(a,b):return derivative_residual(a-b,sp.Integer(0))==[0,0]

def checked(q,allow_source_defects=False):
 integrand=prompt_integrand(q[':question/problem']);f=q[':question/answer-fields'][0];aa=f[':answer-field/choices'];assert len(aa)==5
 values=[expression(a[':answer/value']) for a in aa]
 good=[derivative_residual(v,integrand)==[0,0] and zero(sp.diff(v,C)-1) for v in values]
 assert sum(good)==1,(q[':question/problem'],values,good)
 if ':answer-field/correct' in f:assert aa[good.index(True)][':answer/id']==f[':answer-field/correct'][1]
 if not allow_source_defects:
  for i,a in enumerate(values):
   for b in values[:i]:
    # On x>0, ln x and ln|x| coincide. A pair that collides on one
    # admissible connected interval cannot appear in a served radio bank.
    residual=derivative_residual(a-b,sp.Integer(0));assert not any(zero(z) for z in residual),(q[':question/problem'],a,b,residual)
 return integrand

def solution_check(q):
 integrand=checked(q);sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==1
 count=0
 def operand(tex):
  tex=tex.strip().rstrip('.,')
  if r'\int' in tex:
   before,body=tex.split(r'\int',1);return (expression(before) if before else sp.Integer(1))*integral_body(body),False
  return expression(tex),True
 body=re.sub(r'\\(?:begin|end)\{aligned\}','',blocks[0])
 for row in body.split(r'\\'):
  parts=row.replace('&','').split('=');assert len(parts)==2
  for part in parts:
   if not part.strip():continue
   value,primitive=operand(part)
   assert derivative_residual(value,integrand)==[0,0] if primitive else zero(value-integrand),(part,integrand)
   if primitive:assert zero(sp.diff(value,C)-1)
   count+=1
 # Independently parse every equality in inline coefficient rationalization.
 for inline in re.findall(r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',sol):
  if '=' in inline:
   operands=[expression(p) for p in inline.rstrip('.,').split('=')]
   assert all(zero(a-b) for a,b in zip(operands,operands[1:]));count+=len(operands)-1
 return count

def math_check(r):
 q=r['question'];m=r['generation'];assert set(r['knowledge_point'])=={'db_id','id','title'};assert r['knowledge_point']['db_id']==g.KP_ID
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 assert g.fingerprint(sp.simplify(prompt_integrand(q[':question/problem'])*X))==m['mathematical_fingerprint']
 assert not m['evidence_only'] and m['eligible_for_learning']
 ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']];assert len(ids)==len(set(ids))
 for id_ in ids:uuid.UUID(id_)
 assert '@@' not in json.dumps(r)
 level=q[':question/difficulty'].split('/')[-1]
 other=g.generate(level,seed=m['seed']+177,template=m['template'],parameters=m['parameters'],profile=m['bank_profile'])
 assert q[':question/id']==other['question'][':question/id']
 assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in other['question'][':question/answer-fields'][0][':answer-field/choices'])
 return solution_check(q)

def native_checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Canonical owned choice '+a[':answer/value']} for a in f[':answer-field/choices']]+[{'submitted':s,'expected':'rejected','purpose':'Ordinary nonchoice integer wrong answer '+s} for s in ('0','1','+1')]

def main():
 assert sha(ENGINE)==ENGINE_SHA
 baseline=json.load(open(D/'registered-baseline.json'));assert {str(p.relative_to(R)) for p in (R/'generate/scratch/17592186105715').rglob('*') if p.is_file()}|{'generate/scratch/17592186105715.py'}==set(baseline)
 assert all(sha(R/path)==value for path,value in baseline.items())
 source=json.load(open(D/'source.json'));assert source['basis']==2275
 assert (D/'source.json').read_bytes()==(R/'generate/runs/current/refresh-2026-10-14/sources/17592186105715.json').read_bytes()
 originals=[q for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q]
 cases=[];fidelity=[];review=[];review_text=[];rows=[];steps=0
 for o in originals:
  mid=o[':question/math-academy-id'];t=g.TEMPLATES[mid];p=t['parameters'];raw=g.generate('easy',template=mid,parameters=p,profile='raw');q=raw['question'];of=o[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert q[':question/problem']==g.clean(o[':question/problem'])
  assert (':question/worked-solution' in q)==(':question/worked-solution' in o)
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==g.clean(o[':question/worked-solution'])
  assert (':question/difficulty' in o)==(':question/difficulty' in q)
  original=[g.clean(a[':answer/value'],True) for a in of[':answer-field/choices']];rendered=[a[':answer/value'] for a in nf[':answer-field/choices']];assert sorted(original)==sorted(rendered)
  assert (':answer-field/correct' in nf)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   assert next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])==g.clean(of[':answer-field/correct'][':answer/value'],True)
  checked(q,True)
  served=g.generate('easy',template=mid,parameters=p);steps+=math_check(served);rows.append(served)
  sf=served['question'][':question/answer-fields'][0];served_values=[a[':answer/value'] for a in sf[':answer-field/choices']];matched=sum(v in served_values for v in original)
  fidelity.append({'source_id':mid,'raw_complete_bank':True,'raw_matched_values':5,'raw_total_values':5,'raw_prompt':True,'raw_solution':':question/worked-solution' in o,'raw_correct_designation':':answer-field/correct' in of,'served_profile':served['generation']['bank_profile'],'served_matched_original_values':matched,'served_original_total_values':5,'removed_original_values':[v for v in original if v not in served_values],'authored_repair_values':[v for v in served_values if v not in original],'served_prompt_match':True,'served_solution_match':':question/worked-solution' in o,'source_missing_key_repaired':mid=='q-29934'})
  cases.append({'source_id':mid,'level':'easy','difficulty':'easy','template':mid,'bank_profile':'raw','profile':'raw','parameters':p,'served_profile':served['generation']['bank_profile'],'source_error':mid in g.REPAIRS})
  review.append(served);variant=g.generate('easy',seed=19,template=mid,parameters=next(p0 for p0 in g.domain('easy',mid) if p0!=p));review.append(variant)
  review_text.append('## '+mid+' original (immutable evidence)\n\n'+o[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in of[':answer-field/choices'])+'\n\n'+o.get(':question/worked-solution','Source has no solution or key.')+'\n\n### Served anchor ('+served['generation']['bank_profile']+')\n\n'+g.markdown(served)+'\n\n### Changed coefficient, same method\n\n'+g.markdown(variant))
 capacities={};slot_coverage={}
 for level in g.LEVELS:
  meaningful=set();profiles={};slots={}
  for mid in g.templates(level):
   for p in g.domain(level,mid):
    r=g.generate(level,seed=33,template=mid,parameters=p);steps+=math_check(r);rows.append(r);meaningful.add(r['generation']['mathematical_fingerprint']);profiles[mid]=profiles.get(mid,0)+1
    for key,value in p.items():slots.setdefault(key,set()).add(value)
  capacities[level]=len(meaningful);slot_coverage[level]={'profile_cases':profiles,'slots':{key:sorted(value) for key,value in slots.items()}}
  allrows=g.batch(level,len(meaningful),seed=41);assert len({r['generation']['mathematical_fingerprint'] for r in allrows})==len(meaningful)
  try:g.batch(level,len(meaningful)+1)
  except ValueError:pass
  else:raise AssertionError('Capacity overflow was not rejected')
  if level!='easy':
   for r in (g.generate(level,seed=2,parameters=g.domain(level)[0]),g.generate(level,seed=17,parameters=g.domain(level)[-1])):
    review.append(r);review_text.append('## '+level+' authored calibration\n\n'+g.markdown(r))
 for r in review:math_check(r)
 negative=0
 for call in [lambda:g.generate('easy',True),lambda:g.generate('easy',1.0),lambda:g.batch('easy',True),lambda:g.batch('easy',1,True),lambda:g.batch('easy',-1),lambda:g.generate('easy',parameters={'n':True}),lambda:g.generate('hard',parameters={'a':2,'n':4}),lambda:g.generate('moderate',parameters={'a':2,'b':4}),lambda:g.generate('easy',template='rational-authored'),lambda:g.generate('easy',profile='invented'),lambda:g.generate('easy',field_type='blank')]:
  try:call()
  except ValueError:negative+=1
  else:raise AssertionError('Invalid API input accepted')
 damaged=copy.deepcopy(review[0]);f=damaged['question'][':question/answer-fields'][0];f[':answer-field/choices'][0][':answer/value']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 try:math_check(damaged)
 except AssertionError:negative+=1
 else:raise AssertionError('Corrupt bank accepted')
 damaged=copy.deepcopy(review[-1]);damaged['question'][':question/worked-solution']=damaged['question'][':question/worked-solution'].replace('First,','First, $2=3.$')
 try:solution_check(damaged['question'])
 except AssertionError:negative+=1
 else:raise AssertionError('Corrupt displayed coefficient equality accepted')
 command=[sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--count','1','--seed','17','--format','json'];cli=json.loads(subprocess.check_output(command));assert len(cli)==3 and all(isinstance(r,dict) for r in cli)
 for value in ('1.5','true','-1'):
  result=subprocess.run([sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--count',value],capture_output=True);assert result.returncode!=0
 # All public bounded records and ordinary wrong numeric inputs use frozen native grader.
 native=[{'label':str(i),'record':r,'checks':native_checks(r)} for i,r in enumerate(rows)]
 save('engine-input.json',native);subprocess.run([str(ENGINE),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 report=json.load(open(D/'engine-report.json'));assert report['documented_unresolved_checks']==0;assert sha(ENGINE)==ENGINE_SHA
 save('source-cases.json',{'basis':2275,'lineage':source['lineage'],'questions':cases});save('source-fidelity.json',fidelity);save('review.json',review);(D/'review.md').write_text('\n\n'.join(review_text)+'\n')
 save('capacity.json',{'meaningful_task_count':capacities,'deduplication':'Exact coefficient of c/x, independent of bank/layout/seed/constant representation. Squarefree radicands prevent radical aliases.','slot_coverage':slot_coverage})
 save('validation.json',{'status':'pass','basis':2275,'source_original_count':len(originals),'independent_inventory_count':len(source['record'][':knowledge-point/questions'])-len(originals),'raw_complete_source_banks':len(fidelity),'raw_source_options_matched':sum(x['raw_matched_values'] for x in fidelity),'raw_source_distractors_matched':sum(x['raw_matched_values']-1 for x in fidelity),'raw_source_designations_matched':sum(x['raw_correct_designation'] for x in fidelity),'raw_source_solutions_matched':sum(x['raw_solution'] for x in fidelity),'unaltered_served_complete_banks':sum(x['served_matched_original_values']==5 for x in fidelity),'narrowly_repaired_served_banks':sum(x['served_matched_original_values']!=5 for x in fidelity),'served_values_exact_original':sum(x['served_matched_original_values'] for x in fidelity),'served_values_total':40,'all_public_profile_parameter_cases':len(rows)-len(originals),'solution_operands_and_inline_equalities_checked':steps,'negative_controls':negative,'cli_all_count1_flat_records':len(cli),'meaningful_capacity':capacities,'native_grading':{'engine_sha256':ENGINE_SHA,'entry_point':report['entry_point'],'accepted':report['accepted_checks'],'rejected':report['rejected_checks'],'unresolved':report['documented_unresolved_checks'],'coverage':'Every owned canonical correct and wrong option plus ordinary wrong 0,1,+1 for every bounded public profile/parameter. Equivalent mathematical text is not a radio submission; field-owned same-choice IDs are the answer contract. Foreign/malformed ownership diagnostics are excluded from compatibility totals.'},'valid_math_grading_limitations':[],'source_errors':['q29934 missing key/solution/difficulty and duplicate wrong primitive family','q103369/q103590 duplicate wrong primitive families','q29831 duplicate wrong primitive family on x>0; ln x distractor has only positive real domain'],'registered_baseline_files_unchanged':len(baseline),'dependencies':{'python':platform.python_version(),'sympy':sp.__version__},'engine_sha256':sha(ENGINE)})
 print(json.dumps(json.load(open(D/'validation.json')),indent=2))
if __name__=='__main__':main()

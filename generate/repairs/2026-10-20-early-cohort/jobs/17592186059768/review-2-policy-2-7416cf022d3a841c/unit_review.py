"""Independent follow-up of changed bank-capacity construction.
Run context Python -B unit_review.py; all outputs relative to this evidence folder.
"""
import sys
sys.dont_write_bytecode=True
import review as a
import copy,itertools,hashlib
E=a.E
previous=a.load(a.JOB/'review-1-policy-2-a0f21dc2de58c6f5/relocated-package/17592186059768.py','previous_unit_generator')
failures=[]
for value in (1,-1):
 try: previous.generate('easy',941713401,profile='q-71722',parameters={'2':value,'3':4})
 except ValueError as ex:failures.append({'parameters':{'2':value,'3':4},'old_error':str(ex)})
 else:raise AssertionError('Old input should fail')
records=[];results=[]
for name,src in a.g.PROFILES.items():
 level=src[':question/difficulty'][':db/ident'].split('/')[-1];slots=[str(n) for n in a.g.slots(src)]
 cases=[{k:v for k in slots} for v in (-1,1)]
 if name=='q-71722':cases += [{'2':v,'3':c} for v,c in itertools.product((-2,-1,1,2),(-24,4,24))]
 for ps in cases:
  seed=951830011+len(records)
  if name=='q-71722' and abs(ps['2'])==1 and ps['3']==4:seed=941713401
  r=a.g.generate(level,seed,profile=name,parameters=ps);a.check_math(r)
  assert len(a.bank(r))==5
  assert len({str(a.sign(m)) for m in a.bank(r)})==1
  records.append(r);results.append({'profile':name,'parameters':ps,'seed':seed,'math':'passed','same_mask_bank':True})
a.save('unit-records.json',records);a.save('unit-results.json',{'old_exact_failures':failures,'current_cases':results,'all_passed':True})
# Strict old acceptance witness, unchanged except which generator module is imported.
script=(E/'boundary_regression.py').read_text()
script=script.replace('r=a.g.generate',"a.g=a.load(a.JOB/'review-1-policy-2-a0f21dc2de58c6f5/relocated-package/17592186059768.py','previous_strict_generator')\nr=a.g.generate")
(E/'old_boundary_regression.py').write_text(script)
old=a.run([a.PY,'-B',E/'old_boundary_regression.py'],'old-boundary-regression-command.json');assert old.returncode!=0
now=a.run([a.PY,'-B',E/'boundary_regression.py'],'boundary-regression-command.json');assert now.returncode==0
# Author checks are claims; execute redirected copies against old and current.
author=(a.PKG/'checks/unit_regression.py').read_text()
(E/'author-unit-regression.py').write_text(author.replace('from regression import','from author_regression import'))
# Hyphen-named prior redirected module needs importable counterpart.
(E/'author_regression.py').write_text((E/'author-regression.py').read_text().replace(str(E/'author-check'),str(E/'author-unit-check')))
p=a.run([a.PY,'-B',E/'author-unit-regression.py'],'author-unit-command.json');assert p.returncode==0
oldmodule=(E/'author_regression.py').read_text().replace(str(a.PKG),str(a.JOB/'review-1-policy-2-a0f21dc2de58c6f5/relocated-package')).replace(str(E/'author-unit-check'),str(E/'author-old-unit-check'))
(E/'author_old_unit.py').write_text(oldmodule)
(E/'author-old-unit-regression.py').write_text(author.replace('from regression import','from author_old_unit import'))
p=a.run([a.PY,'-B',E/'author-old-unit-regression.py'],'author-old-unit-command.json');assert p.returncode!=0 and 'Not enough distinct same-mask' in p.stderr
# Relevant signed-unit pair at fixed seed and constant; valid units formerly crashed.
pair=[a.g.generate('easy',941713401,profile='q-71722',parameters={'2':v,'3':4}) for v in (1,-1,2)]
for r in pair:a.check_math(r)
assert len({str(a.correct_matrix(r)) for r in pair})==3
a.save('unit-counterfactual-records.json',pair)
allrecords=a.read(E/'source-replays.json')+a.read(E/'independent-samples.json')+a.read(E/'boundary-records.json')+a.read(E/'runner-batch.json')+a.read(E/'counterfactual-records.json')+records+pair
a.save('math-results.json',{'method':'Independent visible-equation exact integer parser, complete bank uniqueness/key and all worked-solution equations/matrices','count':len(allrecords),'records':a.checks(allrecords)})
# Mutate a repaired record to ensure the witness rejects stale keys.
bad=copy.deepcopy(pair[0]);a.field(bad)[':answer-field/correct'][1]=next(c[':answer/id'] for c in a.field(bad)[':answer-field/choices'] if c[':answer/id']!=a.correct_id(a.field(bad)))
try:a.check_math(bad)
except AssertionError:mutation=True
else:raise AssertionError('stale key accepted')
a.save('witness-mutation.json',{'wrong_key_rejected':mutation,'record':bad})
a.save('grader-input.json',[{'label':f'independent-{i}-{r["generation"]["template"]}','record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==a.correct_id(a.field(r)) else 'rejected','purpose':'independently parsed visible prompt; all five responses'} for c in a.field(r)[':answer-field/choices']]} for i,r in enumerate(allrecords)])
for level in ('easy','moderate'):a.save('unit-'+level+'.json',[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)])
# All five exact batch records plus controlled relevant/irrelevant/role pairs and repaired +/-1.
a.save('render-input.json',a.read(E/'runner-batch.json')+a.read(E/'counterfactual-records.json')[:3]+pair)
(E/'session-state.md').write_text('Milestone: all ten source banks replayed; 40 fresh normal samples, 20 boundaries, 32 targeted unit/repeated cases, controlled pairs and exact five-question batch independently checked. Old strict unit witness and author checks fail the old package and pass current package. Current native grading, UI rendering and delivery pending. Package unchanged.\n')
print({'unit_cases':len(records),'total_math_records':len(allrecords),'old_failure_demonstrated':len(failures),'current_exact_acceptance':True})

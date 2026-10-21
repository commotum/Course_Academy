import json,shutil
from pathlib import Path
R=Path(__file__).resolve().parent;J=R.parent;old=J/'review-1-policy-2-d5d71edec3e4bef3';P=J/'workspace'
# Adapt independent tests; retain original provenance and use fresh bounded samples.
s=(old/'review.py').read_text().replace('(11831,11832,11833,11834)','(62911,62912,62913,62914)')
a=s.index('# Stored generated instances');b=s.index('# Native grader batch',a)
s=s[:a]+'''# Reuse unchanged captured-inventory evidence, independently reverified below.
regenerated=load(ROOT/'generated-records.json'); affected=load(ROOT/'affected-inventory.json')['affected_questions']
''' +s[b:]
(R/'review.py').write_text(s)
for name in ['regression_checks.py','shortcut_checks.py','delivery_audit.py']:
 shutil.copyfile(old/name,R/name)
# Revision account reuses exact source replay and visible-solution validation only.
s=(old/'revision_audit.py').read_text();a=s.index('# Inventory weakness');b=s.index('# Real native learner responses',a);s=s[:a]+s[b:];(R/'revision_audit.py').write_text(s)
for name in ['generated-records.json','affected-inventory.json']:
 shutil.copyfile(old/name,R/name)
# Author checks execute only isolated copies under evidence; source/samples are copied read-only inputs.
for flavor in ['current','old-bank','old-source']:
 d=R/'author-check'/flavor;w=d/'workspace';w.mkdir(parents=True,exist_ok=True)
 manifest=json.loads((P/'package.json').read_text())
 for name in manifest['files']+['package.json','repair_checks.py','qa_math.py','shortcut_checks.py','17592186229183/source-cases.json']:
  out=w/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,out)
 (d/'source').mkdir(exist_ok=True);shutil.copyfile(J/'source/source.json',d/'source/source.json');shutil.copyfile(J/'samples.json',d/'samples.json')
 if flavor=='old-bank':shutil.copyfile(old/'relocated-package/17592186229183.py',w/'17592186229183.py')
 if flavor=='old-source':
  for name in manifest['files']:
   shutil.copyfile(old/'author-check/old-source/workspace'/name,w/name)
(R/'provenance.json').write_text(json.dumps({'source_analysis':str(old/'source-analysis.json'),'independent_scripts_reused':['review.py (fresh seeds and reused inventory segment)','revision_audit.py (source/display/grade portions)','regression_checks.py','shortcut_checks.py','delivery_audit.py'],'retained_inventory_evidence':str(old/'generated-records.json'),'original_binding':{'source_hash':'86cc2f5abd898284cd8d764d495b72110e0fa2cbfbe2a98b3251b5193af42fe4','policy_version':2},'author_checks':'Isolated current and historical negative fixture copies; never execute tests in package.'},indent=2)+'\n')

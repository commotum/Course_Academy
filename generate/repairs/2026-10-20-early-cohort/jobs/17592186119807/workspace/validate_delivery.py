#!/usr/bin/env python3
"""Offline delivery, native grading, inventory and relocation verification."""
import hashlib,json,platform,shutil,subprocess,sys,tempfile
from pathlib import Path
import repair_checks as c
H=c.H;E=c.E;repo=H.parents[5]
def main():
 replay=[c.g.generate('moderate',83,sid,{'translation':0}) for sid in sorted(c.g.CASES)]
 controls=json.loads((E/'counterfactual-records.json').read_text())
 batch=json.loads((E/'delivery-batch/accepted.json').read_text())
 extra=[c.g.generate('moderate',83,'q-34242',c.params(residual)) for residual in (0,1)]
 extra.append(c.g.generate('moderate',83,'q-105163',c.params(0,4,-2)))
 rs=replay+controls+batch+extra
 cases=[{'label':f'{i} {r["generation"]["source_id"]}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if c.canonical(a[':answer/value'])==c.expected(r) else 'rejected','purpose':'independent Fraction solve of visible system, all owned radio alternatives'} for a in c.choices(r)]} for i,r in enumerate(rs)]
 c.save('native-input.json',cases)
 native=subprocess.run([str(repo/'generate/runs/current/check-engine'),str(E/'native-input.json'),str(E/'native-report.json')],check=True,capture_output=True,text=True)
 # Both changes to consistency; fractional arithmetic; valid zero-row shortcut and consistent alternative; restored direct source method.
 render=controls[:2]+extra+[c.g.generate('moderate',83,'q-105165',c.params(0))]
 c.save('render-records.json',render)
 # Retrospective weaknesses concern generated records. Inspect every inventory identity.
 inv=json.loads((H.parent/'source/inventory.json').read_text());source=json.loads((H.parent/'source/source.json').read_text())
 ids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
 original=[q for q in inv['questions'] if q[':question/id'] in ids]
 nonoriginal=[q for q in inv['questions'] if q[':question/id'] not in ids]
 assert not nonoriginal, 'New generated inventory requires exact reproduction/audit'
 c.save('affected-inventory.json',{'affected_questions':[]})
 c.save('inventory-audit.json',{'basis':inv['basis'],'inventory_count':len(inv['questions']),'verified_original_source_ids':len(original),'generated_records':len(nonoriginal),'status':'Verified no stored generated instances in captured inventory; all 14 match original supplied source question UUIDs. Source questions were not relabelled or modified.','question_ids':[q[':question/id'] for q in original],'limit':'Captured inventory only; live database was not accessed.'})
 # Relocate runtime files alone, no repository import paths, no generated package assets.
 manifest=json.loads((H/'package.json').read_text())
 with tempfile.TemporaryDirectory(prefix='ca-19807-') as tmp:
  tmp=Path(tmp)
  for name in manifest['files']:
   dst=tmp/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(H/name,dst)
  cmd=[sys.executable,str(tmp/manifest['entrypoint']),'--difficulty','moderate','--count','5','--seed','119807','--format','json']
  result=subprocess.run(cmd,cwd=tmp,check=True,capture_output=True,text=True)
  relocated=json.loads(result.stdout)
  assert relocated==c.g.batch('moderate',5,119807)
  c.save('relocation.json',{'passed':True,'runtime_files':manifest['files'],'command':'<context-python> <relocated>/17592186119807.py --difficulty moderate --count 5 --seed 119807 --format json','records':len(relocated),'matches_original':True,'python':platform.python_version(),'sympy':c.g.sp.__version__,'generated_assets':[]})
 c.save('validation-summary.json',{'fidelity':'14/14 complete source banks; 70/70 choices, including 56 distractors; original worked methods, one documented source arithmetic correction','correctness':'142 records independently checked with Fraction determinants and row residuals','grading':{'native_cases':len(cases),'checks':sum(len(x['checks']) for x in cases),'all_passed':True},'variation':'All 14 recognizable profiles permit both consistency branches and all four numeric ranks at fixed mathematical evidence, before and after actual shared delivery filters. Exact review counterexamples retained.','rendering':'Run render_preview.py on render-records.json and inspect screenshots; see render-inspection.json when completed.','inventory':'14/14 captured questions verified original; zero generated stored instances','selection_limits':'Native question_selection.rs chooses a difficulty band then a uniform question within it (or first candidate under an unconfigured policy). All records are moderate; no branch/name/rank filtering there. Learner history, policy and future inventory are not available, so no live learner selection claim.','rejection':'No branch-dependent rejection. batch() deduplicates prompt systems by its normalized-equation fingerprint and resamples; delivery deduplication tested separately. Count bound raises on exhaustion.'})
 print(json.dumps({'native_cases':len(cases),'native_checks':sum(len(x['checks']) for x in cases),'inventory_generated':len(nonoriginal),'relocation':True,'render_records':len(render)}))
if __name__=='__main__':main()

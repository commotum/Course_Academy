import copy,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'generate'))
from scripts.generator_publish import Publisher,stable_identities,content_fingerprint
from scripts.generator_packages import resolve_registered_script
import substitution_pedagogy as model
p=Publisher.from_environment(source=':agent/codex');summaries=[]
for row in json.loads((H/'capture.json').read_text())['knowledge_points']:
 kp=row['kp'];d=H/str(kp);entry=resolve_registered_script(row['registered_generator'],ROOT,p.config.math_root);target=d/'package';target.mkdir(exist_ok=True)
 for name in('generator.py','source-evidence.json','band-contract.json'):
  out=target/name
  if out.exists():out.chmod(out.stat().st_mode|0o200)
  shutil.copy2(entry.parent/name,out);out.chmod(out.stat().st_mode|0o200)
 for name in('substitution_pedagogy.py','inverse_substitution_models.py','integration_answer_bank.py'):shutil.copy2(ROOT/'generate'/name,target/name)
 ev=json.loads((target/'source-evidence.json').read_text());pool=[]
 for band in('easy','moderate','hard'):pool+=model.batch(kp,band,8,20261025,evidence=ev)
 accepted=copy.deepcopy(pool)
 for r in accepted:r['question']=stable_identities(r['question'],ev['kp']['id'])
 for name,records in(('candidate-pool',pool),('accepted-pool',accepted)):(d/(name+'.json')).write_text(json.dumps(records,indent=2)+'\n')
 before=json.loads((d/'records-before.json').read_text());oldfps={content_fingerprint(r['question'])for r in before};nnew=sum(content_fingerprint(r['question'])not in oldfps for r in pool)
 assert nnew==0 if kp!=17592186064220 else nnew>0
 summaries.append({'kp':kp,'replacements':nnew});print(kp,'final bank replacements',nnew,flush=True)
(H/'build-verification.json').write_text(json.dumps({'passed':True,'knowledge_points':summaries},indent=2)+'\n')

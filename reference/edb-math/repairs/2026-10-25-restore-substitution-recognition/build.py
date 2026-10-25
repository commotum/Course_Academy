"""Build isolated packages; install local mirrors only after publication."""
import argparse,copy,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'generate/scratch/17592186068915'));sys.path.insert(0,str(ROOT/'generate'))
from scripts.generator_publish import Publisher,stable_identities,content_fingerprint
from scripts.generator_packages import resolve_registered_script
import trig_scaffold,substitution_pedagogy

def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--install',action='store_true');args=ap.parse_args();p=Publisher.from_environment(source=':agent/codex');summary=[]
 for row in json.loads((H/'capture.json').read_text())['knowledge_points']:
  kp=row['kp'];d=H/str(kp);trig=kp in trig_scaffold.CASES;model=trig_scaffold if trig else substitution_pedagogy;helper='trig_scaffold.py'if trig else'substitution_pedagogy.py';entry=resolve_registered_script(row['registered_generator'],ROOT,p.config.math_root)
  target=d/'package';target.mkdir(exist_ok=True)
  manifest=json.loads((entry.parent/'generator-package.json').read_text())
  for name in manifest['files']:
   out=target/name;out.parent.mkdir(parents=True,exist_ok=True)
   if out.exists():out.chmod(out.stat().st_mode|0o200)
   shutil.copy2(entry.parent/name,out);out.chmod(out.stat().st_mode|0o200)
  shutil.copy2(ROOT/'generate'/helper,target/helper)
  shutil.copy2(ROOT/'generate/integration_answer_bank.py',target/'integration_answer_bank.py')
  evidence=json.loads((target/'source-evidence.json').read_text());old_origins=copy.deepcopy(evidence['band_origin'])
  evidence['band_origin']['easy']='Authored easy complete-calculation practice using small source-supported forms and full-answer choices. The learner must choose the substitution; no primitive or substitution is provided.'
  before=json.loads((d/'records-before.json').read_text())
  excluded={r['generation']['mathematical_fingerprint']for r in before[8:] if kp!=17592186064250 or r['question'][':question/difficulty'].endswith('/moderate')}
  evidence['easy_excluded_tasks']=sorted(excluded | (set(evidence.get('excluded_tasks',[]))if kp!=17592186064250 else set()))
  evidence['band_origin']['moderate']='Full calculation with source-supported families and small parameters; mastered prerequisite formulas and routine endpoint values are recalled.'
  evidence['band_origin']['hard']=old_origins['hard'].replace('endpoint values supplied','endpoint values').replace('endpoint facts supplied','endpoint facts recalled').replace('values supplied','values').replace('with familiar endpoint values supplied','with familiar endpoint values')
  evidence['support_policy']='mastered-prerequisite-recall';evidence['support_policy_evidence']='reference/edb-math/audits/2026-10-24-integration-hint-provenance/README.md';save(target/'source-evidence.json',evidence)
  contract=json.loads((target/'band-contract.json').read_text());contract['version']=model.VERSION;contract['support_policy']='mastered-prerequisite-recall';contract['band_origin']=evidence['band_origin'];contract['support']='All bands assess complete calculation and recognition of the substitution. Easy uses complete-answer choices and small forms. Moderate uses exact entry where supported. No substitution, primitive or routine endpoint reminders appear before answering. Domain assumptions remain; worked solutions explain every step.'
  for band in('easy','moderate','hard'):
   if isinstance(contract.get(band),dict):contract[band]['provided_substitution']=False;contract[band]['operation']='evaluate';contract[band]['provided_primitive']=False;contract[band]['provided_endpoint_values']=False
  if isinstance(contract.get('easy'),dict):contract['easy']['displayed_bank_coefficient_maximum']=12
  save(target/'band-contract.json',contract)
  records=[]
  for band in('easy','moderate','hard'):records+=model.batch(kp,band,8,20261024,evidence=evidence)
  before=json.loads((d/'records-before.json').read_text());assert len(before)==len(records)==24
  for old,new in zip(before,records):
   if not old['question'][':question/difficulty'].endswith('/easy'):
    assert content_fingerprint(old['question'])==content_fingerprint(new['question'])
   else:assert content_fingerprint(old['question'])!=content_fingerprint(new['question'])
  save(d/'candidate-pool.json',records)
  accepted=copy.deepcopy(records)
  for r in accepted:r['question']=stable_identities(r['question'],evidence['kp']['id'])
  save(d/'accepted-pool.json',accepted)
  if args.install:
   proof=json.loads((d/'verification.json').read_text());assert proof['passed']
   local=ROOT/f'generate/scratch/{kp}';local.mkdir(exist_ok=True)
   for name in [*manifest['files'],'integration_answer_bank.py']:
    shutil.copy2(target/name,ROOT/f'generate/scratch/{kp}.py'if name=='generator.py'else local/name)
   save(local/'capabilities.json',{'supported_levels':['easy','moderate','hard'],'implementation_version':model.VERSION,'band_contract':'band-contract.json','support_policy':'mastered-prerequisite-recall','band_origin':evidence['band_origin'],'maximum_records_per_call':100})
   (local/'README.md').write_text(f'# Substitution practice — KP {kp}\n\nVersion: {model.VERSION}.\n\nAll bands require choosing the substitution and completing the integral. Easy uses full-answer choices and small parameters. Full calculations retrieve mastered integration formulas and routine endpoint values. Complete worked solutions and mathematical domain assumptions remain.\n\nCurrent immutable package and validation: `reference/edb-math/repairs/2026-10-25-restore-substitution-recognition/`. Older extraction and validation artifacts are historical evidence.\n')
  summary.append({'kp':kp,'version':model.VERSION,'changed_questions':8,'unchanged_full_questions':16});print(kp,'built; retained full-calculation questions preserved',flush=True)
 save(H/'build-verification.json',{'passed':True,'knowledge_points':summary})
if __name__=='__main__':main()

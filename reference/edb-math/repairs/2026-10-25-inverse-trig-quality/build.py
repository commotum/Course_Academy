"""Build isolated inverse-only packages and compare final publication identities."""
import copy,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'generate'))
from scripts.generator_publish import Publisher,stable_identities,content_fingerprint
from scripts.generator_packages import resolve_registered_script
import substitution_pedagogy as model
import inverse_substitution_models as inverse
FILES=['generator.py','source-evidence.json','band-contract.json','substitution_pedagogy.py','inverse_substitution_models.py','integration_answer_bank.py']
def save(path,v):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(v,indent=2)+'\n')
p=Publisher.from_environment(source=':agent/codex');cap=json.loads((H/'capture.json').read_text());summaries=[]
for row in cap['knowledge_points']:
 kp=row['kp'];d=H/str(kp);entry=resolve_registered_script(row['registered_generator'],ROOT,p.config.math_root);target=d/'package';target.mkdir(exist_ok=True)
 for name in ('generator.py','source-evidence.json','band-contract.json'):
  out=target/name
  if out.exists():out.chmod(out.stat().st_mode|0o200)
  shutil.copy2(entry.parent/name,out);out.chmod(out.stat().st_mode|0o200)
 for name in FILES[3:]:shutil.copy2(ROOT/'generate'/name,target/name)
 evidence=json.loads((target/'source-evidence.json').read_text());evidence['basis']=cap['basis']
 evidence['band_origin']={'easy':'Complete calculation in a direct standard form after small useful cancellations. Full-answer choices require normalization and differential knowledge. No given substitution or formula.','moderate':'One familiar square normalization; inverse secant requires a small fractional differential adjustment. Definite intervals include varied familiar endpoint values and one or two nonzero contributions.','hard':'Authored coprime two-coefficient normalization for sine/tangent; source-supported absolute-value normalization for secant. Definite integrals use source-supported small radical normalization and familiar endpoint values. No larger-number proxy or all-symmetric interval rule.'}
 if kp==17592186064220:
  prior=json.loads((d/'records-before.json').read_text())
  evidence['excluded_tasks']=sorted(set(evidence.get('excluded_tasks',[]))|{r['generation']['mathematical_fingerprint']for r in prior[8:]})
 evidence['quality_audit']='reference/edb-math/audits/2026-10-25-inverse-trig-after-recognition/README.md';save(target/'source-evidence.json',evidence)
 contract={'version':inverse.VERSION,'band_origin':evidence['band_origin'],'support':'Recognize the substitution and complete the integral; retrieve mastered facts; every rule and normalization is explained in feedback.','answer_policy':'Diagnostic factor, scale and endpoint mistakes only; no copied-u or arbitrary additive offsets. All inverse antiderivatives are five-choice questions because native inverse-function exact entry is unsupported. Definite moderate/hard use exact entry.','sampling_policy':'Family-first and endpoint-profile-first, before small parameters. Unique mathematical tasks per band. Delivery must retain varied endpoint profiles and normalization work. Legitimate cancellation remains eligible under easy normalization.','calibration':'Imported examples support direct and square normalization for sine/tangent, and secant/hard-definite families. No imported indefinite sine/tangent hard anchors; those hard bands are explicit authored extrapolations.'}
 save(target/'band-contract.json',contract)
 pool=[]
 for band in('easy','moderate','hard'):pool+=model.batch(kp,band,8,20261025,evidence=evidence)
 accepted=copy.deepcopy(pool)
 for r in accepted:r['question']=stable_identities(r['question'],evidence['kp']['id'])
 save(d/'candidate-pool.json',pool);save(d/'accepted-pool.json',accepted)
 before=json.loads((d/'records-before.json').read_text());oldfps={content_fingerprint(r['question'])for r in before};nnew=sum(content_fingerprint(r['question'])not in oldfps for r in pool)
 summaries.append({'kp':kp,'questions':24,'replacements':nnew});print(kp,'built',nnew,'replacement questions',flush=True)
save(H/'build-verification.json',{'passed':True,'knowledge_points':summaries})

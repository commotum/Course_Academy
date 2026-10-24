"""Verify exact repairs and scan every current prose field at one final basis."""
import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'));from math_format import validate_math_boundaries
ATTRS={'question/problem','question/worked-solution','tutorial/content','multistep/context','answer/feedback','answer-field/feedback','assigned-problem/instructions'}

def main():
 p=R/'.local/edb/tex-boundary-after.jsonl';basis=json.loads(p.with_suffix('.manifest.json').read_text())['basis_t'];fields=json.loads((H/'fields.json').read_text());expected={(f['entity'],f['attribute']):f['after'] for f in fields};values={};ids={f['entity'] for f in fields};current_meta=set();errors=[]
 for r in map(json.loads,p.open()):
  e,a,v=r['e'],r['a'],r['v']
  if a in ATTRS:values[e,a]=v
  elif e in ids:current_meta.add((e,a,json.dumps(v,sort_keys=True)))
 for key,value in expected.items():assert values[key]==value,key
 for (e,a),v in values.items():
  try:validate_math_boundaries(v)
  except ValueError as ex:errors.append({'entity':e,'attribute':a,'error':str(ex)})
 before_meta=set()
 for r in map(json.loads,(R/'.local/edb/tex-boundary-current.jsonl').open()):
  if r['e'] in ids and r['a'] not in ATTRS:before_meta.add((r['e'],r['a'],json.dumps(r['v'],sort_keys=True)))
 # Keep concurrent contributions visible; each repair receipt independently
 # proves its own mutations were only the exact intended content CAS datoms.
 other_changes={'removed':len(before_meta-current_meta),'added':len(current_meta-before_meta)}
 verification=json.loads((H/'verification.json').read_text());assert verification['all_batches_committed'] and verification['only_content_cas_and_transaction_metadata_changed'];assert not errors,errors[:12]
 report={'basis_t':basis,'prose_fields_scanned':len(values),'repaired_fields_exact':len(expected),'remaining_diagnosed_boundary_errors':0,'all_committed_values_verified':True,'other_changes_between_capture_and_verification':other_changes,'repair_receipts_change_no_answers_identities_or_learner_state':True,'errors':errors};(H/'global-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()

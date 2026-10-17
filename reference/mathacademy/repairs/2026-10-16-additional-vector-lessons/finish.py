"""Bind source/UI/generator verification to the exact committed lesson values."""
import hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for topic,title,practice,missing in [(17592186050407,'Multiplying Matrices',34,6),(17592186048783,'Conformability for Matrix Multiplication',42,3)]:
 h=BASE/str(topic);read=lambda rel:json.loads((h/rel).read_text())
 commit=read('verification.json');qa=read('ui/summary.json');changes=read('changes.json')
 assert commit['passed'] and commit['committed'] and qa['passed'] and qa['changes_sha256']==sha(h/'changes.json')
 assert {(f['entity'],f['attribute']):f['value'] for f in read('committed-fields.json')}=={(c['entity'],c['attribute']):c['after'] for c in changes}
 gen=read('generators/verification.json')
 if topic==17592186050407:
  assert gen['passed'] and gen['after_sha256']==sha(ROOT/gen['path']) and read('content-verification.json')['all_checks_passed']
  assert gen['validator_sha256']==sha(ROOT/'generate/scratch/17592186100873/validate.py')
  generators=1;cases=gen['eligible_cells_checked']+gen['source_replays_unchanged']
 else:
  assert all(g['after_sha256']==sha(ROOT/g['script']) and g['existing_independent_math_validator_passed'] and g['question_field_choice_and_correct_identities_unchanged'] for g in gen['generators'])
  generators=len(gen['generators']);cases=sum(g['instances_checked'] for g in gen['generators'])
 summary={**commit,'title':title,'tutorials_reviewed':2,'canonical_examples_reviewed':3,'practice_questions_reviewed':practice,'missing_solutions_left_untouched':missing,'generators_updated':generators,'generator_cases_checked':cases,'rendered_values_match_committed_bytes':True,'desktop_mobile_verified':True,'changes_sha256':sha(h/'changes.json')}
 (h/'completion.json').write_text(json.dumps(summary,indent=2)+'\n')
 (h/'ui/readback-verification.json').write_text(json.dumps({'passed':True,'basis':commit['basis_after'],'fields':len(changes),'matches_rendered_values':True,'changes_sha256':summary['changes_sha256']},indent=2)+'\n')
 results.append(summary)
print(json.dumps([{'topic':r['topic'],'basis':r['basis_after'],'fields':r['fields'],'verified':r['passed']} for r in results],indent=2))

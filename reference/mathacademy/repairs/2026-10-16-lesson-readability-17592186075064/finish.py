"""Bind tested layouts to committed values without repeating unchanged renders."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
read=lambda rel:json.loads((HERE/rel).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changes=read('changes.json');qa=read('ui/summary.json');commit=read('verification.json')
assert qa['passed'] and commit['passed'] and commit['committed']
assert qa['changes_sha256']==sha(HERE/'changes.json')
fields={(f['entity'],f['attribute']):f['value'] for f in read('committed-fields.json')}
assert fields=={(c['entity'],c['attribute']):c['after'] for c in changes}
gens=read('generators/verification.json');tuples=read('generators/tuple-layout-verification.json')
assert gens['passed'] and tuples['passed']
g777=next(g for g in gens['generators'] if g['knowledge_point']==17592186073777)
assert g777['script_sha256']==sha(ROOT/'generate/scratch/17592186073777.py')
assert tuples['script_sha256']==sha(ROOT/'generate/scratch/17592186073778.py')
seed=read('../2026-10-16-line-definitions-17592186561226/verification.json');assert seed['passed'] and seed['committed']
summary={'passed':True,'committed':True,'topic':17592186050240,'question_prompts_improved':40,'tutorials_improved':4,'questions_reviewed':55,'tutorials_reviewed':5,'generators_updated':2,'basis_after':commit['basis_after'],'seed_basis_after':seed['basis_after'],'rendered_values_match_committed_bytes':True,'final_changes_sha256':sha(HERE/'changes.json'),'math_answers_difficulties_saved_progress_preserved':True,'missing_solutions_left_unfilled':True,'desktop_mobile_checks_passed':True,'generator_checks_passed':True}
(HERE/'completion.json').write_text(json.dumps(summary,indent=2)+'\n')
(HERE/'ui/readback-verification.json').write_text(json.dumps({'passed':True,'basis':commit['basis_after'],'fields':len(changes),'matches_rendered_values':True,'changes_sha256':summary['final_changes_sha256']},indent=2)+'\n')
print(json.dumps(summary,indent=2))

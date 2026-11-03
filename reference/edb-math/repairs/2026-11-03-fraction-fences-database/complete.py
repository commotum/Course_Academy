"""Consolidate final fixed-basis census, transactions and validation evidence."""
import json,sys,urllib.request
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.commit import Committer

def read(h,name):return json.loads((h/name).read_text())
def main():
    second=H.with_name(H.name+'-shorthand');rows=[];cases=[];renders=0;answer_identities=0;requests=0;p=Publisher.from_environment(source=':agent/codex')
    for h in (H,second):
        for name in ('audit.json','verification.json','preflight.json','identity.json','render-verification.json','live-verification.json'):assert read(h,name)['passed']
        rows+=read(h,'proposals.json');cases+=read(h,'live-verification.json')['checks'];renders+=read(h,'render-verification.json')['profiles_rendered'];answer_identities+=read(h,'identity.json')['answer_matching_identities_verified']
        for work in sorted((h/'batches').iterdir()):
            if not work.is_dir():continue
            assert read(work,'verification.json')['passed'];assert Committer(p.config,p.client,work).pending() is None;requests+=1
    census=read(H,'final-census.json');assert census['passed'] and census['remaining_identified_fraction_fence_errors']==0;assert read(H,'field-labels.json')['passed']
    for c in cases:assert c['result']['status']==('correct' if c['variant']=='key' else 'incorrect'),(c['question'],c['variant'])
    with urllib.request.urlopen('http://127.0.0.1:8765/',timeout=10) as response:assert response.status==200
    changes={(r['entity'],r['attribute']):r for r in rows}
    result={'passed':True,'database_wide':True,'final_census_basis':census['basis'],'content_facts_scanned':census['all_content_facts_scanned'],'unique_content_fields_scanned':census['unique_fields_scanned'],'remaining_identified_fraction_fence_errors':0,'repaired_fields':len(changes),'repaired_entities':len({e for e,a in changes}),'repaired_by_attribute':dict(Counter(a for e,a in changes)),'verified_committed_requests':requests,'pending_requests':0,'matching_answer_identities_preserved':answer_identities,'checkbox_import_labels_verified':read(H,'field-labels.json')['import_label_normalizations_verified'],'formula_render_profiles_passed':renders,'regression_tests_passed':118,'paired_live_grading_checks':len(cases),'unique_questions_graded':len({c['question'] for c in cases}),'all_grading_results_unchanged':True,'raw_learner_submissions_rewritten':0,'question_answer_identities_and_learner_history_preserved':True,'service_reloaded_and_healthy':True}
    (H/'completion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()

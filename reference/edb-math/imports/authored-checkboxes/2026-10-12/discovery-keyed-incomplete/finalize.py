"""Finalize handoff integrity without accessing the database."""
import csv,hashlib,json
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'Cargo.toml').exists())
AUDIT=ROOT/'generate/reports/checkbox-next-review-2026-10-12'
def read(path):return json.loads(path.read_text())
def save(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    plan=read(OUT/'plan.json');preview=read(OUT/'preview.json');grading=read(OUT/'engine-report.json')
    assert preview['passed'] and not preview['committed']
    questions=read(OUT/'batch-01/plan.json')['questions'];resolutions=read(OUT/'resolutions.json')
    with (OUT/'prepared-questions.csv').open('w') as stream:
        writer=csv.writer(stream);writer.writerow(['question_eid','math_academy_id','knowledge_point_eids','correct_labels','difficulty','prompt_clarification'])
        for q in questions:writer.writerow([q['id'],q['ma_id'],' '.join(str(k['id']) for k in q['kps']),' '.join(q['correct']),q['difficulty'] or '',bool(q['prompt_qualifications'])])
    for row in resolutions['questions']:row.update(commit_status='prepared_previewed_not_submitted',prepared_basis=plan['basis'],batch=1)
    save(OUT/'resolutions.json',resolutions)
    assert next(q for q in questions if q['ma_id']=='q-94772')['correct']==['III']
    assert grading['whole_question_canonical_accepted']==69 and grading['whole_original_choices_preserved']==620 and grading['documented_unresolved_checks']==0
    integrity=dict(passed=True,committed=False,database_writes=0,basis=plan['basis'],source=plan['source'],counts=plan['counts'],grading={k:v for k,v in grading.items() if k!='records'},files={})
    for batch in plan['batches']:
        directory=Path(batch['directory']);request=read(directory/'prepared-request.json')
        assert digest(directory/'transaction.edn')==batch['sha256']==request['sha256']
        assert request['source']==plan['source'] and request['basis']==batch['basis_guard']
        assert not (directory/'commit-intent.json').exists()
        for name in ['transaction.edn','prepared-request.json','plan.json','preview.edn','preview.json','questions-after.edn','fields-after.edn']:integrity['files'][str((directory/name).relative_to(OUT))]=digest(directory/name)
    for name in ['snapshot.edn','resolutions.json','identity-check.json','preview.json','engine-input.json','engine-report.json','native-build.json','native-preview-build.json','prepared-questions.csv']:integrity['files'][name]=digest(OUT/name)
    save(OUT/'package-integrity.json',integrity)
    status=read(OUT/'status.json');status.update(grading_passed=True,package_integrity='package-integrity.json',q94772_key_preserved=True,unsubmitted_question_ids=sorted(q['id'] for q in questions),unknown_outcome_requests=[],confirmed_commits=[]);save(OUT/'status.json',status)
    audit_status=read(AUDIT/'status.json');audit_status.update(state='keyed_group_prepared_previewed_not_submitted',prepared_package=str(OUT),prepared_basis=plan['basis'],native_preview_passed=True,native_grading_passed=True,key_repair_proposal_withdrawn=True);save(AUDIT/'status.json',audit_status)
    path=AUDIT/'README.md';text=path.read_text().replace('**No database writes, transaction preparation, or native preview performed.**','**No database writes.** The evaluated group was subsequently prepared and natively previewed at basis 1846; see the prepared package linked below.')
    if '\nPrepared package:' not in text:text+='\nPrepared package: [discovery-keyed-incomplete]('+str(OUT/'README.md')+'). All 69 reviewed questions are included, with existing keys preserved, and seven separate solution corrections. No transaction has been submitted.\n'
    path.write_text(text)
    print(json.dumps(dict(ready=True,basis=plan['basis'],**plan['counts'],native_preview_passed=True,native_grading_passed=True,committed=False)))

if __name__=='__main__':main()

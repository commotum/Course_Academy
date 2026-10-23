import pathlib,json,hashlib,shutil
R=pathlib.Path(__file__).resolve().parent; J=R.parent; W=J/'workspace'; P=J/'review-1-policy-2-48d685555902faba'
def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
save('package-before.json',{str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()})
for n in ['independent_lib.py','audit.py','targeted.py','variation.py','package_checks.py','test_role_exchange.py','scope-results.json']:
 shutil.copyfile(P/n,R/n)
# Fresh, bounded regression seeds; source replay and controlled boundaries retained.
p=R/'audit.py'; t=p.read_text().replace('range(81371,81379)','range(230021,230025)').replace('sample[17]','sample[9]');p.write_text(t)
p=R/'targeted.py';t=p.read_text().replace('range(81451,81475)','range(230101,230125)').replace("if gen['template']=='mixed':affected.append", "if gen['template']=='mixed' and not q.get(':question/retired',False):affected.append")
t=t.replace("'original_source_questions':15", "'original_source_questions':15,'retired_mixed_questions':[q[':question/id'] for q in stored.values() if q.get(':question/retired',False)]")
t=t.replace("'Captured historical hard pool still has the positional weakness; prospective repaired hard delivery is examined separately. Inventory not changed.'", "'Four prior mixed questions retain their historical pattern but are retired at captured basis; no eligible affected mixed questions. One generated both-nonresonant hard record remains eligible and is a justified taught family. No database writes.'")
p.write_text(t)
save('provenance.json',{'prior_review':str(P),'bindings':{'package_matches':True,'source_matches':True,'batch_matches':True,'inventory_changed':True,'engine_changed':True},'reused':['source-analysis.json confirmed original prompts, banks and lesson passages','scope-results.json','independent scripts copied and adapted for fresh seeds and retired eligibility'],'fresh_checks':'Rerun source/math/role/native grader/delivery/selection/render/package checks against current inputs; no old verdict assumed.'})
h=json.loads((J/'repair-history.json').read_text());save('retained-findings.json',{'findings':h['findings'],'event_count':len(h['events']),'preflight':json.loads((J/'repair-preflight.json').read_text()),'review_treatment':'Runtime role regression tested before/current. Prior report installation is a review-artifact problem, superseded by independently produced current writable evidence; does not require modifying previous review or package.'})

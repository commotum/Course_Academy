import pathlib,json,shutil,hashlib
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'review-357-policy-2-5595bf9a345705ea';W=E.parent/'workspace'
names=['review_helpers.py','focused_review.py','reproduce_batch_shortcut.py','reproduce_inventory_shortcut.py','finalize_review.py','previous-runner-batch.json','source-replays.json','source-replay-results.json','independent-records.json','normal-catalog-records.json','construction-regression.json','counterfactual-results.json','math-results.json','grader-final-input.json','grader-final-results.json','render-records.json','render-inspection.json','packaging-results.json','boundary-rejections.json','batch-selection-regression.json','pedagogical-variation.json']
for n in names:shutil.copy2(P/n,E/n)
shutil.copytree(P/'render',E/'render',dirs_exist_ok=True)
provenance={'previous_review':str(P),'binding':json.load(open(P/'review-binding.json')),'current_binding':json.load(open(E/'review-binding.json')),'reused_files':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in names},'reason':'Package, batch, source, policy and engine bindings match; only inventory changed. Reuse independent full coverage and rerun focused scripts; inventory-dependent evidence regenerated.'}
for k in ['package_hash','batch_hash','source_hash','policy_version','engine_hash']:assert provenance['binding'][k]==provenance['current_binding'][k]
(E/'reuse-provenance.json').write_text(json.dumps(provenance,indent=2))
(E/'package-before.json').write_text(json.dumps({str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()},indent=2))
p=E/'focused_review.py';t=p.read_text().replace('202610220+i','202610229+i').replace('seed=20261022,','seed=20261029,').replace('seed=20261023,','seed=20261030,')
t=t.replace("'limits':'Captured basis; no live learner history. Moderate record is ineligible under an easy-only draw but remains in the selectable bank for moderate practice.'","'limits':'Captured basis only; all generated legacy records retired and excluded from practice. Original source records preserved.'")
t=t.replace("Inventory basis 5574 has one eligible moderate legacy median shortcut and two retired easy records.","Inventory basis 5577 has all three generated legacy defects retired.")
p.write_text(t)
print('Prepared independent evidence; matched bindings; refreshed script uses new seeds.')

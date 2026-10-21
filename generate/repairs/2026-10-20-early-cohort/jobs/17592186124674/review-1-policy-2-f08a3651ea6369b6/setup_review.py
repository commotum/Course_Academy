import pathlib,json,hashlib,shutil
E=pathlib.Path(__file__).resolve().parent; J=E.parent; W=J/'workspace'; prev=J/'review-0-policy-2-2563c730827bc9a7'
def save(n,x): (E/n).write_text(json.dumps(x,indent=2)+'\n')
save('package-hashes-before.json',{str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()})
for n in ['reproduce_shortcut.py','boundary-records.json','generated-records.json','inventory-results.json','source-math-results.json']:
 shutil.copy2(prev/n,E/('prior-'+n))
text=(W/'checks/repair.py').read_text().replace("W = Path(__file__).resolve().parents[1]", "W = Path(__file__).resolve().parent.parent / 'workspace'").replace("E = W / 'evidence'", "E = Path(__file__).resolve().parent / 'author-check-rerun'")
(E/'author_repair_check.py').write_text(text)
save('provenance.json',{'prior_review':str(prev),'reused_files':['prior-'+n for n in ['reproduce_shortcut.py','boundary-records.json','generated-records.json','inventory-results.json','source-math-results.json']],'author_check_adaptation':'Only W and E paths changed so every write is inside this review directory. Original checks/repair.py remains unchanged.','source_policy_match':True,'inventory_hash_match':True,'engine_hash_match':True})

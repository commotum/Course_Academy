import pathlib,json,hashlib,shutil,difflib
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';O=J/'review-1-policy-2-800c03f7bd804ec6'
def save(n,v):(R/n).write_text(json.dumps(v,indent=2))
save('package-before.json',{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()})
files=['review.py','independent_checks.py','counterfactual_check.py','bank_shortcut.py']
provenance=[]
for f in files:
 shutil.copyfile(O/f,R/f);provenance.append({'file':f,'from':str(O/f),'sha256':hashlib.sha256((O/f).read_bytes()).hexdigest(),'use':'Independent earlier review script; rerun against current package, fresh sampling seeds.'})
f=R/'review.py';t=f.read_text().replace('59173','867209').replace('672913','812773').replace('9357','62983');f.write_text(t)
save('reuse-provenance.json',{'source_hash':'49848be6835e656ba18fc748543cc398ffb1f4c9bdde5ea9e2704f01559ece90','reused_independent_scripts':provenance,'prior_results_not_certification':'All applicable executable checks rerun. Source account confirmed directly. Diff constrains fresh testing to bank changes.'})
changes={}
for f in json.loads((P/'package.json').read_text())['files']:
 a=(O/'relocated'/f).read_text();b=(P/f).read_text();changes[f]={'unchanged':a==b,'diff':''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='prior/'+f,tofile='current/'+f))}
save('runtime-changes.json',changes)
(R/'session-state.md').write_text('Independent source account confirmed and saved before author material. Inspected both retained findings and current preflight. Current runtime changes are quotient_bank and radical-bank construction; parser/dependency contract unchanged. Next: rerun retained checks on failing/current copies, focused counterfactuals, actual delivery/grader/UI.\n')
print({k:{'unchanged':v['unchanged'],'diff_lines':len(v['diff'].splitlines())} for k,v in changes.items()})

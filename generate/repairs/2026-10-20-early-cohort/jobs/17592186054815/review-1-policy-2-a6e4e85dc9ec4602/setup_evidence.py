import pathlib,json,shutil,hashlib,subprocess,sys
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';P=J/'review-0-policy-2-30c6820df2e8d8dd';PY='/home/jake/Developer/Course_Academy/.venv/bin/python'
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
save('package-hashes-before.json',hashes())
provenance=[]
for name in ['source_acceptance.py','finish_checks.py']:
 dst=E/('previous-'+name);shutil.copy2(P/name,dst);provenance.append({'from':str(P/name),'to':dst.name,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
# Author checks are run from an evidence-only copy to prevent their hardcoded output writes touching package.
A=E/'author-check-copy';shutil.copytree(W,A,ignore=shutil.ignore_patterns('evidence','__pycache__'),dirs_exist_ok=True)
commands=[]
for label,pkg in [('old',P/'relocated'),('current',W)]:
 cmd=[PY,'-B',str(E/'previous-source_acceptance.py'),'--package',str(pkg),'--source',str(J/'source/source.json'),'--output',str(E/f'source-acceptance-{label}.json')]
 r=subprocess.run(cmd,capture_output=True,text=True);commands.append({'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 assert r.returncode==(1 if label=='old' else 0)
cmd=[PY,'-B',str(A/'checks/repair_check.py')];r=subprocess.run(cmd,capture_output=True,text=True);commands.append({'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0,r.stderr
save('retained-check-execution.json',{'preflight':json.load(open(J/'repair-preflight.json')),'commands':commands,'provenance':provenance,'note':'Earlier strict regression fails on retained original relocated package and passes current package. Author check copied before execution; writes only below evidence_root. It is corroboration, not independent acceptance.'})
print(json.dumps({'old_regression_exit':commands[0]['exit_code'],'current_regression_exit':commands[1]['exit_code'],'author_check_exit':r.returncode}))

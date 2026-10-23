import pathlib,json,subprocess,sys
H=pathlib.Path(__file__).resolve().parent;J=H.parent;P=J/'workspace';PY='/home/jake/Developer/Course_Academy/.venv/bin/python';old=J/'review-0-policy-2-8040d13f050e26af/relocated'
results=[]
# Both independent retained regression and author regression must distinguish old and current packages.
author=(P/'checks/replay_completeness.py').read_text()
for label,pkg,expected in [('prior',old,False),('current',P,True)]:
 cmd=[PY,'-B',str(H/'replay_regression.py'),'--package',str(pkg)]
 r=subprocess.run(cmd,capture_output=True,text=True)
 results.append({'test':'retained independent regression','package':label,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'expected_pass':expected});assert (r.returncode==0)==expected
 text=author.replace('ROOT = Path(__file__).resolve().parents[1]',f'ROOT = Path({str(pkg)!r})')
 path=H/f'author-regression-{label}.py';path.write_text(text)
 cmd=[PY,'-B',str(path),'--source',str(J/'source/source.json'),'--output',str(H/f'author-replays-{label}.json')]
 r=subprocess.run(cmd,capture_output=True,text=True)
 results.append({'test':'author regression relocated without changing checks','package':label,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'expected_pass':expected});assert (r.returncode==0)==expected
(H/'repair-regression-results.json').write_text(json.dumps(results,indent=2))
sys.dont_write_bytecode=True;sys.path.insert(0,str(P));import generator as g
cs=json.load(open(H/'counterfactual-records.json'));base=cs[9];col=g.generate(template='chelsea-dual-blank',seed=1218,parameters={'name':'A','entries':[[1,2],[4,5]]});cs.append(col)
(H/'counterfactual-records.json').write_text(json.dumps(cs,indent=2))
cases=json.load(open(H/'grader-input.json'));cases.append({'label':'Chelsea column removal 2x3 to 2x2','record':col,'checks':[{'field_index':i,'submitted':v,'expected':out} for i in [0,1] for v,out in [('2','accepted'),('4/2','accepted'),('3','rejected')]]})
(H/'grader-input.json').write_text(json.dumps(cases,indent=2))
rs=json.load(open(H/'render-input.json'));rs.append(col);(H/'render-input.json').write_text(json.dumps(rs,indent=2))
print('Both tests fail on prior missing-profile example and pass on current package. Added independent column-removal control.')

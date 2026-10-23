import os,subprocess,pathlib,json
R=pathlib.Path(__file__).resolve().parent;J=R.parent;REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
results=[]
for name in ['batch','samples','controls','counterfactual-records','natural-boundary-records']:
 cmd=[str(REPO/'.venv/bin/python'),str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(R/(name+'.json')),'--source',str(J/'source/source.json'),'--inventory',str(J/'source/inventory.json'),'--difficulty','easy','--output',str(R/('delivery-'+name)),'--asset-root',str(R/'assets'),'--math-root','/media/jake/SSD/EDB/math']
 p=subprocess.run(cmd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 results.append({'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
(R/'delivery-commands.json').write_text(json.dumps(results,indent=2));print(json.dumps([{'name':n,'exit_code':p['returncode']} for n,p in zip(['batch','samples','controls','counterfactual-records','natural-boundary-records'],results)]))

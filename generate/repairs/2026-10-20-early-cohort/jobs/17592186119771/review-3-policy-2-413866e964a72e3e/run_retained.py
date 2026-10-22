import pathlib,json,subprocess,sys,shutil,os
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'review-2-policy-2-0c1c91bdcd7c4ff5';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def run(cmd):
 r=subprocess.run(cmd,capture_output=True,text=True,env=env,cwd=E);return {'command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
shutil.copyfile(P/'runner-batch.json',E/'prior-runner-batch.json')
report={}
report['old_sparse']=run([sys.executable,str(E/'test_single_witness.py'),str(E.parent/'review-1-policy-2-0e9bf2a26bc3c6cc/relocated/17592186119771.py')])
shutil.copyfile(E/'single-witness-acceptance.json',E/'prior-single-witness-acceptance.json')
report['current_sparse']=run([sys.executable,str(E/'test_single_witness.py')])
report['old_batch']=run([sys.executable,str(E/'test_batch_shortcut.py'),str(E/'prior-runner-batch.json')])
report['current_batch']=run([sys.executable,str(E/'test_batch_shortcut.py')])
for name in ['single_witness','batch_shortcut']:
 report['author_'+name]=run([sys.executable,str(E/'author-suite'/f'{name}.py')])
assert report['old_sparse']['exit']!=0 and report['old_batch']['exit']!=0
assert all(report[x]['exit']==0 for x in ['current_sparse','current_batch','author_single_witness','author_batch_shortcut'])
(E/'retained-regression-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:{'exit':v['exit'],'stdout':v['stdout'][:450]} for k,v in report.items()}))

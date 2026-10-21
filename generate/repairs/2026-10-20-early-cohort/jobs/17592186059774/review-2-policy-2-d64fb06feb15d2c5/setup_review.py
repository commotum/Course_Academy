from pathlib import Path
import json,hashlib,shutil,subprocess,os
R=Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';old=J/'review-1-policy-2-22438d1e0e264086';repo=Path('/home/jake/Developer/Course_Academy')
def save(n,x):(R/n).write_text(json.dumps(x,indent=2))
def hashes(p):return {str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(p.rglob('*')) if f.is_file()}
save('package-before.json',hashes(P))
(R/'reused').mkdir(exist_ok=True)
for n in ['source-corrections.json','independent.py','targeted_audit.py','post_delivery.py','source-replays.json','fresh-samples.json','coverage.json','inventory-review.json','selection-results.json','pedagogical-variation.json']:
 shutil.copy2(old/n,R/'reused'/n)
shutil.copy2(old/'independent.py',R/'independent.py')
shutil.copy2(old/'source-corrections.json',R/'source-corrections.json')
diff=subprocess.run(['diff','-u',str(old/'relocated/generator.py'),str(P/'generator.py')],capture_output=True,text=True)
(R/'revision.diff').write_text(diff.stdout)
unchanged={n:(old/'relocated'/n).read_bytes()==(P/n).read_bytes() for n in ['source_data.json','math_format.py','requirements.txt','package.json']}
save('revision-diff.json',{'unchanged_files':unchanged,'executable_changes':'revision.diff','provenance':'Prior independent artifacts copied to reused/ from '+str(old),'source_confirmed':'source-analysis.json'})
assert all(unchanged.values())
# Run supplied executable regressions on relocated copies, with path-only changes.
results=[]
for name,base,checks in [('author-current',P,['check_source_capture.py','check_batch_decisions.py']),('author-previous',old/'relocated',['check_batch_decisions.py']),('author-original',J/'review-0-policy-2-58ea7688b3968c62'/'relocated',['check_source_capture.py'])]:
 dest=R/name;dest.mkdir(exist_ok=True);(dest/'checks').mkdir(exist_ok=True);(dest/'evidence/batch-repair').mkdir(parents=True,exist_ok=True)
 for f in json.load(open(P/'package.json'))['files']+['package.json']:shutil.copy2(base/f,dest/f)
 shutil.copy2(P/'checks/independent.py',dest/'checks/independent.py')
 for c in checks:
  text=(P/'checks'/c).read_text().replace("ROOT.parent / 'source/source.json'",repr(str(J/'source/source.json'))).replace("(ROOT.parent / 'source/source.json')",repr(str(J/'source/source.json')))
  # Path division expression needs a Path instance.
  text=text.replace(repr(str(J/'source/source.json')),"Path("+repr(str(J/'source/source.json'))+")")
  text=text.replace('REPO = ROOT.parents[5]','REPO = Path('+repr(str(repo))+')')
  text=text.replace("str(ROOT.parent / 'source/inventory.json')",repr(str(J/'source/inventory.json')))
  (dest/'checks'/c).write_text(text)
  shutil.copy2(old/'runner-batch.json',dest/'evidence/batch-repair/retained-runner-batch.json')
  command=[str(repo/'.venv/bin/python'),str(dest/'checks'/c)]
  pr=subprocess.run(command,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
  results.append({'package':name,'script':c,'path_only_adaptation':True,'command':command,'exit_code':pr.returncode,'stdout':pr.stdout,'stderr':pr.stderr})
save('preflight-reproduction.json',results)
print(json.dumps([{k:x[k] for k in ['package','script','exit_code','stdout']} for x in results]))

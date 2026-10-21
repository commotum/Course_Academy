"""Reproducible minimal-package relocation and deterministic CLI check."""
import pathlib,json,tempfile,subprocess,shutil,sys,hashlib
P=pathlib.Path(__file__).resolve().parents[1];m=json.loads((P/'package.json').read_text());python=sys.executable
assert m['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':__import__('sympy').__version__}}
assert all(not pathlib.Path(f).is_absolute() and '..' not in pathlib.Path(f).parts for f in m['files'])
args=['--difficulty','easy','--count','5','--seed','8114','--format','json']
a=subprocess.check_output([python,str(P/m['entrypoint']),*args]);assert a==subprocess.check_output([python,str(P/m['entrypoint']),*args])
with tempfile.TemporaryDirectory(prefix='dilution-relocation-') as tmp:
 dest=pathlib.Path(tmp)
 for f in m['files']:
  q=dest/f;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/f,q)
 b=subprocess.check_output([python,str(dest/m['entrypoint']),*args],cwd=tmp)
 assert a==b
recs=json.loads(a);assert len(recs)==5
(P/'evidence/batch.json').write_bytes(a)
(P/'evidence/runtime.json').write_text(json.dumps({'exact_dependencies':m['dependencies'],'runtime_files':m['files'],'deterministic':True,'relocation_identical':True,'command':[python,m['entrypoint'],*args],'record_count':len(recs),'batch_sha256':hashlib.sha256(a).hexdigest()},indent=2))
print('Runtime: exact dependencies, deterministic CLI and relocation passed; five easy records saved.')

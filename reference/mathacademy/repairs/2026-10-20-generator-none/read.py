import json,threading,subprocess,hashlib,shutil,ast
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.edn import dumps,loads
from scripts.generator_packages import resolve_registered_script,materialize_package
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];DB=EDBClient(Config(),threading.Event())
def save(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,default=str)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def native(directory,basis,groups):
 directory.mkdir(parents=True,exist_ok=True);(directory/'native-pulls.edn').write_text(dumps(groups)+'\n')
 p=subprocess.run([str(ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'),str(directory),str(basis)],env=DB.environment,capture_output=True,text=True,timeout=240);(directory/'stderr').write_text(p.stderr);p.check_returncode()
 return {n:loads((directory/(n+'.edn')).read_text())for n,_,_ in groups}
if __name__=='__main__':
 identity=DB.status();save('identity.json',identity);registry=DB.query('[:find ?kp ?g ?s :where [?kp :knowledge-point/question-generator ?g] [?g :question-generator/script ?s]]',[],HERE/'evidence','registry',identity['basis']);save('registry.json',registry)
 source=json.loads((HERE/'source-none-by-kp.json').read_text());affected=[]
 for kp,g,ref in registry:
  if str(kp)not in source:continue
  script=resolve_registered_script(ref,ROOT,Path(DB.config.math_root));manifest=script.parent/'generator-package.json';packaged=manifest.exists()
  if packaged:
   dest=HERE/'originals'/str(kp)
   if not dest.exists():materialize_package(ref,Path(DB.config.math_root),dest)
   m=json.loads((dest/'generator-package.json').read_text());runtime=dest/m['entrypoint']
  else:runtime=script;m=None
  tree=ast.parse(runtime.read_text());functions=[{'name':n.name,'args':[a.arg for a in n.args.args]}for n in tree.body if isinstance(n,ast.FunctionDef)and n.name.startswith(('generate','batch','catalog'))]
  imports=[ast.unparse(n)for n in ast.walk(tree)if isinstance(n,(ast.Import,ast.ImportFrom))]
  affected.append({'kp':kp,'entity':g,'reference':ref,'script':str(script),'runtime_script':str(runtime),'packaged':packaged,'manifest':m,'functions':functions,'imports':imports,'source_none':source[str(kp)],'before_sha256':sha(script)})
 save('affected.json',affected)
 print(json.dumps({'basis':identity['basis'],'registry':len(registry),'affected':len(affected),'legacy':sum(not r['packaged']for r in affected)}))
 for r in affected:print(r['kp'],r['runtime_script'],r['functions'])

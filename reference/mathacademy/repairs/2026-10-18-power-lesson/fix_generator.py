"""Prepare and publish the remaining fraction-parenthesis generator fix."""
import ast,hashlib,json,shutil,threading
from pathlib import Path
from scripts.generator_packages import build_manifest,manifest_digest,verify_package,publish_package,resolve_registered_script
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.edn import dumps,loads,kw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE=':agent/codex'
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def prepare():
 kp=next(k for k in json.loads((HERE/'topic.json').read_text())[0][0][':topic/knowledge-points'] if k[':db/id']==17592186064303);gen=kp[':knowledge-point/question-generator'];ref=gen[':question-generator/script'];old=Path('/media/jake/SSD/EDB/math')/Path(ref).parent;pkg=verify_package(old,Path(ref).parts[2]);dest=HERE/'generator-repair';dest.mkdir(exist_ok=True)
 for name in pkg.manifest['files']:shutil.copyfile(old/name,dest/name)
 canonical=(ROOT/'scripts/question_capture/math_format.py').read_text();node=next(n for n in ast.parse(canonical).body if isinstance(n,ast.FunctionDef) and n.name=='scalable_fraction_parentheses');helper='\n'.join(canonical.splitlines()[node.lineno-1:node.end_lineno])+'\n\n\n'
 def patch(path):
  text=path.read_text()
  if 'def scalable_fraction_parentheses' not in text:
   text=text.replace('def normalize_tex(value):',helper+'def normalize_tex(value):');text=text.replace('text = _matrix_layouts(_legacy_commands(text))','text = scalable_fraction_parentheses(_matrix_layouts(_legacy_commands(text)))');path.write_text(text)
  assert 'text = scalable_fraction_parentheses(_matrix_layouts(_legacy_commands(text)))' in text
 patch(dest/'math_format.py');path=dest/'generator.py';path.write_text(path.read_text().replace("VERSION = '1.1.0'","VERSION = '1.1.1'"))
 workspaces=[]
 for script in (ROOT/'.local/learning').rglob('workspace/generator.py'):
  if '17592186064303' in script.read_text() and script.with_name('math_format.py').is_file():patch(script.with_name('math_format.py'));workspaces.append(str(script.relative_to(ROOT)))
 manifest=build_manifest(dest,pkg.entrypoint,pkg.manifest['files'],dependencies=pkg.manifest['dependencies']);digest=manifest_digest(manifest);save('generator-manifest.json',manifest);save('generator-update.json',{'entity':gen[':db/id'],'old_reference':ref,'new_reference':f'generators/{digest[:2]}/{digest}/{pkg.entrypoint}','digest':digest,'workspaces_patched':workspaces});print('Prepared generator',digest)
def commit():
 assert json.loads((HERE/'generator-audit.json').read_text())['passed'];assert json.loads((HERE/'generator-ui/rendering.json').read_text())['passed']
 db=EDBClient(Config(),threading.Event());info=json.loads((HERE/'generator-update.json').read_text());manifest=json.loads((HERE/'generator-manifest.json').read_text());pkg=publish_package(HERE/'generator-repair','generator.py',manifest['files'],db.config.math_root,dependencies=manifest['dependencies'],expected_digest=info['digest']);assert pkg.reference==info['new_reference']
 forms=[[kw(':db/cas'),info['entity'],kw(':question-generator/script'),info['old_reference'],info['new_reference']]];tx=HERE/'generator-transaction.edn';tx.write_text(dumps(forms)+'\n');intent=HERE/'generator-request.json'
 if intent.exists():request=json.loads(intent.read_text())
 else:
  report=loads(db.command('with','--file',tx,'--source',SOURCE));assert report[':edb/committed'] is False and len(report[':edb/tx-data'])==3
  assert db.status()['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
  digest=hashlib.sha256(tx.read_bytes()).hexdigest();basis=report[':edb/db-before-t'];request={'source':SOURCE,'basis':basis,'digest':digest,'request_key':'power-lesson-generator-v1-b'+str(basis)+'-'+digest};save('generator-request.json',request)
 assert hashlib.sha256(tx.read_bytes()).hexdigest()==request['digest']
 if not (HERE/'generator-receipt.edn').exists():
  output=db.command('transact','--file',tx,'--source',request['source'],'--basis',request['basis'],'--endpoint',db.config.endpoint,'--request-key',request['request_key'],'--timeout-ms','120000',timeout=150);(HERE/'generator-receipt.edn').write_text(output)
 report=loads((HERE/'generator-receipt.edn').read_text());assert report[':edb/committed'] is True
 attrs={str(i):e for e,i in loads((HERE.parent/'2026-10-18-big-parentheses/evidence/idents.edn').read_text())}
 assert len(report[':edb/tx-data'])==3 and all(s==attrs[SOURCE] and a in (attrs[':question-generator/script'],attrs[':db/txInstant']) for e,a,v,t,s,added in report[':edb/tx-data'])
 rows=db.query('[:find (pull ?g [*]) :in $ ?g :where [?g :question-generator/id _]]',[info['entity']],HERE/'committed','generator',report[':edb/basis-t']);assert rows[0][0][':question-generator/script']==info['new_reference'];resolve_registered_script(info['new_reference'],ROOT,db.config.math_root)
 save('generator-verification.json',{'passed':True,'committed':True,'basis_after':report[':edb/basis-t'],'new_reference':info['new_reference'],'only_generator_reference_changed':True,'readback_matches':True});print('Committed and verified generator update at',report[':edb/basis-t'])
if __name__=='__main__':
 import sys
 commit() if '--commit' in sys.argv else prepare()

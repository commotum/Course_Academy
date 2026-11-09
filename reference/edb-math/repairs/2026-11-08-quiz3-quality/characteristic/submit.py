import sys,json,hashlib,subprocess
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection,loads
base=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic').resolve();root=Path.cwd();db=connection();tx=base/'transaction.edn';sha=hashlib.sha256(tx.read_bytes()).hexdigest();intent=base/'commit-intent.json'
if not intent.exists():intent.write_text(json.dumps({'database':'math','source':':course-academy.source/editor','endpoint':'/tmp/edb-math/writer.sock','file':str(tx),'sha256':sha,'request_key':'quiz3-characteristic-quality-'+sha[:24],'read_basis':json.loads((base/'basis.json').read_text())['basis'],'guards':'CAS on every changed old cardinality-one value plus installed question/field/tutorial specs; preserve detached historical entities'},indent=2)+'\n')
i=json.loads(intent.read_text());assert sha==i['sha256']
if '--commit'not in sys.argv:
 exe=root/'.local/edb/capture-runtime/native-preview-74dc6726c42c0594c98069f66077a9078a8cf13732f8beabc35fba79f9795d81'
 args=[str(exe),'with','--database','math','--file',str(tx),'--source',i['source']];name='preview'
else:
 assert (base/'preview.edn').exists();args=[str(root/'.local/edb/capture-runtime/math-edb'),'transact','--database','math','--file',str(tx),'--source',i['source'],'--endpoint',i['endpoint'],'--request-key',i['request_key']];name='receipt'
p=subprocess.run(args,env=db.env,capture_output=True,text=True,timeout=210);(base/(name+'.edn')).write_text(p.stdout);(base/(name+'.stderr')).write_text(p.stderr);print('exit',p.returncode,'output',p.stdout[:500],'stderr',p.stderr[:600]);sys.exit(p.returncode)

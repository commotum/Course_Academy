"""Persist, preview, commit and verify the user-authorized text-only repair."""
from pathlib import Path
import collections,hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps,loads
assert sys.argv[1:]==['--apply-user-authorized']
changes=json.loads((HERE/'changes.json').read_text());prep=json.loads((HERE/'preparation.json').read_text())
render=json.loads((HERE/'render-verification.json').read_text());assert render['passed'] and render['fields']==len(changes)
forms=loads((HERE/'transaction.edn').read_text())
assert forms==[[':db/cas',c['entity'],':'+c['attribute'],c['before'],c['after']] for c in changes]
assert len(changes)==prep['fields'] and prep['missing_fields_added']==prep['structural_edits']==0
sha=hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest();assert sha==prep['transaction_sha256']
db=Publisher.from_environment(source=':agent/codex').client
status=json.loads((HERE/'status.json').read_text());assert db.status()['lineage']==status['lineage']
intent={'database':'math','lineage':status['lineage'],'source':':agent/codex','endpoint':'/tmp/edb-math/writer.sock','file':str(HERE/'transaction.edn'),'sha256':sha,'request_key':'repair-vector-topic-latex-2026-10-30-'+sha[:24]}
intent_path=HERE/'commit-intent.json'
if intent_path.exists():assert json.loads(intent_path.read_text())==intent
else:intent_path.write_text(json.dumps(intent,indent=2))
cli=ROOT.parent/'EDB/target/release/edb'
def run(command,name,*args):
    result=subprocess.run([str(cli),command,'--database','math','--file',intent['file'],'--source',intent['source'],*args],env=db.environment,capture_output=True,text=True,timeout=180)
    (HERE/(name+'.edn')).write_text(result.stdout);(HERE/(name+'.stderr')).write_text(result.stderr)
    assert result.returncode==0,result.stderr
    return loads(result.stdout)
def verify_datoms(report):
    data=report[':edb/tx-data'];assert len(data)==2*len(changes)+1
    # Compare complete entity/value/operation multisets, including repeated strings.
    targets={c['entity'] for c in changes}
    expected=collections.Counter((c['entity'],c[side],added) for c in changes for side,added in [('before',False),('after',True)])
    actual=collections.Counter((d[0],d[2],d[-1]) for d in data if d[0] in targets)
    assert actual==expected,'Unexpected transaction datoms'
receipt_path=HERE/'receipt.edn'
if receipt_path.exists() and receipt_path.stat().st_size:
    receipt=loads(receipt_path.read_text());assert receipt[':edb/committed']
else:
    if not (HERE/'submission-started.json').exists():
        preview=run('with','preview');assert preview[':edb/committed'] is False;verify_datoms(preview)
        (HERE/'submission-started.json').write_text(json.dumps(intent))
    receipt=run('transact','receipt','--endpoint',intent['endpoint'],'--request-key',intent['request_key'],'--timeout-ms','120000')
    assert receipt[':edb/committed']
verify_datoms(receipt);basis=receipt[':edb/db-after-t']
def read(name):
    text=db.command('query','--as-of',basis,'--file',HERE/(name+'-query.edn'),'--inputs',HERE/(name+'-inputs.edn'))
    (HERE/(name+'-after.edn')).write_text(text);return loads(text)
actual=read('preapply');assert {(e,str(a)[1:]):v for e,a,v in actual}=={(c['entity'],c['attribute']):c['after'] for c in changes}
for name in ['protected-structure','missing-solutions','answer-types']:
    before=loads((HERE/(name+'.edn')).read_text());after=read(name)
    assert sorted(map(dumps,after))==sorted(map(dumps,before)),name+' changed'
report={'committed':True,'basis':basis,'source':intent['source'],'request_key':intent['request_key'],'fields':len(changes),'entities':len({c['entity'] for c in changes}),'exact_readback_matches':True,'missing_solutions_preserved':True,'answer_keys_and_field_membership_unchanged':True,'source_inherited_math_unchanged':True,'unresolved_candidates':0,'repaired_field_render_passed':True}
(HERE/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

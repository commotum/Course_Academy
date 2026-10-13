"""Remove the redundant None checkbox while retaining its original evidence."""
import hashlib
import json
import runpy
import subprocess
import sys
import threading
from pathlib import Path
from types import SimpleNamespace

BASE = Path(__file__).resolve().parent
shared = runpy.run_path(str(BASE/'migrate.py'))
DB, ROOT, SOURCE = (shared[k] for k in ('DB','ROOT','SOURCE'))
kw, dumps, loads, save = (shared[k] for k in ('kw','dumps','loads','save'))
OUT = BASE/'remove-none'
OUT.mkdir(exist_ok=True)
QUESTION = 17592186234490

def query(q, inputs, name, basis):
    return DB.query(q,inputs,OUT,name,basis)

def prepare():
    assert not (OUT/'commit-intent.json').exists(), 'Resolve saved submission first'
    basis = DB.basis()
    questions = query('[:find (pull ?q '+shared['PATTERN']+') :in $ ?q :where [?q :question/id _]]',
      [QUESTION],'question-before',basis)
    assert len(questions)==1
    question = questions[0][0]
    fields = question[':question/answer-fields']
    assert {f[':answer-field/key'] for f in fields} == {'I','II','III','None'}
    field = next(f for f in fields if f[':answer-field/key']=='None')
    assert field[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'
    bank = {a[':db/id']:a[':answer/value'] for a in field[':answer-field/choices']}
    assert set(bank.values())=={'true','false'}
    users = query('''[:find ?answer (pull ?item [* {:task-item/status [:db/id :db/ident]}])
      :in $ [?answer ...] :where [?item :task-item/responses ?answer]]''',
      [list(bank)],'responses-before',basis)
    items = {i[':db/id']:i for _,i in users}
    forms = [[kw('db/retract'),QUESTION,kw('question/answer-fields'),field[':db/id']],
      [kw('db/ensure'),QUESTION,kw('question/validate')]]
    for answer,item in users:
        assert item[':task-item/content'][':db/id']==QUESTION
        # A true None response would need a separate review of its historical
        # correctness semantics. The existing saved answer is explicitly false.
        assert bank[answer]=='false'
        forms += [[kw('db/retract'),item[':db/id'],kw('task-item/responses'),answer],
          [kw('db/ensure'),item[':db/id'],kw('task-item/validate')]]
    tx = OUT/'transaction.edn'
    tx.write_text(dumps(forms)+'\n')
    manifest = {'basis':basis,'question':QUESTION,'removed_field':field[':db/id'],
      'removed_responses':[[answer,item[':db/id']] for answer,item in users],
      'source':SOURCE,'sha256':hashlib.sha256(tx.read_bytes()).hexdigest()}
    save(OUT/'plan.json',manifest)
    helper = shared['preview_executable'](SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),
      repo_root=ROOT,preview_bin=None),threading.Event())
    p = subprocess.run([str(helper),'with','--database','math','--file',str(tx),'--source',SOURCE],
      env=DB.env,capture_output=True,text=True,check=True,timeout=120)
    (OUT/'preview.edn').write_text(p.stdout)
    receipt = loads(p.stdout)
    assert receipt[':edb/committed'] is False and receipt[':edb/db-before-t']==basis
    check(receipt,manifest)
    print(json.dumps({'preview_passed':True,'basis':basis,'response_links_removed':len(users)}))

def check(receipt,manifest):
    attrs = dict(DB.attributes(OUT,receipt[':edb/db-before-t']))
    expected = {(QUESTION,kw('question/answer-fields'),manifest['removed_field'])}
    expected.update((item,kw('task-item/responses'),answer) for answer,item in manifest['removed_responses'])
    actual = set()
    for e,a,v,tx,s,added in receipt[':edb/tx-data']:
        assert s==17592186045436
        if added:
            assert attrs[a]==':db/txInstant'
        else:
            actual.add((e,attrs[a],v))
    assert actual==expected

def commit_verify():
    manifest = json.loads((OUT/'plan.json').read_text())
    tx = OUT/'transaction.edn'
    assert hashlib.sha256(tx.read_bytes()).hexdigest()==manifest['sha256']
    intentfile = OUT/'commit-intent.json'
    if not intentfile.exists():
        assert DB.basis()==manifest['basis'], 'Head changed; prepare again'
        save(intentfile,{'database':'math','endpoint':DB.args.endpoint,'basis':manifest['basis'],
          'source':SOURCE,'sha256':manifest['sha256'],
          'request_key':f'q-96676-remove-none-{manifest["basis"]}-{manifest["sha256"]}'})
    intent = json.loads(intentfile.read_text())
    assert intent['sha256']==manifest['sha256'] and intent['source']==SOURCE
    receipt = DB._commit(intent,tx,OUT)
    assert receipt[':edb/committed'] is True
    check(receipt,manifest)
    after = receipt[':edb/db-after-t']
    before = loads((OUT/'question-before.edn').read_text())[0][0]
    current = query('[:find (pull ?q '+shared['PATTERN']+') :in $ ?q :where [?q :question/id _]]',
      [QUESTION],'question-after',after)[0][0]
    expected = dict(before)
    expected[':question/answer-fields'] = [f for f in before[':question/answer-fields'] if f[':db/id']!=manifest['removed_field']]
    assert current==expected
    olditems = {i[':db/id']:i for _,i in loads((OUT/'responses-before.edn').read_text())}
    for itemid,old in olditems.items():
        now = query('''[:find (pull ?i [* {:task-item/status [:db/id :db/ident]}])
          :in $ ?i :where [?i :task-item/id _]]''',[itemid],'item-after-'+str(itemid),after)[0][0]
        expected = dict(old)
        removed = {answer for answer,i in manifest['removed_responses'] if i==itemid}
        expected[':task-item/responses'] = [a for a in old[':task-item/responses'] if a[':db/id'] not in removed]
        assert now==expected
    original = query('[:find (pull ?q '+shared['PATTERN']+') :in $ ?q :where [?q :question/id _]]',
      [QUESTION],'question-history-before',manifest['basis'])[0][0]
    assert original==before
    field = query('''[:find (pull ?f [* {:answer-field/type [:db/id :db/ident]}
      {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}
      {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}])
      :in $ ?f :where [?f :answer-field/id _]]''',[manifest['removed_field']],'retained-field',after)[0][0]
    assert field==next(f for f in before[':question/answer-fields'] if f[':db/id']==manifest['removed_field'])
    # Reconfirm attribution on the previously committed batch itself.
    migration = loads((BASE/'commit.edn').read_text())
    assert migration[':edb/committed'] is True and all(d[4]==17592186045436 for d in migration[':edb/tx-data'])
    result = {'committed':True,'verified':True,'basis_before':manifest['basis'],'basis_after':after,
      'question':QUESTION,'remaining_field_keys':['I','II','III'],'source':SOURCE,
      'saved_response_links_removed':len(manifest['removed_responses']),
      'original_field_and_answers_retained':True,'original_question_verified_in_history':True,
      'learner_correctness_timing_xp_and_progress_unchanged':True,
      'prior_migration_source_verified':SOURCE}
    save(OUT/'verification.json',result)
    print(json.dumps(result))

if __name__=='__main__':
    {'prepare':prepare,'commit':commit_verify}[sys.argv[1]]()

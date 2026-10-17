"""Prepare this lesson using the established checkbox migration implementation."""
import importlib.util
import json
from pathlib import Path
from read_scope import DB, QUESTION, ITEM
from scripts.database.edn import loads, dumps, kw

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'Cargo.toml').exists())
LEGACY = ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-12/finder-easy/prepare.py'
spec = importlib.util.spec_from_file_location('checkbox_migration', LEGACY)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.OUT = HERE
m.AUDIT = HERE/'audit-input.json'
SOURCE = m.SOURCE
IDS = [17592186492000, 17592186492056]

def prepare():
    assert not (HERE/'commit-intent.json').exists(), 'Reconcile retained submission first'
    snapshot = loads((HERE/'snapshot.edn').read_text())
    current = DB.status()
    assert current['lineage'] == snapshot['lineage']
    # Refresh every read dependency together immediately before preparation.
    basis = current['basis']
    questions = DB.query('[:find (pull ?q '+QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',
                        [IDS], HERE/'refresh', 'questions', basis)
    prior = {q[':db/id']:q for [q] in snapshot['questions']}
    assert all(q == prior[q[':db/id']] for [q] in questions), 'Question changed: re-review before preparing'
    items = DB.query('[:find ?q (pull ?item '+ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',
                     [IDS], HERE/'refresh', 'items', basis)
    assert items == [r for r in snapshot['items'] if r[0] in IDS], 'Learner state changed: re-review'
    source = DB.query('[:find (pull ?s [:db/id :db/ident :db/doc]) :in $ ?ident :where [?s :db/ident ?ident]]',
                      [kw(SOURCE)], HERE/'refresh', 'source', basis)
    assert len(source) == 1
    from scripts.database.edn import Tagged
    refs = sorted({r[':db/id'] for [q] in questions for f in q[':question/answer-fields']
                   for r in [f]+f[':answer-field/choices']})
    incoming = DB.query('[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]',
                        [[Tagged('edb/ref',e) for e in refs]], HERE/'refresh','incoming',basis)
    assert sorted(incoming) == sorted(snapshot['incoming']), 'Ownership or response use changed'
    attrs = {r[0][':db/id']:r[0][':db/ident'] for r in snapshot.get('schema',snapshot['attributes'])}
    q_by_field = {q[':question/answer-fields'][0][':db/id']:q[':db/id'] for [q] in questions}
    answer_fields = {a[':db/id']:f[':db/id'] for [q] in questions for f in q[':question/answer-fields'] for a in f[':answer-field/choices']}
    for e,a,target in incoming:
        name = str(attrs[a])
        assert (name == ':question/answer-fields' and q_by_field.get(target)==e) or (
            name in (':answer-field/choices', ':answer-field/correct') and answer_fields.get(target)==e), (e,name,target)
    assert all(not item.get(':task-item/responses') for _,item in items)
    if 'schema' not in snapshot:
        snapshot['schema'] = snapshot['attributes']
    snapshot.update(basis=basis, attributes=list(attrs.items()),source=source,response_users=[])
    if not (HERE/'initial-snapshot.edn').exists():
        (HERE/'initial-snapshot.edn').write_bytes((HERE/'snapshot.edn').read_bytes())
    (HERE/'snapshot.edn').write_text(dumps(snapshot)+'\n')
    audit = {'basis':basis,'counts':{'secondary_questions':0},'direct_candidates':[{'questions':[
        {'id':q[':db/id'],'ma_id':q[':question/math-academy-id'],
         'kp':q[':knowledge-point/_questions'][0][':db/id'],
         'kp_title':q[':knowledge-point/_questions'][0][':knowledge-point/title'],
         'problem':q[':question/problem'],'review_flags':[]} for [q] in questions]}]}
    m.save('audit-input.json',audit)
    m.plan()
    plan=json.loads((HERE/'plan.json').read_text())
    assert plan['counts']['questions']==2 and not plan['deferred']
    plan['notes'] = ['Both existing database keys independently match the algebra and worked solutions.',
        'All ten original radio options map to their actual selected subsets.',
        'The one saved task item has no responses; its state remains unchanged.',
        'Preserves solutions, difficulty, memberships, original fields and answers, and learner state.',
        'Adds one checkbox per Roman-labeled equation and Select all that apply.',
        'Full basis guard, prompt CAS, native ensures, and exact native grading verification required.']
    m.save('plan.json',plan)
    request=json.loads((HERE/'prepared-request.json').read_text())
    request['request_key']='lesson-17592186492056-checkbox-v1-b'+str(basis)+'-'+plan['transaction_sha256']
    m.save('prepared-request.json',request)
    forms=m.loads((HERE/'transaction.edn').read_text())
    identities={'answer/id':[],'answer-field/id':[]}
    for form in forms:
        if isinstance(form,dict):
            for attr in identities:
                if m.kw(attr) in form:identities[attr].append(form[m.kw(attr)])
    for attr,values in identities.items():
        collisions=DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',
            [values], HERE/'refresh', 'identity-'+attr.replace('/','-'), basis)
        assert not collisions,'Prospective authored identity already exists'
    pulls=[['questions',QUESTION,IDS],['retained','[*]',plan['retained_original_entities']],
           ['items',ITEM,[item[':db/id'] for _,item in items]]]
    (HERE/'native-pulls.edn').write_text(dumps(pulls)+'\n')
    m.save('status.json',{'stage':'prepared','basis':basis,'lineage':snapshot['lineage'],
                         'selected_ids':IDS,'committed_ids':[],'source':SOURCE})

if __name__=='__main__':prepare()

"""Read-only final checks of scoped stored repairs and unrelated Gaussian item."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent
ROOT=H.parents[3]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import Publisher,QUESTION_PULL,jsonable

def read(p):return json.loads(Path(p).read_text())
def canonical(x):
    if isinstance(x,dict):return {k:canonical(v) for k,v in sorted(x.items())}
    if isinstance(x,list):return sorted([canonical(v) for v in x],key=lambda v:json.dumps(v,sort_keys=True))
    return x

def same(a,b):return canonical(a)==canonical(b)

p=Publisher.from_environment();status=p.client.status();basis=status['basis'];results=[]
for name,kp,allowed in [('normal',17592186092240,{':question/problem'}),('vector',17592186235285,{':question/problem',':question/worked-solution'})]:
    D=H.parent/('2026-11-11-'+name+'-independent-practice')
    if name=='normal':before=read(D/'siblings.json')
    else:before=read(D/'capture/kp.json')[':knowledge-point/questions']
    after=p.read_kp(kp,H/(name+'-readback'),basis)
    actual={q[':db/id']:jsonable(q) for q in after[':knowledge-point/questions']}
    changes=[];imports=0
    for q in before:
        i=q[':db/id'];assert i in actual,('missing question',i)
        changed={key for key in set(q)|set(actual[i]) if not same(q.get(key),actual[i].get(key))}
        if q.get(':question/math-academy-id'):
            imports+=1;assert not changed,('import changed',i,changed)
        else:assert changed<=allowed,('unapproved attributes changed',i,changed)
        if changed:changes.append({'entity':i,'attributes':sorted(changed)})
    expected=set([x['entity'] for x in read(D/'case-ledger.json') if x['changed']]) if name=='normal' else {17592186735164}
    assert {r['entity'] for r in changes}==expected,('unexpected repaired set',changes,expected)
    results.append({'name':name,'kp':kp,'baseline_questions':len(before),'imports_unchanged':imports,'changed':changes,'registration':jsonable(after[':knowledge-point/question-generator'])})
    (H/(name+'-live-kp.json')).write_text(json.dumps(jsonable(after),indent=2)+'\n')
base=read(H/'baseline.json')['gaussian_question'];rows=p.client.query('[:find (pull ?q '+QUESTION_PULL+') :in $ ?q :where [?q :question/id _]]',[17592186757021],H,'gaussian-final',basis)
assert same(jsonable(rows[0][0]),base),'Gaussian question changed'
result={'passed':True,'basis':basis,'results':results,'gaussian_unchanged':True}
(H/'live-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

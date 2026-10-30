"""Combine reviewed text repairs, independently check invariants, refresh EDB."""
from pathlib import Path
import collections,hashlib,json,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps,loads,kw
from scripts.question_capture.math_format import MATH,validate_math_structure

def canonical(value):
    # Only approved font/decoration changes are ignored; every other byte must match.
    value=re.sub(r'\\mathbf\s*(?:\{([A-Za-z])\}|\s+([A-Za-z]))',lambda m:m[1] or m[2],value)
    value=re.sub(r'([A-Z]{2})\^\(\s*→\s*\)',lambda m:r'\overrightarrow{'+m[1]+'}',value)
    value=re.sub(r'([A-Z]{2})\^\(\s*[―¯‾]\s*\)',lambda m:r'\overline{'+m[1]+'}',value)
    value=re.sub(r'\\overset\{\s*(?:\\to|\\rightarrow|→)\s*\}(?=\{)',lambda m:r'\overrightarrow',value)
    value=re.sub(r'\\overset\{\s*[―¯‾]\s*\}(?=\{)',lambda m:r'\overline',value)
    value=re.sub(r'\\overset\{\s*\\longleftrightarrow\s*\}(?=\{)',lambda m:r'\overleftrightarrow',value)
    return value

if __name__=='__main__':
    assert not (HERE/'submission-started.json').exists(),'Do not rebuild a submitted request'
    changes=[];seen=set()
    for topic in (17592186048780,17592186049485):
        directory=HERE/f'topic-{topic}'
        assert json.loads((directory/'unresolved.json').read_text())==[],'Unresolved repair candidates'
        for row in json.loads((directory/'changes.json').read_text()):
            row['attribute']=row['attribute'].lstrip(':');key=(row['entity'],row['attribute'])
            assert key not in seen,key;seen.add(key)
            assert row['attribute'] in ('question/problem','question/worked-solution','tutorial/content','answer/value')
            assert row['before'] and row['after'] and row['before']!=row['after']
            assert row['source_evidence'],key
            assert canonical(row['before'])==canonical(row['after']),('Unexpected non-typography change',key)
            bare=row['attribute']=='answer/value'
            if not bare:
                assert MATH.sub('MATH',row['before'])==MATH.sub('MATH',row['after']),('Prose change',key)
            validate_math_structure(row['after'],bare_math=bare)
            changes.append(row)
    db=Publisher.from_environment(source=':agent/codex').client;status=db.status()
    assert status['lineage']=='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
    (HERE/'status.json').write_text(json.dumps(status,indent=2))
    query='[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]'
    inputs=[[[r['entity'],kw(r['attribute'])] for r in changes]]
    current=db.query(query,inputs,HERE,'preapply',status['basis'])
    actual={(e,str(a)[1:]):v for e,a,v in current}
    assert len(actual)==len(changes)
    conflicts=[{'entity':r['entity'],'attribute':r['attribute']} for r in changes if actual[r['entity'],r['attribute']]!=r['before']]
    (HERE/'conflicts.json').write_text(json.dumps(conflicts,indent=2));assert not conflicts,conflicts
    # Ensure missing fields stay missing and duplicate field memberships are untouched.
    protected='''[:find (pull ?q [:db/id {:question/answer-fields [:db/id :answer-field/key {:answer-field/correct [:db/id]} {[:answer-field/choices :limit nil] [:db/id]}]}]) :in $ [?q ...] :where [?q :question/id _]]'''
    db.query(protected,[[17592186097240,17592186106065,17592186097046]],HERE,'protected-structure',status['basis'])
    missing=db.query('[:find (pull ?q [:db/id :question/worked-solution]) :in $ [?q ...] :where [?q :question/id _]]',[[17592186097240,17592186106065]],HERE,'missing-solutions',status['basis'])
    assert all(':question/worked-solution' not in row[0] for row in missing)
    answer_ids=[r['entity'] for r in changes if r['attribute']=='answer/value']
    types=db.query('[:find ?e ?ident :in $ [?e ...] :where [?e :answer/type ?type] [?type :db/ident ?ident]]',[answer_ids],HERE,'answer-types',status['basis'])
    assert len(types)==len(answer_ids) and all(str(t)==':answer.type/math' for e,t in types)
    forms=[[kw('db/cas'),r['entity'],kw(r['attribute']),r['before'],r['after']] for r in changes]
    (HERE/'transaction.edn').write_text(dumps(forms))
    (HERE/'changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False))
    (HERE/'render-input.json').write_text(json.dumps([{'entity':r['entity'],'attribute':r['attribute'],'value':r['after'],'bare_math':r['attribute']=='answer/value'} for r in changes]))
    report={'basis':status['basis'],'fields':len(changes),'entities':len({r['entity'] for r in changes}),'attributes':dict(collections.Counter(r['attribute'] for r in changes)),'only_approved_typography_changed':True,'prose_unchanged':True,'source_inherited_math_unchanged':True,'missing_fields_added':0,'structural_edits':0,'transaction_sha256':hashlib.sha256((HERE/'transaction.edn').read_bytes()).hexdigest()}
    (HERE/'preparation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

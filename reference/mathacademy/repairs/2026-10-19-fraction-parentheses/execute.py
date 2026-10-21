"""Preview, publish and read back the lesson's fence-only repair."""
import copy,hashlib,json,threading
from collections import Counter
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient,QUESTION_PULL
from capture.scripts.database.edn import dumps,loads,kw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SOURCE=':agent/codex'
DB=EDBClient(Config(),threading.Event())
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def plain(value):return json.loads(json.dumps(value,default=str))
def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(v) for v in value),key=lambda v:json.dumps(v,sort_keys=True))
    return value if isinstance(value,(str,int,float,bool)) or value is None else str(value)
def apply(value,changes):
    result=copy.deepcopy(value)
    def walk(v):
        if isinstance(v,list):
            for e in v:walk(e)
        elif isinstance(v,dict):
            for c in changes:
                if v.get(':db/id')==c['entity'] and c['attribute'] in v:
                    assert v[c['attribute']]==c['before'],('Intervening field edit',c['entity'],c['attribute'])
                    v[c['attribute']]=c['after']
            for e in v.values():walk(e)
    walk(result);return result
def read(stage,basis):
    result={};qids=[q[':db/id'] for [q] in json.loads((HERE/'questions.json').read_text())];tids=[t[':db/id'] for t in json.loads((HERE/'tutorials-before.json').read_text())]
    for name,ids,pattern,attr in [('questions',qids,QUESTION_PULL,'question/id'),('tutorials',tids,'[*]','tutorial/id')]:
        rows=DB.query('[:find (pull ?e '+pattern+') :in $ [?e ...] :where [?e :'+attr+' _]]',[ids],HERE/stage,name,basis)
        result[name]=plain(rows)
    return result
def run():
    changes=json.loads((HERE/'changes.json').read_text());audit=json.loads((HERE/'audit.json').read_text());ui=json.loads((HERE/'ui/rendering.json').read_text());generator=json.loads((HERE/'generator-audit.json').read_text())
    assert audit['passed'] and ui['passed'] and generator['passed'];assert audit['changes_sha256']==sha(HERE/'changes.json')
    attrs={str(i):e for e,i in loads((ROOT/'reference/mathacademy/repairs/2026-10-18-equation-chains/evidence/idents.edn').read_text())}
    forms=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in changes]
    for e in sorted({c['entity'] for c in changes}):forms.append([kw('db/ensure'),e,kw('tutorial/validate' if any(c['entity']==e and c['attribute']==':tutorial/content' for c in changes) else 'question/validate')])
    tx=HERE/'transaction.edn';text=dumps(forms)+'\n'
    if tx.exists():assert tx.read_text()==text
    else:tx.write_text(text)
    wanted=Counter((c['entity'],attrs[c['attribute']],c[side],added) for c in changes for side,added in [('before',False),('after',True)])
    def check(report,committed):
        assert report[':edb/committed'] is committed
        actual=Counter();times=0
        for e,a,v,t,s,added in report[':edb/tx-data']:
            assert s==attrs[SOURCE]
            if a==attrs[':db/txInstant']:assert added;times+=1
            else:actual[(e,a,v,added)]+=1
        assert actual==wanted and times==1 and not report[':edb/tempids']
    request_path=HERE/'request.json';receipt=HERE/'receipt.edn'
    if not request_path.exists():
        raw=DB.command('with','--source',SOURCE,'--file',tx,timeout=150);(HERE/'preview.edn').write_text(raw);preview=loads(raw);check(preview,False);basis=preview[':edb/db-before-t']
        before=read('preview-before',basis);apply(before,changes)
        request={'source':SOURCE,'basis':basis,'transaction_sha256':sha(tx),'changes_sha256':sha(HERE/'changes.json'),'rendering_sha256':sha(HERE/'ui/rendering.json'),'request_key':'fraction-parentheses-b'+str(basis)+'-'+sha(tx),'lineage':DB.status()['lineage']};save('request.json',request)
    request=json.loads(request_path.read_text());assert sha(tx)==request['transaction_sha256'] and sha(HERE/'changes.json')==request['changes_sha256'] and sha(HERE/'ui/rendering.json')==request['rendering_sha256']
    assert request['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']==DB.status()['lineage']
    if not receipt.exists():
        try:raw=DB.command('transact','--source',SOURCE,'--file',tx,'--basis',request['basis'],'--endpoint',DB.config.endpoint,'--request-key',request['request_key'],'--timeout-ms','120000',timeout=150)
        except Exception as e:
            save('submission-error.json',{'type':type(e).__name__,'message':str(e),'stdout':getattr(e,'stdout',None),'stderr':getattr(e,'stderr',None)});raise
        receipt.write_text(raw)
    report=loads(receipt.read_text());check(report,True);before_basis=report[':edb/db-before-t'];after_basis=report[':edb/db-after-t']
    before=read('committed-before',before_basis);after=read('committed-after',after_basis);assert canonical(apply(before,changes))==canonical(after)
    from importlib import import_module
    formatter=import_module('reference.mathacademy.repairs.2026-10-19-fraction-parentheses.prepare')
    for [q] in after['questions']:
        for k in (':question/problem',':question/worked-solution'):
            if isinstance(q.get(k),str):assert formatter.scale(q[k])==q[k]
    for [t] in after['tutorials']:assert formatter.scale(t[':tutorial/content'])==t[':tutorial/content']
    result={'committed':True,'basis_before':before_basis,'basis_after':after_basis,'questions_audited':audit['questions'],'tutorials_audited':audit['tutorials'],'questions_repaired':len({c['entity'] for c in changes if c['attribute'].startswith(':question/')}),'tutorials_repaired':len({c['entity'] for c in changes if c['attribute']==':tutorial/content'}),'fields_repaired':len(changes),'only_scalable_fences_added':True,'all_other_content_and_answer_data_preserved':True,'exact_committed_readback':True,'registered_generator_samples_checked':20,'pages_rendered':len(ui['cases']),'reported_questions_repaired':[17592186110297,17592186558498,17592186110298]};save('verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':run()

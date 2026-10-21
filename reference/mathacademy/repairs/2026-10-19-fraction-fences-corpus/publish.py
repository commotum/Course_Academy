"""Bounded, exact-CAS corpus repair using the existing application writer."""
import argparse,copy,hashlib,importlib,json,subprocess,threading
from collections import defaultdict
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.edn import dumps,loads,kw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SOURCE=':agent/codex'
DB=EDBClient(Config(),threading.Event());PREP=importlib.import_module('reference.mathacademy.repairs.2026-10-19-fraction-fences-corpus.prepare');READER=importlib.import_module('reference.mathacademy.repairs.2026-10-19-fraction-fences-corpus.read')
READ=READER.READ;SUBMIT=ROOT/'.local/fraction-fence-audit/submit-cas'
IDENTS={e:i for e,i in json.loads((ROOT/'reference/mathacademy/repairs/2026-10-18-equation-chains/idents.json').read_text())};SOURCE_ID=next(e for e,i in IDENTS.items() if i==SOURCE)
def save(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return sorted((canonical(x) for x in v),key=lambda x:json.dumps(x,sort_keys=True))
    return v if isinstance(v,(str,int,float,bool)) or v is None else str(v)
def apply(before,changes):
    result=copy.deepcopy(before);by_id=defaultdict(list);seen=set()
    for c in changes:by_id[c['entity']].append(c)
    def walk(v):
        if isinstance(v,list):
            for x in v:walk(x)
        elif isinstance(v,dict):
            for c in by_id.get(v.get(':db/id'),[]):
                if c['attribute'] in v:
                    assert v[c['attribute']]==c['before'],('Field changed',c['entity'],c['attribute']);v[c['attribute']]=c['after'];seen.add((c['entity'],c['attribute']))
            for x in v.values():walk(x)
    walk(result);assert len(seen)==len(changes);return result
def read(out,basis,groups):
    out.mkdir(exist_ok=True);(out/'native-pulls.edn').write_text(dumps(groups)+'\n');r=subprocess.run([str(READ),str(out),str(basis)],env=DB.environment,capture_output=True,text=True,timeout=240);(out/'read.stderr').write_text(r.stderr);r.check_returncode()
    return [e for name,_,_ in groups for e in loads((out/(name+'.edn')).read_text())]
def make_groups(changes):
    qs=sorted({q for c in changes for q in c['owning_questions']});ts=sorted({c['entity'] for c in changes if c['attribute']==':tutorial/content'});ans=sorted({c['entity'] for c in changes if c['attribute'].startswith(':answer/')});groups=[]
    for kind,pattern,ids in [('questions',READER.QUESTION,qs),('tutorials','[*]',ts),('answers','[* {:answer/type [:db/id :db/ident]}]',ans)]:
        for start in range(0,len(ids),100):groups.append([kind+'-'+str(start),pattern,ids[start:start+100]])
    return groups
def check_report(report,changes,committed):
    assert report[':edb/committed'] is committed;wanted={(c['entity'],c['attribute'],c[side],added) for c in changes for side,added in [('before',False),('after',True)]};observed=set();times=0
    for e,a,v,t,s,added in report[':edb/tx-data']:
        assert s==SOURCE_ID
        if IDENTS[a]==':db/txInstant':assert added;times+=1;continue
        observed.add((e,IDENTS[a],v,added))
    assert observed==wanted and times==1 and not report[':edb/tempids']
def verify_inputs():
    review=json.loads((HERE/'render-verification.json').read_text());assert review['passed'] and review['changes_sha256']==sha(HERE/'changes.json')
    assert review['math_cases_sha256']==sha(HERE/'math-cases.json')
    for name,digest in review['ui_sha256'].items():assert sha(ROOT/'ui'/name)==digest
    assert DB.status()['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
    return review
def plan():
    changes=json.loads((HERE/'changes.json').read_text());parent={}
    def find(x):
        parent.setdefault(x,x)
        if parent[x]!=x:parent[x]=find(parent[x])
        return parent[x]
    def key(c):return 'q:'+str(c['owning_questions'][0]) if c['owning_questions'] else ('t:' if c['attribute']==':tutorial/content' else 'a:')+str(c['entity'])
    for c in changes:
        first=find(key(c))
        for q in c['owning_questions']:parent[find('q:'+str(q))]=first
    components=defaultdict(list)
    for i,c in enumerate(changes):components[find(key(c))].append(i)
    def priority(indices):
        es={changes[i]['entity'] for i in indices}
        return 0 if es&{17592186111878,17592186110491} else 1 if any(changes[i]['attribute']==':tutorial/content' for i in indices) else 2
    batches=[];indices=[];size=0
    for group in sorted(components.values(),key=lambda g:(priority(g),g[0])):
        n=sum(len(dumps([kw('db/cas'),changes[i]['entity'],kw(changes[i]['attribute']),changes[i]['before'],changes[i]['after']]).encode())+2 for i in group)
        if indices and size+n>3*1024*1024:batches.append(indices);indices=[];size=0
        indices.extend(group);size+=n
    if indices:batches.append(indices)
    result={'changes_sha256':sha(HERE/'changes.json'),'batches':[{'index':i,'change_indices':group,'fields':len(group)} for i,group in enumerate(batches)],'fields':len(changes),'exact_field_CAS':True,'entity_validation':True}
    save(HERE/'batch-plan.json',result);print(json.dumps({'batches':len(batches),'fields':len(changes),'batch_sizes':[len(g) for g in batches]}))
def publish_batch(batch,all_changes):
    out=HERE/'batches'/str(batch['index']);out.mkdir(parents=True,exist_ok=True);original=[all_changes[i] for i in batch['change_indices']]
    if (out/'verification.json').exists():assert json.loads((out/'verification.json').read_text())['committed'];return
    request_path=out/'request.json';receipt=out/'receipt.edn'
    if request_path.exists():
        request=json.loads(request_path.read_text());changes=json.loads((out/'changes.json').read_text());groups=loads((out/'native-pulls.edn').read_text())
    else:
        identity=DB.status();groups=make_groups(original);before=read(out/'preflight',identity['basis'],groups);current={e[':db/id']:e for e in before};changes=[];already=[]
        for c in original:
            value=current[c['entity']][c['attribute']]
            if value==c['after']:already.append({'entity':c['entity'],'attribute':c['attribute']});continue
            assert value==c['before'],('Concurrent content edit needs review',c['entity'],c['attribute'])
            changes.append(c)
        save(out/'already-repaired.json',already);save(out/'changes.json',changes);(out/'native-pulls.edn').write_text(dumps(groups)+'\n')
        if not changes:save(out/'verification.json',{'committed':True,'fields':0,'already_repaired':len(already),'basis_after':identity['basis']});return
        forms=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in changes]
        qs={q for c in changes for q in c['owning_questions']};ts={c['entity'] for c in changes if c['attribute']==':tutorial/content'};ans={c['entity'] for c in changes if c['attribute'].startswith(':answer/')}
        for ids,spec in [(qs,'question/validate'),(ts,'tutorial/validate'),(ans,'answer/validate')]:forms.extend([kw('db/ensure'),e,kw(spec)] for e in sorted(ids))
        tx=out/'transaction.edn';tx.write_text(dumps(forms)+'\n');assert tx.stat().st_size<8*1024*1024
        raw=DB.command('with','--source',SOURCE,'--file',tx,timeout=240);(out/'preview.edn').write_text(raw);preview=loads(raw);check_report(preview,changes,False)
        request={'source':SOURCE,'endpoint':DB.config.endpoint,'database':identity['database'],'lineage':identity['lineage'],'preview_basis':preview[':edb/db-before-t'],'request_key':'fraction-fences-corpus-'+sha(tx),'transaction_file':str(tx),'transaction_sha256':sha(tx),'changes_sha256':sha(out/'changes.json'),'global_changes_sha256':sha(HERE/'changes.json'),'render_verification_sha256':sha(HERE/'render-verification.json'),'concurrency':'All mutations are exact field CAS; entity specs assess authoritative current db-after.'};save(request_path,request)
    assert sha(Path(request['transaction_file']))==request['transaction_sha256'] and sha(out/'changes.json')==request['changes_sha256'] and sha(HERE/'changes.json')==request['global_changes_sha256'] and sha(HERE/'render-verification.json')==request['render_verification_sha256']
    if not receipt.exists():
        args=[str(SUBMIT),'transact','--database',request['database'],'--file',request['transaction_file'],'--endpoint',request['endpoint'],'--request-key',request['request_key'],'--source',SOURCE,'--timeout-ms','180000']
        r=subprocess.run(args,env=DB.environment,capture_output=True,text=True,timeout=210)
        if r.returncode:save(out/'submission-error.json',{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});r.check_returncode()
        receipt.write_text(r.stdout)
    report=loads(receipt.read_text());check_report(report,changes,True);before=read(out/'committed-before',report[':edb/db-before-t'],groups);after=read(out/'committed-after',report[':edb/db-after-t'],groups);assert canonical(apply(before,changes))==canonical(after)
    verify={'committed':True,'basis_before':report[':edb/db-before-t'],'basis_after':report[':edb/db-after-t'],'fields':len(changes),'already_repaired':len(json.loads((out/'already-repaired.json').read_text())),'exact_committed_readback':True,'only_fence_sizing_changed':True,'all_other_question_answer_and_tutorial_data_preserved':True,'request_key':request['request_key']};save(out/'verification.json',verify);print(json.dumps({'batch':batch['index'],**verify}),flush=True)
def publish():
    verify_inputs();plan=json.loads((HERE/'batch-plan.json').read_text());assert plan['changes_sha256']==sha(HERE/'changes.json');changes=json.loads((HERE/'changes.json').read_text())
    for batch in plan['batches']:publish_batch(batch,changes)
    results=[json.loads((HERE/'batches'/str(b['index'])/'verification.json').read_text()) for b in plan['batches']];assert sum(r['fields']+r['already_repaired'] for r in results)==len(changes)
    result={'committed':True,'fields_repaired':sum(r['fields'] for r in results),'already_repaired':sum(r['already_repaired'] for r in results),'batches':len(results),'basis_after':max(r['basis_after'] for r in results),'by_attribute':json.loads((HERE/'preparation-summary.json').read_text())['by_attribute'],'only_scalable_parentheses_added':True,'exact_committed_readback':True,'answer_ids_correct_links_and_all_other_pulled_data_preserved':True,'learner_records_untouched':True};save(HERE/'verification.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['plan','publish']);globals()[p.parse_args().action]()

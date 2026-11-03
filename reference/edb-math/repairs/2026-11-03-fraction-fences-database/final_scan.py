"""Fresh fixed-basis database-wide census after the committed fence repair."""
import gzip,hashlib,json,re,shutil,subprocess,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from scripts.question_capture.math_format import scalable_fraction_parentheses as fix,normalize_fraction_fences_prose as prose

def main():
    assert json.loads((H/'verification.json').read_text())['passed']
    p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];path=H/'final-snapshot.jsonl'
    result=subprocess.run(['/tmp/operator-notation-export','--database',str(p.config.database),str(path)],env={**p.client.environment,'OPERATOR_AUDIT_BASIS':str(basis)},capture_output=True,text=True)
    (H/'final-export.log').write_text(result.stdout+result.stderr);result.check_returncode()
    types={int(k):v for k,v in json.loads((H/'types.json').read_text()).items()};remaining=[];seen={};counts=Counter();candidates=[]
    for line in path.open():
        r=json.loads(line);key=r['e'],r['a'];text=r['raw_string'];counts[r['a']]+=1
        if key in seen:assert seen[key]==text;continue
        seen[key]=text
        if not isinstance(text,str) or not re.search(r'\\(?:dfrac|tfrac|frac)(?![A-Za-z])',text):continue
        after=fix(text) if r['a']=='answer/value' else prose(text)
        if after!=text:candidates.append({'entity':r['e'],'attribute':r['a'],'before':text,'after':after})
    ids=sorted({r['entity'] for r in candidates if r['attribute'] in ('answer/value','answer-field/key') and r['entity'] not in types})
    for start in range(0,len(ids),1000):
        out=p.client.query('[:find (pull ?e [:db/id {:answer/type [:db/ident]} {:answer-field/type [:db/ident]}]) :in $ [?e ...] :where [?e ?a ?v]]',[ids[start:start+1000]],H/'final-types','types-'+str(start),basis)
        types.update({r[0][':db/id']:jsonable(r[0]) for r in out})
    for r in candidates:
        if r['attribute']=='answer/value':
            kind=types[r['entity']].get(':answer/type',{}).get(':db/ident')
            r['after']=fix(r['before']) if kind==':answer.type/math' else prose(r['before']) if kind==':answer.type/text' else r['before']
        elif r['attribute']=='answer-field/key' and types[r['entity']].get(':answer-field/type',{}).get(':db/ident')!=':answer-field.type/checkbox':continue
        if r['after']!=r['before']:remaining.append(r)
    (H/'remaining.json').write_text(json.dumps(remaining,indent=2)+'\n')
    with path.open('rb') as stream:sha=hashlib.file_digest(stream,'sha256').hexdigest()
    result={'passed':not remaining,'basis':basis,'all_content_facts_scanned':sum(counts.values()),'unique_fields_scanned':len(seen),'by_attribute':dict(counts),'remaining_identified_fraction_fence_errors':len(remaining),'snapshot_sha256':sha,'complete_fixed_basis_read':True,'answer_types_resolved':True}
    (H/'final-census.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert not remaining
    for name in ('snapshot','final-snapshot'):
        source=H/(name+'.jsonl')
        if source.exists():
            with source.open('rb') as stream,gzip.open(H/(name+'.jsonl.gz'),'wb',compresslevel=6) as target:shutil.copyfileobj(stream,target)
            source.unlink()

if __name__=='__main__':main()

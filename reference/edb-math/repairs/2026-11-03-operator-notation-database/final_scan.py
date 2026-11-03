"""Fresh whole-database residual census after the committed repair."""
import gzip,hashlib,json,re,shutil,subprocess,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from scripts.question_capture.math_format import MATH,NAMED_FUNCTION_OPERATORS,_BUILTIN_OPERATORS,normalize_function_operators as fix

names='|'.join(sorted(NAMED_FUNCTION_OPERATORS,key=len,reverse=True));named=re.compile(names)
bad=re.compile(r'\\(?:'+'|'.join(n for n in NAMED_FUNCTION_OPERATORS if n not in _BUILTIN_OPERATORS and n not in ('div','mod'))+r')(?![A-Za-z])|\\(?:'+names+r')[xyztuvw](?![A-Za-z])')
styled=re.compile(r'\\(?:text|textrm|mathrm|mathit|mathbf)\s*\{\s*(?:arccsc|arcsec|arccot)\s*\}')
protected=re.compile(r'\\(?:operatorname|text|textrm|mathrm|mathit|mathbf|mathtt|mathsf|begin|end)\*?\s*\{[^{}]*\}')
commands=re.compile(r'\\[A-Za-z]+')
def possible(text):
    if not named.search(text):return False
    if styled.search(text):return True
    outside=protected.sub('',text)
    return bool(bad.search(outside) or r'\u2061' in outside or named.search(commands.sub('',outside)))
def repair_prose(text):
    return MATH.sub(lambda m:fix(m[0]) if possible(m[0]) else m[0],text)

def main():
    assert json.loads((H/'verification.json').read_text())['passed']
    p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis'];path=Path('/tmp/operator-final-census.jsonl')
    result=subprocess.run(['/tmp/operator-notation-export','--database',str(p.config.database),str(path)],env={**p.client.environment,'OPERATOR_AUDIT_BASIS':str(basis)},capture_output=True,text=True)
    (H/'final-export.log').write_text(result.stderr);result.check_returncode()
    manifest=json.loads(path.with_suffix('.manifest.json').read_text());types={int(k):v for k,v in json.loads((H/'types.json').read_text()).items()};remaining=[];seen={};counts=Counter();unknown=[]
    for line in path.open():
        r=json.loads(line);key=r['e'],r['a'];text=r['raw_string'];counts[r['a']]+=1
        if key in seen:assert seen[key]==text;continue
        seen[key]=text
        if not isinstance(text,str):continue
        if r['a']=='answer/value':
            if not possible(text):continue
            after=fix(text)
            if after==text:continue
            kind=types.get(r['e'],{}).get(':answer/type',{}).get(':db/ident')
            if kind is None:unknown.append(r);continue
            if kind==':answer.type/text':after=repair_prose(text)
            elif kind!=':answer.type/math':continue
        else:after=repair_prose(text)
        if after!=text:remaining.append({'entity':r['e'],'attribute':r['a'],'before':text,'after':after})
    if unknown:
        ids=sorted({r['e'] for r in unknown});out=p.client.query('[:find (pull ?e [:db/id {:answer/type [:db/ident]}]) :in $ [?e ...] :where [?e :answer/id _]]',[ids],H/'final-types','types',basis)
        newtypes={r[0][':db/id']:jsonable(r[0]) for r in out}
        for r in unknown:
            kind=newtypes[r['e']][':answer/type'][':db/ident'];text=r['raw_string'];after=fix(text) if kind==':answer.type/math' else repair_prose(text) if kind==':answer.type/text' else text
            if after!=text:remaining.append({'entity':r['e'],'attribute':r['a'],'before':text,'after':after})
    (H/'remaining.json').write_text(json.dumps(remaining,indent=2)+'\n')
    digest=hashlib.file_digest(path.open('rb'),'sha256').hexdigest()
    result={'passed':not remaining,'basis':basis,'all_content_fields_scanned':sum(counts.values()),'unique_fields_scanned':len(seen),
        'by_attribute':dict(counts),'remaining_identified_operator_errors':len(remaining),'snapshot_sha256':digest,
        'complete_fixed_basis_read':True,'answer_types_resolved':True}
    (H/'final-census.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    assert not remaining,'Residual operator errors require repair'
    with path.open('rb') as source,gzip.open(H/'final-snapshot.jsonl.gz','wb',compresslevel=6) as target:shutil.copyfileobj(source,target)
    (H/'final-snapshot.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');path.unlink()

if __name__=='__main__':main()

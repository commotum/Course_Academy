"""Find unscaled parentheses enclosing fractions in every stored content field."""
import gzip,hashlib,importlib.util,json
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('fraction_fence_formatter',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False,default=str)+'\n')
def scale(value,bare=False):return fmt.scalable_fraction_parentheses(value) if bare else fmt.MATH.sub(lambda m:fmt.scalable_fraction_parentheses(m[0]),value)
def signature(value):return value.replace(r'\left','').replace(r'\right','')
def run():
    fields={};scanned=Counter()
    stream=(HERE/'snapshot.jsonl').open() if (HERE/'snapshot.jsonl').exists() else gzip.open(HERE/'snapshot.jsonl.gz','rt')
    for line in stream:
        r=json.loads(line);e,a,v=r['e'],':'+r['a'],r['raw_string'];scanned[a]+=1
        if not isinstance(v,str):continue
        k=e,a
        if k in fields:assert fields[k]['before']==v;continue
        after=scale(v,a==':answer/value')
        if after==v:continue
        assert signature(v)==signature(after)
        assert scale(after,a==':answer/value')==after
        fields[k]={'entity':e,'attribute':a,'before':v,'after':after,'source':r['source'],'tx':r['tx']}
    stream.close();changes=list(fields.values());save('candidate-changes.json',changes)
    manifest=json.loads((HERE/'snapshot.manifest.json').read_text());summary={'basis':manifest['basis_t'],'all_content_fields_scanned':manifest['all_content_attribute_counts'],'fraction_bearing_fields_scanned':dict(scanned),'candidate_fields':len(changes),'entities':len({c['entity'] for c in changes}),'by_attribute':dict(Counter(c['attribute'] for c in changes)),'only_scalable_parentheses_added':True};save('scan-summary.json',summary);print(json.dumps(summary,indent=2))
    for e in (17592186111878,17592186110491):assert any(c['entity']==e for c in changes),('Reported entry missing',e)
if __name__=='__main__':run()

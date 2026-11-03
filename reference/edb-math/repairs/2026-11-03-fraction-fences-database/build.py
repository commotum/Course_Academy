"""Prepare fraction-fence sizing edits across all stored authored content."""
import gzip,json,re,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from scripts.question_capture.math_format import normalize_fraction_fences_prose as prose,scalable_fraction_parentheses as fix

def skeleton(text):
    text=text.replace(r'\left','').replace(r'\right','').replace(r'\langle','⟨').replace(r'\rangle','⟩')
    return re.sub(r'\s+','',text)

def main():
    manifest=json.loads((H/'snapshot.manifest.json').read_text());basis=manifest['basis_t'];potential=[];seen={};scanned=Counter()
    path=H/'snapshot.jsonl';reuse='--reuse' in sys.argv
    stream=[] if reuse else path.open() if path.exists() else gzip.open(path.with_suffix('.jsonl.gz'),'rt')
    for line in stream:
        r=json.loads(line);a=r['a'];text=r['raw_string'];key=(r['e'],a)
        if key in seen:assert seen[key]==text;continue
        seen[key]=text;scanned[a]+=1
        if not isinstance(text,str):continue
        after=fix(text) if a=='answer/value' else prose(text)
        if after!=text:potential.append({'entity':r['e'],'attribute':a,'before':text,'after':after,'source':r['source'],'tx':r['tx']})
    if reuse:
        potential=json.loads((H/'potential.json').read_text());scanned=Counter(manifest['all_content_attribute_counts'])
        for row in potential:
            row['after']=fix(row['before']) if row['attribute']=='answer/value' else prose(row['before'])
    else:
        stream.close();(H/'potential.json').write_text(json.dumps(potential,indent=2)+'\n')
    p=Publisher.from_environment(source=':agent/codex');ids=sorted({r['entity'] for r in potential if r['attribute'] in ('answer/value','answer-field/key')})
    types={int(k):v for k,v in json.loads((H/'types.json').read_text()).items()} if reuse else {}
    for start in ([] if reuse else range(0,len(ids),1000)):
        rows=p.client.query('[:find (pull ?e [:db/id {:answer/type [:db/ident]} {:answer-field/type [:db/ident]}]) :in $ [?e ...] :where [?e ?a ?v]]',[ids[start:start+1000]],H/'types','types-'+str(start),basis)
        types.update({r[0][':db/id']:jsonable(r[0]) for r in rows})
    (H/'types.json').write_text(json.dumps(types,indent=2)+'\n');proposals=[];excluded=[]
    for r in potential:
        if r['attribute']=='answer/value':
            kind=types[r['entity']].get(':answer/type',{}).get(':db/ident')
            r['after']=fix(r['before']) if kind==':answer.type/math' else prose(r['before']) if kind==':answer.type/text' else r['before']
        if r['attribute']=='answer-field/key':
            kind=types[r['entity']].get(':answer-field/type',{}).get(':db/ident')
            if kind!=':answer-field.type/checkbox':
                excluded.append({**r,'reason':'Non-checkbox key may be a response placeholder; inspect separately'});continue
        if r['after']==r['before']:continue
        assert skeleton(r['before'])==skeleton(r['after']),(r['entity'],r['attribute'])
        assert (fix(r['after']) if r['attribute']=='answer/value' and types[r['entity']].get(':answer/type',{}).get(':db/ident')==':answer.type/math' else prose(r['after']))==r['after']
        proposals.append(r)
    (H/'proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');(H/'excluded.json').write_text(json.dumps(excluded,indent=2)+'\n')
    report={'passed':not excluded,'basis':basis,'all_content_fields_scanned':sum(scanned.values()),'by_attribute_scanned':dict(scanned),
        'repair_fields':len(proposals),'repair_entities':len({r['entity'] for r in proposals}),
        'by_attribute_repaired':dict(Counter(r['attribute'] for r in proposals)),'excluded_for_review':len(excluded),
        'only_fence_sizing_equivalent_angle_spelling_and_spacing_changed':True,'idempotent':True}
    (H/'audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()

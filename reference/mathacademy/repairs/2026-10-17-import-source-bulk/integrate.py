"""Merge independently source-bound edits without changing untouched field text."""
import argparse, copy, hashlib, json, sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--layout',action='store_true');args=parser.parse_args()
    snapshot=Path((HERE/'snapshot-directory.txt').read_text().strip())
    current={e[':db/id']:e for e in json.loads((snapshot/'entities.json').read_text())}
    merged={};inputs={};resolved_overlaps=[]
    input_paths=[(name,HERE/name/'changes.json') for name in ('primary','secondary','manual')]
    input_paths.append(('manual-adjacent',HERE/'primary/adjacent-interval-changes.json'))
    for name,path in input_paths:
        inputs[str(path.relative_to(HERE))]=sha(path)
        data=json.loads(path.read_text());rows=data['changes'] if isinstance(data,dict) else data
        for row in rows:
            e,a=row['entity'],row['attribute'];assert a in (':tutorial/content',':question/problem',':question/worked-solution',':answer/value')
            assert row['before']==current[e][a],('Current value differs',e,a)
            edits=sorted(row['replacements'],key=lambda x:(x['start'],x['end']))
            value=row['before'];end=0
            for r in edits:
                assert 0<=end<=r['start']<r['end']<=len(value),(e,a,r)
                assert value[r['start']:r['end']]==r['before'],(e,a,'Span differs')
                assert r['before']!=r['after'] and r.get('source_occurrence_id'),(e,a,'Missing changed source span')
                end=r['end']
            for r in reversed(edits):value=value[:r['start']]+r['after']+value[r['end']:]
            assert value==row['after'],(e,a,'Unaccounted change')
            key=(e,a)
            if key not in merged:merged[key]={'entity':e,'attribute':a,'before':row['before'],'replacements':[],'queues':[]}
            dst=merged[key];dst['queues'].append(name)
            for r in edits:
                matches=[old for old in dst['replacements'] if r['start']<old['end'] and old['start']<r['end']]
                if matches:
                    same_span=len(matches)==1 and all(matches[0][k]==r[k] for k in ('start','end','before'))
                    if same_span and matches[0]['after']!=r['after'] and r['source_occurrence_id']=='3428:step-182411:340346':
                        assert name=='secondary' and matches[0].get('conversion',{}).get('manual_source_review')
                        resolved_overlaps.append({'entity':e,'attribute':a,'source_occurrence_id':r['source_occurrence_id'],'selected':'primary reviewed finite-set restoration','reason':'Generic source TeX treats intended set braces as grouping and hides them; preceding source definition confirms visible set braces.'})
                        continue
                    assert same_span and matches[0]['after']==r['after'],(e,a,'Conflicting edits',r['source_occurrence_id'],r['start'],r['end'])
                    matches[0].setdefault('source_occurrence_ids',[matches[0]['source_occurrence_id']])
                    if r['source_occurrence_id'] not in matches[0]['source_occurrence_ids']:matches[0]['source_occurrence_ids'].append(r['source_occurrence_id'])
                else:dst['replacements'].append(copy.deepcopy(r))
    layout_count=0
    if args.layout:
        path=HERE/'primary/layout-overrides.json';inputs[str(path.relative_to(HERE))]=sha(path)
        for override in json.loads(path.read_text()):
            key=override['entity'],override['attribute'];assert key in merged
            matches=[r for r in merged[key]['replacements'] if r['start']==override['start'] and r['end']==override['end'] and r['source_occurrence_id']==override['source_occurrence_id']]
            assert len(matches)==1 and matches[0]['after']==override['before_after'],('Layout input changed',key,override['source_occurrence_id'])
            matches[0]['after']=override['after'];matches[0]['layout_review']=override
            layout_count+=1
    changes=[]
    for key,row in sorted(merged.items()):
        value=row['before'];row['replacements'].sort(key=lambda x:x['start'])
        for r in reversed(row['replacements']):value=value[:r['start']]+r['after']+value[r['end']:]
        row['after']=value;row['before_sha256']=hashlib.sha256(row['before'].encode()).hexdigest();row['after_sha256']=hashlib.sha256(value.encode()).hexdigest()
        assert value!=row['before'];changes.append(row)
    result={'snapshot':str(snapshot),'identity':json.loads((snapshot/'identity.json').read_text()),'inputs':inputs,'changes':changes,'reviewed_overlap_resolutions':resolved_overlaps,
        'summary':{'fields':len(changes),'entities':len({r['entity'] for r in changes}),'attributes':dict(Counter(r['attribute'] for r in changes)),'source_replacements':sum(len(r['replacements']) for r in changes),'layout_overrides':layout_count}}
    write(HERE/'integrated-changes.json',result);print(json.dumps(result['summary'],indent=2))
if __name__=='__main__':main()

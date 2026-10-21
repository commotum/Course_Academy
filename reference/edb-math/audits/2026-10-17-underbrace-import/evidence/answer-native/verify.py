import sys
sys.dont_write_bytecode=True
from pathlib import Path
import collections,json,re
ROOT=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(ROOT))
from capture.scripts.database.edn import loads
HERE=Path(__file__).resolve().parent;E=HERE.parent
data=json.loads((E/'current-results.json').read_text());meta={r[':db/id']:r for r in json.loads((E/'metadata.json').read_text())}
for r in json.loads((E/'archive-current.json').read_text()):meta.setdefault(r[':db/id'],{}).update(r)
chars='⏟⏞︷︸';aids={1064:':tutorial/content',1071:':question/problem',1074:':question/worked-solution',1080:':answer/value',1081:':answer/feedback',1085:':multistep/context'}
current=[];history=[]
for attr in data:
    for e,v,tx,s in attr['rows']:
        if any(c in v for c in chars):current.append((e,attr['attribute'],v,tx,s))
for p in HERE.glob('history-*.edn'):
    for e,a,v,tx,s,added in loads(p.read_text()):history.append((e,aids[a],v,tx,s,added))
cur=set(current);hist=set(history);assert len(cur)==len(current);assert len(hist)==len(history)
cp={(e,a) for e,a,v,tx,s in cur};hp={(e,a) for e,a,v,tx,s,added in hist if added}
ce={e for e,a in cp};he={e for e,a in hp}
formerly_bad_fields=hp-cp;formerly_bad_entities=he-ce
history_adds={(e,a,v,tx,s) for e,a,v,tx,s,added in hist if added}
unexplained=cur-history_adds

def classify(e):
    m=meta.get(e,{})
    if ':tutorial/id' in m or ':tutorial/math-academy-id' in m:return 'tutorial'
    ma=m.get(':question/math-academy-id','')
    if ma.startswith('q-'):return 'practice_question'
    if ma.startswith('e-'):return 'canonical_example'
    if m.get(':knowledge-point/_canonical-example'):return 'canonical_example'
    if m.get(':knowledge-point/_questions'):return 'practice_question'
    if ':question/id' in m:return 'question_unknown_origin'
    return 'metadata_missing'

def totals(rows):
    occ=collections.Counter();shape=collections.Counter();unknown=[]
    for e,a,v,*_ in rows:
        for c in chars:occ[c]+=v.count(c)
        residual=v
        for name,pat in [('tex_under_subscript',r'_\{⏟\}'),('tex_over_overset',r'\\overset\{⏞\}'),('ascii_under_subscript',r'_\(⏟\)'),('ascii_over_superscript',r'\^\(⏞\)')]:
            matches=list(re.finditer(pat,residual));shape[name]+=len(matches);residual=re.sub(pat,'',residual)
        if any(c in residual for c in chars):unknown.append({'entity':e,'attribute':a,'residual':residual})
    return {'occurrences_by_glyph':dict(occ),'occurrence_count':sum(occ.values()),'shape_counts':dict(shape),'unclassified':unknown,'exhaustive':not unknown}

current_by_attr={a:{'fields':len({e for e,at in cp if at==a}),'occurrences':sum(sum(v.count(c) for c in chars) for e,at,v,tx,s in cur if at==a)} for a in sorted({a for e,a in cp})}
history_by_attr={a:{'ever_affected_fields':len({e for e,at in hp if at==a}),'historical_rows':sum(at==a for e,at,v,tx,s,added in hist),'historical_assertion_rows':sum(at==a and added for e,at,v,tx,s,added in hist),'historical_retraction_rows':sum(at==a and not added for e,at,v,tx,s,added in hist)} for a in sorted({a for e,a in hp})}
result={'basis':3625,'database_reads_performed_by_this_verifier':0,'current':{'affected_attributes':len(cp),'affected_entities':len(ce),'matching_datom_rows':len(cur),'unique_entity_types':dict(collections.Counter(classify(e) for e in ce)),'by_attribute':current_by_attr,**totals(cur)},'history':{'ever_affected_attributes':len(hp),'ever_affected_entities':len(he),'matching_datom_rows':len(hist),'matching_assertion_rows':sum(added for e,a,v,tx,s,added in hist),'matching_retraction_rows':sum(not added for e,a,v,tx,s,added in hist),'by_attribute':history_by_attr,'unique_entity_types':dict(collections.Counter(classify(e) for e in he)),**totals(hist)},'formerly_bad':{'currently_clean_entities':len(formerly_bad_entities),'currently_clean_fields':len(formerly_bad_fields),'entity_ids':sorted(formerly_bad_entities),'fields':sorted(formerly_bad_fields),'unique_entity_types':dict(collections.Counter(classify(e) for e in formerly_bad_entities))},'current_malformed_assertions_absent_from_history':sorted(unexplained),'all_current_malformed_assertions_present_in_history':not unexplained,'missing_metadata_entity_ids':sorted(he-set(meta))}
assert not unexplained
assert result['current']['exhaustive']
assert result['history']['exhaustive']
(HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:({kk:vv for kk,vv in v.items() if kk not in ['fields','entity_ids','unclassified']} if isinstance(v,dict) else v) for k,v in result.items()},ensure_ascii=False,indent=2))

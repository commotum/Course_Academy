"""Produce current and historical inventories from the pinned read-only evidence."""
import collections,csv,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from capture.scripts.database.edn import loads
HERE=Path(__file__).resolve().parent;E=HERE/'evidence'
META={r[':db/id']:r for r in json.loads((E/'all-metadata.json').read_text())}
ATTRS={a:str(i) for a,i in loads((E/'string-attributes.edn').read_text())}
RESULTS=json.loads((E/'current-results.json').read_text())

def save(name,value):
 (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def nested(v,key):
 if isinstance(v,dict):
  if key in v:yield v
  for x in v.values():yield from nested(x,key)
 elif isinstance(v,list):
  for x in v:yield from nested(x,key)
def info(e):
 m=META[e]
 return {'entity':e,'source_id':m.get(':question/math-academy-id','tutorial-'+str(m[':tutorial/math-academy-id']) if ':tutorial/math-academy-id' in m else None),
 'kind':'tutorial' if ':tutorial/id' in m else 'canonical-example' if m.get(':question/math-academy-id','').startswith('e-') else 'practice-question' if ':question/math-academy-id' in m else 'other',
 'title':m.get(':tutorial/title'),
 'topics':sorted({t[':db/id']:{'entity':t[':db/id'],'source_id':t[':topic/math-academy-id'],'title':t[':topic/title']} for t in nested(m,':topic/title')}.values(),key=lambda t:t['entity']),
 'knowledge_points':sorted({k[':db/id'] for k in nested(m,':knowledge-point/title')})}
def signatures(s):
 out=[]
 for m in re.finditer('[⏟⏞︷︸]',s):
  l=s[max(0,m.start()-20):m.start()];r=s[m.end():m.end()+10]
  if l.endswith('_{') and r.startswith('}') and m[0]=='⏟':kind='underbrace-as-subscript'
  elif l.endswith('\\overset{') and r.startswith('}') and m[0]=='⏞':kind='overbrace-as-overset'
  elif l.endswith('_(') and r.startswith(')') and m[0]=='⏟':kind='flattened-underbrace'
  elif l.endswith('^(') and r.startswith(')') and m[0]=='⏞':kind='flattened-overbrace'
  else:raise AssertionError(('unclassified',m[0],l,r))
  out.append({'offset':m.start(),'signature':kind,'excerpt':s[max(0,m.start()-95):m.end()+65]})
 return out

current=[]
for r in RESULTS:
 for e,v,tx,src in r['rows']:
  sig=signatures(v)
  if sig:current.append({**info(e),'attribute':r['attribute'],'value':v,'assertion_tx':tx,'source_entity':src,'occurrences':sig})
assert len({(r['entity'],r['attribute']) for r in current})==len(current)
current.sort(key=lambda r:(r['entity'],r['attribute']))
save('current-affected.json',current)

hist=[]
for p in (E/'answer-native').glob('history-*.edn'):
 for e,a,v,tx,src,added in loads(p.read_text()):hist.append((e,ATTRS[a],v,tx,src,added))
hf=collections.defaultdict(list)
for e,a,v,tx,src,added in hist:hf[e,a].append({'value':v,'tx':tx,'source_entity':src,'added':added})
cf={(r['entity'],r['attribute']) for r in current};ce={e for e,a in cf}
history=[]
for (e,a),versions in sorted(hf.items()):
 history.append({**info(e),'attribute':a,'still_affected':(e,a) in cf,'first_bad_assertion_tx':min(x['tx'] for x in versions if x['added']),
 'last_bad_assertion_tx':max(x['tx'] for x in versions if x['added']),'bad_assertions':sum(x['added'] for x in versions),'bad_retractions':sum(not x['added'] for x in versions),
 'historical_value_variants':len({x['value'] for x in versions})})
assert cf<=set(hf)
save('historically-affected.json',history)
clean=sorted({r['entity'] for r in history}-ce)
save('historical-only.json',[info(e) for e in clean])

def tsv(name,rows,history=False):
 with (HERE/name).open('w') as f:
  w=csv.writer(f,delimiter='\t');w.writerow(['entity','attribute','kind','source_id','topic_ids','lesson_titles','knowledge_points','brace_occurrences' if not history else 'still_affected','snippet' if not history else 'historical_value_variants'])
  for r in rows:
   w.writerow([r['entity'],r['attribute'],r['kind'],r['source_id'],','.join(str(t['entity']) for t in r['topics']),' | '.join(t['title'] for t in r['topics']),','.join(map(str,r['knowledge_points'])),r['still_affected'] if history else len(r['occurrences']),r['historical_value_variants'] if history else r['occurrences'][0]['excerpt'].replace('\n',' ')])
tsv('current-affected.tsv',current);tsv('historically-affected.tsv',history,True)

lessons={}
for r in current:
 for t in r['topics']:
  x=lessons.setdefault(t['entity'],{**t,'affected_entities':set(),'affected_fields':[],'brace_occurrences':0})
  x['affected_entities'].add(r['entity']);x['affected_fields'].append([r['entity'],r['attribute']]);x['brace_occurrences']+=len(r['occurrences'])
for x in lessons.values():x['affected_entities']=sorted(x['affected_entities']);x['entity_count']=len(x['affected_entities']);x['field_count']=len(x['affected_fields'])
lesson_rows=sorted(lessons.values(),key=lambda x:(-x['entity_count'],x['title']));save('lessons.json',lesson_rows)
with (HERE/'lessons.tsv').open('w') as f:
 w=csv.writer(f,delimiter='\t');w.writerow(['topic_entity','topic_source_id','title','affected_items','affected_fields','malformed_braces','entity_ids'])
 for x in lesson_rows:w.writerow([x['entity'],x['source_id'],x['title'],x['entity_count'],x['field_count'],x['brace_occurrences'],','.join(map(str,x['affected_entities']))])

original=json.loads((E/'archive-current.json').read_text())
summary={
 'database':json.loads((E/'status.json').read_text()),'database_writes':0,
 'current_scanned_string_attributes':len(RESULTS),'current_content_fields_scanned':sum(r['total_fields'] for r in RESULTS if r['attribute'] in [':tutorial/content',':question/problem',':question/worked-solution',':answer/value',':answer/feedback',':multistep/context']),
 'current':{'affected_entities':len(ce),'affected_fields':len(current),'lessons':len(lessons),'malformed_braces':sum(len(r['occurrences']) for r in current),
 'entities_by_kind':dict(collections.Counter(info(e)['kind'] for e in ce)),
 'fields_by_attribute':dict(collections.Counter(r['attribute'] for r in current)),
 'occurrences_by_signature':dict(collections.Counter(s['signature'] for r in current for s in r['occurrences'])),
 'unmapped_entities':sorted(e for e in ce if not info(e)['topics']),
 'answer_values_scanned':json.loads((E/'answer-native/stats.json').read_text())['current_datoms'],'affected_answer_values':0,'affected_feedback':0,'affected_multistep_contexts':0},
 'history':{'affected_entities':len({r['entity'] for r in history}),'affected_fields':len(history),'affected_lessons':len({t['entity'] for r in history for t in r['topics']}),'matching_events':len(hist),'currently_clear_entities':len(clean),'currently_clear_fields':len(set(hf)-cf)},
 'original_archive':{'affected_items':len(original),'currently_affected':sum(any('⏟' in v or '⏞' in v for v in r.values() if isinstance(v,str)) for r in original),'currently_clear':sum(not any('⏟' in v or '⏞' in v for v in r.values() if isinstance(v,str)) for r in original)},
 'verification':{'all_current_bad_fields_in_retained_history':cf<=set(hf),'all_current_signatures_classified':True,'all_current_entities_have_lesson':not any(not info(e)['topics'] for e in ce)}
}
save('summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))

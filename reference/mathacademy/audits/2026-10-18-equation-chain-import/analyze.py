"""Analyze the complete native snapshot without opening a database writer."""
import gzip,json,re
from collections import Counter,defaultdict
from pathlib import Path
from .patterns import HERE,detect,save,IDENTITY
CONTENT={':tutorial/content',':question/problem',':question/worked-solution',':answer/value',':answer/feedback'}
META={':topic/title',':topic/math-academy-id',':tutorial/title',':tutorial/math-academy-id',':question/math-academy-id'}
RELS={':topic/knowledge-points',':knowledge-point/questions',':knowledge-point/canonical-example',':question/answer-fields',':answer-field/choices',':answer-field/correct',':activity/scope',':activity/steps',':step/content'}
def run():
 meta=defaultdict(dict);rels={a:defaultdict(set) for a in RELS};fields={};counts=Counter()
 with ((HERE/'snapshot.jsonl').open() if (HERE/'snapshot.jsonl').exists() else gzip.open(HERE/'snapshot.jsonl.gz','rt')) as stream:
  for line in stream:
   r=json.loads(line);e=r['e'];a=':'+r['a'];v=r['raw_string'] if r['raw_string'] is not None else r['ref_eid'] if r['ref_eid'] is not None else r['uuid'] if r['uuid'] is not None else int(r['value_edn']) if re.fullmatch(r'-?\d+',r['value_edn']) else r['value_edn']
   if a in CONTENT:
    counts[a]+=1
    key=(e,a)
    if key not in fields:fields[key]={'entity':e,'attribute':a,'value':v,'provenance':[]}
    assert fields[key]['value']==v
    fields[key]['provenance'].append({'tx':r['tx'],'source':r['source']})
   elif a in META:meta[e][a]=v
   elif a in RELS:rels[a][e].add(v)
 def reverse(a):
  d=defaultdict(set)
  for left,values in rels[a].items():
   for right in values:d[right].add(left)
  return d
 kp_topics=reverse(':topic/knowledge-points');q_kps=reverse(':knowledge-point/questions')
 for q,kps in reverse(':knowledge-point/canonical-example').items():q_kps[q].update(kps)
 a_fields=reverse(':answer-field/choices')
 for a,fs in reverse(':answer-field/correct').items():a_fields[a].update(fs)
 f_qs=reverse(':question/answer-fields');step_activities=reverse(':activity/steps');content_steps=reverse(':step/content')
 findings=[];bytopic={}
 for (e,a),field in fields.items():
  reasons,details=detect(field['value'],a==':answer/value')
  if not reasons:continue
  qs={e} if a.startswith(':question/') else {q for f in a_fields[e] for q in f_qs[f]} if a.startswith(':answer/') else set()
  topics={t for q in qs for kp in q_kps[q] for t in kp_topics[kp]}
  for step in content_steps[e]:
   for activity in step_activities[step]:topics.update(rels[':activity/scope'][activity])
  ts=[{':db/id':t,**meta[t]} for t in sorted(topics)]
  item={**field,'reasons':reasons,'details':details,'confirmed_pattern':any(r!='legacy-eqalign' for r in reasons),'lessons':ts,'source_id':meta[e].get(':tutorial/math-academy-id',meta[e].get(':question/math-academy-id')),'owning_questions':sorted(qs)};findings.append(item)
  for topic in ts:
   t=bytopic.setdefault(topic[':db/id'],{**topic,'confirmed_fields':0,'legacy_only_fields':0,'findings':[]})
   t['confirmed_fields' if item['confirmed_pattern'] else 'legacy_only_fields']+=1;t['findings'].append({'entity':e,'attribute':a,'reasons':reasons,'confirmed_pattern':item['confirmed_pattern']})
 lessons=sorted(bytopic.values(),key=lambda t:(-t['confirmed_fields'],-t['legacy_only_fields'],t[':db/id']))
 export=json.loads((HERE/'snapshot.manifest.json').read_text());summary={**IDENTITY,'all_content_attribute_counts':export['all_content_attribute_counts'],'candidate_field_counts':dict(counts),'fields_with_patterns':len(findings),'confirmed_pattern_fields':sum(f['confirmed_pattern'] for f in findings),'legacy_only_fields':sum(not f['confirmed_pattern'] for f in findings),'entities':len({f['entity'] for f in findings}),'reason_counts':dict(Counter(reason for f in findings for reason in f['reasons'])),'lessons_with_confirmed_patterns':sum(t['confirmed_fields']>0 for t in lessons),'lessons_with_legacy_only':sum(t['confirmed_fields']==0 for t in lessons),'unmapped_fields':sum(not f['lessons'] for f in findings),'database_writes':0}
 save('findings.json',findings);save('lessons.json',lessons);save('summary.json',summary)
 print(json.dumps(summary,indent=2));print('TOP LESSONS',json.dumps([{k:v for k,v in t.items() if k!='findings'} for t in lessons[:22]],indent=2))
if __name__=='__main__':run()

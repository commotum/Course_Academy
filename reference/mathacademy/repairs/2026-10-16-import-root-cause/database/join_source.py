"""Join reviewed source-loss occurrences to exact unchanged original fields.

This is a read-only repair-candidate queue, not an edit script. Whole-field
equality guards against overwriting intervening captures/repairs. A matching
formula is evidence of a loss class, never permission for global replacement.
"""
from pathlib import Path
import argparse,collections,csv,gzip,hashlib,json,re,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import MATH
SOURCE=HERE.parent/'source/primary-mixed-title.jsonl'

def save(name,data):
 (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def jsonl(name,rows):
 with (HERE/name).open('w') as f:
  for row in rows:f.write(json.dumps(row,ensure_ascii=False)+'\n')
def strip_math(value):
 value=value.strip()
 for left,right in [('$$','$$'),(r'\[',r'\]'),(r'\(',r'\)'),('$','$')]:
  if value.startswith(left) and value.endswith(right):return value[len(left):-len(right)].strip()
 return value
def norm(value):return re.sub(r'\s+','',strip_math(value))
def formulas(text,attribute):
 result=[norm(m.group()) for m in MATH.finditer(text)]
 if attribute==':answer/value':result.append(norm(text))
 return result

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--secondary',action='store_true');args=parser.parse_args()
 source_path=SOURCE if not args.secondary else HERE.parent/'source/occurrences.jsonl'
 prefix='' if not args.secondary else 'secondary-'
 original=[];index=collections.defaultdict(list)
 baseline=HERE/'baseline-comparison.jsonl'
 for line in (baseline.open() if baseline.exists() else gzip.open(str(baseline)+'.gz','rt')):
  row=json.loads(line);original.append(row)
  for topic in row['original_topic_ids']:index[(topic,str(row['source_id']),row['attribute'])].append(row)
 raw=source_path.read_bytes();all_occurrences=[json.loads(line) for line in raw.splitlines() if line]
 if args.secondary:
  occurrences=[]
  for row in all_occurrences:
   mechanisms=[m for m in row.get('mechanisms',[]) if m['code']!='mixed-title-first-fragment']
   if not mechanisms:continue
   attrs={m['attribute'] for m in row.get('stored_json_matches',[])}
   if not row.get('legacy_output_confirmed_in_archived_json') or len(attrs)!=1 or row['attribute'] not in attrs:continue
   occurrences.append({**row,'mechanisms':mechanisms})
 else:occurrences=all_occurrences
 candidate=[];review=[];unmapped=[];field_rows={}
 for source in occurrences:
  mapped=index.get((source['topic_id'],str(source['source_id']),source['attribute']),[])
  info={k:source[k] for k in ['id','topic_id','topic_title','kind','source_id','attribute','source_file','source_line','source_offset','source_title_index','legacy_text','legacy_markdown','stored_json_matches','mechanisms'] if k in source}
  if not mapped:unmapped.append({**info,'classification':'no-original-field-mapping'});continue
  expected=formulas(source['legacy_markdown'],source['attribute'])
  if not expected:expected=[norm(source['legacy_markdown'])]
  matched=[r for r in mapped if any(e and e in formulas(r['original_value'],r['attribute']) for e in expected)]
  if not matched:
   review.append({**info,'classification':'source-loss-original-render-not-anchored',
    'mapped_fields':[{'entity':r['entity'],'attribute':r['attribute'],'comparison':r['comparison'],'uuid':r['uuid']} for r in mapped]})
   continue
  for record in matched:
   item={**info,'entity':record['entity'],'uuid':record['uuid'],'original_file':record['original_file'],
    'original_file_sha256':record['original_file_sha256'],'original_sha256':record['original_sha256'],
    'current_sha256':record['current_sha256'],'comparison':record['comparison'],'context':record.get('current_context')}
   if record['comparison']=='unchanged-original':
    item['classification']='source-backed-candidate-original-field-unchanged'
    candidate.append(item);key=(record['entity'],record['attribute'])
    if key not in field_rows:field_rows[key]={'entity':record['entity'],'attribute':record['attribute'],
      'uuid':record['uuid'],'current_value':record['original_value'],'current_sha256':record['current_sha256'],
      'context':record['current_context'],'source_occurrences':[],'classification':'source-backed-candidate-original-field-unchanged'}
    field_rows[key]['source_occurrences'].append(item)
   else:
    item['classification']='intervening-change-requires-contextual-review' if record['comparison']=='changed-since-original' else 'current-content-absent'
    review.append(item)
 fields=[field_rows[key] for key in sorted(field_rows)]
 jsonl(prefix+'source-backed-candidates.jsonl',fields);jsonl(prefix+'source-comparison-review.jsonl',review);jsonl(prefix+'source-unmapped.jsonl',unmapped)
 field_review={}
 for row in candidate+review:
  if row.get('entity') is None:continue
  key=(row['entity'],row['attribute'])
  item=field_review.setdefault(key,{'entity':row['entity'],'attribute':row['attribute'],'state':row['classification'],
   'source_ids':set(),'source_topic_ids':set(),'current_topic_entities':set(),'mechanisms':set(),'source_occurrences':set()})
  item['source_ids'].add(str(row['source_id']));item['source_topic_ids'].add(row['topic_id'])
  item['current_topic_entities'].update((row.get('context') or {}).get('topic_ids',[]))
  item['mechanisms'].update(m['code'] for m in row.get('mechanisms',[]));item['source_occurrences'].add(row['id'])
 field_review=[{k:sorted(v) if isinstance(v,set) else v for k,v in row.items()} for key,row in sorted(field_review.items())]
 save(prefix+'affected-fields.json',field_review)
 with (HERE/(prefix+'affected-fields.csv')).open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=['entity','attribute','state','source_ids','source_topic_ids','current_topic_entities','mechanisms','source_occurrences']);writer.writeheader()
  for row in field_review:writer.writerow({k:';'.join(map(str,v)) if isinstance(v,list) else v for k,v in row.items()})
 lessons=collections.defaultdict(lambda:collections.defaultdict(set))
 for row in field_review:
  for topic in row['source_topic_ids']:lessons[topic][row['state']].add((row['entity'],row['attribute']))
 save(prefix+'affected-lessons.json',[{'source_topic_id':topic,'states':{state:len(keys) for state,keys in sorted(states.items())},'fields':sorted({key for keys in states.values() for key in keys})} for topic,states in sorted(lessons.items())])
 mechanism_fields=collections.defaultdict(set)
 for row in candidate:
  for code in {m['code'] for m in row['mechanisms']}:mechanism_fields[code].add((row['entity'],row['attribute']))
 summary={**json.loads((HERE/'identity.json').read_text()),'source_stream':str(source_path),
  'source_stream_sha256':hashlib.sha256(raw).hexdigest(),'source_occurrences':len(occurrences),
  'unchanged_original_candidate_occurrences':len(candidate),'unchanged_original_candidate_fields':len(fields),
  'unchanged_original_candidate_entities':len({r['entity'] for r in fields}),
  'unchanged_original_candidate_source_topics':len({r['topic_id'] for r in candidate}),
  'candidate_fields_by_attribute':dict(collections.Counter(r['attribute'] for r in fields)),
  'candidate_fields_by_mechanism':{code:len(keys) for code,keys in sorted(mechanism_fields.items())},
  'mechanism_counts_overlap':True,
  'review_occurrences':len(review),'review_classifications':dict(collections.Counter(r['classification'] for r in review)),
  'unmapped_occurrences':len(unmapped),'evidence_rule':'Source detector confirms the legacy fragment in archived source JSON; original imported rendered math contains that exact normalized math body; the complete current field equals the complete archived imported field byte for byte.',
  'limitations':['Source class negative controls must be reviewed before calling candidates semantic corruption.',
   'Changed fields are not assumed repaired; they require contextual source alignment.',
   'Repeated equal formulas must be addressed by source ordinal/context, never blind text replacement.',
   'No semantic conclusion or repair follows solely from syntax regex flags.'],
  'database_mutations':0}
 save(prefix+'source-comparison-summary.json',summary);print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main()

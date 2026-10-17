"""Audit the pinned native export against original committed import forms.

No database connection or mutation. Preserves a strict distinction between
source-backed candidates, changed fields requiring review, and syntax flags.
"""
from pathlib import Path
import collections,gzip,hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.edn import loads
from scripts.question_capture.math_format import MATH,legacy_system_rows
CONTENT={':tutorial/content',':question/problem',':question/worked-solution',':answer/value'}
RELATIONS={':topic/knowledge-points',':knowledge-point/questions',':knowledge-point/canonical-example',
 ':question/answer-fields',':answer-field/choices',':answer-field/correct',':activity/scope',':activity/steps',':step/content'}
IMPORT=Path('/media/jake/SSD/EDB/math/imports/math-academy/MA-Content')

def save(name,value):
 (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str)+'\n')
def jsonl(name,rows):
 with (HERE/name).open('w') as f:
  for row in rows:f.write(json.dumps(row,ensure_ascii=False,default=str)+'\n')
def digest(value):return hashlib.sha256(value.encode()).hexdigest()
def scan_native():
 metadata=collections.defaultdict(dict);relations=collections.defaultdict(list);facts={};counts=collections.Counter()
 native=HERE/'native.jsonl'
 with (native.open() if native.exists() else gzip.open(HERE/'native.jsonl.gz','rt')) as f:
  for line in f:
   row=json.loads(line);attr=':'+row['a'];entity=row['e'];counts[attr]+=1
   value=row['raw_string'] if row['raw_string'] is not None else row['uuid'] if row['uuid'] is not None else row['ref_eid'] if row['ref_eid'] is not None else loads(row['value_edn'])
   if attr in CONTENT:
    key=(entity,attr)
    if key in facts:assert facts[key]['value']==value,('Multiple distinct current content values',key)
    else:facts[key]={'entity':entity,'attribute':attr,'value':value,'sha256':digest(value),'provenance':[]}
    facts[key]['provenance'].append({'transaction':row['tx'],'source':row['source']})
   elif attr in RELATIONS:relations[attr].append([entity,value])
   else:
    if attr in metadata[entity]:assert metadata[entity][attr]==value
    metadata[entity][attr]=value
 jsonl('content.jsonl',(facts[k] for k in sorted(facts)))
 save('entities.json',metadata);save('relations.json',relations)
 return metadata,relations,facts,counts

def ownership(metadata,relations):
 def forward(attr):
  result=collections.defaultdict(set)
  for a,b in relations[attr]:result[a].add(b)
  return result
 def reverse(attr):
  result=collections.defaultdict(set)
  for a,b in relations[attr]:result[b].add(a)
  return result
 kp_topics=reverse(':topic/knowledge-points');q_kps=reverse(':knowledge-point/questions')
 for q,kps in reverse(':knowledge-point/canonical-example').items():q_kps[q].update(kps)
 answer_fields=reverse(':answer-field/choices')
 for a,fields in reverse(':answer-field/correct').items():answer_fields[a].update(fields)
 field_questions=reverse(':question/answer-fields');step_activities=reverse(':activity/steps');activity_topics=forward(':activity/scope')
 tutorial_topics=collections.defaultdict(set)
 for step,content in relations[':step/content']:
  if ':tutorial/id' not in metadata.get(content,{}):continue
  for activity in step_activities[step]:tutorial_topics[content].update(activity_topics[activity])
 def context(entity,attr):
  fields=answer_fields.get(entity,set()) if attr==':answer/value' else set()
  questions={q for f in fields for q in field_questions[f]} if fields else {entity} if attr.startswith(':question/') else set()
  kps={kp for q in questions for kp in q_kps[q]}
  topics={t for kp in kps for t in kp_topics[kp]} | tutorial_topics.get(entity,set())
  return {'source_id':metadata.get(entity,{}).get(':tutorial/math-academy-id') if attr==':tutorial/content' else metadata.get(entity,{}).get(':question/math-academy-id'),
   'question_ids':sorted(questions),'answer_field_ids':sorted(fields),
   'question_source_ids':sorted({metadata[q][':question/math-academy-id'] for q in questions if ':question/math-academy-id' in metadata.get(q,{})}),
   'kp_ids':sorted(kps),'topic_ids':sorted(topics),
   'topics':[{'entity':t,'math_academy_id':metadata.get(t,{}).get(':topic/math-academy-id'),'title':metadata.get(t,{}).get(':topic/title')} for t in sorted(topics)]}
 return context

def baseline(metadata,facts,context):
 identities={(attr,str(value)):entity for entity,attrs in metadata.items() for attr,value in attrs.items() if attr in {':question/id',':tutorial/id',':answer/id'}}
 manifest=json.loads((IMPORT/'manifest.json').read_text());rows=[];archive=[]
 for batch in manifest['batches']:
  if batch.get('group')!='archived MA lessons':continue
  path=IMPORT/batch['file'];raw=path.read_bytes();actual=hashlib.sha256(raw).hexdigest();assert actual==batch['sha256'],('Archived import changed',path)
  forms=loads(raw.decode());refs={f[':db/id']:f for f in forms if isinstance(f,dict) and isinstance(f.get(':db/id'),str)}
  ref_topics=collections.defaultdict(set);ref_kps=collections.defaultdict(set)
  for form in forms:
   if ':topic/knowledge-points' in form:
    topic=form[':db/id'][1]
    for kp in form[':topic/knowledge-points']:
     ref_topics[kp].add(topic);k=refs[kp]
     for q in k.get(':knowledge-point/questions',[])+[k[':knowledge-point/canonical-example']]:
      ref_topics[q].add(topic);ref_kps[q].add(kp)
   if ':activity/steps' in form and ':activity/scope' in form:
    topic=form[':activity/scope'][1]
    for step in form[':activity/steps']:ref_topics[refs[step][':step/content']].add(topic)
  def add(form,kind,attr,owner=None):
   uuid=str(form[':'+kind+'/id']);entity=identities.get((':'+kind+'/id',uuid));value=form[attr]
   owner=owner or form;ref=owner.get(':db/id');source_id=owner.get(':tutorial/math-academy-id',owner.get(':question/math-academy-id'))
   if source_id is None and isinstance(ref,str) and ref.startswith('question-'):source_id='q-'+ref.rsplit(':',1)[-1].removeprefix('question-')
   current=facts.get((entity,attr))
   row={'kind':kind,'uuid':uuid,'entity':entity,'attribute':attr,'source_id':source_id,
    'original_owner_ref':ref,'original_topic_ids':sorted(ref_topics[ref]),'original_kp_refs':sorted(ref_kps[ref]),
    'original_file':str(path),'original_file_sha256':actual,'original_value':value,'original_sha256':digest(value),
    'current_sha256':current['sha256'] if current else None,
    'comparison':'unchanged-original' if current and value==current['value'] else 'changed-since-original' if current else 'current-field-absent' if entity is not None else 'current-entity-absent'}
   if current:row['current_context']=context(entity,attr)
   if kind=='answer':row['original_question_uuid']=str(owner[':question/id'])
   rows.append(row)
  for form in forms:
   for attr in CONTENT- {':answer/value'}:
    if attr in form:add(form,'tutorial' if attr.startswith(':tutorial/') else 'question',attr)
   for field in form.get(':question/answer-fields',[]):
    for answer in field.get(':answer-field/choices',[]):add(answer,'answer',':answer/value',form)
  archive.append({'path':str(path),'sha256':actual,'bytes':len(raw),'old_basis':batch['old_basis']})
 jsonl('baseline-comparison.jsonl',rows)
 save('archived-import-manifest.json',{'path':str(IMPORT/'manifest.json'),'sha256':hashlib.sha256((IMPORT/'manifest.json').read_bytes()).hexdigest(),'batches':archive})
 return rows

def syntax_candidates(facts,context):
 rows=[]
 for fact in facts.values():
  value=fact['value'];reasons=[]
  if re.search(r'\[(?:MATH|IMG|Missing image):',value):reasons.append('unresolved-source-placeholder')
  if re.search(r'<(?:mjx-container|math|svg)\b',value):reasons.append('raw-math-html')
  if re.search(r'&lt;!--|\\<\!--|<!--',value):reasons.append('html-comment-marker')
  expressions=[m.group() for m in MATH.finditer(value)]
  if fact['attribute']==':answer/value':expressions.append(value)
  for expression in expressions:
   for left,right in [('$$','$$'),(r'\[',r'\]'),(r'\(',r'\)'),('$','$')]:
    if expression.startswith(left) and expression.endswith(right):expression=expression[len(left):-len(right)];break
   if re.search(r'(?<!\\)%[^\n]*(?:\\(?:begin|end|frac|sqrt)|[=+])',expression):reasons.append('tex-comment-may-hide-content')
   if legacy_system_rows(expression):reasons.append('legacy-flattened-system')
   if re.search(r'\[[^\[\]\n]*\|[^\[\]\n]*;[^\[\]\n]*\]',expression):reasons.append('legacy-flattened-matrix')
  if reasons:rows.append({**{k:v for k,v in fact.items() if k!='value'},'classification':'syntax-candidate-not-proven-corruption','reasons':sorted(set(reasons)),'context':context(fact['entity'],fact['attribute']),'value':value})
 jsonl('syntax-candidates.jsonl',rows)
 return rows

def main():
 metadata,relations,facts,counts=scan_native();context=ownership(metadata,relations)
 originals=baseline(metadata,facts,context);syntax=syntax_candidates(facts,context)
 summary={**json.loads((HERE/'identity.json').read_text()),'scope':'All current facts for the selected content and ownership attributes; no course, topic or source restriction.',
  'content_fields':len(facts),'content_entities':len({e for e,a in facts}),
  'content_fields_by_attribute':dict(collections.Counter(a for e,a in facts)),
  'metadata_counts':dict(counts),'original_import_fields':len(originals),
  'original_comparisons':dict(collections.Counter(r['comparison'] for r in originals)),
  'original_comparisons_by_attribute':{a:dict(collections.Counter(r['comparison'] for r in originals if r['attribute']==a)) for a in sorted(CONTENT)},
  'syntax_candidate_fields':len(syntax),'syntax_reasons':dict(collections.Counter(reason for r in syntax for reason in r['reasons'])),
  'missing_solutions':'Not authored or classified as corruption; absent values are outside this content export.',
  'database_mutations':0}
 save('audit-summary.json',summary);print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main()

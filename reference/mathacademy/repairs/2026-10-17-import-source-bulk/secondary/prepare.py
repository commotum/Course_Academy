"""Produce complete classified secondary queue and anchored repair proposals."""
from pathlib import Path
import collections,hashlib,importlib.util,json,re,sys,time
HERE=Path(__file__).resolve().parent;BULK=HERE.parent;AUDIT=BULK.parent/'2026-10-16-import-root-cause'
sys.path.insert(0,str(HERE));import convert_source as conv
sys.path.insert(0,str(BULK/'primary'));import position_map as pm
from scripts.question_capture.math_format import MATH
rows=[json.loads(l) for l in (AUDIT/'database/secondary-source-backed-candidates.jsonl').read_text().splitlines()]
entities={r[':db/id']:r for r in json.loads((BULK/'snapshot-3482/entities.json').read_text())}
def digest(v):return hashlib.sha256(v.encode()).hexdigest()
def norm(v):return re.sub(r'\s+','',pm.scan.md.math_to_markdown(v,display=False))
def stripped(v):
 for a,b in [('$$','$$'),('\\[','\\]'),('\\(','\\)'),('$','$')]:
  if v.startswith(a) and v.endswith(b):return v[len(a):-len(b)].strip()
 return v

def wrap(tex,before,answer_type):
 if answer_type==':answer.type/math':return tex
 for a,b in [('$$','$$'),('\\[','\\]'),('\\(','\\)'),('$','$')]:
  if before.startswith(a) and before.endswith(b):return a+ ('\n'+tex+'\n' if a in ('$$','\\[') else tex)+b
 matches=list(MATH.finditer(before))
 if len(matches)==1 and matches[0].start()==0 and re.fullmatch(r'[,.;:?!]*',before[matches[0].end():]):
  suffix=before[matches[0].end():]
  if suffix:
   tail=re.sub(r'(?:\\right\.|\\end\{(?:array|aligned|cases)\}|[}\s])+$','',tex)
   if tail.endswith(suffix):suffix='' # Source already carries the visible punctuation.
   elif tex.rstrip().endswith(suffix) and not tex.rstrip().endswith(r'\right.'):
    tex=tex.rstrip()[:-len(suffix)].rstrip()
  return wrap(tex,matches[0][0],answer_type)+suffix
 raise ValueError('Target is not delimited math')

def answer_identity(row):
 # An answer/value is itself exactly one mathematical object; source choice
 # identity must uniquely map to this rendered value in its original owner.
 o=pm.sources[row['source_occurrences'][0]['id']]
 item=json.loads(Path(o['source_file']).with_suffix('.json').read_text())['lesson']['items']
 item=next(x for x in item if x['dom_id']==o['dom_id'])
 # Recover the exact archived choice identity, including choices deduplicated
 # by the original importer. The UUID binds ordinal; matching text does not.
 qid=str(item['question_id']);identities=[]
 for qkey in (qid,str(o['topic_id'])+':'+qid):
  for index,choice in enumerate(item.get('choices',[]),1):
   if str(pm.seed.ident('answer',f'{qkey}:1:{index}'))==row['uuid']:
    original=pm.render_item(item,o['topic_id'],':answer/value')[index-1][0][1]
    identities.append((f'choices/{index-1}',original))
  for index,select in enumerate(item.get('select_lists',[]),1):
   for cindex,choice in enumerate(select['options'],1):
    if str(pm.seed.ident('answer',f'{qkey}:{index}:{cindex}'))==row['uuid']:
     ctx=pm.md.MarkdownContext(image_resolver=pm.md.LessonImageResolver(str(o['topic_id']),pm.md.DEFAULT_LESSONS_ROOT),standalone_math_display=False)
     original=stripped(pm.md.render_select_option_markdown(choice,ctx).strip())
     identities.append((f'/select_lists/{select["index"]}/options/{cindex-1}',original))
 if len(identities)!=1 or identities[0][1]!=row['current_value']:raise ValueError('Archived answer UUID/ordinal/value mismatch')
 answer_key=identities[0][0]
 return answer_key

def answer_span(row):
 answer_key=answer_identity(row)
 spans=[]
 for x in row['source_occurrences']:
  s=pm.sources[x['id']]
  if answer_key.startswith('choices/'):
   raw=Path(s['source_file']).read_text();start=raw.index('id="'+s['dom_id']+'"')
   starts=list(re.finditer(r'<td\b[^>]*class="[^"]*\bquestionWidget-choiceText\b[^"]*"',raw[start:s['source_offset']]))
   if len(starts)-1!=int(answer_key.split('/')[1]):continue
  keys={m['json_field'] for m in s['stored_json_matches'] if m['attribute']==':answer/value'}
  if not any(k==answer_key or k.endswith(answer_key) for k in keys):raise ValueError('Answer source choice mismatch')
  old=conv.old.canonical(stripped(s['legacy_markdown']));new=conv.old.canonical(row['current_value'])
  if old!=new:raise ValueError('Answer is not one complete legacy math body')
  raw=Path(s['source_file']).read_text()
  if raw[s['source_offset']:s['source_offset']+len(s['source_html'])]!=s['source_html']:raise ValueError('Source bytes mismatch')
  spans.append({'source_occurrence_id':s['id'],'source_html':s['source_html'],'source_sha256':s['source_sha256'],'source_file':s['source_file'],'start':0,'end':len(row['current_value']),'old_markdown':row['current_value']})
 if not spans:raise ValueError('No source occurrence for exact original answer ordinal')
 return spans

def process(row):
 entity=entities[row['entity']];answer_type=entity.get(':answer/type',{}).get(':db/ident')
 current=entity[row['attribute']]
 d={'entity':row['entity'],'attribute':row['attribute'],'source_occurrences':[s['id'] for s in row['source_occurrences']]}
 if row['entity']==17592186130324 and row['attribute']==':tutorial/content':
  d['classification']='repaired-by-manual-contextual-merge';return d,None
 if row['attribute']==':answer/value' and answer_type!=':answer.type/math' and not list(MATH.finditer(row['current_value'])):
  d.update(classification='no-change-text-answer-not-tex',answer_type=answer_type);return d,None
 try:
  if row['attribute']==':answer/value' and answer_type==':answer.type/math':spans=answer_span(row)
  elif row['attribute']==':answer/value':
   key=answer_identity(row)
   if not key.startswith('choices/'):raise ValueError('Text select answer needs positional replay')
   index=int(key.split('/')[1]);filtered=[]
   for occ in row['source_occurrences']:
    source=pm.sources[occ['id']];raw=Path(source['source_file']).read_text();start=raw.index('id="'+source['dom_id']+'"')
    starts=[m.start()+start for m in re.finditer(r'<td\b[^>]*class="[^"]*\bquestionWidget-choiceText\b[^"]*"',raw[start:source['source_offset']])]
    if len(starts)-1==index:filtered.append(occ)
   if not filtered:raise ValueError('Source occurrence belongs to different original choice')
   spans=pm.bind({**row,'source_occurrences':filtered})
  else:spans=pm.bind(row)
  replacements=[]
  for span in spans:
   source=pm.sources[span['source_occurrence_id']];result=conv.convert_source(source)
   if result['errors']:raise ValueError('; '.join(result['errors']))
   if result['source_sha256']!=span['source_sha256']:raise ValueError('Source digest mismatch')
   tex=result['tex']
   if not tex:raise ValueError('Conversion has no visible expression')
   after=wrap(tex,span['old_markdown'],answer_type)
   if after==span['old_markdown']:continue
   replacements.append({**span,'before':span['old_markdown'],'after':after,'source_offset':source['source_offset'],'source_line':source['source_line'],'mechanisms':source['mechanisms'],'features':result['features'],'binding':'byte-exact-original-owner-replay' if row['attribute']!=':answer/value' else 'archived-answer-uuid-and-source-ordinal-complete-math-body'})
  # Repeated archival evidence for the same entire answer must agree.
  unique={}
  for r in replacements:
   key=(r['start'],r['end'])
   if key in unique and unique[key]['after']!=r['after']:raise ValueError('Conflicting source conversions of one span')
   unique.setdefault(key,r)
  replacements=list(unique.values())
  before=row['current_value']
  if current!=before:
   # Scope fresh intervening prose edits: every target must remain unique and
   # identical, retaining all current non-target bytes.
   for r in replacements:
    if current.count(r['before'])!=1:raise ValueError('Intervening change ambiguous exact target')
    r['start']=current.index(r['before']);r['end']=r['start']+len(r['before']);r['binding']+='; fresh-unique-exact-span-prose-preserved'
   before=current
  replacements.sort(key=lambda r:r['start'])
  if any(a['end']>b['start'] for a,b in zip(replacements,replacements[1:])):raise ValueError('Overlapping bound replacements')
  after=before
  for r in reversed(replacements):
   assert after[r['start']:r['end']]==r['before'];after=after[:r['start']]+r['after']+after[r['end']:]
  if after==before:d['classification']='no-change-source-already-equivalent';return d,None
  if re.findall(r'\{\{[^{}]+\}\}',before)!=re.findall(r'\{\{[^{}]+\}\}',after):raise ValueError('Answer-control marker changed')
  change={'entity':row['entity'],'attribute':row['attribute'],'before':before,'after':after,'before_sha256':digest(before),'after_sha256':digest(after),'answer_type':answer_type,'replacements':replacements}
  d.update(classification='proposed',replacements=len(replacements),before_sha256=digest(before),after_sha256=digest(after));return d,change
 except Exception as exc:
  if str(exc)=='No source occurrence for exact original answer ordinal':
   d.update(classification='no-change-loss-witness-belongs-to-other-original-choice',reason=str(exc),original_choice=answer_identity(row))
  else:d.update(classification='unresolved-source-context',reason=str(exc))
  return d,None

def main():
 decisions=[];changes=[];started=time.time()
 with (HERE/'decisions.jsonl').open('w') as ds,(HERE/'changes.jsonl').open('w') as cs:
  for n,row in enumerate(rows):
   d,c=process(row);decisions.append(d);ds.write(json.dumps(d,ensure_ascii=False)+'\n');ds.flush()
   if c:changes.append(c);cs.write(json.dumps(c,ensure_ascii=False)+'\n');cs.flush()
   if n%100==0:print(json.dumps({'processed':n+1,'changes':len(changes),'seconds':round(time.time()-started)}),flush=True)
 for name,data in [('decisions.json',decisions),('changes.json',changes)]: (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 summary={'queue_fields':len(rows),'proposed':len(changes),'classification':dict(collections.Counter(d['classification'] for d in decisions)),'unresolved_reasons':dict(collections.Counter(d.get('reason','').split(',')[0] for d in decisions if d['classification'].startswith('unresolved'))),'seconds':round(time.time()-started,1)}
 (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()

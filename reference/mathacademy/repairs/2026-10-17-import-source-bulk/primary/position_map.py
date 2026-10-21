"""Bind source occurrences to exact original Markdown spans by instrumented replay.

No database access or writes. Every result requires byte-identical replay of the
complete original content field with source tags stripped. Repeated fragments
are independently tagged in source DOM order; no value-only substitution.
"""
from pathlib import Path
import collections, copy, hashlib, html, importlib.util, json, re, sys
from bs4 import BeautifulSoup
from functools import lru_cache
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
AUDIT=HERE.parent.parent/'2026-10-16-import-root-cause'
sys.path.insert(0,str(ROOT))

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
scan=module('bulk_source_scan',AUDIT/'source/scan.py')
legacy=scan.legacy;md=scan.md
seed=module('bulk_original_import',ROOT/'scripts/generate_ma_lesson_seed.py')
original_extract=legacy.extract_math_from_node
original_render=md.math_to_markdown
sources={r['id']:r for line in (AUDIT/'source/occurrences.jsonl').read_text().splitlines() if (r:=json.loads(line))}
# Half-open bracket interval fallback used by original importer.
old_placeholder=md.extract_math_placeholder

def fixed_placeholder(value):
 result=old_placeholder(value)
 if result is None and value.startswith('[MATH:') and value.endswith(']') and value.count('[MATH:')==1 and '[FREE_ENTRY' not in value and '[SELECT' not in value:return value[6:-1].strip()
 return result
md.extract_math_placeholder=fixed_placeholder


def digest(value):return hashlib.sha256(value.encode()).hexdigest()

def make_item(item,node):
 if item['item_type']=='step':return legacy.build_step_item(item['lesson_index'],item['step_index'],node)
 return legacy.build_question_item(item['lesson_index'],item['question_index'],node)

@lru_cache(maxsize=200)
def read_source(path_string):
 path=Path(path_string);raw=path.read_text();return raw,json.loads(path.with_suffix('.json').read_text())

def owner_source(occ):
 path=Path(occ['source_file']);raw,data=read_source(str(path))
 assert raw[occ['source_offset']:occ['source_offset']+len(occ['source_html'])]==occ['source_html']
 item=next(x for x in data['lesson']['items'] if x['dom_id']==occ['dom_id'])
 owner_position=raw.find('id="'+occ['dom_id']+'"');owner_start=raw.rfind('<',0,owner_position);owner_end=scan.owner_end(raw,owner_position)
 soup=BeautifulSoup(raw[owner_start:owner_end],'html.parser')
 soup._bulk_owner_start=owner_start
 node=soup.find(id=occ['dom_id'])
 assert node is not None
 return item,node,soup,raw

def render_item(item,topic,attribute):
 # Mirror the actual EDB importer, not the earlier Markdown quiz-block seed.
 # reference/edb-math/bin/generate-ma-lessons-json.py: question_form/lesson_forms.
 ctx=md.MarkdownContext(image_resolver=md.LessonImageResolver(str(topic),md.DEFAULT_LESSONS_ROOT))
 if item['item_type']=='step':
  if item['step_type']=='tutorial':value='\n'.join(md.render_tutorial_step(item,ctx)).strip()
  else:
   question_ctx=md.MarkdownContext(image_resolver=ctx.image_resolver,standalone_math_display=False)
   prompt=[];explanation=[]
   for section in item['sections']:
    if section['section_type']=='example_question':prompt.extend(md.prompt_blocks(section,question_ctx))
    elif md.normalize_ws(section.get('readable_text','')).upper()!='EXPLANATION':explanation.extend(md.html_fragment_to_blocks(section.get('normalized_html',''),ctx))
   value=md.blocks_to_markdown(prompt if attribute==':question/problem' else explanation)
  return seed.markdown_images(value,str(topic))
 ctx.standalone_math_display=False
 if attribute==':answer/value':
  result=[]
  for n,choice in enumerate(item.get('choices',[])):
   value=md.render_choice_markdown(choice,ctx).strip()
   inline=re.fullmatch(r'\$([^$]+)\$',value,re.S);display=re.fullmatch(r'\$\$\s*(.*?)\s*\$\$',value,re.S)
   representation=('math',(inline or display)[1].strip()) if inline or display else ('text',seed.markdown_images(value,str(topic)))
   if choice.get('content_type')=='image':representation=seed.answer_value(choice,value,str(topic))
   result.append((representation,f'choices/{n}'))
  return result
 prompt,body,graphic,calculator=[md.prompt_blocks(item.get(k,{}),ctx) for k in ('prompt','body','graphic','calculator_instructions')]
 simple=(item['question_format']=='multiple-choice' and not body and not graphic and not calculator and len(prompt)==1 and prompt[0].kind in {'paragraph','display_math'} and all(c.get('content_type')=='text' for c in item.get('choices',[])))
 problem=md.render_question_content_markdown(item,ctx,prompt,body,graphic,calculator,simple_inline_prompt=simple)
 if item['question_format']!='multiple-choice':
  inputs=item['free_entry_blanks'] if item['question_format']=='free-response' else item['select_lists']
  number=iter(range(1,len(inputs)+1))
  problem,replaced=seed.UNDERLINE.subn(lambda _:'{{field-'+str(next(number))+'}}',problem)
  assert replaced==len(inputs),(topic,item['question_id'],replaced,len(inputs))
 return seed.markdown_images(problem,str(topic))

def bind(row):
 occurrences=[sources[x['id']] for x in row['source_occurrences']]
 assert len({(o['source_file'],o['dom_id']) for o in occurrences})==1
 first=occurrences[0];item,node,soup,raw=owner_source(first)
 replay=make_item(item,node)
 # Compare all original JSON content containers, including controls and choices.
 original_fields=list(scan.item_fields(item));replayed_fields=list(scan.item_fields(replay))
 assert [(a,k,x.get('normalized_html')) for a,k,x in original_fields]==[(a,k,x.get('normalized_html')) for a,k,x in replayed_fields],('Owner JSON replay differs',row['entity'])
 original=render_item(item,first['topic_id'],row['attribute'])
 if row['attribute']==':answer/value':
  matches=[(kind,value,key) for (kind,value),key in original if value==row['current_value']]
  assert len(matches)==1,('Answer render match ambiguity',len(matches))
  _,original,answer_key=matches[0]
 else:answer_key=None
 # Imported canonical image paths and harmless block ordering can differ from
 # archived Markdown. Bind only if the complete ordered formula sequence is exact.
 from scripts.question_capture.math_format import MATH
 old_math=list(MATH.finditer(original));current_math=list(MATH.finditer(row['current_value']))
 def mathnorm(text):return re.sub(r'\s+','',text)
 block_order=False
 if original!=row['current_value']:
  if [mathnorm(x[0]) for x in old_math]!=[mathnorm(x[0]) for x in current_math]:
   assert collections.Counter(original.split('\n\n'))==collections.Counter(row['current_value'].split('\n\n')),('Full math sequence replay differs',row['entity'])
   block_order=True
 # Tag the exact title or MathML node in the retained source DOM.
 tags={};occurrence_index={}
 for number,occ in enumerate(occurrences):
  tag='BULKSOURCE'+str(number)+'END'
  if occ.get('source_title_index') is not None:
   target=soup.find_all('title')[len(re.findall(r'<title\b',raw[soup._bulk_owner_start:occ['source_offset']]))]
  else:
   # MathML outside title: source prefix provides its DOM ordinal.
   prefix=raw[soup._bulk_owner_start:occ['source_offset']]
   index=len(re.findall(r'<math\b',prefix))
   target=soup.find_all('math')[index]
  assert target.find_parent(id=first['dom_id']) is not None
  target['data-bulk-source']=tag
  tags[tag]=occ;occurrence_index[occ['id']]=number
 def tagged_extract(source_node):
  result=original_extract(source_node)
  own=source_node.get('data-bulk-source')
  target=source_node.find(attrs={'data-bulk-source':True})
  tag=own or (target.get('data-bulk-source') if target else None)
  if tag:
   assert result and scan.compact(result[0])==scan.compact(tags[tag]['legacy_text']),(tag,'legacy text mismatch')
   return tag+' '+result[0],result[1]
  return result
 def tagged_render(raw_value,display):
  prefix=raw_value.split(' ',1)[0]
  if prefix in tags:
   occ=tags[prefix];value=original_render(occ['legacy_text'],display)
   return 'ZZBEGIN'+prefix+'ZZ'+value+'ZZEND'+prefix+'ZZ'
  return original_render(raw_value,display)
 legacy.extract_math_from_node=tagged_extract;md.math_to_markdown=tagged_render
 try:
  tagged=make_item(item,node);marked=render_item(tagged,first['topic_id'],row['attribute'])
  if answer_key is not None:marked=next(value for (kind,value),key in marked if key==answer_key)
 finally:legacy.extract_math_from_node=original_extract;md.math_to_markdown=original_render
 clean=re.sub(r'ZZ(?:BEGIN|END)BULKSOURCE\d+ENDZZ','',marked)
 if clean!=original:
  (HERE/('debug-'+str(row['entity'])+'-original.txt')).write_text(original)
  (HERE/('debug-'+str(row['entity'])+'-clean.txt')).write_text(clean)
 assert clean==original,('Tagged full field replay differs',row['entity'],digest(clean),row['current_sha256'])
 spans=[];pos=0;clean_pos=0
 for match in re.finditer(r'ZZBEGIN(BULKSOURCE\d+END)ZZ([\s\S]*?)ZZEND\1ZZ',marked):
  clean_pos+=match.start()-pos
  spans.append({'source_occurrence_id':tags[match[1]]['id'],'source_html':tags[match[1]]['source_html'],
    'source_sha256':tags[match[1]]['source_sha256'],'source_file':tags[match[1]]['source_file'],
    'start':clean_pos,'end':clean_pos+len(match[2]),'old_markdown':match[2]})
  clean_pos+=len(match[2]);pos=match.end()
 assert sorted(s['source_occurrence_id'] for s in spans)==sorted(o['id'] for o in occurrences),('Tag not emitted exactly once',row['entity'])
 assert all(original[s['start']:s['end']]==s['old_markdown'] for s in spans)
 if block_order:
  old_blocks=list(re.finditer(r'(?s)(?:\A|(?<=\n\n))(.+?)(?=\n\n|\Z)',original));new_blocks=list(re.finditer(r'(?s)(?:\A|(?<=\n\n))(.+?)(?=\n\n|\Z)',row['current_value']))
  for span in spans:
   block=next(b for b in old_blocks if b.start()<=span['start'] and span['end']<=b.end())
   earlier=sum(b[0]==block[0] and b.start()<block.start() for b in old_blocks)
   target=[b for b in new_blocks if b[0]==block[0]][earlier]
   offset=target.start()-block.start();span.update(start=span['start']+offset,end=span['end']+offset,binding='exact-block-preserving-source-occurrence-order')
 elif original!=row['current_value']:
  for span in spans:
   matches=[(i,x) for i,x in enumerate(old_math) if span['start']<=x.start() and x.end()<=span['end']]
   assert len(matches)==1,('Source span not one math formula',row['entity'],span['source_occurrence_id'])
   i,match=matches[0]
   assert original[span['start']:match.start()].strip()=='' and original[match.end():span['end']].strip() in ('','.',',','?','!',';'),('Unmapped source prefix/suffix',row['entity'])
   target=current_math[i];span.update(start=target.start(),end=target.end(),old_markdown=target[0],binding='entire-ordered-math-sequence-equal',math_ordinal=i)
 else:
  for span in spans:span['binding']='entire-field-byte-identical'
 return spans

if __name__=='__main__':
 rows=[json.loads(line) for line in (AUDIT/'database/source-backed-candidates.jsonl').read_text().splitlines()]
 good=[];bad=[]
 for n,row in enumerate(rows):
  try:good.append({**row,'spans':bind(row)})
  except Exception as e:bad.append({'entity':row['entity'],'attribute':row['attribute'],'error':repr(e)})
  if n%25==0:print(n,len(good),len(bad),flush=True)
 (HERE/'bound.json').write_text(json.dumps(good,ensure_ascii=False,indent=2)+'\n')
 (HERE/'position-exceptions.json').write_text(json.dumps(bad,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'bound':len(good),'exceptions':len(bad),'errors':collections.Counter(x['error'].split(',')[0] for x in bad)},indent=2))

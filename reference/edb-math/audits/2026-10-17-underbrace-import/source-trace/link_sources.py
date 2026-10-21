import sys
sys.dont_write_bytecode=True
import json,re,collections,hashlib,importlib.util
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');A=R/'reference/edb-math/audits/2026-10-17-underbrace-import';E=A/'evidence';O=Path('/tmp/underbrace-import-trace-agent')
sys.path.insert(0,str(R/'capture'));from scripts.database.edn import loads
metadata={v[':db/id']:v for v in json.loads((E/'metadata.json').read_text())}
attrs={':tutorial/content':'content',':question/problem':'problem',':question/worked-solution':'worked_solution'}
live=[]
for attr in attrs:
 file=E/'current'/(attr[1:].replace('/','-')+'.edn')
 for eid,text,tx,source in loads(file.read_text()):
  if not ('⏟' in text or '⏞' in text):continue
  m=metadata[eid];sid=m.get(':question/math-academy-id')
  if sid is None and ':tutorial/math-academy-id' in m:sid='tutorial-'+str(m[':tutorial/math-academy-id'])
  live.append({'eid':eid,'attribute':attr,'source_identity':sid,'current_text':text,'current_sha256':hashlib.sha256(text.encode()).hexdigest(),'sources':[]})
byid=collections.defaultdict(list)
for row in live:byid[row['source_identity']].append(row)
def minor(text):return re.sub(r'\s+',' ',str(text).replace('\u2061','').replace(r'\u2061','')).strip()
rank={'exact_saved_import':0,'minor_normalization_saved_import':1,'exact_capture_record':2,'minor_normalization_capture_record':3,'exact_archived_json_render':4,'minor_normalization_archived_json_render':5,'source_identity_only':6,'no_source_evidence':7}
def add(row,source,text=None,kind='saved_import'):
 match='source_identity_only'
 if text is not None:
  source['value_sha256']=hashlib.sha256(text.encode()).hexdigest();source['brace_glyph_count']=text.count('⏟')+text.count('⏞')
  if text==row['current_text']:match='exact_'+kind
  elif minor(text)==minor(row['current_text']):match='minor_normalization_'+kind
 source['match_class']=match;row['sources'].append(source)
imports=R/'reference/edb-math/imports/math-academy/newer-captures'
for filename,key in [('questions-with-local-images.json','questions'),('source-occurrences.json','records'),('tutorials.json','occurrences')]:
 p=imports/filename;data=json.loads(p.read_text())[key];n=0
 for idx,item in enumerate(data):
  mid=item.get('math_academy_id');sid='tutorial-'+str(mid) if filename=='tutorials.json' else mid
  if sid not in byid:continue
  for row in byid[sid]:
   v=item.get(attrs[row['attribute']]);source={'kind':'newer_import_record','record_file':str(p),'record_key':key,'record_index':idx,'topic_id':item.get('topic_id'),'task':item.get('task'),'stream':item.get('stream'),'source_directory':item.get('source_directory'),'source_file':item.get('source_file'),'source_files':item.get('source_files',[])}
   if v is not None:add(row,source,v)
  n+=1
 print(filename,'relevant_records',n,flush=True)
 del data
census=json.loads(Path('/tmp/underbrace-source-census-agent/affected-source-items.json').read_text())
spec=importlib.util.spec_from_file_location('ma_brace_links_renderer',Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py'));md=importlib.util.module_from_spec(spec);sys.modules[spec.name]=md;spec.loader.exec_module(md)
original_math_placeholder=md.extract_math_placeholder
def placeholder(raw):
 v=original_math_placeholder(raw);t=raw.strip()
 if v is None and t.startswith('[MATH:') and t.endswith(']') and t.count('[MATH:')==1 and '[FREE_ENTRY' not in t and '[SELECT' not in t:return t[6:-1].strip()
 return v
md.extract_math_placeholder=placeholder
class SourceImageResolver:
 def relative_markdown_path(self,src):return src
cache={};render_errors=[]
for item in census:
 sid=item['source_identity']
 if sid not in byid:continue
 p=Path(item['file']);data=cache.setdefault(str(p),json.loads(p.read_text()));step=data['lesson']['items'][item['item_index']]
 ctx=md.MarkdownContext(image_resolver=SourceImageResolver());qctx=md.MarkdownContext(image_resolver=ctx.image_resolver,standalone_math_display=False);rendered={}
 try:
  if item['step_type']=='tutorial':rendered['content']='\n'.join(md.render_tutorial_step(step,ctx)).strip()
  elif item['step_type']=='example':
   prompt=[];explain=[]
   for sec in step['sections']:
    if sec['section_type']=='example_question':prompt.extend(md.prompt_blocks(sec,qctx))
    elif md.normalize_ws(sec.get('readable_text','')).upper()!='EXPLANATION':explain.extend(md.html_fragment_to_blocks(sec.get('normalized_html',''),ctx))
   rendered['problem']=md.blocks_to_markdown(prompt).strip();rendered['worked_solution']=md.blocks_to_markdown(explain).strip()
  else:
   fragments=[md.prompt_blocks(step.get(k,{}),qctx) for k in ('prompt','body','graphic','calculator_instructions')];prompt,body,graphic,calculator=fragments
   simple=step['question_format']=='multiple-choice' and not body and not graphic and not calculator and len(prompt)==1 and prompt[0].kind in {'paragraph','display_math'} and all(c.get('content_type')=='text' for c in step.get('choices',[]))
   rendered['problem']=md.render_question_content_markdown(step,qctx,prompt,body,graphic,calculator,simple_inline_prompt=simple).strip()
 except Exception as e:render_errors.append({'source_identity':sid,'error':str(e)})
 for row in byid[sid]:
  source={'kind':'archived_source_json','record_file':str(p),'html_file':str(p.with_suffix('.html')),'selector':('#question-'+str(item['question_id'])) if item['question_id'] else '#step-'+str(item['step_id']),'topic_id':item['topic_id'],'item_index':item['item_index'],'normalized_source_leaf_paths':item['leaf_paths'],'normalized_source_brace_counts':item['counts']}
  add(row,source,rendered.get(attrs[row['attribute']]),'archived_json_render')

def finalize():
 counts=collections.Counter()
 for row in live:
  row['match_class']=min((s['match_class'] for s in row['sources']),key=lambda x:rank[x],default='no_source_evidence');counts[row['match_class']]+=1
  row['sources'].sort(key=lambda x:rank[x['match_class']])
 (O/'source-links-internal.json').write_text(json.dumps(live,ensure_ascii=False,indent=2)+'\n')
 (O/'source-links.json').write_text(json.dumps([{k:v for k,v in r.items() if k!='current_text'} for r in live],ensure_ascii=False,indent=2)+'\n')
 summary={'total_attributes':len(live),'entities':len(set(r['eid'] for r in live)),'by_match_class':dict(counts),'normalization_for_minor_match':'Remove actual U+2061 and literal backslash-u2061; collapse whitespace only. No brace correction, no equation simplification, no function-name changes.','archived_json_render_image_policy':'Source image paths preserved, no guessed mapping. Image-bearing changes may therefore classify as identity only.','render_errors':render_errors,'missing_source_identities':sorted(set(r['source_identity'] for r in live if not r['sources']),key=lambda x:str(x)),'full_raw_source_verification':False}
 (O/'source-link-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
finalize()

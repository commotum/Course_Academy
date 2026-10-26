"""Bind visually reviewed native-notation candidates to current uses and sources."""
import collections,csv,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/native-math-visual-audit-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from audit_math_image_imports import svg_kind
old=json.loads((R/'reference/edb-math/audits/2026-10-22-math-images/assets.json').read_text());items={};reviews=[]
def select(group,indices,category,description):
 values=json.loads((W/(group+'.json')).read_text())
 for i in indices:
  a=values[i];reviews.append({'group':group,'index':i,'path':a['path'],'decision':'native-notation-candidate','category':category,'reason':description});items.setdefault(a['path'],{**a,'category':category,'reason':description,'visual_reviews':[]})['visual_reviews'].append({'group':group,'index':i})
select('topic-focused',[0,1,2,3,10,11,12,13,14,15,16,17,18,19,20,21,22,23,28,31,32,33,34,35,36,37,38,39,40,41,*range(52,59),65,66,*range(68,74),*range(79,95)],'annotated-math','Visual consists primarily of mathematical symbols, numbers, labels, arrows, braces, or a schematic matrix; preserve those cues in native notation.')
select('shortwide-tutorial',[3,4,5,56,61,62,63,64,185,199,214,253,291,296,297,355,357,359,360,361,407,408,471,472,473,588,589,595,596],'annotated-math','Visual consists primarily of mathematical notation and explanatory arrows, labels or boxes; suitable for native reconstruction without removing the explanation.')
select('tutorial-priority',[19,22,23,24,20,46,47,48,49,50,51],'symbolic-diagram','A symbolic dependency or change-of-coordinate diagram; retain the full diagram structure in native vector/TeX-compatible form.')
proofcache={};rawcache={}
for a in items.values():
 p=Path('/media/jake/SSD/EDB/math')/a['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==p.stem;a['source_evidence']=[]
 for source in a['source_paths']:
  src=Path(source);html=src.parents[1]/(src.parents[2].name+'.html')
  if not html.exists():continue
  if str(html)not in rawcache:rawcache[str(html)]=html.read_text()
  raw=rawcache[str(html)];tags=[m[0]for m in re.finditer(r'<img\b[^>]*>',raw,re.I)if src.stem in m[0]]
  if tags:a['source_evidence'].append({'source_image':source,'archived_html':str(html),'original_img_tags':tags})
 a['capture_evidence']=old.get(a['path'],{}).get('capture_evidence',[]);a['source_img_capture_confirmed']=any(e['kind']=='source-image'for e in a['capture_evidence']);a['current_fields']=len({(u['entity'],u['attribute'])for u in a['uses']})
field_keys={(u['entity'],u['attribute'])for a in items.values()for u in a['uses']}
current_fields=[d for d in json.loads((W/'image-facts.json').read_text())if(d['e'],d['a'])in field_keys]
field_hashes={(d['e'],d['a']):hashlib.sha256(d['v'].encode()).hexdigest()for d in current_fields}
for a in items.values():
 for u in a['uses']:u['value_sha256']=field_hashes[u['entity'],u['attribute']]
(H/'candidate-fields.json').write_text(json.dumps(current_fields,indent=2)+'\n')
# Record every visually reviewed item, including non-candidates, so contact-sheet
# selection is not confused with an exhaustive review of all database images.
for group in ['shortwide-tutorial','tutorial-priority','new-short','topic-focused']:
 vals=json.loads((W/(group+'.json')).read_text());selected={(r['group'],r['index'])for r in reviews}
 for i,a in enumerate(vals):
  if(group,i)not in selected:reviews.append({'group':group,'index':i,'path':a['path'],'decision':'retain-as-graphic','reason':'Visual review: spatial plot, geometric model, area model, graph, state machine or other illustration; not selected as a notation-only replacement.'})
# Recheck all current SVGs, including assets first seen since the earlier audit.
svgs=[]
for a in json.loads((W/'assets.json').read_text()):
 if a['path'].endswith('.svg'):
  kind,reason=svg_kind((Path('/media/jake/SSD/EDB/math')/a['path']).read_text());svgs.append({'path':a['path'],'kind':kind,'reason':reason,'uses':len(a['uses'])})
(H/'svg-review.json').write_text(json.dumps(svgs,indent=2)+'\n');(H/'visual-review.json').write_text(json.dumps(reviews,indent=2)+'\n');out=list(items.values());(H/'candidates.json').write_text(json.dumps(out,indent=2)+'\n');(W/'confirmed-candidates.json').write_text(json.dumps(out));fields={(u['entity'],u['attribute'])for a in out for u in a['uses']};entities={e for e,_ in fields};topics={c['topic/math-academy-id']for a in out for u in a['uses']for c in u['context']if'topic/math-academy-id'in c}
summary={'basis_t':8100,'candidate_assets':len(out),'image_occurrences':sum(len(a['uses'])for a in out),'content_fields':len(fields),'entities':len(entities),'topics':len(topics),'categories':dict(collections.Counter(a['category']for a in out)),'visually_reviewed_unique_assets':len({r['path']for r in reviews}),'source_img_evidence_assets':sum(bool(a['source_evidence'])for a in out),'original_source_confirmed_assets':sum(bool(a['source_evidence'])or a['source_img_capture_confirmed']for a in out),'source_paths_available':sum(bool(a['source_paths'])for a in out),'current_svg_kinds':dict(collections.Counter(s['kind']for s in svgs)),'database_modified':False,'exhaustive_image_semantic_review':False};(H/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
with(H/'candidates.csv').open('w')as f:
 writer=csv.writer(f);writer.writerow(['entity','attribute','topics','image_path','category','identity','context_excerpt'])
 for a in out:
  for u in a['uses']:
   own=next((c for c in u['context']if c['entity']==u['entity']),{});writer.writerow([u['entity'],u['attribute'],u['topic_titles'],a['path'],a['category'],own.get('question/math-academy-id',own.get('tutorial/math-academy-id','')),u['nearby']])
print(json.dumps(summary,indent=2))
for a in out:
 if a['visual_reviews'][0]['group']=='topic-focused'and a['visual_reviews'][0]['index']in[1,3,28,31,33,39]or a['visual_reviews'][0]['group']=='tutorial-priority'and a['visual_reviews'][0]['index']in[22,46]:
  print('EXAMPLE',a['visual_reviews'],[(u['entity'],u['attribute'],u['topic_titles'])for u in a['uses']])

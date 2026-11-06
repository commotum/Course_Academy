import json,re,subprocess,unicodedata
from pathlib import Path
from urllib.parse import urlsplit,unquote
W=Path('/tmp/255-final-guide-review');S=Path('/home/jake/Developer/study');p=S/'vault/F26/255/Undated_SG-2.md';text=p.read_text();inv=json.loads((W/'inventory.json').read_text())
assert text.startswith('\n')and not text.startswith('\n\n')and text.endswith('\n')
assert re.findall(r'^## Problem (\d+)$',text,re.M)==[str(n)for n in range(1,41)]
assert '```'not in text
pdf=subprocess.check_output(['pdftotext','-layout','/home/jake/Downloads/255 Final Exam Guide_v1.pdf','-'],text=True).split('What topics are covered on the exam?')[1]
pdf=re.sub(r'Section [56]\.\d:[^\n]*','',pdf)
pdf=re.sub(r'^.*MTH\s+255\s+FINAL\s+EXAM[^\n]*$','',pdf,flags=re.M)
items=list(re.finditer(r'\((\d+)\)\s+',pdf));assert len(items)==40
norm=lambda s:re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s).replace('$','').replace('’',"'").replace('•','').replace('\f','')).strip()
for i,m in enumerate(items):
 source=pdf[m.end():items[i+1].start()if i+1<len(items)else len(pdf)]
 source=re.sub(r'(\w)-\s*\n\s*(\w)',r'\1\2',source)
 dest=re.sub(r'^-\s*','',inv[i]['objective'],flags=re.M)
 assert norm(source)==norm(dest),(i+1,norm(source),norm(dest))
markers=list(re.finditer(r'^## Problem (\d+)$',text,re.M));targets=set();links=0;local_copies=[]
for i,m in enumerate(markers):
 body=text[m.end():markers[i+1].start()if i+1<len(markers)else len(text)]
 assert len(re.findall(r'^\*\*Topics:\*\*',body,re.M))==1
 assert len(re.findall(r'^\*\*Prerequisites:\*\*',body,re.M))==1
 assert re.search(r'^\*\*Topics:\*\*[^\n]*\n\*\*Prerequisites:\*\*',body,re.M)
 assert inv[i]['objective']in body
for label,target in re.findall(r'\[([^\]]+)\]\(<([^>]+)>\)',text):
 split=urlsplit(target);q=Path(unquote(split.path))if split.scheme=='file'else(p.parent/unquote(split.path)).resolve()
 assert q.is_file(),q;links+=1
 if q.suffix=='.md':
  t=q.read_text();mid=int(re.search(r'^lesson-id:\s*(\d+)\s*$',t,re.M)[1]);targets.add(mid)
  if '/MA/'not in str(q):
   assert '**Example' in t or '**Question' in t,(q,'No study content in existing local lesson')
   local_copies.append(str(q))
assert len(targets)==55
home=S/'vault/F26/255/Home.md';h=home.read_text();line='- [Undated_SG-2](<Undated_SG-2.md>)\n'
if line not in h:
 anchor='\n[Lesson library]';assert anchor in h;home.write_text(h.replace(anchor,line+anchor,1))
report={'passed':True,'source_objectives_compared':40,'fieldless_questions':40,'quiz_blocks':0,'source_bullet_cases_preserved':[8,25,27,32,33],'links_verified':links,'unique_topics_and_prerequisites':55,'existing_local_lessons_verified':len(set(local_copies)),'component_only_items':[x['number']for x in inv if x['component_only']],'quiz_validator':'Not applicable: intentionally zero quiz blocks; bundled validator reports no quiz blocks found.'}
(W/'local-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

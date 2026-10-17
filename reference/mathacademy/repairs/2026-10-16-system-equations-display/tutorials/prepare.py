"""Restore two captured tutorials' source layout without changing their content."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
AUDIT=ROOT/'reference/mathacademy/audits/2026-10-16-system-equations-display'
fields=json.loads((AUDIT/'content/fields.json').read_text())
changes=[]
for eid in [17592186199637,17592186097842]:
 f=next(f for f in fields if f['entity']==eid and f['attribute']==':tutorial/content')
 before=f['value']
 if eid==17592186199637:
  sections=before.split('\n\n')
  introduction='\n\n'.join(sections[:3])
  bullets='\n\n'.join(sections[3:]).split('\n- ')
  bodies=[]
  for bullet in bullets:
   if bullet.startswith('- '):bullet=bullet[2:]
   bullet=re.sub(r'(?<=[.!])(?=!\[\]\()', '\n\n',bullet)
   lines=bullet.splitlines()
   parts=[]
   for line in lines:
    if not line.strip():continue
    if line.startswith('$') and line.endswith('$'):
     line='$$\n'+line[1:-1]+'\n$$'
    parts.append(line)
   bodies.append('- '+('\n\n'.join(parts)).replace('\n','\n  '))
  after=introduction+'\n\n'+'\n\n'.join(bodies)
  assert after.count('$$')==6
  assert re.findall(r'!\[\]\([^)]*\)',before)==re.findall(r'!\[\]\([^)]*\)',after)
  reason='Restore the original two display systems and display solution tuple, separate graphic paragraphs, and preserve both example list items.'
 else:
  sections=before.split('\n\n')
  assert len(sections)==11
  intro,body,conclusion=sections[0],sections[1:-1],sections[-1]
  assert len(body)==9 and all(line.startswith('- ') for line in body)
  b=[line[2:].rstrip() for line in body]
  after='\n\n'.join([intro, '1. '+b[0], '2. '+b[1]+'\n\n   - '+b[2]+'\n   - '+b[3], '3. '+b[4], '4. '+b[5]+'\n\n   - '+b[6], '5. '+b[7], '6. '+b[8], conclusion])
  reason='Restore six numbered algorithm steps with two nested bullets under step 2 and one under step 4, matching original source HTML including ol start=5.'
 def content(v):
  v=re.sub(r'(?m)^\s*(?:[-*]|\d+\.)\s+','',v)
  return re.sub(r'\s+','',v).replace('$$','$')
 assert content(before)==content(after),(eid,'content changed')
 changes.append({'entity':eid,'attribute':':tutorial/content','before':before,'after':after,'topic':f['topic'],'reason':reason,'source':str((AUDIT/f'source/tutorial-{eid}-original.html').relative_to(ROOT)),'source_sha256':hashlib.sha256((AUDIT/f'source/tutorial-{eid}-original.html').read_bytes()).hexdigest(),'preservation_check':'Exact prose, images and mathematical text preserved after ignoring layout, list markers and single-versus-double dollar delimiters.'})
(HERE/'changes.json').write_text(json.dumps(changes,indent=2)+'\n')
print(json.dumps({'changes':len(changes),'entities':[c['entity'] for c in changes],'preservation_passed':True}))

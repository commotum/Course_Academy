import json,re,hashlib,time
from pathlib import Path
from collections import Counter
from bs4 import BeautifulSoup
root=Path('/home/jake/Developer/Course_Academy');audit=root/'reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/legacy-provenance'
inventory=json.loads((audit/'inventory.json').read_text());owners=inventory['directories_by_question'];directory_mids={}
for mid,dirs in owners.items():
 for directory in dirs:directory_mids.setdefault(directory,set()).add(mid)
findings=[];counts=Counter();visited=set()
for directory,mids in directory_mids.items():
 state=json.loads((Path(directory)/'state.json').read_text())
 for mid in mids:
  record=state.get('questions',{}).get(mid,{})
  for name in ('before','history','after'):
   original=record.get(name,{})
   html=original.get('html','');digest=hashlib.sha256(html.encode()).hexdigest()
   if not html or (mid,digest) in visited:continue
   visited.add((mid,digest));counts['distinct_original_owning_html']+=1
   if '<mphantom' not in html.lower():continue
   page=BeautifulSoup(html,'html.parser');counts['html_with_phantom']+=1
   for node in page.find_all('mphantom'):
    if node.find_parent(class_=lambda c:c and any(v in c.split() for v in ('studentAnswer','studentAnswerHeader','questionWidget-feedback','answerDetails','questionWidget-result'))):continue
    classes=[v for p in node.parents for v in p.get('class',[])]
    authored=any(c in classes for c in ('questionWidget-text','questionText','questionBody','questionWidget-body','exampleQuestion','questionExplanation','questionWidget-explanation','exampleExplanation','questionWidget-choiceText','choiceText'))
    if not authored:continue
    counts['authored_phantom_nodes']+=1
    ancestors=[];decorations=[];fences=[]
    for p in node.parents:
     if p.name in ('mstyle','mpadded','menclose','mrow'):
      attrs=dict(p.attrs)
      if p.name!='mrow' or attrs:ancestors.append({'tag':p.name,'attributes':attrs})
      if p.get('mathbackground') and p.get('mathbackground').lower() not in ('transparent','none'):decorations.append(p)
      elif re.search(r'(?:border|background)\s*(?:[-\w]*\s*):',p.get('style',''),re.I):decorations.append(p)
      elif p.name=='menclose':decorations.append(p)
      if p.name=='mrow':
       direct=[c.get_text() for c in p.find_all('mo',recursive=False)]
       if any(c in ('[',']','(',')','{','}','|') for c in direct):fences.append(direct)
     if p.name=='math':break
    if decorations or fences:
     kind='decorated' if decorations else 'fenced'
     counts[kind+'_phantom_nodes']+=1
     findings.append({'id':mid,'directory':directory,'original_record':name,'original_html_sha256':digest,'dom_id':original.get('dom_id'),'part':'choice' if any(c in classes for c in ('questionWidget-choiceText','choiceText')) else 'solution' if any(c in classes for c in ('questionExplanation','questionWidget-explanation','exampleExplanation')) else 'problem','kind':kind,'phantom_html':str(node),'ancestor_attributes':ancestors,'decorations':[str(p) for p in decorations],'fences':fences})
report={'unique_owning_questions':len(owners),'owning_directories':len(directory_mids),'counts':dict(counts),'unique_affected_question_ids':sorted({r['id'] for r in findings}),'decorated_question_ids':sorted({r['id'] for r in findings if r['kind']=='decorated'}),'findings':findings,'database_writes':0,'scope':'Original owning before/history/after authored prompts/solutions/choices only; learner regions excluded; no source mutation'}
Path('/tmp/boxed-phantom-independent-inventory.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps({k:v for k,v in report.items() if k!='findings'},indent=2))

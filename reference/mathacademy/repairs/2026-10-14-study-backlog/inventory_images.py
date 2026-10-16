import json,re,xml.etree.ElementTree as ET
from pathlib import Path
H=Path(__file__).resolve().parent;M=Path('/media/jake/SSD/EDB/math')
rows={}
for f in json.loads((H/'fields.json').read_text()):
 for match in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)',f['before']):
  name=match[1];x=rows.setdefault(name,{'path':name,'uses':[]});x['uses'].append([f['entity'],f['attribute']])
for x in rows.values():
 p=M/x['path'];x['bytes']=p.stat().st_size;x['kind']=p.suffix[1:]
 if p.suffix=='.svg':
  root=ET.fromstring(p.read_bytes());title=next((n for n in root.iter() if n.tag.split('}')[-1]=='title'),None)
  x['has_title']=title is not None;x['mathml_count']=sum(n.tag.split('}')[-1]=='math' for n in title.iter()) if title is not None else 0
 else:x['mathml_count']=0
(H/'images.json').write_text(json.dumps(list(rows.values()),indent=2)+'\n')
print('Fields:',len(json.loads((H/'fields.json').read_text())),'images:',len(rows),'uses:',sum(len(x['uses']) for x in rows.values()))
for x in rows.values():print(x['path'][:23],x['kind'],'mathml',x['mathml_count'],'uses',x['uses'][:2])

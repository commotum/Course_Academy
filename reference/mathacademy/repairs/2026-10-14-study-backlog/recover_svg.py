"""Recover formula SVG titles through the existing MathML capture parser.
Only staging artifacts are written. Unknown structures remain review findings.
"""
import copy,hashlib,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'))
from math_format import normalize_tex,validate_tex
SOURCE=(R/'scripts/question_capture/dom.js').read_text()
M=Path('/media/jake/SSD/EDB/math');out=[]
def local(node):return node.tag.split('}')[-1]
def html_math(n):
 n=copy.deepcopy(n)
 for child in n.iter():
  child.tag=local(child)
  child.attrib={k.split('}')[-1]:v for k,v in child.attrib.items()}
 return ET.tostring(n,encoding='unicode')
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page();page.route('**/*',lambda route:route.abort())
 for item in json.loads((H/'images.json').read_text()):
  if item['kind']!='svg':continue
  path=M/item['path'];root=ET.fromstring(path.read_bytes());title=next((n for n in root.iter() if local(n)=='title'),None)
  evidence=[]
  def recover(node):
   if local(node) in ['mjx-container','math']:
    maths=[node] if local(node)=='math' else [n for n in node.iter() if local(n)=='math']
    assert len(maths)==1,(item['path'],'Ambiguous source maths',len(maths))
    page.set_content('<div id="fixture"><div class="questionWidget-text">'+html_math(maths[0])+'</div></div>')
    x=page.locator('#fixture').evaluate(SOURCE)
    assert not x['errors'] and not x['assets'],(item['path'],x['errors'])
    text=x['problem'];assert text.startswith('$') and text.endswith('$'),text
    size=2 if text.startswith('$$') else 1
    evidence.append({'mathml':html_math(maths[0]),'tex':text[size:-size].strip()})
    return text[size:-size].strip()
   return (node.text or '')+''.join(recover(c)+(c.tail or '') for c in node)
  try:
   assert title is not None
   text=validate_tex(normalize_tex(recover(title).strip()))
   out.append({**item,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'tex':text,'components':evidence})
  except Exception as e:out.append({**item,'error':str(e),'components':evidence})
 browser.close()
(H/'svg-recovery.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'images':len(out),'recovered':sum('tex' in x for x in out),'issues':[{'path':x['path'],'error':x['error']} for x in out if 'error' in x]}))

from pathlib import Path
import json,shutil,hashlib
from bs4 import BeautifulSoup
ROOT=Path('/home/jake/Developer/Course_Academy')
OUT=ROOT/'reference/mathacademy/audits/2026-10-16-system-equations-display/source'
records=[]
for entity,topic,cid,shot in [(17592186097842,1048,3156,'02-step-17197.png'),(17592186199637,4638,9689,'02-structural-2.png')]:
    src=Path(f'/home/jake/Developer/MA/DATA/Lessons/{topic}/Source')
    htmlpath=src/f'{topic}.html'
    soup=BeautifulSoup(htmlpath.read_text(),'html.parser')
    node=soup.select_one(f'[contentid="{cid}"]')
    original=OUT/f'tutorial-{entity}-original.html'
    original.write_text(str(node))
    screenshot=OUT/f'tutorial-{entity}-original.png'
    shutil.copyfile(src/'Sections'/shot,screenshot)
    d=json.loads((src/f'{topic}.json').read_text())
    def find(x):
        if isinstance(x,dict):
            if str(x.get('content_id'))==str(cid):return x
            for v in x.values():
                y=find(v)
                if y:return y
        elif isinstance(x,list):
            for v in x:
                y=find(v)
                if y:return y
    record=find(d)
    assert record
    normalized=OUT/f'tutorial-{entity}-extracted.json'
    normalized.write_text(json.dumps(record,indent=2)+'\n')
    evidence={'entity':entity,'math_academy_topic':topic,'math_academy_tutorial':cid,'source_dom_id':node.get('id'),
              'original_html':str(original.relative_to(ROOT)), 'source_screenshot':str(screenshot.relative_to(ROOT)),
              'normalized_json':str(normalized.relative_to(ROOT)), 'original_html_sha256':hashlib.sha256(htmlpath.read_bytes()).hexdigest(),
              'source_block_math_count':len(node.select('.mjpage__block')), 'source_top_level_ordered_lists':[
                  {'start':li.get('start','1'),'direct_items':len(li.find_all('li',recursive=False)),
                   'nested_lists':len(li.select('li > ul'))} for li in node.find_all('ol',recursive=False)]}
    if entity==17592186097842:
        evidence.update(finding='Six numbered source steps with nested bullets under steps2 and4 became nine flat unordered bullets in current database content.',
                        boundary='Original HTML and normalized JSON preserve ol/ul nesting, but JSONdrops olstart=5. Markdown conversion/import flattened or lost hierarchy downstream. Exact DBimport converter not traced here; independent MA Markdown has collapsed nested text and reset numbering too.')
    else:
        evidence.update(finding='Two source equation systems and the general solution tuple are display blocks, with separate graphic divs between paragraphs. Current database Markdown puts systems inline with single soft newlines.',
                        boundary='Old lesson-json.py render_math (line560) replaces every formula with spanclass=math, discarding mjpage__block class. Downstream Markdown cannot recover source display intent inside list paragraphs.')
    records.append(evidence)
(OUT/'tutorial-findings.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))

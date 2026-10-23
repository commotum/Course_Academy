"""Recover formula assets from exact source titles and rendered retained/source TeX.

No OCR and no database writes. Matching compares visible glyphs, styles and
fraction/script/root/table structure, not prose similarity or guessed formulas.
"""
import collections,hashlib,importlib.util,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
RAW=ROOT/'.local/edb/math-image-import-audit-2026-10-22'
AUDIT=ROOT/'reference/edb-math/audits/2026-10-22-math-images'
sys.path.insert(0,str(ROOT/'scripts'))
from audit_math_image_imports import objects
spec=importlib.util.spec_from_file_location('source_converter',ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/secondary/convert_source.py')
conv=importlib.util.module_from_spec(spec);spec.loader.exec_module(conv)
MATH=re.compile(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$')
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def prepare():
 assets=json.loads((AUDIT/'assets.json').read_text()); wanted={p:r for p,r in assets.items() if r['kind'].startswith('math-')}
 svg={};cache={}
 for path,r in wanted.items():
  if path.endswith('.svg'):svg[path]=(Path('/media/jake/SSD/EDB/math')/path).read_text();continue
  digest=Path(path).stem
  for evidence in r['capture_evidence']:
   file=evidence['file']
   if file not in cache:cache[file]=json.loads((ROOT/file).read_text())
   for obj in objects(cache[file]):
    if obj.get('tag')!='svg' or not isinstance(obj.get('html'),str):continue
    hashes={obj.get('sha256'),obj.get('original_svg_sha256'),obj.get('source_sha256'),hashlib.sha256(obj['html'].encode()).hexdigest()}
    hashes|={Path(obj[k]).stem for k in ['path','original_svg_path'] if obj.get(k)}
    if digest in hashes:
     svg[path]=obj['html'];break
   if path in svg:break
 assert len(svg)==len(wanted),(len(svg),len(wanted),set(wanted)-svg.keys())
 save(RAW/'repair-source-svgs.json',svg)
 candidates={};direct={};errors=[]
 def add(tex,evidence):
  tex=tex.strip()
  if not tex:return
  if tex not in candidates:candidates[tex]=[]
  if evidence not in candidates[tex]:candidates[tex].append(evidence)
 def source(html,evidence):
  out=conv.convert_source({'id':str(evidence),'source_html':html})
  if out['errors']:errors.append({'evidence':evidence,'errors':out['errors']});return None
  add(out['tex'],evidence);return out['tex']
 for path,s in svg.items():
  title=re.search(r'<title\b[^>]*>[\s\S]*?</title>',s)
  if title:
   tex=source(title[0],{'kind':'asset-title','path':path})
   if tex:direct[path]={'tex':tex,'method':'asset-title','source_sha256':hashlib.sha256(title[0].encode()).hexdigest()}
 # Reuse already reviewed exact-asset mappings, keeping their provenance.
 for file in (ROOT/'reference/mathacademy/repairs').rglob('*replacements.json'):
  try:data=json.loads(file.read_text())
  except ValueError:continue
  if not isinstance(data,dict):continue
  for path,tex in data.items():
   if path in wanted and isinstance(tex,str):add(tex,{'kind':'reviewed-asset-replacement','path':path,'file':str(file.relative_to(ROOT))})
 for row in map(json.loads,(RAW/'affected-history.jsonl').open()):
  if not row['added']:continue
  for m in MATH.finditer(row['v']):
   body=m[0][2:-2] if m[0].startswith(('$$','\\[','\\(')) else m[0][1:-1]
   add(body,{'kind':'retained-history','entity':row['e'],'attribute':row['a'],'t':row['t']})
 archives=set(s['html'] for r in json.loads((AUDIT/'recovery-candidates.json').read_text()) for s in r['matching_archived_lesson_sources'])
 for i,file in enumerate(sorted(archives)):
  text=Path(file).read_text()
  for title in re.finditer(r'<title\b[^>]*>[\s\S]*?</title>',text):
   if 'MathJax' not in title[0].split('>')[0]:continue
   source(title[0],{'kind':'archived-title','file':file,'offset':title.start()})
  for m in re.finditer(r'<math\b[\s\S]*?</math>',text):source(m[0],{'kind':'archived-mathml','file':file,'offset':m.start()})
  if i%100==0:print('archives',i,'candidates',len(candidates),flush=True)
 save(RAW/'repair-candidates.json',[{'tex':tex,'evidence':ev} for tex,ev in candidates.items()])
 save(HERE/'direct-recoveries.json',direct);save(HERE/'conversion-errors.json',errors)
 print(json.dumps({'assets':len(svg),'direct':len(direct),'candidates':len(candidates),'conversion_errors':len(errors)}))
if __name__=='__main__':prepare()

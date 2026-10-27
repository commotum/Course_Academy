import json,re,sys,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import dumps,kw
from question_capture.math_format import MATH,validate_math_structure
p=H/'recover_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('index=collections.defaultdict(list)')[0],str(p),'exec'),ns);formulas=ns['formulas'];meta=json.loads((R/'.local/edb/structural-math-2026-10-26/metadata.json').read_text());rows=json.loads((H/'evaluation-bar-postscan-candidates.json').read_text());want={meta[str(d['e'])]['question/math-academy-id']for d in rows};sources={}
for path in Path('/home/jake/Developer/MA/DATA/Lessons').glob('*/Source/*.json'):
 if not path.with_suffix('.html').exists():continue
 data=json.loads(path.read_text());use=[i for i in data.get('lesson',{}).get('items',[])if i.get('item_type')=='step'and'e-'+str(i.get('content_id'))in want]
 if not use:continue
 raw=path.with_suffix('.html').read_text();raw=re.sub(r'<svg\b[\s\S]*?</svg>',lambda m:'<svg>'+''.join(re.findall(r'<title\b[^>]*>[\s\S]*?</title>',m[0],re.I))+'</svg>',raw,flags=re.I);soup=BeautifulSoup(raw,'html.parser')
 for item in use:
  node=soup.find(id=item['dom_id'])
  if node:sources['e-'+str(item['content_id'])]=(node,path.with_suffix('.html'))
fields=[];edits=[]
for d in rows:
 identity=meta[str(d['e'])]['question/math-academy-id'];node,path=sources[identity];part=node.find(class_='exampleQuestion'if d['a']=='question/problem'else'exampleExplanation');src=formulas(str(part));ms=list(MATH.finditer(d['v']));assert len(src)==len(ms),(identity,len(src),len(ms));changes=[]
 for i,m in enumerate(ms):
  if re.search(r'\\[Bb]ig(?:g)?[lrm]?\s*\\right',m[0])or re.search(r'\\(?:dfrac|frac)\s*\{[^{}]*\\mid[^{}]*\\right\s*\|\s*\^',m[0]):
   tex=src[i];assert isinstance(tex,str),(identity,i,tex);changes.append((m.start(),m.end(),'$$\n'+tex+'\n$$'));edits.append({'entity':d['e'],'attribute':d['a'],'source_identity':identity,'source_path':str(path),'before':m[0],'after':tex,'span':[m.start(),m.end()]})
 assert changes
 after=d['v']
 for a,b,value in reversed(changes):after=after[:a]+value+after[b:]
 validate_math_structure(after);assert re.findall(r'\{\{[^{}]+\}\}',after)==re.findall(r'\{\{[^{}]+\}\}',d['v']);assert re.findall(r'!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>',after)==re.findall(r'!\[[^\]]*\]\([^)]*\)|<img\b[^>]*>',d['v'])
 fields.append({'entity':d['e'],'attribute':d['a'],'before':d['v'],'after':after,'before_sha256':hashlib.sha256(d['v'].encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'math_answer':False,'answer_fields':[],'reasons':['source-evaluation-bar-recovery']})
b=H/'batch-04';b.mkdir(exist_ok=True);(b/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');(b/'source-edits.json').write_text(json.dumps(edits,indent=2)+'\n');(b/'transaction.edn').write_text(dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in fields])+'\n')
for name in ['verify_render.py','verify_db.py','apply.py']:(b/name).write_text((H/name).read_text().replace('R=H.parents[3]','R=H.parents[4]'))
print('Exact-source evaluation-bar repairs:',len(fields),'fields;',len(edits),'formula blocks.')

import hashlib,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('parents=json.loads')[0],str(p),'exec'),ns)
from question_capture.math_format import ENV,environment,cells
sourcepath=Path('/home/jake/Developer/MA/DATA/Lessons/1171/Source/1171.html');soup=BeautifulSoup(sourcepath.read_text(),'html.parser');data=json.loads((H/'current.json').read_text());out=[];repairs=[]
def grids(text):
 gs=[]
 for m in ENV.finditer(text):
  if m.groups()!=('begin','bmatrix'):continue
  span=environment(text,m.start());gs.append(cells(text[span[0]:span[1]]))
 return gs
canon=lambda c:re.sub(r'\s+|[{}]','',re.sub(r'\\color\{[A-Za-z]+\}','',c)).replace(r'\times',r'\cdot')
for activity in data['structure']:
 for step in activity[':activity/steps']:
  c=step[':step/content']
  if':tutorial/content'not in c:continue
  src=soup.find(attrs={'contentid':str(c[':tutorial/math-academy-id'])});assert src is not None
  fs=[ns['normalize_source_tex'](ns['reconstruct'](title))for title in src.find_all('title')];original=grids('\n'.join(fs));current=grids(c[':tutorial/content']);eq=[[list(map(canon,row))for row in g]for g in original]==[[list(map(canon,row))for row in g]for g in current]
  if c[':tutorial/math-academy-id']==2996:
   from question_capture.math_format import MATH
   ms=list(MATH.finditer(c[':tutorial/content']));assert len(ms)==len(fs);after=c[':tutorial/content']
   for m,tex in reversed(list(zip(ms,fs))):
    if r'\color' in tex:
     size=2 if m[0].startswith('$$')else 1;after=after[:m.start()]+('$$\n'+tex+'\n$$'if size==2 else'$'+tex+'$')+after[m.end():]
   assert after!=c[':tutorial/content'];repairs.append([c[':db/id'],'tutorial/content',c[':tutorial/content'],after,'source-selection-highlight'])
  result={'entity':c[':db/id'],'source_tutorial':c[':tutorial/math-academy-id'],'source_formulas':len(fs),'source_matrices':len(original),'stored_matrices':len(current),'matrix_cells_and_annotations_match':eq,'source_colors':len(src.select('[mathcolor]'))};out.append(result)
  (H/('tutorial-'+str(c[':tutorial/math-academy-id'])+'-source.html')).write_text(str(src));print(result)
(H/'tutorial-changes.json').write_text(json.dumps(repairs,indent=2)+'\n');(H/'tutorial-source-verification.json').write_text(json.dumps({'source':str(sourcepath),'sha256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'tutorials':out},indent=2)+'\n');assert all(d['matrix_cells_and_annotations_match']for d in out)

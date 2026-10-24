"""Source-only table evidence; keeps the faulty legacy spelling for matching."""
import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from import_historical_question_content import Renderer
class LegacyRenderer(Renderer):
 def m(self,n):
  if getattr(n,'name',None)=='mtable':return r'\begin{aligned}'+r' \\ '.join(self.m(c) for c in n.children)+r'\end{aligned}'
  return super().m(n)

def slim_dom(markup):
 def keep_svg(match):
  titles=re.findall(r'<title\b[^>]*>[\s\S]*?</title>',match[0],re.I)
  keep=[t for t in titles if '<math' in t or '<mtable' in t]
  return '<svg>'+''.join(keep)+'</svg>' if keep else ''
 return re.sub(r'<svg\b[\s\S]*?</svg>',keep_svg,markup,flags=re.I)

def tables(markup,identity,attribute,path,**extra):
 if '<mtable' not in markup or not re.search(r'(?:columnlines|rowlines|frame)=["\'][^"\']*(?:solid|dashed)',markup):return []
 soup=BeautifulSoup(slim_dom(markup),'html.parser');out=[]
 for t in soup.find_all('mtable'):
  if not any(v not in ('none','') for k in ['frame','columnlines','rowlines'] for v in t.get(k,'none').split()):continue
  r=LegacyRenderer(None);old=r.m(t);rows=[]
  for tr in t.find_all(['mtr','mlabeledtr'],recursive=False):
   rows.append([r.m(td) for td in tr.find_all('mtd',recursive=False)])
  out.append({'identity':identity,'attribute':attribute,'path':str(path),'source_attributes':dict(t.attrs),'rows':rows,'old_tex':old,'source_mathml':str(t),'errors':r.errors,**extra})
 return out

def main():
 out=[];attrs=collections.Counter();files=0
 for path in sorted(Path('/home/jake/Developer/MA/DATA/Lessons').glob('*/Source/*.json')):
  html_path=path.with_suffix('.html')
  if not html_path.is_file():continue
  raw=html_path.read_text()
  if '<mtable' not in raw or not re.search(r'(?:columnlines|rowlines|frame)=["\'][^"\']*(?:solid|dashed)',raw):continue
  d=json.loads(path.read_text());files+=1;soup=BeautifulSoup(raw,'html.parser')
  for i in d.get('lesson',{}).get('items',[]):
   if i.get('item_type')!='step':continue
   kind=i.get('step_type');identity=('tutorial:'+str(i['content_id'])) if kind=='tutorial' else ('e-'+str(i['content_id']))
   step=soup.find(id='step-'+str(i['step_id']))
   if step is None:continue
   if kind=='tutorial':out.extend(tables(str(step),identity,'tutorial/content',html_path,step_id=i['step_id'],topic=int(path.stem)))
   else:
    for cls,a in [('exampleQuestion','question/problem'),('exampleExplanation','question/worked-solution')]:
     for part in step.find_all(class_=cls):out.extend(tables(str(part),identity,a,html_path,step_id=i['step_id'],topic=int(path.stem)))
 for r in out:attrs.update({k+'='+str(v):1 for k,v in r['source_attributes'].items() if k in ['columnalign','frame','rowlines','columnlines']})
 (H/'archived-tables.json').write_text(json.dumps(out,indent=2)+'\n');summary={'source_files_with_mathml':files,'ruled_source_table_occurrences':len(out),'unique_legacy_signatures':len({r['old_tex'] for r in out}),'source_attribute_counts':dict(attrs)};(H/'archive-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()

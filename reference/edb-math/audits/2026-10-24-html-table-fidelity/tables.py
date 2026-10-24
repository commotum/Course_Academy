"""Source-aware table audit utilities. No database mutation."""
import html,json,re,sys
from html.parser import HTMLParser
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/html-table-fidelity';sys.path.insert(0,str(R/'scripts/question_capture'))
from math_format import MATH,normalize_source_tex
sys.path.insert(0,str(R/'scripts'));from import_historical_question_content import Renderer

def compact_dom(markup):
 def keep(m):
  titles=re.findall(r'<title\b[^>]*>[\s\S]*?</title>',m[0],re.I)
  return '<svg>'+''.join(titles)+'</svg>'
 return re.sub(r'<svg\b[\s\S]*?</svg>',keep,markup,flags=re.I)

class TableSpans(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=False);self.text=text;self.lines=[0];self.stack=[];self.spans=[]
  for m in re.finditer('\n',text):self.lines.append(m.end())
  self.feed(text)
 def absolute_offset(self):line,col=self.getpos();return self.lines[line-1]+col
 def handle_starttag(self,tag,attrs):
  if tag=='table':self.stack.append(self.absolute_offset())
 def handle_endtag(self,tag):
  if tag=='table'and self.stack:
   start=self.stack.pop();end=self.text.find('>',self.absolute_offset())+1;self.spans.append((start,end))

def split_row(line):
 saved=[]
 def protect(m):saved.append(m[0]);return 'CAMATHCELL'+str(len(saved)-1)+'END'
 line=MATH.sub(protect,line.strip());line=line[1:]if line.startswith('|')else line;line=line[:-1]if line.endswith('|')else line
 parts=re.split(r'(?<!\\)\|',line)
 return [re.sub(r'CAMATHCELL(\d+)END',lambda m:saved[int(m[1])],p).replace(r'\|','|').strip()for p in parts]

def current_tables(value):
 out=[]
 if '<table' in value.lower():
  for start,end in TableSpans(value).spans:
   n=BeautifulSoup(value[start:end],'html.parser').find('table')
   out.append({'start':start,'end':end,'format':'html','rows':[[str(c.decode_contents()).strip()for c in tr.find_all(['td','th'],recursive=False)]for tr in n.find_all('tr')if tr.find_parent('table')is n],'html':str(n)})
 lines=value.splitlines(keepends=True);offsets=[];offset=0
 for line in lines:offsets.append(offset);offset+=len(line)
 i=1
 while i<len(lines):
  if '|'not in lines[i]or not re.fullmatch(r'\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*',lines[i]):i+=1;continue
  first=i-1
  if '|'not in lines[first]:i+=1;continue
  end=i+1
  while end<len(lines)and'|'in lines[end]and lines[end].strip():end+=1
  start=offsets[first];stop=offsets[end]if end<len(lines)else len(value)
  if not any(t['start']<=start<t['end']for t in out):out.append({'start':start,'end':stop,'format':'markdown','rows':[split_row(lines[j])for j in range(first,end)if j!=i],'alignment':split_row(lines[i]),'text':value[start:stop]})
  i=end
 return sorted(out,key=lambda r:r['start'])

def key(value):
 value=re.sub(r'<[^>]+>',' ',value);value=html.unescape(value)
 value=value.replace('[MATH:','').replace(']','')if '[MATH:'in value else value
 value=value.replace(r'\pi','π').replace(r'\alpha','α').replace(r'\beta','β').replace(r'\mu','μ').replace(r'\sigma','σ')
 value=value.replace('−','-').replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac')
 value=re.sub(r'\{([^{}])\}',r'\1',value)
 value=re.sub(r'\\(?:displaystyle|textstyle|left|right)|\\[,!;:]','',value)
 value=re.sub(r'\\(?:operatorname|mathrm|textrm|text|mathit|mathbf)\{([^{}]*)\}',r'\1',value)
 value=re.sub(r'\{\{(?:answer-field:)?[^}]+\}\}','BLANK',value)
 return re.sub(r'[\s$*]','',value)

def grid_key(rows):return tuple(tuple(key(c)for c in row)for row in rows)

def source_cell(cell):
 n=BeautifulSoup(str(cell),'html.parser')
 for math in list(n.find_all(['mjx-container','math'])):
  if math.parent is None or math.find_parent(['mjx-container','math']):continue
  root=math if math.name=='math'else math.find('math')
  if root:
   r=Renderer(None);tex=r.m(root)
   if not r.errors:math.replace_with(NavigableString('$'+tex+'$'))
 for svg in list(n.find_all('svg')):
  title=svg.find('title')
  if title and not title.find('math'):
   try:value=normalize_source_tex(title.get_text())
   except ValueError:value=title.get_text()
   svg.replace_with(NavigableString('$'+value+'$'))
 for node in n.select('input,select,.freeResponseTextbox,.selectList'):
  if node.parent is not None:node.replace_with(NavigableString('BLANK'))
 for node in n.select('script,style,mjx-assistive-mml'):node.decompose()
 return re.sub(r'\s+',' ',n.get_text(' ',strip=True)).strip()

def style_props(node):
 return {k.strip().lower():v.strip()for k,sep,v in(re.match(r'([^:]+)(:)(.*)',p).groups()for p in node.get('style','').split(';')if':'in p)}

def source_table(table,identity,attribute,path,**extra):
 rows=[];features={'alignment':False,'shading':False,'merged_cells':False,'explicit_headers':False,'nested_tables':bool(table.find('table')),'explicit_grid':False};cells=[]
 ta=dict(table.attrs);ts=style_props(table)
 features['alignment']=table.get('align')in ['center','right']or ts.get('margin')=='auto'or ts.get('text-align')in ['center','right']
 features['explicit_grid']=table.get('rules')in ['all','rows','cols']or table.get('border','0')not in ['0','']or'border'in ts
 for tr in table.find_all('tr'):
  if tr.find_parent('table')is not table:continue
  row=[];details=[]
  for cell in tr.find_all(['td','th'],recursive=False):
   props=style_props(cell);row.append(source_cell(cell));details.append({'tag':cell.name,'attrs':dict(cell.attrs),'text':row[-1]})
   features['alignment']|=cell.get('align')in ['center','right']or props.get('text-align')in ['center','right']
   features['shading']|=bool(cell.get('bgcolor')or props.get('background-color')or props.get('background'))
   features['merged_cells']|=any(cell.get(a,'1')!='1'for a in ['rowspan','colspan'])
   features['explicit_headers']|=cell.name=='th'
  if row:rows.append(row);cells.append(details)
 return {'identity':identity,'attribute':attribute,'path':str(path),'rows':rows,'cells':cells,'table_attrs':ta,'features':features,'source_html':str(table),**extra}

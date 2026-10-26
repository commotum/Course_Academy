"""Find exact partial-formula imports in a captured native snapshot."""
import collections,hashlib,importlib.util,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/mixed-math-titles';sys.path[:0]=[str(R/'scripts'),str(H)]
from reconstruct import reconstruct,SourceRenderer
from import_historical_question_content import Renderer
from question_capture.math_format import MATH,normalize_source_tex
BASE=Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source')
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
old=module('legacy_json_audit',BASE/'3-JSON/lesson-json.py');md=module('legacy_md_audit',BASE/'5-MD/md.py')
def save(path,value):path.write_text(json.dumps(value,default=str,indent=2)+'\n')
def key(value):
 v=value.strip().strip('$');v=re.sub(r'\\(?:displaystyle|textstyle)\b|\\[,!;:]','',v);v=v.replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac').replace('−','-');v=re.sub(r'\\(?:left|right)\s*','',v);v=re.sub(r'\\(?:begin|end)\{(?:aligned|matrix|bmatrix|pmatrix|vmatrix)\}',lambda m:'OPENARRAY'if'begin'in m[0]else'CLOSEARRAY',v)
 v=re.sub(r'\\(?:color|textcolor)\{[^{}]+\}','',v);v=re.sub(r'\\(?:operatorname|textrm|mathrm|text)\{([^{}]*)\}',r'\1',v)
 for _ in range(5):
  new=re.sub(r'\{([^{}])\}',r'\1',v)
  if new==v:break
  v=new
 return re.sub(r'\s','',v).rstrip('.,')
def variants(node):
 if node.name=='math':root=node
 else:root=node.select_one('mjx-assistive-mml math')or node.find('math')
 results=[]
 if root:
  r=Renderer(None);value=r.m(root)
  if not r.errors:
   results.append(value)
   try:results.append(normalize_source_tex(value))
   except ValueError:pass
  raw=old.mathml_to_text(root)
  try:results.append(md.normalize_math_tex(raw))
  except Exception:pass
 else:
  title=node.find('title')
  if title:results.append(title.get_text())
 return {key(x)for x in results if x.strip()}
def roots(part):
 nodes=part.select('.mjpage,mjx-container,math');ids={id(n)for n in nodes};return [n for n in nodes if not any(id(p)in ids for p in n.parents)]
def main():
 meta=collections.defaultdict(dict);owners=collections.defaultdict(list);values={};idents={};attrs={'tutorial/content','question/problem','question/worked-solution','answer/value'}
 for line in (W/'current.jsonl').open():
  d=json.loads(line);e,a,v=d['e'],d['a'],d['v']
  if a in attrs and isinstance(v,str):values[e,a]=d
  if a in ['question/math-academy-id','tutorial/math-academy-id','answer/type','answer-field/type','answer-field/correct']:meta[e][a]=v
  if a=='db/ident':idents[e]=v
  if a in ['answer-field/choices','question/answer-fields']:owners[v].append([e,a])
 index=collections.defaultdict(list)
 for (e,a),d in values.items():
  m=meta[e]
  if a=='tutorial/content':identities=['tutorial:'+str(m.get('tutorial/math-academy-id'))]
  elif a.startswith('question/'):identities=[m.get('question/math-academy-id')]
  else:identities=[meta[q].get('question/math-academy-id')for f,attr in owners[e]if attr=='answer-field/choices'for q,attr in owners[f]if attr=='question/answer-fields']
  spans=list(MATH.finditer(d['v']));pieces=[{'span':[s.start(),s.end()],'text':s[0],'key':key(s[0])}for s in spans]
  if a=='answer/value'and idents.get(m.get('answer/type'))==':answer.type/math'and not spans:pieces=[{'span':[0,len(d['v'])],'text':d['v'],'key':key(d['v']),'bare_math':True}]
  d={**d,'pieces':pieces}
  for identity in identities:
   if identity:index[identity,a].append(d)
 save(W/'metadata.json',meta);save(W/'owners.json',owners);save(W/'idents.json',idents)
 matches=[];sources=[];unresolved=[];counts=collections.Counter();all_values={}
 for p in sorted(Path('/home/jake/Developer/MA/DATA/Lessons').glob('*/Source/*.html')):
  counts['archived_lessons_examined']+=1;raw=p.read_text();title_chunks=re.findall(r'<title\b[^>]*>[\s\S]*?</title>',raw,re.I)
  if not any('<math'in x and'<mjx-container'in x for x in title_chunks):continue
  data=json.loads(p.with_suffix('.json').read_text());items=data.get('lesson',{}).get('items',[])
  use=[]
  for item in items:
   if item['item_type']=='step':kind=item['step_type'];identity='tutorial:'+str(item['content_id'])if kind=='tutorial'else'e-'+str(item['content_id'])
   else:kind='question';identity='q-'+str(item['question_id'])
   if any((identity,a)in index for a in attrs):use.append((item,kind,identity))
  if not use:continue
  compact=re.sub(r'<svg\b[\s\S]*?</svg>',lambda m:'<svg>'+''.join(re.findall(r'<title\b[^>]*>[\s\S]*?</title>',m[0],re.I))+'</svg>',raw,flags=re.I);soup=BeautifulSoup(compact,'html.parser');counts['mixed_title_lesson_pages']+=1
  for item,kind,identity in use:
   root=soup.find(id=item['dom_id'])
   if root is None:continue
   parts=[('tutorial/content',root)]if kind=='tutorial'else [('question/problem',n)for n in root.find_all(class_=['exampleQuestion','questionText','questionWidget-text'])]+[('question/worked-solution',n)for n in root.find_all(class_=['exampleExplanation','questionExplanation','questionWidget-explanation'])]+[('answer/value',n)for n in root.find_all(class_=['questionWidget-choiceText','choiceText','selectListOption'])]
   for attr,part in parts:
    entries=[]
    for n in roots(part):
     title=n.find('title');mixed=bool(title and title.find('math')and any(isinstance(x,NavigableString)and x.strip()for x in title.children));entry={'keys':variants(n),'mixed':mixed}
     if mixed:
      proof={'identity':identity,'attribute':attr,'path':str(p),'dom_id':item['dom_id'],'topic':data['topic_id'],'title':str(title),'partial_keys':sorted(entry['keys'])}
      try:
       tex=reconstruct(title);entry['recovered_tex']=tex;entry['keys'].add(key(tex));proof['recovered_tex']=tex
      except Exception as error:proof['reconstruction_error']=str(error)
      sources.append(proof);entry['proof']=proof
     entries.append(entry)
    for i,entry in enumerate(entries):
     if not entry['mixed']:continue
     proof=entry['proof'];old_keys=set(proof['partial_keys']);fullkey=key(entry['recovered_tex'])if'recovered_tex'in entry else None
     # An outer wrapper must change the formula, not simply spell its layout.
     if fullkey is not None and fullkey in old_keys:continue
     for record in index.get((identity,attr),[]):
      pieces=record['pieces'];hits=[(j,c)for j,c in enumerate(pieces)if c['key']in old_keys and c['key']!=fullkey]
      for j,c in hits:
       ordered=len(entries)==len(pieces)and all(piece['key']in source['keys']for piece,source in zip(pieces,entries))and i==j
       same_partial=[x for x in entries if x['mixed']and x['proof']['partial_keys']==proof['partial_keys']]
       unique=len(hits)==1 and len(same_partial)==1 and sum(bool(x['keys']&old_keys)for x in entries)==1
       if not (ordered or unique):unresolved.append({'entity':record['e'],'attribute':attr,'span':c['span'],'source':proof,'reason':'Ambiguous repeated partial formula'});continue
       row={'entity':record['e'],'attribute':attr,'span':c['span'],'before_formula':c['text'],'source':proof,'matching':'entire-formula-sequence'if ordered else'unique-source-bound-partial-formula','bare_math':c.get('bare_math',False)}
       if 'reconstruction_error'in proof:unresolved.append({**row,'reason':proof['reconstruction_error']});continue
       row['after_formula']=entry['recovered_tex']if c.get('bare_math')else'$$\n'+entry['recovered_tex']+'\n$$';matches.append(row);all_values[record['e'],attr]={k:v for k,v in record.items()if k!='pieces'}
  if counts['mixed_title_lesson_pages']%100==0:print('Examined',counts['archived_lessons_examined'],'lessons; mixed formulas',len(sources),'matched',len(matches),flush=True)
 # De-duplicate identical source occurrences without guessing conflicting ones.
 grouped=collections.defaultdict(list)
 for m in matches:grouped[m['entity'],m['attribute'],tuple(m['span'])].append(m)
 confirmed=[]
 for key_,rows in grouped.items():
  if len({key(r['after_formula'])for r in rows})==1:confirmed.append(rows[0])
  else:unresolved.append({'entity':key_[0],'attribute':key_[1],'span':key_[2],'reason':'Conflicting complete source formulas','options':rows})
 save(W/'values.json',list(all_values.values()));save(H/'source-formulas.json',sources);save(H/'confirmed.json',confirmed);save(H/'unresolved.json',unresolved);report={**counts,'mixed_source_formulas':len(sources),'confirmed_formula_repairs':len(confirmed),'affected_fields':len({(m['entity'],m['attribute'])for m in confirmed}),'unresolved_candidates':len(unresolved),'attributes':dict(collections.Counter(m['attribute']for m in confirmed))};save(H/'audit-summary.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()

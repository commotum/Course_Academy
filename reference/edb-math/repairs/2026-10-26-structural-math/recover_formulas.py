"""Propose complete source formulas for structurally malformed old imports."""
import collections,json,re,sys,difflib
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/structural-math-2026-10-26';sys.path[:0]=[str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import reconstruct,SourceRenderer
from question_capture.math_format import MATH,validate_tex,ENV,environment
meta=json.loads((W/'metadata.json').read_text());values={(r['e'],r['a']):r['v']for r in json.loads((W/'values.json').read_text())};sourcefields=json.loads((W/'source-fields.json').read_text());targets=collections.defaultdict(set)
for d in json.loads((H/'malformed-structure.json').read_text()):targets[d['e'],d['a']].add(d['start'])
for d in json.loads((H/'table-candidates.json').read_text()):
 if d['env']!='aligned':targets[d['e'],d['a']].add(d['span'][0])
def roots(s):
 ns=s.select('.mjpage,mjx-container,math');ids={id(n)for n in ns};return[n for n in ns if not any(id(p)in ids for p in n.parents)]
def formulas(html):
 out=[]
 for n in roots(BeautifulSoup(html,'html.parser')):
  t=n.find('title')
  try:
   if t:tex=reconstruct(t)
   else:
    m=n if n.name=='math'else n.find('math');r=SourceRenderer(None);tex=r.m(m)
    if r.errors:raise ValueError(r.errors)
   validate_tex(tex);out.append(tex)
  except Exception as ex:out.append({'error':str(ex)})
 return out
def numbers(tex):
 tex=re.sub(r'\\(?:hspace|vspace|kern|mkern)\{[^{}]*\}','',tex)
 return re.findall(r'(?<![A-Za-z])\d+(?:\.\d+)?',tex)
index=collections.defaultdict(list)
for s in sourcefields:index[s['identity'],s['attribute']].append(s)
proposals=[];unresolved=[]
for(e,a),starts in targets.items():
 m=meta.get(str(e),{});identity='tutorial:'+str(m.get('tutorial/math-academy-id'))if a=='tutorial/content'else m.get('question/math-academy-id');before=values[e,a];maths=list(MATH.finditer(before));where=[i for i,x in enumerate(maths)if any(x.start()<=start<x.end()for start in starts)];sources=index.get((identity,a),[]);options=[];notes=[]
 for s in sources:
  fs=formulas(s['html'])
  if len(fs)!=len(maths):notes.append({'path':s['path'],'source_formulas':len(fs),'stored_formulas':len(maths)});continue
  changes=[];valid=True
  for i in where:
   old=maths[i][0];new=fs[i]
   if not isinstance(new,str):valid=False;break
   if numbers(old)!=numbers(new):valid=False;notes.append({'path':s['path'],'index':i,'reason':'numeric token sequence differs','old_numbers':numbers(old),'new_numbers':numbers(new)});break
   changes.append({'index':i,'span':[maths[i].start(),maths[i].end()],'before':old,'after':'$$\n'+new+'\n$$'if old.startswith(('$$',r'\['))else'$'+new+'$'})
  if valid and changes:options.append({'e':e,'a':a,'identity':identity,'source_path':s['path'],'changes':changes})
 unique={json.dumps(o['changes'],sort_keys=True):o for o in options}
 if len(unique)==1:proposals.append(next(iter(unique.values())))
 else:unresolved.append({'e':e,'a':a,'identity':identity,'source_options':len(sources),'matching_options':len(unique),'notes':notes,'before':before})
(H/'source-formula-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');(H/'source-formula-unresolved.json').write_text(json.dumps(unresolved,indent=2)+'\n');print('fields',len(targets),'proposed',len(proposals),'unresolved',len(unresolved),'mathblocks',sum(len(o['changes'])for o in proposals))
for o in unresolved:print(o['e'],o['a'],o['identity'],'sources',o['source_options'],'matches',o['matching_options'],str(o['notes'])[:450])

"""Use unchanged surrounding source prose to disambiguate residual math matches."""
import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/mixed-math-titles';sys.path.insert(0,str(H));import audit
from reconstruct import reconstruct
from question_capture.math_format import MATH

def tokens(text):return re.findall(r'camath\d+end|[a-z]+|\d+',text.lower())
def around(words,index):
 at=words.index('camath'+str(index)+'end');return ([x for x in words[:at]if not x.startswith('camath')][-24:],[x for x in words[at+1:]if not x.startswith('camath')][:24])
def score(a,b):
 pre=0;post=0
 for x,y in zip(a[0][::-1],b[0][::-1]):
  if x!=y:break
  pre+=1
 for x,y in zip(a[1],b[1]):
  if x!=y:break
  post+=1
 return pre,post

def main():
 resolved=json.loads((H/'resolved.json').read_text());known={(r['entity'],r['attribute'],tuple(r['span']))for r in resolved};pending=[r for r in json.loads((H/'remaining.json').read_text())if(r['entity'],r['attribute'],tuple(r['span']))not in known];values={(r['e'],r['a']):r for r in json.loads((W/'values.json').read_text())};soups={};parts={};current={};accepted=[];remaining=[]
 for row in pending:
  proof=row['source'];path=proof['path'];k=row['entity'],row['attribute'];ck=path,proof['dom_id'],row['attribute']
  if ck not in parts:
   if path not in soups:
    raw=Path(path).read_text();compact=re.sub(r'<svg\b[\s\S]*?</svg>',lambda m:'<svg>'+''.join(re.findall(r'<title\b[^>]*>[\s\S]*?</title>',m[0],re.I))+'</svg>',raw,flags=re.I);soups[path]=BeautifulSoup(compact,'html.parser')
   root=soups[path].find(id=proof['dom_id']);part=root if row['attribute']=='tutorial/content'else root.find(class_=['exampleQuestion','questionText','questionWidget-text']if row['attribute']=='question/problem'else['exampleExplanation','questionExplanation','questionWidget-explanation']);copy=BeautifulSoup(str(part),'html.parser');nodes=audit.roots(copy);source_titles=[str(n.find('title'))if n.find('title')else None for n in nodes]
   for i,n in enumerate(nodes):n.replace_with(NavigableString(' CAMATH'+str(i)+'END '))
   parts[ck]=(tokens(copy.get_text(' ',strip=True)),source_titles)
  words,titles=parts[ck]
  if k not in current:
   text=values[k]['v'];matches=list(MATH.finditer(text));number=iter(range(len(matches)));plain=MATH.sub(lambda m:' CAMATH'+str(next(number))+'END ',text);plain=re.sub(r'!?\[([^]]*)\]\([^)]*\)',r'\1',plain);current[k]=(matches,tokens(BeautifulSoup(plain,'html.parser').get_text(' ',strip=True)))
  matches,curwords=current[k];j=next(j for j,m in enumerate(matches)if[m.start(),m.end()]==row['span']);target=row.get('target_source_index');options=row.get('alignment_options',[])
  if target is None or target>=len(titles)or titles[target]!=str(BeautifulSoup(proof['title'],'html.parser').title):remaining.append({**row,'prose_reason':'Source part identity differs'});continue
  actual=around(curwords,j);scores={i:score(around(words,i),actual)for i in options};pre,post=scores[target];other=max((sum(s)for i,s in scores.items()if i!=target),default=-10);strong=pre>=3 and post>=3
  if not strong or pre+post<other+3:remaining.append({**row,'prose_scores':scores});continue
  try:tex=reconstruct(BeautifulSoup(proof['title'],'html.parser').title)
  except Exception as err:remaining.append({**row,'prose_reason':str(err)});continue
  old=matches[j][0];marker='$$'if old.startswith(('$$',r'\['))else'$';accepted.append({**row,'before_formula':old,'after_formula':marker+'\n'+tex+'\n'+marker if marker=='$$'else'$'+tex+'$','matching':'unique-source-prose-anchors','prose_scores':scores})
 groups=collections.defaultdict(list)
 for row in resolved+accepted:groups[row['entity'],row['attribute'],tuple(row['span'])].append(row)
 final=[]
 for k,rows in groups.items():
  if len({audit.key(r['after_formula'])for r in rows})==1:final.append(rows[0])
  else:remaining.extend({**r,'prose_reason':'Conflicting complete source values'}for r in rows)
 (H/'prose-resolved.json').write_text(json.dumps(accepted,indent=2)+'\n');(H/'final-resolved.json').write_text(json.dumps(final,indent=2)+'\n');(H/'final-remaining.json').write_text(json.dumps(remaining,indent=2)+'\n');print({'added':len(accepted),'final':len(final),'remaining_spans':len({(r['entity'],r['attribute'],tuple(r['span']))for r in remaining}),'remaining_fields':len({(r['entity'],r['attribute'])for r in remaining})})
if __name__=='__main__':main()

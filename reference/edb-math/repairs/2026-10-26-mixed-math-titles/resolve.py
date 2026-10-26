"""Resolve repeated fragments only when every optimal sequence alignment agrees."""
import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/mixed-math-titles';sys.path.insert(0,str(H))
import audit
from reconstruct import reconstruct
from question_capture.math_format import MATH

def save(name,v):(H/name).write_text(json.dumps(v,default=str,indent=2)+'\n')
def matrix(m,n,source,current):
 f=[[0]*(n+1)for _ in range(m+1)]
 for i in range(m):
  for j in range(n):f[i+1][j+1]=max(f[i][j+1],f[i+1][j],f[i][j]+int(current[j]['key']in source[i]))
 b=[[0]*(n+1)for _ in range(m+1)]
 for i in range(m-1,-1,-1):
  for j in range(n-1,-1,-1):b[i][j]=max(b[i+1][j],b[i][j+1],b[i+1][j+1]+int(current[j]['key']in source[i]))
 return f,b

def main():
 original=json.loads((H/'confirmed.json').read_text());uncertain=json.loads((H/'unresolved.json').read_text());allrows=original+uncertain;wanted={(r['entity'],r['attribute'])for r in allrows};values={}
 for line in(W/'current.jsonl').open():
  d=json.loads(line)
  if(d['e'],d['a'])in wanted:values[d['e'],d['a']]=d
 (W/'values.json').write_text(json.dumps(list(values.values()))+'\n');contexts={};soups={};aligns={};out=[];remaining=[];skips=[];seen=set()
 # Candidates refer to one exact source title and current math span. DP
 # includes every source math item, so equal numbers elsewhere are anchors,
 # not evidence to replace all repeated occurrences indiscriminately.
 for row in allrows:
  if 'source'not in row or'span'not in row:remaining.append(row);continue
  proof=row['source'];tag=(row['entity'],row['attribute'],tuple(row['span']),proof['path'],proof['dom_id'],proof['title']);
  if tag in seen:continue
  seen.add(tag);p=proof['path'];ctxkey=(p,proof['dom_id'],row['attribute'],proof['title'])
  if ctxkey not in contexts:
   if p not in soups:
    raw=Path(p).read_text();compact=re.sub(r'<svg\b[\s\S]*?</svg>',lambda m:'<svg>'+''.join(re.findall(r'<title\b[^>]*>[\s\S]*?</title>',m[0],re.I))+'</svg>',raw,flags=re.I);soups[p]=BeautifulSoup(compact,'html.parser')
   root=soups[p].find(id=proof['dom_id']);expected=BeautifulSoup(proof['title'],'html.parser').title;title=next((t for t in root.find_all('title')if t.get('id')==expected.get('id')and str(t)==str(expected)),None);assert title is not None,(p,proof['dom_id'])
   names={'question/problem':['exampleQuestion','questionText','questionWidget-text'],'question/worked-solution':['exampleExplanation','questionExplanation','questionWidget-explanation']}
   parts=[root]if row['attribute']=='tutorial/content'else root.find_all(class_=names[row['attribute']]);part=next(n for n in parts if any(n is parent for parent in title.parents));nodes=audit.roots(part);source=[];i=None
   for k,n in enumerate(nodes):
    keys=audit.variants(n);t=n.find('title')
    if t:
     try:keys.add(audit.key(reconstruct(t)))
     except Exception:pass
    source.append(keys)
    if t is title:i=k
   assert i is not None;contexts[ctxkey]=(source,i,title,id(part))
  source,i,title,partid=contexts[ctxkey];literal=[str(c)for c in title.children if isinstance(c,NavigableString)];joined=''.join(literal);before=''.join(str(c)for c in title.children if isinstance(c,NavigableString)).strip()
  children=list(title.children);first=next((j for j,c in enumerate(children)if not isinstance(c,NavigableString)),None)
  if first is not None:
   pre=''.join(str(c)for c in children[:first]if isinstance(c,NavigableString));post=''.join(str(c)for c in children[first+1:]if isinstance(c,NavigableString))
   if re.sub(r'\s','',pre)==r'\eqalign{'and re.sub(r'\s','',post)=='}':skips.append({**row,'reason':'Only a redundant complete-formula eqalign wrapper was omitted'});continue
  record=values[row['entity'],row['attribute']];pieces=[{'span':[m.start(),m.end()],'key':audit.key(m[0]),'text':m[0]}for m in MATH.finditer(record['v'])];j=next(j for j,c in enumerate(pieces)if c['span']==row['span']);ak=(partid,row['entity'],row['attribute'])
  if ak not in aligns:
   f,b=matrix(len(source),len(pieces),source,pieces);aligns[ak]=(f,b)
  f,b=aligns[ak];score=f[-1][-1];options=[k for k,s in enumerate(source)if pieces[j]['key']in s and f[k][j]+1+b[k+1][j+1]==score];ratio=score/max(1,min(len(source),len(pieces)))
  skip_score=max(f[k][j]+b[k][j+1]for k in range(len(source)+1))
  if len(options)!=1 or options[0]!=i or ratio<.7 or skip_score==score:
   remaining.append({**row,'alignment_options':options,'alignment_score':score,'source_math_count':len(source),'current_math_count':len(pieces),'ratio':ratio});continue
  try:tex=reconstruct(title)
  except Exception as err:remaining.append({**row,'reason':str(err)});continue
  if audit.key(tex)==pieces[j]['key']:skips.append({**row,'reason':'Complete expression already present'});continue
  old=pieces[j]['text'];marker='$$'if old.startswith(('$$',r'\['))else'$';after=(marker+'\n'+tex+'\n'+marker)if marker=='$$'else'$'+tex+'$';out.append({**row,'after_formula':after,'matching':'unique-in-all-optimal-source-math-alignments','alignment_score':score,'source_math_count':len(source),'current_math_count':len(pieces)})
  if len(contexts)%100==0:print('Source contexts',len(contexts),'confirmed',len(out),'pending',len(remaining),flush=True)
 groups=collections.defaultdict(list)
 for r in out:groups[r['entity'],r['attribute'],tuple(r['span'])].append(r)
 resolved=[]
 for k,rows in groups.items():
  if len({audit.key(r['after_formula'])for r in rows})==1:resolved.append(rows[0])
  else:remaining.extend({**r,'reason':'Conflicting source reconstructions'}for r in rows)
 save('resolved.json',resolved);save('remaining.json',remaining);save('nondefects.json',skips);report={'confirmed_formulas':len(resolved),'fields':len({(r['entity'],r['attribute'])for r in resolved}),'remaining_unique_spans':len({(r['entity'],r['attribute'],tuple(r['span']))for r in remaining if'span'in r}),'nondefect_candidates':len(skips),'attributes':dict(collections.Counter(r['attribute']for r in resolved))};save('resolution-summary.json',report);print(report)
if __name__=='__main__':main()

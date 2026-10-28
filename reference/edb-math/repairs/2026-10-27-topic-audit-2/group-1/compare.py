import collections,difflib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,normalize_source_tex
D=json.loads((H/'current.json').read_text());S=json.loads((H/'sources.json').read_text());idx=collections.defaultdict(list)
for s in S:idx[s['identity'],s['attribute']].append(s)
def canon(v):
 v=normalize_source_tex(v);v=re.sub(r'\\color\{[^{}]+\}','',v);v=re.sub(r'\\(?:left|right|displaystyle|textstyle)|\\[,;!]','',v);v=re.sub(r'\\(?:mathbf|mathbb|mathrm|mathcal|mathit|textrm)\b','',v);v=v.replace('⁡','').replace('∼',r'\sim').replace('⟹',r'\Longrightarrow').replace('⟨',r'\langle').replace('⟩',r'\rangle').replace('∞',r'\infty').replace('∈',r'\in').replace('−','-').replace('×',r'\times').replace(r'\dfrac',r'\frac');v=re.sub(r'\s+|[{}]','',v);return v
records=[]
for obj,ident,attrs in [(c,'tutorial:'+str(c[':tutorial/math-academy-id']),['tutorial/content'])for c in D['contents']if':tutorial/content'in c]+[(q,q[':question/math-academy-id'],['question/problem','question/worked-solution'])for q in D['questions']if':question/math-academy-id'in q]:
 for a in attrs:
  v=obj.get(':'+a)
  if v is None:continue
  fs=[]
  for m in MATH.finditer(v):
   k=2 if m[0].startswith(('$$',r'\[',r'\('))else 1;fs.append(m[0][k:-k])
  cfs=list(map(canon,fs));opts=[]
  for s in idx[ident,a]:
   sfs=s['formulas'];cs=list(map(canon,sfs));score=difflib.SequenceMatcher(None,cfs,cs,autojunk=False).ratio();matches=sum(x==y for x,y in zip(cfs,cs))if len(cfs)==len(cs)else None
   opts.append({'path':s['path'],'formulas':sfs,'score':score,'equal_count':matches})
  best=max(opts,key=lambda x:x['score'])if opts else None
  records.append({'entity':obj[':db/id'],'identity':ident,'attribute':a,'current':fs,'best':best,'source_variants':len(opts)})
(H/'comparison.json').write_text(json.dumps(records,indent=2));print('records',len(records),'source present',sum(bool(r['best'])for r in records),'formula sequence exact canonical',sum(bool(r['best']and r['best']['score']==1)for r in records));print('tutorial comparisons')
for r in records:
 if r['identity'].startswith('tutorial:'):print(r['identity'],r['entity'],len(r['current']),None if not r['best']else(len(r['best']['formulas']),r['best']['score']))
print('high mismatch examples')
for r in records:
 if r['best']and r['best']['score']<1 and len(r['current'])==len(r['best']['formulas']) and not r['identity'].startswith('tutorial:'):
  print(r['identity'],r['attribute'],len(r['current']),round(r['best']['score'],2))

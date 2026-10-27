import json,re,sys,collections
from pathlib import Path
from bs4 import BeautifulSoup
R=Path.cwd();H=R/'reference/edb-math/repairs/2026-10-26-structural-math';W=R/'.local/edb/structural-math-2026-10-26'
ns={'__file__':str(H/'recover_formulas.py')};exec(compile((H/'recover_formulas.py').read_text().split('index=collections.defaultdict(list)')[0],str(H/'recover_formulas.py'),'exec'),ns);formulas=ns['formulas'];MATH=ns['MATH']
meta=json.loads((W/'metadata.json').read_text());parents=json.loads((W/'parents.json').read_text())
rows=json.loads(Path('/tmp/structural-pipe-extended.json').read_text());targets=[]
for d in rows:
 matches=[m for m in MATH.finditer(d['v']) if m[0] in d['suspicious_math']]
 if matches:targets.append((d,matches))
print('target fields',len(targets),flush=True)
def identities(d):
 m=meta.get(str(d['e']),{})
 if d['a']=='tutorial/content':return ['tutorial:'+str(m.get('tutorial/math-academy-id'))]
 if d['a']=='answer/value':return [meta.get(str(q),{}).get('question/math-academy-id')for f,a in parents.get(str(d['e']),[])if a=='answer-field/choices'for q,a in parents.get(str(f),[])if a=='question/answer-fields']
 return [m.get('question/math-academy-id')]
wanted={(i,d['a'])for d,ms in targets for i in identities(d)if i};index=collections.defaultdict(list)
for src in json.loads(Path('/tmp/structural-pipe-source-index.json').read_text()):index[src['identity'],src['attribute']].append({k:v for k,v in src.items()if k not in ('identity','attribute')})
cached=set(index)
def slim(raw):return re.sub(r'<svg\b[\s\S]*?</svg>',lambda m:'<svg>'+''.join(re.findall(r'<title\b[^>]*>[\s\S]*?</title>',m[0],re.I))+'</svg>',raw,flags=re.I)
domcache={}
def captured(raw,identity,path,rootid=None):
 if not raw:return
 key=str(path)
 if key not in domcache:domcache.clear();domcache[key]=BeautifulSoup(slim(raw),'html.parser')
 soup=domcache[key];root=soup.find(id=rootid)if rootid else soup
 if root is None:return
 if identity.startswith('tutorial:'):parts=[('tutorial/content',root)]
 else:parts=[(a,n)for a,classes in [('question/problem',['exampleQuestion','questionWidget-text','questionText']),('question/worked-solution',['exampleExplanation','questionExplanation','questionWidget-explanation']),('answer/value',['questionWidget-choiceText','choiceText','selectListOption'])]for c in classes for n in root.find_all(class_=c)]
 for a,n in parts:
  if(identity,a)in wanted and(identity,a)not in cached:index[identity,a].append({'path':str(path),'html':str(n)})
for p in Path('/home/jake/Developer/MA/DATA/Lessons').glob('*/Source/*.json'):
 data=json.loads(p.read_text());use=[]
 for i in data.get('lesson',{}).get('items',[]):
  identity=('tutorial:'+str(i['content_id'])if i.get('step_type')=='tutorial'else'e-'+str(i['content_id']))if i.get('item_type')=='step'else'q-'+str(i['question_id'])if i.get('question_id')else None
  if any(ident==identity and(ident,a)not in cached for ident,a in wanted):use.append((i,identity))
 if use and p.with_suffix('.html').exists():
  raw=p.with_suffix('.html').read_text()
  for i,identity in use:captured(raw,identity,p.with_suffix('.html'),i.get('dom_id'))
for line in (R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);mt=re.search(r'(q-\d+)-(?:before|after)\.json$|history-(q-\d+)\.json$|example-(\d+)\.json$',p.name)
 if not mt:continue
 identity=mt[1]or mt[2]or'e-'+mt[3]
 if not any(ident==identity and(ident,a)not in cached for ident,a in wanted):continue
 if not p.is_absolute():p=R/p
 if p.exists():
  data=json.loads(p.read_text());captured(data.get('html')or data.get('raw_html'),identity,p)
Path('/tmp/structural-pipe-source-index.json').write_text(json.dumps([{'identity':i,'attribute':a,**v}for(i,a),items in index.items()for v in items]))
def sig(s):
 s=re.sub(r'\\(?:begin|end)\{[^{}]+\}(?:\{[clr| ]+\})?','',s)
 s=re.sub(r'\\\\(?:\[[^]]*\])?','',s)
 s=re.sub(r'\\(?:displaystyle|textstyle|left|right|big|Big|bigg|Bigg|quad|qquad|,|;|!)\b','',s)
 s=s.replace(r'\dfrac',r'\frac').replace(r'\mid','|').replace(r'\vert','|').replace('−','-')
 s=re.sub(r'[\s$;|&{}()]','',s)
 return s
proposals=[];unresolved=[]
cache={}
for d,ms in targets:
 opts=[]
 for ident in identities(d):
  for src in index.get((ident,d['a']),[]):
   k=src['html'];fs=cache.setdefault(k,formulas(k));changes=[]
   for m in ms:
    found=[f for f in fs if isinstance(f,str)and sig(m[0])==sig(f)and r'\begin{'in f]
    found=set(found)
    if len(found)==1:
     f=next(iter(found));changes.append({'span':[m.start(),m.end()],'before':m[0],'after':('$$\n'+f+'\n$$')if m[0].startswith('$$')else'$'+f+'$'})
   if changes:opts.append({'entity':d['e'],'attribute':d['a'],'identity':ident,'source_path':src['path'],'before':d['v'],'changes':changes})
 unique={json.dumps(o['changes'],sort_keys=True):o for o in opts}
 if len(unique)==1:proposals.append(next(iter(unique.values())))
 else:unresolved.append({'entity':d['e'],'attribute':d['a'],'identities':identities(d),'source_options':sum(len(index.get((i,d['a']),[]))for i in identities(d)),'matching_options':len(unique),'before':d['v']})
Path('/tmp/structural-pipe-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');Path('/tmp/structural-pipe-unresolved.json').write_text(json.dumps(unresolved,indent=2)+'\n')
print('proposed fields',len(proposals),'formula blocks',sum(len(o['changes'])for o in proposals),'unresolved',len(unresolved),flush=True)
for o in proposals:
 print(o['entity'],o['attribute'],o['identity'],[(x['before'][:160],x['after'][:160])for x in o['changes']],flush=True)

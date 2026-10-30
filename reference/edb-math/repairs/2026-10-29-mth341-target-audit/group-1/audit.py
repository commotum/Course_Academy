import json,re,sys,collections,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,validate_math_structure,validate_tex,normalize_source_tex,normalize_matrix_answer_tables
p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';s=p.read_text();ns={'__file__':str(p)};exec(compile(s.split('parents=json.loads')[0]+s[s.index('def roots(s):'):s.index('def visible(tex):')],str(p),'exec'),ns)
D=json.loads((H/'current.json').read_text());Q=D['questions'];byid={q.get(':question/math-academy-id'):q for q in Q if q.get(':question/math-academy-id')};sources=collections.defaultdict(list)
def slim(s):return re.sub(r'<svg\b[\s\S]*?</svg>',lambda m:'<svg>'+''.join(re.findall(r'<title\b[^>]*>[\s\S]*?</title>',m[0],re.I))+'</svg>',s,flags=re.I)
def parts(root,ident,path):
 if ident.startswith('tutorial:'):sets=[('tutorial/content',[root])]
 else:
  sets=[]
  for a,classes in [('question/problem',['exampleQuestion','questionWidget-text','questionText']),('question/worked-solution',['exampleExplanation','questionExplanation','questionWidget-explanation']),('answer/value',['questionWidget-choiceText','choiceText','selectListOption'])]:
   found=[]
   for cls in classes:found+=root.find_all(class_=cls)
   if found:sets.append((a,found))
 for a,nodes in sets:
  for n in nodes:
   # Ignore duplicate nested question-widget wrappers.
   if any(x is not n and x in n.parents for x in nodes):continue
   formulas=ns['formulas'](str(n));sources[ident,a].append({'path':str(path),'formulas':formulas,'html':str(n)})
for t in D['topics']:
 path=Path('/home/jake/Developer/MA/DATA/Lessons')/str(t['ma_id'])/'Source'/f'{t["ma_id"]}.html'
 if not path.exists():continue
 soup=BeautifulSoup(slim(path.read_text()),'html.parser');meta=json.loads(path.with_suffix('.json').read_text())
 for i in meta.get('lesson',{}).get('items',[]):
  ident=('tutorial:'+str(i['content_id'])if i.get('step_type')=='tutorial'else'e-'+str(i['content_id']))if i.get('item_type')=='step'else'q-'+str(i['question_id'])if i.get('question_id')else None
  if not ident:continue
  root=soup.find(id=i.get('dom_id'))
  if root:parts(root,ident,path)
paths=[]
for line in (R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);m=re.search(r'(q-\d+)-(?:before|after)\.json$|history-(q-\d+)\.json$|example-(\d+)\.json$',p.name)
 if m and(m[1]or m[2]or'e-'+m[3])in byid:paths.append((m[1]or m[2]or'e-'+m[3],p if p.is_absolute()else R/p))
seen=set()
for ident,p in paths:
 if (ident,str(p))in seen or not p.exists():continue
 seen.add((ident,str(p)));data=json.loads(p.read_text());html=data.get('html')or data.get('raw_html')
 if html:parts(BeautifulSoup(slim(html),'html.parser'),ident,p)
print('sources',len(seen),len(sources),flush=True)
(H/'sources.json').write_text(json.dumps([{'identity':i,'attribute':a,**v}for(i,a),vs in sources.items()for v in vs],indent=2)+'\n')
fields=[];issues=[]
for c in D['contents']:
 if ':tutorial/content'in c:fields.append((c[':db/id'],'tutorial/content',c[':tutorial/content'],'tutorial:'+str(c[':tutorial/math-academy-id']),False))
for q in Q:
 ident=q.get(':question/math-academy-id')
 for a in ['question/problem','question/worked-solution']:
  if ':'+a in q:fields.append((q[':db/id'],a,q[':'+a],ident,False))
 if not q.get(':question/worked-solution'):issues.append({'entity':q[':db/id'],'identity':ident,'issue':'missing-solution','fields':len(q.get(':question/answer-fields',[]))})
 for f in q.get(':question/answer-fields',[]):
  if not f.get(':answer-field/correct'):issues.append({'entity':q[':db/id'],'field':f[':db/id'],'identity':ident,'issue':'missing-key','choices':len(f.get(':answer-field/choices',[]))})
  for a in f.get(':answer-field/choices',[]):
   if ':answer/value'in a:fields.append((a[':db/id'],'answer/value',a[':answer/value'],ident,a.get(':answer/type',{}).get(':db/ident')==':answer.type/math'))
   if ':answer/feedback'in a:fields.append((a[':db/id'],'answer/feedback',a[':answer/feedback'],ident,False))
fields=list({(f[0],f[1]):f for f in fields}.values())
def canon(s):
 s=re.sub(r'\\color\{[^{}]+\}','',s);s=re.sub(r'\\(?:left|right|displaystyle|textstyle)\b|\\[,;!]|\\hspace\{[^{}]*\}','',s);s=s.replace(r'\times',r'\cdot').replace(r'\dfrac',r'\frac').replace('⁡','').replace('−','-');return re.sub(r'\s|[{}]','',s)
report=[];diffs=[]
for e,a,v,ident,bare in fields:
 errors=[]
 try:validate_tex(v)if bare else validate_math_structure(v)
 except Exception as ex:errors.append(str(ex));issues.append({'entity':e,'attribute':a,'identity':ident,'issue':'validation','message':str(ex),'value':v})
 ms=[v]if bare else[m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1]for m in MATH.finditer(v)]
 opts=sources[ident,a]; attempts=[]
 for src in opts:
  fs=src['formulas'];ok=all(isinstance(f,str)for f in fs)
  if not ok:continue
  score=sum(canon(x)==canon(y)for x,y in zip(ms,fs)) if len(ms)==len(fs)else -1
  attempts.append((score,src))
 exact=next((s for score,s in attempts if score==len(ms)),None)
 best=max(attempts,key=lambda a:a[0],default=(None,None));r={'entity':e,'attribute':a,'identity':ident,'bare':bare,'math_count':len(ms),'sources':len(opts),'matched':bool(exact),'best_score':best[0],'errors':errors};report.append(r)
 if best[1]and (not exact or any('\\color'in s and '\\color'not in c for c,s in zip(ms,best[1]['formulas']))):diffs.append({**r,'before':v,'math':ms,'source':best[1]})
 if a=='question/problem'and normalize_matrix_answer_tables(v)!=v:issues.append({'entity':e,'attribute':a,'issue':'matrix-answer-table','value':v,'after':normalize_matrix_answer_tables(v)})
(H/'field-audit.json').write_text(json.dumps(report,indent=2)+'\n');(H/'issues.json').write_text(json.dumps(issues,indent=2)+'\n');(H/'source-differences.json').write_text(json.dumps(diffs,indent=2)+'\n');(H/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');print('fields',len(fields),'diffs',len(diffs),'issues',len(issues));print(collections.Counter(d['issue']for d in issues));print('source matching',sum(r['matched']for r in report))

import collections,copy,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
p=R/'reference/edb-math/repairs/2026-10-26-structural-math/recover_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('index=collections.defaultdict(list)')[0],str(p),'exec'),ns)
p=H/'propose_formulas.py';cs={'__file__':str(p)};exec(compile(p.read_text().split('props=[]')[0],str(p),'exec'),cs);canon=cs['canonical']
D=json.loads((H/'current.json').read_text());targets={q[':question/math-academy-id']:q for q in D['questions']if':question/math-academy-id'in q};sourcebanks=collections.defaultdict(list)
def add(ident,node,path):
 if node is None:return
 choices=node.select('.questionWidget-choiceText')or node.select('.questionChoiceText')
 if not choices:return
 bank=[]
 for choice in choices:
  roots=ns['roots'](choice);fs=ns['formulas'](str(choice));bare=len(roots)==len(fs)==1
  for root,f in zip(roots,fs):
   if isinstance(f,str):root.replace_with('$'+f+'$')
  text=choice.get_text(' ',strip=True);bank.append({'value':fs[0]if bare and text.strip()==('$'+fs[0]+'$')else text,'math':bare and text.strip()==('$'+fs[0]+'$'),'html':str(choice)})
 key=json.dumps(bank,sort_keys=True)
 if not any(x['signature']==key for x in sourcebanks[ident]):sourcebanks[ident].append({'path':str(path),'choices':bank,'signature':key})
for t in D['topics']:
 p=Path('/home/jake/Developer/MA/DATA/Lessons')/str(t['ma_id'])/'Source'/f"{t['ma_id']}.html"
 if not p.exists():continue
 s=BeautifulSoup(p.read_text(),'html.parser');m=json.loads(p.with_suffix('.json').read_text())
 for i in m['lesson']['items']:
  ident=('e-'+str(i['content_id']))if i.get('step_type')=='example'else'q-'+str(i['question_id'])if i.get('question_id')else None
  if ident in targets:add(ident,s.find(id=i['dom_id']),p)
for line in(R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);m=re.search(r'(q-\d+)-(?:before|after)\.json$|history-(q-\d+)\.json$|example-(\d+)\.json$',p.name)
 if not m:continue
 ident=m[1]or m[2]or'e-'+m[3]
 if ident not in targets:continue
 p=p if p.is_absolute()else R/p
 if not p.exists():continue
 try:d=json.loads(p.read_text())
 except Exception:continue
 html=d.get('html')or d.get('raw_html')
 if html:add(ident,BeautifulSoup(html,'html.parser'),p)
report=[];props=[]
def key(v):return canon(v.replace('$','')).replace(r'\!','')
for ident,q in targets.items():
 for field in q.get(':question/answer-fields',[]):
  if field[':answer-field/type'][':db/ident']not in [':answer-field.type/radio',':answer-field.type/select']:continue
  bank=field.get(':answer-field/choices',[]);attempts=[]
  for source in sourcebanks[ident]:
   sourcechoices=source['choices'];matches=[]
   for a in bank:
    candidates=[s for s in sourcechoices if key(s['value'])==key(a[':answer/value'])];matches.append({'answer':a[':db/id'],'matches':candidates})
   attempts.append({'source':source,'matches':matches,'matched':sum(len(m['matches'])==1 for m in matches)})
  best=max(attempts,key=lambda a:a['matched'])if attempts else None
  report.append({'question':q[':db/id'],'identity':ident,'field':field[':db/id'],'choices':len(bank),'source_path':best['source']['path']if best else None,'unique_matching_values':best['matched']if best else 0,'source_options':len(attempts),'unmatched':[a for a,m in zip(bank,best['matches'])if len(m['matches'])!=1]if best else []})
  if best:
   for a,m in zip(bank,best['matches']):
    if len(m['matches'])!=1:continue
    src=m['matches'][0]['value'];old=a[':answer/value']
    if a[':answer/type'][':db/ident']!=':answer.type/math':continue
    if old.count(r'\{')>=src.count(r'\{'):continue
    props.append({'entity':a[':db/id'],'attribute':'answer/value','before':old,'after':src,'reason':'Source choice has visible set braces lost to TeX grouping braces in imported answer value. Mathematical entries and order match.','evidence':{'basis':9047,'question':q[':db/id'],'field':field[':db/id'],'identity':ident,'source_path':best['source']['path'],'check':'Unique full mathematical-token match after removing styles and invisible group braces.'},'confidence':'high','requires_parent_history_review':True})
(H/'source-choice-banks.json').write_text(json.dumps(sourcebanks,indent=2));(H/'choice-source-comparison.json').write_text(json.dumps(report,indent=2));(H/'answer-format-proposals.json').write_text(json.dumps(props,indent=2));print('banks',len(report),'source banks',sum(bool(r['source_path'])for r in report),'all values matched',sum(r['choices']==r['unique_matching_values']for r in report),'answer set-brace proposals',len(props));print('unmatched',[(r['identity'],r['unique_matching_values'],r['choices'])for r in report if r['source_path']and r['choices']!=r['unique_matching_values']])

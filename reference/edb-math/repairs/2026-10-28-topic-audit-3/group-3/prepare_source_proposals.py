import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
sys.path.insert(0,'scripts');from question_capture.math_format import MATH,normalize_source_tex,validate_math_structure
from import_historical_question_content import Renderer
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());F={(f['entity'],f['attribute']):f for f in json.loads((H/'fields.json').read_text())};S=json.loads((H/'source-records.json').read_text());M=json.loads((H/'source-manifest.json').read_text());props={};unresolved=[]
FONT=r'\\(?:mathbf|mathbb|mathcal|mathfrak|mathit|boldsymbol|overrightarrow|vec|widehat)'
def core(t):
 t=normalize_source_tex(t).replace('⁡','').replace('′',"'");t=re.sub(r'([A-Z]{2})\^\(→\)',r'\1',t);t=re.sub(r'\\(?:[,;:! ]|left|right)\s*','',t);t=re.sub(r'\\hspace\{[^{}]*\}|\\color\{[^{}]*\}','',t);t=re.sub(r'\\(?:mathbf|mathbb|mathcal|mathfrak|mathit|boldsymbol|overrightarrow|vec|widehat|mathrm|textrm|text|operatorname)','',t);t=re.sub(r'\\(?:ln|sin|cos|tan|arcsin|arccos|arctan)',lambda m:m[0][1:],t);t=t.replace(r'\{','').replace(r'\}','');return re.sub(r'[{}\s$]','',t)
def mathvalues(v):return [m[0][2:-2]if m[0].startswith(('$$',r'\[',r'\('))else m[0][1:-1]for m in MATH.finditer(v)]
def role_missing(old,new):
 return len(re.findall(FONT,new))>len(re.findall(FONT,old))or len(re.findall(r'\\[{}]',new))>len(re.findall(r'\\[{}]',old))or len(re.findall(r'\\color\{',new))>len(re.findall(r'\\color\{',old))
def propose(e,a,after,reason,evidence):
 before=F[e,a]['value'];assert sorted(re.findall(r'\{\{[^{}]+\}\}',before))==sorted(re.findall(r'\{\{[^{}]+\}\}',after));validate_math_structure(after,bare_math=F[e,a]['bare']);props[e,a]={'entity':e,'attribute':a,'before':before,'after':after,'reason':reason,'evidence':evidence,'confidence':'high'}
options=collections.defaultdict(dict)
for s in S:
 e,a=s['entity'],s['attribute'];old=mathvalues(F[e,a]['value']);new=s['formulas'];changes={}
 if len(old)!=len(new):
  for i,x in enumerate(old):
   ys={y for y in new if core(x)==core(y)and role_missing(x,y)and len(re.findall(FONT,y))+len(re.findall(r'\\[{}]',y))>len(re.findall(FONT,x))+len(re.findall(r'\\[{}]',x))}
   if len(ys)==1:changes[i]=next(iter(ys))
 for i,(x,y)in enumerate(zip(old,new))if len(old)==len(new)else[]:
  if core(x)==core(y)and role_missing(x,y):changes[i]=y
 if not changes:continue
 after=F[e,a]['value'];ms=list(MATH.finditer(after))
 for i,v in reversed(list(changes.items())):
  m=ms[i];after=after[:m.start()]+('$$\n'+v+'\n$$'if m[0].startswith('$$')else'$'+v+'$')+after[m.end():]
 options[e,a][after]={'path':s['path'],'source_identity':s['source_identity'],'formula_indices':list(changes)}
for key,opts in options.items():
 if len(opts)==1:
  after,ev=next(iter(opts.items()));propose(*key,after,'Recover mathematical font roles, visible set braces, and instructional highlighting from the retained original source.',ev)
 else:unresolved.append({'entity':key[0],'attribute':key[1],'reason':'source alternatives differ','variants':len(opts)})
# Original choice HTML retains fonts that earlier normalized capture values lost.
bankreport=[];keyreport=[];sourcecache=[]
for q in D['questions']:
 sid=q.get(':question/math-academy-id');paths=[p for p in M.get(sid,[])if p.endswith('.json')]
 if not paths:continue
 chosen=next((p for p in paths if p.endswith('-before.json')),paths[0]);raw=json.loads(Path(chosen).read_text());rr=Renderer(None);candidates=collections.defaultdict(list)
 for sf in raw.get('fields',[]):
  for choice in sf.get('choices',[]):
   html=choice.get('html');value=rr.text(BeautifulSoup(html,'html.parser'))if html else choice.get('value','');candidates[sf['key']].append({'value':value,'role':'source choice','html':html})
 statements=[]
 soup=BeautifulSoup(raw.get('html')or raw.get('raw_html')or'','html.parser')
 for li in soup.select('.questionStatements > li'):statements.append({'value':re.sub(r'^-\s*','',rr.text(li)),'role':'source statement','html':str(li)})
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/id']==17592186408166:
   matches=[c for c in statements if core(c['value'])==core(f[':answer-field/key'])];keyreport.append({'entity':f[':db/id'],'question':q[':db/id'],'source':sid,'path':chosen,'matches':matches})
   if len({m['value']for m in matches})==1 and role_missing(f[':answer-field/key'],matches[0]['value']):propose(f[':db/id'],'answer-field/key',matches[0]['value'],'Restore the retained original statement notation in the checkbox label.',{'path':chosen,'question':q[':db/id'],'source_identity':sid,'source_statement':matches[0]['value']})
  for answer in f.get(':answer-field/choices',[]):
   candidates_here=candidates[f[':answer-field/key']];matches=[c for c in candidates_here if core(c['value'])==core(answer[':answer/value'])];bankreport.append({'entity':answer[':db/id'],'field':f[':db/id'],'question':q[':db/id'],'source':sid,'path':chosen,'source_candidates':len(candidates_here),'normalized_matches':len(matches)})
   afters={c['value']:c for c in matches if role_missing(answer[':answer/value'],c['value'])}
   if len(afters)==1:
    after=next(iter(afters));bare=answer[':answer/type'][':db/id']==17592186045498
    if bare and len(list(MATH.finditer(after)))==1 and MATH.fullmatch(after):after=after[2:-2]if after.startswith('$$')else after[1:-1]
    # Mixed prose incorrectly typed as math is handled in the dedicated bank repair.
    if bare and '$'in after:continue
    propose(answer[':db/id'],'answer/value',after,'Recover the original mathematical font role or visible set braces in the choice.',{'path':chosen,'question':q[':db/id'],'source_identity':sid,'field':f[':db/id']})
 sourcecache.append({'question':q[':db/id'],'source_identity':sid,'path':chosen,'statements':statements,'choices':dict(candidates),'errors':rr.errors})
# Display standalone integral calculations while retaining prose references inline.
for (e,a),f in F.items():
 if a not in ('question/problem','question/worked-solution','tutorial/content'):continue
 text=props.get((e,a),{}).get('after',f['value']);changes=[]
 for m in MATH.finditer(text):
  if m[0].startswith(('$$',r'\['))or r'\int'not in m[0]:continue
  start=text.rfind('\n\n',0,m.start())+2;end=text.find('\n\n',m.end());end=end if end>=0 else len(text);para=text[start:m.start()]+text[m.end():end];para=re.sub(r'\{\{[^{}]+\}\}','',para).strip()
  if re.fullmatch(r'(?i)(?:(?:calculate|evaluate|compute|find|what is)(?: the)?(?: indefinite| definite)?(?: integral)?)?[\s?.:]*',para):changes.append(m)
 if changes:
  after=text
  for m in reversed(changes):after=after[:m.start()]+'\n\n$$\n'+m[0][1:-1]+'\n$$\n\n'+after[m.end():]
  after=re.sub(r'\n{3,}','\n\n',after).strip();ev=props.get((e,a),{}).get('evidence',{});ev['standalone_integrals_displayed']=len(changes);propose(e,a,after,'Display standalone integral calculations; preserve prose references and original mathematical content.',ev)
(H/'proposals.json').write_text(json.dumps(list(props.values()),indent=2));(H/'source-bank-comparisons.json').write_text(json.dumps(bankreport,indent=2));(H/'checkbox-source-comparisons.json').write_text(json.dumps(keyreport,indent=2));(H/'source-choice-cache.json').write_text(json.dumps(sourcecache,indent=2));(H/'source-proposal-unresolved.json').write_text(json.dumps(unresolved,indent=2));print('proposals',len(props),collections.Counter(p['attribute']for p in props.values()),'sourcebanks',len(bankreport),'checkboxlabelscompared',len(keyreport),'unresolved',len(unresolved))

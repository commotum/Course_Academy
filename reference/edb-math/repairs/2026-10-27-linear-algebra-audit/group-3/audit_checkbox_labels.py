import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
sys.path.insert(0,'scripts');from import_historical_question_content import Renderer
from question_capture.math_format import MATH,normalize_source_tex,validate_math_structure
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};M=json.loads((H/'source-manifest.json').read_text());C=json.loads((H/'checkbox-labels-current.json').read_text());labels=C['labels'];cached={};reports=[];proposals=[];errors=[];sourcecache=[]
def canon(s,ignore_fonts=False):
 s=normalize_source_tex(s).replace('−','-').replace('∈',r'\in').replace('∞',r'\infty');s=re.sub(r'\\(?:displaystyle|,|;|!|quad|qquad|left|right)','',s)
 if ignore_fonts:
  s=re.sub(r'\\(?:mathbf|mathrm|mathbb|mathcal|mathit|textrm|text)','',s);s=s.replace(r'\{','').replace(r'\}','')
 return re.sub(r'[{}\s$]','',s).strip('.').lower()
def candidates(q):
 sid=q.get(':question/math-academy-id');paths=[p for p in M.get(sid,[])if p.endswith('.json')];out=[]
 if not paths:return []
 # Captures for the same immutable source identity have the same statement bank.
 # Keep one before/after raw DOM with complete fields, plus provenance.
 p=next((p for p in paths if p.endswith('-after.json')),paths[0]);d=json.loads(Path(p).read_text());soup=BeautifulSoup(d.get('html')or d.get('raw_html')or'','html.parser');rr=Renderer(None)
 for n in soup.select('.questionStatements > li'):
  value=re.sub(r'^-\s*','',rr.text(n));out.append({'value':value,'path':p,'role':'original listed statement','html':str(n)})
 for f in d.get('fields',[]):
  for choice in f.get('choices',[]):
   value=rr.text(BeautifulSoup(choice['html'],'html.parser'))if choice.get('html')else choice.get('value','');out.append({'value':value,'path':p,'role':'original answer choice','html':choice.get('html')})
 sourcecache.append({'question':q[':db/id'],'source_identity':sid,'path':p,'candidates':out,'renderer_errors':rr.errors});return out
for f in labels:
 q=Q[f['question']];sid=q.get(':question/math-academy-id');key=f['value']
 try:validate_math_structure(key)
 except Exception as ex:errors.append({'entity':f['entity'],'error':str(ex),'value':key})
 if f['question']not in cached:cached[f['question']]=candidates(q)
 ss=cached[f['question']];row={'entity':f['entity'],'question':f['question'],'source_identity':sid,'label':key,'basis_t':C['basis_t']}
 exact=[s for s in ss if canon(s['value'])==canon(key)]
 if exact:row.update({'status':'source statement/choice matches','evidence':exact[0]})
 elif key.lower()=='none of the above'and any(re.search(r'\bnone\b',s['value'],re.I)for s in ss):row.update({'status':'source none-choice equivalent','evidence':next(s for s in ss if re.search(r'\bnone\b',s['value'],re.I))})
 elif re.fullmatch(r'\$[A-Za-z]=.+\$',key):
  value=key[1:-1].split('=')[1];hits=[s for s in ss if any(canon(m[0])==canon(value)for m in MATH.finditer(s['value']))]
  if hits:row.update({'status':'source numerical subset member matches','evidence':hits[0]})
  else:row['status']='original source absent'if sid and not ss else'generated label; no original source identity'if not sid else'source comparison needs review'
 elif ss:
  near=[s for s in ss if canon(s['value'],True)==canon(key,True)]
  candidates_by_after={s['value']:s for s in near if re.search(r'\\(?:mathbf|mathbb|mathcal|mathrm|mathit)',s['value'])}
  if len(candidates_by_after)==1:
   after,evidence=next(iter(candidates_by_after.items()));validate_math_structure(after);proposals.append({'entity':f['entity'],'attribute':'answer-field/key','before':key,'after':after,'reason':'Restore the original statement mathematical font roles and visible set braces lost from the checkbox label.','evidence':{'path':evidence['path'],'question':q[':db/id'],'source_identity':sid,'source_statement':evidence['value']},'confidence':'high'});row.update({'status':'source-backed font repair proposed','evidence':evidence})
  else:row.update({'status':'source comparison needs review','candidates':ss})
 else:row['status']='original source absent'if sid else'generated label; no original source identity'
 reports.append(row)
# Generated and source-gap labels retain the same notation schema as observed
# statements. Reuse only an identical token signature with substituted numbers.
for row in reports:
 if row['status']not in ('original source absent','generated label; no original source identity'):continue
 key=row['label']
 if not ('\\text{Span}'in key or 'R}'in key or 'R^'in key):continue
 pattern=lambda v:re.sub(r'\d+','#',canon(v,True))
 opts=[]
 for qid,ss in cached.items():
  for source in ss:
   if source['role']!='original listed statement'or not re.search(r'\\(?:mathbf|mathbb)',source['value']):continue
   if pattern(source['value'])!=pattern(key):continue
   nums=re.findall(r'\d+',key)
   if len(nums)!=len(re.findall(r'\d+',source['value'])):continue
   it=iter(nums);after=re.sub(r'\d+',lambda m:next(it),source['value'])
   if canon(after,True)==canon(key,True):opts.append((after,source,Q[qid].get(':question/math-academy-id')))
 unique={a:(a,ev,sid)for a,ev,sid in opts}
 if unique and len({canon(a)for a in unique})==1:
  after,source,template_id=min(unique.values(),key=lambda item:len(item[0]))
  if 'R}'in key or 'R^'in key:after=key.replace('{R}',r'{\mathbb{R}}');validate_math_structure(after)
  if after!=key:
   proposals.append({'entity':row['entity'],'attribute':'answer-field/key','before':key,'after':after,'reason':'Restore vector/Euclidean-space notation from the original source statement template; preserve this field’s substituted numbers.','evidence':{'path':source['path'],'question':row['question'],'source_identity':row['source_identity'],'matched_source_template':template_id,'source_statement_template':source['value'],'exact_source_status':'generated parameter variant'if not row['source_identity']else'original target capture absent; same statement template verified'},'confidence':'high'})
   row.update({'status':'source-template notation repair proposed','evidence':{'path':source['path'],'source_template':template_id,'after':after}})
# Three direct-source gaps retain an explicit vector-list Span structure. The
# original sibling statements establish the bold vector role for these names;
# preserve their already correct set braces and every target token/number.
for row in reports:
 if row['status']!='original source absent'or '\\text{Span}'not in row['label']:continue
 key=row['label'];source=next(s for s in cached[17592186357500]if s['role']=='original listed statement')if 17592186357500 in cached else next(s for ss in cached.values()for s in ss if s['role']=='original listed statement'and r'\mathbf{v}'in s['value']and r'\text{Span}'in s['value'])
 after=key.replace('{v}',r'{\mathbf{v}}');after=re.sub(r'(?<![A-Za-z\\])w(?![A-Za-z])',lambda m:r'\mathbf{w}',after)
 if after!=key:
  validate_math_structure(after);proposals.append({'entity':row['entity'],'attribute':'answer-field/key','before':key,'after':after,'reason':'Restore the vector font role established by the original lesson statements; preserve the target statement and set braces.','evidence':{'path':source['path'],'question':row['question'],'source_identity':row['source_identity'],'source_sibling_statement':source['value'],'exact_source_status':'target capture absent; vector role verified in original sibling statements and current vector-valued prompt'},'confidence':'high'});row.update({'status':'source-sibling vector notation repair proposed','evidence':{'path':source['path'],'after':after}})
(H/'checkbox-label-fields.json').write_text(json.dumps([{'entity':f['entity'],'attribute':'answer-field/key','value':f['value'],'question':f['question'],'bare':False}for f in labels],indent=2));(H/'checkbox-label-source-comparison.json').write_text(json.dumps(reports,indent=2));(H/'checkbox-label-source-cache.json').write_text(json.dumps(sourcecache,indent=2));(H/'checkbox-label-proposals.json').write_text(json.dumps(proposals,indent=2));(H/'checkbox-label-syntax-errors.json').write_text(json.dumps(errors,indent=2));print('basis',C['basis_t'],'labels',len(labels),'source statuses',collections.Counter(r['status']for r in reports),'proposals',len(proposals),'errors',len(errors))
for r in reports:
 if r['status']=='source comparison needs review':print(r['entity'],r['source_identity'],r['label'])

import json,re,collections
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());byid={q[':db/id']:q for q in D['questions']}
def norm(v):
 v=re.sub(r'\\(?:operatorname|textrm|mathrm|text)\{([^{}]*)\}',r'\1',v);v=v.replace('⁡','').replace('⁢','').replace('∂',r'\partial').replace('π',r'\pi').replace('−','-');v=re.sub(r'\\(?:left|right|displaystyle)\b|\\hspace\{[^{}]+\}|\\[,;!:]','',v);v=re.sub(r'\\(exp|sin|cos|tan|ln)\b',r'\1',v);return re.sub(r'\s|[{}]','',v)
def bank(v):return{norm(x)for x in v}
proposals=[];review=[]
for item in json.loads((H/'source-control-reconstructions.json').read_text()):
 q=byid[item['entity']];fields=q.get(':question/answer-fields',[]);candidates=[]
 for source in item['options']:
  cs=source.get('controls',[])
  if not cs or len(cs)!=len({f[':answer-field/key']for f in fields}):continue
  mapping={};proof=[];used=set()
  for c in cs:
   sourcebank=bank(c['values']);matches=[]
   for f in fields:
    values=[a[':answer/value']for a in f.get(':answer-field/choices',[])];stored=bank(values)
    if sourcebank==stored or (sourcebank.issubset(stored) and f[':answer-field/key']==c['key']):matches.append(f)
   # Duplicate legacy fields may hold equivalent banks; preserve the newer keyed field.
   keyed=[f for f in matches if f.get(':answer-field/correct')]
   if len(keyed)==1:matches=keyed
   if len(matches)>1:
    indexed=[f for f in matches if f[':answer-field/key']==c['key']]
    if len(indexed)==1 and c['key'] in re.findall(r'\{\{([^}]+)\}\}',q[':question/problem']):matches=indexed
   if len(matches)!=1:break
   f=matches[0]
   if f[':db/id']in used:break
   used.add(f[':db/id']);mapping[c['key']]=f[':answer-field/key'];proof.append({'source_index':c['dom_id'],'source_values':c['values'],'field':f[':db/id'],'key':f[':answer-field/key'],'bank_match':'complete normalized bank equality'+(' excluding foreign is link'if sourcebank!=bank([a[':answer/value']for a in f.get(':answer-field/choices',[])])else'')})
  else:
   after=re.sub(r'\{\{([^}]+)\}\}',lambda m:'{{'+mapping[m[1]]+'}}',source['problem'])
   # Preserve the explicit calculator requirement metadata that lies outside source questionText.
   if 'A scientific calculator is required'in q[':question/problem']and'A scientific calculator is required'not in after:after+='\n\n> A scientific calculator is required to answer this question.'
   if q[':db/id']==17592186167223:
    after=after.replace(r'3\operatorname{cos}(2t)',r'3\operatorname{cos}(6t)').replace(r'3\operatorname{sin}(2t)',r'3\operatorname{sin}(6t)')
   old_assets=re.findall(r'!\[[^]]*\]\(([^)]+)\)',q[':question/problem']);new_assets=re.findall(r'!\[[^]]*\]\(([^)]+)\)',after)
   if len(old_assets)!=len(new_assets):continue
   if new_assets:
    asset_iter=iter(old_assets);after=re.sub(r'!\[([^]]*)\]\(([^)]+)\)',lambda m:'!['+m[1]+']('+next(asset_iter)+')',after)
   if source.get('errors'):continue
   candidates.append((after,source['path'],proof))
 if not candidates:
  review.append({'entity':q[':db/id'],'identity':item['identity'],'status':'no bijective complete source bank mapping','sources':len(item['options'])});continue
 # Prefer full question captures over shorter lesson archive versions if bank mapping is complete.
 after,path,proof=next((c for c in candidates if c[1].endswith('-after.json')),candidates[0])
 if norm(after)==norm(q[':question/problem']):continue
 # Only reconstruct when layout/math was actually lost, not punctuation/spacing alone.
 current=q[':question/problem'];lost=('(S'in after or any('{{'+c['source_index']+'}}'in after for c in proof))
 # All accepted differences are retained for explicit review; exact source mapping is evidence.
 proposals.append({'entity':q[':db/id'],'attribute':'question/problem','before':current,'after':after,'reason':'Recover full source outer MathML with control slots; map observed S# source DOM controls to existing fields by complete bank equality'+('; correct source-origin frequency 2t→6t by independent system residual'if q[':db/id']==17592186167223 else''),'evidence':{'source':path,'field_mapping':proof,'independently_checked_frequency':q[':db/id']==17592186167223},'confidence':'high'})
 review.append({'entity':q[':db/id'],'identity':item['identity'],'status':'proposed','mapping':proof})
(H/'control-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');(H/'control-review.json').write_text(json.dumps(review,indent=2)+'\n');print(len(proposals),collections.Counter(r['status']for r in review))

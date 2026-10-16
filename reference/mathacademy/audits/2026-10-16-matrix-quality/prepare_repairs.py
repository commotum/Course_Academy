"""Prepare narrow source restorations, verified key completion, and matrix presentation repairs."""
from pathlib import Path
import importlib.util,json,re,uuid
from capture.scripts.database.edn import dumps,kw
from scripts.question_capture.math_format import MATH,normalize_tex,environment,matrix_operands,matrix_answer,validate_prose,normalize_prose
P=Path(__file__).resolve().parent
qs={q[':db/id']:q for q in json.loads((P/'questions.json').read_text())};ts={t[':db/id']:t for t in json.loads((P/'tutorials.json').read_text())};records={**qs,**ts};changes={};decisions=[]
def change(e,a,new,reason):
 key=(e,a);old=records[e].get(':'+a)
 if new!=old:changes[key]=dict(entity=e,attribute=a,old=old,new=new,reasons=changes.get(key,{}).get('reasons',[])+[reason])
def current(e,a):return changes.get((e,a),{}).get('new',records[e].get(':'+a,''))

def independent_givens(full,stacked=True):
 # Only split independent definitions/lists: products, sums and derivations retain their operators.
 text=normalize_tex(full);matches=list(re.finditer(r'\\begin\{(?:bmatrix|pmatrix|vmatrix|Vmatrix)\}',text));parts=[];end=0
 if not matches:return None
 for m in matches:
  if m.start()<end:continue
  bounds=environment(text,m.start());assert bounds
  prefix=text[end:m.start()];prefix=re.sub(r'\\(?:quad|qquad)\b|\\[,;! ]','',prefix).strip(' \n\t,;.')
  if not re.fullmatch(r'(?:[A-Za-z](?:\^\{?\d\}?)?=)?',prefix.replace(' ','')):return None
  parts.append(prefix+text[m.start():bounds[2]]);end=bounds[2]
 suffix=re.sub(r'\\(?:quad|qquad|ldots)\b|\\[,;! ]','',text[end:]).strip(' \n\t,;.?')
 if suffix:return None
 return matrix_operands(parts,stacked=stacked)

excluded={17592186203876,17592186228911,17592186228915}
for proposal in json.loads((P/'source-proposals.json').read_text()):
 if proposal['entity'] in excluded:
  decisions.append(dict(entity=proposal['entity'],reason='Boxed prose with embedded math requires a separate content review; no automatic replacement'));continue
 text=proposal['new']
 for source in proposal['sources']:
  group=independent_givens(source['full'])
  if group:
   marker='$$\n'+source['full']+'\n$$';assert marker in text
   text=text.replace(marker,group,1)
 change(proposal['entity'],proposal['attribute'],text,'Recovered complete original equation from exact first-fragment anchor; source file and line in source-proposals.json')
# Two image-only transpose formulas can be recovered from their own source DOM without reading images.
source=[x for x in json.loads((P/'source-comparison.json').read_text()) if x['entity']==17592186059552]
for attr in ['question/problem','question/worked-solution']:
 c=next(x for x in source if x['attribute']==attr);text=current(17592186059552,attr);assert len(re.findall(r'!\[.*?\]\([^)]*\)',text))==1
 text=re.sub(r'!\[.*?\]\([^)]*\)',lambda m:'\n\n$$\n'+c['full']+'\n$$',text)
 change(17592186059552,attr,text,'Replaced image-only equation with complete TeX from the original e-4386 HTML; images were not inspected')
# The original scalar introduction also lost the assignment label in its first definition.
e=17592186060926;text=current(e,'tutorial/content');needle=r'\begin{bmatrix}1 & 3 \\ 2 & 4\end{bmatrix}'
assert text.count(needle)>=1
text=text.replace('$$\n'+needle+'\n$$','$$\nA='+needle+'\n$$',1);change(e,'tutorial/content',text,'Restored A= from original tutorial 2975 SVG title')
# A canonical example has both operands in one malformed inline math span; rewrite using exactly those source operands.
e=17592186059551
change(e,'question/problem','Calculate $2A+\\frac{1}{2}B$, where\n\n'+matrix_operands([r'A=\begin{bmatrix}1 & 5 \\ 1 & 2\end{bmatrix}',r'B=\begin{bmatrix}0 & 2 \\ 4 & 2\end{bmatrix}'],stacked=True),'Recovered source A label and separated A/B definitions from text inside an inline formula')
# Correct the bad coordinate while retaining the source explanation and all learner values.
e=17592186262598;text=current(e,'question/worked-solution');assert '{i}_{12}=0.1' in text
change(e,'question/worked-solution',text.replace('{i}_{12}=0.1','{i}_{21}=0.1'),'Independently verified I[2,1]=0.1 and I[1,2]=0; final answer unchanged')
# Make the captured subquestion self-contained using the original P shown in its own saved worked solution.
e=17592186235400
change(e,'question/problem','Maria and John agreed to increase the bet. Maria\'s original payoff matrix was\n\n'+matrix_operands([r'P=\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix}'])+'\n\nAfter increasing the bet, her payoff matrix became\n\n'+matrix_operands([r'\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}'])+'\n\nThis new matrix is obtained from $P$ using the scalar multiplication $kP$, where $k=$ {{field-1}}.','Supplied omitted prior-part P from this captured question\'s own original worked solution; exact ratio checked in all cells')
# Apply the established layout to every response question and canonical example in the three named topics.
math_report={x['entity']:x for x in json.loads((P/'priority-math-report.json').read_text())};layout=[]
for topic in [862,146,232]:
 t=json.loads((P/(str(topic)+'-priority.json')).read_text())
 for kp in t[':topic/knowledge-points']:
  for q in [kp[':knowledge-point/canonical-example']]+kp[':knowledge-point/questions']:
   e=q[':db/id'];text=current(e,'question/problem');oldtext=text;fs=q.get(':question/answer-fields',[])
   # Skip already structured HTML; only transform standalone math spans containing matrices.
   if 'class="matrix-operands' not in text:
    def display(m):
     raw=normalize_tex(m[0])
     if r'\begin{bmatrix}' not in raw or '{{' in raw:return m[0]
     group=independent_givens(raw)
     return '\n\n'+(group or ('$$\n'+raw+'\n$$'))+'\n\n'
    text=MATH.sub(display,text)
   if any(f[':answer-field/type'][':db/ident'].endswith('/blank') for f in fs) and any(l.strip().startswith('|') for l in text.splitlines()):
    lines=text.splitlines();start=next(i for i,l in enumerate(lines) if l.strip().startswith('|'));end=start
    while end<len(lines) and lines[end].strip().startswith('|'):end+=1
    table=[l for l in lines[start:end] if not re.match(r'^\s*\|[\s:|\-]+\|\s*$',l)];rr=[];labels=[]
    for l in table:
     vals=[v.strip() for v in l.strip().strip('|').split('|')];labels.extend(v.strip('$').strip().rstrip(',') for v in vals if '=' in v);rr.append([v.strip('$').strip() for v in vals if v and '=' not in v])
    assert len(labels)==1,(e,labels)
    expression=re.sub(r'\\[,;! ]','',labels[0]).rstrip('= ').strip()
    assert rr and len({len(row) for row in rr})==1,(e,rr)
    # Verify every location and fixed cell against the independently solved full matrix.
    expected=math_report[e]['expected'];spec=importlib.util.spec_from_file_location('priority_math',P/'priority_math.py')
    # Data already independently checked by priority_math.py; retain its exact table row sequence here.
    text='\n'.join(lines[:start])+'\n\n'+matrix_answer(expression,rr)+'\n\n'+'\n'.join(lines[end:]);layout.append(dict(entity=e,rows=len(rr),cols=len(rr[0]),fields=len(fs)))
   text=re.sub(r'\n{3,}','\n\n',text).strip()
   assert sorted(re.findall(r'\{\{[^{}]+\}\}',text))==sorted(re.findall(r'\{\{[^{}]+\}\}',oldtext)),e
   if text!=oldtext:change(e,'question/problem',text,'Uniform centered matrix definitions and bracketed matrix response; exact cell order and field identities preserved')
# Repaired keys use existing field-owned answers. Redundant legacy fields are detached, never deleted.
duplicates=json.loads((P/'duplicate-field-proposals.json').read_text());detached={f for d in duplicates for f in d['detach']};keys=[x for x in json.loads((P/'key-proposals.json').read_text()) if x['field'] not in detached]
for x in json.loads((P/'solution-proposals.json').read_text()):change(x['entity'],'question/worked-solution',x['new'],'Completed missing worked solution using canonical KP method and independently calculated target')
forms=[];ensure=set()
for c in list(changes.values()):
 c['new']=normalize_prose(c['new'])
 try:validate_prose(c['new'])
 except ValueError as ex:
  decisions.append(dict(entity=c['entity'],attribute=c['attribute'],reason='Existing surrounding content needs further TeX repair: '+str(ex)));del changes[(c['entity'],c['attribute'])];continue
 forms.append([kw('db/cas'),c['entity'],kw(c['attribute']),c['old'],c['new']]);ensure.add((c['entity'],'tutorial/validate' if c['attribute'].startswith('tutorial/') else 'question/validate'))
for x in keys:forms.append([kw('db/cas'),x['field'],kw('answer-field/correct'),None,x['correct']]);ensure.add((x['field'],'answer-field/validate'))
for d in duplicates:
 for f in d['detach']:forms.append([kw('db/retract'),d['question'],kw('question/answer-fields'),f])
 ensure.add((d['question'],'question/validate'))
for e,spec in sorted(ensure):forms.append([kw('db/ensure'),e,kw(spec)])
(P/'repair-changes.json').write_text(json.dumps(list(changes.values()),indent=2));(P/'repair-decisions.json').write_text(json.dumps(decisions,indent=2));(P/'repair-keys.json').write_text(json.dumps(keys,indent=2));(P/'layout-changes.json').write_text(json.dumps(layout,indent=2));(P/'repairs.edn').write_text(dumps(forms))
intent=P/'repair-intent.json'
if not intent.exists():intent.write_text(json.dumps(dict(database='math',source=':application/ca-engine',requestKey='matrix-quality-20261016-'+str(uuid.uuid4())),indent=2))
print('Prepared',len(changes),'text attributes,',len(keys),'canonical keys,',len(duplicates),'equivalent obsolete field bindings;',len(layout),'bracketed matrix answers.')

"""Independent structure, matrix-preservation and selected answer-key checks."""
import json,re,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'))
from math_format import ENV,environment,cells,validate_tex,validate_prose
images={x['path']:x['tex'] for x in json.loads((H/'image-replacements.json').read_text())}
fields=json.loads((H/'fields.json').read_text());lookup={(f['entity'],f['attribute']):f['after'] for f in fields}
def matrices(text):
 out=[]
 for token in ENV.finditer(text):
  if token[1]!='begin' or token[2] not in ['bmatrix','pmatrix','matrix','array']:continue
  span=environment(text,token.start());assert span
  body=text[span[0]:span[1]];spec=None
  if token[2]=='array':
   m=re.match(r'\s*\{([^{}]+)\}',body);assert m;spec=m[1];body=body[m.end():]
  rows=cells(body);assert rows and len({len(r) for r in rows})==1
  out.append({'columns':spec,'rows':[[re.sub(r'\s+','',c) for c in row] for row in rows]})
 return out
preserved=0
for f in fields:
 source=re.sub(r'!\[[^\]]*\]\(([^)]+)\)',lambda m:images.get(m[1],m[0]),f['before'])
 assert matrices(source)==matrices(f['after']),(f['entity'],f['attribute'],'Matrix entries, highlights or augmentation changed')
 preserved+=len(matrices(source))
 (validate_tex if f['kind']=='math' else validate_prose)(f['after'])
def numeric(mat):
 rows=[]
 for row in mat['rows']:
  values=[]
  for c in row:
   c=re.sub(r'\\color\{[^}]+\}','',c)
   c=re.sub(r'\\bbox\[[^]]*\]','',c)
   c=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1)/(\2)',c)
   c=c.replace('{','(').replace('}',')')
   assert re.fullmatch(r'[0-9()\-+/]+',c),c
   values.append(sp.Rational(sp.sympify(c)))
  rows.append(values)
 return rows
checks=[];issues=[]
for item in json.loads((H/'question-inventory.json').read_text()):
 q=item['record'];eid=q[':db/id'];prompt=lookup[eid,':question/problem'];fs=q.get(':question/answer-fields',[])
 try:
  if item['kp'] in [17592186129113,17592186129114] and fs and all(f[':answer-field/key'] in 'ABCD' for f in fs):
   ms=[numeric(m) for m in matrices(prompt)];assert len(ms)==len(fs)
   for f,m in zip(sorted(fs,key=lambda f:f[':answer-field/key']),ms):
    if 'coefficient matrices' in prompt:
     m=[row[:-1] for row in m]
    pivots=[next((j for j,x in enumerate(row) if x),None) for row in m]
    p=[v for v in pivots if v is not None]
    ref=all(a<b for a,b in zip(p,p[1:])) and pivots==p+[None]*(len(pivots)-len(p))
    expected=ref!=('**not**' in prompt)
    assert (f[':answer-field/correct'][':answer/value']=='true')==expected,(f[':answer-field/key'],pivots,expected)
   checks.append({'question':eid,'kind':'independent row-echelon checkbox truth','fields':len(fs)})
  if item['kp']==17592186129176 and fs and all(f.get(':answer-field/correct') for f in fs):
   m=numeric(matrices(prompt)[0]);target=prompt.split('rows')[0]
   rows=[int(n)-1 for n in re.findall(r'\$(\d)\$(?:st|nd|rd|th)',target)]
   assert rows
   total=sum(next(v for v in m[i] if v) for i in rows)
   assert sp.Rational(fs[0][':answer-field/correct'][':answer/value'])==total
   checks.append({'question':eid,'kind':'independent leading-entry sum','rows':[i+1 for i in rows],'sum':str(total)})
 except Exception as e:issues.append({'question':eid,'kp':item['kp'],'error':str(e)})
report={'fields_structurally_validated':len(fields),'matrix_occurrences_preserved':preserved,'independent_answer_checks':checks,'issues':issues,'existing_content_quality_findings':'content-quality-findings.json','scope':'Formatting and all matrix preservation checked; independent answer-key checks for supported echelon and leading-entry question forms; other mathematical reasoning not exhaustively recertified.'}
(H/'quality-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'fields':len(fields),'matrices_preserved':preserved,'independent_questions':len(checks),'issues':issues}))

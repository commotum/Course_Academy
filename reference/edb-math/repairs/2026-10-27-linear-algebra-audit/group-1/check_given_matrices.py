import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import ENV,environment,cells
p=H/'propose_formulas.py';ns={'__file__':str(p)};exec(compile(p.read_text().split('props=[]')[0],str(p),'exec'),ns);canon=ns['canonical']
D=json.loads((H/'proposed.json').read_text());S=json.loads((H/'sources.json').read_text());idx=collections.defaultdict(list)
for s in S:
 if s['attribute']=='question/problem':idx[s['identity']].append(s)
def matrices(text):
 out=[]
 for m in ENV.finditer(text):
  if m[1]!='begin'or m[2]not in ['bmatrix','pmatrix','vmatrix','matrix','array']:continue
  span=environment(text,m.start())
  if not span:continue
  body=text[span[0]:span[1]]
  if m[2]=='array':
   spec=re.match(r'\{[clr|]+\}',body)
   if not spec:continue
   body=body[spec.end():]
  grid=cells(body)
  if not grid:continue
  out.append(tuple(tuple(canon(c).rstrip('.,')for c in row)for row in grid))
 return sorted(out)
report=[]
for q in D['questions']:
 ident=q.get(':question/math-academy-id')
 if not ident:continue
 text=q[':question/problem']+'\n'+'\n'.join(f[':answer-field/key']for f in q.get(':question/answer-fields',[])if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox');given=matrices(text);attempts=[]
 for s in idx[ident]:
  source=matrices('\n'.join(s['formulas']));attempts.append({'path':s['path'],'match':source==given,'source_matrices':len(source),'source_values':source})
 match=next((a for a in attempts if a['match']),None);report.append({'question':q[':db/id'],'identity':ident,'given_matrices':len(given),'available_source_versions':len(attempts),'matched_source':match['path']if match else None,'attempts':attempts if attempts and not match else [],'current_values':given if attempts and not match else None})
(H/'given-matrix-source-validation.json').write_text(json.dumps(report,indent=2));print('source prompts',sum(bool(r['available_source_versions'])for r in report),'matrix matches',sum(bool(r['matched_source'])for r in report),'unmatched',[(r['identity'],r['given_matrices'],r['attempts'])for r in report if r['available_source_versions']and not r['matched_source']])

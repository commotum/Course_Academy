"""Verify rendered mathematical content independently of generation metadata."""
import json,re,pathlib
root=pathlib.Path(__file__).resolve().parent
files=['samples.json','batch-records.json','source-replay-records.json','counterfactual-records.json','minimal-shortcut.json','render-remaining-records.json']
def matrix(text):
 m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',text,re.S)
 return [[v.strip() for v in row.split('&')] for row in m[1].split('\\\\')] if m else None
out=[]
for file in files:
 for r in json.load(open(root/file)):
  q=r['question'];s=q[':question/problem'];sol=q[':question/worked-solution'];a=matrix(s);i,j=map(int,re.search(r'_\{(\d)(\d)\}',s).groups());name=re.search(r'matrix \$([A-Z])\$',s)[1];n=len(a)
  expected=a[i-1][j-1] if i<=n and j<=n else 'No such entry'
  f=q[':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1];actual=next(v[':answer/value'] for v in f[':answer-field/choices'] if v[':answer/id']==cid)
  checks={'square':all(len(row)==n for row in a),'key':actual==expected,'unique_options':len(set(v[':answer/value'] for v in f[':answer-field/choices']))==len(f[':answer-field/choices']),'solution_row_column':re.search(rf'\${i}\$(?:st|nd|rd|th) row and \${j}\$(?:st|nd|rd|th) column',sol) is not None,'solution_target':all(t==f'{i}{j}' for t in re.findall(r'_\{(\d\d)\}',sol))}
  if expected!='No such entry':
   checks['solution_value']=re.search(rf'_\{{{i}{j}\}}='+re.escape(expected)+r'\.\$',sol) is not None
   checks['solution_matrix']=matrix(sol)==a
   checks['solution_matrix_name']=re.search(rf'{name}\s*=',sol) is not None
  else:
   axis='row' if i>n else 'column';index=i if i>n else j
   checks['solution_absence']=f'${n}\\times {n}$' in sol and re.search(rf'does not have the \${index}\$(?:st|nd|rd|th) {axis}',sol) is not None
  out.append({'file':file,'question_id':q[':question/id'],'expected':expected,'actual':actual,'checks':checks,'passed':all(checks.values())})
(root/'math-verification.json').write_text(json.dumps(out,indent=2)+'\n')
failed=[x for x in out if not x['passed']];print(json.dumps({'checks':len(out),'failed':failed},indent=2));raise SystemExit(bool(failed))

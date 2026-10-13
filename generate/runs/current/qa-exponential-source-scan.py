"""Pre-review source mathematics; underdefined originals remain explicit evidence."""
import json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent
z=importlib.util.spec_from_file_location('expscanparser',R/'ode-scalar-parser.py');p=importlib.util.module_from_spec(z);z.loader.exec_module(p);x=p.x;y=p.y
def scalar(t):return p.scalar(t.replace(r'\dfrac',r'\frac'))
def same(a,b):return s.simplify(s.expand(a-b))==0
def check(k):
 source=R/f'sources/{k}.json';qs=json.loads(source.read_text())['record'][':knowledge-point/questions'];results=[]
 for q in qs:
  text=q[':question/problem'];row={'source_id':q[':question/math-academy-id'],'raw_prompt_self_contained':True}
  if 'y=f(h(x))' in text:
   row.update(raw_prompt_self_contained=False,note='Function definitions absent from captured prompt; solution/widget context required for completion.');results.append(row);continue
  match=re.search(r'(?:f\(x\)|y)\s*=\s*([^$]*)\$',text);assert match,text;F=scalar(match[1]);D=s.diff(F,x);criterion='derivative'
  if 'slope' in text or 'equation of the tangent' in text:
   at=re.search(r'where \$x\s*=\s*(.*?)\$',text);assert at,text;X=scalar(at[1]);D=s.simplify(D.subs(x,X));criterion='slope'
   if 'equation of the tangent' in text:D=y-F.subs(x,X)-D*(x-X);criterion='tangent_line'
  if '{{field-1}}$' in text and r'\cdot' in text.split('{{field-1}}',1)[1]:
   factor=scalar(text.split('{{field-1}}',1)[1].replace('$','').strip().removeprefix(r'\cdot').strip());D=s.simplify(D/factor);criterion='supplied_exponential_fragment'
  row['criterion']=criterion;row['fields']=[]
  for field in q.get(':question/answer-fields',[]):
   values=[];eligible=[]
   for a in field.get(':answer-field/choices',[]):
    raw=a[':answer/value'];v=scalar(raw.split('=',1)[0])-scalar(raw.split('=',1)[1]) if criterion=='tangent_line' else scalar(raw);values.append(v)
    if criterion=='tangent_line':ratio=s.simplify(v/D);valid=not ratio.free_symbols and ratio!=0
    else:valid=same(v,D)
    if valid:eligible.append(a[':answer/value'])
   assert len(eligible)==1,(k,row['source_id'],eligible,D)
   selected=field.get(':answer-field/correct',{}).get(':answer/value');assert selected is None or selected in eligible,(row,selected,eligible)
   assert all(not same(v,w) for i,v in enumerate(values) for w in values[:i]),row
   row['fields'].append({'type':field[':answer-field/type'][':db/ident'],'bank_values':len(values),'independently_valid':eligible,'existing_key_valid':selected is not None})
  results.append(row)
 out={'kp_id':k,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'status':'passed_with_explicit_underdefined_sources' if any(not r['raw_prompt_self_contained'] for r in results) else 'passed','questions':results};(R/f'qa/{k}-source-math-scan.json').write_text(json.dumps(out,indent=2)+'\n');print(k,out['status'],len(results),'questions',sum(len(r.get('fields',[])) for r in results),'fields')
if __name__=='__main__':
 for k in (17592186092260,17592186092261,17592186092263):check(k)

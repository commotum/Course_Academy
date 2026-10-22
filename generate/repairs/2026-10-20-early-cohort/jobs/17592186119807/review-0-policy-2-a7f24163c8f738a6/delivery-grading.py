import json,pathlib,re,sys
sys.dont_write_bytecode=True
import sympy as s
E=pathlib.Path(__file__).resolve().parent; rs=json.loads((E/'delivery-batch/accepted.json').read_text());cases=[]
for i,r in enumerate(rs):
 vs=[s.Matrix([s.Rational(v.strip()) for v in x.split(r'\\')]) for x in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',r['question'][':question/problem'],re.S)];a,c,b=vs;sol=s.linsolve((a.row_join(c),b));truth='No solution' if sol==s.EmptySet else str(sum(next(iter(sol))))
 cases.append({'label':'delivered-batch-'+str(i),'record':r,'checks':[{'submitted_answer_id':o[':answer/id'],'expected':'accepted' if o[':answer/value']==truth else 'rejected','purpose':'independent truth after actual publisher normalization and ID replacement'} for o in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
(E/'delivery-grader-input.json').write_text(json.dumps(cases,indent=2))

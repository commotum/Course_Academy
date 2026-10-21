import sys,json,pathlib,copy
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E.parent/'workspace'))
import generator as g
p={'matrix':[[6,-6,0],[6,0,6],[-6,6,6]],'target':0,'factor':[1,3],'candidate_factors':[[1,3],[1,2],[2,1],[-1,2],[-1,3]]}
records=[g.generate('easy',834,'scale-arithmetic',{**p,'target':t}) for t in [0,1]]
(E/'target-records.json').write_text(json.dumps(records,indent=2)+'\n')
# Independent expected matrices using explicit known division; do not call bank().
expected=[[[2,-2,0],[6,0,6],[-6,6,6]],[[6,-6,0],[2,0,2],[-6,6,6]]]
cases=json.load(open(E/'grader-input.json'))
for n,(r,good) in enumerate(zip(records,expected)):
 f=r['question'][':question/answer-fields'][0]
 def tex(m):return '\\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in m)+'\\end{bmatrix}'
 value=tex(good);assert sum(a[':answer/value']==value for a in f[':answer-field/choices'])==1
 cases.append({'label':'controlled-scale-target-'+str(n),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==value else 'rejected','purpose':'target row changed with same matrix, factor, candidate factors, and seed'} for a in f[':answer-field/choices']]})
(E/'grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
(E/'target-results.json').write_text(json.dumps({'parameters':p,'changed':'target 0 to 1 only','expected_matrices':expected,'prompt_operations':[r['question'][':question/problem'].split('row operation')[1] for r in records],'solutions':[r['question'][':question/worked-solution'] for r in records],'key_values':[next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in records]},indent=2)+'\n')

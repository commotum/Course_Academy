import sys,json
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'workspace'))
import generator
from review_math import check,correct_index
records=[generator.generate(template='q-74628',seed=12980722+j*65537) for j in range(10)]
Path('shortcut-controls.json').write_text(json.dumps(records,indent=2))
res=[check(r) for r in records];Path('shortcut-controls-math.json').write_text(json.dumps(res,indent=2,default=str))
cases=json.load(open('grader-input.json'))
for r in records:
 q=r['question'];f=q[':question/answer-fields'][0];idx=correct_index(q)
 cases.append({'label':'shortest-option-control:'+q[':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==idx else 'rejected','purpose':'Independent control for apparent shortest-option cue'} for j,a in enumerate(f[':answer-field/choices'])]})
Path('grader-all-input.json').write_text(json.dumps(cases,indent=2))
hits=sum(min(range(5),key=lambda j:len(r['question'][':question/answer-fields'][0][':answer-field/choices'][j][':answer/value']))==correct_index(r['question']) for r in records)
Path('shortcut-control-results.json').write_text(json.dumps({'command':'shortcut_control.py','template':'q-74628','seeds':[12980722+j*65537 for j in range(10)],'cue':'shortest option TeX','correct':hits,'total':10,'baseline':0.2,'math_errors':[a for a in res if a['errors']],'conclusion':'Initial 3/3 success does not persist on independent seeds; code samples correct slot before exchangeable candidate values.'},indent=2))
print('shortest-option control:',hits,'/10; math failures',sum(bool(a['errors']) for a in res))

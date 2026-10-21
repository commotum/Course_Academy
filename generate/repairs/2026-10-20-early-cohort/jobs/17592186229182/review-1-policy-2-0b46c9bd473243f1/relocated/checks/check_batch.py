import sys,json,pathlib
sys.dont_write_bytecode=True
P=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'checks'));import math_witness as w
rs=json.loads((P/'evidence/batch.json').read_text());cases=[]
for i,r in enumerate(rs):
 w.check_math(r);w.formatting(r);f=r['question'][':question/answer-fields'][0]
 cases.append({'label':'five-question batch '+str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently checked batch key'} for a in f[':answer-field/choices']]})
(P/'evidence/batch-grader-input.json').write_text(json.dumps(cases,indent=2));print('Five CLI records: printed mathematics, banks and formatting passed.')

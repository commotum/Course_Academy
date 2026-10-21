from review import *
import importlib.util
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(E/'assets')
s=importlib.util.spec_from_file_location('gen',PK/(KP+'.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
base=json.loads((E/'counterfactual-records.json').read_text())[0];p=base['generation']['parameters'];r=g.generate('moderate',seed=base['generation']['seed'],template='possible_product',parameters={**p,'b':-1})
def key(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
q=base['question'];z=r['question']
result={'change':'b=1 to b=-1 in two one-variable distractors, same target a*x*y, seed and other parameters','prompt_preserved':q[':question/problem']==z[':question/problem'],'solution_preserved':q[':question/worked-solution']==z[':question/worked-solution'],'key_image_preserved':key(base)==key(r),'displayed_bank_changed':q[':question/answer-fields'][0][':answer-field/choices']!=z[':question/answer-fields'][0][':answer-field/choices']}
assert all(v for k,v in result.items() if k!='change')
dump('irrelevant-display-records.json',[base,r]);dump('irrelevant-display-result.json',result)
f=z[':question/answer-fields'][0]
dump('extra-grader-input.json',[{'label':'irrelevant displayed distractor pair after','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'target plot preserved despite irrelevant distractor sign change'} for a in f[':answer-field/choices']]}])
print(result)

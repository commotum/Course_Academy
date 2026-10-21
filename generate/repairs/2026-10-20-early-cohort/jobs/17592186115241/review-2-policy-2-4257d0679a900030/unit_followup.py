import sys,json,pathlib,collections,subprocess
sys.dont_write_bytecode=True
from independent_math import *
from reproduce_unit_shortcut import probe
E=pathlib.Path(__file__).resolve().parent
def read(p):return json.load(open(E/p))
def dump(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
paths=['batch.json','delivery-batch/accepted.json','fresh.json','delivery-fresh/accepted.json','source-shortcut-records.json','delivery-source-shortcut/accepted.json','cue-control-records.json','delivery-controls/accepted.json']
measurements={}
for path in paths:
 rows=[]
 for r in read(path):
  M=system(r['question'][':question/problem']);equal=M.cols==3 and all(M[i,0]==M[i,1] for i in range(M.rows))
  rows.append({'question_id':r['question'][':question/id'],'seed':r['generation']['seed'],'profile':r['generation']['bank_profile'],'recognizable_equal_coefficients':equal,'probe':probe(r)})
 groups={}
 for name,rr in [('overall',rows),('equal-coefficient rank-one systems',[r for r in rows if r['recognizable_equal_coefficients']]),('q-32244 ordinary source-profile',[r for r in rows if r['profile']=='q-32244'])]:
  a=[r for r in rr if r['probe']['applicable']]
  groups[name]={'records':len(rr),'correct':sum(r['probe']['shortcut_correct'] for r in a),'total':len(a),'baseline':0.2}
 measurements[path]={'rows':rows,'groups':groups}
minimal=read('minimal-unit-shortcut.json')['record'];dump('render-unit-records.json',[minimal])
# Reuse completed native all-choice invocation: verify exact current record and UUID are present.
inputs=read('grader-input.json');outputs=read('grader-results.json');idx=next(i for i,c in enumerate(inputs) if c['record']==minimal);lab=inputs[idx]['label'];result=next(r for r in outputs['records'] if r['label']==lab)
assert len([c for c in result['checks'] if c['outcome']=='accepted'])==1
assert next(c for c in inputs[idx]['checks'] if c['submitted_answer_id']==probe(minimal)['selected_answer_id'])['expected']=='accepted'
assert measurements['source-shortcut-records.json']['groups']['q-32244 ordinary source-profile']==measurements['delivery-source-shortcut/accepted.json']['groups']['q-32244 ordinary source-profile']
dump('unit-shortcut-results.json',{'command':str(sys.executable)+' -B unit_followup.py','strategy':'Use only the typography of the answer bank: select its sole unmultiplied y in the first coordinate. No equation, sign, constant or arithmetic used to choose.','measurements':measurements,'minimal_native_grading':{'input_case_index':idx,'input_case':inputs[idx],'result_case':result},'mechanism':'q-32244 affine transport fixes correct slope=-1. candidate_bank excludes zero slopes and samples other nonzero integer slopes; whenever no distractor has slope +1 or -1, the correct unmultiplied-y expression is unique. Matching denominators did not equalize this typographic signature. This is an answer-producing action cue, not elimination or verification of a candidate against equations.','batch_conclusion':'The exact five-record runner batch has no successful instance of this conditional cue. This is a generator/source-profile defect, not a demonstrated batch-selection failure.'})
I=json.load(open(E.parent/'source/inventory.json'));hist=read('generated-records.json');checks=[{'question_id':r['question'][':question/id'],'entity_id':r['review_evidence']['stored_entity_id'],'generator_version':r['generation']['generator_version'],'probe':probe(r),'two_coordinate_rank_one':len(vec(field(r)[':answer-field/choices'][0][':answer/value']))==2} for r in hist]
assert not any(x['two_coordinate_rank_one'] for x in checks)
dump('inventory-unit-cue.json',{'captured_basis':I['basis'],'captured_count':len(I['questions']),'historical_generated_count':len(hist),'tested':checks,'demonstrated_new_unit_cue_affected_generated_records':0,'result':'All ten reproduced generated inventory records are moderate/hard with three/four coordinates; none belongs to this two-coordinate cue family. Fourteen other inventory questions are original instructional sources and are not labelled generated. Existing historical component-frequency defects remain in affected-inventory.json.','limits':'This is a verified absence of this particular two-coordinate cue among the ten reproduced generated inventory records, not a general absence of other inventory defects.'})
cp=subprocess.run([sys.executable,'-B',str(E/'reproduce_unit_shortcut.py')],capture_output=True,text=True);assert cp.returncode==1
dump('unit-strict-regression.json',{'command':cp.args,'exit':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
print(json.dumps({p:x['groups'] for p,x in measurements.items()},indent=2))

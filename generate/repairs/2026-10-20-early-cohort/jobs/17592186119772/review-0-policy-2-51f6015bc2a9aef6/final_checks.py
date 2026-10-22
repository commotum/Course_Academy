#!/usr/bin/env python3
import json,sys,pathlib,hashlib
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
load=lambda n:json.load(open(E/n))
# Extend the batched native grader run to post-delivery and historical records.
cases=load('grader-input.json')
for stage,filename in [('delivered','delivery-batch/accepted.json'),('inventory','generated-records.json')]:
 for i,r in enumerate(load(filename)):
  checks=[]
  for fi,f in enumerate(r['question'][':question/answer-fields']):
   aid=f[':answer-field/correct'][1]
   for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==aid else 'rejected','purpose':'Post-delivery or content-verified historical response; all bank choices'})
  cases.append({'label':stage+'-'+str(i),'record':r,'checks':checks})
(E/'grader-input-final.json').write_text(json.dumps(cases,indent=2)+'\n')
v=load('pedagogical-variation.json')
v['shortcut_probes'].append({'cue':'Label D alone','subgroup':'Exact runner batch, post-delivery','scope':'within_template','strategy':'Always select the matrix labeled D; ignore every entry and its size.','correct':5,'total':5,'baseline':0.2,'disposition':'defect','conclusion':'All five records use q-126352 and have correct label D. Uniform random choice among five is 0.2. This perfect fixed-label shortcut affects the actual batch even though larger control sets contain other correct labels.','sample_refs':['delivery-batch/accepted.json','shortcut-delivered-batch.json','strict-regression-report.json']})
(E/'pedagogical-variation.json').write_text(json.dumps(v,indent=2)+'\n')
# Source profile rules remain distinct from the definition; retain exact minimal input.
r=load('strict-regression-report.json')
minimal={'source_profile':'q-126354','source_question_id':'8edd360b-8c0f-5c8f-b5f1-4655b27f3fa4','seed':20261022,'parameters':r['tests'][0]['parameters'],'expected_correct':'A','actual_error':r['tests'][0]['error'],'command':'/home/jake/Developer/Course_Academy/.venv/bin/python strict_regressions.py'}
(E/'minimal-failing-case.json').write_text(json.dumps(minimal,indent=2)+'\n')
# Representative screenshots were visually inspected, beyond renderer success.
(E/'visual-inspection.json').write_text(json.dumps({'renderer':'Unmodified UI through render_preview.py','screenshots_inspected':['render/question-001.png','render/question-003.png','render-counterfactual/question-002.png','render-counterfactual/question-003.png'],'result':'Matrices have distinct rows/columns and readable brackets; full radio controls, target wording, worked-solution matrices and prose display correctly. Upper/lower transpose and irrelevant diagonal change are visible. No clipping or mathematical rendering artifacts observed.','automatic_reports':['render/rendering.json','render-counterfactual/rendering.json'],'limits':'Representative desktop screenshots, not an audit of every viewport.'},indent=2)+'\n')
# Validate required pedagogical-variation fields against the supplied schema.
try:
 import jsonschema
 schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'))
 jsonschema.validate(v,schema);schema_status='passed with jsonschema'
except ImportError:
 schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'))
 assert set(v)==set(schema['required'])
 for key in ['fixed_features','answer_roles','coverage','counterfactuals','shortcut_probes']:
  assert v[key]
  required=schema['properties'][key]['items']['required']
  assert all(set(x)==set(required) for x in v[key])
 schema_status='required fields and nested field sets checked; jsonschema not installed'
def paths(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='sample_refs':yield from v
   else:yield from paths(v)
 elif isinstance(x,list):
  for v in x:yield from paths(v)
for p in paths(v):assert not pathlib.Path(p).is_absolute() and (E/p).is_file() and (E/p).stat().st_size>0,p
(E/'evidence-validation.json').write_text(json.dumps({'pedagogical_schema':schema_status,'all_sample_refs_exist_nonempty':True},indent=2)+'\n')
print(json.dumps({'grader_cases':len(cases),'pedagogical_schema':schema_status,'strict_regressions_failed':sum(not x['passed'] for x in r['tests'])}))

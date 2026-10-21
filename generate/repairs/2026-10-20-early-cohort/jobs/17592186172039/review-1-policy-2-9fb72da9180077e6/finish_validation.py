import json,pathlib,hashlib
E=pathlib.Path(__file__).resolve().parent
# Reuse only our independent visible-equation checker definitions, not its test runs.
ns={'__file__':str(E/'audit.py')};exec(compile((E/'audit.py').read_text().split("source=json.loads")[0],str(E/'audit.py'),'exec'),ns)
load=lambda n:json.loads((E/n).read_text());cases=load('native-input.json');results=[]
for name in ['delivery-batch/accepted.json','delivery-samples/accepted.json']:
 rs=load(name)
 for i,r in enumerate(rs):
  d=ns['inspect'](r);cases.append(ns['native'](r,'delivered '+name+' '+str(i)));results.append({'file':name,'index':i,'question_id':r['question'][':question/id'],'visible_math_correct':True,'truth_mask':d['mask']})
b=load('boundary-results.json')
for name,r in [('resampled',b['seeded_retry']['record']),('default_none',b['same_initial_seed_with_default_none']),('canonical',b['canonical_source']['record'])]:ns['inspect'](r);cases.append(ns['native'](r,name))
(E/'native-input.json').write_text(json.dumps(cases,indent=2)+'\n');(E/'delivered-validation.json').write_text(json.dumps(results,indent=2)+'\n')
# Supplementary conditional probe: useful algebraic simplification is the intended skill.
ped=load('pedagogical-variation.json');rs=[r for r in load('samples-all.json') if r['generation']['parameters']['a']==r['generation']['parameters']['b']==2 and r['generation']['parameters']['c']>0]
hits=sum(all((('positive' in f[':answer-field/key'])==(ns['correct'](f)=='true')) for f in r['question'][':question/answer-fields'] if f[':answer-field/key']!='None of the above') for r in rs)
ped['shortcut_probes'].append({'cue':'Both powers squared, coefficient positive','subgroup':'hard x^2 y^2 with positive coefficient','scope':'other_recognizable_subgroup','strategy':'Select positive claims in every queried quadrant','correct':hits,'total':len(rs),'baseline':0.125,'disposition':'intended_skill','conclusion':'Guessing a complete subset has 1/8 baseline. Perfect prediction here is mathematical: both squared coordinates and positive coefficient are positive in every open quadrant. It uses the target sign/parity skill.','sample_refs':['samples-all.json']})
ped['delivery']['sample_refs'].extend(['boundary-results.json','delivered-validation.json']);ped['limitations'].append('Live policy weights and learner history are not captured; selection.json makes its positive-moderate-band condition explicit and tests fresh and history-exclusion scenarios. This is a read-only rule reproduction, not a live selection run.')
(E/'pedagogical-variation.json').write_text(json.dumps(ped,indent=2)+'\n')
(E/'render-inspection.json').write_text(json.dumps({'passed':True,'inspected':['render/contact-sheet.png','render/question-006.png','render/question-007.png','render/question-009.png','render/question-011.png','render/question-012.png','render-extra/question-001.png','render-extra/question-002.png','render-extra/question-003.png'],'observations':['Exact runner batch viewed in contact sheet: checkbox claim labels and correct subsets present.','Relevant coefficient change switches all ordinary truths and sign diagram; target change updates visible statement and explanation.','Magnitude rescaling preserves decisions and sign diagram.','Easy cx diagram has constant signs within each half-plane. Hard parity diagram matches squared-factor signs.','Compact numbered solution typesets its monomial, y^2 and x.','Empty substantive subset has a visible correctly selected None.','No clipping, missing diagram, invalid MathJax or broken controls observed.']},indent=2)+'\n')
print('Delivered math checked; appended delivered and boundary native cases; saved visual inspection.')

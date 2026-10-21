import sys;sys.dont_write_bytecode=True
import json,pathlib,importlib.util
R=pathlib.Path(__file__).resolve().parent
# Reuse the independently authored cue evaluator without re-running its sample generation.
s=(R/'shortcut_confirmation.py').read_text();prefix=s[:s.index("raw=json.loads")];ns={'__file__':str(R/'shortcut_confirmation.py')};exec(compile(prefix,'shortcut_confirmation.py','exec'),ns)
load=lambda p:json.loads((R/p).read_text())
delivered=load('holdout-delivery/accepted.json');result=ns['evaluate'](delivered,'fresh holdout delivered')
assert result['correct']==result['total']>0
report=load('shortcut-confirmation.json');report['results'].append(result);ns['save']('shortcut-confirmation.json',report)
cases=load('grader-input-complete.json')
for inputname,stage in [('delivery/accepted.json','discovery delivered'),('holdout-delivery/accepted.json','fresh holdout delivered')]:
 records=load(inputname);rs=next(a for a in report['results'] if a['stage']==stage)
 for trial in rs['trials']:
  r=records[trial['sample_index']];idx=trial['selected_indices'][0]
  cases.append({'label':'shortcut '+stage+' '+str(trial['sample_index']),'record':r,'checks':[{'submitted_answer_id':r['question'][':question/answer-fields'][0][':answer-field/choices'][idx][':answer/id'],'expected':'accepted','purpose':'Answer selected by constant matching plus unit-numerator/single-digit-denominator cue, without integration of power'}]})
ns['save']('grader-input-final.json',cases)
print({'fresh_holdout_delivered_shortcut':(result['correct'],result['total']),'total_grader_records':len(cases)})

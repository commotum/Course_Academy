"""Refresh extraction evidence from the frozen cohort and normal generator masks."""
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
RECIPES={
 'linear-log-radio':['-a/(x lnB): omit derivative of x','a/(x lnB): reverse sign and omit derivative of x','x-a/(x lnB): leave x undifferentiated','1-1/(x lnB): omit log coefficient','1-a/(x lnB): correct'],
 'quadratic-log-radio':['2x-a/(x lnB): correct','legacy_a/(x lnlegacy_base): unrelated historical expression; interpretation unresolved','2x-1/(x lnB): omit log coefficient','x-1/(x lnB): omit power multiplier and log coefficient','x-a/(x lnB): omit power multiplier'],
 'scaled-log':['1/(x lnB): omit coefficient','a/(Bx): replace lnB with B','a/(x lna): use coefficient as base','a/(x lnB): correct','a/x: omit lnB'],
 'exp-explicit-radio':['E^x lnE+1/(x lnB): correct','E^x lnE+1/lnB: omit x','E^x+1/(x lnB): omit lnE','E^x lnE+1/x: omit lnB','wrong_expbase^x lnE+1/(x lnB): altered base; interpretation unresolved'],
 'exp-common-radio':['E^x lnE+1/(x ln10): correct','E^x lnE+1/ln10: omit x','E^x+1/(x ln10): omit lnE','E^x lnE+1/x: omit ln10','wrong_expbase^x lnE+1/(x ln10): altered base; interpretation unresolved'],
 'quadratic-slope':['2a-b/lnB: derivative evaluated at1'],
 'log-minus-ln':['1/(x lnB)-b/x: correct derivative fragment'],
 'cubic-slope':['27a+1-b/(3 lnB): derivative evaluated at3'],
 'exp-common-blank':['E^x lnE+1/(x ln10): correct derivative fragment'],
 'negative-exp-log':['-e^x+a/(x lnB): correct derivative fragment'],
 'log-ln-exp-slope':['a/lnB-b+c e: derivative evaluated at1'],
}
rows=[]
for t,(level,mid) in g.TEMPLATES.items():
 if mid is None:continue
 source=g.SOURCES[mid];_,_,answer,_=g.expressions(t,g.PARAMETERS[t])
 for f in source.get(':question/answer-fields',[]):
  for index,a in enumerate(f[':answer-field/choices']):
   correct=f.get(':answer-field/correct',{}).get(':answer/id')==a[':answer/id'] if ':answer-field/correct' in f else None
   rows.append({'source_id':mid,'template':t,'field_key':f[':answer-field/key'],'profile':'raw-source','original_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'exact_symbolic_value':str(v.math(a[':answer/value'])),'recipe':RECIPES[t][index],'observed_correct_designation':correct,'independently_correct':v.equal(v.math(a[':answer/value']),answer),'interpretation_unresolved':'unresolved' in RECIPES[t][index],'opaque_bank':t in g.OPAQUE})
(HERE/'choice-mapping.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
(HERE/'variable-masks.json').write_text(json.dumps(g.MASKS,indent=2,ensure_ascii=False)+'\n')
print('Frozen choice mapping:',len(rows),'values; masks:',len(g.MASKS))

"""Separate native transport diagnostics from mathematical equivalence checks."""
import copy,json,subprocess
from pathlib import Path
import validate as v
HERE=Path(__file__).resolve().parent
g=v.g
def main():
 rows=[];semantics=[]
 for sid,t in g.PROFILES.items():
  r=g.generate(t['difficulty'],0,profile=sid,parameters={'b':9})
  f=r['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);canonical=a[':answer/value'];equivalent='('+canonical+')+1'
  assert v.equal(v.sp.diff(v.scalar(equivalent),v.x),v.prompt_data(r['question']),t['a']*v.x**t['m']+9)
  rows.append({'label':sid+' radio transport diagnostics','record':r,'checks':[{'submitted':'0','expected':'unresolved','purpose':'Foreign numeric answer ID is outside this field; ownership diagnostic, not a mathematical error.'},{'submitted':canonical,'expected':'unresolved','purpose':'Math text in a radio ID transport is malformed, irrespective of mathematical validity.'},{'submitted':equivalent,'expected':'unresolved','purpose':'Legitimate primitive with constant shift +1, submitted as math text to an ID-only radio field; malformed transport, never labeled wrong mathematics.'}]})
  # A blank fixture is a diagnostic only: supported learner output remains
  # original radio. Record the native full-expression equality limitation.
  blank=copy.deepcopy(r);bf=blank['question'][':question/answer-fields'][0];bf[':answer-field/type']=':answer-field.type/blank';blank['question'][':question/problem']+='\n\n{{selection}}'
  rows.append({'label':sid+' primitive semantic diagnostics (authored blank fixture only)','record':blank,'checks':[{'submitted':canonical,'expected':'accepted','purpose':'Canonical primitive accepted by the actual full-expression blank grader.'},{'submitted':equivalent,'expected':'rejected','purpose':'Known native equivalence limitation: +1 is a mathematically valid arbitrary-constant shift, not a wrong primitive. Blank grader checks expression equality rather than derivatives modulo constants.'}]})
  semantics.append({'profile':sid,'canonical':canonical,'valid_equivalent_primitive':equivalent,'independent_derivative_equivalence':True,'normal_response_contract':'select an owned radio answer ID','blank_fixture_role':'Diagnostic only; not a normal output format. Rejection of a +1 shift is a known native semantic limitation, not incorrect mathematics.'})
 v.save('native-diagnostics-input.json',rows)
 subprocess.run([str(HERE/'check-engine'),str(HERE/'native-diagnostics-input.json'),str(HERE/'native-diagnostics.json')],check=True)
 v.save('equivalence-limits.json',{'normal_native_math_unresolved':0,'radio_contract':'Field-owned answer IDs; primitive text is not a valid transport.','primitive_equivalence':'All displayed banks are pairwise distinct after differentiation, so additive integration constants cannot make duplicate choices. Independently verified +1 shifts are legitimate primitive equivalents.','diagnostic_probes':semantics,'logscale_equivalence':'Not applicable: exponent -1, logarithmic integration, and the next rational/logarithm KP are outside this power-rule KP. No logarithmic distractors or claims are introduced.'})
if __name__=='__main__':main()

"""Precise source-preserving display patches not covered by matrix normalization."""
import json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
AUDIT=ROOT/'reference/mathacademy/audits/2026-10-16-mth341-added-targets'
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import validate_prose,normalize_prose
fields=json.loads((AUDIT/'fields.json').read_text())
changes=[]
for f in fields:
 before=f['value'];after=before;reasons=[]
 if f['entity'] in (17592186069113,17592186069114) and f['attribute']==':question/problem':
  bad='coordinates$($\n{{field-1}}\n$$,\n{{field-2}}\n$)$.'
  assert bad in after
  after=after.replace(bad,'coordinates ({{field-1}}, {{field-2}}).')
  reasons.append('Restore the coordinate-pair punctuation around the existing two inline answer fields; remove broken dollar delimiters and preserve field order and IDs.')
 if f['entity']==17592186069129 and f['attribute']==':question/problem':
  assert '$.$a =$' in after
  after=after.replace('$.$a =$','$.\n\n$a =$')
  reasons.append('Separate the existing parameter-answer labels from the preceding sentence so a= does not run into the coordinate punctuation.')
 if '⏟' in after:
  after,count=re.subn(r'\{\{([^{}]+)\}_\{⏟\}\}_\{([ab])\}',lambda m:'\\underbrace{'+m[1]+'}_{'+m[2]+'}',after)
  assert count==2 and '⏟' not in after,(f['entity'],count)
  reasons.append('Replace extracted underbrace glyphs incorrectly nested as subscripts with genuine extensible underbraces; retain the exact coefficient/constant expressions and a/b labels.')
 if before!=after:
  assert re.findall(r'\{\{field-\d+\}\}',before)==re.findall(r'\{\{field-\d+\}\}',after)
  assert re.findall(r'-?\d+',before)==re.findall(r'-?\d+',after)
  validate_prose(normalize_prose(after))
  changes.append({'entity':f['entity'],'attribute':f['attribute'],'before':before,'after':after,'reason':' '.join(reasons)})
assert len(changes)==27,len(changes)
(HERE/'changes.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'fields':len(changes),'entities':len({c['entity'] for c in changes}),'underbrace_fields':sum('underbrace' in c['reason'] for c in changes),'coordinate_fields':sum('coordinate' in c['reason'] for c in changes)},indent=2))

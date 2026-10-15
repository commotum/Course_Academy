"""Reconcile validation with the separate valid-math compatibility audit and freeze."""
import hashlib,json,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result=json.loads((D/'validation.json').read_text());audit=json.loads((D/'blank-equivalents-report.json').read_text())
result['additional_valid_math_blank_audit']={k:audit[k]for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')}
result['limitations']=['The frozen engine leaves 19 exact logarithm-power blank rewrites unresolved. Of 19 primitives differing by a constant absorbed by the supplied +K, 9 are rejected and 10 unresolved. All 19 explicit log(abs(u)) equivalents are accepted. This separate valid-math audit is not counted as a canonical contract pass; no foreign or malformed submissions occur.','No observed hard practice; hard is a conservative authored same-backbone profile.','Legacy unrated q-12500 has no captured correct designation or solution and is reference-only.']
(D/'validation.json').write_text(json.dumps(result,indent=2))
base=json.loads((D/'registered-baseline.json').read_text())['paths'];paths=[D.with_name('17592186068724.py'),*sorted(p for p in D.with_name('17592186068724').rglob('*')if p.is_file())];assert {str(p.relative_to(ROOT)):sha(p)for p in paths}==base
assert sha(D/'check-engine')=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
review=json.loads((D/'review.json').read_text());md=['# Source and served variants','Nine rated source anchors match complete prompt, solution, field contract, ordered banks and correct designation exactly. Each variant uses the same operational named-slot renderer. The legacy unrated record is reference-only. See validation.json for the separate valid-math engine limitations.']
for item in review:
 md.append('## '+item['source'][':question/math-academy-id'])
 for title,q in [('Captured source',item['source']),('Served anchor',item['served_anchor']['question']),('Served variant',item['variant']['question'])]:
  md.extend([title,q[':question/problem'],q[':question/worked-solution'],'Choices: '+json.dumps([a[':answer/value']for a in q[':question/answer-fields'][0][':answer-field/choices']])])
(D/'review.md').write_text('\n\n'.join(md))
# The hard review uses an already independently checked public instance.
records=json.loads((D/'native-input.json').read_text());hard=[r['record']for r in records if r['record']['question'][':question/difficulty']==':question.difficulty/hard'];(D/'hard-review.json').write_text(json.dumps([hard[0],hard[-1]],indent=2))
cap={'supported_levels':['easy','moderate','hard'],'capacities':result['capacities'],'finite_total':sum(c['distinct_math_tasks']for c in result['capacities'].values()),'basis':2275,'hard_provenance':'authored q-113719 same-backbone nonmonic quartic profile','plots':'none','database_writes':0,'registration_changes':0,'native_contract':result['native'],'valid_math_limitations':result['additional_valid_math_blank_audit'],'unsupported':['Legacy unrated source lacks a key and worked solution and is reference-only.']};(D/'capabilities.json').write_text(json.dumps(cap,indent=2))
(D/'engine-limitations.md').write_text('''# Frozen engine compatibility limitations\n\nThe required canonical, explicit-multiplication, additive-zero equivalents and ordinary wrong responses pass over every bounded blank instance; all field-owned radio choices pass their expected results. The separate `blank-equivalents-report.json` audit covers 57 mathematically valid extra entries. All 19 `-4*ln(abs(2*t^2+c))` entries are accepted. All 19 exact logarithm-power rewrites `-ln((2*t^2+c)^4)` are unresolved. Scaling the logarithm argument by 2 changes only a constant absorbed by the supplied +K; nine such entries are rejected and ten unresolved. These are valid-math compatibility limitations, not malformed/foreign submissions or source errors. Symbolic derivative checks and the per-case native probe evidence are retained. No engine modification is proposed.\n''')
files=[D.with_suffix('.py'),*sorted(p for p in D.rglob('*')if p.is_file()and p.name!='freeze.json'and '__pycache__'not in p.parts)]
freeze={'status':'ready for independent parent review; not registered','script_sha256':sha(D.with_suffix('.py')),'basis':2275,'engine_sha256':sha(D/'check-engine'),'registered_baseline_unchanged':True,'excluded_ephemeral':['__pycache__','freeze.json self hash'],'files':{str(p.relative_to(ROOT)):sha(p)for p in files}}
(D/'freeze.json').write_text(json.dumps(freeze,indent=2));print(json.dumps({'script_sha256':freeze['script_sha256'],'files':len(files),'capacity':cap['finite_total'],'native':result['native'],'additional_valid_math_audit':result['additional_valid_math_blank_audit'],'limits':result['limitations']},indent=2))

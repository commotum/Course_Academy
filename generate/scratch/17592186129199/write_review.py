import json,re,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sources=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']
replays=json.loads((HERE/'replayed-sources.json').read_text());variants=json.loads((HERE/'review.json').read_text());validation=json.loads((HERE/'validation.json').read_text())
lines=['# Originals and generated variants','', 'All nine original banks are preserved. Each original is followed by two parameterized generated examples of its family; two examples for each authored hard family appear afterwards. q-161044 has an inferred key/authored moderate difficulty/authored solution. Original source worked solutions are shown as raw Markdown to make the two literal-set brace anomalies visible; generated solutions show their presentation repair. Every displayed radio choice is independently verified as a complete setup object.','', 'Validation: '+str(validation['complete_raw_banks']['matched'])+'/9 raw banks; 45/45 exact values; 8/8 observed keys + 1 independent inference; 6 raw-exact and 2 brace-normalized solutions; '+str(validation['native_checks'])+' real engine checks; '+str(validation['independent_displayed_math_records'])+' displayed-math records. Hard is authored, not observed. Scalar coincidences are in bank-collisions.json and do not define validity for this setup task.','']
def display(rec):
 q=rec['question'];f=q[':question/answer-fields'][0];out=[q[':question/problem'],'']
 for i,a in enumerate(f[':answer-field/choices']):out+= [str(i+1)+'. $'+a[':answer/value']+'$'+(' **Correct setup**' if a[':answer/id']==f[':answer-field/correct'][1] else '')]
 out+=['',q[':question/worked-solution'],''];return out
for old,rep in zip(sources,replays):
 sid=old[':question/math-academy-id'];family=rep['generation']['template'];lines+=['## Original '+sid+' — '+family,'', 'Observed '+old.get(':question/difficulty',{}).get(':db/ident','unrated; moderate assignment is authored')+'. Original raw bank follows; option order is captured order.','',rep['question'][':question/problem'],'']
 for i,a in enumerate(old[':question/answer-fields'][0][':answer-field/choices']):lines+=[str(i+1)+'. $'+a[':answer/value']+'$']
 lines+=['', 'Original solution (raw evidence):','', '```markdown',old.get(':question/worked-solution','[No source worked solution captured]'),'```','']
 for j,rec in enumerate([r for r in variants if r['generation']['template']==family]):
  lines+=['### Generated variant '+str(j+1)+' — '+rec['question'][':question/difficulty'].split('/')[-1],'', 'Parameters: `'+json.dumps(rec['generation']['parameters'])+'`; bank remains the complete observed profile.','']+display(rec)
for family in ('root_product','root_difference'):
 lines+=['## Authored hard extension — '+family,'', 'No observed hard source exists. Same-method origin-centered quarter-sector rewrite with radial-root and double-angle simplification.','']
 for j,rec in enumerate([r for r in variants if r['generation']['template']==family]):lines+=['### Generated hard variant '+str(j+1),'']+display(rec)
(HERE/'review.md').write_text('\n'.join(lines)+'\n')
(HERE/'plot-review.md').write_text('''# Plot visual review

The canonical example and all nine source rasters were viewed in their original full resolution; radius, origin, axes and sector orientation agreed with the independently read mathematical solutions and root reviewer’s domain map. Exact original image copies are retained.

Generated review plots were inspected for full circles, upper/left/lower semicircles and all quadrant sectors. Square and nonsquare radii were inspected. A semicircle D label initially touched an axis and was moved into the interior. Radical intercept labels initially touched a blue boundary; final version 3 places x intercept labels outward and y intercept labels above/below the actual intercept, preserving exact value labels. Final radical √13 lower-left sector shows readable −√13 labels and no collision with its circular edge. Axis arrowheads, x/y labels, D label, equal scale and pale fill are visible; plots carry no extra mathematical branch.

Native same-instance/different-instance concurrent rendering uses fresh private directories. PNG and geometry sidecars are completed through atomic replacement, with only unique private temporary inputs. Sidecars are checked against actual question parameters and exact bounds; no cache-hit-only concurrency claim is made. Original asset hashes, renderer and record hashes are listed in freeze-hashes.json.
''')

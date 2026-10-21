"""Combine reviewed presentation fixes into full uncommitted repair cases."""
import copy,json,re,importlib.util,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent;RUN=HERE.parent
spec=importlib.util.spec_from_file_location('extract',HERE/'extract.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
base=json.loads((RUN/'mapped-cases.json').read_text())['cases'];cases={c['after'][':db/id']:copy.deepcopy(c)for c in base}
done={c['after'][':db/id']for c in json.loads((RUN/'batches/mapped-01/attempt-3730/cases.json').read_text())['cases']}
changed=set();proofs=[]
for fix in json.loads((RUN/'exceptions/further-review/overrides.json').read_text()):
 eid=fix['question_eid'];assert eid not in done
 c=cases[eid];assert c['after'][fix['attribute']]==fix['before'],(eid,fix['attribute'])
 c['after'][fix['attribute']]=fix['after'];changed.add(eid);proofs.append(fix)
all_layout=json.loads((HERE/'overflow-own-overrides.json').read_text())+json.loads((RUN/'exceptions/further-review/overflow-overrides.json').read_text())
assert len({f['field_id']for f in all_layout})==len(all_layout)
(HERE/'overflow-overrides.json').write_text(json.dumps(all_layout,ensure_ascii=False,indent=2)+'\n')
solution_spans=collections.defaultdict(dict)
for fix in all_layout:
 eid=fix['question_eid'];assert eid not in done
 c=cases[eid];f=next(f for f in c['after'][':question/answer-fields']if f[':db/id']==fix['field_id']);obj=next(o for o in c['objects']if o['field_id']==fix['field_id'])
 assert f[':answer-field/key']==obj['content']==fix['before'],eid
 # All overlays are delimiter/spacing-only reflows. Mathematical token order is
 # independently checked after removing dollar delimiters and spacing commands.
 compact=lambda s:re.sub(r'\s+|\$|\\(?:,|;|quad\b|qquad\b)|\\(?:begin|end)\{gathered\}|\\\\|\\(?:left|right)|\\(?=[{}])','',s)
 assert compact(fix['before'])==compact(fix['after']),(eid,'Mathematical token change')
 f[':answer-field/key']=obj['content']=fix['after'];obj['layout_repair']=fix
 changed.add(eid);proofs.append(fix)
 if fix.get('math_spans'):
  spans=fix['math_spans']
 else:
  spans=[]
  for m in mod.MATH.finditer(fix['before']):
   prefix,suffix=fix['before'][:m.start()],fix['before'][m.end():]
   if fix['after'].startswith(prefix) and fix['after'].endswith(suffix):
    replacement=fix['after'][len(prefix):len(fix['after'])-len(suffix)if suffix else None]
    if replacement!=m[0]:spans.append({'before':m[0],'after':replacement})
  assert len(spans)==1,(eid,'Could not identify the one equation span')
 for span in spans:
  previous=solution_spans[eid].get(span['before'])
  assert previous in(None,span['after'])
  solution_spans[eid][span['before']]=span['after']
for eid,spans in solution_spans.items():
 c=cases[eid];old=c['after'].get(':question/worked-solution','')
 new=mod.MATH.sub(lambda m:spans.get(m[0],m[0])if not m[0].startswith('$$')else m[0],old)
 if new!=old:
  c['after'][':question/worked-solution']=new
  proofs.append({'question_eid':eid,'attribute':':question/worked-solution','before':old,'after':new,'reason':'Reuse the same formatting for full-object references and identical isolated inline mathematics; display formulas and all mathematical tokens are unchanged.'})
for fix in json.loads((RUN/'exceptions/further-review/relation-brace-overrides.json').read_text()):
 eid=fix['question_eid'];c=cases[eid];old=c['after'][fix['attribute']];new=old
 for span in fix['math_spans']:
  assert new.count(span['before'])==fix['expected_count_per_span'],(eid,'Relation brace span mismatch')
  new=new.replace(span['before'],span['after'])
 c['after'][fix['attribute']]=new;changed.add(eid)
 proofs.append({**fix,'before':old,'after':new})
held=set(json.loads((RUN/'remaining-render-hold-ids.json').read_text()))
assert changed<=held
changed=held
result={'cases':[cases[eid]for eid in sorted(changed)]}
(HERE/'final-cases.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(HERE/'final-format-proofs.json').write_text(json.dumps(proofs,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'changed_uncommitted_questions':len(changed),'format_fixes':len(proofs),'question_ids':sorted(changed)},indent=2))

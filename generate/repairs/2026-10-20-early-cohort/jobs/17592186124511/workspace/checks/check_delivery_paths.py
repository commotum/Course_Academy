"""Check delivered controlled pairs and construct post-normalization grader cases."""
import importlib.util,json,sys,collections
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('content',ROOT/'checks/check_content.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
records=json.loads((ROOT/'evidence/delivery/accepted.json').read_text());pairs=json.loads((ROOT/'evidence/counterfactual-delivery/accepted.json').read_text())
assert len(pairs)==6
masks=[v.inspect(r)[0] for r in pairs]
assert masks[0]==(True,True,False) and masks[1]==(False,False,True) and masks[2]==(True,False,True)
assert masks[0]==masks[3] and masks[4]==masks[5]
selected={}
for r in records:
 v.inspect(r);selected.setdefault(r['generation']['template'],r)
assert set(selected)==set(v.g.TEMPLATES)
v.save('postdelivery-native-input.json',[v.native(r,'delivered-'+t) for t,r in selected.items()]+[v.native(r,'delivered-counterfactual-'+str(i)) for i,r in enumerate(pairs)])
# Observable presentation cues, including positions after checkbox shuffling.
summary={}
for stage,items in [('before',json.loads((ROOT/'evidence/probe-records.json').read_text())),('after',records)]:
 groups=collections.defaultdict(list)
 for r in items:
  t=r['generation']['template'];fs=r['question'][':question/answer-fields'];radio=fs[0][':answer-field/type'].endswith('/radio')
  cue=(t,'radio' if radio else 'checkbox',len(fs),len(fs[0][':answer-field/choices']))
  response=(str(next(i for i,a in enumerate(fs[0][':answer-field/choices']) if a[':answer/id']==fs[0][':answer-field/correct'][1])) if radio else ''.join('1' if v.correct(f)=='true' else '0' for f in fs))
  groups[cue].append(response)
 summary[stage]={str(k):{'trials':len(rows),'responses':dict(collections.Counter(rows)),'best_constant_response_successes':max(collections.Counter(rows).values())} for k,rows in groups.items()}
 for k,rows in groups.items():assert len(set(rows))>1,('fixed visible response',stage,k)
source=json.loads((ROOT.parent/'source/source.json').read_text());inventory=json.loads((ROOT.parent/'source/inventory.json').read_text());questions=inventory['questions'];generated=[q for q in questions if not q.get(':question/math-academy-id')]
assert not generated
v.save('inventory-assessment.json',{'basis':inventory['basis'],'questions_inspected':len(questions),'source_questions':len(questions),'generated_questions':0,'status':'verified absence of stored generated instances in supplied inventory','finding':'repository import closure failure affects execution/packaging, not the content of an original source question','affected_inventory_file':'../affected-inventory.json','source_questions_marked_as_generated':0})
v.save('surface-cues.json',{'passed':True,'groups':summary,'controlled_pairs_survived_delivery':6,'limits':['A true/false comparison predictable from its mathematical meaning is the assessed theorem, not an incidental cue.','Explicit None is source-backed in two profiles only.','Learner freshness/history, entity IDs and current selection policy are not present; live learner draws were not simulated.'],'selection_code_inspection':'engine/rust/question_selection.rs select() partitions fresh eligible candidates by difficulty and draws within the chosen band; no template/truth-mask filter; legacy unconfigured policy picks the first entity.'})
print('Postdelivery controlled pairs and presentation-cue checks passed; 21 native cases saved. Inventory: 17 originals, zero generated instances.')

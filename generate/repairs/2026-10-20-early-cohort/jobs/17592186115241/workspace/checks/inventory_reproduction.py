"""Reproduce historical generated records without mutating their stored inventory."""
import json,sys,types
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from witness import shortcut
REPO=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(REPO))
from scripts.generator_publish import normalized_question
E=ROOT/'evidence'
original=json.load(open(ROOT/'17592186115241/reference/replenishment/basis-2701/generated.json'))
inv=json.load(open(ROOT.parent/'source/inventory.json'))
old=types.ModuleType('before_repair');old.__file__=str(ROOT/'17592186115241.py')
exec(compile((E/'generator-before.py').read_text(),old.__file__,'exec'),old.__dict__)
records=[];affected=[];checks=[]
for prior in original:
 md=prior['generation'];level=prior['question'][':question/difficulty'].split('/')[-1]
 r=old.generate(level,seed=md['seed'],parameters=md['parameters'],profile=md['bank_profile'])
 matches=[q for q in inv['questions'] if normalized_question(q,identity=False)==normalized_question(r['question'],identity=False)]
 assert len(matches)==1
 q=matches[0]
 assert normalized_question(q,identity=True)==normalized_question(r['question'],identity=True)
 assert all(r['generation'].get(k)==value for k,value in md.items() if k not in ('preparation_basis','source_snapshot'))
 probe=shortcut(r);assert probe.get('unique_modes') and probe.get('correct')
 r['review_evidence']={'metadata_provenance':'pre-repair executable replay of packaged historical generated.json','stored_entity_id':q[':db/id'],'inventory_basis':inv['basis']}
 records.append(r)
 affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Repeated first/second component modes uniquely identify the correct complete vector without inspecting equations.','reproduction':f'python -B checks/inventory_reproduction.py; difficulty={level}, seed={md["seed"]}, parameters='+json.dumps(md['parameters'],separators=(',',':')),'evidence_path':'generated-records.json'})
 checks.append({'id':q[':question/id'],'entity_id':q[':db/id'],'content_and_all_identities_match':True,'generation_matches_historical_metadata':True,'shortcut':probe})
(E/'generated-records.json').write_text(json.dumps(records,indent=2))
(E/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2))
(E/'inventory-results.json').write_text(json.dumps({'captured_count':len(inv['questions']),'generated_reproductions':len(records),'demonstrated_affected':len(affected),'checks':checks,'limits':['Only the ten records with historical generation metadata were reproduced; the rest of the captured inventory is untested for generated provenance. This is not a verified absence of other affected records.','No database changes; no original source question is marked generated.','Stored inventory contains no generation metadata. Seeds/parameters were recovered from the pre-existing historical artifact and verified against exact question/field/answer identities and content.']},indent=2))
print(json.dumps({'reproduced':len(records),'demonstrated_affected':len(affected),'inventory_count':len(inv['questions'])}))

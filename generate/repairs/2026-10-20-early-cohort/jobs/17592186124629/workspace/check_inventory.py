"""Read-only audit of captured inventory provenance; never relabel originals."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
source_path=JOB/'source/source.json'
inventory_path=JOB/'source/inventory.json'
source=json.loads(source_path.read_text())
inventory=json.loads(inventory_path.read_text())
originals={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
questions=inventory['questions']
assert {q[':question/id'] for q in questions}==originals
assert all(not any('generat' in key for key in q) for q in questions)
report=json.loads((ROOT/'evidence/inventory-assessment.json').read_text())
report.update(inventory_basis=inventory['basis'],questions_inspected=len(questions),original_source_questions=len(questions),
              stored_generated_questions=0,demonstrated_generated_instances_affected=0,
              inspected_ids=sorted(originals),inventory_sha256=hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
              reproduction='python check_inventory.py')
(ROOT/'evidence/inventory-assessment.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
print(json.dumps({'status':'pass','original_questions':len(questions),'stored_generated_questions':0,'affected_generated_questions':0}))

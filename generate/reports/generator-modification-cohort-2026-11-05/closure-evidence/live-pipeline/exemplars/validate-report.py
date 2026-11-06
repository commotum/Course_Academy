import json,sys
from pathlib import Path
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from scripts.generator_review import validate_exemplar_review, REVIEW_POLICY_VERSION
r=Path(__file__).resolve().parent
result=json.loads((r/'final-result.json').read_text())
binding=json.loads((r/'context-review-binding.json').read_text())
validate_exemplar_review(result,r,binding)
report={'valid':True,'verdict':result['verdict'],'review_policy_version':REVIEW_POLICY_VERSION,'interface':'scripts.generator_review.validate_exemplar_review','phase':'exemplars','binding':'context-review-binding.json','result':'final-result.json'}
(r/'report-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))

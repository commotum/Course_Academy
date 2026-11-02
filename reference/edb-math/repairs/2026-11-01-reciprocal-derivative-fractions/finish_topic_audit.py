"""Finish all three KP format checks; do not infer missing source answer keys."""
import copy,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from scripts.question_capture.math_format import normalize_fraction_answer_tables,validate_prose
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis'];summary=[];render=[]
for kp in (17592186119939,17592186119940,17592186119941):
    k=jsonable(p.read_kp(kp,H/'whole-topic'/str(kp),basis));questions=[k[':knowledge-point/canonical-example'],*k[':knowledge-point/questions']];issues=[]
    for q in questions:
        for attr in (':question/problem',':question/worked-solution'):
            if q.get(attr):
                validate_prose(q[attr]);assert normalize_fraction_answer_tables(q[attr])==q[attr]
                if re.search(r'^\|',q[attr],re.M):issues.append({'question':q[':db/id'],'attribute':attr,'kind':'table_requires_review'})
        if kp!=17592186119939:
            out=copy.deepcopy(q);fields=out.setdefault(':question/answer-fields',[])
            if any(not f.get(':answer-field/correct') for f in fields):out[':question/answer-fields']=[]
            render.append({'question':out})
    summary.append({'kp':kp,'title':k[':knowledge-point/title'],'practice_questions':len(k[':knowledge-point/questions']),'canonical_examples':1,'remaining_tables':issues,'registered_generator':k.get(':knowledge-point/question-generator')})
    assert not issues
(H/'remaining-topic-render-input.json').write_text(json.dumps(render,indent=2)+'\n')
(H/'whole-topic-audit.json').write_text(json.dumps({'passed':True,'basis':basis,'practice_questions':sum(r['practice_questions'] for r in summary),'canonical_examples':3,'kps':summary,'database_writes':0},indent=2)+'\n')
print(json.dumps(summary,indent=2))

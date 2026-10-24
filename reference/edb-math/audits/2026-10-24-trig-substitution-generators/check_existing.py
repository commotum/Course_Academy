"""Read-only audit of actual stored generated questions and source coverage."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp

H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT));from scripts.generator_publish import normalized_question


def load(kp):
    sys.modules.pop('printed',None)
    path=ROOT/f'generate/scratch/{kp}.py'
    spec=importlib.util.spec_from_file_location('audit_'+str(kp),path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def main():
    topic=json.loads((H/'topic.json').read_text())['topic'];checks=[];cases=[]
    for kp in topic[':topic/knowledge-points']:
        if kp[':db/id']not in (17592186068917,17592186068918):continue
        g=load(kp[':db/id'])
        for question in kp[':knowledge-point/questions']:
            if question.get(':question/math-academy-id'):continue
            body,lo,hi=g.p.integral(question[':question/problem']);assert lo is None and hi is None
            field=question[':question/answer-fields'][0];correct=field[':answer-field/correct'][':answer/id'];matches=[]
            for a in field[':answer-field/choices']:
                value=g.p.scalar(a[':answer/value'])
                if sp.trigsimp(sp.diff(value,g.x)-body)==0:matches.append(a[':answer/id'])
            assert matches==[correct],(question[':db/id'],matches,correct)
            q=normalized_question(question)
            for f in q[':question/answer-fields']:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct']]
            record={'knowledge_point':{'db_id':kp[':db/id'],'title':kp[':knowledge-point/title']},'question':q,'generation':{'template':'current-stored-generated'}}
            cases.append({'label':'stored '+str(question[':db/id']),'record':record,'checks':[
                {'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected'}for a in field[':answer-field/choices']]})
            checks.append({'question':question[':db/id'],'kp':kp[':db/id'],'derivative_and_unique_key_verified':True})
    product=load(17592186068917);hard=list(product.candidates('hard'));zeros=[(t,p)for t,p in hard if product.math_data(t,p['m'])[2]==0]
    assert len(hard)==55 and len(zeros)==22
    summary={'stored_generated_math_verified':checks,'product_hard_candidates':len(hard),'product_hard_zero_candidates':len(zeros),
             'zero_families':dict(Counter(t for t,p in zeros)),'database_writes':0}
    (H/'existing-math-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    (H/'existing-grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
    print(json.dumps({'stored_generated_math_verified':len(checks),'hard_zero_candidates':len(zeros),'hard_candidates':len(hard)}))


if __name__=='__main__':main()

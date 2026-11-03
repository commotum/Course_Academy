"""Fraction-fence changes only; preserve every mathematical token and key."""
import copy,json,re,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import scalable_fraction_parentheses as fix,normalize_fraction_fences_prose as prose

def signature(text):
    text=text.replace(r'\left','').replace(r'\right','').replace(r'\langle','⟨').replace(r'\rangle','⟩')
    return re.sub(r'\s+','',text)

def main():
    kps=json.loads((H/'lesson-before.json').read_text());changes={};questions=[];after=copy.deepcopy(kps)
    def propose(e,attr,before,desired):
        if before==desired:return
        assert signature(before)==signature(desired)
        assert (fix(desired) if attr=='answer/value' else prose(desired))==desired
        key=e,attr;row={'entity':e,'attribute':attr,'before':before,'after':desired}
        assert key not in changes or changes[key]==row;changes[key]=row
    for kp,k in after.items():
        for role,q in [('practice',q) for q in k[':knowledge-point/questions']]+[('canonical',k[':knowledge-point/canonical-example'])]:
            start=len(changes)
            for attr in (':question/problem',':question/worked-solution'):
                if attr in q:
                    desired=prose(q[attr]);propose(q[':db/id'],attr[1:],q[attr],desired);q[attr]=desired
            for field in q.get(':question/answer-fields',[]):
                for a in field.get(':answer-field/choices',[]):
                    kind=a[':answer/type'][':db/ident'];value=a[':answer/value']
                    desired=fix(value) if kind==':answer.type/math' else prose(value) if kind==':answer.type/text' else value
                    propose(a[':db/id'],'answer/value',value,desired);a[':answer/value']=desired
                correct=field.get(':answer-field/correct')
                if correct:field[':answer-field/correct']=next(a for a in field[':answer-field/choices'] if a[':db/id']==correct[':db/id'])
            if len(changes)>start:questions.append({'entity':q[':db/id'],'kp':int(kp),'role':role})
    for item in json.loads((H/'lessons.json').read_text()):
        for step in item[0].get(':activity/steps',[]):
            content=step[':step/content']
            if content.get(':tutorial/content'):
                value=content[':tutorial/content'];propose(content[':db/id'],'tutorial/content',value,prose(value))
    proposals=list(changes.values());(H/'proposals.json').write_text(json.dumps(proposals,indent=2)+'\n')
    (H/'lesson-after.json').write_text(json.dumps(after,indent=2)+'\n')
    affected={r['entity'] for r in questions};render=[]
    for k in after.values():
        for q in k[':knowledge-point/questions']+[k[':knowledge-point/canonical-example']]:
            if q[':db/id'] in affected:
                q=copy.deepcopy(q);q[':question/answer-fields']=[f for f in q.get(':question/answer-fields',[]) if f.get(':answer-field/correct')]
                render.append({'knowledge_point':{'title':k[':knowledge-point/title']},'question':q})
    (H/'render-input.json').write_text(json.dumps(render,indent=2)+'\n')
    report={'passed':True,'questions_audited':sum(len(k[':knowledge-point/questions'])+1 for k in kps.values()),
        'questions_affected':questions,'text_fields_repaired':len(proposals),'by_attribute':dict(Counter(r['attribute'] for r in proposals)),
        'only_sizing_commands_and_equivalent_angle_glyphs_changed':True,'identities_and_correct_links_preserved':True}
    (H/'audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='questions_affected'},indent=2))

if __name__=='__main__':main()

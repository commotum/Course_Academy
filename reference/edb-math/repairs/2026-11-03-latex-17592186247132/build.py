"""Audit the entire lesson and prepare operator-only changes."""
import copy,json,re,sys
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import MATH,normalize_inverse_trig_operators as fix,validate_tex

def prose(text):return MATH.sub(lambda m:fix(m[0]),text)
def skeleton(text):
    # Formatting wrappers/commands around these names have no mathematical role.
    text=re.sub(r'\\(?:operatorname|text|textrm|mathrm|mathit|mathbf)\s*\{\s*(arcsec|arccsc|arccot)\s*\}',r'\1',text)
    text=re.sub(r'\\(arcsec|arccsc|arccot)',r'\1',text)
    return re.sub(r'\s+','',text)

def main():
    rows=json.loads((H/'lesson-questions.json').read_text());source=json.loads((H/'source/source.json').read_text())
    changes={};after=copy.deepcopy(rows);questions=[];answers=[]
    def change(eid,attr,before,after,kind):
        if before==after:return
        assert skeleton(before)==skeleton(after),(eid,attr,before,after)
        key=(eid,attr);row={'entity':eid,'attribute':attr,'before':before,'after':after,'kind':kind}
        assert key not in changes or changes[key]==row
        changes[key]=row
    for old,new in zip(rows,after):
        q,n=old['question'],new['question'];affected=False
        for attr in ('question/problem','question/worked-solution'):
            key=':'+attr
            if key in q:
                n[key]=prose(q[key]);change(q[':db/id'],attr,q[key],n[key],old['role'])
                affected |= n[key]!=q[key]
        for field in n.get(':question/answer-fields',[]):
            for a in field.get(':answer-field/choices',[]):
                kind=a[':answer/type'][':db/ident']
                before=a[':answer/value'];value=fix(before) if kind==':answer.type/math' else prose(before) if kind==':answer.type/text' else before
                change(a[':db/id'],'answer/value',before,value,'answer');a[':answer/value']=value
                if before!=value:affected=True;answers.append(a[':db/id'])
                if a.get(':answer/feedback'):
                    feedback=a[':answer/feedback'];fixed=prose(feedback)
                    change(a[':db/id'],'answer/feedback',feedback,fixed,'feedback');a[':answer/feedback']=fixed
                if kind==':answer.type/math':validate_tex(value)
            # Correct answers are pulled again, but they refer to the same entity.
            if field.get(':answer-field/correct'):
                correct=field[':answer-field/correct'];field[':answer-field/correct']=next(a for a in field[':answer-field/choices'] if a[':db/id']==correct[':db/id'])
        if affected:questions.append({'entity':q[':db/id'],'kp':old['kp'],'source':q.get(':question/math-academy-id'),'role':old['role']})
    for lesson in source['material']['lessons']:
        for step in lesson[':activity/steps']:
            c=step[':step/content']
            if ':tutorial/content' in c:
                before=c[':tutorial/content'];change(c[':db/id'],'tutorial/content',before,prose(before),'tutorial')
    proposals=list(changes.values());(H/'proposals.json').write_text(json.dumps(proposals,indent=2)+'\n')
    (H/'lesson-questions-repaired.json').write_text(json.dumps(after,indent=2)+'\n')
    affected={r['entity'] for r in questions};render=[]
    for r in after:
        if r['question'][':db/id'] not in affected:continue
        q=r['question'];q.setdefault(':question/answer-fields',[])
        # A partial import can be previewed without inventing its missing key.
        q=copy.deepcopy(q);q[':question/answer-fields']=[f for f in q[':question/answer-fields'] if f.get(':answer-field/correct')]
        render.append({'knowledge_point':{'db_id':r['kp'],'title':r['title']},'question':q})
    (H/'render-input.json').write_text(json.dumps(render,indent=2)+'\n')
    report={'passed':True,'questions_audited':len(rows),'practice_imports':sum(bool(r['question'].get(':question/math-academy-id')) for r in rows if r['role']=='practice'),
        'practice_generated':sum(not bool(r['question'].get(':question/math-academy-id')) for r in rows if r['role']=='practice'),
        'questions_affected':questions,'by_kp':dict(Counter(r['kp'] for r in questions)),
        'changed_answers':sorted(set(answers)),'changes_by_kind':dict(Counter(r['kind'] for r in proposals)),
        'formatting_skeleton_unchanged':True,'field_answer_identities_and_correct_links_preserved':True,
        'incomplete_import_keys_not_invented':True}
    (H/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('questions_affected','changed_answers')},indent=2))

if __name__=='__main__':main()

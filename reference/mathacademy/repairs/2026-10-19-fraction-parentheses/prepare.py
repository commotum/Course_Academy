"""Apply fraction fence sizing, preserving all other lesson content exactly."""
import copy,hashlib,importlib.util,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('fraction_formatter',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def scale(value,bare=False):return fmt.scalable_fraction_parentheses(value) if bare else fmt.MATH.sub(lambda m:fmt.scalable_fraction_parentheses(m[0]),value)
def run():
    questions=json.loads((HERE/'questions.json').read_text());activities=json.loads((HERE/'activities.json').read_text());tutorials={t[':db/id']:t for [a] in activities for step in a.get(':activity/steps',[]) for t in [step.get(':step/content',{})] if ':tutorial/content' in t};changes={};checks=0
    def visit(entity,attribute,bare=False):
        nonlocal checks
        old=entity.get(attribute)
        if not isinstance(old,str):return
        checks+=1;new=scale(old,bare)
        assert re.sub(r'\\(?:left|right)','',old)==re.sub(r'\\(?:left|right)','',new)
        if old!=new:
            change={'entity':entity[':db/id'],'attribute':attribute,'before':old,'after':new}
            key=entity[':db/id'],attribute
            if key in changes:assert changes[key]==change
            changes[key]=change
    for [q] in questions:
        for key in (':question/problem',':question/worked-solution'):visit(q,key)
        for f in q.get(':question/answer-fields',[]):
            for a in f.get(':answer-field/choices',[])+[f.get(':answer-field/correct',{})]:
                kind=a.get(':answer/type',{});kind=kind.get(':db/ident') if isinstance(kind,dict) else kind
                visit(a,':answer/value',kind==':answer.type/math');visit(a,':answer/feedback')
    for t in tutorials.values():visit(t,':tutorial/content')
    after=copy.deepcopy(questions);tafter=copy.deepcopy(list(tutorials.values()))
    def apply(value):
        if isinstance(value,list):
            for v in value:apply(v)
        elif isinstance(value,dict):
            for (entity,key),c in changes.items():
                if value.get(':db/id')==entity and key in value:assert value[key]==c['before'];value[key]=c['after']
            for v in value.values():apply(v)
    apply(after);apply(tafter)
    records=[];index=[]
    for [q] in after:
        p=copy.deepcopy(q)
        # Canonical examples have no selection fields. Missing source keys are
        # preview-only omissions; no answer data is authored by this repair.
        p[':question/answer-fields']=[f for f in p.get(':question/answer-fields',[]) if f.get(':answer-field/correct')]
        records.append({'question':p});index.append({'kind':'question','entity':q[':db/id']})
    for t in tafter:
        records.append({'question':{':question/problem':t[':tutorial/content'],':question/worked-solution':'',':question/answer-fields':[]}});index.append({'kind':'tutorial','entity':t[':db/id']})
    save('changes.json',list(changes.values()));save('questions-after.json',after);save('tutorials-before.json',list(tutorials.values()));save('tutorials-after.json',tafter);save('render-input.json',records);save('render-index.json',index)
    summary={'passed':True,'questions':len(questions),'tutorials':len(tutorials),'fields_checked':checks,'fields_repaired':len(changes),'entities_repaired':len({c['entity'] for c in changes.values()}),'attributes':sorted({c['attribute'] for c in changes.values()}),'only_scalable_fences_added':True,'changes_sha256':hashlib.sha256((HERE/'changes.json').read_bytes()).hexdigest()};save('audit.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':run()

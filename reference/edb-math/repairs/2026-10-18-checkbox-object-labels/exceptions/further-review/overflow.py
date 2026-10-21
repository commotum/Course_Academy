"""Wrap reviewed long equations at existing relation/addition boundaries."""
import copy,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
MATH=re.compile(r'(?<!\\)\$(?!\$)(?:\\.|[^$])*?(?<!\\)\$')

def top_indices(body,chars):
    depth={'{':0,'(':0,'[':0};closing={'}':'{',')':'(',']':'['};found=[];i=0
    while i<len(body):
        c=body[i]
        if c=='\\':
            m=re.match(r'\\[a-zA-Z]+|\\.',body[i:]);i+=len(m[0])if m else 1;continue
        if c in depth:depth[c]+=1
        elif c in closing:depth[closing[c]]-=1
        elif c in chars and all(v==0 for v in depth.values()):found.append(i)
        if any(v<0 for v in depth.values()):return []
        i+=1
    return found if all(v==0 for v in depth.values())else[]

def main():
    original=json.loads((ROOT/'mapped-cases.json').read_text())['cases']
    cases={c['question']:c for c in original}
    over=json.loads((ROOT/'mapping/overflow-review.json').read_text())
    owned=[];overrides=[];revised={}
    for row in over:
        qid=row['question_eid'];case=cases[qid]
        fields=sorted(case['after'][':question/answer-fields'],key=lambda f:f[':db/id'])
        field=fields[row['choice_index']];key=field[':answer-field/key']
        candidates=[]
        for math_index,math in enumerate(MATH.finditer(key)):
            body=math[0][1:-1]
            if '\\begin{' in body or ':' in body or top_indices(body,','):continue
            equals=top_indices(body,'=')
            if len(equals)!=1:continue
            # Only the substantial formula causing the measured overflow; do
            # not alter unrelated short mathematical spans in a prose caption.
            rights=row['choice'].get('svgRights',[])
            if math_index>=len(rights) or rights[math_index]<=row['choice']['right']+1:continue
            candidates.append((math,equals[0]))
        if len(candidates)!=1:continue
        math,eq=candidates[0];body=math[0][1:-1]
        cuts=[eq]+[i for i in top_indices(body,'+-−')if i>eq+1]
        parts=[body[a:b].strip()for a,b in zip([0]+cuts,cuts+[len(body)])]
        if not all(parts):continue
        replacement=' '.join('$'+p+'$'for p in parts)
        after=key[:math.start()]+replacement+key[math.end():]
        # Dollar-delimiter insertion and whitespace are the only changes.
        assert re.sub(r'\s+','',key.replace('$',''))==re.sub(r'\s+','',after.replace('$',''))
        override={'question_eid':qid,'field_id':field[':db/id'],'before':key,'after':after,'math_spans':[{'before':math[0],'after':replacement}],'reason':'Allow the unchanged equation to wrap at its equality and outer additive operators; every mathematical token is preserved.'}
        overrides.append(override);owned.append({'question_eid':qid,'field_id':field[':db/id'],'choice_index':row['choice_index'],'before':key})
        if qid not in revised:revised[qid]=copy.deepcopy(case)
        target=revised[qid]
        for f in target['after'][':question/answer-fields']:
            if f[':db/id']==field[':db/id']:f[':answer-field/key']=after
        for obj in target['objects']:
            if obj['field_id']==field[':db/id']:obj['content']=after
    (HERE/'overflow-owned.json').write_text(json.dumps(owned,ensure_ascii=False,indent=2)+'\n')
    (HERE/'overflow-overrides.json').write_text(json.dumps(overrides,ensure_ascii=False,indent=2)+'\n')
    (HERE/'overflow-cases.json').write_text(json.dumps({'cases':list(revised.values())},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'questions':len(revised),'fields':len(overrides),'ids':sorted(revised)}))
if __name__=='__main__':main()

"""Reviewed, exact-math layout repairs; this script never writes the database."""
import copy,json,re,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
CAPTURE=HERE/'capture-3479/snapshot.json'
MATRIX=re.compile(r'([A-D])\s*=\s*(\\begin\{bmatrix\}(.*?)\\end\{bmatrix\})',re.S)
STATEMENT=re.compile(r'(?m)^\s*(?:-\s*)?(?:\*\*)?(III|II|I)\.(?:\*\*)?\s+(.+?)\s*$')
CONVERT={17592186571387,17592186571390,17592186571405,17592186571420}
RETIRE=17592186571448
def matrix(body):return sp.Matrix([[sp.Rational(v.strip()) for v in r.split('&')] for r in body.split(r'\\')])
def direction_test(m,direction):return bool(m.is_upper if direction=='upper' else m.is_lower)
def statement_truth(text,m,name):
    match=re.fullmatch(r'\$(.*?)\$ is (upper|lower) triangular\.?',text)
    assert match,text
    expression=match[1].replace('{','').replace('}','').replace(' ','')
    terms=re.findall(r'([+-]?)([A-D](?:\^T)?)',expression)
    assert ''.join(sign+term for sign,term in terms)==expression,expression
    value=sp.zeros(m.rows)
    for sign,term in terms:
        assert term[0]==name
        value+=(-1 if sign=='-' else 1)*(m.T if term.endswith('^T') else m)
    return direction_test(value,match[2])
def key(f):return f[':answer-field/correct'][':answer/value']=='true'
def native_field(q,label,content,truth):
    fid=uuid.uuid5(uuid.UUID(q[':question/id']),'checkbox-object-v2:'+label)
    choices=[{':answer/id':str(uuid.uuid5(fid,value)),':answer/type':':answer.type/text',':answer/value':value} for value in ['false','true']]
    return {':answer-field/id':str(fid),':answer-field/key':content,':answer-field/type':':answer-field.type/checkbox',
        ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[int(truth)][':answer/id']]}
def selections(text,labels):
    if text.strip()=='None':return []
    values=re.findall(r'\b(?:III|II|I)\b' if labels==['I','II','III'] else r'\b[A-C]\b',text)
    assert values and len(set(values))==len(values) and set(values)<=set(labels),text
    return values
def main():
    snapshot=json.loads(CAPTURE.read_text());plans=[];afters=[];retained=[]
    for [q] in snapshot['questions']:
        fs=q.get(':question/answer-fields',[])
        if not fs:continue
        checkbox=all(f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox' for f in fs)
        if not checkbox and q[':db/id'] not in CONVERT:
            if q[':db/id']!=RETIRE:retained.append({'id':q[':db/id'],'reason':'Single best description or a single complete matrix answer; no detached option list.'})
            continue
        before=q[':question/problem'];after=copy.deepcopy(q);matches=list(STATEMENT.finditer(before));objects=[]
        if matches:
            assert [m[1] for m in matches]==['I','II','III']
            anchor=MATRIX.search(before);assert anchor
            m=matrix(anchor[3]);name=anchor[1]
            for match in matches:
                text=match[2].rstrip('.')+'.'
                objects.append({'source_label':match[1],'content':text,'truth':statement_truth(text,m,name),'source_fragment':match[0].strip()})
            prefix=before[:matches[0].start()].strip()
            prefix=re.sub(r'Consider the matrix\s+\$.*?\$\.?\s*',lambda _:f'Consider the matrix\n\n$$\n{name}={anchor[2]}\n$$\n\n',prefix,count=1,flags=re.S)
            if 'Select all that apply.' not in prefix:prefix+='\n\nSelect all that apply.'
            after[':question/problem']=prefix
            worked=q[':question/worked-solution']
            for obj in sorted(objects,key=lambda o:len(o['source_label']),reverse=True):
                # Replace the source identifier while retaining its full explanation.
                worked=re.sub(r'Statement '+obj['source_label']+r' is (true|false)',
                    lambda mo:obj['content'].rstrip('.')+': **'+mo[1].capitalize()+'.**',worked)
            worked=re.sub(r'\n\nTherefore, the correct answer is .*?\.?$',
                '\n\nThe true statements are:\n\n'+'\n'.join('- '+o['content'] for o in objects if o['truth']),worked,flags=re.S)
            if q[':db/id']==17592186120426:
                worked='$A$ is neither upper nor lower triangular because $a_{12}=1$ and $a_{21}=-1$ are both nonzero. However,\n\n$$\nA^{T}+A=\\begin{bmatrix}-6 & 0 & 0 \\\\ 0 & 2 & 0 \\\\ 0 & 0 & 10\\end{bmatrix}\n$$\n\nis diagonal, so $A^{T}+A$ is upper triangular.'
            corrections=[]
            if q[':db/id']==17592186262616:
                assert '$A$ has non-zero entries above' in worked
                worked=worked.replace('$A$ has non-zero entries above','$B$ has non-zero entries above')
                corrections.append('Corrected a solution typo naming A instead of B.')
            if q[':db/id']==17592186262618:
                old='${B}^{T}$ is lower triangular: **False.**, since $B$ has non-zero entries below the main diagonal:'
                assert old in worked
                worked=worked.replace(old,'${B}^{T}$ is lower triangular: **False.** It has non-zero entries above the main diagonal:')
                corrections.append('Corrected the transpose explanation: B transpose has a nonzero entry above its diagonal.')
            worked=worked.replace('**True.**.','**True.**').replace('**False.**.','**False.**')
            worked=worked.replace('**True.**, since','**True.** This holds because').replace('**False.**, since','**False.** This fails because')
            after[':question/worked-solution']=worked
        else:
            anchors=list(MATRIX.finditer(before));assert [a[1] for a in anchors]==['A','B','C']
            direction=re.search(r'are (upper|lower) triangular',before)[1]
            objects=[{'source_label':a[1],'content':f'${a[1]}={a[2]}$','truth':direction_test(matrix(a[3]),direction),'source_fragment':a[0]} for a in anchors]
            after[':question/problem']=f'Which of the following matrices are {direction} triangular matrices?\n\nSelect all that apply.'
            corrections=[]
        assert any(o['truth'] for o in objects), 'Do not introduce an all-false practice case'
        labels=[o['source_label'] for o in objects]
        if checkbox:
            bylabel={f[':answer-field/key']:f for f in fs};assert set(bylabel)==set(labels)
            for o in objects:
                f=bylabel[o['source_label']];assert key(f)==o['truth'],q[':db/id']
                o['field_id']=f[':answer-field/id'];o['field_eid']=f[':db/id']
            byid={f[':db/id']:f for f in after[':question/answer-fields']}
            for o in objects:byid[o['field_eid']][':answer-field/key']=o['content']
            mapping=[]
        else:
            assert len(fs)==1
            mapping=[{'old_answer':a[':db/id'],'value':a[':answer/value'],'selected_labels':selections(a[':answer/value'],labels)} for a in fs[0][':answer-field/choices']]
            expected={o['source_label'] for o in objects if o['truth']}
            canonical=next(x for x in mapping if x['old_answer']==fs[0][':answer-field/correct'][':db/id'])
            assert set(canonical['selected_labels'])==expected,q[':db/id']
            after[':question/answer-fields']=[native_field(q,o['source_label'],o['content'],o['truth']) for o in objects]
            for o,f in zip(objects,after[':question/answer-fields']):o['field_id']=f[':answer-field/id']
            assert not any(qid==q[':db/id'] for qid,_ in snapshot['items']), 'Response migration required'
        plans.append({'question':q[':db/id'],'math_academy_id':q.get(':question/math-academy-id'),'kp_ids':[k[':db/id'] for k in q[':knowledge-point/_questions']],
            'decision':'repair_checkbox_labels' if checkbox else 'convert_radio','objects':objects,'choice_mapping':mapping,'separate_solution_corrections':corrections,
            'before':q,'after':after})
        afters.append(after)
    assert len(plans)==20 and sum(p['decision']=='convert_radio' for p in plans)==4
    bad=next(q for [q] in snapshot['questions'] if q[':db/id']==RETIRE)
    match=MATRIX.search(bad[':question/problem']);m=matrix(match[3])
    assert all(not statement_truth(s[2],m,match[1]) for s in STATEMENT.finditer(bad[':question/problem']))
    assert bad[':question/answer-fields'][0][':answer-field/correct'][':answer/value']=='None'
    assert not any(qid==RETIRE for qid,_ in snapshot['items'])
    data={'basis':snapshot['basis'],'lineage':snapshot['lineage'],'source':':agent/gpt-6.1-sol-high','cases':plans,'retained_radios':retained,
        'retire':{'question':RETIRE,'kp':17592186119784,'reason':'Original MA all-false combination question, unseen/unanswered; withdraw under the user no-all-false preference.','before':bad}}
    (HERE/'content-plan.json').write_text(json.dumps(data,indent=2)+'\n')
    (HERE/'after-questions.json').write_text(json.dumps(afters,indent=2)+'\n')
    print(json.dumps({'label_repairs':16,'radio_conversions':4,'all_false_retirements':1,'retained_radios':len(retained),'exact_truth_verified':True}))
if __name__=='__main__':main()

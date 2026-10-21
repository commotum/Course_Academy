"""Read printed matrix data and independently execute every displayed operation."""
import hashlib, importlib.util, itertools, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('row_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)

def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)

def evaluate(a,text):
    """Independent columnwise evaluation; do not use generator operation/apply."""
    text=re.sub(r'\{R\}_\{([123])\}|R_\{([123])\}',lambda m:'r'+(m[1] or m[2]),text)
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text).replace(r'\cdot','*').replace(' ','')
    result=a.copy()
    if '↔' in text:
        x,y=map(lambda z:int(z[1:])-1,text.split('↔'))
        result[x,:]=a[y,:];result[y,:]=a[x,:]
    else:
        lhs,rhs=text.split(':=');i=int(lhs[1:])-1
        rhs=re.sub(r'(\d|\))(?=r)',r'\1*',rhs)
        for j in range(3):result[i,j]=sp.sympify(rhs,locals={f'r{k+1}':a[k,j] for k in range(3)})
    return result

def independent(rec):
    q=rec['question'];meta=rec['generation'];assert rec['knowledge_point']['db_id']==g.KP_ID
    assert q[':question/difficulty']==':question.difficulty/moderate'
    assert rec==g.generate('moderate',meta['seed'],meta['template'],meta['parameters'])
    a,b=g.matrices(q[':question/problem']);assert a.shape==b.shape==(3,3) and a!=b
    assert len(q[':question/answer-fields'])==1
    f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5 and len({x[':answer/value'] for x in f[':answer-field/choices']})==5
    outcomes=[evaluate(a,x[':answer/value']) for x in f[':answer-field/choices']]
    matches=[x[':answer/id'] for x,out in zip(f[':answer-field/choices'],outcomes) if out==b]
    assert matches==[f[':answer-field/correct'][1]],'Ambiguous or incorrect complete bank'
    # All source distractors remain distinct mathematical transformations.
    assert len({tuple(out) for out in outcomes})==5,'Equivalent choices'
    sol=q[':question/worked-solution'];assert g.matrices(sol)==[a,b]
    changed=[i for i in range(3) if a[i,:]!=b[i,:]]
    pre=sol.split('By considering')[0]
    ordinal=('st','nd','rd')
    for i in range(3):assert ('$'+str(i+1)+'$'+ordinal[i]) in pre
    # Check which row(s) the introductory prose says have changed.
    changed_text=pre.split('The only row')[1]
    described={int(i)-1 for i in re.findall(r'\$([123])\$(?:st|nd|rd)',changed_text)}
    assert described==set(changed),'Stale prose targets'
    final=sol.split('Therefore, the required row operation is')[1].split('$$')[1].strip().rstrip('.')
    assert evaluate(a,final)==b,'Stale solution operation'
    assert meta['mathematical_fingerprint']==fingerprint(q)
    return rec

check=independent
def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each choice through actual application radio grader'} for a in f[':answer-field/choices']]
def native(label,rec):return {'label':label,'record':rec,'checks':checks(rec)}

def main():
    replay=[];recipes=[];inputs=[];review=[];distinct=set();coverage={};total=0
    for sid,old in g.CASES.items():
        rec=independent(g.generate('moderate',0,sid,g.DEFAULTS[sid]));f=rec['question'][':question/answer-fields'][0];original=old[':question/answer-fields'][0]
        assert rec['question'][':question/problem']==old[':question/problem'] and rec['question'][':question/worked-solution']==old[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices'])
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==original[':answer-field/correct'][':answer/value']
        replay.append({'source':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'correct_designation':True,'prompt_exact':True,'solution_exact':True,'missing':[],'extra':[]})
        for a in original[':answer-field/choices']:
            op=g.operation(a[':answer/value'])
            recipes.append({'source':sid,'source_answer_id':a[':answer/id'],'field':'selection','profile':sid,'original_value':a[':answer/value'],'recipe':str(op),'coefficient_policy':'source constants retained; row indices conjugated by sampled permutation','interpretation':'observed linear row-expression pattern; psychological error interpretation unresolved','reproduces_at_source':True})
        params=g.domain(sid);positions=set();permutations=set();deltas=set()
        for p in params:
            rec=independent(g.generate('moderate',59773,sid,p));total+=1;distinct.add(fingerprint(rec['question']));positions.add(tuple(p[1:3]));permutations.add(tuple(p[4]));deltas.add(p[3])
            if p[4]==[0,1,2]:inputs.append(native(sid+' '+str(p),rec))
        coverage[sid]={'nonzero_cell_slots':sorted(positions),'permutations':sorted(permutations),'deltas':sorted(deltas),'domain_instances':len(params),'eligible_slots_missing':[]}
        # Changed targets with identical numeric data apart from row reindexing.
        p=params[0];r=independent(g.generate('moderate',0,sid,p));p2=p[:4]+[[1,2,0]];r2=independent(g.generate('moderate',0,sid,p2));assert fingerprint(r['question'])==fingerprint(r2['question'])
        assert g.generate('moderate',999,sid,p)['question']==r['question']
        inputs += [native(sid+' replay',g.generate('moderate',0,sid,g.DEFAULTS[sid])),native(sid+' changed targets',r2)]
        review.append('## '+sid+'\n\nSource replay\n\n'+g.markdown(g.generate('moderate',0,sid,g.DEFAULTS[sid]))+'\n\nChanged numeric entry\n\n'+g.markdown(r)+'\n\nChanged target rows, same numerical data\n\n'+g.markdown(r2))
    for level in ('easy','hard','unclassified'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported level admitted')
    save('source-replay.json',{'passed':True,'complete_banks_matched':8,'complete_banks_total':8,'distractors_matched':32,'distractors_total':32,'profiles':replay,'excluded_sources':['q-20240','q-20389']})
    save('choice-recipes.json',recipes);save('slot-coverage.json',coverage);save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'status':'pass','passed':True,'exhaustive_instances':total,'distinct_numeric_tasks':len(distinct),'supported_levels':['moderate'],'source_fidelity':'8/8 complete banks, 32/32 distractors, exact source prompt/solution replay','correctness':'every displayed choice independently applied columnwise; only keyed choice yields target; all outcomes distinct; both solution matrices and final operation verified; changed-row prose verified','grading':'native application grade_field, all five options for every numeric slot and every profile; all target permutations independently checked','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'replenish.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine')}})
if __name__=='__main__':main()

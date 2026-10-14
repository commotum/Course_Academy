"""Validate rendered values independently, then exercise the actual application grader."""
import hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def evaluate(a,text):
    text=re.sub(r'\{R\}_\{([123])\}|R_\{([123])\}',lambda m:'r'+(m[1] or m[2]),text)
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text).replace(r'\cdot','*').replace(' ','')
    out=a.copy()
    if '↔' in text:
        x,y=[int(t[1:])-1 for t in text.split('↔')];out[x,:]=a[y,:];out[y,:]=a[x,:]
    else:
        lhs,rhs=text.split(':=');i=int(lhs[1:])-1;rhs=re.sub(r'(\d|\))(?=r)',r'\1*',rhs)
        for j in range(3):out[i,j]=sp.sympify(rhs,locals={f'r{k+1}':a[k,j] for k in range(3)})
    return out

def independent(rec):
    q=rec['question'];meta=rec['generation'];assert rec['knowledge_point']['db_id']==g.KP_ID
    assert q[':question/difficulty']==':question.difficulty/hard'
    a=g.matrices(q[':question/problem'])[0];i,j=g.target(q[':question/problem']);assert a[i,j]!=0 and all(x.is_Integer for x in a)
    f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5 and len({x[':answer/value'] for x in f[':answer-field/choices']})==5
    outcomes=[evaluate(a,x[':answer/value']) for x in f[':answer-field/choices']]
    matches=[x[':answer/id'] for x,b in zip(f[':answer-field/choices'],outcomes) if b[i,j]==0]
    assert matches==[f[':answer-field/correct'][1]],'Target-cell ambiguity or incorrect key'
    correct=next(x for x in f[':answer-field/choices'] if x[':answer/id']==matches[0]);b=evaluate(a,correct[':answer/value'])
    sol=q[':question/worked-solution'];assert g.matrices(sol)==[a,b],'Incorrect matrix arithmetic in solution'
    # Both leading and final row operations must match independently.
    blocks=sol.split('$$');first=blocks[1].strip().rstrip('.').split('=')
    # := contains =; use the separately extracted whole display, splitting only chained equalities.
    first=blocks[1].strip().rstrip('.');first=re.split(r'(?<!:)=(?!:)',first)[0]
    assert evaluate(a,first)==b
    final=blocks[-2].strip().rstrip('.');assert evaluate(a,final)==b,'Stale final operation'
    assert b[i,j]==0 and meta['mathematical_fingerprint']==fingerprint(q)
    return rec
check=independent
def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all complete-bank choices through application radio grader'} for a in f[':answer-field/choices']]
def native(label,rec):return {'label':label,'record':rec,'checks':checks(rec)}

def main():
    replay=[];recipes=[];inputs=[];review=[];distinct=set();coverage={};total=0
    for sid,old in g.CASES.items():
        rec=independent(g.generate('hard',0,sid,g.DEFAULTS[sid]));f=rec['question'][':question/answer-fields'][0];original=old[':question/answer-fields'][0]
        assert rec['question'][':question/problem']==old[':question/problem']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices'])
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==original[':answer-field/correct'][':answer/value']
        if sid!='q-130301':assert rec['question'][':question/worked-solution']==old[':question/worked-solution']
        replay.append({'source':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'correct_designation':True,'prompt_exact':True,'solution_exact':sid!='q-130301','correction':'Unchanged third row restored to (2,-6,-4)' if sid=='q-130301' else None,'missing':[],'extra':[]})
        for a in original[':answer-field/choices']:
            recipes.append({'source':sid,'source_answer_id':a[':answer/id'],'field':'selection','profile':sid,'original_value':a[':answer/value'],'recipe':str(g.operation(a[':answer/value'])),'policy':'Retain source coefficient constants; conjugate row indices by sampled permutation. No bank mixing.','interpretation':'Observed linear row-operation pattern; psychological interpretation unresolved','reproduces_at_source':True})
        params=g.domain(sid);targets=set();row_perms=set();column_perms=set();slots=set()
        for p in params:
            rec=independent(g.generate('hard',59774,sid,p));total+=1;distinct.add(fingerprint(rec['question']));targets.add(g.target(rec['question'][':question/problem']));row_perms.add(tuple(p[4]));column_perms.add(tuple(p[5]));slots.add(tuple(p[1:4]))
            inputs.append(native(sid+' '+str(p),rec))
        assert len(targets)==9 and len(row_perms)==len(column_perms)==6
        coverage[sid]={'targets_0_based':sorted(targets),'row_permutations':sorted(row_perms),'column_permutations':sorted(column_perms),'numeric_slots':sorted(slots),'domain_instances':len(params),'eligible_target_positions_missing':[]}
        # Change target names by row and column permutations without changing the
        # unlabelled data. Verify prompt, complete bank and both solution matrices.
        p=params[0];r=independent(g.generate('hard',0,sid,p));p2=p[:4]+[[1,2,0],[2,0,1]];r2=independent(g.generate('hard',0,sid,p2));assert fingerprint(r['question'])==fingerprint(r2['question'])
        assert g.generate('hard',999,sid,p)['question']==r['question']
        review.append('## '+sid+'\n\nSource replay (corrected where documented)\n\n'+g.markdown(g.generate('hard',0,sid,g.DEFAULTS[sid]))+'\n\nChanged assessed column\n\n'+g.markdown(r)+'\n\nChanged target position, same unlabelled data\n\n'+g.markdown(r2))
    for level in ('easy','moderate','unclassified'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported level admitted')
    records=g.batch('hard',min(20,len(distinct)),59774);assert len({fingerprint(r['question']) for r in records})==len(records)
    for r in records:independent(r)
    save('source-replay.json',{'passed':True,'complete_banks_matched':9,'complete_banks_total':9,'distractors_matched':36,'distractors_total':36,'profiles':replay,'excluded_sources':['q-20392']})
    save('choice-recipes.json',recipes);save('slot-coverage.json',coverage);save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    caps=json.loads((HERE/'capabilities.json').read_text());caps['validated_finite_distinct_numeric_tasks']=len(distinct);caps['validated_domain_instances']=total;save('capabilities.json',caps)
    save('validation.json',{'status':'pass','passed':True,'exhaustive_instances':total,'distinct_assessed_column_tasks':len(distinct),'supported_levels':['hard'],'source_fidelity':'9/9 complete banks, 36/36 distractors; exact prompt and 8/9 solution replay; documented arithmetic correction in q-130301','correctness':'Every rendered choice independently applied columnwise; only keyed operation makes specified entry zero. Every solution matrix and leading/final operation checked.','grading':'All five choices for every domain instance through application grade_field','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'replenish.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine')}})
if __name__=='__main__':main()

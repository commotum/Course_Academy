"""Exact source-bank replay, displayed-system oracle, exhaustive finite domain."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('two_coefficients',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def native(label,rec):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all field-owned answers through actual learner radio grader'} for a in f[':answer-field/choices']]}
def check(rec):
    q=rec['question'];meta=rec['generation'];sid=meta['bank_profile'];t=meta['parameters']['translation']
    a,c,b=g.vectors(q[':question/problem']);A=sp.ImmutableMatrix.hstack(a,c);aug=A.row_join(b)
    consistent=A.rank()==aug.rank();assert A.rank()==2
    solved=(A.T*A).inv()*A.T*b if consistent else None
    expected=str(sum(solved)) if consistent else 'No solution'
    f=q[':question/answer-fields'][0]
    assert q[':question/difficulty']==':question.difficulty/moderate' and len(q[':question/answer-fields'])==1
    assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5 and len({(o[':answer/type'],o[':answer/value']) for o in f[':answer-field/choices']})==5
    correct=[o[':answer/value'] for o in f[':answer-field/choices'] if o[':answer/id']==f[':answer-field/correct'][1]]
    assert correct==[expected] and sum(o[':answer/value']==expected for o in f[':answer-field/choices'])==1
    assert meta['correct_value']==expected and meta['consistent']==consistent
    assert meta['mathematical_fingerprint']==fingerprint(q) and rec['knowledge_point']['db_id']==g.KP_ID
    a0,c0,b0=g.vectors(g.CASES[sid][':question/problem']);assert a==a0 and c==c0 and b==b0+t*a+2*t*c
    # Independently solve the specified two rows and check its residual in all rows.
    plan=g.PLANS[sid]
    if plan[0]=='contradiction':
        assert t==0 and a[0]==c[0]==0 and b[0]!=0
    else:
        rows=(plan[2],plan[3]);pair=sp.Matrix([[a[i],c[i]] for i in rows]);rhs=sp.Matrix([b[i] for i in rows]);candidate=pair.inv()*rhs
        assert all(z.is_Integer for z in candidate) and list(map(str,candidate))==meta['candidate_coefficients']
        residual=A*candidate-b;assert all(residual[i]==0 for i in rows)
        assert (residual[plan[-1]]==0)==consistent
        if consistent:assert candidate==solved
        if plan[0]=='eliminate':
            _,elim,i,j,m,n,sub,checkrow=plan
            assert m*A[i,elim]+n*A[j,elim]==0 and m*A[i,1-elim]+n*A[j,1-elim]!=0
        else:assert A[plan[2],1-plan[1]]==0
        if t:
            # Check rendered supplied matrices and every numeric substitution equation
            # by independently evaluating the concrete coefficient products.
            text=q[':question/worked-solution'];ms=g.vectors(' '.join(m[0] for m in list(g.MATRIX.finditer(text))[:3]))
            assert ms[0:3]==[a,c,b]
            checkrow=plan[-1];lhs=(A*candidate)[checkrow]
            final=str(lhs)+' &='+str(b[checkrow]);assert final in text
            for index,value in enumerate(candidate):assert g.X[index]+'='+str(value) in text
            assert ('true statement.' in text)==consistent
            assert ('false statement.' in text)==(not consistent)
            if consistent:assert ')+('+str(candidate[1])+')='+expected+'.' in text
    # Whole record deterministic replay catches stale prompt/solution/answer parts.
    assert g.generate('moderate',meta['seed'],sid,meta['parameters'])==rec
    return rec
def fidelity(old,rec):
    check(rec);q=rec['question'];of=old[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
    assert q[':question/problem']==g.normalize_prose(old[':question/problem'])
    assert q[':question/worked-solution']==g.normalize_prose(old[':question/worked-solution'])
    oldbank=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in of[':answer-field/choices'])
    newbank=sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])
    assert oldbank==newbank
    assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
def main():
    inputs=[];replay=[];components=[];coverage={};review=[]
    for sid,old in sorted(g.CASES.items()):
        src=g.generate('moderate',0,sid,{'translation':0});fidelity(old,src)
        replay.append({'source':sid,'template':g.template_id(sid),'profile':sid,'matched_choices':5,'matched_distractors':4,'complete_bank':True,'correct_designation':True,'normalized_prompt_exact':True,'normalized_solution_exact':True,'missing':[],'extra':[]})
        a,c,b=g.vectors(old[':question/problem']);f=old[':question/answer-fields'][0]
        components.append({'source':sid,'db_id':old[':db/id'],'difficulty':'moderate','vectors':[list(map(str,v)) for v in (a,c,b)],'plan':g.PLANS[sid],'profile':sid,'fields':['selection:radio'],'choices':[{'source_answer_id':a[':answer/id'],'type':a[':answer/type'][':db/ident'],'source_value':a[':answer/value'],'recipe':'constant text No solution' if a[':answer/type'][':db/ident']==':answer.type/text' else '('+a[':answer/value']+')+3*t','source_value_reproduced':True,'interpretation':'observed value translation; mistake intent unresolved'} for a in f[':answer-field/choices']]})
        for t in g.domain(sid):
            rec=check(g.generate('moderate',0,sid,{'translation':t}));inputs.append(native(sid+' t='+str(t),rec))
            alt=g.generate('moderate',994,sid,{'translation':t});assert alt['question'][':question/id']==rec['question'][':question/id']
            if t==1:
                review.append('## '+sid+'\n\nSource replay\n\n'+g.markdown(src)+'\n\nChanged right-hand side\n\n'+g.markdown(rec))
                stale=copy.deepcopy(rec);stale['question'][':question/worked-solution']=src['question'][':question/worked-solution']
                try:check(stale)
                except AssertionError:pass
                else:raise AssertionError('Stale solution accepted')
        coverage[sid]={'declared_translation':list(g.domain(sid)),'sampled_translation':list(g.domain(sid)),'unsampled':[],'fixed_target':'x1+x2; both coefficients are the complete two-unknown response, changing operation changes skill','fixed_coefficients':'preserve source elimination signs, zero structure, row choices and workload','unchanged_branch':src['generation']['consistent']}
    for level in ('easy','hard','unclassified'):
        try:g.batch(level,1)
        except ValueError:pass
        else:raise AssertionError('Unsupported level admitted')
    for t in (-3,3,True,0.5):
        try:g.generate('moderate',0,'q-34054',{'translation':t})
        except ValueError:pass
        else:raise AssertionError('Invalid boundary accepted')
    records=g.catalog();fps={fingerprint(r['question']) for r in records};sourcefps={fingerprint(q) for q in g.CASES.values()}
    assert len(records)==len(fps)==46 and len(fps-sourcefps)==36
    try:g.batch('moderate',47)
    except ValueError:pass
    else:raise AssertionError('Finite limit ignored')
    save('source-replay.json',{'passed':True,'matched_banks':10,'total_banks':10,'matched_distractors':40,'total_distractors':40,'profiles':replay,'source_errors':[],'presentation':'captured source already normalized; source wording retained at t=0; variants explicitly render the same operative stages'})
    save('source-components.json',components);save('slot-coverage.json',coverage);save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    assert json.loads((HERE/'native-grading.json').read_text())['documented_unresolved_checks']==0
    save('previews.json',g.batch('moderate',5,119807));(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('capabilities.json',{'supported_levels':['moderate'],'unsupported_levels':['easy','hard'],'finite_distinct_tasks':46,'finite_new_variants':{'moderate':36},'finite_profile_limit':{'q-34242':1},'exceptions':[{'levels':['easy','hard'],'scope':'current source evidence and conservative same-method package','reason':'All ten complete practice questions are rated moderate. No source-backed easy/hard template exists. Relabeling or adding different operations to fill these bands is outside this package; reclassify when new evidence arrives.','shortage_each':5,'filled':False},{'profile':'q-34242','limit':1,'reason':'Immediate 0=nonzero contradiction has no new assessed arithmetic under the declared RHS translation. Other coordinates are irrelevant; do not count their changes as novelty.'}],'bounded_domain':'Nine source profiles allow integer translation t=-2..2; immediate contradiction has t=0 only. This finite workload policy is not a claim of global mathematical impossibility.'})
    save('validation.json',{'passed':True,'source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'exhaustive_profile_instances':46,'distinct_mathematical_tasks':46,'new_variants_excluding_sources':36,'complete_banks':'10/10','source_distractors':'40/40','fidelity':'normalized prompt and solution exact at source parameters; every complete bank and correct designation matched','correctness':'independent displayed-system rank and normal-equation solution, independent chosen-row solve and residual, source elimination coefficients, concrete rendered candidate references, deterministic complete-record replay','grading':'230 real engine radio checks; 46 accepted and 184 rejected','slot_coverage':'every allowed translation/profile; signed boundaries; original-only immediate contradiction; stale-solution negative control; target is fixed complete sum, not an eligible-position slot','plot_requirement':'none; column matrices are TeX, canonical SVG contains standalone MathJax notation','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',ROOT/'generate/runs/current/check-engine')}})
    print(json.dumps({'passed':True,'instances':46,'source_banks':'10/10','new_variants':36}))
if __name__=='__main__':main()

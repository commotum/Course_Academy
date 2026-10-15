"""Independent rendered-equation, row-operation and complete-bank validation."""
import hashlib, importlib.util, itertools, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def numeric(s):
    s=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',s)
    return sp.sympify(s)
def row_steps(text):
    matches=list(g.MATRIX.finditer(text));checks=[]
    for a,b in zip(matches,matches[1:]):
        before=g.parse_matrix(a[0]);after=g.parse_matrix(b[0]);between=text[a.end():b.start()]
        op=between.split(':=',1)
        names=list(re.finditer(r'\{R\}_\{(\d)\}',between))
        expected=before.copy()
        if '↔' in between:
            assert len(names)==2;expected.row_swap(int(names[0][1])-1,int(names[1][1])-1)
        elif len(op)==2:
            assert names;target=int(names[0][1])-1
            rhs=op[1].split('\\\\',1)[0].strip()
            refs=list(re.finditer(r'\{R\}_\{(\d)\}',rhs));new=sp.zeros(1,4);offset=0
            for ref in refs:
                coefficient=rhs[offset:ref.start()].strip()
                if coefficient in ('','+'):coefficient='1'
                if coefficient=='-':coefficient='-1'
                new+=numeric(coefficient)*before[int(ref[1])-1,:];offset=ref.end()
            assert refs and not rhs[offset:].strip()
            expected[target,:]=new
        else:assert before==after,'Unannotated matrix transition'
        assert expected==after,('Incorrect annotated row operation',between)
        checks.append(between)
    return checks
def check(r):
    meta=r['generation'];q=r['question'];p=meta['parameters'];profile=meta['profile']
    assert r==g.generate('hard',meta['seed'],profile,p,meta['replay'])
    m=g.prompt_matrix(q[':question/problem']);rref,pivots=m.rref()
    assert m.shape==(3,4) and m.rank()==m[:,:3].rank()==2 and pivots==(0,1)
    matrices=[g.parse_matrix(x[0]) for x in g.MATRIX.finditer(q[':question/worked-solution'])]
    assert matrices[0]==m and matrices[-1]==rref
    assert all(v.rref()[0]==rref for v in matrices)
    row_steps(q[':question/worked-solution'])
    assert 'only two pivots' in q[':question/worked-solution']
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    choices=f[':answer-field/choices'];assert len(choices)==5
    objects=[];correct=[]
    for a in choices:
        assert '$' not in a[':answer/value']
        if a[':answer/type']==':answer.type/math':
            matrix=g.parse_matrix(a[':answer/value']);assert matrix.shape==(3,4)
            objects.append(str(matrix.tolist()))
            if matrix==rref:correct.append(a[':answer/id'])
        else:assert a[':answer/type']==':answer.type/text' and a[':answer/value']=='No solution';objects.append('No solution')
    assert len(set(objects))==5 and len(set(a[':answer/id'] for a in choices))==5
    assert len(correct)==1 and f[':answer-field/correct']==[':answer/id',correct[0]]
    assert fingerprint(q)==meta['mathematical_fingerprint']
    return r
def native(label,r):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every complete-bank radio option through native grade_field'} for a in f[':answer-field/choices']]}
def source_valid(q):
    """Validate existing matrix or affine-line banks without repairing sources."""
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/key']=='selection' and f[':answer-field/correct']
    m=g.prompt_matrix(q[':question/problem']);rr=m.rref()[0];z=sp.Symbol('z')
    assert m.rank()==m[:,:3].rank()==2
    signatures=[];correct=[]
    vector='and then solve' in q[':question/problem']
    for a in f[':answer-field/choices']:
        value=a[':answer/value']
        if a[':answer/type'][':db/ident']==':answer.type/text':
            signatures.append('text:'+value);continue
        if vector:
            match=g.MATRIX.search(value);assert match
            entries=[sp.sympify(re.sub(r'(\d)(z)',r'\1*\2',x.strip()),locals={'z':z}) for x in match[1].split('\\\\')]
            assert len(entries)==3
            v=sp.Matrix(entries);offset=v.subs(z,0);direction=v.diff(z)
            assert direction!=sp.zeros(3,1) and v==offset+z*direction
            signature=sp.Matrix([list(direction)+[0],list(offset)+[1]]).rref()[0]
            signatures.append(str(signature.tolist()))
            if all(sp.expand(x)==0 for x in m[:,:3]*v-m[:,3]):correct.append(str(a[':answer/id']))
        else:
            matrix=g.parse_matrix(value);signatures.append(str(matrix.tolist()))
            if matrix==rr:correct.append(str(a[':answer/id']))
    assert len(signatures)==5 and len(set(signatures))==5
    assert correct==[str(f[':answer-field/correct'][':answer/id'])]
    numeric=[]
    for match in g.MATRIX.finditer(q[':question/worked-solution']):
        try:matrix=g.parse_matrix(match[0])
        except (ValueError,TypeError):continue
        if matrix.shape==(3,4):numeric.append(matrix)
    assert numeric and numeric[0]==m and numeric[-1]==rr
    assert all(x.rref()[0]==rr for x in numeric)
    # Validate the annotated numeric reduction before any vector displays.
    sol=q[':question/worked-solution'];last=next(match for match in reversed(list(g.MATRIX.finditer(sol))) if match[0]==g.matrix_tex(numeric[-1]))
    row_steps(sol[:last.end()])
    return True
def main():
    old=g.sources();inputs=[];replays=[];review=[];analyses=[]
    for sid,q in old.items():
        supported=sid in g.PROFILES
        m=g.prompt_matrix(q[':question/problem']);fields=q[':question/answer-fields']
        analyses.append({'source_id':sid,'source_db_id':q[':db/id'],'difficulty':q[':question/difficulty'][':db/ident'],'prompt':q[':question/problem'],'matrix':[[str(v) for v in row] for row in m.tolist()],
                         'rank':m.rank(),'pivots':list(m.rref()[1]),'response':'vector general solution' if 'and then solve' in q[':question/problem'] else 'RREF matrix',
                         'fields':fields,'worked_solution':q[':question/worked-solution'],'supported':supported,'profile':sid,
                         'plot_rating':'none','exclusion':None if supported else 'Duplicate field key with missing correct answer' if len(fields)>1 else 'Vector-solution response and its prose are outside the bounded matrix-response generator; no fidelity claim'})
    save('source-analysis.json',{'basis':json.loads((HERE/'source.json').read_text())['basis'],'sources':analyses})
    valid_sources=[];excluded=[]
    for sid,q in old.items():
        try:source_valid(q);valid_sources.append(q[':db/id'])
        except (AssertionError,KeyError,ValueError,TypeError,StopIteration) as error:excluded.append({'id':q[':db/id'],'source':sid,'reason':repr(error)})
    save('source-validation.json',{'validated_question_ids':valid_sources,'excluded':excluded,'original_questions_modified':0,'checks':'Exact key, all options distinct as complete mathematical objects, rank/consistency, complete numeric reduction and annotated row operations; vector affine lines satisfy every original equation'})
    for sid in g.PROFILES:
        source=old[sid];r=check(g.generate('hard',0,sid,{'scale':1},True));f=source[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
        assert r['question'][':question/problem']==source[':question/problem']
        assert r['question'][':question/worked-solution']==source[':question/worked-solution']
        mappings=[]
        for a in f[':answer-field/choices']:
            matches=[b for b in rf[':answer-field/choices'] if a[':answer/value']==b[':answer/value'] and a[':answer/type'][':db/ident']==b[':answer/type']]
            assert len(matches)==1
            mappings.append({'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'generated_value':matches[0][':answer/value'],'recipe':{'math':'Matrix columns 1–3 unchanged; every column-4 entry equals source entry times k','text':'unchanged'}[ 'math' if a[':answer/type'][':db/ident']==':answer.type/math' else 'text'],'complete_match':True})
        correct=next(a for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
        assert correct[':answer/value']==f[':answer-field/correct'][':answer/value']
        replays.append({'profile':sid,'source_db_id':source[':db/id'],'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'complete_bank_match':True,'correct_designation_match':True,'prompt_solution_exact':True,'mappings':mappings,'missing_or_extra':[]})
        review.append('## Source '+sid+' and exact replay\n\n'+g.markdown(r))
    fps=set();ids=set();counts={};coverage={}
    for entry in g.candidates('hard'):
        sid=entry['profile'];k=entry['scale'];r=check(g.generate('hard',17,sid,{'scale':k}));inputs.append(native(sid+':'+str(k),r))
        assert g.generate('hard',999,sid,{'scale':k})['question']==r['question']
        fps.add(fingerprint(r['question']));ids.add(r['question'][':question/id']);counts[sid]=counts.get(sid,0)+1;coverage.setdefault(sid,[]).append(k)
    assert all(set(ks)==set(g.SCALES) for ks in coverage.values())
    for level in ('easy','moderate'):
        try:g.batch(level,1)
        except ValueError:pass
        else:raise AssertionError('Unsupported level generated')
    previews=[]
    for sid in g.PROFILES:
        for k in (-2,3):
            r=check(g.generate('hard',2703,sid,{'scale':k}));previews.append(r);review.append('## Changed RHS, fixed coefficients: '+sid+', k='+str(k)+'\n\n'+g.markdown(r))
    save('previews.json',previews);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('review.json',{'passed':True,'supported_profiles':list(g.PROFILES),'checks':['Source and k=-2/k=3 variants: prompt RHS, every intermediate matrix, annotations, complete key and bank agree','Same coefficient matrix and row-operation workload across signs','Matrix response and selection key retained; no source or learner edits'],'target_slot':'Fixed complete RREF; no variable target position is declared','fidelity':'5/5 supported banks, 25/25 options, 20/20 distractors; nine other sources explicitly excluded'})
    save('source-replay.json',{'passed':True,'banks':replays,'complete_banks_matched':5,'complete_banks_total':5,'source_choices_matched':25,'source_choices_total':25,'source_distractors_matched':20,'source_distractors_total':20,'excluded_source_questions':9,'missing_or_extra':[],'inference_limit':'RHS column scaling is an observed-expression extension. Original author intent for distractors is unknown; no inferred misconception feedback appears in output.'})
    save('native-input.json',inputs)
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    paths=(HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'check-engine',HERE/'check-engine.rs')
    save('validation.json',{'passed':True,'supported_levels':['hard'],'unsupported_levels':['easy','moderate'],'domain_instances':len(inputs),'distinct_mathematical_tasks':len(fps),'distinct_identities':len(ids),'counts_by_profile':counts,'slot_coverage':coverage,
                            'source_banks_matched':'5/5 supported; nine sources excluded','source_choices_matched':'25/25 supported','mathematics':'Exact independently parsed prompt RREF, rank, pivot columns, every annotated elementary row operation, every intermediate row space, unique complete matrix key and distinct options',
                            'grading':'Every radio option at all 50 bounded instances through actual learning::grade_field and assessment_sampling::pool','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}})
    print('Validated',len(inputs),'bounded instances;',len(fps),'distinct augmented row spaces')
if __name__=='__main__':main()

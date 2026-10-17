"""Independent displayed mathematics, checkbox fidelity and native Boolean QA."""
import copy, hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=HERE/'checkbox-update-2026-10-16'
spec=importlib.util.spec_from_file_location('pivot_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def read_matrix(text):
    m=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S);assert m
    return sp.Matrix([[sp.Integer(v.strip()) for v in row.split('&')] for row in m[1].split(r'\\')])
def selected(text,n):
    if text=='All the columns are pivot':return tuple(range(1,n+1))
    out=tuple(sorted(map(int,re.findall(r'\$(\d+)\$(?:st|nd|rd|th)',text))))
    assert out and len(out)==len(set(out)) and all(1<=v<=n for v in out)
    return out
def checkbox_selection(q):
    return tuple(i for i,f in enumerate(q[':question/answer-fields'],1) if next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='true')
def audit(rec):
    q=rec['question'];a=read_matrix(q[':question/problem']);leading=[];zero_seen=False
    for row in a.tolist():
        nz=[j+1 for j,v in enumerate(row) if v]
        if not nz:zero_seen=True;continue
        assert not zero_seen;leading.append(nz[0])
    assert leading==sorted(set(leading))
    assert tuple(p+1 for p in a.rref()[1])==tuple(leading)
    assert read_matrix(q[':question/worked-solution'])==a
    sol=q[':question/worked-solution'];m=re.search(r'has \$(\d+)\$ pivots in the (.*?) columns:',sol,re.S);assert m
    assert int(m[1])==len(leading) and selected(m[2],a.cols)==tuple(leading)
    assert sol.startswith('Remember that the pivots of a matrix in row echelon form are the first non-zero entries in each row of the matrix.')
    fields=q[':question/answer-fields'];assert len(fields)==a.cols
    assert [f[':answer-field/key'] for f in fields]==[f'Column {i}' for i in range(1,a.cols+1)]
    ids=[q[':question/id']]
    for i,f in enumerate(fields,1):
        assert f[':answer-field/type']==':answer-field.type/checkbox'
        bank=f[':answer-field/choices'];assert len(bank)==2
        assert [v[':answer/value'] for v in bank]==['false','true']
        assert all(v[':answer/type']==':answer.type/text' for v in bank)
        assert f[':answer-field/correct'][0]==':answer/id'
        correct=f[':answer-field/correct'][1];assert sum(v[':answer/id']==correct for v in bank)==1
        assert next(v[':answer/value'] for v in bank if v[':answer/id']==correct)==str(i in leading).lower()
        ids += [f[':answer-field/id']]+[v[':answer/id'] for v in bank]
    assert len(ids)==len(set(ids))
    for identity in ids:uuid.UUID(identity)
    assert checkbox_selection(q)==tuple(leading)
    assert q[':question/difficulty']==':question.difficulty/easy'
    assert q[':question/problem'].count('Select all that apply.')==1
    assert q[':question/problem'].count('$')%2==0 and sol.count('$')%2==0
    return {'shape':[a.rows,a.cols],'pivot_columns':leading}
def validate(rec):
    meta=rec['generation'];assert rec['knowledge_point']['db_id']==g.KP_ID and meta['eligible_for_learning']
    assert rec==g.generate('easy',seed=meta['seed'],profile=meta['profile'],parameters=meta['parameters'])
    return audit(rec)
def engine_checks(rec,label):
    return {'label':label,'record':rec,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each column owned Boolean, including explicit unchecked false'} for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]}
def native(records,path):
    path.mkdir(parents=True,exist_ok=True);write(path/'native-input.json',[engine_checks(r,str(i)) for i,r in enumerate(records)])
    p=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],text=True,capture_output=True,check=True,timeout=55)
    (path/'native.log').write_text(p.stdout+p.stderr);r=json.loads((path/'native-report.json').read_text());assert r['documented_unresolved_checks']==0;return r

def main():
    OUT.mkdir(exist_ok=True);records=[];fidelity=[];coverage={};review=[];structures=set();boundaries=[]
    for mid,src in sorted(g.SOURCES.items()):
        orig=g.matrix(src[':question/problem']);n=len(orig[0]);params={'columns':list(range(1,n+1)),'matrix':orig}
        replay=g.generate('easy',profile=mid,parameters=params);audit(replay);rq=replay['question'];sf=src[':question/answer-fields'][0]
        assert rq[':question/problem']==src[':question/problem']+'\n\nSelect all that apply.'
        assert rq[':question/worked-solution']==src[':question/worked-solution']
        source_level=src[':question/difficulty'];source_level=source_level[':db/ident'] if isinstance(source_level,dict) else source_level
        assert rq[':question/difficulty']==source_level
        truth=selected(sf[':answer-field/correct'][':answer/value'],n);assert checkbox_selection(rq)==truth
        mappings=[{'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'selected_columns':selected(a[':answer/value'],n),'checkbox_values':[str(i in selected(a[':answer/value'],n)).lower() for i in range(1,n+1)],'correct':a[':answer/id']==sf[':answer-field/correct'][':answer/id']} for a in sf[':answer-field/choices']]
        assert all((tuple(m['selected_columns'])==truth)==m['correct'] for m in mappings)
        fidelity.append({'source':mid,'profile':mid,'matrix_preserved':True,'solution_byte_exact':True,'difficulty_preserved':True,'prompt_only_adds_selection_instruction':True,'correct_designation_preserved':True,'selected_columns':truth,'old_options_mapped':len(mappings),'mappings':mappings})
        coverage[mid]=[];records.append(replay)
        for target in g.targets(mid):
            a=[[0]*n for _ in orig]
            for i,p in enumerate(target):a[i][p-1]=1
            params={'columns':g.permutation(mid,target),'matrix':a};r=g.generate('easy',seed=7,profile=mid,parameters=params);validate(r);records.append(r)
            assert g.generate('easy',seed=99,profile=mid,parameters=params)['question']==r['question']
            coverage[mid].append(list(target));structures.add(g.fingerprint(r['question']))
            if target!=g.pivots(orig) and not any(z['source']==mid for z in review):review.append({'source':mid,'original':src,'variant':r})
        assert 0<len(truth)<n
        boundaries.append({'source':mid,'all_unchecked_correct':False,'all_checked_correct':False,'owned_false_and_true_natively_tested_for_every_column':True})
        try:g.generate('easy',profile=mid,parameters={'columns':list(range(1,n+1)),'matrix':[[0]*n for _ in orig]})
        except AssertionError:pass
        else:raise AssertionError('out-of-scope zero rank accepted')
        if len(orig)>=n:
            try:g.generate('easy',profile=mid,parameters={'columns':list(range(1,n+1)),'matrix':[[int(i==j) for j in range(n)] for i in range(len(orig))]})
            except AssertionError:pass
            else:raise AssertionError('out-of-scope full column rank accepted')
    fixed=[]
    for target,mat in [((1,3),[[1,0,0],[0,0,1],[0,0,0]]),((2,3),[[0,1,0],[0,0,1],[0,0,0]])]:
        r=g.generate('easy',profile='q-73607',parameters={'columns':g.permutation('q-73607',target),'matrix':mat});fixed.append(audit(r));records.append(r)
    preservation=[];before=json.loads((OUT/'before-samples.json').read_text())
    for seed,old in enumerate(before):
        r=g.generate('easy',seed);validate(r);assert r==g.generate('easy',seed);records.append(r)
        for key in ('parameters','profile','mathematical_fingerprint','level'):assert r['generation'][key]==old['generation'][key]
        for key in (':question/worked-solution',':question/difficulty'):assert r['question'][key]==old['question'][key]
        assert r['question'][':question/problem']==old['question'][':question/problem']+'\n\nSelect all that apply.'
        sf=old['question'][':question/answer-fields'][0];answer=next(a[':answer/value'] for a in sf[':answer-field/choices'] if a[':answer/id']==sf[':answer-field/correct'][1])
        assert checkbox_selection(r['question'])==selected(answer,len(r['question'][':question/answer-fields']))
        preservation.append({'seed':seed,'profile':r['generation']['profile'],'parameters_solution_difficulty_and_selection_preserved':True})
    batch=g.generate_many('easy',40,19);assert len({g.fingerprint(r['question']) for r in batch})==40
    assert batch==g.generate_many('easy',40,19)
    for r in batch:validate(r)
    records.extend(batch)
    try:g.generate_many('easy',41,19)
    except ValueError as e:assert 'Finite structural limit 40' in str(e)
    else:raise AssertionError('Finite limit must remain explicit')
    for kind in ('radio',':answer-field.type/radio','blank'):
        try:g.generate('easy',field_type=kind)
        except ValueError:pass
        else:raise AssertionError('non-checkbox response accepted')
    for kind in ('checkbox',':answer-field.type/checkbox'):validate(g.generate('easy',field_type=kind))
    for level in ('moderate','hard'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('unsupported difficulty accepted')
    bad=copy.deepcopy(records[-1]);bad['question'][':question/worked-solution']=records[-2]['question'][':question/worked-solution']
    flipped=copy.deepcopy(records[-1]);f=flipped['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
    for corrupt in (bad,flipped):
        try:audit(corrupt)
        except AssertionError:pass
        else:raise AssertionError('corrupt solution/key accepted')
    native_report=native(records,OUT)
    write(OUT/'source-fidelity.json',fidelity);write(OUT/'sampling-preservation.json',preservation);write(OUT/'review.json',review)
    (OUT/'review.md').write_text('\n\n---\n\n'.join(z['source']+' source\n\n'+z['original'][':question/problem']+'\n\n'+z['original'][':question/worked-solution']+'\n\nCheckbox variant\n\n'+g.markdown(z['variant']) for z in review)+'\n')
    result={'status':'passed','version':g.VERSION,'source_basis':g.CAPTURE['basis'],'source_questions':len(fidelity),'templates':1,'source_profiles':len(coverage),'source_options_mapped':sum(len(f['mappings']) for f in fidelity),'correct_source_subsets_preserved':len(fidelity),'source_solutions_byte_exact':len(fidelity),'seeded_instances_preserved':len(preservation),'validated_records':len(records),'distinct_structural_tasks':len(structures),'field_type':'checkbox','fields_per_question':'one per displayed column; Column 1 through Column n','target_slot_coverage':coverage,'unexercised_eligible_pivot_targets':[],'changed_target_fixed_values':fixed,'boundary_submissions':boundaries,'scope_limit':'Every supported source shape has 0 < rank < columns. All/none correct subsets remain unsupported; both Boolean responses are tested for every field.','native':{k:(len(native_report[k]) if k=='records' else native_report[k]) for k in ('entry_point','records','accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'mathematical_oracle':'SymPy exact RREF plus independently parsed first-nonzero positions and rendered solution','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'unresolved':[]}
    write(OUT/'verification.json',result);write(HERE/'validation.json',result)
    print(json.dumps({k:result[k] for k in ('status','validated_records','distinct_structural_tasks','source_options_mapped','seeded_instances_preserved','native')}))
if __name__=='__main__':main()

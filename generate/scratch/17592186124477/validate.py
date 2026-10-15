"""Independent rendered-matrix, solution, bank, source fidelity and grader checks."""
import hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('pivot_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def write(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def read_matrix(text):
    match=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S);assert match
    a=sp.Matrix([[sp.Integer(v.strip()) for v in row.split('&')] for row in match[1].split(r'\\')])
    return a
def selected(text,n):
    if text=='All the columns are pivot':return tuple(range(1,n+1))
    out=tuple(sorted(map(int,re.findall(r'\$(\d+)\$(?:st|nd|rd|th)',text))))
    assert out and len(out)==len(set(out)) and all(1<=v<=n for v in out)
    return out
def audit(rec):
    q=rec['question'];a=read_matrix(q[':question/problem']);leading=[];zero_seen=False
    for row in a.tolist():
        nz=[j+1 for j,v in enumerate(row) if v]
        if not nz:zero_seen=True;continue
        assert not zero_seen;leading.append(nz[0])
    assert leading==sorted(set(leading))
    # RREF's pivot set is an independent exact elimination oracle.
    assert tuple(p+1 for p in a.rref()[1])==tuple(leading)
    assert read_matrix(q[':question/worked-solution'])==a
    sol=q[':question/worked-solution'];m=re.search(r'has \$(\d+)\$ pivots in the (.*?) columns:',sol,re.S);assert m
    assert int(m[1])==len(leading) and selected(m[2],a.cols)==tuple(leading)
    assert sol.startswith('Remember that the pivots of a matrix in row echelon form are the first non-zero entries in each row of the matrix.')
    f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];assert len(bank)==5
    values=[selected(v[':answer/value'],a.cols) for v in bank];assert len(set(values))==5
    correct=f[':answer-field/correct'][1];assert sum(v[':answer/id']==correct for v in bank)==1
    for v,value in zip(bank,values):assert (value==tuple(leading))==(v[':answer/id']==correct)
    assert q[':question/difficulty']==':question.difficulty/easy' and f[':answer-field/type']==':answer-field.type/radio'
    assert f[':answer-field/key']=='selection' and all(v[':answer/type']==':answer.type/text' for v in bank)
    assert q[':question/problem'].count('$')%2==0 and sol.count('$')%2==0
    return {'shape':[a.rows,a.cols],'pivot_columns':leading}

def validate(rec):
    meta=rec['generation'];assert rec['knowledge_point']['db_id']==g.KP_ID and meta['eligible_for_learning']
    replay=g.generate('easy',seed=meta['seed'],profile=meta['profile'],parameters=meta['parameters'])
    assert rec==replay;return audit(rec)

def engine_checks(rec,label):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'full owned choice bank'} for a in f[':answer-field/choices']]}
def native(records,path):
    path.mkdir(parents=True,exist_ok=True);write(path/'native-input.json',[engine_checks(r,str(i)) for i,r in enumerate(records)])
    p=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],text=True,capture_output=True,check=True,timeout=55)
    (path/'native.log').write_text(p.stdout+p.stderr);r=json.loads((path/'native-report.json').read_text());assert r['documented_unresolved_checks']==0;return r

def main():
    records=[];fidelity=[];components=[];coverage={};review=[];structures=set()
    for mid,src in sorted(g.SOURCES.items()):
        orig=g.matrix(src[':question/problem']);n=len(orig[0]);params={'columns':list(range(1,n+1)),'matrix':orig}
        replay=g.generate('easy',profile=mid,parameters=params);audit(replay);sq=src;rq=replay['question'];sf=sq[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
        assert rq[':question/problem']==sq[':question/problem'] and rq[':question/worked-solution']==sq[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        rc=next(a for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert rc[':answer/value']==sf[':answer-field/correct'][':answer/value']
        fidelity.append({'source':mid,'profile':mid,'matched_distractors':4,'total_distractors':4,'complete_bank':True,'correct_designation':True,'prompt_solution_byte_exact':True,'missing_options':[],'extra_options':[]})
        components.append({'source':mid,'matrix':orig,'pivots':g.pivots(orig),'shape':[len(orig),n],'profile':mid,'choices':[{'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'recipe':{'operation':'column-index bijection applied to entire observed subset','subset':selected(a[':answer/value'],n)},'misconception':'unresolved; retain observed subset pattern','correct':a[':answer/id']==sf[':answer-field/correct'][':answer/id']} for a in sf[':answer-field/choices']]})
        coverage[mid]=[];records.append(replay)
        # Every eligible pivot location for every observed profile, with values
        # fixed at one: catches stale targets independently of coefficient noise.
        for target in g.targets(mid):
            perm=g.permutation(mid,target);a=[[0]*n for _ in orig]
            for i,p in enumerate(target):a[i][p-1]=1
            params={'columns':perm,'matrix':a};r=g.generate('easy',seed=7,profile=mid,parameters=params);audit(r);validate(r);records.append(r)
            assert g.generate('easy',seed=99,profile=mid,parameters=params)['question']==r['question']
            coverage[mid].append(list(target));structures.add(g.fingerprint(r['question']))
            if target!=g.pivots(orig) and not any(z['source']==mid for z in review):review.append({'source':mid,'original':src,'variant':r})
    # A stronger changed-target probe keeps the complete numerical data fixed:
    # swap the first two columns of the same identity-like REF matrix.
    a=[[1,0,0],[0,0,1],[0,0,0]];b=[[0,1,0],[0,0,1],[0,0,0]]
    fixed_values=[]
    for target,mat in [((1,3),a),((2,3),b)]:
        r=g.generate('easy',profile='q-73607',parameters={'columns':g.permutation('q-73607',target),'matrix':mat});fixed_values.append(audit(r));records.append(r)
    # Deterministic normal sampling and boundary signs/zero trailing cells.
    for seed in range(200):
        r=g.generate('easy',seed);validate(r);assert r==g.generate('easy',seed);records.append(r)
    batch=g.generate_many('easy',40,19);assert len({g.fingerprint(r['question']) for r in batch})==40
    assert batch==g.generate_many('easy',40,19)
    for r in batch:validate(r)
    records.extend(batch)
    try:g.generate_many('easy',41,19)
    except ValueError as e:assert 'Finite structural limit 40' in str(e)
    else:raise AssertionError('Finite limit must remain explicit')
    # Negative tests prove the independent audit catches stale rendered keys.
    import copy
    bad=copy.deepcopy(records[-1]);bad['question'][':question/worked-solution']=records[-2]['question'][':question/worked-solution']
    try:audit(bad)
    except AssertionError:pass
    else:raise AssertionError('Stale solution was accepted')
    native_report=native(records,HERE/'reference/validation')
    write(HERE/'source-components.json',components);write(HERE/'source-fidelity.json',fidelity);write(HERE/'review.json',review)
    (HERE/'review.md').write_text('\n\n---\n\n'.join(z['source']+' source\n\n'+z['original'][':question/problem']+'\n\n'+z['original'][':question/worked-solution']+'\n\nVariant\n\n'+g.markdown(z['variant']) for z in review))
    capabilities={'supported_levels':['easy'],'unsupported_levels':{l:{'status':'unsupported','bounded_reason':'All 13 observed practice records are easy. Reading supplied REF pivots requires no elimination. Difficulty escalation would require new operations or a new instructional template; neither is supported by the captured evidence.','source_basis':g.CAPTURE['basis'],'reopen_when':'New rated source evidence establishes a comparable same-method band.'} for l in ('moderate','hard')},'structural_variant_limit':len(structures),'counting_rule':'distinct (row count, column count, ordered pivot columns); ignore coefficients, label, seed and choice bank','finite_limit_scope':'observed dimensions/ranks; no claim that the mathematical skill has a global finite domain'}
    write(HERE/'capabilities.json',capabilities)
    result={'status':'passed','source_basis':g.CAPTURE['basis'],'source_questions':13,'templates':1,'complete_bank_profiles':13,'matched_source_distractors':52,'total_source_distractors':52,'complete_source_banks':13,'missing_options':[],'extra_options':[],'validated_records':len(records),'distinct_structural_tasks':len(structures),'target_slot_coverage':coverage,'unexercised_eligible_pivot_targets':[],'changed_target_fixed_values':fixed_values,'native':native_report,'plots':'none; source practice and canonical images are standalone LaTeX matrix typesetting','mathematical_oracle':'SymPy exact RREF plus independently parsed first-nonzero positions and rendered solution','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()}
    write(HERE/'validation.json',result);print(json.dumps({k:result[k] for k in ('status','validated_records','distinct_structural_tasks','matched_source_distractors')}))
if __name__=='__main__':main()

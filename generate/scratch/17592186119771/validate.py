"""Historical v2 validation, retained with its original policy assertions.

Do not use this main entry point for the current v3 generator. The current
validator is dense-update-2026-10-17/validate.py. Shared readback/normalization
helpers below remain useful to it; frozen v2 evidence is not rewritten.

Runs under the existing project .venv. Never touches EDB or shared files.
"""
import copy, hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def write(name,value): (D/name).write_text(json.dumps(value,indent=2)+'\n')

def read(text):
    m=re.search(r'([AC])\s*=\s*\[?\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\2\}',text,re.S)
    assert m,'Missing displayed matrix'
    matrix=[[int(v.strip()) for v in row.split('&')] for row in m[3].split(r'\\')]
    assert len(matrix) in (2,3,4) and all(len(row)==len(matrix) for row in matrix)
    return matrix,m[1],m[2]

def expected(matrix):
    n=len(matrix)
    above=all(matrix[i][j]==0 for i in range(n) for j in range(i+1,n))
    below=all(matrix[i][j]==0 for i in range(n) for j in range(i))
    identity=all(matrix[i][j]==int(i==j) for i in range(n) for j in range(n))
    return 'Identity matrix' if identity else 'Diagonal matrix' if above and below else 'Lower triangular matrix' if above else 'Upper triangular matrix' if below else 'Other'

def balanced(text):
    assert text.count('$')%2==0
    depth=0
    for c in text:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert r'\\begin' not in text and r'\\end' not in text
    assert '{{' not in text and '--' not in text and '+-' not in text

def structural(rec,raw=False):
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=rec['question'];meta=rec['generation'];matrix,letter,layout=read(q[':question/problem']);n=len(matrix);answer=expected(matrix)
    assert answer in g.FAMILIES.values()
    assert meta['parameters']=={'matrix':matrix,'letter':letter,'layout':layout}
    assert meta['parameter_fingerprint']==g.task_key(matrix)
    assert meta['evidence_only']==raw and meta['eligible_for_learning']==(not raw)
    if not raw:
        level=q[':question/difficulty'].split('/')[-1]
        assert (level=='easy' and n in (2,3) and answer in ('Upper triangular matrix','Lower triangular matrix')) or (level=='moderate' and n==3 and answer=='Diagonal matrix') or (level=='hard' and n==4)
        assert g.CRITERION in q[':question/problem']
        assert len(q[':question/answer-fields'])==1
    balanced(q[':question/problem']);uuid.UUID(q[':question/id'])
    fields=q[':question/answer-fields'];all_ids=[]
    for f in fields:
        assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
        uuid.UUID(f[':answer-field/id']);values=[a[':answer/value'] for a in f[':answer-field/choices']]
        assert sorted(values)==sorted(g.LABELS) and len(values)==5
        ids=[a[':answer/id'] for a in f[':answer-field/choices']];all_ids+=ids
        assert len(set(ids))==5
        for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/text'
        if ':answer-field/correct' in f:
            assert f[':answer-field/correct'][0]==':answer/id'
            assert f[':answer-field/correct'][1] in ids
            assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==answer
        else: assert raw
    assert len(set(all_ids))==len(all_ids),'Answer identities must be field-owned'
    if ':question/worked-solution' not in q: assert raw; return answer
    sol=q[':question/worked-solution'];balanced(sol)
    assert read(sol)==(matrix,letter,layout),'Repeated complete matrix differs'
    region='above and below' if answer=='Diagonal matrix' else 'above' if answer=='Lower triangular matrix' else 'below'
    opening=f"Notice that ${letter}$ is a matrix for which all entries {region} the diagonal are $0$'s:"
    assert sol.startswith(opening+'\n\n')
    nzero_region=[matrix[i][j] for i in range(n) for j in range(n) if i!=j and (answer=='Diagonal matrix' or (i<j if answer=='Lower triangular matrix' else i>j))]
    assert all(v==0 for v in nzero_region)
    therefore=f'Therefore, it is {"an" if answer=="Upper triangular matrix" else "a"} {answer.lower()}.'
    assert sol.count('Therefore, it is')==1 and therefore in sol
    if answer=='Diagonal matrix': assert sol.endswith(therefore)
    else:
        w=re.search(r'\$\{([ac])\}_\{(\d)(\d)\}=(-?\d+)\\ne 0\.\$',sol);assert w,'Concrete witness missing'
        i,j=int(w[2])-1,int(w[3])-1;value=int(w[4]);assert 0<=i<n and 0<=j<n
        assert w[1]==letter.lower() and matrix[i][j]==value!=0
        assert (i>j if answer=='Lower triangular matrix' else i<j)
        cells=[(a,b) for a in range(n) for b in range(n) if matrix[a][b] and (a>b if answer=='Lower triangular matrix' else a<b)]
        assert (i,j)==cells[0],'Source first witness recipe must generalize'
        opposite='upper' if answer=='Lower triangular matrix' else 'lower';side='below' if answer=='Lower triangular matrix' else 'above'
        text=f'It is not {"an" if opposite=="upper" else "a"} {opposite} triangular matrix or a diagonal matrix since there is a non-zero element {side} the diagonal:'
        assert text in sol and sol.endswith(w[0])
    return answer

def normalize_source_question(q):
    out=copy.deepcopy(q)
    if ':question/difficulty' in out:out[':question/difficulty']=g.enum(out[':question/difficulty'])
    out.pop(':question/id')
    for f in out[':question/answer-fields']:
        f.pop(':answer-field/id');f[':answer-field/type']=g.enum(f[':answer-field/type'])
        if ':answer-field/correct' in f: f[':answer-field/correct']=f[':answer-field/correct'][':answer/value']
        for a in f[':answer-field/choices']:a.pop(':answer/id');a[':answer/type']=g.enum(a[':answer/type'])
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return out

def normalize_replay(q):
    out=copy.deepcopy(q);out.pop(':question/id')
    for f in out[':question/answer-fields']:
        f.pop(':answer-field/id')
        if ':answer-field/correct' in f:f[':answer-field/correct']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        for a in f[':answer-field/choices']:a.pop(':answer/id')
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return out

def checks(rec):
    result=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        assert ':answer-field/correct' in f
        for a in f[':answer-field/choices']:
            result.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete observed five-category radio bank / owned lookup ref'})
    return result

def mutation_rejected(rec,mutator):
    mutated=copy.deepcopy(rec);mutator(mutated)
    try:structural(mutated)
    except (AssertionError,ValueError,IndexError):return True
    raise AssertionError('Structural mutation accepted')

def main():
    assert g.SOURCE==json.loads((ROOT/'generate/runs/current/sources/17592186119771.json').read_text())
    native=[];review=[];cases=[];ledger=[];rawreplays=[];positions=set();coverage={};layout_coverage=set();total=0
    widgets=json.loads(Path('/home/jake/Developer/MA/DATA/Lessons/1777/Source/1777.json').read_text())
    widget=next(it for it in widgets['lesson']['items'] if it.get('question_id')=='13759')
    assert widget['question_format']=='multiple-choice' and widget['choice_count']==5
    assert sorted(c['readable_text'].strip() for c in widget['choices'])==sorted(g.LABELS)
    write('authoritative-widget.json',widget)
    for sid,q in g.SOURCES.items():
        matrix,letter,layout=read(q[':question/problem']);p={'matrix':matrix,'letter':letter,'layout':layout};kind=g.family(matrix);level=g.source_levels(sid)
        case={'source_id':sid,'template':kind,'level':level,'parameters':p,'bank_profile':'raw:'+sid};cases.append(case)
        rec=g.generate(level,parameters=p,template=kind,profile='raw:'+sid,field_type='radio');structural(rec,True)
        assert normalize_replay(rec['question'])==normalize_source_question(q),'All original keys, banks, ratings and prose must replay'
        assert (':question/difficulty' in q)==(':question/difficulty' in rec['question'])
        assert (':question/worked-solution' in q)==(':question/worked-solution' in rec['question'])
        rawreplays.append(rec);review.append({'label':'Original raw replay '+sid,'record':rec})
        for f in q[':question/answer-fields']:
            ledger.append({'source_id':sid,'source_field':f[':answer-field/id'],'field_key_present':':answer-field/key' in f,'correct_present':':answer-field/correct' in f,'complete_bank_match':True,'values_matched':5,'correct_designation_match':':answer-field/correct' in f,'correct_inferred_for_normal_only':':answer-field/correct' not in f,'choices':[{'original_answer_id':a[':answer/id'],'value':a[':answer/value'],'type':g.enum(a[':answer/type']),'recipe':'fixed category '+a[':answer/value'],'profile':'raw:'+sid,'recorded_correct':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') if ':answer-field/correct' in f else None} for a in f[':answer-field/choices']]})
        # Native fixture projection only of source fields with recorded correct refs.
        keyed=copy.deepcopy(rec);keyed['question'][':question/answer-fields']=[f for f in keyed['question'][':question/answer-fields'] if ':answer-field/correct' in f]
        if keyed['question'][':question/answer-fields']:native.append({'label':'raw keyed source fixture '+sid,'record':keyed,'checks':checks(keyed)})
        normal=g.generate(level,parameters=p,template=kind,profile='source:'+sid);structural(normal)
        assert normal['question'][':question/problem']==q[':question/problem']+'\n\n'+g.CRITERION
        if ':question/worked-solution' in q:assert normal['question'][':question/worked-solution']==q[':question/worked-solution']
        native.append({'label':'completed normal source '+sid,'record':normal,'checks':checks(normal)})
        # Parameterized public raw replay, including first witness moving to another cell.
        varied=[row[:] for row in matrix]
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if varied[i][j]:varied[i][j]=-2 if varied[i][j]>0 else 2
        if kind!='diagonal' and len(matrix)==3:
            for i in range(3):
                for j in range(3):
                    if i!=j:varied[i][j]=0
            i,j=(2,0) if kind=='lower' else (1,2);varied[i][j]=-7
        changed=g.generate(level,parameters={**p,'matrix':varied},template=kind,profile='raw:'+sid);structural(changed,True)
        assert changed['question'][':question/problem']!=rec['question'][':question/problem']
        assert set(changed['question'])==set(rec['question'])
        generated=g.generate(level,parameters={**p,'matrix':varied},template=kind,profile='source:'+sid);structural(generated)
        review.append({'label':'Generated changed-mask source-family variant '+sid,'record':generated})
    for level in g.SUPPORTED_LEVELS:
        cat=g.catalog(level);seen=set()
        for index,(kind,pattern) in enumerate(cat):
            m=[list(row) for row in pattern]
            rec=g.generate(level,index,template=kind,parameters={'matrix':m,'letter':'C' if index%2 else 'A','layout':'aligned'});structural(rec)
            fp=rec['generation']['parameter_fingerprint'];assert fp not in seen;seen.add(fp)
            native.append({'label':'full meaningful catalog '+level+'/'+str(index),'record':rec,'checks':checks(rec)})
        assert len(seen)==len(cat)
        for seed in range(200):
            rec=g.generate(level,seed);structural(rec);meta=rec['generation'];total+=1
            replay=g.generate(level,seed,template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile']);assert replay==rec
            alternate=g.generate(level,seed+997,template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile']);assert alternate['question'][':question/id']==rec['question'][':question/id']
            coverage[level+'/'+meta['template']]=coverage.get(level+'/'+meta['template'],0)+1
            layout_coverage.add((level,meta['template'],len(meta['parameters']['matrix']),meta['parameters']['layout']))
            f=rec['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
        for rec in g.batch(level,min(4,len(cat)),42):review.append({'label':'Generated '+level+' default variant','record':rec})
        if level=='hard':
            for kind in g.FAMILIES:
                for seed in (91,193):review.append({'label':'Generated authored hard '+kind+' variant','record':g.generate_hard(seed,template=kind)})
        assert len({r['generation']['parameter_fingerprint'] for r in g.batch(level,len(cat),100)})==len(cat)
    assert ('easy','lower',3,'bmatrix') in layout_coverage
    assert positions==set(range(5));assert set(coverage)=={'easy/lower','easy/upper','moderate/diagonal','hard/lower','hard/upper','hard/diagonal'}
    # Conditional fingerprints distinguish substantive support/unit masks only.
    assert g.task_key([[1,0],[2,3]])==g.task_key([[0,0],[-9,1]])
    assert g.task_key([[1,0,0],[0,2,0],[0,0,0]])==g.task_key([[1,0,0],[0,-4,0],[0,0,7]])
    assert g.task_key([[1,0,0],[0,2,0],[0,0,0]])!=g.task_key([[2,0,0],[0,1,0],[0,0,0]])
    assert g.task_key([[1,0,0],[2,1,0],[0,0,1]])!=g.task_key([[1,0,0],[0,1,0],[0,2,1]])
    invalid=[('easy',{'matrix':[[1,0],[0,1]],'letter':'A','layout':'aligned'}),('easy',{'matrix':[[1,2],[3,4]],'letter':'A','layout':'aligned'}),('moderate',{'matrix':[[1,0],[0,2]],'letter':'A','layout':'aligned'}),('hard',{'matrix':[[1,0,0],[2,1,0],[0,0,1]],'letter':'A','layout':'aligned'}),('easy',{'matrix':[[10,0],[1,1]],'letter':'A','layout':'aligned'}),('easy',{'matrix':[[True,0],[1,1]],'letter':'A','layout':'aligned'})]
    invalid_calls=[{'level':'easy','field_type':'checkbox'},{'level':'easy','profile':'absent'},{'level':'easy','profile':False},{'level':'easy','template':'diagonal'},{'level':'easy','parameters':{'matrix':[[1,0],[2,3]],'letter':'B','layout':'aligned'}},{'level':'easy','profile':'raw:q-13759'},{'level':'moderate','profile':'raw:q-13759','parameters':{'matrix':[[1,0,0],[2,3,0],[4,5,6]],'letter':'A','layout':'aligned'}}]
    for args in invalid_calls:
        try:g.generate(**args)
        except ValueError:pass
        else:raise AssertionError('Invalid profile/shape call accepted')
    for level,p in invalid:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Invalid level/domain input accepted')
    base=g.generate('easy',parameters={'matrix':[[2,0,0],[0,1,0],[-7,0,0]],'letter':'C','layout':'aligned'})
    mutations=[lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('entries above','entries below')),lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('{31}=-7','{21}=-7')),lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('-7 & 0 & 0','-8 & 0 & 0')),lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].split('\n\nIt is not')[0]),lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'][0].__setitem__(':answer/value','Invented category'),lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',str(uuid.uuid4())]),lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('-7 & 0 & 0','0 & 0 & 0'))]
    for fn in mutations:mutation_rejected(base,fn)
    write('source-cases.json',cases);write('source-replay.json',rawreplays);write('choice-ledger.json',ledger);write('review.json',review)
    (D/'review.md').write_text('\n\n---\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
    write('engine-input.json',native);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'native-grading.json')],check=True)
    engine=json.loads((D/'native-grading.json').read_text());assert engine['documented_unresolved_checks']==0
    sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    result={'status':'pass','database':'math','basis':1356,'lineage':g.SOURCE['lineage'],'python_version':sys.version.split()[0],'sympy_version':g.sp.__version__,
        'source_questions':10,'source_full_raw_replays':10,'source_prompt_exact':10,'source_solutions_exact':9,'source_solutions_present':9,'raw_key_presence_parity':10,
        'complete_source_banks_matched':11,'source_choice_values_matched':55,'source_correct_designations_matched':9,'source_correct_designations_present':9,'source_missing_correct_designations':2,
        'normal_source_complete_banks':10,'normal_source_solutions_exact':9,'normal_source_solutions_authored':1,'normal_source_duplicate_field_repairs':1,'normal_source_inferred_keys':1,'normal_source_prompt_criterion_additions':10,
        'meaningful_catalog_counts':{l:len(g.catalog(l)) for l in g.SUPPORTED_LEVELS},'full_catalog_patterns_verified':164,'sampled_normal_records_verified':total,'default_family_coverage':coverage,'default_layout_coverage':[list(x) for x in sorted(layout_coverage)],'structural_mutations_rejected':len(mutations),'native_records':len(native),
        'native_grading':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','entry_point')},
        'hashes':{'generator':sha(D.with_suffix('.py')),'validator':sha(__file__),'source':sha(D/'source.json'),'grader_binary':sha(ROOT/'generate/runs/current/check-engine'),'grader_source':sha(ROOT/'generate/runs/current/check-engine.rs')},
        'limitations':['Raw q-13759 preserves both captured selection fields; original MA widget confirms one radio. Normal q-13759 supplies one field.', 'Raw q-13769 omits original missing rating, solution and correct ref; normal supplies authored easy assignment, solution and independently verified lower-triangular key.', 'Two raw source fields have no correct ref and cannot be native graded without fabricating captured evidence; only the nine originally keyed fields are graded in source fixtures. All completed normal source banks grade.', 'Hard 4x4 is an authored same-method workload extension, not an observed MA difficulty.', 'Finite meaningful banks: 16 easy / 7 moderate / 141 hard. Numeric changes increase presentation variety only.']}
    write('validation.json',result);write('capabilities.json',{'levels':list(g.SUPPORTED_LEVELS),'field_types':['radio'],'profiles':['five-labels']+['raw:'+s for s in g.SOURCES]+['source:'+s for s in g.SOURCES],'meaningful_catalog_counts':result['meaningful_catalog_counts'],'source_basis':1356})
    print(json.dumps({k:result[k] for k in ('status','meaningful_catalog_counts','source_full_raw_replays','source_choice_values_matched','native_records','native_grading')}))
if __name__=='__main__':main()

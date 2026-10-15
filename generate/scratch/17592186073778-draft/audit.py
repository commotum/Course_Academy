"""Additional immutable-boundary, provenance, held-slot and signed-domain checks."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('private_validation',D/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(D/name).write_text(json.dumps(obj,indent=2)+'\n')
def registered():
    r=ROOT/'generate/scratch';kp='17592186073778'
    paths=[r/(kp+'.py'),*sorted((r/kp).rglob('*')),*sorted((r/'__pycache__').glob(kp+'.*.pyc'))]
    return {'files':{str(p.relative_to(ROOT)):sha(p) for p in paths if p.is_file()},'pathset':[str(p.relative_to(ROOT)) for p in paths]}
def main():
    baseline=json.loads((D/'registered-baseline.json').read_text());assert registered()==baseline
    wrappers={}
    for name,folder,id in [('source','sources','17592186073778'),('topic','topics','17592186050240'),('lesson','lessons','17592186050240')]:
        p=ROOT/'generate/runs/current'/folder/(id+'.json');assert (D/(name+'.json')).read_bytes()==p.read_bytes();wrappers[name]=sha(p)
        c=json.loads(p.read_text());assert {k:c[k] for k in g.SOURCE}==g.SOURCE
    source=json.loads((D/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];cases=json.loads((D/'source-cases.json').read_text())
    assert len(qs)==2 and all(':question/math-academy-id' in q for q in qs)
    assert {q[':question/math-academy-id'] for q in qs}=={c['source_id'] for c in cases}
    inv=json.loads((D/'independent-inventory.json').read_text());assert inv['questions']==[] and {k:inv[k] for k in g.SOURCE}==g.SOURCE
    m=json.loads((D/'reference/grader-build.json').read_text());files={m['source']:m['source_sha256'],m['library']:m['library_sha256'],m['binary']:m['binary_sha256'],**m['engine_sources'],**m['dependencies']};assert len(files)==42
    assert all(sha(ROOT/p)==h for p,h in files.items());assert m['binary_sha256']=='33510bf3ac27a1eb28e9bad7b4121a22d2fa787026d3102268daa4ecf98b1617'
    save('reference/grader-provenance-check.json',{'verified':42,'all_match':True,'files':files})
    counts={};native=[];held=[];records=[]
    for level,base in [('easy',dict(a=6,b=1,c=8,r=4)),('moderate',dict(a=1,b=4,c=4,r=4)),('hard',dict(a=1,b=6,c=5,r=4))]:
        count=0
        for signs in itertools.product([-1,1],repeat=4):
            p={k:val*s for (k,val),s in zip(base.items(),signs)}
            for template in g.TEMPLATES:
                rec=g.generate(level,seed=count,template=template,parameters=p);v.check(rec);records.append(rec);count+=1
                # C0 is checked on all learner strings, including each displayed choice.
                stack=[rec['question']]
                while stack:
                    z=stack.pop()
                    if isinstance(z,dict):stack.extend(z.values())
                    elif isinstance(z,list):stack.extend(z)
                    elif isinstance(z,str):assert all(ord(c)>=32 or c in '\n\t' for c in z)
            if signs in [(-1,-1,-1,-1),(1,1,1,1)]:native.append(v.native(rec,'signed boundary '+level+str(signs)))
        counts[level]=count
        basefp=None;ids=set()
        for var in ['x','t','u']:
            for multiplier in ['-4','-2','2','4']:
                p={**base,'variable':var,'r':multiplier};rec=g.generate(level,template='blank_coordinate',parameters=p);v.check(rec)
                fp=rec['generation']['parameter_fingerprint'];basefp=basefp or fp;assert fp==basefp
                assert rec['question'][':question/id']==g.generate(level,seed=987,template='blank_coordinate',parameters=p)['question'][':question/id']
                ids.add(rec['question'][':question/id']);held.append(rec)
        assert len(ids)==12
    # Different option permutations preserve content ID. Canonical normalization precedes UUIDs.
    r=g.generate('moderate',seed=1,template='radio_family',parameters=dict(a=3,b=2,c=2,r=2));others=[g.generate('moderate',seed=i,template='radio_family',parameters=r['generation']['parameters']) for i in range(16)]
    assert len({z['question'][':question/id'] for z in others})==1
    assert len({tuple(a[':answer/id'] for a in z['question'][':question/answer-fields'][0][':answer-field/choices']) for z in others})>1
    for rec in [r,*records,*held]:
        q=rec['question'];f=q[':question/answer-fields'][0]
        assert q[':question/problem']==g.normalize_prose(q[':question/problem'])
        assert q[':question/worked-solution']==g.normalize_prose(q[':question/worked-solution'])
        assert all(a[':answer/value']==g.normalize_tex(a[':answer/value']) for a in f[':answer-field/choices'])
    corrupt=copy.deepcopy(r);corrupt['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+='\x0c'
    try:g.checked_record(corrupt)
    except ValueError:pass
    else:raise AssertionError('C0 mutation accepted by public content guard')
    save('signed-native-input.json',native);subprocess.run([str(ROOT/m['binary']),str(D/'signed-native-input.json'),str(D/'signed-native-report.json')],check=True,capture_output=True,text=True)
    nr=json.loads((D/'signed-native-report.json').read_text());assert nr['documented_unresolved_checks']==0
    assert registered()==baseline
    save('audit.json',{'passed':True,'source_basis':1356,'refresh_absent_ROOT_authorized_prior_snapshot':True,'wrapper_byte_matches':wrappers,'MA_source_ids':sorted(c['source_id'] for c in cases),'independent_inventory':0,'native_provenance_hashes_verified':42,'native_binary_sha256':m['binary_sha256'],'signed_boundary_records':counts,'held_data_slot_records':len(held),'slots':{'free_coordinate':['x','t','u'],'row_multiplier':[-4,-2,2,4]},'held_other_coefficients':True,'signed_components_independently_read_from_display':True,'C0_learner_strings_checked':True,'C0_public_guard_mutation_rejected':True,'normalized_before_ID_evidence':True,'native_signed_boundary':{'accepted':nr['accepted_checks'],'rejected':nr['rejected_checks'],'unresolved':0},'registered_files_and_pathset_unchanged':True,'registered_files':len(baseline['files']),'normalization_dependency_sha256':sha(ROOT/'scripts/question_capture/math_format.py'),'draft_sha256':sha(D.with_suffix('.py')),'ROOT_approval':'pending'})
    print(json.dumps(json.loads((D/'audit.json').read_text()),indent=2))
if __name__=='__main__':main()

"""Current-source fidelity, substantive task identities, and declared slot coverage."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess
from functools import reduce
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
g=v.g
LEVELS=('easy','moderate','hard')
GENERATOR_UUID=g.uid('question-generator')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint(q):
    # Remove unknown-letter, vector-name, row-order, coordinate-order, and row-scale aliases.
    prompt=q[':question/problem'].replace(r'\langle','⟨').replace(r'\rangle','⟩');variable=re.search(r'Find \$([A-Za-z])\$',prompt)[1]
    m=g.printed_vectors(prompt).subs(sp.Symbol(variable),sp.Symbol('U'))
    keys=[]
    for cols in itertools.permutations(range(3)):
        rows=[]
        for row in m.tolist():
            es=[sp.expand(row[j])for j in cols]
            coeffs=[c for e in es for c in sp.Poly(e,sp.Symbol('U')).all_coeffs()]
            common=reduce(sp.gcd,coeffs)
            if common:es=[sp.cancel(e/common)for e in es]
            vals=tuple(map(str,es));neg=tuple(str(-e)for e in es)
            rows.append(min(vals,neg))
        keys.append(tuple(sorted(rows)))
    return g.digest(min(keys))
def as_record(q):
    q=copy.deepcopy(q)
    q[':question/id']=str(q[':question/id'])
    q[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    fs=[]
    for f in q[':question/answer-fields']:
        fs.append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']}for a in f[':answer-field/choices']]})
    out={k:q[k]for k in (':question/id',':question/problem',':question/worked-solution',':question/difficulty')};out[':question/answer-fields']=fs
    return {'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':out,'generation':{'eligible_for_learning':False,'evidence_only':True,'template':q.get(':question/math-academy-id','existing'),'profile':'source-current'}}
def check(r):
    assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
    level=r['question'][':question/difficulty'].split('/')[-1];assert level in LEVELS
    assert r['generation']['profile']=='method'
    replay=g.generate(level,parameters=r['generation']['parameters'],template=r['generation']['template'],field_type=r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1],seed=r['generation']['seed'])
    assert replay==r,'Generator instance does not replay exactly'
    v.check(r)
    return fingerprint(r['question'])
def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed' and validation['source']['basis']==2535
    eng=json.loads((HERE/'engine-input.json').read_text())
    subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    components=[]
    for sid,q in g.ORIGINALS.items():
        var,d,roots=g.roots_from_prompt(q[':question/problem']);m=g.printed_vectors(q[':question/problem']);options=[]
        for f in q[':question/answer-fields']:
            correct=f.get(':answer-field/correct',{}).get(':answer/id')
            for a in f[':answer-field/choices']:
                options.append({'field_key':f[':answer-field/key'],'field_type':f[':answer-field/type'][':db/ident'],'answer_type':a[':answer/type'][':db/ident'],'source_value':a[':answer/value'],'original_correct':None if correct is None else a[':answer/id']==correct,'recipe':'scalar/root RHS atom minus affine shift h','interpretation':'opaque source evidence; not a learner-facing error recipe'})
        components.append({'source_id':sid,'vectors':[[str(z)for z in row]for row in m.tolist()],'determinant':str(d),'roots':list(map(str,roots)),'worked_solution_blocks':re.findall(r'\$\$(.*?)\$\$',q.get(':question/worked-solution',''),re.S),'profile':'source:'+sid+':raw','options':options})
    (HERE/'components.json').write_text(json.dumps(components,indent=2)+'\n')
    cover={};fixtures=[]
    for level,template in [('easy','linear'),('moderate','linear'),('moderate','quadratic'),('hard','linear')]:
        slots=set();patterns=set();signs=set();zeros=set();fingerprints=set()
        for seed in range(150):
            r=g.generate(level,seed,template=template);m=g.printed_vectors(r['question'][':question/problem']);x=sp.Symbol('k')
            pos=tuple((i,j)for i in range(3)for j in range(3)if x in m[i,j].free_symbols)
            slots.update(pos);patterns.add(pos);signs.update(int(sp.sign(z))for z in m if not z.free_symbols);zeros.update((i,j)for i in range(3)for j in range(3)if m[i,j]==0);fingerprints.add(fingerprint(r['question']))
            if seed<12:check(r);fixtures.append(v.native(r,f'{level}-{template}-{seed}'))
        expected={(i,j)for i in ((1,2)if level=='hard'else range(3))for j in range(3)}
        assert slots==expected and len(fingerprints)>=140
        if level=='easy':assert len(zeros)==9
        if level=='moderate'and template=='linear':
            assert {p for p in patterns if len(p)==2}=={tuple(sorted(((i,j),(i,(j+1)%3))))for i in range(3)for j in range(3)}
        cover[level+'/'+template]={'sample_count':150,'distinct_tasks':len(fingerprints),'positions':sorted(slots),'eligible_positions':sorted(expected),'unseen_eligible_positions':[],'patterns':sorted(patterns),'numeric_signs':sorted(signs),'zero_positions':sorted(zeros)}
    # Same base numerical data; only which component is unknown changes.
    baseline=[['2','-3','4'],['5','6','-7'],['-2','8','3']];targets=[]
    for pos in ((0,0),(1,1)):
        data=copy.deepcopy(baseline);data[pos[0]][pos[1]]='k'
        r=g.generate('moderate',template='linear',field_type='blank',parameters={'vectors':data,'variable':'k'});check(r)
        x=sp.Symbol('k');m=g.printed_vectors(r['question'][':question/problem']);assert [(i,j)for i in range(3)for j in range(3)if m[i,j].has(x)]==[pos]
        targets.append(r);fixtures.append(v.native(r,'controlled-target-'+str(pos)))
    assert targets[0]['question'][':question/problem']!=targets[1]['question'][':question/problem']
    for index,r in enumerate(targets):
        params=copy.deepcopy(r['generation']['parameters']);params['variable']='t';params['vectors']=[[z.replace('k','t')for z in row]for row in params['vectors']]
        alias=g.generate('moderate',template='linear',field_type='blank',parameters=params);check(alias);assert fingerprint(alias['question'])==fingerprint(r['question']);fixtures.append(v.native(alias,'variable-t-'+str(index)))
    (HERE/'reference/slot-grading-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
    subprocess.run([str(HERE/'check-engine'),str(HERE/'reference/slot-grading-input.json'),str(HERE/'reference/slot-grading-report.json')],check=True)
    report={'status':'passed','source_basis':2535,'source_questions':len(g.ORIGINALS),'source_bank_fidelity':validation['source_coverage'],'slot_coverage':cover,'controlled_changed_target_examples':targets,'actual_grader_sha256':sha(HERE/'check-engine'),'generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(HERE/'validate.py'),'inventory_validator_sha256':sha(Path(__file__)),'content_identity':'mathematical task excludes variable letters, vector names, row and coordinate permutations, nonzero row scaling, bank choice, seed and option order','supported_levels':list(LEVELS),'capability_exceptions':[],'sampling_policy':'Authored coordinate bound <=8 remains conservative; exact evidence replays additionally cover larger coefficients, scaled unknown x, and repeated unknowns in two vectors. Evidence-only source profiles are never imported.'}
    (HERE/'reference/inventory-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ['status','source_questions','supported_levels','capability_exceptions']}))
if __name__=='__main__':main()

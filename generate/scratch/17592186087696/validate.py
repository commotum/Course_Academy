"""Validate rendered dimensions and boolean keys independently, then native grading."""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
from collections import Counter
from pathlib import Path
D=Path(__file__).resolve().parent;REPO=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,value): (D/name).write_text(json.dumps(value,indent=2)+'\n')
def read_prompt(q):
    pairs=g.parse_matrices(q[':question/problem'])
    return pairs

def check_record(rec):
    q=rec['question'];pairs=read_prompt(q);assert len(pairs)==3
    fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};assert set(fields)=={l for l,m in pairs}
    assert q[':question/difficulty']==':question.difficulty/easy'
    identities=[q[':question/id']];selected=[]
    for label,m in pairs:
        rows=len(m);cols=len(m[0]);assert all(len(row)==cols for row in m)
        f=fields[label];assert f[':answer-field/type']==':answer-field.type/checkbox'
        bank={a[':answer/value']:a for a in f[':answer-field/choices']};assert set(bank)=={'true','false'}
        assert all(a[':answer/type']==':answer.type/text' for a in bank.values())
        expected='true' if rows==cols else 'false';assert f[':answer-field/correct']==[':answer/id',bank[expected][':answer/id']]
        identities+=[f[':answer-field/id']]+[a[':answer/id'] for a in bank.values()]
        step=next(s for s in q[':question/worked-solution'].split('\n\n') if s.startswith('- $'+label+'$'))
        assert ('*not*' in step)==(rows!=cols)
        assert f'It has ${rows}$ row' in step and f'and ${cols}$ column' in step
        assert f'${rows}\\times {cols}$' in step
        if expected=='true':selected.append(label)
    conclusion=q[':question/worked-solution'].split('Therefore, ')[1]
    assert re.findall(r'\$([A-Z])\$',conclusion)==selected
    if not selected:assert 'none of these matrices' in conclusion
    assert len(identities)==len(set(identities))
    assert rec['generation']['mathematical_fingerprint']==g.mathematical_fingerprint('three-checkbox',g.parameters_of(q))
    return True

def engine_item(rec):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        bank={a[':answer/id']:a for a in f[':answer-field/choices']};cv=bank[f[':answer-field/correct'][1]][':answer/value']
        for value in ('true','false'):
            checks.append({'field_index':i,'submitted_answer_id':next(a[':answer/id'] for a in bank.values() if a[':answer/value']==value),'expected':'accepted' if value==cv else 'rejected','purpose':'Checkbox boolean input'})
        # Check both field-owned boolean choices through the actual ID-selection contract.
    return {'label':rec['question'][':question/id'],'record':rec,'checks':checks}

def native_engine():
    sys.path.insert(0,str(REPO/'scripts'))
    from serve_graph_explorer import build_learning
    build_learning(REPO.parent/'EDB')
    libraries={n:max((REPO/'target/release/deps').glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
    source=D/'check-engine.rs';source.write_bytes((REPO/'generate/runs/current/check-engine.rs').read_bytes());engine=D/'check-engine'
    cmd=['rustc','--edition=2024','-O',str(source)]
    for name,path in libraries.items():cmd+=['--extern',name+'='+str(path)]
    cmd+=['-L','dependency='+str(REPO/'target/release/deps'),'-L','dependency='+str(REPO.parent/'EDB/target/release/deps'),'-o',str(engine)]
    subprocess.run(cmd,check=True)
    write('engine-build.json',{'libraries':{n:str(p) for n,p in libraries.items()},'hashes':{n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in libraries.items()},'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    return engine

def main():
    cases=[];records=[];review=[]
    for sid in g.SUPPORTED_SOURCES:
        src=g.QS[sid];p=g.SOURCE_PARAMS[sid];rec=g.generate(parameters=p);check_record(rec)
        assert rec['question'][':question/problem']==src[':question/problem'],sid
        assert rec['question'][':question/worked-solution']==src[':question/worked-solution'],sid
        for f in rec['question'][':question/answer-fields']:
            sf=next(f2 for f2 in src[':question/answer-fields'] if f2[':answer-field/key']==f[':answer-field/key'])
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
            cv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert cv==sf[':answer-field/correct'][':answer/value']
        cases.append({'source_id':sid,'parameters':p,'shape_triple':[g.shape(m) for m in p['matrices']],'complete_banks_matched':3,'choices_matched':6,'prompt_exact':True,'solution_exact':True});records.append(rec)
        review.append('Source '+sid+' (exact replay)\n\n'+g.markdown(rec))
    # Exhaust all dimensions in every slot, with other mathematical data held fixed.
    coverage={str(i):set() for i in range(3)};patterns=set()
    for i in range(3):
        for rows,cols in g.SHAPES:
            dims=[(2,2),(2,3),(1,1)];dims[i]=(rows,cols)
            p={'labels':['A','B','C'],'matrices':[[['0']*c for _ in range(r)] for r,c in dims],'none_instruction':True,'trailing_space':False,'legacy_plural':False}
            rec=g.generate(parameters=p);check_record(rec);records.append(rec);coverage[str(i)].add((rows,cols))
    for bits in itertools.product((False,True),repeat=3):
        p={'labels':['A','B','C'],'matrices':[[['1']*(2 if sq else 3) for _ in range(2)] for sq in bits],'none_instruction':True,'trailing_space':False,'legacy_plural':False}
        rec=g.generate(parameters=p);check_record(rec);records.append(rec);patterns.add(bits)
    tasks=set()
    for seed in range(150):
        rec=g.generate(seed=seed);check_record(rec);records.append(rec);tasks.add(rec['generation']['mathematical_fingerprint'])
        assert g.generate(seed=seed+1,parameters=rec['generation']['parameters'])['question']==rec['question']
    # Coefficient, label and permutation changes alone cannot establish diversity.
    p=records[-1]['generation']['parameters'];p2=json.loads(json.dumps(p));p2['labels']=['X','Y','Z'];p2['matrices']=[[[str(int(x)+1) for x in row] for row in m] for m in reversed(p2['matrices'])]
    assert g.mathematical_fingerprint('',p)==g.mathematical_fingerprint('',p2)
    for level in ('moderate','hard'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('unsupported difficulty produced')
    write('source-cases.json',cases);write('validation-instances.json',records)
    engine=native_engine();write('native-input.json',[engine_item(r) for r in records]);subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
    native=json.loads((D/'native-report.json').read_text());assert native['documented_unresolved_checks']==0 and native['accepted_checks']==len(records)*3 and native['rejected_checks']==len(records)*3
    for seed in (0,2,5):review.append('Variant seed '+str(seed)+'\n\n'+g.markdown(g.generate(seed=seed)))
    (D/'review.md').write_text('\n\n---\n\n'.join(review)+'\n')
    write('validation.json',{'status':'pass','source_basis':g.SOURCE['basis'],'source_banks_matched':15,'source_banks_total':15,'source_choices_matched':30,'source_choices_total':30,'exact_prompts':5,'exact_solutions':5,'excluded_source_ids':['q-7826'],'excluded_canonical_id':'e-4391','mathematical_instances_checked':len(records),'distinct_sample_tasks':len(tasks),'slot_dimension_coverage':{k:sorted(v) for k,v in coverage.items()},'all_8_selection_patterns_checked':len(patterns),'changed_dimension_with_other_matrices_fixed':True,'seed_independent_identity':True,'coefficient_label_order_only_duplicates_excluded':True,'actual_learner_grader_passed':True,'fidelity':'exact for five supported source questions; incomplete radio and canonical excluded'})
if __name__=='__main__':main()

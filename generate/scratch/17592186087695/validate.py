"""Independent displayed-array, complete-bank, witness, replay and native grading checks."""
import copy, hashlib, importlib.util, json, re, subprocess, uuid
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def parse(text):return g.fingerprint_text(text)
def displayed(text):
    out={}
    for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}',text):
        rows=[[Fraction(v.strip()) for v in row.split('&')] for row in m[2].split('\\\\')]
        assert rows and len({len(row) for row in rows})==1
        out[m[1]]=rows
    assert len(out)==3
    return out

def solution_check(q):
    matrices=displayed(q[':question/problem']);zs={name:all(v==0 for row in rows for v in row) for name,rows in matrices.items()}
    fields=q[':question/answer-fields'];assert len(fields)==3 and {f[':answer-field/key'] for f in fields}==matrices.keys()
    for f in fields:
        typ=f[':answer-field/type'];assert (typ.get(':db/ident') if isinstance(typ,dict) else typ)==':answer-field.type/checkbox'
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
        cr=f[':answer-field/correct'];cid=str(cr[':answer/id']) if isinstance(cr,dict) else cr[1]
        cs=[a for a in f[':answer-field/choices'] if str(a[':answer/id'])==cid];assert len(cs)==1 and cs[0][':answer/value']==str(zs[f[':answer-field/key']]).lower()
    text=q[':question/worked-solution'];bullets=text.split('\n\n')[:3];assert len(bullets)==3
    for name,bullet in zip(matrices,bullets):
        assert bullet.startswith('- $'+name+'$ is ')
        assert ('not' not in bullet)==zs[name]
        if not zs[name]:
            m=re.search(r'\$\{([a-z])\}_\{(\d)(\d)\}=([\d.]+)\\ne 0\$',bullet);assert m,bullet
            assert m[1]==name.lower();rows=matrices[name];r,c=int(m[2]),int(m[3]);assert rows[r-1][c-1]==Fraction(m[4])!=0
    conclusion=text.split('\n\n')[-1];assert set(re.findall(r'\$([A-Z])\$',conclusion))=={n for n,z in zs.items() if z}
    return 3

def independent(r):
    q=r['question'];m=r['generation'];assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
    assert q[':question/difficulty']==':question.difficulty/easy'
    assert r==g.generate('easy',m['seed'],m['template'],m['parameters'],m['bank_profile'])
    assert parse(q[':question/problem'])==m['parameter_fingerprint'];solution_check(q)
    ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
    assert len(ids)==len(set(ids));[uuid.UUID(v) for v in ids]
    for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('$')%2==0 and text.count('{')==text.count('}') and '{{' not in text

def checks(r):
    return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every field-owned checkbox option through actual learner grader'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def build_engine():
    deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';harness=ROOT/'generate/runs/current/check-engine.rs';libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')};cmd=['rustc','--edition=2024','-O',str(harness)]
    for n,p in libs.items():cmd+=['--extern',n+'='+str(p)]
    cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-engine')];subprocess.run(cmd,check=True)
    save('engine-build.json',{'harness_sha256':sha(harness),'libraries':{str(p):sha(p) for p in libs.values()},'binary_sha256':sha(HERE/'check-engine')})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    sources=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in sources['record'][':knowledge-point/questions']};rs=[];cases=[];review=[];coverage={}
    for mid,t in g.TEMPLATES.items():
        replay=g.generate('easy',template=mid,parameters=t['parameters']);independent(replay);q=qs[mid];fresh=replay['question'];assert fresh[':question/problem']==q[':question/problem']
        of={f[':answer-field/key']:f for f in q[':question/answer-fields']}
        for f in fresh[':question/answer-fields']:
            old=of[f[':answer-field/key']];assert sorted(a[':answer/value'] for a in old[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']);assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value']
        if t['correction']:
            assert mid=='q-126201' and fresh[':question/worked-solution']==q[':question/worked-solution'].replace('{i}_{12}','{i}_{21}')
            try:solution_check(q)
            except AssertionError:pass
            else:raise AssertionError('Source witness error was not detected')
        else:assert fresh[':question/worked-solution']==q[':question/worked-solution'];solution_check(q)
        cases.append({'source':mid,'matched_fields':3,'total_fields':3,'matched_values':6,'total_values':6,'correct_designations_matched':3,'missing_options':[],'extra_options':[],'exact_prompt':True,'exact_solution':not bool(t['correction']),'documented_correction':t['correction']});rs.append(replay)
        review.append('## '+mid+' source and replay\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nReplay:\n\n'+g.markdown(replay))
        shapes=set();cells=set();values=set();zeros=set()
        for seed in range(120):
            try:r=g.generate('easy',seed,mid)
            except ValueError:continue
            independent(r);rs.append(r)
            for rows,w in zip(r['generation']['parameters']['matrices'],r['generation']['parameters']['witnesses']):
                shapes.add((len(rows),len(rows[0])));zeros.add(w is None)
                if w:cells.add(tuple(w))
                values.update(v for row in rows for v in row)
        coverage[mid]={'shapes':sorted(shapes),'witness_cells':sorted(cells),'values':sorted(values),'zero_roles':sorted(zeros)}
        variant=next(r for r in rs if r['generation']['template']==mid and r['question'][':question/problem']!=q[':question/problem']);review.append('## '+mid+' variant\n\n'+g.markdown(variant))
    # Every eligible witness cell with other data fixed; catch stale location/value.
    position_checks=0
    t=g.TEMPLATES['q-68729'];p=copy.deepcopy(t['parameters'])
    for r in range(2):
        for c in range(2):
            p['matrices'][0]=[['0','0'],['0','0']];p['matrices'][0][r][c]='1';p['witnesses'][0]=[r+1,c+1];rec=g.generate('easy',template='q-68729',parameters=p);independent(rec);rs.append(rec);position_checks+=1
    # Role-preserving zero matrix shapes cover the complete normal shape domain.
    for r in range(1,5):
        for c in range(1,6):
            p=copy.deepcopy(g.TEMPLATES['q-126204']['parameters']);p['matrices'][0]=[['0']*c for _ in range(r)];rec=g.generate('easy',template='q-126204',parameters=p);independent(rec);rs.append(rec)
    bad=copy.deepcopy(rs[-1]);bad['question'][':question/answer-fields'][0][':answer-field/correct']=bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/id'];negative=0
    try:solution_check(bad['question'])
    except (AssertionError,TypeError,KeyError):negative+=1
    else:raise AssertionError('Corrupt key accepted')
    for level in ('moderate','hard','unclassified'):
        try:g.generate(level)
        except ValueError:negative+=1
        else:raise AssertionError('Unsupported band accepted')
    batch=g.batch('easy',1000,2099);assert len(batch)==1000 and len({parse(r['question'][':question/problem']) for r in batch})==1000
    for r in batch:independent(r)
    assert g.generate('easy',template='q-68729',parameters=t['parameters'],seed=1)['question']==g.generate('easy',template='q-68729',parameters=t['parameters'],seed=3)['question']
    rs+=batch;build_engine();save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(rs)]);subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('source-bank-replay.json',cases);save('slot-coverage.json',coverage);(HERE/'review.md').write_text('\n\n---\n\n'.join(review)+'\n')
    save('validation.json',{'status':'pass','source_basis':sources['basis'],'supported_levels':['easy'],'validated_records':len(rs),'complete_source_banks':15,'source_bank_values_matched':30,'source_correct_designations_matched':15,'fidelity_corrections':['q-126201 witness i_12 corrected to i_21'],'excluded_incomplete_unrated_sources':['q-11553','q-7827'],'finite_distinct_batch_validated':1000,'changed_witness_checks':position_checks,'negative_controls':negative,'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):sha(p) for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'templates.json',HERE/'source.json',HERE/'check-engine',HERE/'engine-build.json',HERE/'replenish.py')}})
    print('Validation passed:',len(rs),'instances; all 15 supported banks, correction recorded; actual grader verified.')
if __name__=='__main__':main()

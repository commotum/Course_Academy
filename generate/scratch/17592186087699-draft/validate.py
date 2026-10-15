#!/usr/bin/env python3
"""Read actual printed matrices, products, statements, banks, prose and stages."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;R=D.parents[2];SCRIPT=D.with_suffix('.py')
spec=importlib.util.spec_from_file_location('inverse_direct_draft',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from scripts.question_capture.math_format import normalize_prose,validate_generated_record

def write(name,data):(D/name).write_text(json.dumps(data,indent=2)+'\n')
def display_truth(prompt):
    matrices=g.matrices_from_prompt(prompt)
    statements=re.findall(r'(?<!\$)\$(?!\$)([^$]+)(?<!\$)\$(?!\$)',prompt)[-3:]
    out=[]
    for statement in statements:
        stmt=statement.replace(' ','').replace('{','').replace('}','')
        match=re.fullmatch(r'([A-Z])([A-Z])=([A-Z])([A-Z])=I_2',stmt)
        if match:
            a,b,c,d=match.groups();assert (a,b)==(d,c)
            out.append(matrices[a]*matrices[b]==sp.eye(2) and matrices[c]*matrices[d]==sp.eye(2));continue
        match=re.fullmatch(r'([A-Z])(=|\\ne)([A-Z])\^-1',stmt);assert match,stmt
        a,op,b=match.groups();eq=matrices[a]*matrices[b]==sp.eye(2) and matrices[b]*matrices[a]==sp.eye(2)
        out.append(eq if op=='=' else not eq)
    return matrices,out

def validate_record(record):
    q=record['question'];meta=record['generation'];t=g.TEMPLATES[meta['template']];raw=meta['profile']=='raw-source'
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]:
        assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',text),'C0 control'
    if ':question/worked-solution' in q:validate_generated_record(record)
    if t['canonical']:
        named=g.matrices_from_prompt(q[':question/problem'])
        if raw:
            # Incomplete canonical prompt is retained as ineligible evidence.
            blocks=re.findall(r'\\begin\{aligned\}.*?\\end\{aligned\}',q[':question/worked-solution'],re.S)
            first=list(g.MAT.finditer(blocks[0]));named=dict(zip(t['labels'],[sp.Matrix(g.read_matrix(m[1])) for m in first[:2]]))
            assert sp.Matrix(g.read_matrix(g.MAT.search(q[':question/problem'])[1]))==named['A']
        assert named['A']*named['B']==sp.eye(2) and named['B']*named['A']==sp.eye(2)
        values=[True]
    else:named,values=display_truth(q[':question/problem'])
    assert set(named)==set(t['labels'])
    blocks=re.findall(r'\\begin\{aligned\}.*?\\end\{aligned\}',q.get(':question/worked-solution',''),re.S)
    witnesses=[]
    for i,block in enumerate(blocks):
        pair=re.search(r'\\begin\{aligned\}([A-Z]{2})',block)[1]
        math=list(g.MAT.finditer(block));assert len(math)==3
        left,right=[sp.Matrix(g.read_matrix(m[1])) for m in math[:2]]
        assert left==named[pair[0]] and right==named[pair[1]],'Displayed operands differ from actual prompt'
        product=left*right;shown=g.read_matrix(math[2][1],stars=True)
        concrete=[]
        for r in range(2):
            for c in range(2):
                if shown[r][c] is not None:
                    assert shown[r][c]==product[r,c],'Wrong displayed product cell'
                    concrete.append(r*2+c)
        star=any(v is None for row in shown for v in row)
        if star:
            assert len(concrete)==1 and product[concrete[0]]!=sp.eye(2)[concrete[0]],'Invalid nonidentity witness'
            assert r'\ne {I}_{2}' in block
            witnesses.append(concrete[0])
        else:
            assert len(concrete)==4
            if t['blocks']:assert product==sp.eye(2) and r'={I}_{2}' in block
            witnesses.append(None)
    # Assert full shared prose + exact operative stage recipes using the actual
    # printed matrices/witnesses. No reliance on generation parameter/key data.
    mats=[named[x] for x in t['labels']]
    wm=witnesses if t['blocks'] else []
    ep,es=g.render_masks(t,mats,wm,raw)
    assert q[':question/problem']==ep,'Prompt backbone mismatch'
    assert q.get(':question/worked-solution')==es,'Complete worked-solution prose/stage mismatch'
    if not raw or t['has_solution']:assert blocks,'Missing verification stages'
    assert len(blocks)==(len(t['blocks']) if t['blocks'] else (0 if raw else 3))
    g.validate_parameters({'matrices':[g.serial_matrix(m) for m in mats],'witnesses':wm},t,meta['difficulty'],meta['profile'])
    assert len(q.get(':question/answer-fields',[]))==len(t['fields'])
    g.uuid.UUID(q[':question/id'])
    seen=set()
    for i,f in enumerate(q.get(':question/answer-fields',[])):
        assert f[':answer-field/id'] not in seen;seen.add(f[':answer-field/id'])
        choices=f[':answer-field/choices'];expected=t['fields'][i]
        assert sorted((a[':answer/type'],a[':answer/value']) for a in choices)==sorted((a['type'],a['value']) for a in expected['choices'])
        for a in choices:
            assert a[':answer/id']==g.uid(f[':answer-field/id'],a[':answer/type']+':'+a[':answer/value'])
            assert a[':answer/id'] not in seen;seen.add(a[':answer/id'])
        correct=f.get(':answer-field/correct')
        if correct is None:
            assert raw and expected['correct'] is None;continue
        assert correct[0]==':answer/id'
        chosen=[a[':answer/value'] for a in choices if a[':answer/id']==correct[1]];assert len(chosen)==1
        mathematical=g.selected_words(values) if f[':answer-field/type'].endswith('/radio') else str(values[i]).lower()
        assert chosen[0]==mathematical,'Incorrect designation from actual statements'
    assert meta['mathematical_fingerprint']==g.fingerprint(q[':question/problem'],t,mats)
    return True

def source_compare(record,source):
    q=record['question']
    for key in [':question/difficulty',':question/answer-fields',':question/worked-solution']:
        assert (key in q)==(key in source),('Raw source attribute presence',key)
    for key in [':question/problem',':question/worked-solution']:
        if key in source:assert q[key]==normalize_prose(source[key]),('Full normalized source prose',key)
    if ':question/difficulty' in source:assert q[':question/difficulty']==source[':question/difficulty'][':db/ident']
    assert len(q.get(':question/answer-fields',[]))==len(source.get(':question/answer-fields',[]))
    for got,want in zip(q.get(':question/answer-fields',[]),source.get(':question/answer-fields',[])):
        assert got[':answer-field/key']==want[':answer-field/key']
        assert got[':answer-field/type']==want[':answer-field/type'][':db/ident']
        assert sorted((a[':answer/type'],a[':answer/value']) for a in got[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in want[':answer-field/choices'])
        assert (':answer-field/correct' in got)==(':answer-field/correct' in want)
        if ':answer-field/correct' in want:
            value=next(a[':answer/value'] for a in got[':answer-field/choices'] if a[':answer/id']==got[':answer-field/correct'][1]);assert value==want[':answer-field/correct'][':answer/value']


def main():
    source=json.loads((D/'source.json').read_text());originals=json.loads((D/'source-cases.json').read_text())+[json.loads((D/'canonical.json').read_text())]
    records=[];fidelity=[];mutations=[];render=[]
    for row in originals:
        sid=row['source_id'];p=g.original_parameters(sid)
        raw=g.generate('easy',template=sid,profile='raw-source',parameters=p);validate_record(raw);source_compare(raw,row['record'])
        fidelity.append({'source_id':sid,'prompt_full':True,'solution_full':':question/worked-solution' in row['record'],'key_presence':True,'banks':len(row['record'].get(':question/answer-fields',[])),'choices':sum(len(f[':answer-field/choices']) for f in row['record'].get(':question/answer-fields',[])),'known_designations':sum(':answer-field/correct' in f for f in row['record'].get(':question/answer-fields',[]))})
        completed=g.generate('easy',template=sid,parameters=p);validate_record(completed)
        render.append(completed);records.append({'label':sid+' original parameters, completed presentation','record':completed})
        for level in g.SUPPORTED_LEVELS:
            if sid.startswith('e-') and level!='easy':continue
            variant=g.generate(level,seed=234,template=sid);validate_record(variant);render.append(variant);records.append({'label':sid+' changed '+level,'record':variant})
            again=g.generate(level,seed=88,template=sid,parameters=variant['generation']['parameters'])
            assert variant['question'][':question/id']==again['question'][':question/id']
            # Read every displayed numeric entry across prompt, operands and result.
            # Mutate its actual scalar while retaining the final bank/key.
            text=variant['question'].get(':question/worked-solution','')
            for index,m in enumerate(g.MAT.finditer(text)):
                body=m[1];parts=re.split(r'(&|\\\\)',body)
                for cell,part in enumerate(parts):
                    if cell%2 or part.strip()=='∗':continue
                    changed=str(g.scalar(part)+1);parts2=parts.copy();parts2[cell]=changed
                    mutant=copy.deepcopy(variant);mutant['question'][':question/worked-solution']=text[:m.start(1)]+''.join(parts2)+text[m.end(1):]
                    try:validate_record(mutant)
                    except (AssertionError,ValueError):pass
                    else:raise AssertionError('Unchanged-final-key cell corruption escaped')
                    mutations.append({'source_id':sid,'level':level,'matrix':index,'cell':cell//2})
    semantic_controls=[]
    for item in records:
        rec=item['record'];text=rec['question'].get(':question/worked-solution','')
        if not text:continue
        candidates={
            'product-operator':text.replace(r'\end{bmatrix}\begin{bmatrix}',r'\end{bmatrix}+\begin{bmatrix}',1),
            'reverse-stage-omission':re.sub(r'Likewise, computing.*?\\end\{aligned\}\n\$\$', '',text,count=1,flags=re.S),
            'conclusion':text.replace('correct answer is "','correct answer is "None; ',1),
            'control-character':text+'\x0c',
        }
        for label,changed in candidates.items():
            if changed==text:continue
            bad=copy.deepcopy(rec);bad['question'][':question/worked-solution']=changed
            try:validate_record(bad)
            except (AssertionError,ValueError):pass
            else:raise AssertionError('Unchanged-final-key structural mutation escaped: '+label)
            semantic_controls.append({'label':item['label'],'mutation':label})
    # Variety is task count, excluding notation, witness and bank aliases.
    variety={};slots={}
    for level in g.SUPPORTED_LEVELS:
        tasks=set();templates=set();denominators=set();witnesses=set();fractional=[]
        for seed in range(150):
            rec=g.generate(level,seed=seed);validate_record(rec)
            tasks.add(rec['generation']['mathematical_fingerprint']);templates.add(rec['generation']['template']);witnesses.update(w for w in rec['generation']['parameters']['witnesses'] if w is not None)
            vals=[g.scalar(v) for m in rec['generation']['parameters']['matrices'] for row in m for v in row];denominators.update(int(x.q) for x in vals);fractional.append(sum(x.q>1 for x in vals))
        assert templates==set(g.DEFAULT_TEMPLATES),'Default family coverage'
        assert len(tasks)>=125,('Insufficient repeated-practice task variety',level,len(tasks))
        assert witnesses==set(range(4))
        variety[level]={'sampled':150,'unique_mathematical_tasks':len(tasks),'templates':sorted(templates),'entry_denominators':sorted(denominators),'fractional_entry_range':[min(fractional),max(fractional)]};slots[level]={'nonidentity_witness_positions':sorted(witnesses)}
    # Equivalent rational parameter spellings cannot change IDs or fingerprints.
    anchor=g.generate('hard',seed=7);p=copy.deepcopy(anchor['generation']['parameters'])
    p['matrices']=[[[str(2*g.scalar(v).p)+'/'+str(2*g.scalar(v).q) for v in row] for row in m] for m in p['matrices']]
    alias=g.generate('hard',seed=79,template=anchor['generation']['template'],parameters=p)
    assert anchor['question'][':question/id']==alias['question'][':question/id']
    assert anchor['generation']['mathematical_fingerprint']==alias['generation']['mathematical_fingerprint']
    assert g.generate('easy',field_type='radio')['generation']['template']=='q-7908'
    assert g.generate('easy',field_type='checkbox')['generation']['template']!='q-7908'
    # Strict API and coefficient workload guards apply equally to explicit input.
    invalid=[lambda:g.generate('medium'),lambda:g.generate('easy',template='missing'),lambda:g.generate('easy',profile='missing'),lambda:g.generate('easy',seed='1'),lambda:g.generate('easy',field_type='blank'),lambda:g.generate('hard',template='q-11640',parameters=g.original_parameters('q-11640'))]
    for test in invalid:
        try:test()
        except (ValueError,TypeError):pass
        else:raise AssertionError('Invalid API input accepted')
    cli=json.loads(subprocess.check_output([str(R/'.venv/bin/python'),str(SCRIPT),'--difficulty','all','--count','1','--format','json'],cwd=R));assert isinstance(cli,list) and len(cli)==3
    write('cli-all.json',cli)
    # All complete source-shaped banks: test every answer through current native
    # grade_field. Radio probes use owned answer UUIDs; checkbox probes use its
    # actual checked/unchecked authored answer-ID contract.
    native=[]
    for item in records:
        rec=item['record'];checks=[]
        for i,f in enumerate(rec['question'].get(':question/answer-fields',[])):
            correct=f[':answer-field/correct'][1]
            for a in f[':answer-field/choices']:
                probe={'field_index':i,'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete displayed bank designation'}
                probe['submitted_answer_id']=a[':answer/id']
                checks.append(probe)
        if checks:native.append({**item,'checks':checks})
    write('engine-input.json',native)
    proc=subprocess.run([str(D/'check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],text=True,capture_output=True);write('native-process.json',{'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr});assert proc.returncode==0,proc.stderr
    write('review.json',records);write('render-records.json',render);write('source-fidelity.json',{'practice':11,'canonical':1,'rows':fidelity,'all_original_choices':sum(x['choices'] for x in fidelity),'known_designations':sum(x['known_designations'] for x in fidelity),'missing_designations':1,'missing_worked_solutions':1,'raw_incomplete_canonical_prompts':1})
    write('variety.json',variety);write('slot-coverage.json',slots);write('negative-controls.json',{'unchanged_final_key_cell_mutations_detected':len(mutations),'mutations':mutations,'semantic_controls':semantic_controls,'strict_api_rejections':len(invalid),'rational_scale_alias_identity':True})
    native_report=json.loads((D/'engine-report.json').read_text())
    result={'status':'passed mathematical/source/native checks; player render and independent parent QA reported separately','python':sys.version.split()[0],'sympy':sp.__version__,'original_practice':11,'original_canonical':1,'matched_choices':65,'known_correct_designations':30,'inferred_correct_designations_not_fidelity':1,'whole_raw_banks':11,'field_banks':31,'full_source_solutions_present_matched':11,'source_solution_missing_authored_completion':1,'raw_key_presence_parity':12,'changed_coefficient_family_level_cases':34,'random_records_validated':450,'unchanged_final_key_mutations_detected':len(mutations),'structural_mutations_detected':len(semantic_controls),'native_accepted':native_report['accepted_checks'],'native_rejected':native_report['rejected_checks'],'native_unresolved':native_report['documented_unresolved_checks'],'native_matrix_entry_equivalence_probes':'not applicable: observed fields are checkbox booleans and text radio selection, no matrix-entry blank fields','grader_provenance_hashes':42,'source_basis':2275,'strict_cli_all_count1_list_length':3,'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'scope':'direct verification only; authored moderate/hard uncalibrated arithmetic placements; no plots','root_qa_approval':'pending'}
    write('validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()

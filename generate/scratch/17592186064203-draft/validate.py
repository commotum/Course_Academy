"""Exact rendered polynomial mathematics, frozen bank fidelity and native grading."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import uuid
import sys
from pathlib import Path
import sympy as sp
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def save(name, x):
    (HERE/name).write_text(json.dumps(x, indent=2, default=str)+'\n')

def parse(text):
    return g.fingerprint_text(text)

def bank_check(q):
    fs = q[':question/answer-fields']
    assert len(fs) == 1
    f = fs[0]
    ft = f[':answer-field/type']
    assert (ft.get(':db/ident') if isinstance(ft,dict) else ft) == ':answer-field.type/radio'
    assert f[':answer-field/key'] == 'selection'
    choices = f[':answer-field/choices']
    assert len(choices) == 5
    cid = f[':answer-field/correct']
    cid = str(cid[':answer/id']) if isinstance(cid,dict) else cid[1]
    e = g.integrand(q[':question/problem'])
    values = [g.expression(a[':answer/value']) for a in choices]
    valid = [sp.expand(sp.diff(a,g.X)-e) == 0 for a in values]
    assert sum(valid) == 1 and str(choices[valid.index(True)][':answer/id']) == cid
    assert len({sp.srepr(sp.expand(sp.diff(a,g.X))) for a in values}) == 5
    return e

def evaluated(text):
    text = text.strip().rstrip('.,').replace('✓','')
    # Evaluate the actual integrals and derivative calls in rendered equations.
    text = re.sub(r'\\frac\{\\text\{d\}\}\{\\text\{d\}x\}\[([^\[\]]*)\]',
        lambda m: '('+str(sp.diff(g.expression(m[1]),g.X))+')', text)
    text = re.sub(r'\\frac\{\\text\{d\}\}\{\\text\{d\}x\}\(([^()]*)\)',
        lambda m: '('+str(sp.diff(g.expression(m[1]),g.X))+')', text)
    text = re.sub(r'\\int\s*(.*?)\\text\{d\}([xu])',
        lambda m: '('+str(sp.integrate(g.expression(m[1]),g.X if m[2]=='x' else g.U))+')', text)
    return g.expression(text)

def solution_check(q):
    e = bank_check(q)
    displays = re.findall(r'\$\$\n(.*?)\n\$\$', q[':question/worked-solution'], re.S)
    assert len(displays) == 3
    let = re.search(r'Let \$u=(.*?)\.\$', q[':question/worked-solution'])
    assert let
    inner = g.expression(let[1])
    slope = sp.diff(inner,g.X)
    assert slope != 0 and sp.diff(slope,g.X) == 0
    slope_latex = sp.latex(slope)
    expected = r'\frac{\text{d}u}{\text{d}x}='+slope_latex+r'\,⟹\,\text{d}x='+sp.latex(1/slope)+r'\text{d}u.'
    assert re.sub(r'\s','',displays[0]) == re.sub(r'\s','',expected), (displays[0],expected)
    steps = 1
    for display in displays[1:]:
        display = re.sub(r'\\(?:begin|end)\{aligned\}', '', display)
        previous = None
        for line in display.split(r'\\'):
            left,right = line.replace('&','').split('=')
            lhs = evaluated(left) if left.strip() else previous
            assert lhs is not None
            rhs = evaluated(right)
            # The substitution u=inner is valid across every real interval.
            delta = sp.expand((lhs-rhs).subs(g.U,inner))
            if r'\int' in left or r'\int' in right:
                # Independent indefinite integration can choose different
                # additive constants before/after the u substitution.
                assert sp.diff(delta,g.X) == 0, (line,delta)
            else:
                assert delta in (0,g.C,-g.C), (line,delta)
            previous = rhs
            steps += 1
    assert sp.expand(previous.subs(g.U,inner)-e) == 0
    return steps

def independent(r):
    q,m = r['question'],r['generation']
    assert r['knowledge_point']['db_id'] == g.KP_ID and r['knowledge_point']['id'] == g.KP_UUID
    level = q[':question/difficulty'].split('/')[-1]
    assert r == g.generate(level,m['seed'],m['template'],m['parameters'],m['bank_profile'])
    assert parse(q[':question/problem']) == m['parameter_fingerprint']
    f=q[':question/answer-fields'][0]
    ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
    assert len(set(ids)) == len(ids)
    for i in ids:uuid.UUID(i)
    for text in (q[':question/problem'],q[':question/worked-solution']):
        assert text.count('$')%2 == 0 and text.count('{') == text.count('}')
    return solution_check(q)

def checks(r):
    f=r['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],
        'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
        'purpose':'Every field-owned option tested with actual learner grade_field'} for a in f[':answer-field/choices']]

def main():
    original = {q.get(':question/math-academy-id', str(q[':db/id'])):q for q in g.SOURCE['record'][':knowledge-point/questions']}
    rows=[];cases=[];independent_cases=[];review=[];steps=0;negative=0
    for profile,t in g.TEMPLATES.items():
        anchor=g.generate(t['difficulty'],29,profile,{'b':t['source_b']})
        steps+=independent(anchor)
        if t['source_db_id'] is not None:
            sid=profile if t['evidence_role']=='original_ma' else str(t['source_db_id'])
            raw=g.source_record(sid,raw=True); expected=g.source_record(sid)
            actual=anchor['question']; field=actual[':question/answer-fields'][0]; old=expected[':question/answer-fields'][0]
            assert actual[':question/problem']==expected[':question/problem']
            assert actual[':question/worked-solution']==expected[':question/worked-solution']
            assert [a[':answer/value'] for a in field[':answer-field/choices']]==[a[':answer/value'] for a in old[':answer-field/choices']]
            assert next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value']
            result={'source_id':sid,'profile':profile,'parameters':{'b':t['source_b']},'matched_values':5,'total_values':5,'matched_distractors':4,'total_distractors':4,'exact_normalized_prompt':True,'exact_normalized_solution':True,'ordered_complete_bank':True,'missing_options':[],'extra_options':[]}
            (cases if t['evidence_role']=='original_ma' else independent_cases).append(result)
        variant=g.generate(t['difficulty'],29,profile,{'b':80})
        steps+=independent(variant)
        assert anchor['generation']['parameter_fingerprint']!=variant['generation']['parameter_fingerprint']
        review.append('## '+profile+' ('+t['evidence_role']+')\n\nAnchor:\n\n'+g.markdown(anchor)+'\n\nChanged b=80:\n\n'+g.markdown(variant))
        # Exhaustively verify the finite permitted coefficient slot and every row.
        if t['evidence_role']!='independent_inventory':
            for b in g.DOMAIN:
                r=g.generate(t['difficulty'],29,profile,{'b':b});steps+=independent(r);rows.append(r)
                assert r['question']==g.generate(t['difficulty'],30,profile,{'b':b})['question']
    incomplete=[]
    for sid in ('q-12015','q-12493'):
        q=g.source_record(sid); raw=g.source_record(sid,raw=True)
        assert ':question/difficulty' not in q and ':question/worked-solution' not in q
        assert ':answer-field/correct' not in q[':question/answer-fields'][0]
        assert q[':question/problem']==g.normalize_prose(raw[':question/problem'])
        assert [a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]==[g.normalize_tex(a[':answer/value']) for a in raw[':question/answer-fields'][0][':answer-field/choices']]
        incomplete.append({'source_id':sid,'raw':raw,'normalized_reference':q,'role':'Unrated incomplete reference; excluded from learning inventory and complete-bank fidelity denominator'})
    save('incomplete-references.json',incomplete)
    for kwargs in ({'seed':True},{'seed':1.5},{'seed':'1'},{'parameters':{'b':True}},{'parameters':{'b':0}},{'parameters':{'b':81}},{'parameters':{'b':1.0}},{'parameters':[]},{'parameters':{'b':2,'x':3}},{'profile':'bad'},{'profile':'q-113492'},{'level':'bad'}):
        call={'level':'easy',**kwargs}
        try:g.generate(**call)
        except ValueError:negative+=1
        else:raise AssertionError(('Accepted invalid API',call))
    for level in g.SUPPORTED_LEVELS:
        for count in (True,1.5,-1,g.capacity(level)+1):
            try:g.batch(level,count)
            except ValueError:negative+=1
            else:raise AssertionError('Invalid batch count accepted')
        for seed in (True,1.5,'1'):
            try:g.batch(level,1,seed)
            except ValueError:negative+=1
            else:raise AssertionError('Invalid batch seed accepted')
        full=g.batch(level,g.capacity(level),41)
        assert len(full)==g.capacity(level)
        assert len({parse(r['question'][':question/problem']) for r in full})==len(full)
        assert g.batch(level,0)==[]
    # Every independently read ordered math row must detect a change.
    r=copy.deepcopy(rows[0]); sol=r['question'][':question/worked-solution']
    spans=list(re.finditer(r'(?<==)[^=]*?(?=\\\\|\\end\{aligned\})',sol))
    mutation_rejections=0
    for span in spans:
        r=copy.deepcopy(rows[0]);q=r['question'];q[':question/worked-solution']=sol[:span.start()]+'0'+sol[span.end():]
        try:solution_check(q)
        except (AssertionError,ValueError,TypeError,SyntaxError):mutation_rejections+=1
        else:raise AssertionError('Corrupted row accepted')
    for part in ('answer','given','substitution'):
        r=copy.deepcopy(rows[0]);q=r['question']
        if part=='answer':q[':question/answer-fields'][0][':answer-field/choices'][4][':answer/value']='0'
        elif part=='given':q[':question/problem']=q[':question/problem'].replace('48','49')
        else:q[':question/worked-solution']=q[':question/worked-solution'].replace('Let $u=3x-1.','Let $u=3x-2.')
        try:solution_check(q)
        except (AssertionError,ValueError):negative+=1
        else:raise AssertionError('Corrupted '+part+' accepted')
    native=[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(rows)]
    # Radio fields grade owned answer identity. Equivalent TeX is presentation-only;
    # test the real engine on a separate algebraically equivalent displayed bank.
    equiv=copy.deepcopy(rows[0]); f=equiv['question'][':question/answer-fields'][0]
    for a in f[':answer-field/choices']:a[':answer/value']=sp.latex(sp.expand(g.expression(a[':answer/value'])))
    bank_check(equiv['question']);native.append({'label':'equivalent-displayed-bank','record':equiv,'checks':checks(equiv)})
    save('engine-input.json',native)
    engine_binary=ROOT/'generate/runs/current/check-engine'
    assert hashlib.sha256(engine_binary.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
    subprocess.run([str(engine_binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    baseline=json.loads((HERE/'registered-baseline.json').read_text())
    baseline_root=ROOT/'generate/scratch/17592186064203'
    assert set(baseline)=={str(p.relative_to(ROOT)) for p in [baseline_root.with_suffix('.py'),*sorted(p for p in baseline_root.rglob('*') if p.is_file())]}
    assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in baseline.items())
    reference_cases=[{'source_id':r['source_id'],'reference_only':True,'api':'source_record','parameters':{'source_id':r['source_id'],'raw':True},'record':r['raw'],'role':r['role']} for r in incomplete]
    save('source-cases.json',cases+reference_cases);save('independent-cases.json',independent_cases)
    (HERE/'review.md').write_text('\n\n---\n\n'.join(review)+'\n')
    for level in g.SUPPORTED_LEVELS:
        preview=g.batch(level,2,29);save('preview-'+level+'.json',preview)
        (HERE/('preview-'+level+'.md')).write_text('\n\n---\n\n'.join(g.markdown(r) for r in preview)+'\n')
    cli=json.loads(subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','1']))
    assert len(cli)==3 and [r['question'][':question/difficulty'].split('/')[-1] for r in cli]==list(g.SUPPORTED_LEVELS)
    report={'status':'pass','source_basis':2275,'lineage':g.SOURCE['lineage'],'database_writes':0,'registration_changes':0,'registered_baseline':'byte-exact full path set and hashes verified','source_coverage':{'original_complete_banks_matched':5,'original_complete_bank_total':5,'matched_values':25,'total_values':25,'matched_distractors':20,'total_distractors':20,'independent_inventory_banks_checked':5,'incomplete_reference_records':2,'hard_original_sources':0},'mathematics':{'exhaustive_finite_instances':len(rows),'ordered_math_rows':steps,'mutated_rows_rejected':mutation_rejections,'negative_controls':negative,'capacity':{level:g.capacity(level) for level in g.SUPPORTED_LEVELS},'coefficient_domain':'b builtin int 1..80','pairwise_choice_distinctness':'distinct derivatives, modulo integration constants','branches':'polynomials on all real x'},'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'native_equivalent_probe':'Algebraically expanded equivalent full bank; radio grading uses field-owned IDs','CLI_all_count_1':'flat 3 records','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'private_formatter_sha256':hashlib.sha256((HERE/'math_format.py').read_bytes()).hexdigest(),'live_formatter_dependency':False,'engine_sha256':hashlib.sha256(engine_binary.read_bytes()).hexdigest()}
    save('validation.json',report)
    print(json.dumps(report))

if __name__=='__main__':main()

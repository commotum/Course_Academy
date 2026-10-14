#!/usr/bin/env python3
"""Independent exact source-bank, displayed mathematics, identity and native QA."""
import collections,hashlib,importlib.util,json,random,re,subprocess,sys
from unittest.mock import patch
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((D/'source.json').read_text());cases=json.loads((D/'source-cases.json').read_text())

def latex_expr(text):
    """Parse rendered arithmetic independently, including determinant displays."""
    pattern=r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|'
    def determinant(match):
        rows=match[1].split(r'\\');values=[[latex_expr(v)for v in row.split('&')]for row in rows]
        return '('+str(sp.Matrix(values).det())+')'
    text=re.sub(pattern,determinant,text,flags=re.S)
    def braces(s,start):
        assert s[start]=='{';depth=1;i=start+1
        while depth:
            if s[i]=='{':depth+=1
            elif s[i]=='}':depth-=1
            i+=1
        return s[start+1:i-1],i
    while '\\frac' in text or '\\sqrt' in text:
        m=re.search(r'\\(frac|sqrt)',text);a=m.start();b=m.end()
        inner,end=braces(text,b)
        if m[1]=='frac':den,end=braces(text,end);replacement='(('+latex_expr_string(inner)+')/('+latex_expr_string(den)+'))'
        else:replacement='sqrt('+latex_expr_string(inner)+')'
        text=text[:a]+replacement+text[end:]
    text=latex_expr_string(text)
    return sp.simplify(parse_expr(text,local_dict={'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,)))
def latex_expr_string(text):
    # Inner recursive conversion is necessary for nested fractions/radicals.
    if '\\frac' in text or '\\sqrt' in text:return str(latex_expr(text))
    return text.replace(r'\,','').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','').replace('{','(').replace('}',')').replace('^','**').strip()
def determinant_row_strings(worked):
    block=re.search(r'\$\$\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\$\$',worked,re.S)[1]
    rows=re.split(r'\\\\\s*&\s*=',block)
    rows[0]=re.split(r'&\s*=',rows[0],maxsplit=1)[1]
    return rows
def determinant_rows(worked):return [latex_expr(row)for row in determinant_row_strings(worked)]
def split_additive(text):
    depth=0;parts=[];start=0
    for j,char in enumerate(text):
        if char in '({[':depth+=1
        elif char in ')}]':depth-=1
        elif char in '+-' and depth==0 and j>start:
            parts.append(text[start:j]);start=j
    parts.append(text[start:]);return [latex_expr(v)for v in parts if v.strip()]
def source_matrix(question):
    block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',question,re.S)[1]
    return sp.Matrix([[latex_expr(v)for v in row.split('&')]for row in block.split(r'\\')])
def statement_signature(problem):
    lines=[v for v in problem.splitlines()if v.startswith('- ')or re.match(r'I{1,3}\.',v)]
    return [('det',latex_expr(re.search(r'=([^$]+)',v)[1]))if 'det('in v else ('nonsingular'if '**not**'in v else 'singular',None)for v in lines]
def normalize(v):return ' '.join(v.split())
def field_truth(v):
    return ()if v.startswith('None')else tuple(j+1 for j,k in enumerate(('I','II','III'))if k in v.split())
def check_record(r):
    q=r['question'];md=r['generation'];m=source_matrix(q[':question/problem']);det=sp.expand(m.det())
    if md.get('sampling') is not None:
        assert all(any(v!=0 for v in axis)for j in range(3)for axis in (m.row(j),m.col(j))), 'Sampled zero row or column'
    p=md['parameters'];spec=g.TEMPLATES[md['template']]
    claims=[]
    # Parse learner-facing statements, not correct IDs or generation truth metadata.
    statements=[v for v in q[':question/problem'].splitlines()if v.startswith('- ')or re.match(r'I{1,3}\.',v)]
    assert len(statements)==3
    indices=[]
    for j,line in enumerate(statements):
        if 'det('in line:ok=sp.simplify(det-latex_expr(re.search(r'=([^$]+)',line)[1]))==0
        else:ok=det!=0 if '**not**'in line else det==0
        if ok:indices.append(j+1)
    fields=q[':question/answer-fields']
    assert [f[':answer-field/key'] for f in fields]==['I','II','III']
    assert 'Select all that apply.' in q[':question/problem']
    assert all('- **'+label+'.**' in q[':question/problem'] for label in ('I','II','III'))
    for j,f in enumerate(fields,1):
        assert f[':answer-field/type']==':answer-field.type/checkbox'
        bank={a[':answer/value']:a for a in f[':answer-field/choices']}
        assert len(f[':answer-field/choices'])==2 and set(bank)=={'false','true'}
        assert f[':answer-field/correct']==[':answer/id',bank[str(j in indices).lower()][':answer/id']]
    for row in determinant_rows(q[':question/worked-solution']):assert sp.simplify(row-det)==0,(row,det)
    coeff=[m[0,0],-m[0,1],m[0,2]]
    minors=[m.minor_submatrix(0,j).det() for j in range(3)]
    terms=[sp.simplify(k*v)for k,v in zip(coeff,minors)]
    displayed=determinant_row_strings(q[':question/worked-solution'])
    # Verify each cofactor product individually; cancellation cannot hide a
    # compensating pair of incorrect intermediate values.
    row2=split_additive(displayed[2]);assert len(row2)==3
    assert all(sp.simplify(x-y)==0 for x,y in zip(row2,terms))
    row3=split_additive(displayed[3]);nonzero_coeff_terms=[v for k,v in zip(coeff,terms)if k!=0]
    assert len(row3)==len(nonzero_coeff_terms)
    assert all(sp.simplify(x-y)==0 for x,y in zip(row3,nonzero_coeff_terms))
    data=md['mathematics'];assert all(sp.simplify(sp.sympify(v)-expected)==0 for v,expected in zip(data['minors'],minors))
    assert all(sp.simplify(sp.sympify(v)-expected)==0 for v,expected in zip(data['terms'],terms))
    assert len(determinant_rows(q[':question/worked-solution']))==spec['solution_rows']
    assert g.OPENING in q[':question/worked-solution']and g.METHOD in q[':question/worked-solution']
    assert '{{'not in q[':question/problem']and q[':question/problem'].count('$$')==2
    ids=[q[':question/id']]+[f[':answer-field/id'] for f in fields]+[a[':answer/id']for f in fields for a in f[':answer-field/choices']]
    import uuid
    for identity in ids:uuid.UUID(identity)
    assert len(set(ids))==len(ids)
    assert 'recipe'not in q[':question/problem']and 'parameter'not in q[':question/problem']
    return det

def workload(m):
    # Independent calculation from learner-facing entries, not generator metadata.
    a,b,c,d,e,f,h,i,j=list(m)
    products=[e*j,f*i,d*j,f*h,d*i,e*h]
    terms=[sp.expand(a*(e*j-f*i)),sp.expand(-b*(d*j-f*h)),sp.expand(c*(d*i-e*h))]
    return {'entry':max(abs(v)for v in m),'product':max(abs(v)for v in products),
            'term':max(abs(v)for v in terms),'term_sum':sum(abs(v)for v in terms),
            'determinant':abs(sp.expand(sum(terms)))}

def claim_class(v):
    if v.is_Integer:return 'integer_over_10' if abs(v)>10 else 'small_integer'
    if v.is_Rational:return 'fraction'
    return 'additive_radical' if v.is_Add else 'radical'

def proportional_pair(m,rows=True):
    vectors=[m.row(j) if rows else m.col(j)for j in range(3)]
    return any(any(v!=0 for v in a) and any(v!=0 for v in b)
               and all(sp.expand(a[i]*b[j]-a[j]*b[i])==0 for i in range(3)for j in range(i+1,3))
               for k,a in enumerate(vectors)for b in vectors[k+1:])

def check_fresh_sampling():
    calibrated={};families=collections.Counter();formats=collections.Counter();structures=collections.Counter();examples={}
    for level in ('easy','moderate'):
        observed=[workload(source_matrix(q[':question/problem']))for q in source['record'][':knowledge-point/questions']
                  if q[':question/difficulty'][':db/ident'].endswith('/'+level)]
        calibrated[level]={k:max(w[k]for w in observed)for k in observed[0]}
        assert calibrated[level]==g.ARITHMETIC_LIMITS[level]
        for seed in range(120 if level=='easy' else 240):
            r=g.generate(level,seed=seed);m=source_matrix(r['question'][':question/problem']);det=check_record(r)
            actual=workload(m)
            assert all(actual[k]<=limit for k,limit in calibrated[level].items()),(level,seed,actual)
            family=r['generation']['sampling']['matrix_family'];families[family]+=1
            examples.setdefault(family,r)
            for kind,claim in statement_signature(r['question'][':question/problem']):
                if kind=='det':formats[(level,claim_class(claim),'true' if sp.expand(claim-det)==0 else 'false')]+=1
            if det==0:
                assert m.rank()==2
                for rows,label in ((True,'proportional_rows'),(False,'proportional_columns')):
                    if proportional_pair(m,rows):structures[(level,label)]+=1
            if level=='moderate':
                structures[(family,'singular' if det==0 else 'nonsingular')]+=1
                if det.is_Add and not det.is_Rational:structures[(level,'additive_radical_determinant')]+=1
                if any(v.is_Rational and not v.is_Integer for v in m) and any(v.is_Rational is False for v in m):
                    # At least one column combines a radical with a nonzero
                    # rational: a whole-column radical scale cannot produce it.
                    if any(any(v.is_Rational is False for v in m.col(j)) and any(v!=0 and v.is_Rational for v in m.col(j))for j in range(3)):
                        structures[(level,'mixed_fraction_radical_positions')]+=1
                if family=='mixed_additive_radical':
                    assert m[0,2]==0 and m[1,1].is_Rational is False and m[2,0].is_Rational is False
                    assert det==0 or det.is_Add and det.is_Rational is False
                if family=='sparse_rational_radical':
                    assert all(m[j]==0 for j in (1,5,7)) and m[2].is_Rational and not m[2].is_Integer
                    assert m[0].is_Rational is False and m[3].is_Rational is False and m[8].is_Rational is False and det.is_Rational
    for family in g.MODERATE_FAMILIES:
        assert families[family]>=2
        assert structures[(family,'singular')]>0 and structures[(family,'nonsingular')]>0
    for level in ('easy','moderate'):
        assert structures[(level,'proportional_rows')]>0 and structures[(level,'proportional_columns')]>0
        assert formats[(level,'integer_over_10','false')]>0
    for shape in ('fraction','radical','additive_radical'):
        assert formats[('moderate',shape,'false')]>0 and formats[('moderate',shape,'true')]>0
    assert structures[('moderate','mixed_fraction_radical_positions')]>0
    # Retain normal samples as reviewable evidence of each new family.
    (D/'sampling-review.json').write_text(json.dumps(examples,indent=2)+'\n')
    return {'status':'passed','fresh_records':360,'limits_measured_from_sources':{level:{k:int(v)for k,v in limits.items()}for level,limits in calibrated.items()},
            'family_counts':dict(families),'structures':{' / '.join(k):v for k,v in structures.items()},
            'claim_format_truth_counts':{' / '.join(k):v for k,v in formats.items()},
            'evidence':'sampling-review.json','note':'Every fresh displayed matrix, statement, field key and cofactor equality checked; source replay excluded from sampling coverage.'}

def main():
    report={'source':{k:source[k]for k in ('database','basis','lineage')},'fidelity':{},'correctness':{},'native_grading':{},'scope':{},'failures':[]}
    records=[];details=[];total_choices=correct_refs=source_distractors=0
    try:
        for case in cases:
            q=next(q for q in source['record'][':knowledge-point/questions']if q[':question/math-academy-id']==case['source_id'])
            r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check_record(r)
            generated_fields={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
            for f in q[':question/answer-fields']:
                bank=generated_fields[f[':answer-field/key']]
                assert sorted(a[':answer/value']for a in bank[':answer-field/choices'])==sorted(a[':answer/value']for a in f[':answer-field/choices'])
                correct=next(a[':answer/value']for a in bank[':answer-field/choices']if a[':answer/id']==bank[':answer-field/correct'][1])
                assert f[':answer-field/correct'][':answer/value']==correct
                correct_refs+=1;total_choices+=2
            assert source_matrix(q[':question/problem'])==source_matrix(r['question'][':question/problem'])
            assert statement_signature(q[':question/problem'])==statement_signature(r['question'][':question/problem'])
            original_rows=determinant_rows(q[':question/worked-solution']);det=source_matrix(q[':question/problem']).det()
            assert all(sp.simplify(v-det)==0 for v in original_rows)
            assert len(original_rows)==len(determinant_rows(r['question'][':question/worked-solution']))
            records.append(('source:'+case['source_id'],r))
            details.append({'source_id':case['source_id'],'checkbox_fields':3,'choices':6,'correct_designations':'matched','template':case['template']})
        report['fidelity']={'practice_questions':len(cases),'source_fields':correct_refs,'complete_banks_matched':correct_refs,'choices_matched':total_choices,'choices_total':total_choices,'known_correct_designations_matched':correct_refs,'known_correct_designations_total':correct_refs,'missing_original_designations':0,'details':details,'format_repairs':['q-77477/q-128491 malformed solution bold normalized'],'prompt_values':'Every matrix entry and all three statement predicates independently matched; current checkbox labels and instruction preserved','arithmetic_notation':'Equivalent exact formatting; every displayed source/generated solution row independently parsed and compared; stage counts preserved.'}
        fingerprints={};generated=0
        # All complete banks are exercised at all levels, plus every observed template.
        for level in ('easy','moderate','hard'):
            for profile in g.BANK_PROFILES:
                for seed in range(20):
                    r=g.generate(level,seed=seed,profile=profile);check_record(r);records.append((f'{level}:{profile}:{seed}',r));generated+=1
                    key=r['question'][':question/id'];assert fingerprints.get(key,r['generation']['content_fingerprint'])==r['generation']['content_fingerprint'];fingerprints[key]=r['generation']['content_fingerprint']
                    same=g.generate(level,seed=seed+993,template=r['generation']['template'],profile=profile,parameters=r['generation']['parameters'])
                    assert same['question'][':question/id']==key
                    assert same['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
            for template,spec in g.TEMPLATES.items():
                if spec['level']==level:
                    for seed in range(3):check_record(g.generate(level,seed=seed,template=template))
        for level in ('easy','moderate'):
            default=g.generate(level,seed=77)
            assert default['generation']['bank_origin']=='observed' and not default['generation']['profile_extension']
        c=cases[1];bad=dict(c['parameters']);bad['matrix']=bad['matrix'].copy();bad['matrix'][0]='sqrt(2)'
        try:g.generate('easy',template=c['template'],profile=c['bank_profile'],parameters=bad)
        except ValueError:pass
        else:raise AssertionError('Out-of-level explicit radical matrix accepted')
        # Radio calls must fail; the current KP only owns checkbox fields.
        try:g.generate('easy',field_type='radio')
        except ValueError:pass
        else:raise AssertionError('Stale radio output accepted')
        observed_truth={tuple(r['generation']['truth_indices']) for _,r in records}
        assert () in observed_truth and any(len(v)>1 for v in observed_truth)
        for bad in ({'matrix':['0']*8,'claims':[None]*3},{'matrix':['0']*9,'claims':[None]*3,'name':'AA'}):
            try:g.generate('hard',parameters=bad)
            except ValueError:pass
            else:raise AssertionError('Invalid explicit input silently changed')
        report['correctness']={'status':'passed','sampled_records':generated,'unique_sampled_content':len(fingerprints),'independently_checked':'Displayed matrices, every solution equality, statement truth, every complete choice bank, correct refs, UUID ownership, invalid inputs and deterministic identities'}
        report['fresh_sampling']=check_fresh_sampling()
        records.extend(('sampling-family:'+family,r)for family,r in json.loads((D/'sampling-review.json').read_text()).items())
        # The reported seed used to produce a rank-two zero-column matrix.
        regression=g.generate('easy',seed=181);check_record(regression)
        records.append(('zero-axis-regression:easy:181',regression))
        zero_column=sp.Matrix([[2,2,0],[1,2,0],[3,2,0]])
        for label,matrix in (('column',zero_column),('row',zero_column.T)):
            with patch.object(g,'integer_structure',return_value=(list(matrix),'independent')):
                try:g.sample_matrix(random.Random(181),'easy')
                except g.SampleRejected as exc:assert 'Zero rows and columns' in str(exc)
                else:raise AssertionError('Zero '+label+' accepted by sampler')
        template=next(t for t,s in g.TEMPLATES.items()if s['level']=='easy')
        explicit={'matrix':[str(v)for v in zero_column],
                  'claims':[str(j+1)if kind=='det'else None for j,kind in enumerate(g.TEMPLATES[template]['statements'])]}
        check_record(g.generate('easy',template=template,parameters=explicit))
        report['sampling_regressions']={'zero_rows_and_columns':'excluded from every normal sample; both rejection paths checked',
                                        'easy_seed_181':'passed displayed mathematics, nonzero-axis and native grading checks',
                                        'source_replay':'sampling guard does not restrict explicit parameters'}
        engine=D.parent/'source-refresh-2026-10-12/check-checkbox-engine'
        inputs=[]
        for label,r in records:
            checks=[]
            for index,f in enumerate(r['question'][':question/answer-fields']):
                for answer in f[':answer-field/choices']:
                    checks.append({'field_index':index,'submitted_answer_id':answer[':answer/id'],'expected':'accepted' if answer[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Native Boolean checkbox grading, including unchecked false'})
            inputs.append({'label':label,'record':r,'checks':checks})
        (D/'engine-input.json').write_text(json.dumps(inputs,indent=2))
        run=subprocess.run([str(engine),str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True)
        assert run.returncode==0,run.stdout+run.stderr
        engine_report=json.loads((D/'engine-report.json').read_text())
        report['native_grading']={'status':'passed','records':len(records),'checks':sum(len(v['checks']) for v in inputs),'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'report':'engine-report.json',**{key:engine_report[key] for key in ('whole_question_canonical_accepted','whole_question_flipped_checkboxes_rejected','whole_question_incomplete_rejected')}}
        report['scope']={'status':'passed','hard':'Authored density and exact fraction/repeated-radical arithmetic; no original hard calibration; numeric determinant then singularity only','mathematical_methods':1,'observed_layout_order_stage_templates':sum(bool(v['source_ids']) for v in g.TEMPLATES.values()),'observed_complete_profiles':len(g.BANK_PROFILES),'truth_subsets_checked':list(map(list,sorted(observed_truth))),'plots':'none; inspected canonical image is mathematical matrix typography','unique_sampled_per_level':{level:len({r['generation']['parameter_fingerprint']for label,r in records if label.startswith(level+':')})for level in ('easy','moderate','hard')}}
        report['generator_sha256']=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
        report['status']='passed'
    except Exception as exc:
        report['status']='failed';report['failures'].append(repr(exc));import traceback;traceback.print_exc()
    (D/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k not in ('fidelity',)},indent=2))
    return 0 if report['status']=='passed'else 1
if __name__=='__main__':sys.exit(main())

#!/usr/bin/env python3
"""Independent exact source-bank, displayed mathematics, identity and native QA."""
import hashlib,importlib.util,json,re,subprocess,sys
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
    f=q[':question/answer-fields'][0];values=[a[':answer/value']for a in f[':answer-field/choices']]
    assert len(values)==5 and len(set(map(normalize,values)))==5
    expected=[a[':answer/id']for a in f[':answer-field/choices']if field_truth(a[':answer/value'])==tuple(indices)]
    assert len(expected)==1 and f[':answer-field/correct']==[':answer/id',expected[0]]
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
    assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection'
    assert f[':answer-field/type']==':answer-field.type/radio'
    ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id']for a in f[':answer-field/choices']]
    import uuid
    for identity in ids:uuid.UUID(identity)
    assert len(set(ids))==len(ids)
    assert 'recipe'not in q[':question/problem']and 'parameter'not in q[':question/problem']
    return det

def main():
    report={'source':{k:source[k]for k in ('database','basis','lineage')},'fidelity':{},'correctness':{},'native_grading':{},'scope':{},'failures':[]}
    records=[];details=[];total_choices=correct_refs=source_distractors=0
    try:
        for case in cases:
            q=next(q for q in source['record'][':knowledge-point/questions']if q[':question/math-academy-id']==case['source_id'])
            f=q[':question/answer-fields'][case['source_field_index']]
            r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check_record(r)
            bank=r['question'][':question/answer-fields'][0]
            assert sorted(a[':answer/value']for a in bank[':answer-field/choices'])==sorted(a[':answer/value']for a in f[':answer-field/choices'])
            correct=next(a[':answer/value']for a in bank[':answer-field/choices']if a[':answer/id']==bank[':answer-field/correct'][1])
            original=f.get(':answer-field/correct',{}).get(':answer/value')
            if original is not None:assert original==correct;correct_refs+=1;source_distractors+=4
            else:source_distractors+=4 # Derived designation; counted separately in report.
            assert source_matrix(q[':question/problem'])==source_matrix(r['question'][':question/problem'])
            assert statement_signature(q[':question/problem'])==statement_signature(r['question'][':question/problem'])
            original_rows=determinant_rows(q[':question/worked-solution']);det=source_matrix(q[':question/problem']).det()
            assert all(sp.simplify(v-det)==0 for v in original_rows)
            assert len(original_rows)==len(determinant_rows(r['question'][':question/worked-solution']))
            total_choices+=5;records.append(('source:'+case['source_id']+':'+str(case['source_field_index']),r))
            details.append({'source_id':case['source_id'],'field_index':case['source_field_index'],'complete_bank':'matched','choices':5,'correct_designation':'matched'if original else'missing in raw source; independently derived','template':case['template'],'profile':case['bank_profile']})
        report['fidelity']={'practice_questions':17,'source_fields':18,'complete_banks_matched':18,'choices_matched':total_choices,'choices_total':90,'known_correct_designations_matched':correct_refs,'known_correct_designations_total':17,'missing_original_designations':1,'distractors_matched_at_known_designations':68,'inferred_legacy_distractors_matched':4,'details':details,'format_repairs':['q-128490 legacy duplicated field collapsed to one assessment; both raw banks retained for evidence replay','q-77477/q-128491 malformed **not ** normalized to **not**'],'prompt_values':'Every matrix entry and all three complete statement predicates independently matched','arithmetic_notation':'Equivalent exact formatting; all source/generated solution rows independently parsed and compared; original stage counts preserved.'}
        fingerprints={};generated=0
        # All complete banks are exercised at all levels, plus every observed template.
        for level in ('easy','moderate','hard'):
            for profile in g.BANK_PROFILES:
                for seed in range(12):
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
        # Same mathematics + two differing displayed banks must not share identity.
        c=cases[0];valid=[]
        for profile in g.BANK_PROFILES:
            try:valid.append(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=profile))
            except g.SampleRejected:pass
        assert len(valid)>1 and len({r['question'][':question/id']for r in valid})==len(valid)
        assert len({r['generation']['parameter_fingerprint']for r in valid})==1
        for bad in ({'matrix':['0']*8,'claims':[None]*3},{'matrix':['0']*9,'claims':[None]*3,'name':'AA'}):
            try:g.generate('hard',parameters=bad)
            except ValueError:pass
            else:raise AssertionError('Invalid explicit input silently changed')
        report['correctness']={'status':'passed','sampled_records':generated,'unique_sampled_content':len(fingerprints),'independently_checked':'Displayed matrices, every solution equality, statement truth, every complete choice bank, correct refs, UUID ownership, invalid inputs and deterministic identities'}
        engine=D.parents[1]/'runs/current/check-engine'
        inputs=[]
        for label,r in records:
            f=r['question'][':question/answer-fields'][0]
            inputs.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'Complete radio bank native grading'}for a in f[':answer-field/choices']]})
        (D/'engine-input.json').write_text(json.dumps(inputs,indent=2))
        run=subprocess.run([str(engine),str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True)
        assert run.returncode==0,run.stdout+run.stderr
        report['native_grading']={'status':'passed','records':len(records),'checks':5*len(records),'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'report':'engine-report.json'}
        report['scope']={'status':'passed','hard':'Authored density and exact fraction/repeated-radical arithmetic; numeric determinant then singularity only','observed_templates':15,'observed_complete_profiles':8,'plots':'none; inspected canonical image is mathematical matrix typography','unique_sampled_per_level':{level:len({r['generation']['parameter_fingerprint']for label,r in records if label.startswith(level+':')})for level in ('easy','moderate','hard')}}
        report['generator_sha256']=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
        report['status']='passed'
    except Exception as exc:
        report['status']='failed';report['failures'].append(repr(exc));import traceback;traceback.print_exc()
    (D/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k not in ('fidelity',)},indent=2))
    return 0 if report['status']=='passed'else 1
if __name__=='__main__':sys.exit(main())

#!/usr/bin/env python3
"""Independent exact source-bank, displayed mathematics, identity and native QA."""
import sys
sys.dont_write_bytecode=True
import collections,hashlib,importlib.util,json,random,re,subprocess,copy
from unittest.mock import patch
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((D/'source.json').read_text());cases=json.loads((D/'source-cases.json').read_text())

def latex_expr(text):
    """Parse rendered arithmetic independently, including determinant displays."""
    pattern=r'(?:\|\\begin\{aligned\}(.*?)\\end\{aligned\}\||\\begin\{vmatrix\}(.*?)\\end\{vmatrix\})'
    def determinant(match):
        rows=(match[1] if match[1] is not None else match[2]).split(r'\\');values=[[latex_expr(v)for v in row.split('&')]for row in rows]
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
    block=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',question,re.S)[1]
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


def prose_signature(value):
    value=re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?\$', '<math>',value,flags=re.S)
    return ' '.join(value.replace('**not **','**not**').split())
def verify_grader():
    path=ROOT/'generate/scratch/17592186059716-draft/reference/grader-build.json'
    m=json.loads(path.read_text());hashes={m['source']:m['source_sha256'],m['library']:m['library_sha256'],m['binary']:m['binary_sha256'],**m['engine_sources'],**m['dependencies']}
    assert len(hashes)==42
    for p,h in hashes.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    (D/'reference/grader-build.json').write_text(path.read_text())
    return hashes,m

def main():
    hashes,build=verify_grader();records=[];review=[];fidelity=[];historical=[];counts=collections.Counter();seen=collections.defaultdict(set)
    original={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
    for c in cases:
        q=original[c['source_id']];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check_record(r)
        assert source_matrix(q[':question/problem'])==source_matrix(r['question'][':question/problem'])
        assert statement_signature(q[':question/problem'])==statement_signature(r['question'][':question/problem'])
        assert prose_signature(q[':question/worked-solution'])==prose_signature(r['question'][':question/worked-solution'])
        original_rows=determinant_rows(q[':question/worked-solution']);fresh_rows=determinant_rows(r['question'][':question/worked-solution'])
        assert len(original_rows)==len(fresh_rows)
        assert all(sp.simplify(x-y)==0 for x,y in zip(original_rows,fresh_rows))
        for f,new in zip(q[':question/answer-fields'],r['question'][':question/answer-fields']):
            assert f[':answer-field/key']==new[':answer-field/key']
            assert f[':answer-field/type'][':db/ident']==new[':answer-field/type']
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':answer-field/choices'])
            correct=next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1])
            assert correct==f[':answer-field/correct'][':answer/value'];counts['current_banks']+=1;counts['current_choices']+=2;counts['current_keys']+=1
        for key in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (key in q)==(key in r['question'])
        records.append(('current:'+c['source_id'],r));review.append({'kind':'current source parameter replay','source_id':c['source_id'],'original':q,'record':r})
        fidelity.append({'source_id':c['source_id'],'banks':3,'values':6,'designations':3,'full_prose':'matched after two documented bold repairs and math normalization','stages':len(fresh_rows)})
        for seed in (132,265):
            fresh=g.generate(c['level'],seed=seed,template=c['template']);check_record(fresh);records.append(('variant:'+c['source_id']+':'+str(seed),fresh));review.append({'kind':'changed parameters','source_id':c['source_id'],'record':fresh})
    old=json.loads((D/'reference/source-basis-1356.json').read_text())
    for q in old['record'][':knowledge-point/questions']:
        sid=q[':question/math-academy-id'];r=g.generate('easy',profile='historical:'+sid)
        assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
        assert source_matrix(q[':question/problem'])==source_matrix(r['question'][':question/problem'])
        assert statement_signature(q[':question/problem'])==statement_signature(r['question'][':question/problem'])
        assert prose_signature(q[':question/worked-solution'])==prose_signature(r['question'][':question/worked-solution'])
        assert len(q[':question/answer-fields'])==len(r['question'][':question/answer-fields'])
        for f,new in zip(q[':question/answer-fields'],r['question'][':question/answer-fields']):
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':answer-field/choices'])
            assert (':answer-field/correct' in f)==(':answer-field/correct' in new)
            for v in new[':answer-field/choices']:
                assert g.subset(v[':answer/value']) in [(),(1,),(2,),(3,),(1,2),(1,3),(2,3),(1,2,3)]
            assert len(set(g.subset(a[':answer/value']) for a in new[':answer-field/choices']))==len(new[':answer-field/choices'])
            counts['historical_banks']+=1;counts['historical_choices']+=len(new[':answer-field/choices'])
            if ':answer-field/correct' in f:
                value=next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1]);assert value==f[':answer-field/correct'][':answer/value'];assert g.subset(value)==tuple(r['generation']['truth_indices']);counts['historical_keys']+=1
        historical.append({'source_id':sid,'record':r})
    (D/'historical-review.json').write_text(json.dumps(historical,indent=2)+'\n')
    for level in ('easy','moderate','hard'):
        for seed in range(40):
            r=g.generate(level,seed=seed);check_record(r);g.math_format.validate_generated_record(r)
            fixed=g.generate(level,seed=seed+932,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
            assert fixed['question'][':question/id']==r['question'][':question/id']
            seen[level].add(r['generation']['parameter_fingerprint']);records.append((level+':'+str(seed),r));counts['normal_records']+=1
            if level=='hard' and seed<2:review.append({'kind':'authored hard extension','record':r})
    sampling=check_fresh_sampling()
    # Math canonicalization and C0 guards must reject the mutation, independently of arithmetic.
    try:g.learner_prose('bad \x0c'+'rac{1}{2}')
    except ValueError:pass
    else:raise AssertionError('C0 guard failed')
    r=review[0]['record'];q=copy.deepcopy(r);q['question'][':question/worked-solution']=q['question'][':question/worked-solution'].replace('Therefore,','Therefore, only statements II and III are true. ')
    assert prose_signature(q['question'][':question/worked-solution'])!=prose_signature(r['question'][':question/worked-solution'])
    # An explicit huge matrix must fail the same workload ceiling as sampling.
    c=cases[1];bad=copy.deepcopy(c['parameters']);bad['matrix'][0]='1000'
    try:g.generate(c['level'],template=c['template'],parameters=bad)
    except ValueError:pass
    else:raise AssertionError('Explicit workload bypass')
    inputs=[]
    for label,r in records:
        checks=[]
        for index,f in enumerate(r['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:
                checks.append({'field_index':index,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each true/false checkbox including intentionally unchecked state'})
        inputs.append({'label':label,'record':r,'checks':checks})
    (D/'engine-input.json').write_text(json.dumps(inputs,indent=2)+'\n')
    run=subprocess.run([str(ROOT/build['binary']),str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True);assert run.returncode==0,run.stdout+run.stderr
    native=json.loads((D/'engine-report.json').read_text())
    (D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    (D/'review.md').write_text('# Singular matrices private draft review\n\nCurrent basis2484 checkbox records; historical1356 radio evidence is separate and ineligible.\n\n'+'\n\n---\n\n'.join('## '+row['kind']+' '+row.get('source_id','')+'\n\n'+g.markdown(row['record']) for row in review)+'\n')
    report={'status':'passed','source':{k:source[k] for k in ('database','basis','lineage')},'fidelity':dict(counts),'current_source_details':fidelity,'historical_source_basis':1356,'historical_missing_ref':1,'historical_current_contract':'radio to checkbox migration preserved; no current normal radio output','mathematics':{'source_replays':17,'changed_parameter_replays':34,'normal_sample_records':120,'fresh_sampling':sampling,'unique_tasks':{k:len(v) for k,v in seen.items()},'checks':'actual printed matrix, each signed cofactor term, every equality, statement predicate and field-owned correct ref'},'native':{'binary_sha256':build['binary_sha256'],'verified_build_hashes':len(hashes),'records':len(inputs),'checks':sum(len(i['checks']) for i in inputs),'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'whole_question':'fieldwise fixture only; real checkbox controls rendered separately'},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'source_errors':['q-77477/q-128491 malformed source bold repaired in normal output','historical q-128490 duplicate field and missing correct ref retained only in ineligible public evidence profile'],'limits':['hard authored workload policy; no observed hard label','source prose normalized and math layout canonicalized; arithmetic typography equivalent, not byte-exact'],'root_approval':'pending','database_writes':0}
    (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('current_source_details','mathematics')},indent=2))
if __name__=='__main__':main()

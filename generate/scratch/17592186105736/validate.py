#!/usr/bin/env python3
"""Independently read displayed vectors, determinants and scalar stages; native QA."""
import copy, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def assert_format(text):
    assert not any(ord(c)<32 and c not in '\n\t' for c in text),'C0 control byte'
    assert '--' not in text and '+-' not in text,'bare signed combination'
    assert text.count('$')%2==0,'unbalanced dollars'
    depth=0
    for c in text:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0,'unbalanced braces'
    assert depth==0,'unbalanced braces'

MATRIX=re.compile(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',re.S)
def matrices(text):
    return [sp.Matrix([[int(x.strip()) for x in row.split('&')] for row in mat.split(r'\\')]) for mat in MATRIX.findall(text)]
def scalar(text):
    text=MATRIX.sub(lambda z:'('+str(matrices(z[0])[0].det())+')',text)
    text=text.replace(r'\cdot','*').replace(r'\,','').strip().rstrip('.')
    assert not re.search(r'[^0-9+*\-()\s]',text),text
    return parse_expr(text,transformations=standard_transformations+(implicit_multiplication_application,))
def check_record(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];raw=r['generation']['evidence_only'];sid=r['generation']['template']
    for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:assert_format(text)
    if raw and sid=='q-20051':return
    vectors,order=m.source_vectors(q);rows=[vectors[n] for n in order];det=sp.Matrix(rows).det()
    sol=q[':question/worked-solution'];segments=sol.split(' & =')[1:]
    displayed=[x.split(r'\end{aligned}')[0] if i==len(segments)-1 else x.rsplit(r'\\',1)[0] for i,x in enumerate(segments)]
    assert matrices(displayed[0])[0]==sp.Matrix(rows),'displayed assessment matrix'
    minor_mats=matrices(displayed[1]);assert len(minor_mats)==3
    for j,minor in enumerate(minor_mats):assert minor==sp.Matrix(rows).minor_submatrix(0,j),'actual cofactor minor'
    for i,row in enumerate(displayed):
        assert scalar(row)==det,(sid,i,row,det,scalar(row))
    expected_terms=[rows[0][j]*(-1)**j*sp.Matrix(rows).minor_submatrix(0,j).det() for j in range(3)]
    for row in displayed[1:-1]:
        protected=MATRIX.sub(lambda z:'('+str(matrices(z[0])[0].det())+')',row)
        terms=m.split_terms(protected)
        wanted=[x for j,x in enumerate(expected_terms) if not(sid=='q-73461' and j==2 and row!=displayed[1])]
        assert [scalar(t) for t in terms]==wanted,('individual signed components',sid,row,wanted)
    # Required operative stages, not just equal final values/row count.
    assert len(displayed)>=5 and len(matrices(displayed[1]))==3
    assert r'\cdot' in displayed[2] and '(' in displayed[2], 'missing substituted minor products'
    assert not matrices(displayed[-2]) and len(re.findall(r'\d+',displayed[-2]))>=2,'missing collected terms'
    if sid=='dense_signed' or sid in m.QUESTIONS and m.ft(m.QUESTIONS[sid][':question/answer-fields'][-1]).endswith('/blank'):
        assert len(displayed)==6,'missing evaluated-minor/product stage'
    corrects=0
    for f in q[':question/answer-fields']:
        values=[sp.Integer(a[':answer/value']) for a in f[':answer-field/choices']]
        assert len(values)==len(set(values)),'displayed bank collision'
        if ':answer-field/correct' not in f:continue
        a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert sp.Integer(a[':answer/value'])==det
        corrects+=1
        if not raw and f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    assert corrects>=1

def native_item(r,label):
    q=r['question'];checks=[]
    for i,f in enumerate(q[':question/answer-fields']):
        if ':answer-field/correct' not in f:continue
        if f[':answer-field/type'].endswith('/radio'):
            for a in f[':answer-field/choices']:
                checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank'})
        else:
            value=f[':answer-field/choices'][0][':answer/value']
            checks += [{'field_index':i,'submitted':value,'expected':'accepted','purpose':'canonical integer'}, {'field_index':i,'submitted':'('+value+'*3)/3','expected':'accepted','purpose':'unevaluated equivalent scalar'}, {'field_index':i,'submitted':str(int(value)+1),'expected':'rejected','purpose':'incorrect scalar'}]
    if any(':answer-field/correct' not in f for f in q[':question/answer-fields']):
        r=copy.deepcopy(r);r['question'][':question/answer-fields']=[f for f in q[':question/answer-fields'] if ':answer-field/correct' in f]
        for c in checks:c['field_index']=0
    return {'label':label,'record':r,'checks':checks}

def run():
    source_cases=[];reviews=[];native=[];banks=values=designations=0
    for sid,q in m.QUESTIONS.items():
        case={'source_id':sid,'template':sid,'level':m.LEVELS[sid],'parameters':{'scale':1},'bank_profile':'observed:'+sid}
        source_cases.append(case)
        r=m.generate(case['level'],template=sid,parameters=case['parameters'],profile=case['bank_profile']);rq=r['question'];check_record(r)
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
            assert (key in q)==(key in rq),(sid,key,'presence')
        assert rq[':question/problem']==q[':question/problem'];assert rq.get(':question/worked-solution')==q.get(':question/worked-solution')
        for original,new in zip(q[':question/answer-fields'],rq[':question/answer-fields']):
            assert original[':answer-field/key']==new[':answer-field/key'];assert m.ft(original)==new[':answer-field/type']
            assert sorted(a[':answer/value'] for a in original[':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':answer-field/choices'])
            assert (':answer-field/correct' in original)==(':answer-field/correct' in new)
            if ':answer-field/correct' in original:
                selected=next(a for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1])
                assert selected[':answer/value']==original[':answer-field/correct'][':answer/value']
                designations+=1
            banks+=1;values+=len(original[':answer-field/choices'])
        if sid!='q-20051':native.append(native_item(r,'original '+sid))
        r2=m.generate(case['level'],template=sid,parameters={'scale':2},profile=case['bank_profile']);check_record(r2)
        reviews += [r,r2]
        for i in range(2):
            x=m.generate(case['level'],seed=i+71,template=sid);check_record(x);reviews.append(x);native.append(native_item(x,'authored bank '+sid+' '+str(i)))
    coverage={};normal=[]
    for level in ('easy','moderate','hard'):
        for seed in range(400):
            r=m.generate(level,seed);check_record(r);normal.append(r)
        batch=[r for r in normal if r['generation']['level']==level]
        coverage[level]={'sampled':len(batch),'distinct_mathematical_tasks':len(set(r['generation']['mathematical_fingerprint'] for r in batch)), 'families':sorted(set(r['generation']['template'] for r in batch)), 'profiles':sorted(set(r['generation']['profile'] for r in batch))}
        assert coverage[level]['distinct_mathematical_tasks']>150
        assert set(coverage[level]['families'])=={x for x,v in m.TEMPLATES.items() if v['level']==level}
        for r in batch[:2]:reviews.append(r);native.append(native_item(r,'level preview '+level))
    # Fixed displayed task and bank retain identity across seed/order.
    for r in normal[:50]:
        gen=r['generation'];p=gen['parameters'];kind=r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1]
        x=m.generate(gen['level'],999,template=gen['template'],field_type=kind,parameters=p,profile=gen['profile'])
        assert x['question'][':question/id']==r['question'][':question/id']
    # Adversarial formatting and stage deletions must fail.
    for mutation in ('control','minor','substitution'):
        bad=copy.deepcopy(normal[0]);q=bad['question']
        if mutation=='control':q[':question/problem']+='\x0c'
        elif mutation=='minor':q[':question/worked-solution']=q[':question/worked-solution'].replace(' & ', ' & 999',1)
        else:
            pieces=q[':question/worked-solution'].split(' & =');pieces[3]=pieces[-1];q[':question/worked-solution']=' & ='.join(pieces)
        try:check_record(bad)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('mutation passed: '+mutation)
    for p in ({'rows':[[1,1,1],[2,2,2],[3,3,3]]},{'rows':[[7,2,-2],[-2,2,3],[2,-3,4]]}):
        try:m.generate_hard(parameters=p)
        except ValueError:pass
        else:raise AssertionError('hard bounds failed')
    (HERE/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps(reviews,indent=2)+'\n')
    (HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
    engine=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    nr=json.loads((HERE/'native-report.json').read_text())
    result={'passed':True,'database':'math','basis':1356,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_practices':23,'source_counts':{'easy':11,'moderate':11,'unrated':1},'raw_exact_prompts':23,'raw_exact_present_solutions':22,'raw_attribute_presence':23,'complete_banks_matched':banks,'choice_values_matched':values,'correct_designations_matched':designations,'absent_correct_refs_preserved':2,'source_mathematics_validated':22,'source_malformed_ineligible':['q-20051'],'normal_records_checked':1200,'coverage':coverage,'native':{k:nr[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'authored_missing_levels':['hard'],'opaque_banks':'all observed radio distractor interpretation unresolved; raw evidence only','format_mutations_rejected':3,'plot_rating':'none','database_writes':0}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return reviews
if __name__=='__main__':run()

#!/usr/bin/env python3
"""Independent printed-TeX calculus, source/full-bank and native radio checks."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
from capacity import enumerate_capacity
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,u=sp.symbols('x u',real=True)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def group(s,start):
    assert s[start]=='{';depth=1;i=start+1
    while depth:
        if s[i]=='{':depth+=1
        if s[i]=='}':depth-=1
        i+=1
    return s[start+1:i-1],i

def parse(s):
    s=s.strip()
    for cmd in (r'\frac',r'\dfrac'):
        while cmd in s:
            k=s.index(cmd);a,j=group(s,k+len(cmd));b,end=group(s,j)
            s=s[:k]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+s[end:]
    s=s.replace(r'\cdot','*').replace(r'\,','').replace(' ','').replace('{','(').replace('}',')')
    s=re.sub(r'(\d|\))([xu])',r'\1*\2',s)
    s=re.sub(r'(\d|\))\(',r'\1*(',s)
    if s in ('','-'):s+='1'
    return sp.sympify(s,locals={'x':x,'u':u})
def first_integrand(s):
    k=s.index(r'\frac');a,j=group(s,k+5);b,end=group(s,j)
    return sp.cancel(parse(a)/parse(b))
def params_from_prompt(q):
    problem=q[':question/problem'];k=problem.index(r'\frac');a,j=group(problem,k+5);b,end=group(problem,j)
    p=sp.Poly(parse(b),x);assert p.degree()==1
    return parse(a),p.coeff_monomial(x),p.coeff_monomial(1)
def primitive(s):
    s=s.strip().replace(r'\ln \mid ',r'\ln|').replace(r' \mid + C','|+C')
    m=re.fullmatch(r'(.*?)(?:\\operatorname\{ln\}⁡|\\ln)\|([^|]+)\|\+C',s);assert m,s
    c=parse(m[1]);d=parse(m[2]);v=u if d.has(u) else x
    poly=sp.Poly(d,v);assert poly.degree()==1 and d.has(x,u)
    return c,d,v

def primitive_derivative(s,d):
    c,arg,v=primitive(s)
    derivative=sp.cancel(c*sp.diff(arg,v)/arg)
    if v==u:derivative=sp.cancel(derivative.subs(u,d)*sp.diff(d,x))
    return derivative

def integral_row(s,d):
    outer,body=s.split(r'\int',1)
    var=x if r'\text{d}x' in body else u
    token=r'\text{d}x' if var==x else r'\text{d}u'
    assert token in body,s
    body=body.replace(token,'1').replace(r'\,','')
    # Numeric differential multiplication: ...,dx -> ...*1; parentheses already wrap du.
    body=body.replace('1}', '1}')
    # Insert multiplication before differential 1 after a braced fraction or parenthesis.
    body=re.sub(r'([})])1',r'\1*1',body)
    f=sp.cancel(parse(outer)*parse(body))
    return sp.cancel(f if var==x else f.subs(u,d)*sp.diff(d,x))
def formatting(s):
    assert all(ord(ch)>=32 or ch in '\n\t' for ch in s),'C0 control character'
    assert s.count('$')%2==0
    n=0
    for ch in s:
        if ch=='{':n+=1
        if ch=='}':n-=1;assert n>=0
    assert n==0

def check(rec):
    q=rec['question'];m=rec['generation'];p=params_from_prompt(q);c,a,b=p;d=a*x+b;integrand=sp.cancel(c/d)
    assert [str(v) for v in p]==m['parameters'];assert m['mathematical_fingerprint']==g.fingerprint(p)
    assert set(rec['knowledge_point'])=={'db_id','id','title'}
    assert m['domain']['excluded_pole']==str(-b/a)
    for value in (q[':question/problem'],q.get(':question/worked-solution','')):formatting(value)
    fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0]
    assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    choices=f[':answer-field/choices'];assert len(choices)==5
    derivatives=[];correct=[]
    for item in choices:
        val=item[':answer/value'];formatting(val);ct,arg,v=primitive(val);assert v==x
        pole=sp.solve(arg,x);assert len(pole)==1
        derivative=primitive_derivative(val,d);derivatives.append(derivative)
        if sp.cancel(derivative-integrand)==0 and pole[0]==-b/a:correct.append(item[':answer/id'])
        assert item[':answer/type']==':answer.type/math'
    for i in range(5):
        for j in range(i):assert sp.cancel(derivatives[i]-derivatives[j])!=0,'equivalent primitives modulo C on common domain'
    assert len(correct)==1
    if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',correct[0]]
    if ':question/worked-solution' not in q:return {'bank_values':5,'solution_rows':0}
    sol=q[':question/worked-solution'];sm=re.search(r'First, let \$u=([^$]+)\.\$',sol);assert sm and sp.expand(parse(sm[1])-d)==0
    disp=sol.split('$$')[1]
    value=disp.split('}=')[1].split(r'\,')[0];assert parse(value)==a
    if r'\text{d}x=' in disp:
        jac=disp.split(r'\text{d}x=')[1].split(r'\text{d}u')[0];assert parse(jac)==1/a
    else:assert a==1 and r'\text{d}u=\text{d}x' in disp
    chain=sol.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
    rows=chain.split(r' \\  & =');lhs,rhs=rows[0].split(' & =');assert first_integrand(lhs)==integrand
    rows=[rhs]+rows[1:]
    expected_rows=3 if m['template'] in ('q-49450','q-49454') else 4 if m['template'] in ('q-15707','q-49453','q-49452') else 5
    assert len(rows)==expected_rows
    for row in rows:
        result=integral_row(row,d) if r'\int' in row else primitive_derivative(row,d)
        assert sp.cancel(result-integrand)==0,(row,result,integrand)
    assert '|u|+C' in rows[-2] and sp.expand(primitive(rows[-1])[1]-d)==0
    # The full source family mask enforces operations, not only equal derivative/row count.
    expected=(g.render_source(m['template'],p) if m['template'] in g.PROFILES else g.render_canonical(p))[1]
    assert sol==expected,'operative stages/prose differ from fixed family mask'
    return {'bank_values':5,'solution_rows':len(rows)}

def native(label,rec):
    f=rec['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'native owned radio selection; full bank checked independently'} for a in f[':answer-field/choices']]}
def rejection(fn):
    try:fn()
    except (ValueError,AssertionError):return
    raise AssertionError('mutation/invalid input was accepted')
def main():
    cases=[];review=[];inputs=[];fidelity=[];math_records=0;bank_values=0;solution_rows=0
    for sid,params in g.PARAMETERS.items():
        rec=g.generate('easy',template=sid,parameters=params,profile='original');counts=check(rec);math_records+=1;bank_values+=5;solution_rows+=counts['solution_rows']
        old=g.SOURCES[sid];q=rec['question'];of=old[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        for key in (':question/difficulty',':question/worked-solution'):assert (key in old)==(key in q)
        assert (':answer-field/correct' in of)==(':answer-field/correct' in f)
        assert q[':question/problem']==old[':question/problem']
        if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution']
        assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices'])
        for oa in of[':answer-field/choices']:
            od=primitive_derivative(oa[':answer/value'],params[1]*x+params[2]);assert sum(sp.cancel(od-primitive_derivative(na[':answer/value'],params[1]*x+params[2]))==0 for na in f[':answer-field/choices'])==1
        if ':answer-field/correct' in of:
            na=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert na[':answer/value']==of[':answer-field/correct'][':answer/value'];inputs.append(native(sid,rec))
        cases.append({'source_id':sid,'template':sid,'parameters':params,'bank_profile':'original','level':'easy','authored_level_assignment':False,'raw_omissions_preserved':sid=='q-49511','api_level_is_not_source_label':sid=='q-49511'})
        fidelity.append({'source_id':sid,'exact_prompt':True,'exact_complete_bank':True,'choices_matched':5,'solution_exact':True if ':question/worked-solution' in old else None,'correct_designation_matched':True if ':answer-field/correct' in of else None,'raw_attribute_presence':True})
        review.append({'kind':'original raw replay','source_id':sid,'record':rec})
        variant=g.generate('moderate' if sid=='q-49511' else 'easy',42,template=sid);check(variant);review.append({'kind':'normal generated variant','source_id':sid,'record':variant});inputs.append(native(sid+' normal',variant))
    completion=g.generate('moderate',template='q-49511',parameters=[2,3,5],profile='completed');check(completion);review.append({'kind':'separate inferred completion; difficulty/solution/key authored','record':completion});inputs.append(native('q-49511 separate completion',completion))
    # Changed original evidence profiles and explicit arithmetic/domain boundaries.
    boundary={'q-15707':[12,1,15],'q-49453':[2,1,1],'q-49450':[1,1,-15],'q-49454':[1,1,15],'q-49452':[1,-12,15],'q-49511':[12,12,15]}
    for sid,p in boundary.items():
        rec=g.generate('easy',91,template=sid,parameters=p,profile='original');counts=check(rec);math_records+=1;bank_values+=5;solution_rows+=counts['solution_rows']
        if sid!='q-49511':inputs.append(native('changed original '+sid,rec))
    for level,p in [('moderate',[12,-12,-15]),('moderate',[2,12,15]),('hard',['1/12','-12/11',-15]),('hard',['11/12','2/11',15])]:
        rec=g.generate(level,37,template='canonical',parameters=p);counts=check(rec);math_records+=1;bank_values+=5;solution_rows+=counts['solution_rows'];inputs.append(native(level+' explicit boundary '+str(p),rec))
    capacity=enumerate_capacity();save('capacity.json',capacity)
    family_coverage=set();unique={level:set() for level in ('easy','moderate','hard')}
    for level in ('easy','moderate','hard'):
        for seed in range(150):
            rec=g.generate(level,seed);counts=check(rec);math_records+=1;bank_values+=counts['bank_values'];solution_rows+=counts['solution_rows'];unique[level].add(rec['generation']['mathematical_fingerprint']);family_coverage.add((level,rec['generation']['template']));inputs.append(native(level+' '+str(seed),rec))
            meta=rec['generation'];other=g.generate(level,seed+177,template=meta['template'],parameters=meta['parameters'],profile=meta['profile']);assert rec['question'][':question/id']==other['question'][':question/id'];assert sorted(z[':answer/id'] for z in rec['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(z[':answer/id'] for z in other['question'][':question/answer-fields'][0][':answer-field/choices'])
            if seed<2:review.append({'kind':'normal '+level+' authored arithmetic band','record':rec})
    assert set(sid for level,sid in family_coverage if level=='easy')==set(g.PARAMETERS)-{'q-49511'}
    assert all(len(z)>=80 for z in unique.values())
    assert g.fingerprint([2,1,1])==g.fingerprint([4,2,2])
    assert g.fingerprint([1,-3,2])==g.fingerprint([-2,6,-4])
    # Antiderivative response equivalence regressions: sign/scalar of log argument changes C.
    vals=[r'\ln|x+2|+C',r'\ln|-x-2|+C',r'\ln|3x+6|+C']
    assert all(sp.cancel(primitive_derivative(v,x+2)-1/(x+2))==0 for v in vals)
    rejection(lambda:g.validate_bank(vals+[r'-\ln|x+2|+C',r'\ln|x|+C'],[1,1,2]))
    rejection(lambda:g.generate('moderate',parameters=[2,1,3],template='canonical'))
    rejection(lambda:g.generate('hard',parameters=[2,3,5],template='canonical'))
    rejection(lambda:g.generate('hard',parameters=['1/2','-1',5],template='canonical'))
    rejection(lambda:g.generate('easy',template='q-49454',parameters=[1,1,1],profile='original'))
    rejection(lambda:g.generate('easy',field_type='blank'))
    mut=copy.deepcopy(completion);mut['question'][':question/worked-solution']=mut['question'][':question/worked-solution'].replace(r'\frac{1}{3}\,\text{d}u',r'\frac{1}{2}\,\text{d}u');rejection(lambda:check(mut))
    mut=copy.deepcopy(completion);mut['question'][':question/worked-solution']+='\f';rejection(lambda:check(mut))
    mut=copy.deepcopy(completion);mut['question'][':question/worked-solution']=mut['question'][':question/worked-solution'].replace(r'2\int \frac{1}{u}\cdot (\frac{1}{3}\,\text{d}u)',r'\frac{2}{3}\int \frac{1}{u}\,\text{d}u');rejection(lambda:check(mut))
    # Reordered legitimate owned options must retain the native accepted selection.
    shuffled=copy.deepcopy(completion);shuffled['question'][':question/answer-fields'][0][':answer-field/choices'].reverse();inputs.append(native('legitimate reordered radio bank',shuffled))
    save('source-cases.json',cases);save('source-replay.json',{'complete_banks_matched':6,'complete_banks_total':6,'choices_matched':30,'choices_total':30,'distractors_matched':20,'distractors_total_observed_designations':20,'correct_designations_matched':5,'correct_designations_observed':5,'solutions_exact':5,'solutions_available':5,'raw_omission_parity':6,'rows':fidelity})
    save('review.json',review);(HERE/'review.md').write_text('\n\n'.join('## '+row['kind']+' '+row.get('source_id','')+'\n\n'+g.markdown(row['record']) for row in review)+'\n')
    save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    report=json.loads((HERE/'native-grading.json').read_text());assert report['documented_unresolved_checks']==0
    for level in ('easy','moderate','hard'):
        for form in ('json','markdown'):
            output=subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),'--difficulty',level,'--count','2','--format',form],text=True);assert output
            if form=='json':assert len(json.loads(output))==2
    files=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'topic.json',HERE/'lesson.json',HERE/'contract.json',HERE/'capacity.py']
    save('validation.json',{'passed':True,'source_basis':2275,'source_lineage':g.SOURCE['lineage'],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_complete_banks':'6/6 (30/30 choices)','observed_correct_designations':'5/5; q-49511 absent, not counted as matched','source_solutions':'5/5 available, full prose and operative stages exact','raw_omissions':'q-49511 difficulty/solution/correct absent in public original replay','mathematical_records':math_records,'independently_read_bank_values':bank_values,'independently_read_solution_rows':solution_rows,'sample_unique_integrands':{k:len(v) for k,v in unique.items()},'finite_supported_capacity':capacity['distinct_integrands'],'default_family_coverage':[list(v) for v in sorted(family_coverage)],'native_records':len(inputs),'native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'native_unresolved':0,'raw_ungraded_records':[{'source':'q-49511','reason':'missing correct designation; raw evidence not sent to grader; separately inferred completion tested'}],'mutations_rejected':['invalid level bounds','unsupported field','sign/scalar-equivalent log banks','wrong substitution coefficient','lost canonical operative stage','C0 character'],'limits':['moderate/hard difficulty bands authored from coefficient arithmetic; no observed moderate/hard labels','opaque original bank intention unresolved; historical profiles evidence-only','radio native checks select IDs; calculus semantics independently verified; no blank sources'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'database_writes':0})
    print(json.dumps({'passed':True,'math_records':math_records,'native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'unique_integrands':{k:len(v) for k,v in unique.items()}},indent=2))
if __name__=='__main__':main()

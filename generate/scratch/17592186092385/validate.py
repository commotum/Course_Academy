"""Independent prompt, solution, source-bank and real-engine grading checks."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('intercepts_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',real=True);y=sp.Symbol('y',real=True)

def expression(text):
    text=text.replace('\\\\','\\').replace('\\left','').replace('\\right','').replace('\\,','').replace('\\cdot','*')
    def group(s,i):
        assert s[i]=='{', (s,i)
        depth=1;j=i+1
        while depth:
            if s[j]=='{':depth+=1
            if s[j]=='}':depth-=1
            j+=1
        return s[i+1:j-1],j
    def convert(s):
        out='';i=0
        while i<len(s):
            if s.startswith('\\frac',i) or s.startswith('\\dfrac',i):
                i+=len('\\dfrac') if s.startswith('\\dfrac',i) else len('\\frac')
                a,i=group(s,i);b,i=group(s,i);out+='(('+convert(a)+')/('+convert(b)+'))'
            elif s.startswith('\\sqrt',i):
                i+=5;n='2'
                if s[i]=='[':j=s.index(']',i);n=s[i+1:j];i=j+1
                a,i=group(s,i);out+='(('+convert(a)+')**(1/('+n+')))'
            elif s[i]=='{':a,i=group(s,i);out+='('+convert(a)+')'
            elif s[i]=='^':out+='**';i+=1
            else:out+=s[i];i+=1
        return out
    return parse_expr(convert(text),local_dict={'x':x,'y':y},transformations=standard_transformations+(implicit_multiplication_application,))

def equal(a,b):
    # Radical branches are checked at positive abscissas; simplify powers there.
    return sp.simplify(sp.powdenest(a-b,force=True))==0

def parsed(q):
    problem=q[':question/problem']
    f=expression(re.search(r'\$(?:f\(x\)|y)\s*=\s*(.*?)\$',problem)[1])
    px,py=re.search(r'at the point \$\((.*?)\)',problem)[1].split(',')
    p=expression(px);yp=expression(py)
    assert equal(f.subs(x,p),yp),'Point not on curve'
    if any(t.as_powers_dict().get(x,sp.Integer(0)).q!=1 for t in f.as_ordered_terms()): assert p>0
    m=sp.simplify(sp.diff(f,x).subs(x,p));assert m.is_finite and m!=0
    n=-1/m;b=sp.simplify(yp-n*p)
    axis=re.search(r'intersects the \$([xy])\$-axis',problem)[1]
    a=sp.simplify(-b/n) if axis=='x' else b
    return f,p,yp,m,n,b,a,axis

def parse_question(q):
    f,p,_,_,_,_,_,axis=parsed(q)
    return g.fingerprint_expr(f,p,axis)

def solution_check(q):
    f,p,yp,m,n,b,a,axis=parsed(q)
    assert q.get(':question/worked-solution') and q.get(':question/answer-fields')
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
    assert len(blocks)==5,'Expected five source solution blocks'
    def last_rhs(block):
        return block.rsplit('=',1)[1].replace(r'\end{aligned}','').strip().rstrip('.,')
    assert equal(expression(last_rhs(blocks[0])),sp.diff(f,x)),'Wrong derivative'
    assert equal(expression(last_rhs(blocks[1])),m),'Wrong tangent slope'
    assert equal(expression(last_rhs(blocks[2])),n),'Wrong normal slope'
    assert equal(expression(last_rhs(blocks[3])),n*x+b),'Wrong normal line'
    assert equal(expression(last_rhs(blocks[4])),a),'Wrong intercept'
    conclusion=re.search(r'Therefore,.*?\$\((.*?)\)\.?\$',q[':question/worked-solution'],re.S)[1]
    cx,cy=map(expression,conclusion.replace(r'\,','').split(','))
    assert equal(cx,a if axis=='x' else 0) and equal(cy,0 if axis=='x' else a)
    for field in q[':question/answer-fields']:
        ft=field[':answer-field/type'];ft=ft if isinstance(ft,str) else ft[':db/ident']
        correct=field[':answer-field/correct'];cid=correct[':answer/id'] if isinstance(correct,dict) else correct[1]
        choices=field[':answer-field/choices']
        if ft==':answer-field.type/radio':
            assert len(choices)==5
            values=[tuple(map(expression,c[':answer/value'].strip('()').split(','))) for c in choices]
            target=(a,sp.Integer(0)) if axis=='x' else (sp.Integer(0),a)
        else:
            assert ft==':answer-field.type/blank' and len(choices)==1
            assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
            values=[expression(c[':answer/value']) for c in choices]
            target=a if field[':answer-field/key']=='field-1' else sp.Integer(0)
        assert len(set(values))==len(values)
        assert [c[':answer/id'] for c,val in zip(choices,values) if val==target]==[cid]
    return f,p,a,axis

def independent(rec):
    f,p,a,axis=solution_check(rec['question'])
    meta=rec['generation'];mid=meta['template'];s=meta['parameters']['scale']
    assert meta['parameter_fingerprint']==g.fingerprint_expr(f,p,axis)
    assert rec==g.generate_profile(mid,s,meta['seed'])
    assert rec['question'][':question/difficulty']==':question.difficulty/'+g.SPECS[mid][3]
    return True

def checks(rec):
    solution_check(rec['question']);out=[]
    for i,field in enumerate(rec['question'][':question/answer-fields']):
        if field[':answer-field/type']==':answer-field.type/radio':
            out.extend({'field_index':i,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Complete source bank option'} for c in field[':answer-field/choices'])
        else:
            a=expression(field[':answer-field/choices'][0][':answer/value'])
            out.extend({'field_index':i,'submitted':text,'expected':expected,'purpose':purpose} for text,expected,purpose in [(sp.latex(a),'accepted','Canonical'),(str(a),'accepted','Exact notation'),('('+str(a)+'*2)/2','accepted','Equivalent expression'),(str(a+1),'rejected','Wrong offset'),(str(a-1),'rejected','Wrong negative offset')])
    return out

def main():
    evidence=[];preview=[]
    for mid in g.SPECS:
        original=g.ROWS[mid];r=g.generate_profile(mid,1);independent(r);solution_check(original)
        fields=[]
        for of,rf in zip(sorted(original[':question/answer-fields'],key=lambda f:f[':answer-field/key']),r['question'][':question/answer-fields']):
            def math_value(c):
                t=c[':answer/value']
                return tuple(map(expression,t.strip('()').split(','))) if t.startswith('(') else expression(t)
            observed=[math_value(c) for c in of[':answer-field/choices']]
            generated=[math_value(c) for c in rf[':answer-field/choices']]
            assert set(observed)==set(generated) and len(observed)==len(generated)
            oc=math_value(of[':answer-field/correct'])
            rc=math_value(next(c for c in rf[':answer-field/choices'] if c[':answer/id']==rf[':answer-field/correct'][1]))
            assert oc==rc
            fields.append({'key':of[':answer-field/key'],'matched_options':len(observed),'total_options':len(observed),'missing':[],'extra':[],'correct_designation':True})
        assert r['question'][':question/problem']==original[':question/problem']
        assert r['question'][':question/worked-solution']==original[':question/worked-solution']
        evidence.append({'source':mid,'fields':fields,'complete_bank':True,'prompt_and_solution_exact':True})
        for s in range(1,13):
            r=g.generate_profile(mid,s);independent(r);preview.append(r)
    for level in g.SUPPORTED_LEVELS:
        a=g.batch(level,999,12);b=g.batch(level,999,12)
        assert a==b and len({parse_question(r['question']) for r in a})==len(a)
        assert {r['generation']['template'] for r in a}=={mid for mid in g.SPECS if g.SPECS[mid][3]==level}
    for mid,s in [('q-10871',0),('q-10871',13),('q-342222',1)]:
        try:g.generate_profile(mid,s)
        except ValueError:pass
        else:raise AssertionError('Out-of-domain input accepted')
    try:g.batch('hard',5,0)
    except ValueError:pass
    else:raise AssertionError('Unsupported level accepted')
    native=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in preview]
    (HERE/'reference/native-validation-input.json').write_text(json.dumps(native,indent=2))
    grader_build=json.loads((HERE/'reference/grader-build.json').read_text())
    assert hashlib.sha256((HERE/'check-engine').read_bytes()).hexdigest()==grader_build['binary_sha256']
    subprocess.run([str(HERE/'check-engine'),str(HERE/'reference/native-validation-input.json'),str(HERE/'reference/native-validation-report.json')],check=True)
    report=json.loads((HERE/'reference/native-validation-report.json').read_text());assert report['documented_unresolved_checks']==0
    result={'status':'pass','source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'source_replay':evidence,'complete_banks':len(evidence),'matched_options':sum(f['matched_options'] for e in evidence for f in e['fields']),'generated_validated':len(preview),'distinct_tasks':len({parse_question(r['question']) for r in preview}),'native_grader':'course_academy_engine::learning::grade_field','grader_build':'reference/grader-build.json','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'check-engine',HERE/'reference/grader-build.json']}}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'preview.json').write_text(json.dumps(preview,indent=2)+'\n')
    (HERE/'review.md').write_text('\n\n'.join('## '+r['generation']['template']+' scale '+str(r['generation']['parameters']['scale'])+'\n\n'+r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in preview if r['generation']['parameters']['scale'] in (1,2,12)))
    print(json.dumps({'status':'pass','source_banks':len(evidence),'variants':len(preview),'native_checks':report['accepted_checks']+report['rejected_checks']}))

if __name__=='__main__':main()

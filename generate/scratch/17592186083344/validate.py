"""Exact source-bank replay, parsed displayed integrals, limits, and application grading."""
import hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def group(t,i):
    assert t[i]=='{';depth=1;j=i+1
    while depth:
        if t[j]=='{':depth+=1
        if t[j]=='}':depth-=1
        j+=1
    return t[i+1:j-1],j

def expr(t):
    while r'\frac' in t:
        i=t.index(r'\frac');a,j=group(t,i+5);b,k=group(t,j);t=t[:i]+'(('+str(expr(a))+')/('+str(expr(b))+'))'+t[k:]
    while r'\sqrt' in t:
        i=t.index(r'\sqrt');a,j=group(t,i+5);t=t[:i]+'sqrt('+str(expr(a))+')'+t[j:]
    t=t.replace(r'\theta','x');t=re.sub(r'(?<![A-Za-z])[ytz](?![A-Za-z])','x',t);t=t.replace('{','(').replace('}',')').replace('^','**').replace(r'\,','').replace(r'\cdot','*').replace('\\','')
    return parse_expr(t,local_dict={'x':g.x,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def displayed_integrand(q):
    t=q[':question/problem'].replace(r'\dfrac',r'\frac');i=t.index(r'\frac');a,j=group(t,i+5);b,k=group(t,j)
    return s.cancel(expr(a)/expr(b))
def fingerprint(q):
    # All source/generated integrals have one explicit lower bound; ignore variable names/notation.
    if r'\frac' not in q[':question/problem'] and r'\dfrac' not in q[':question/problem']:return 'excluded|'+g.digest(q[':question/problem'])
    m=re.search(r'\\int\s*\}?\s*_\{?(-?\d+)',q[':question/problem']);assert m,q[':question/problem']
    return g.digest([s.srepr(s.factor(displayed_integrand(q))),int(m[1])])
def independent(rec):
    md=rec['generation'];q=rec['question'];m=md['template'];k=md['parameters']['scale'];level=q[':question/difficulty'].split('/')[-1]
    assert rec==g.generate(level,md['seed'],m,md['parameters'])
    C,n,A,B,p,L,v,rad=g.DATA[m];p=s.Rational(p);fun=displayed_integrand(q)
    assert s.simplify(fun-g.expression(m,k))==0,(m,k,'display')
    primitive=s.Rational(C*k,A*n)/(1-p)*(A*g.x**n+B)**(1-p)
    assert s.simplify(s.diff(primitive,g.x)-fun)==0
    limit=s.limit(primitive,g.x,s.oo);assert limit==0
    expected=s.simplify(limit-primitive.subs(g.x,L));assert expected==g.correct(m,k)
    f=q[':question/answer-fields'][0];correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert expr(correct[':answer/value'])==expected
    vals=[expr(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/type']==':answer.type/math'];assert len(set(vals))==len(vals);assert vals.count(expected)==1
    assert (A*L**n+B)>0 and p>1 and (n==1 or L>=0)
    assert all(r'\\theta' not in q[t] for t in (':question/problem',':question/worked-solution'))
    assert all(q[t].count('$')%2==0 and q[t].count('{')==q[t].count('}') for t in (':question/problem',':question/worked-solution'))
    assert q[':question/problem'].count('{{'+f[':answer-field/key']+'}}')==(f[':answer-field/type']==':answer-field.type/blank')
    assert fingerprint(q)==fingerprint(g.generate(level,0,m,{'scale':k})['question'])
    return expected

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    if f[':answer-field/type']==':answer-field.type/radio':return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete choice-bank grading'} for a in f[':answer-field/choices']]
    ans=f[':answer-field/choices'][0][':answer/value']
    return [{'field_index':0,'submitted':t,'expected':ex,'purpose':'exact/equivalent and incorrect blank values'} for t,ex in [(ans,'accepted'),('('+ans+')+0','accepted'),('0','rejected'),('('+ans+')+1','rejected')]]

def main():
    allrecords=[];cases=[];review=[]
    for m,old in g.SOURCES.items():
        level=old[':question/difficulty'][':db/ident'].split('/')[-1];r=g.generate(level,0,m,{'scale':1});independent(r);allrecords.append(r)
        f=r['question'][':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert r['question'][':question/problem']==old[':question/problem'] and r['question'][':question/worked-solution']==old[':question/worked-solution']
        assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in of[':answer-field/choices'])
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
        cases.append({'source':m,'template':m,'bank_profile':r['generation']['bank_profile'],'complete_bank':True,'matched_values':len(f[':answer-field/choices']),'total_values':len(f[':answer-field/choices']),'missing':[],'extra':[],'exact_source_prompt':True,'exact_source_solution':True})
        for k in (2,7,1000):
            v=g.generate(level,1980,m,{'scale':k});independent(v);allrecords.append(v)
        review.append('## '+m+' original / replay\n\n'+g.markdown(r)+'\n\n### Coefficient variant (scale 7)\n\n'+g.markdown(g.generate(level,1980,m,{'scale':7})))
    for level in g.SUPPORTED_LEVELS:
        rs=g.batch(level,12,1980);assert len({fingerprint(r['question']) for r in rs})==len(rs)
        for r in rs:independent(r);allrecords.append(r)
    save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(allrecords)])
    subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    e=json.loads((HERE/'engine-report.json').read_text());assert e['documented_unresolved_checks']==0
    save('source-cases.json',cases);save('review.json',allrecords);(HERE/'review.md').write_text('\n\n---\n\n'.join(review))
    save('validation.json',{'status':'pass','source_basis':1980,'complete_source_banks':len(cases),'matched_values':sum(c['matched_values'] for c in cases),'missing_options':[],'extra_options':[],'independent_display_checks':len(allrecords),'fidelity':'Exact prompt, solution and complete banks at original parameters. Coefficient variants preserve response shapes, banks and solution sequence; math typography is an explicitly recorded layout extension.','correctness':'Parsed displayed integrand, differentiated primitive, exact convergent limit, complete answer uniqueness','native_grading':{k:e[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'reference/initial/source.json',HERE/'check-engine')}})
    print('Passed source-bank replay, displayed integral/limit validation and real grading')
if __name__=='__main__':main()

"""Independent parsing of displayed mathematics, full source replay and grading."""
import hashlib,importlib.util,json,re,subprocess,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('general_base_log',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=g.X

def group(s,i,opening='{',closing='}'):
    assert s[i]==opening,(s,i)
    start=i+1;depth=1;i+=1
    while depth:
        assert i<len(s),(s,start)
        depth+=(s[i]==opening)-(s[i]==closing);i+=1
    return s[start:i-1],i

def math(s):
    s=s.replace(r'\,','').replace(r'\!','').strip().rstrip('.,').replace('⁡','').replace('\u00a0','')
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','')
    s=re.sub(r'\\operatorname\{(ln|log)\}',lambda m:m[1],s)
    s=s.replace(r'\ln','ln').replace(r'\log','log').replace('{log}','log')
    s=re.sub(r'\\text\{[^}]*\}','',s)
    # Differential operators act on the following full parentheses.
    op=r'\frac{}{x}'
    s=s.replace(r'\frac{\text{d}}{\text{d}x}',op)
    while op in s:
        at=s.index(op);part,end=group(s,at+len(op),'(',')')
        s=s[:at]+'('+str(sp.diff(math(part),X))+')'+s[end:]
    while r'\frac' in s:
        at=s.index(r'\frac');n,end=group(s,at+5);d,end2=group(s,end)
        s=s[:at]+'('+str(math(n)/math(d))+')'+s[end2:]
    s=re.sub(r'log_\{(\d+)\}\s*x',r'(log(x)/log(\1))',s)
    s=re.sub(r'log_([0-9]+)\s*x',r'(log(x)/log(\1))',s)
    s=re.sub(r'\blog\s*x',r'(log(x)/log(10))',s)
    s=re.sub(r'ln\s*(\d+)',r'log(\1)',s)
    s=re.sub(r'ln\s*x',r'log(x)',s)
    s=s.replace('ln(','log(').replace('xlog(', 'x*log(').replace('{','(').replace('}',')').replace('^','**').replace(r'\cdot','*')
    return parse_expr(s,local_dict={'x':X,'e':sp.E,'log':sp.log,'exp':sp.exp},transformations=standard_transformations+(implicit_multiplication_application,))

def equal(a,b):return sp.simplify(a-b)==0

def displayed(q):
    return math(re.search(r'\$[fy](?:\(x\))?\s*=([^$]+)',q[':question/problem']).group(1))

def fingerprint(q):
    derivative=sp.diff(displayed(q),X)
    point=re.search(r'instantaneous rate of change at \$x=([^$]+)',q[':question/problem'])
    return hashlib.sha256(json.dumps([sp.srepr(sp.expand(sp.expand_log(derivative,force=True))),str(math(point[1])) if point else None],sort_keys=True).encode()).hexdigest()

def formatting(s):
    assert s.count('$$')%2==0
    assert s.replace('$$','').count('$')%2==0
    depth=0
    for c in s:
        if c=='{':depth+=1
        if c=='}':depth-=1;assert depth>=0
    assert depth==0

def inspect_record(r):
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];p=r['generation']['parameters'];t=r['generation']['template']
    level=q[':question/difficulty'].split('/')[-1]
    g.validate_parameters(p,level,t,r['generation']['bank_profile'])
    f=displayed(q);d=sp.diff(f,X);_,gd,answer=g.expressions(t,p)
    assert equal(d,gd),(t,f,d,gd)
    match=re.search(r'instantaneous rate of change at \$x=([^$]+)',q[':question/problem'])
    expected=sp.simplify(d.subs(X,math(match[1]))) if match else d
    assert equal(expected,answer)
    for s in (q[':question/problem'],q[':question/worked-solution']):formatting(s)
    fields=q[':question/answer-fields'];assert len(fields)==1
    field=fields[0];choices=field[':answer-field/choices'];correct=field[':answer-field/correct'][1]
    assert correct in [a[':answer/id'] for a in choices]
    assert all(str(uuid.UUID(s))==s for s in [q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in choices])
    values=[math(a[':answer/value']) for a in choices]
    assert all(equal(v,expected)==(a[':answer/id']==correct) for v,a in zip(values,choices))
    if field[':answer-field/type'].endswith('/radio'):
        assert len(values)==5
        assert all(not equal(values[i],values[j]) for i in range(5) for j in range(i))
    else:assert len(values)==1 and '{{field-1}}' in q[':question/problem']
    # Verify every RHS of the source solution, including formal derivatives,
    # expanded operations, and substituted evaluation rows.
    blocks=q[':question/worked-solution'].split('$$')
    checks=0
    for block in blocks[3::2]:
        for row in re.split(r'\\\\',block):
            if '& =' not in row:continue
            rhs=row.split('& =',1)[1].split(r'\end{aligned}',1)[0].strip()
            if '|' in rhs:
                # Source's first evaluation row explicitly repeats d(x).
                part=group(rhs,1,'(',')')[0] if rhs.startswith('{(') else None
                assert part is not None and equal(math(part),d),(t,rhs)
                assert 'x='+str(p['point']) in rhs
                value=expected
            else:value=math(rhs)
            assert equal(value,expected if '|' in block or 'Hence' in q[':question/worked-solution'] and block==blocks[-2] and match else d),(t,rhs,value,d,expected)
            checks+=1
    assert checks>=2
    return expected

def checks(r,label):
    f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Every complete source-profile choice'} for a in f[':answer-field/choices']]}
    answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
    value=inspect_record(r)
    return {'label':label,'record':r,'checks':[{'submitted':answer,'expected':'accepted','purpose':'Canonical fragment'},{'submitted':'('+answer+')+0','expected':'accepted','purpose':'Equivalent parenthesized fragment'},{'submitted':r'\frac{2\left('+answer+r'\right)}{2}','expected':'accepted','purpose':'Equivalent scaled unreduced fragment'},{'submitted':'('+answer+')+1','expected':'rejected','purpose':'Incorrect derivative/rate'},{'submitted':'0','expected':'rejected','purpose':'Incorrect constant derivative'}]}

def main():
    reports=[];native=[];review=[]
    for t,(level,mid) in g.TEMPLATES.items():
        source=g.SOURCES[mid];replay=g.generate(level,0,t,g.PARAMETERS[t])
        inspect_record(replay)
        q=replay['question'];sf=source[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        assert q[':question/problem']==source[':question/problem'] and q[':question/worked-solution']==source[':question/worked-solution']
        assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in sf[':answer-field/choices']]
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
        reports.append({'template':t,'source':mid,'profile':'source-bank','complete_banks_matched':1,'complete_banks_total':1,'distractors_matched':len(f[':answer-field/choices'])-1,'distractors_total':len(f[':answer-field/choices'])-1,'prompt_and_solution_exact_replay':True})
        native.append(checks(replay,'source/'+mid))
        for i in range(24):
            r=g.generate(level,100+i,t);inspect_record(r);native.append(checks(r,t+'/'+str(i)))
            assert r==g.generate(level,100+i,t)
            if i<2:review.append({'source':source,'variant':r})
        # Lower and upper bounds, keeping authored common bases and points.
        for boundary in (2,12):
            p=dict(g.PARAMETERS[t])
            for k in p:
                if k not in ('point','wrong_expbase') and not(k=='base' and 'common' in t):p[k]=boundary
            if t=='scaled-log':p['base']=3 if boundary==2 else 11
            r=g.generate(level,0,t,p);inspect_record(r);native.append(checks(r,t+'/boundary/'+str(boundary)))
    (HERE/'source-replay.json').write_text(json.dumps(reports,indent=2)+'\n')
    (HERE/'side-by-side.json').write_text(json.dumps(review,indent=2)+'\n')
    (HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
    subprocess.run([str(HERE/'check-current-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    report=json.loads((HERE/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    result={'status':'passed','templates':len(reports),'source_banks_matched':len(reports),'source_banks_total':len(reports),'source_distractors_matched':sum(r['distractors_matched'] for r in reports),'variants_and_replays_checked':len(native),'fidelity':'exact prompt, solution, complete choices and key replay at all nine complete source questions','mathematics':'Independent displayed-expression differentiation, every bank option and all solution RHS rows','grading':report,'unsupported_levels':['moderate'],'plots':'none'}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='grading'}))
if __name__=='__main__':main()

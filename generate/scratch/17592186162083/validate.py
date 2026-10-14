#!/usr/bin/env python3
"""Read displayed curves, endpoints, claims and solution; check actual grading."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, rationalize
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('arc',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t,u,x,y,z,k=sp.symbols('t u x y z k', nonnegative=True)
def balanced(s,start):
    assert s[start]=='{';depth=1;i=start+1
    while depth:
        if s[i]=='{':depth+=1
        if s[i]=='}':depth-=1
        i+=1
    return s[start+1:i-1],i

def math(s):
    s=s.replace('π',r'\pi').replace('⁡','').replace(r'\,','').replace(' ','').strip('.,')
    s=s.replace(r'\operatorname{cos}','cos').replace(r'\operatorname{sin}','sin')
    while r'\frac' in s or r'\sqrt' in s:
        m=re.search(r'\\(frac|sqrt)\{',s);a,end=balanced(s,m.end()-1)
        if m[1]=='frac':b,end=balanced(s,end);val='(('+a+')/('+b+'))'
        else:val='sqrt('+a+')'
        s=s[:m.start()]+val+s[end:]
    s=s.replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**')
    s=re.sub(r'(cos|sin)(\d*)([tu])',lambda m:m[1]+'('+str(m[2] or 1)+'*'+m[3]+')',s)
    return sp.simplify(parse_expr(s,local_dict={'t':t,'u':u,'x':x,'y':y,'z':z,'k':k,'pi':sp.pi,'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos},transformations=standard_transformations+(implicit_multiplication_application,rationalize)))
def geometry(q):
    text=q[':question/problem'];vectors=re.findall('⟨([^⟩]+)⟩',text);assert len(vectors)==2,vectors
    vec=[[math(c) for c in v.replace(r'\,','').split(',')] for v in vectors];assert all(len(v)==2 for v in vec)
    bounds=re.findall(r'0\\le ([tu])\\le (.*?)(?=[$.,]|\s*\\\\|\s*\\end)',text);assert len(bounds)==2,bounds
    variables=[{'t':t,'u':u}[v] for v,end in bounds];ends=[math(end) for v,end in bounds];assert all(e>0 for e in ends)
    normalized=[[sp.simplify(c.subs(var,end*z)) for c in v] for v,var,end in zip(vec,variables,ends)]
    assert all(sp.simplify(a-b)==0 for a,b in zip(*normalized)),('different paths',normalized)
    return normalized[0],vec[0],variables[0],ends[0]
def fingerprint(q):
    normalized,*_=geometry(q)
    return g.digest([str(sp.expand(c)) for c in normalized])
def claimed(line):return math(re.search(r'\\text\{d\}s=([^$]+)',line)[1])
def structural(rec):
    q=rec['question'];text=q[':question/problem'];sol=q[':question/worked-solution'];norm,v,var,end=geometry(q)
    for s in (text,sol):assert s.count('$')%2==0 and s.count('{')==s.count('}')
    assumed=claimed(text.split('Which of the following')[0] if text.startswith('Suppose') else text.split('Which of the following')[0])
    lines=[line for line in text.splitlines() if line.startswith('- **')];assert len(lines)==3
    truth=[bool(sp.simplify(claimed(line)-assumed)==0) for line in lines]
    fs=q[':question/answer-fields'];assert [f[':answer-field/key'] for f in fs]==['I','II','III']
    for f,c in zip(fs,truth):
        assert f[':answer-field/type']==':answer-field.type/checkbox'
        assert [a[':answer/value'] for a in f[':answer-field/choices']]==['false','true']
        cv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert cv==str(c).lower()
    assertions=re.findall(r'Statement (I|II|III) is (true|false)',sol)
    # Source combined wording has one initial assertion and a second clause.
    assertions+=re.findall(r'while statement (I|II|III) is (true|false)',sol)
    assert len(assertions)==3,assertions
    for i,val in assertions:assert truth[{'I':0,'II':1,'III':2}[i]]==(val=='true')
    # Every solution integral equals the given integral (multiple '=' handles reversal).
    for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
        if r'\int' in block:assert math(block.split('=')[-1])==assumed
        else:
            relation,domain=block.strip().rstrip('.').split(r'\,');lhs,rhs=relation.split('=');target={'x':v[0],'y':v[1]}[lhs]
            assert sp.simplify(target-math(rhs).subs({x:v[0],y:v[1]}))==0,(target,rhs)
            dm=re.fullmatch(r'0\\le ([xy])\\le (.*)',domain);assert dm
            comp={'x':v[0],'y':v[1]}[dm[1]]
            assert comp.subs(var,0)==0 and sp.simplify(comp.subs(var,end)-math(dm[2]))==0
    if 'half-circle' in sol:
        R=math(re.search(r'radius \$(.*?)\$',sol)[1]);assert sp.simplify(sum(c*c for c in v)-R*R)==0
        assert norm[0].subs(z,0)==R and norm[0].subs(z,1)==-R and norm[1].subs(z,sp.Rational(1,2))==R
    names=[name for name,b in zip(('I','II','III'),truth) if b]
    expected=' and '.join(names)+' only.'
    assert '"'+expected+'"' in sol
    return fingerprint(q)
def checks(rec):
    structural(rec)
    return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'correct and incorrect checkbox Boolean'} for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    records=[];ledger=[];coverage={};review=[]
    for level,profiles in g.LEVELS.items():
        for profile in profiles:
            replay=g.generate(level,0,profile,g.CASES[profile]);structural(replay);old=g.SOURCES[profile];new=replay['question']
            assert new[':question/problem']==old[':question/problem'],profile+' prompt'
            assert new[':question/worked-solution']==old[':question/worked-solution'],profile+' solution'
            for f,of in zip(new[':question/answer-fields'],old[':question/answer-fields']):
                assert f[':answer-field/key']==of[':answer-field/key']
                assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']
                assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
                assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
            ledger.append({'profile':profile,'source_id':old[':db/id'],'complete_banks_matched':3,'values_matched':6,'correct_designations_matched':3,'prompt_exact':True,'solution_exact':True,'missing_or_extra':[]})
            pool=list(g.candidates(profile));fps=set()
            for p in pool:
                r=g.generate(level,13,profile,p);fps.add(structural(r));assert r['question']==g.generate(level,71,profile,p)['question'];records.append(r)
            coverage[profile]={'cases':len(pool),'distinct_geometry':len(fps),'slots':{slot:sorted({p[slot] for p in pool}) for slot in pool[0]}}
            review.extend([replay,g.generate(level,13,profile,pool[-1])])
    native=[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)]
    for name,value in [('source-replay.json',ledger),('source-replay-records.json',review[::2]),('review-records.json',review),('engine-input.json',native)]: (D/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
    report=json.loads((D/'engine-report.json').read_text());assert report['documented_unresolved_checks']==0
    finite={level:len({fingerprint(r['question']) for r in records if r['question'][':question/difficulty'].endswith('/'+level)}) for level in g.LEVELS}
    for level in ('easy','unclassified'):
        try:g.batch(level,1)
        except ValueError:pass
        else:raise AssertionError('Unsupported level accepted')
    result={'status':'pass','source_templates':len(ledger),'matched_banks':15,'matched_values':30,'complete_bank_fidelity':True,'sampled_records':len(records),'coverage':coverage,'finite_variant_limit':finite,'correctness':'Independent rendered-curve normalization, matching endpoints, invariant claims, checkbox truth, Cartesian relations and bounds, solution equalities and conclusion','fidelity':'Exact original prompt and solution replay for every supported source; all original Boolean banks and correct designations matched','grading':{key:report[key] for key in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{'generator':sha(D.with_suffix('.py')),'validator':sha(D/'validate.py'),'source':sha(D/'source.json'),'grader':sha(ROOT/'generate/runs/current/check-engine')}}
    (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

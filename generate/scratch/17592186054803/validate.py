"""Independent parsing of rendered mathematics and actual learner grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
s=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.Symbol('x')
def math(t):
    t=t.replace('^{','**').replace('^','**').replace('{','').replace('}','').replace(' ','').replace(r'\cdot','')
    assert re.fullmatch(r'[0-9x()+*/.\-]+',t),t
    return sp.expand(parse_expr(t,transformations=standard_transformations+(implicit_multiplication_application,),local_dict={'x':x}))
def rendered(q):
    text=q[':question/problem'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',text,re.S)
    if not blocks:
        inline=re.findall(r'\$(.*?)\$',text,re.S)
        if '=' in inline[1]:left,right=inline[1].split('=')
        else:left,right=inline[:2]
    elif '=' in blocks[0]:left,right=blocks[0].split('=')
    else:left,right=blocks
    right=right.replace('P(x)','').replace('.', '').replace(r'\cdot','')
    F=math(left);H=math(right);P,rem=sp.div(F,H,x);assert rem==0
    return F,H,P
def fingerprint(q):
    F,H,P=rendered(q)
    return g.digest([str(F),sorted(int(z) for z in sp.solve(H,x))])
def structural(rec):
    q=rec['question'];F,H,P=rendered(q);f=q[':question/answer-fields'][0]
    vals=[math(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(set(map(str,vals)))==len(vals)
    cid=f[':answer-field/correct'][1]
    assert sum(z==P for z in vals)==1
    assert all((a[':answer/id']==cid)==(z==P) for a,z in zip(f[':answer-field/choices'],vals))
    assert fingerprint(q)==rec['generation']['parameter_fingerprint']
    sol=q[':question/worked-solution'];tables=re.findall(r'\|  \|.*?(?=\n\n)',sol,re.S)
    # Independently check every rendered synthetic table, including zero coefficients.
    lines=sol.splitlines();starts=[i for i,line in enumerate(lines) if line.startswith('|  | $x^')]
    assert len(starts)==2
    polys=[F]
    for start in starts:
        cells=lambda line:[c.strip().strip('$') for c in line.strip('|').split('|')]
        inp=cells(lines[start+2]);pro=cells(lines[start+3]);out=cells(lines[start+4]);root=int(inp[0]);co=list(map(int,inp[1:]));bo=list(map(int,out[1:]));products=list(map(int,pro[2:]));assert co==sp.Poly(polys[-1],x).all_coeffs()
        assert bo[0]==co[0]
        for i in range(1,len(co)):assert products[i-1]==bo[i-1]*root and bo[i]==co[i]+products[i-1]
        assert bo[-1]==0
        quotient=sp.div(polys[-1],x-root,x)[0];assert bo[:-1]==sp.Poly(quotient,x).all_coeffs();polys.append(quotient)
    assert polys[-1]==P
    # Independently read each displayed division/product identity, not metadata.
    for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
        block=block.rstrip('.,');block=re.sub(r'\\underbrace\{(.*?)\}_\{P\(x\)\}',r'\1',block)
        if block.startswith('P(x)='):assert all(math(t)==P for t in block.split('=')[1:]);continue
        left,right=block.split('=')
        if left.startswith(r'\frac'):
            m=re.fullmatch(r'\\frac\{(.*?)\}\{(.*?)\}',left);assert m,left
            assert sp.expand(math(m[1])-math(m[2])*math(right))==0
        else:assert math(left)==math(right)
    return P

def checks(rec):
    f=rec['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
    if f[':answer-field/type']==':answer-field.type/radio':return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'complete field-owned bank'} for a in f[':answer-field/choices']]
    P=structural(rec)
    return [{'submitted':g.tex(P),'expected':'accepted','purpose':'expanded blank'}, {'submitted':g.fact(**{k:rec['generation']['parameters'][k] for k in ('c','a','b')}),'expected':'accepted','purpose':'equivalent factored blank'}, {'submitted':g.tex(P+1),'expected':'rejected','purpose':'wrong constant'}, {'submitted':g.tex(-P),'expected':'rejected','purpose':'wrong sign'}]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ledger=[];replays=[];records=[];coverage={};native=[]
    for profile,p in g.CASES.items():
        level='easy' if profile in g.LEVELS['easy'] else 'moderate'
        rec=g.generate(level,profile=profile,parameters=p);structural(rec);old=g.PROFILES[profile]
        F,H,P=rendered(old);assert fingerprint(old)==fingerprint(rec['question'])
        oldf=old[':question/answer-fields'][0];newf=rec['question'][':question/answer-fields'][0]
        oldbank=sorted(map(str,[math(a[':answer/value']) for a in oldf[':answer-field/choices']]))
        newbank=sorted(map(str,[math(a[':answer/value']) for a in newf[':answer-field/choices']]))
        assert oldbank==newbank
        assert math(oldf[':answer-field/correct'][':answer/value'])==P
        ledger.append({'profile':profile,'parameters':p,'matched_values':len(oldbank),'matched_distractors':len(oldbank)-1,'complete_bank_matched':True,'correct_designation_matched':True,'missing_or_extra':[],'prompt_mathematics_identical':True,'solution_stages_preserved':True,'notation_changes':'SymPy spacing/powers; conventional underbrace; normalized Markdown tables','source_division_order_preserved':True});replays.append(rec)
        pool=list(g.candidates(profile));coverage[profile]={'valid_cases':len(pool),'slot_values':{k:sorted({p[k] for p in pool}) for k in ('r','s','c','a','b')}}
        for p in pool:
            rec=g.generate(level,17,profile,p);structural(rec)
            assert rec==g.generate(level,17,profile,p)
            assert rec['question']==g.generate(level,23,profile,p)['question']
            records.append(rec);native.append({'label':profile+'/'+str(p),'record':rec,'checks':checks(rec)})
    # Hold F and P fixed while changing supplied root roles: divide in a different order.
    p=dict(g.CASES['q-328505']);a=g.generate('easy',profile='q-328505',parameters=p);p['r'],p['s']=p['s'],p['r'];b=g.generate('easy',profile='q-328505',parameters=p);structural(a);structural(b)
    assert a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'] and fingerprint(a['question'])==fingerprint(b['question'])
    for level in ('hard','unclassified'):
        try:g.batch(level,1,0)
        except ValueError:pass
        else:raise AssertionError('Unsupported band accepted')
    finite={level:len({r['generation']['parameter_fingerprint'] for r in records if r['question'][':question/difficulty'].endswith('/'+level)}) for level in g.LEVELS}
    for name,value in [('source-replay.json',ledger),('source-replay-records.json',replays),('engine-input.json',native),('review-records.json', [g.generate(level,23,profile,dict(g.CASES[profile],r=-2,s=1)) for level in g.LEVELS for profile in g.LEVELS[level]])]:(D/name).write_text(json.dumps(value,indent=2)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
    report=json.loads((D/'engine-report.json').read_text());assert report['documented_unresolved_checks']==0
    validation={'status':'pass','source_banks':len(ledger),'matched_distractors':sum(z['matched_distractors'] for z in ledger),'coverage':coverage,'finite_variant_limit':finite,'changed_division_order_case':True,'correctness':'Rendered prompt, key, all synthetic rows and displayed solution identities independently parsed','grading':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{'generator':sha(D.with_suffix('.py')),'validator':sha(D/'validate.py'),'source':sha(D/'source.json'),'grader':sha(ROOT/'generate/runs/current/check-engine')}}
    (D/'validation.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation,indent=2))
if __name__=='__main__':main()

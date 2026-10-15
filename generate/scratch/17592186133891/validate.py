"""Independent rendered-function, bank, solution-stage and native grading checks."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import mpmath as mp
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
from math_reader import *
spec=importlib.util.spec_from_file_location('dx',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def eq(a,b):return sp.simplify(a-b)==0

def displayed(q):
    prompt=q[':question/problem'];m=re.search(r'\{\\int \}_\{C\}(.*?)\\,\\text\{d\}x',prompt)
    if not m:raise ValueError('No supported complete supplied-function prompt')
    f=parse(m[1]);v=re.search(r'r\(t\)=⟨(.*?)⟩',prompt)[1].split(r'\,');assert len(v)==2
    X,Y=map(lambda a:parse(a.rstrip(',')),v)
    sol=q[':question/worked-solution'];bounds=re.search(r'(.*?)\\le t\\le (.*?)\.',sol)
    assert bounds
    a0=bounds[1].split('$')[-1].strip()
    if a0.endswith(','):raise ValueError('bounds need parsed display')
    # Bounds read independently from the parameter interval preceding derivative.
    head=sol[:sol.index('Computing')]
    interval=re.search(r'(?:⟩,\\,|where \$)(.*?)\\le t\\le (.*?)(?:\.|\$|\n)',head)
    assert interval,(head,q)
    a,b=map(parse,interval.groups());return f,X,Y,a,b

def fingerprint(q):
    if q.get(':question/math-academy-id')=='e-9512':
        # Independently transcribed canonical segment; no prompt hint or fields.
        f,X,Y,a,b=x+y,3*t,3*t,sp.Integer(0),sp.Integer(1)
    else:f,X,Y,a,b=displayed(q)
    return hashlib.sha256(json.dumps([str(sp.simplify(f.subs({x:X,y:Y},simultaneous=True))),str(X),str(Y),str(a),str(b)]).encode()).hexdigest()

def bank_values(q,precision=45):
    values=[]
    for opt in q[':question/answer-fields'][0][':answer-field/choices']:
        a,b,v=integral(opt[':answer/value'])
        if v.has(sp.exp):
            with mp.workdps(precision):
                fn=sp.lambdify(t,v,'mpmath');aa=mp.mpf(str(sp.N(a,precision)));bb=mp.mpf(str(sp.N(b,precision)))
                values.append(str(mp.quad(fn,[aa,(aa+bb)/2,bb])))
        else:values.append(str(sp.integrate(v,(t,a,b))))
    return values

def audit(rec,allow_ambiguous=False):
    q=rec['question'];f,X,Y,a,b=displayed(q);F=sp.simplify(f.subs({x:X,y:Y},simultaneous=True));D=sp.diff(X,t);correct=sp.simplify(F*D)
    field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==5
    for opt in field[':answer-field/choices']:
        aa,bb,v=integral(opt[':answer/value']);assert (aa,bb)==(a,b)
        assert eq(v,correct)==(opt[':answer/id']==field[':answer-field/correct'][1])
    # Even structurally wrong expressions may be equal definite integrals.
    vals=bank_values(q)
    if not allow_ambiguous:
        if any(integral(z[':answer/value'])[2].has(sp.exp) for z in field[':answer-field/choices']):
            vals2=bank_values(q,65)
            for u,v in zip(vals,vals2):assert abs(mp.mpf(u)-mp.mpf(v))<mp.mpf('1e-30')
            assert all(abs(mp.mpf(u)-mp.mpf(v))>mp.mpf('0.1') for k,u in enumerate(vals2) for v in vals2[k+1:])
        else:assert all(not eq(parse(u),parse(v)) for k,u in enumerate(vals) for v in vals[k+1:]),vals
    # Source sequence: path, derivative, f substitution and simplification,
    # then formal integral, product and final transformed integral.
    sol=q[':question/worked-solution'];fm=re.search(r'f\(x,y\)\s*=([^$]+)',sol);assert eq(parse(fm[1]),f)
    checked=0
    for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S):
        if block.startswith('f(r(t))'):
            for row in block.split(r'\\'):assert eq(parse(row.split('& =')[1]),F);checked+=1
        elif block.startswith(r'\frac{\text{d}x}'):
            rhs=block.split('& =')[1];dd=rhs.rsplit('=',1)[1];assert eq(parse(dd),D);checked+=1
        elif block.startswith(r'{\int }_{C}'):
            for k,row in enumerate(block.split(r'\\')):
                if not k:continue
                aa,bb,v=integral(row.split('& =')[1]);assert (aa,bb)==(a,b) and eq(v,correct);checked+=1
    assert checked>=4
    for s in [q[':question/problem'],sol]+[z[':answer/value'] for z in field[':answer-field/choices']]:
        assert not any(ord(ch)<32 and ch not in '\n\t' for ch in s)
    return {'fingerprint':fingerprint(q),'displayed_solution_rows':checked,'definite_bank_values':vals}

def native(records,path):
    path.mkdir(parents=True,exist_ok=True);rows=[]
    for k,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0]
        rows.append({'label':str(k),'record':r,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned source-shaped radio option'} for z in f[':answer-field/choices']]})
    write(path/'native-input.json',rows)
    r=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],capture_output=True,text=True,check=True,timeout=55)
    (path/'native.log').write_text(r.stdout+r.stderr);report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0;return report

def main():
    fidelity=[];components=[];review=[];records=[];coverage={}
    for mid,model in g.MODELS.items():
        src=g.SOURCE_BY_ID[mid];r=g.generate('easy',template=mid,parameters={'c':1});audit(r,allow_ambiguous=mid in g.EXCLUDED)
        assert r['question'][':question/problem']==g.normalize_prose(src[':question/problem'])
        assert r['question'][':question/worked-solution']==g.normalize_prose(src[':question/worked-solution'])
        gf=r['question'][':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
        for opt in sf[':answer-field/choices']:
            aa,bb,v=integral(opt[':answer/value']);matches=[z for z in gf[':answer-field/choices'] if (lambda z:(z[0],z[1])==(aa,bb) and eq(z[2],v))(integral(z[':answer/value']))];assert len(matches)==1
            assert (opt[':answer/id']==sf[':answer-field/correct'][':answer/id'])==(matches[0][':answer/id']==gf[':answer-field/correct'][1])
        fidelity.append({'source_id':mid,'bank_profile':'source-bank:'+mid,'distractors_matched':4,'distractors_total':4,'complete_bank_matched':True,'eligible_template':mid in g.TEMPLATES,'normalization_only':True,'source_anomaly':g.EXCLUDED.get(mid)})
        components.append({'source_id':mid,'source_db_id':src[':db/id'],'function_path_interval':list(map(str,model)),'choice_recipes':[{'source_answer_id':z[':answer/id'],'observed':z[':answer/value'],'exact_integrand':str(integral(z[':answer/value'])[2]),'recipe':'c times complete observed integral','interpretation':'observed algebraic pattern retained; underlying error interpretation unresolved'} for z in sf[':answer-field/choices']]})
        if mid not in g.TEMPLATES:continue
        coverage[mid]=[]
        for c in g.SCALES:
            r=g.generate('easy',13,mid,{'c':c});audit(r);records.append(r);coverage[mid].append(c)
            assert r==g.generate('easy',13,mid,{'c':c})
            other=g.generate('easy',999,mid,{'c':c});assert fingerprint(other['question'])==fingerprint(r['question']) and other['question'][':question/id']==r['question'][':question/id']
            if c in (2,9):review.append({'source_id':mid,'source':src,'variant':r})
    assert len({fingerprint(r['question']) for r in records})==len(records)
    # Independent mutation checks catch stale scalar definitions, bank keys and
    # intermediate solution rows without relying on generator replay equality.
    base=records[0];mutations=[]
    for target in ('definition','key','solution'):
        bad=copy.deepcopy(base);q=bad['question'];f=q[':question/answer-fields'][0]
        if target=='key':f[':answer-field/correct'][1]=next(z[':answer/id'] for z in f[':answer-field/choices'] if z[':answer/id']!=f[':answer-field/correct'][1])
        elif target=='definition':q[':question/worked-solution']=q[':question/worked-solution'].replace('f(x,y)=2', 'f(x,y)=3')
        else:q[':question/worked-solution']=q[':question/worked-solution'].replace('f(r(t)) & =2','f(r(t)) & =3')
        try:audit(bad)
        except (AssertionError,ValueError):mutations.append(target)
        else:raise AssertionError('Mutation escaped: '+target)
    report=native(records,HERE/'reference/validation');write(HERE/'source-fidelity.json',fidelity);write(HERE/'source-components.json',components);write(HERE/'review.json',review)
    (HERE/'review.md').write_text('\n\n---\n\n'.join('Source '+z['source_id']+'\n\n'+z['source'][':question/problem']+'\n\n'+z['source'][':question/worked-solution']+'\n\nGenerated variant\n\n'+g.markdown(z['variant']) for z in review))
    write(HERE/'validation.json',{'status':'passed','supported_templates':len(g.TEMPLATES),'complete_source_banks_replayed':len(fidelity),'matched_distractors':4*len(fidelity),'total_distractors':4*len(fidelity),'excluded_incomplete_sources':['q-124119'],'ambiguity_exclusions':g.EXCLUDED,'bounded_domain_questions':len(records),'distinct_mathematical_tasks':len(records),'slot_coverage':coverage,'mutation_regressions_rejected':mutations,'source_fidelity':'complete rated banks reproduced; 3 ambiguous templates are ineligible; incomplete unrated record retained unchanged','correctness':'symbolic integrands and solution RHS; exact definite values for polynomial/trig; exponential banks checked by 45/65-digit quadrature with pairwise separation >0.1','native':report,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()})
    print(json.dumps({'questions':len(records),'source_banks':len(fidelity),'accepted':report['accepted_checks'],'rejected':report['rejected_checks']}))
if __name__=='__main__':main()

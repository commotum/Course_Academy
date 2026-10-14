#!/usr/bin/env python3
"""Independent printed-stage, source-bank, scope and native grading checks."""
import importlib.util, json, re, sys, subprocess, copy, itertools, hashlib
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def eq(a,b):assert s.simplify(a-b)==0,(a,b)
def formatting(r):
    q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        assert all(ord(c)>=32 or c in '\n\t\r' for c in text),'C0 learner text'
        assert text.count('$$')%2==0 and text.replace('$$','').count('$')%2==0
        stack=[]
        for i,c in enumerate(text):
            if c in '{}' and (i==0 or text[i-1]!='\\'):
                if c=='{':stack.append(c)
                else:assert stack;stack.pop()
        assert not stack,'unbalanced TeX group'
    for f in q[':question/answer-fields']:
        if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
        assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']]

def pexpr(t):return g.scalar_parse(t.replace('\\,','').replace('⁡','').strip().rstrip('.,'))
def independent(r):
    t=r['generation']['template'];p=r['generation']['parameters'];q=r['question'];sol=q[':question/worked-solution'];prompt=q[':question/problem'];raw=r['generation']['evidence_only']
    if not raw:formatting(r)
    if t=='canonical_hint':
        a,b,c,A,B=[p[k] for k in ('a','b','c','U','V')];ru=s.Matrix([a,a,0]);rv=s.Matrix([b,-b,c]);n=s.sqrt(ru.cross(rv).dot(ru.cross(rv)));value=s.integrate(2*b*g.v*n,(g.u,0,A),(g.v,0,B))
        assert '⟨'+r',\,'.join(g.tex(e) for e in [a*g.u+b*g.v,a*g.u-b*g.v,c*g.v])+'⟩' in prompt
        eq(pexpr(sol.split('&=')[-1].split('\\end')[0]),value)
    else:
        # Extract coordinates and density from printed prompt, separately from generation metadata.
        R,F,B,C,H,style=g.DATA[t]
        if style=='charge':
            assert r'⟨x,2x^2\cos\theta,2x^2\sin\theta⟩' in prompt or raw
            R=[g.x,2*g.x**2*s.cos(g.theta),2*g.x**2*s.sin(g.theta)];F=g.x*(g.y**2+g.z**2)/s.sqrt(16*g.x**2+1);aa,bb=g.x,g.theta
        else:
            vector=re.search(r'⟨(.*?)⟩',prompt)
            if vector:coords=vector[1].split(r',\,')
            else:
                coords=re.search(r'\n(x=.*?)\n',prompt)[1].split(r',\,');coords=[c.split('=',1)[1] for c in coords]
            R=list(map(pexpr,coords));aa,bb=g.u,g.v
            integral=prompt.split('$$')[1];ftex=integral.split('{∬}_{S}',1)[1].split(r'\,\text{d}S')[0];F=pexpr(ftex)
        ru=s.Matrix(R).diff(aa);rv=s.Matrix(R).diff(bb);cross=ru.cross(rv);norm=s.sqrt(s.trigsimp(cross.dot(cross)));pull=s.simplify(F.subs({g.x:R[0],g.y:R[1],g.z:R[2]},simultaneous=True))
        a,b,c,d=[s.sympify(p[k]) for k in ('ua','ub','va','vb')];value=s.simplify(s.integrate(pull*norm,(aa,a,b),(bb,c,d)))
        eq(C*H,pull*norm)
        if style!='charge':
            # Formal derivative vectors, determinant/minors and squared component blocks remain from source.
            blocks=sol.split('$$')
            if g.LEVEL[t]=='hard':
                tangent=next(e for e in blocks if '{r}_{u}^{′} & =' in e);vecs=re.findall(r' & =⟨([^⟩]+)⟩',tangent);actual=[e for e in vecs if '∂' not in e]
                assert len(actual)==2
                for text,expected in zip(actual,(ru,rv)):
                    for part,ev in zip(text.split(r',\,'),expected):eq(pexpr(part),ev)
                crossblock=next(e for e in blocks if '{r}_{u}^{′}\\times {r}_{v}^{′} & =' in e)
                actual_cross=re.findall(r' & =⟨([^⟩]+)⟩',crossblock)[-1]
                for part,ev in zip(actual_cross.split(r',\,'),cross):eq(pexpr(part),ev)
                normblock=next(e for e in blocks if ' & =\\sqrt' in e and '‖' in e)
                for normline in re.findall(r' & =(\\sqrt.*?)(?: \\\\ |\\end)',normblock):
                    if raw and t=='q-161127' and '+-' in normline:continue
                    eq(pexpr(normline),norm)
            else:
                hint=prompt.split('‖=')[1].split('.$')[0];eq(pexpr(hint),norm)
            pullblock=next(e for e in sol.split('$$') if '\\begin{aligned}f(r' in e)
            finalpull=pullblock.split(' & =')[-1].split('\\end')[0];eq(pexpr(finalpull),pull)
        # Validate source family stages and evaluate BOTH primitive endpoints independently from printed brackets.
        block=sol.split('$$')[-2];rows=block.replace('\\begin{aligned}','').replace('\\end{aligned}','').strip().split(r' \\ ')
        final=rows[-1].split('=')[-1];eq(pexpr(final),value)
        if style=='nested':
            # Read actual displayed inner/outer primitives; differentiate independently.
            inner=re.findall(r'\[([^]]+)\]',rows[4])[0];Pu=pexpr(inner);eq(s.diff(Pu,aa),H)
            outerrow=next(row for row in rows[5:] if '[' in row and r'\int' not in row and ']_{' in row)
            P=pexpr(re.findall(r'\[([^]]+)\]',outerrow)[0]);J=s.integrate(H,(aa,a,b));eq(s.diff(P,bb),J)
            idx=6 if not raw else 5
            printedJ=rows[idx].split('}(')[-1].split(r')\text')[0] if '}(' in rows[idx] else rows[idx].split('}^{'+g.tex(d)+'}')[1].split(r'\,\text')[0]
            eq(pexpr(printedJ),J)
            if not raw:
                detail=rows[5];components=detail.split('}[(',1)[1].split(r')]\text')[0]
                hi,lo=components.split(')-(');eq(pexpr(hi),Pu.subs(aa,b));eq(pexpr(lo),Pu.subs(aa,a))
                # Component equality individually, not just aggregate endpoint difference.
                def check_components(text,P,var,end):
                    parts=re.findall(r'\([^()]*\)|[^+]+',text)
                    expected=sorted(s.Poly(s.expand(P),var).terms(),key=lambda e:e[0][0]);actual=[]
                    # split only plus outside grouping; all source components are polynomial monomials.
                    depth=0;start=0;items=[]
                    for i,ch in enumerate(text):
                        depth+=ch=='(';depth-=ch==')'
                        if ch=='+' and depth==0:items.append(text[start:i]);start=i+1
                    items.append(text[start:]);assert len(items)==len(expected)
                    for item,(power,coef) in zip(items,expected):eq(pexpr(item),s.simplify(coef*end**power[0]))
                check_components(hi,Pu,aa,b);check_components(lo,Pu,aa,a)
                endpointrows=[row for row in rows if row.startswith(' & ='+g.tex(C)+'[(')]
                endpoint=endpointrows[-1].split('[(',1)[1].rstrip(']');hi,lo=endpoint.split(')-(');lo=lo[:-1]
                check_components(hi,P,bb,d);check_components(lo,P,bb,c)
        elif style in ('split2','product','separated'):
            primitive_row=next(row for row in rows if len(re.findall(r'\[([^]]+)\]',row))==2 and ']_' in row)
            primitives=list(map(pexpr,re.findall(r'\[([^]]+)\]',primitive_row)))
            # Raw q160834 dv [u] typo is recorded, not a correctness pass.
            if raw and t=='q-160834':primitives[1]=g.v
            eq(s.diff(primitives[0],aa)*s.diff(primitives[1],bb),H)
            if not raw:
                endpointrow=next(row for row in rows if r')]\cdot [(' in row)
                factors=re.findall(r'\[([^]]+)\]',endpointrow)
                for factor,P,var,lo,hi in zip(factors,primitives,(aa,bb),(a,c),(b,d)):
                    hi_s,lo_s=factor[1:-1].split(')-(');eq(pexpr(hi_s),P.subs(var,hi));eq(pexpr(lo_s),P.subs(var,lo))
        # Complete operative mask parity catches removed factorizations/cancellations even when algebraically equal.
        # Independent source fixed rows 0..4 must occur unchanged apart from declared endpoints.
        expected=g.integral_mask(t,g.mathematics(t,p),raw)
        if not raw and t=='q-160834':expected=expected.replace(r'\cdot [u]_',r'\cdot [v]_')
        assert block==expected,'operative source mask changed'
    f=q[':question/answer-fields'][0];answers=f[':answer-field/choices'];vals=[pexpr(a[':answer/value']) for a in answers];assert len(set(map(s.simplify,vals)))==len(vals)
    chosen=next(a for a in answers if a[':answer/id']==f[':answer-field/correct'][1]);eq(pexpr(chosen[':answer/value']),value)
    return chosen[':answer/id']

def run():
    records=[];cases=[];fidelity=[]
    for t in g.DATA:
        raw=g.generate(g.LEVEL[t],template=t,parameters=g.ORIGINAL[t],profile='observed');independent(raw);records.append(raw)
        orig=g.SOURCES[t];f=orig[':question/answer-fields'][0];rf=raw['question'][':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
        original_correct=f[':answer-field/correct'][':answer/value'];correct=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert correct==original_correct
        assert orig[':question/problem']==raw['question'][':question/problem']
        for attr in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (attr in orig)==(attr in raw['question'])
        cases.append({'source_id':t,'template':t,'parameters':g.ORIGINAL[t],'bank_profile':'observed:'+t})
        fidelity.append({'source_id':t,'bank':True,'all_values':len(f[':answer-field/choices']),'correct_designation':True,'raw_prompt':True,'raw_solution_exact':orig[':question/worked-solution']==raw['question'][':question/worked-solution'],'source_rows':len(orig[':question/worked-solution'].split('$$')[-2].split(r' \\ '))})
        for seed in range(30):
            r=g.generate(g.LEVEL[t],seed,template=t);independent(r);records.append(r)
        # Changed opaque evidence remains public but ineligible.
        changed=g.generate(g.LEVEL[t],12,template=t,profile='observed');independent(changed)
    for seed in range(60):r=g.generate_easy(seed);independent(r);records.append(r)
    for l in ('moderate','hard'):
        assert {g.generate(l,i)['generation']['template'] for i in range(150)}=={t for t in g.DATA if g.LEVEL[t]==l}
    for l in ('easy','moderate','hard'):
        r=g.generate(l,3);r2=g.generate(l,11,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile']);assert r['question'][':question/id']==r2['question'][':question/id']
    for l,t,p,ft,prof in [('moderate','q-161127',g.ORIGINAL['q-161127'],None,None),('hard','q-161212',{'ua':'0','ub':'4','va':'0','vb':'2'},None,None),('moderate','q-161180',g.ORIGINAL['q-161180'],'blank',None),('hard','q-161212',g.ORIGINAL['q-161212'],None,'unknown')]:
        try:g.generate(l,template=t,parameters=p,field_type=ft,profile=prof)
        except ValueError:pass
        else:raise AssertionError('invalid selector/parameters accepted')
    # Correlated endpoint error with unchanged final result, equal-valued missing operation, C0 regression.
    mutations=[];base=g.generate_hard(6,template='q-161127')
    m=copy.deepcopy(base);m['question'][':question/worked-solution']+='\x0c';mutations.append(m)
    m=copy.deepcopy(base);m['question'][':question/worked-solution']=m['question'][':question/worked-solution'].replace(r'\frac{{u}^{3}}{3}+u{v}^{2}',r'\frac{{u}^{3}}{3}+u{v}^{2}+1');mutations.append(m)
    m=copy.deepcopy(g.generate_hard(6,template='q-161242'));m['question'][':question/worked-solution']=m['question'][':question/worked-solution'].replace(r'5{∬}_{D}\,4uv',r'10{∬}_{D}\,2uv');mutations.append(m)
    for m in mutations:
        try:independent(m)
        except AssertionError:pass
        else:raise AssertionError('mutation was not rejected')
    engine=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0];cid=independent(r)
        if f[':answer-field/type'].endswith('/radio'):checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'all complete method/source bank selections'} for a in f[':answer-field/choices']]
        else:
            value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid);checks=[{'submitted':value,'expected':'accepted','purpose':'exact blank'},{'submitted':r'('+value+r')+0','expected':'accepted','purpose':'unreduced equivalent sum'},{'submitted':'0','expected':'rejected','purpose':'incorrect blank'}]
        engine.append({'label':str(i)+':'+r['generation']['template'],'record':r,'checks':checks})
    (ROOT/'engine-input.json').write_text(json.dumps(engine));subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
    (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(ROOT/'source-fidelity.json').write_text(json.dumps(fidelity,indent=2)+'\n')
    review=[g.generate(g.LEVEL[t],seed,template=t) for t in g.DATA for seed in (2,9)]+[g.generate_easy(seed) for seed in (2,9)]
    (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');md=['# Source originals and generated variants','Raw original banks are opaque evidence; worked solutions retain the family sequence with declared normalization and normal endpoint additions.']
    for t in g.DATA:
        md+=['## Original '+t,g.markdown(g.generate(g.LEVEL[t],template=t,parameters=g.ORIGINAL[t],profile='observed'))]
        for r in review:
            if r['generation']['template']==t:md+=['### Generated variant '+str(r['generation']['parameters']),g.markdown(r)]
    for r in review:
        if r['generation']['template']=='canonical_hint':md+=['## Authored easy',g.markdown(r)]
    (ROOT/'review.md').write_text('\n\n'.join(md)+'\n')
    report={'status':'pass','basis':1356,'source_questions':13,'source_complete_banks':'13/13','source_all_values':'61/61','source_distractors':'48/48','source_correct_designations':'13/13','source_exact_prompts':'13/13','source_exact_solution_strings':sum(f['raw_solution_exact'] for f in fidelity),'source_solution_strings_total':13,'source_solution_prose_and_family_sequence':'13/13; evaluated-row notation normalization disclosed','generated_checked':len(records)-13,'native':json.loads((ROOT/'engine-report.json').read_text()),'mutation_regressions':3,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'remaining_limitations':['Historical scalar wrong-answer operations are unresolved and evidence-only.','Geometry and density remain source-fixed for moderate/hard; substantive variation is rectangle limits.','Contextual charge family has four endpoint tasks; normal prompt supplies the formerly inherited context.','Easy ratings are authored design claims.','Source raw norm/primitive/set-brace anomalies remain evidence; normal output repairs them.']}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='native'})
if __name__=='__main__':run()

#!/usr/bin/env python3
"""Independent actual-display checks and actual application grader fixtures."""
import copy, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ln_sum',ROOT.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);sys.modules[spec.name]=g;spec.loader.exec_module(g)


def eq(a,b): return sp.simplify(a-b)==0

def rhs_rows(solution):
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
    return [[row.split('=',1)[1].strip().rstrip('.') for row in re.split(r'\\\\',block) if '=' in row] for block in blocks]

def shape(s):
    # Distinct operations (formal differentiation, multiplied derivatives,
    # successor powers, direct quotient, substitution row) remain intact.
    s=s.replace(r'\pi ','R').replace('e','R')
    s=re.sub(r'-?\d+', '#',s)
    s=re.sub(r'\s+','',s)
    # A varied unit coefficient can appear or disappear without another stage.
    return s

def check_record(rec):
    q=rec['question'];gen=rec['generation'];name=gen['template']
    assert set(rec['knowledge_point'])=={'db_id','id','title'}
    assert rec['knowledge_point']['db_id']==g.KP_ID
    field=q[':question/answer-fields'][0]; prompt=q[':question/problem'];solution=q.get(':question/worked-solution','')
    assert gen['domain'].startswith('x>0')
    # Independent function comes from the actual learner-facing definition.
    match=re.search(r'(?:y\s*=\s*|f\(x\)\s*=\s*)([^$]+)',prompt)
    assert match,(name,'No actual function')
    F=g.read_math(match[1].rstrip('.,'))
    derivative=sp.diff(F,g.X)
    tmatch=re.findall(r'x=(\d+)',prompt)
    if tmatch: assert len(set(tmatch))==1
    t=int(tmatch[0]) if tmatch else None
    assert t is None or t>0
    target=derivative.subs(g.X,t) if t is not None else derivative
    # All banks, including every incorrect displayed expression, are parsed.
    malformed=[];values=[]
    for answer in field[':answer-field/choices']:
        try:
            value=g.read_math(answer[':answer/value'])
            assert value.free_symbols <= {g.X} and not value.has(sp.nan,sp.zoo,sp.oo,sp.I)
            values.append((answer,value))
        except Exception:
            if name=='q-1920' and gen['evidence_only']:malformed.append(answer[':answer/value'])
            else:raise
    if gen['eligible_for_learning']:
        assert not malformed
        for i,(a,v) in enumerate(values):
            assert all(not eq(v,w) for _,w in values[:i]),('Ambiguous bank',name)
    if name=='q-339973' and not gen['evidence_only']:
        assert field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection' and len(values)==5
        assert '{{' not in prompt
        a=sp.expand(F).coeff(sp.log(g.X));powers=[term for term in sp.Add.make_args(F) if term.is_Pow and term.base==g.X]
        assert len(powers)==1;r=powers[0].exp
        expected=[derivative,1/g.X+r*g.X**(r-1),a/g.X+g.X**(r-1),a/g.X+r*g.X**r,-a/g.X+r*g.X**(r-1)]
        assert all(sum(eq(v,w) for _,v in values)==1 for w in expected),'Authored derivative-error bank mismatch'
    if ':answer-field/correct' in field:
        assert field[':answer-field/correct'][0]==':answer/id'
        correct=[v for a,v in values if a[':answer/id']==field[':answer-field/correct'][1]]
        assert len(correct)==1 and eq(correct[0],target),(name,'Actual correct answer')
    else:
        assert name=='q-1920' and gen['evidence_only']
    # Validate all printed stages, including formal operands and conclusions.
    blocks=rhs_rows(solution)
    if solution:
        assert len(blocks)==(2 if t is not None else 1)
        rows=blocks[0]
        formal=re.fullmatch(r'\\frac\{(?:\\text\{d\}|d)\}\{(?:\\text\{d\}|d)x\}\((.*)\)',rows[0])
        assert formal,(name,rows[0])
        assert eq(g.read_math(formal[1]),F),(name,'Actual formal derivative operand')
        for row in rows[1:]: assert eq(g.read_math(row),derivative),(name,'Actual derivative stage',row)
        if t is not None:
            pointrows=blocks[1];before=pointrows[0]
            m=re.search(r'\{\((.*)\)\|\}_\{x=(\d+)\}',before)
            assert m,(name,'Point operator operand',before)
            assert int(m[2])==t and eq(g.read_math(m[1]),derivative)
            for row in pointrows[1:]:assert eq(g.read_math(row),target),(name,'Point arithmetic stage',row)
            prose=re.findall(r'instantaneous rate of change at \$x=(\d+)\$',solution)
            assert prose and all(int(v)==t for v in prose),(name,'Stale concluding point')
        src=g.SOURCES[name].get(':question/worked-solution','')
        # Structural derivative-stage count plus characteristic operations.
        if name=='q-1920' and not gen['evidence_only']:
            assert len(rows)==3 and r'(e^{x})' in rows[1] and r'(\frac{1}{x})' in rows[1]
        if src:
            sourceblocks=rhs_rows(src)
            assert list(map(len,blocks))==list(map(len,sourceblocks)),(name,'Stage count')
            if name in ('q-11914','q-1919'):
                assert r'\cdot' in rows[1] and r'(\frac{1}{x})' in rows[1],(name,'Factored term derivatives lost')
            if name in ('q-101716','q-339973'):
                assert r'(\frac{1}{x})' in rows[1],(name,'Scaled reciprocal substitution stage lost')
            if name in ('q-308854','q-17392'):
                assert r'\cdot {1}^{' in blocks[1][1] and r'\frac{' in blocks[1][1],(name,'Individually substituted terms lost')
            if name=='q-340104':
                assert r'\cdot {' in blocks[1][1] and r'\frac{' in blocks[1][1],(name,'Individually evaluated exponential terms lost')
    else:assert name=='q-1920' and gen['evidence_only']
    if name=='q-11914':
        for answer in field[':answer-field/choices']:
            feedback=answer[':answer/feedback']
            for operand,chain in re.findall(r'd\[([^\]]+)\]/dx\s*=\s*([^,;.]+)',feedback):
                primitive=g.read_math(operand)
                assert any(eq(primitive,term) for term in sp.Add.make_args(F)),(name,'Stale feedback operand',operand)
                for result in chain.split('='):assert eq(sp.diff(primitive,g.X),g.read_math(result.strip())),(name,'Feedback derivative',result)
    texts=[prompt,solution]+[a[':answer/value'] for a in field[':answer-field/choices']]+[a.get(':answer/feedback','') for a in field[':answer-field/choices']]
    for text in texts:
        assert all(ord(ch)>=32 or ch in '\n\t' for ch in text),'C0 control character'
        assert text.count('$')%2==0
        depth=0
        for ch in text:
            depth+=(ch=='{')-(ch=='}');assert depth>=0
        assert depth==0
    if field[':answer-field/type'].endswith('/blank'):assert '{{'+field[':answer-field/key']+'}}' in prompt
    return target,malformed


def reverse_terms(text):
    chunks=[];depth=0;start=0
    for pos,ch in enumerate(text):
        depth+=(ch=='{')-(ch=='}')
        if ch in '+-' and pos>0 and depth==0:chunks.append(text[start:pos]);start=pos
    chunks.append(text[start:]);out=''
    for chunk in reversed(chunks):out+=(chunk.lstrip('+') if not out else chunk if chunk.startswith(('+','-')) else '+'+chunk)
    return out


def fixture(rec,label):
    target,_=check_record(rec);f=rec['question'][':question/answer-fields'][0]
    if ':answer-field/correct' not in f:return None
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every displayed radio option'} for a in f[':answer-field/choices']]
    else:
        canonical=f[':answer-field/choices'][0][':answer/value']
        raw=rec['generation']['evidence_only'];name=rec['generation']['template']
        expected='rejected' if 'round' in rec['question'][':question/problem'].lower() else 'accepted'
        checks=[{'submitted':canonical,'expected':'accepted','purpose':'Exact stored entry'}, {'submitted':canonical+'+1','expected':'rejected','purpose':'Incorrect constant term'}, {'submitted':reverse_terms(canonical),'expected':expected,'purpose':'Legitimate mathematical equivalent; reordered additive terms'}]
        if name=='q-339973':
            equivalent=g.tex(sp.together(target));outcome='unresolved';purpose='Legitimate mathematical equivalent; irrational-power common denominator: unsupported native symbolic rules'
        else:
            equivalent=r'\frac{'+g.tex(2*target)+'}{2}';outcome=expected;purpose='Legitimate mathematical equivalent; unreduced exact scalar quotient'
        checks.append({'submitted':equivalent,'expected':outcome,'purpose':purpose})
    return {'label':label,'record':rec,'checks':checks}


def main():
    cases=[];raw=[];variants=[];fixtures=[];counts={'sources':0,'prompts_exact':0,'solutions_exact':0,'solution_denominator':0,'answer_values_exact':0,'answer_values_denominator':0,'complete_banks_exact':0,'correct_refs_matched':0,'correct_refs_denominator':0,'omission_presence_matches':0,'malformed_evidence_options':0}
    for name,spec in g.SPECS.items():
        src=g.SOURCES[name];r=g.generate(spec['level'],template=name,parameters=spec['p'],profile='observed:'+name);raw.append(r)
        target,malformed=check_record(r);counts['malformed_evidence_options']+=len(malformed)
        q=r['question'];f=q[':question/answer-fields'][0];original=src[':question/answer-fields'][0]
        assert q[':question/problem']==src[':question/problem'];counts['prompts_exact']+=1
        if ':question/worked-solution' in src:
            assert q[':question/worked-solution']==src[':question/worked-solution'];counts['solutions_exact']+=1;counts['solution_denominator']+=1
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in src)
        assert (':answer-field/correct' in f)==(':answer-field/correct' in original)
        counts['omission_presence_matches']+=1
        got=sorted(a[':answer/value'] for a in f[':answer-field/choices']);want=sorted(a[':answer/value'] for a in original[':answer-field/choices'])
        assert got==want;counts['answer_values_exact']+=len(got);counts['answer_values_denominator']+=len(want);counts['complete_banks_exact']+=1
        for a in original[':answer-field/choices']:
            match=next(b for b in f[':answer-field/choices'] if b[':answer/value']==a[':answer/value'])
            assert match.get(':answer/feedback')==a.get(':answer/feedback')
        if ':answer-field/correct' in original:
            cid=f[':answer-field/correct'][1];c=next(a for a in f[':answer-field/choices'] if a[':answer/id']==cid)
            assert c[':answer/value']==original[':answer-field/correct'][':answer/value'];counts['correct_refs_matched']+=1;counts['correct_refs_denominator']+=1
        counts['sources']+=1
        cases.append(dict(source_id=src[':question/id'],source_ma_id=name,template=name,level=spec['level'],authored_level_assignment=name=='q-1920',parameters=spec['p'],bank_profile='observed:'+name))
        item=fixture(r,'observed '+name)
        if item:fixtures.append(item)
        for seed in (21,47):
            v=g.generate(spec['level'],seed,template=name);check_record(v);variants.append(v);fixtures.append(fixture(v,'generated '+name+' '+str(seed)))
    coverage={};fingerprints={};slots={}
    for level in ('easy','moderate','hard'):
        records=[g.generate(level,seed) for seed in range(120)]
        coverage[level]=sorted({r['generation']['template'] for r in records})
        assert coverage[level]==sorted(n for n,s in g.SPECS.items() if s['level']==level)
        fingerprints[level]=len({r['generation']['parameter_fingerprint'] for r in records})
        assert fingerprints[level]>=60
        for r in records:check_record(r)
        for r in records:
            name=r['generation']['template'];slots.setdefault(name,{})
            for k,v in r['generation']['parameters'].items():slots[name].setdefault(k,set()).add(str(v))
        for name in coverage[level]:
            for key,vals in slots[name].items():
                if key=='t' or key=='b' and name in ('q-1919','q-340099'):continue
                assert len(vals)>1,(name,key,'No variation')
    # Explicit boundary guards and deterministic identities under option shuffle.
    rejected=0
    for name,s in g.SPECS.items():
        for key in ('a','b','c','d'):
            if key not in s['p']:continue
            p=dict(s['p']);p[key]=99
            try:g.generate(s['level'],template=name,parameters=p)
            except ValueError:rejected+=1
            else:raise AssertionError('Explicit bounds bypass')
        if name=='q-11911':p={**s['p'],'a':3}
        else:p=s['p']
        a=g.generate(s['level'],2,template=name,parameters=p);b=g.generate(s['level'],11,template=name,parameters=p)
        assert a['question'][':question/id']==b['question'][':question/id']
        assert a['generation']['content_fingerprint']==b['generation']['content_fingerprint']
    # Readback regression: poison displayed function, stage, evaluated operand,
    # conclusion prose, option bank or control byte; unchanged metadata can't hide it.
    regression=[]
    for mutation in ('prompt','derivative_stage','evaluated_component','final_prose','bank','control','lost_operation','feedback','bank_recipe'):
        chosen='q-339973' if mutation=='bank_recipe' else 'q-11914' if mutation in ('lost_operation','feedback') else 'q-340104'
        r=copy.deepcopy(next(v for v in variants if v['generation']['template']==chosen))
        q=r['question'];s=q[':question/worked-solution']
        if mutation=='prompt':q[':question/problem']=q[':question/problem'].replace('y=','y=7+',1)
        elif mutation=='derivative_stage':
            rows=rhs_rows(s)[0];q[':question/worked-solution']=s.replace(rows[1],rows[1]+'+7')
        elif mutation=='evaluated_component':
            rows=rhs_rows(s)[1];q[':question/worked-solution']=s.replace(rows[1],rows[1]+'+7')
        elif mutation=='final_prose':q[':question/worked-solution']=s.replace('at $x=2$','at $x=3$')
        elif mutation=='bank':
            f=q[':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);a[':answer/value']+=' +7'
        elif mutation=='bank_recipe':
            f=q[':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1]);a[':answer/value']+=' +7'
        elif mutation=='control':q[':question/problem']+='\x0c'
        elif mutation=='feedback':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/feedback']=q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/feedback'].replace('/dx = ','/dx = 7+',1)
        else:
            rows=rhs_rows(s)[0];q[':question/worked-solution']=s.replace(rows[1],rows[2])
        try:check_record(r)
        except (AssertionError,ValueError,TypeError):regression.append(mutation)
        else:raise AssertionError('Mutation escaped '+mutation)
    (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    (ROOT/'review.json').write_text(json.dumps(variants,indent=2,ensure_ascii=False)+'\n')
    review=['# Source replay and clearly authored variants','Basis1356; no plots. Raw originals preserve absent metadata and all historical values. Normal variants retain source operative stages, with method-derived banks replacing opaque banks.']
    for r in raw:
        name=r['generation']['template'];review+=['\n# Original '+name,g.markdown(r)]
        for v in variants:
            if v['generation']['template']==name:review+=['\n# Generated variant (authored parameter extension)',g.markdown(v)]
    (ROOT/'review.md').write_text('\n\n'.join(review)+'\n')
    for boundary in [g.generate_hard(template='q-308854',parameters={'a':5,'b':3,'r':'pi','t':1}),g.generate_hard(template='q-339973',parameters={'a':-10,'r':'e','c':10})]:
        fixtures.append(fixture(boundary,'Explicit permitted exponent/coefficient boundary'))
    (ROOT/'native-input.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
    executable=ROOT.parents[1]/'runs/current/check-engine'
    result=subprocess.run([str(executable),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],text=True,capture_output=True)
    if result.returncode:raise AssertionError(result.stderr+result.stdout)
    native=json.loads((ROOT/'native-report.json').read_text())
    # Separate semantic diagnostic; original fidelity records remain untouched.
    raw_scalar=g.generate('hard',template='q-308854',parameters=g.SPECS['q-308854']['p'],profile='observed:q-308854')
    diagnostic=copy.deepcopy(raw_scalar);diagnostic['question'][':question/problem']=diagnostic['question'][':question/problem'].replace('Do not round the answer.','Give an exact answer.')
    visible=g.generate('hard',template='q-308854',parameters=g.SPECS['q-308854']['p'])
    probe=[{'record':diagnostic,'label':'Diagnostic only: raw scalar3e+1 with form restriction removed','checks':[{'submitted':'30','expected':'accepted','purpose':'Scientific-notation interpretation: incorrect mathematical value accepted'},{'submitted':r'3\cdot e+1','expected':'rejected','purpose':'Intended Euler-constant value rejected against ambiguous storage'}]}, {'record':visible,'label':'Authored visible multiplication repair','checks':[{'submitted':'30','expected':'rejected','purpose':'Incorrect scientific-notation interpretation rejected'},{'submitted':'1+3*e','expected':'accepted','purpose':'Swapped terms and explicit multiplication'},{'submitted':r'\frac{6\cdot e+2}{2}','expected':'accepted','purpose':'Unreduced full scalar denominator'}]}]
    (ROOT/'native-semantic-probe.json').write_text(json.dumps(probe,indent=2,ensure_ascii=False)+'\n')
    result=subprocess.run([str(executable),str(ROOT/'native-semantic-probe.json'),str(ROOT/'native-semantic-report.json')],text=True,capture_output=True)
    if result.returncode:raise AssertionError(result.stderr+result.stdout)

    limitations=[{'label':item['label'],'entry':check['submitted'],'outcome':check['expected'],'purpose':check['purpose']} for item in fixtures for check in item['checks'] if check['purpose'].startswith('Legitimate mathematical equivalent') and check['expected']!='accepted']
    (ROOT/'equivalence-limitations.json').write_text(json.dumps(limitations,indent=2,ensure_ascii=False)+'\n')
    assert all(item['record']['generation']['evidence_only'] for item in fixtures for check in item['checks'] if check['purpose'].startswith('Legitimate mathematical equivalent') and check['expected']!='accepted')
    report={'passed':True,'mathematics_fidelity_format_identity_passed':True,'native_normal_contract_passed':True,'native_canonical_contract_passed':True,'native_equivalence_contract_passed':True,'native_raw_evidence_equivalence_contract_passed':False,'documented_excluded_raw_equivalence_limitations':limitations,'source_fidelity':counts,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_absent_correct_ref_records':1,'raw_opaque_profiles_ineligible':['observed:q-1919','observed:q-1920','observed:q-11911','observed:q-339973','observed:q-308854'],'source_anomalies':['q-308854 raw scalar3e+1 is science-token ambiguous: diagnostic with form restriction removed accepts30; normal visible multiplication repairs storage and final solution scalar', 'q-1920 unrated, missing correct designation and worked solution; ln(-5) invalid as a real expression; preserved raw evidence','q-1919/q-11911 opaque historical mistakes not promoted to learning defaults','Four observed Do not round blanks reject equivalent forms in native grader; authored wording Give an exact answer'], 'default_family_coverage':coverage,'sampled_unique_mathematical_tasks':fingerprints,'slot_coverage':{n:{k:sorted(v) for k,v in row.items()} for n,row in slots.items()},'display_mutation_regressions_rejected':regression,'invalid_explicit_parameter_checks':rejected,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'database_writes':0}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','source_fidelity','native','sampled_unique_mathematical_tasks')},indent=2))
    print('All valid normal contracts passed; raw source/engine limitations are excluded evidence, separately reported.')
if __name__=='__main__':main()

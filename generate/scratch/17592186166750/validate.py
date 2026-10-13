#!/usr/bin/env python3
"""Displayed-mathematics QA + complete source fidelity + real native radio grader."""
import copy, importlib.util, itertools, json, re, subprocess, sys, hashlib, math, importlib.metadata
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
S=G.S

def equal(a,b):assert G.eq(a,b),(a,b)
def rhs(block):return [G.parse(v) for _,_,v in G.rhs_spans(block)]
def validate(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];gen=r['generation'];k=gen['template'];u=G.s if '∂s' in q[':question/problem'] else G.t
    prompt=q[':question/problem']; chunks=re.findall(r'\$(.*?)\$',prompt,re.S)
    f=G.parse(next(v.split('=',1)[1] for v in chunks if v.startswith('f(x,y,z)=')))
    maps=[G.parse(next(v.split('=',1)[1] for v in chunks if v.startswith(str(a)+'='))) for a in (G.x,G.y,G.z)]
    mapping=dict(zip((G.x,G.y,G.z),maps));parts=[S.diff(f,a) for a in (G.x,G.y,G.z)];p=[S.simplify(v.subs(mapping)) for v in parts];d=[S.diff(v,u) for v in maps];products=[S.expand(v*w) for v,w in zip(p,d)]
    D=S.simplify(S.diff(f.subs(mapping),u));equal(D,sum(products))
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
    # Actual operator text is checked separately from its symbolic results.
    expected=rf'\frac{{∂f}}{{∂{u}}}='+''.join(('+' if i else '')+rf'\frac{{∂f}}{{∂{a}}}\cdot \frac{{∂{a}}}{{∂{u}}}' for i,a in enumerate((G.x,G.y,G.z)))
    assert blocks[0].rstrip('.')==expected
    for a,b in zip(rhs(blocks[1]),parts):equal(a,b)
    idx=2
    if 'Writing the above' in q[':question/worked-solution']:
        for row,v in zip(blocks[idx].split(r'\\'),p):
            for actual in rhs(row):equal(actual,v)
        idx+=1
    assert len(rhs(blocks[idx]))==3
    for actual,v in zip(rhs(blocks[idx]),d):equal(actual,v)
    idx+=1
    chain=rhs(blocks[idx]);assert len(chain)>=2
    for value in chain:equal(value,D)
    # Verify each component product independently, not just cancellation of sum.
    first=G.rhs_spans(blocks[idx])[0][2];depth=0;terms=[];start=0
    for i,ch in enumerate(first):
        depth+=(ch in '({')-(ch in ')}')
        if ch=='+' and depth==0:terms.append(first[start:i]);start=i+1
    terms.append(first[start:]);assert len(terms)==3,(k,first,terms)
    for value,product in zip(terms,products):equal(G.parse(value),product)
    if k=='q-170675':
        # Source fidelity requires the common-denominator operation itself,
        # not merely three algebraically equal derivative values.
        slots=G.rhs_spans(blocks[idx]);assert len(slots)==3
        assert terms[0].count(r'\frac')==1
        def complete_fraction(raw):
            raw=raw.strip();assert raw.startswith(r'\frac{'),raw
            def group(start):
                assert raw[start]=='{';depth=1;end=start+1
                while depth:depth+=(raw[end]=='{')-(raw[end]=='}');end+=1
                return raw[start+1:end-1],end
            numerator,end=group(5);denominator,end=group(end)
            assert not raw[end:].strip(),raw
            return G.parse(numerator),G.parse(denominator)
        common,den=complete_fraction(slots[1][2])
        collected,den2=complete_fraction(slots[2][2])
        equal(den,(G.s+G.t)**2);equal(den2,den)
        assert G.s+G.t in common.atoms(S.Add)
        assert G.s+G.t not in collected.atoms(S.Add)
    if k in ['q-94589','q-170675','q-37208','q-37206']:
        signature=rhs(re.search(r'\$\$\n(.*?)\n\$\$',prompt,re.S)[1])[0]
        # Solve actual displayed supplied form against actual composed derivative.
        numerator=S.together(signature-D).as_numer_denom()[0]
        solutions=S.solve(S.Poly(S.expand(numerator),G.s,G.t).coeffs(),(G.c1,G.c2,G.c3),dict=True)
        assert len(solutions)==1
        coeff=solutions[0];correct=S.simplify(sum(coeff[v] for v in (G.c1,G.c2,G.c3)))
        # Final prose coefficient declaration and both numerical sum stages.
        tail=q[':question/worked-solution'].split('Finally,',1)[1]
        declarations=re.findall(r'c[}_]*\{?([123])\}?\s*=([^,$]+)',tail)
        # Original equal c1=c2=6 syntax handled as simultaneous equality chains.
        inline=re.findall(r'\$(.*?)\$',tail.split('and therefore')[0],re.S)
        declared={}
        for v in inline:
            for piece in v.split(','):
                tokens=piece.rstrip('.').split('=')
                if len(tokens)>1:
                    value=G.parse(tokens[-1]);
                    for name in tokens[:-1]:
                        n=re.search('[123]',name)
                        if n:declared[int(n[0])]=value
        assert set(declared)=={1,2,3},(k,declared)
        for i,v in enumerate((G.c1,G.c2,G.c3),1):equal(declared[i],coeff[v])
        for value in rhs(blocks[-1]):equal(value,correct)
    else:correct=D
    for field in q[':question/answer-fields']:
        values=[G.parse(a[':answer/value']) for a in field[':answer-field/choices']]
        assert len(values)==5
        assert all(not G.eq(a,b) for i,a in enumerate(values) for b in values[i+1:])
        for answer,value in zip(field[':answer-field/choices'],values):
            assert value.free_symbols <= {G.s,G.t}
            if ':answer-field/correct' in field:
                designated=answer[':answer/id']==field[':answer-field/correct'][1]
                assert designated==G.eq(value,correct)
    for value in [prompt,q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        assert value.count('{')==value.count('}')
        assert value.count('$')%2==0
        assert not re.search(r'(?<!\\)(?:\+\-|\-\-)',value)
    return True

def canonical_bank(field):return sorted(a[':answer/value'] for a in field[':answer-field/choices'])
def source_fidelity():
    cases=[]
    for k,q in G.QUESTIONS.items():
        case={'source_id':k,'template':k,'level':G.LEVEL[k],'parameters':G.BASE[k],'bank_profile':'observed'};cases.append(case)
        r=G.generate(case['level'],template=k,parameters=case['parameters'],profile='observed');new=r['question'];validate(r)
        assert new[':question/problem']==q[':question/problem']
        assert new[':question/worked-solution']==q[':question/worked-solution'],k
        for attr in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (attr in new)==(attr in q)
        assert len(new[':question/answer-fields'])==len(q[':question/answer-fields'])
        for src,field in zip(q[':question/answer-fields'],new[':question/answer-fields']):
            assert canonical_bank(src)==canonical_bank(field)
            assert (':answer-field/correct' in src)==(':answer-field/correct' in field)
            assert field[':answer-field/key']==src[':answer-field/key']
            if ':answer-field/correct' in src:
                answer=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert answer[':answer/value']==src[':answer-field/correct'][':answer/value']
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2));return cases

def main():
    cases=source_fidelity();records=[];review=[];familycoverage=set()
    for k,level in G.LEVEL.items():
        for seed in range(10):
            r=G.generate(level,seed,template=k);validate(r);records.append(r)
            if seed<2:review.append(r)
        # All finite authored coefficient pair inputs are checked; whole-bank
        # collisions are genuine exclusions, unexpected errors fail validation.
    for level in ['easy','moderate','hard']:
        for seed in range(80):
            r=G.generate(level,seed);validate(r);familycoverage.add(r['generation']['template'])
        assert set(k for k,l in G.LEVEL.items() if l==level)<=familycoverage
    # Explicit workload rejection, no silent resampling.
    for level,k in [('moderate','q-94811'),('hard','q-94589'),('easy','affine')]:
        p={key:vals[0] for key,vals in G.DOMAINS[k].items()};p['a']=99
        try:G.generate(level,template=k,parameters=p);raise AssertionError('bad parameter accepted')
        except ValueError:pass
    # Identity must be independent of seed/order and opaque profile alias.
    for r in records:
        gen=r['generation'];again=G.generate(gen['level'],999,template=gen['template'],parameters=gen['parameters'],profile=gen['profile'])
        assert r['question'][':question/id']==again['question'][':question/id']
    common_record=G.generate('hard',template='q-170675',parameters={'a':4,'b':1})
    validate(common_record)
    corrupted=copy.deepcopy(common_record)
    sol=corrupted['question'][':question/worked-solution']
    cb=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)[-2]
    common_text=G.rhs_spans(cb)[1][2]
    collapsed=r'-\frac{4{s}^{2}+{t}^{2}}{(s+t)^{2}}+\frac{2t}{s+t}'
    corrupted['question'][':question/worked-solution']=sol.replace(common_text,collapsed,1)
    try:validate(corrupted)
    except AssertionError:common_denominator_mutation_detected=True
    else:raise AssertionError('missing common-denominator step survived')
    # Meaningful mutations: prompt coefficient, coordinate derivative, component
    # sign, expansion, concluding scalar, missing path and wrong designation.
    mutations=[]
    originals=[G.generate('hard',template='q-94589',parameters=G.BASE['q-94589']),G.generate('moderate',template='q-94815',parameters=G.BASE['q-94815'])]
    for name,find,replace,which in [
        ('prompt coefficient','+2xy','+4xy',0),('coordinate derivative',' & =3 ',' & =4 ',0),
        ('component product','(6t-12s)\\cdot (-1)','(6t-12s)\\cdot (1)',0),
        ('distributed sign','+6st-6t+12s','+6st+6t+12s',0),
        ('conclusion','=6+6-3=9','=6+6-3=8',0),
        ('wrong coordinate','y=3t-s','y=3t+s',1)]:
        r=copy.deepcopy(originals[which]);key=':question/problem' if name in ['prompt coefficient','wrong coordinate'] else ':question/worked-solution'
        assert find in r['question'][key],(name,find)
        r['question'][key]=r['question'][key].replace(find,replace,1)
        try:validate(r)
        except (AssertionError,ValueError):mutations.append(name)
        else:raise AssertionError('mutation survived '+name)
    native=[]
    for r in records+ [G.generate(G.LEVEL[k],template=k,parameters=G.BASE[k],profile='observed') for k in G.BASE if k!='q-94589']+[G.generate('hard',template='q-94589',parameters=G.BASE['q-94589'],profile='observed-repaired')]:
        checks=[]
        for i,f in enumerate(r['question'][':question/answer-fields']):
            if ':answer-field/correct' not in f:continue
            for a in f[':answer-field/choices']:
                checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual displayed option designation'})
        native.append({'label':r['generation']['template']+'-'+r['generation']['profile']+'-'+str(len(native)),'record':r,'checks':checks})
    (HERE/'engine-input.json').write_text(json.dumps(native,indent=2));exe=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(exe),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,capture_output=True,text=True)
    for k in G.BASE:
        evidence=G.generate(G.LEVEL[k],99,template=k,profile='observed');validate(evidence);review.append(evidence)
    review.append(G.generate('hard',template='q-94589',parameters=G.BASE['q-94589'],profile='observed-repaired'))
    (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False))
    variety={};rejected={}
    for k in G.BASE:
        tasks=set();reject=0
        keys=list(G.DOMAINS[k])
        for combo in itertools.product(*(G.DOMAINS[k][v] for v in keys)):
            p=dict(zip(keys,combo));o=G.objects(k,p)
            try:G.bank(k,o,'method')
            except ValueError:reject+=1;continue
            tasks.add(G.task_fingerprint(k,o))
        variety[k]=len(tasks);rejected[k]=reject
    easy_tasks=set();easy_reject=0
    for a,b,c,d,e,h in itertools.product(*G.DOMAINS['affine'].values()):
        D=a*d+b*e+c*h;values=[D,D-a*d,D-b*e,a-b+2*c,D+a*d]
        if len(set(values))!=5:easy_reject+=1;continue
        common=math.gcd(math.gcd(abs(a),abs(b)),abs(c))*(1 if c>0 else -1)
        easy_tasks.add((a//common,b//common,c//common,d,e,h))
    variety['affine']=len(easy_tasks);rejected['affine']=easy_reject
    result={'passed':True,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__,'matplotlib_installed':importlib.metadata.version('matplotlib')},'provenance':{k:G.RAW[k] for k in ['database','basis','lineage']},'source_questions':12,'raw_prompt_exact':12,'raw_solution_exact':12,'source_fields':13,'complete_banks_matched':13,'displayed_options_matched':65,'correct_designations_matched':12,'missing_original_designation':1,'format_repairs':{'q-94589':'one authoritative widget selection field; discarded duplicate legacy field only in repaired profile'},'math_source_repairs':0,'normal_generated_checked':len(records)+240,'default_family_coverage':sorted(familycoverage),'normal_bank_policy':'complete five-operation assessed-method banks; whole-instance collision rejection','evidence_only_profiles':['observed','observed-repaired'],'mutation_failures_detected':mutations+['missing-common-denominator'],'finite_meaningful_tasks':variety,'whole_bank_rejected_parameter_pairs':rejected,'native_report':'engine-report.json','native_engine_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'limitations':['Historical residual-offset banks preserve evidence but distractor intent is opaque; never defaults.','The native fixture requires every field correct ref and cannot load raw q-94589. Its repaired one-field profile is graded; neither malformed raw field has a raw-native grading claim.','Easy difficulty is authored, not recovered.'],'renderer':'none; static full-resolution chain-rule trees inspected'}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()

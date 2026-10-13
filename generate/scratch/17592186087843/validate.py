#!/usr/bin/env python3
"""Source/raw/completed fidelity, independent displayed mathematics, native grading."""
import hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
P=Path(__file__).parent;ROOT=P.parents[2]
spec=importlib.util.spec_from_file_location('asymptotes',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,)

def group(text,i):
    assert text[i]=='{';depth=1;j=i+1
    while depth:
        if text[j]=='{':depth+=1
        elif text[j]=='}':depth-=1
        j+=1
    return text[i+1:j-1],j

def read(text):
    text=text.strip().rstrip('.').replace(r'\left','').replace(r'\right','').replace(r'{)}',')')
    out='';i=0
    while i<len(text):
        if text.startswith(r'\frac',i):
            n,j=group(text,i+5);d,j=group(text,j);out+='(('+str(read(n))+')/('+str(read(d))+'))';i=j
        elif text.startswith(r'\cancel',i):
            n,j=group(text,i+7);out+='('+str(read(n))+')';i=j
        else:out+=text[i];i+=1
    out=out.replace('{','(').replace('}',')').replace('^','**')
    assert '\\' not in out,('unparsed command',out)
    return parse_expr(out,local_dict={'x':X},transformations=TRANS)

def fmt(text):
    assert text.count('$')%2==0,'math delimiters'
    depth=0
    for i,c in enumerate(text):
        if c in '{}':
            if i and text[i-1]=='\\':continue
            depth+=1 if c=='{' else -1
            assert depth>=0,'unmatched close brace'
    assert depth==0,'unmatched open brace'
    assert '+-' not in text and '--' not in text

def prompt_parts(text):
    first=re.search(r'\$f\(x\)(.*?)\$',text,re.S).group(1).strip().lstrip('=').strip().rstrip('.')
    assert not re.search(r'\b[ytz]\b',first),'wrong independent variable'
    if first.startswith(r'\frac'):
        n,j=group(first,5);d,j=group(first,j);assert j==len(first)
        return read(n),read(d)
    # Literal source quotient notation (x)/(x(x-2)).
    left,right=first.split('/',1);return read(left),read(right)

def rootset(expr):return frozenset(sp.solve(expr,X))
def correct(field):return next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
def read_choice(value):
    if value=='The function has no vertical asymptotes':return frozenset()
    values=[]
    for match in re.finditer(r'x\s*=\s*(±\s*)?(-?\d+)',value):
        v=sp.Rational(match.group(2));values.append(v)
        if match.group(1):values.append(-v)
    assert values,('unread displayed root set',value)
    return frozenset(values)


native=[];stage_counter=0

def check(record,raw=False,add_native=True):
    global stage_counter
    assert set(record['knowledge_point'])=={'db_id','id','title'} and record['knowledge_point']['db_id']==g.KP_ID
    q=record['question'];fmt(q[':question/problem']);n,d=prompt_parts(q[':question/problem'])
    assert sp.degree(d,X)<=3 and sp.degree(n,X)<=3
    reduced=sp.cancel(n/d);rd=sp.fraction(reduced)[1];poles=rootset(rd);domain=rootset(d);holes=domain-poles
    assert poles and all(r.is_real for r in domain),'same-KP real-factor boundary'
    assert poles==frozenset(sp.Rational(r) for r in record['generation']['remaining_poles'])
    # Rational cancelled nonmonic roots are read with SymPy's LaTeX parser here
    # via our elementary fraction reader, independently from generation math.
    assert holes==frozenset(read(r) for r in record['generation']['holes'])
    assert domain==frozenset(read(r) for r in record['generation']['original_domain_excludes'])
    sol=q.get(':question/worked-solution')
    if sol:
        fmt(sol);blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==2
        rows=blocks[0].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
        for row in rows:
            assert '&' in row
            value=read(row.split('&',1)[1].strip().lstrip('='))
            assert sp.cancel(value-reduced)==0,('wrong displayed solution row',row)
            stage_counter+=1
        # Ordered structural roles are checked as well as equal values. A
        # collapsed CAS fraction cannot substitute for the factor/cancel stages.
        rhs=[row.split('&',1)[1].strip().lstrip('=').strip() for row in rows]
        cancelled=[i for i,r in enumerate(rhs) if r'\cancel' in r]
        assert cancelled==[len(rhs)-2] and rhs[-2].count(r'\cancel')==2
        assert r'\cancel' not in rhs[-1]
        family=g.TEMPLATES[record['generation']['template']][1]
        if family.startswith('grouped'):
            assert '{x}^{2}(' in rhs[1] and '-(' in rhs[1] or '{x}^{2}(' in rhs[1] and re.search(r'-\d+\(',rhs[1])
            assert '({x}^{2}-' in rhs[2]
            assert rhs[3].count('(')>=3
        if family=='cube':
            assert '^{3}' in rhs[1] and rhs[2].count('^{2}')==2
        if family=='nonmonic':
            assert record['generation']['parameters']['m']>=2
            assert str(record['generation']['parameters']['m'])+'x' in rhs[1]
        count={'factored':3,'factored_zero':3,'grouped_linear':6,'grouped_quadratic':6,'cube':5}.get(g.TEMPLATES[record['generation']['template']][1],4)
        assert len(rows)==count,('stage sequence count',len(rows),count)
        eq=blocks[1].strip();assert eq.endswith('=0');assert rootset(read(eq[:-2]))==poles,'full remaining denominator-root criterion'
        inline=re.findall(r'\$x=(-?\d+(?:/\d+)?)\.?\$',sol)
        assert set(map(sp.Rational,inline))==set(poles),('solution prose root set',inline,poles)
    fields=q.get(':question/answer-fields',[]);checks=[]
    if not fields:
        assert raw and record['generation']['template']==g.RAW_FIELDLESS;return
    for fi,f in enumerate(fields):
        kind=f[':answer-field/type'].split('/')[-1];ids=[a[':answer/id'] for a in f[':answer-field/choices']];assert len(ids)==len(set(ids))
        for a in f[':answer-field/choices']:fmt(a[':answer/value'])
        if kind=='blank':
            assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
            expected=sorted(poles)[int(f[':answer-field/key'][-1])-1]
            assert all(read(a[':answer/value'])==expected for a in f[':answer-field/choices'])
        else:
            sets=[read_choice(a[':answer/value']) for a in f[':answer-field/choices']]
            assert len(sets)==5 and len(set(sets))==5 and sets.count(poles)==1
        if ':answer-field/correct' not in f:
            assert raw and record['generation']['source_missing_correct_ref'];continue
        assert f[':answer-field/correct']==[':answer/id',correct(f)[':answer/id']]
        if kind=='radio':
            assert read_choice(correct(f)[':answer/value'])==poles
            for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a==correct(f) else 'rejected','purpose':'complete owned root-set choice'})
        else:
            value=read(correct(f)[':answer/value']);assert value==expected
            # Numeric fragment requested. Give an unevaluated quadratic-root
            # formula for two poles, and a linear-root formula for one pole.
            if len(poles)==2:
                pp=sp.Poly(rd,X);A,B,C=pp.all_coeffs();disc=B*B-4*A*C
                sign='-' if value==min(poles) else '+'
                equivalent='('+str(-B)+sign+r'\sqrt{'+str(disc)+'})/(2*('+str(A)+'))'
            elif sp.degree(rd,X)==2:
                pp=sp.Poly(rd,X);A,B,C=pp.all_coeffs();equivalent='(-('+str(B)+'))/(2*('+str(A)+'))'
            else:
                pp=sp.Poly(rd,X);A,B=pp.all_coeffs();equivalent='(-('+str(B)+'))/('+str(A)+')'
            checks.extend([{'field_index':fi,'submitted':correct(f)[':answer/value'],'expected':'accepted','purpose':'canonical numeric root fragment'},{'field_index':fi,'submitted':equivalent,'expected':'accepted','purpose':'unreduced root formula from actual printed reduced denominator'},{'field_index':fi,'submitted':str(value+1),'expected':'rejected','purpose':'incorrect numeric root'}])
    if add_native and not raw:native.append({'label':record['generation']['template']+'/'+record['generation']['profile']+'/'+str(record['generation']['seed']),'record':record,'checks':checks})

cases=[];fidelity=[];review=[]
counts={'source_questions':13,'raw_prompts_exact':0,'raw_layouts_exact':0,'complete_banks_exact':0,'source_options_exact':0,'original_correct_designations_matched':0,'missing_correct_designations_inferred':3,'source_worked_solutions_present':10,'source_worked_solutions_exact':0,'authored_missing_solutions':3,'fieldless_sources':1,'source_radio_banks_exact':6,'source_radio_values_exact':30,'source_blank_fields_exact':7,'original_designated_radio_distractors_exact':12,'independently_classified_radio_distractors':12,'completed_source_prompts_exact':12,'completed_source_prompts_total':13,'present_solution_notation_normalizations_in_normal':1,'mathematical_source_errors':0}
for t,(level,family,p) in g.TEMPLATES.items():
    q=g.SOURCES[t];case={'source_id':t,'template':t,'level':level,'parameters':p,'bank_profile':'observed','raw_profile':'raw','original_difficulty':q.get(':question/difficulty'),'authored_level_assignment':':question/difficulty' not in q}
    cases.append(case);raw=g.generate(level,seed=5,template=t,parameters=p,profile='raw');check(raw,True)
    assert raw['question'][':question/problem']==q[':question/problem'];counts['raw_prompts_exact']+=1
    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
        assert (key in raw['question'])==(key in q),('raw attribute-presence mismatch',t,key)
    rf={f[':answer-field/key']:f for f in raw['question'].get(':question/answer-fields',[])};sf={f[':answer-field/key']:f for f in q.get(':question/answer-fields',[])}
    assert set(rf)==set(sf);counts['raw_layouts_exact']+=1
    for key,f in sf.items():
        f2=rf[key];assert f2[':answer-field/type']==f[':answer-field/type'][':db/ident']
        orig=sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in f[':answer-field/choices']);new=sorted((a[':answer/type'],a[':answer/value']) for a in f2[':answer-field/choices']);assert orig==new
        counts['complete_banks_exact']+=1;counts['source_options_exact']+=len(orig)
        if ':answer-field/correct' in f:
            assert correct(f2)[':answer/value']==f[':answer-field/correct'][':answer/value'];counts['original_correct_designations_matched']+=1
        else:assert ':answer-field/correct' not in f2
    if ':question/worked-solution' in q:
        assert raw['question'][':question/worked-solution']==q[':question/worked-solution'];counts['source_worked_solutions_exact']+=1
    else:assert ':question/worked-solution' not in raw['question']
    completed=g.generate(level,seed=5,template=t,parameters=p,profile='observed');check(completed)
    if t in g.RADIO:assert completed['generation']['evidence_only'] and not completed['generation']['eligible_for_learning']
    fidelity.append({'source_id':t,'raw_prompt_exact':True,'raw_layout_exact':True,'options_exact':sum(len(f[':answer-field/choices']) for f in sf.values()),'original_solution_exact':':question/worked-solution' in q,'authored_completion':t in ('q-39800','q-39801','q-80690','q-39802')})
    review.extend([{'label':'raw original '+t,'record':raw},{'label':'completed source replay '+t,'record':completed}])
    for seed in (37,94):
        variant=g.generate(level,seed,template=t,profile='observed');check(variant);review.append({'label':'generated observed-shape variant '+t+' (evidence only for radio)','record':variant})
        normal=g.generate(level,seed,template=t);check(normal);review.append({'label':'generated normal method-bank variant '+t,'record':normal})
(P/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
unique={l:set() for l in ('easy','moderate','hard')};orders=set();normal_count=0
for t,(level,_,_) in g.TEMPLATES.items():
    for seed in range(32):
        r=g.generate(level,seed,template=t);check(r);normal_count+=1;unique[level].add(r['generation']['mathematical_fingerprint'])
        r2=g.generate(level,seed+1000,template=t,parameters=r['generation']['parameters'])
        assert r['question'][':question/id']==r2['question'][':question/id'],'seed-invariant identity'
        assert r['generation']['content_fingerprint']==r2['generation']['content_fingerprint']
        if t in g.RADIO:
            f=r['question'][':question/answer-fields'][0];orders.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a==correct(f)))
assert len(orders)>1
# Independent opaque slots do not inflate normal mathematical/content identity.
for t in ('q-39801','q-39804','q-39931'):
    level=g.TEMPLATES[t][0];r=g.generate(level,99,template=t);p=dict(r['generation']['parameters']);p['opaque']=[v+1 for v in p['opaque']]
    r2=g.generate(level,999,template=t,parameters=p)
    assert r['question'][':question/id']==r2['question'][':question/id']
    assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
bad=[('q-278556',dict(m=2,n=-2,b=-1)),('q-278556',dict(m=5,n=-1,b=-1)),('q-278545',dict(a=2,b=0)),('q-278545',dict(a=2,b=2)),('q-278543',dict(a=2,b=-2,c=3)),('q-39804',dict(a=5,b=-6,opaque=[0])),('q-278535',dict(a=1,b=1))]
for t,p in bad:
    try:g.generate(g.TEMPLATES[t][0],template=t,parameters=p)
    except ValueError:pass
    else:raise AssertionError('explicit workload guard bypass')

# Enumerate finite primitive parameter domains. Layout/profile aliases are not
# extra tasks. Distinct families have different numerator/denominator workload;
# factored_zero is a subset of factored, and spaced masks duplicate their compact
# mathematical family. Opaque slots are excluded entirely.
catalog_ranges={
'q-278535':{'a':range(-6,7),'b':range(-8,9)},
'q-269990':{'a':range(-6,7),'b':range(-8,9)},
'q-278556':{'m':range(2,5),'n':range(-5,6),'b':range(-6,7)},
'q-278536':{'b':range(-8,9)},
'q-278545':{'a':range(1,5),'b':range(-8,9)},
'q-80691':{'a':range(-8,9)},
'q-278543':{'a':range(-6,7),'b':range(-8,9),'c':range(-6,7)},
'q-39802':{'a':range(1,5),'b':range(-8,9),'c':range(-6,7)},
'q-39804':{'a':range(-4,5),'b':range(-8,9)},
'q-39931':{'a':range(1,7)},
}
catalog={};catalog_by_level={l:0 for l in ('easy','moderate','hard')}
for t,ranges in catalog_ranges.items():
    count=0
    for values in itertools.product(*ranges.values()):
        p=dict(zip(ranges,values))
        if 'opaque' in g.TEMPLATES[t][2]:p['opaque']=g.TEMPLATES[t][2]['opaque']
        try:g.guard(t,p)
        except ValueError:continue
        # The only further complete-normal-bank collision in these primitive
        # guards is cube a=-b (removed-root and sign-reversed-pole answers).
        if t=='q-39804' and p['a']==-p['b']:continue
        count+=1
    catalog[t]=count;catalog_by_level[g.TEMPLATES[t][0]]+=count
assert catalog_by_level=={'easy':208,'moderate':496,'hard':2198},catalog_by_level
(P/'catalog.json').write_text(json.dumps({'finite_normal_mathematical_tasks_by_level':catalog_by_level,'representative_family_counts':catalog,'excluded_aliases':['q-80690 is the a=0 subset of q-278535','q-39801 duplicates monic quadratic math family q-269990','q-39800 duplicates quadratic-ratio math family q-278543'],'incidental_opaque_slots_counted':False},indent=2)+'\n')
(P/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
engine=ROOT/'generate/runs/current/check-engine';report=P/'engine-report.json';res=subprocess.run([str(engine),str(P/'engine-input.json'),str(report)],capture_output=True,text=True);assert res.returncode==0,res.stdout+res.stderr
nr=json.loads(report.read_text())
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n')
md=['# Review','Original raw evidence, supported completions, observed-shape variants and normal method-bank variants are labeled separately. Raw omissions have no native grading claim.']
for item in review:
    q=item['record']['question'];md+=['\n## '+item['label'],q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        md.append('Field '+f[':answer-field/key']+' ('+f[':answer-field/type'].split('/')[-1]+')')
        for a in f[':answer-field/choices']:md.append('- '+a[':answer/value']+(' (correct)' if ':answer-field/correct' in f and a==correct(f) else ''))
    md.append(q.get(':question/worked-solution','Source has no captured worked solution.'))
(P/'review.md').write_text('\n\n'.join(md)+'\n')
result={'passed':True,'source_provenance':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'source_fidelity':counts,'fidelity':fidelity,'normal_records_checked':normal_count+26,'observed_variant_records_checked':26,'completed_source_records_checked':13,'raw_source_records_checked':13,'displayed_solution_rows_verified':stage_counter,'distinct_sampled_mathematical_tasks_by_level':{k:len(v) for k,v in unique.items()},'finite_catalog_tasks_by_level':catalog_by_level,'native':{k:nr[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'engine_harness_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'source_limitations':['Three original correct refs absent; independently inferred completions do not count matched designations.','q-39802 original fieldless; raw profile preserves it, completed profiles add two ascending-order blank fields.','Three original worked solutions absent; normal/completed recipes supply canonical-method stages.','All six observed radio banks evidence_only true, eligible_for_learning false; opaque slots do not establish wrong-operation author intent.'],'database_writes':0}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

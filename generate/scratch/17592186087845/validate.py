#!/usr/bin/env python3
"""Independent displayed-TeX math, raw presence/fidelity, identity and native QA.

No import of the generator's symbolic builders/roots for mathematical checks.
The reader is local and independently parses the printed numerator/denominator,
each ordered fraction stage, discriminant stages and complete choice root sets.
"""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
P=Path(__file__).parent;ROOT=P.parents[2];SCRIPT=P.with_suffix('.py')
spec=importlib.util.spec_from_file_location('kp87845',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=s.Symbol('x',real=True);TRANS=standard_transformations+(implicit_multiplication_application,)

def group(text,i):
    assert text[i]=='{';depth=1;j=i+1
    while depth:
        assert j<len(text),'unterminated group'
        depth+=int(text[j]=='{')-int(text[j]=='}');j+=1
    return text[i+1:j-1],j

def read(raw):
    raw=raw.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'{)}',')')
    out='';i=0
    while i<len(raw):
        command=next((c for c in (r'\frac',r'\dfrac',r'\sqrt',r'\cancel') if raw.startswith(c,i)),None)
        if command:
            a,j=group(raw,i+len(command))
            if command in (r'\frac',r'\dfrac'):
                b,j=group(raw,j);out+='(('+str(read(a))+')/('+str(read(b))+'))'
            elif command==r'\sqrt':out+='sqrt('+str(read(a))+')'
            else:out+='('+str(read(a))+')'
            i=j
        else:out+=raw[i];i+=1
    out=out.replace('{','(').replace('}',')').replace('^','**')
    assert '\\' not in out,('unparsed TeX',raw,out)
    value=parse_expr(out,local_dict={'x':X,'sqrt':s.sqrt},transformations=TRANS)
    assert value.free_symbols<= {X},('wrong mathematical variables',raw,value)
    return value

def fmt(text):
    assert text.count('$')%2==0,('math delimiters',text)
    depth=0
    for i,c in enumerate(text):
        if c in '{}':
            if i and text[i-1]=='\\':continue
            depth+=1 if c=='{' else -1;assert depth>=0
    assert depth==0,'brace groups'
    assert '+-' not in text and '--' not in text

def fraction_parts(raw):
    raw=raw.strip().rstrip('.,');m=re.match(r'\\(?:d?frac)',raw);assert m,raw
    n,j=group(raw,m.end());d,j=group(raw,j);assert not raw[j:].strip(),raw
    return read(n),read(d)

def prompt_parts(text):
    match=re.search(r'f\(x\)\s*=([^$]+)',text);assert match,text
    return fraction_parts(match[1])

def real_roots(p):return frozenset(r for r in s.solve(p,X) if r.is_real)
def choice_roots(value):
    if value=='The function has no vertical asymptotes':return frozenset()
    text=value.replace('$','').replace(r'\,','').replace('only','').replace(' and ', ',').strip()
    # Entire RHS expressions are split at comma separators, preserving fractions.
    values=[]
    for part in text.split(','):
        part=part.strip()
        if not part:continue
        lhs,rhs=part.split('=',1);assert lhs.strip()=='x',value
        if r'\pm' in rhs:
            v=read(rhs.replace(r'\pm',''));values.extend([v,-v])
        else:values.append(read(rhs))
    assert values and all(v.is_real and not v.free_symbols for v in values),value
    return frozenset(values)

def simplify_rootsets(values):return frozenset(s.simplify(v) for v in values)
def enum(value):return value[':db/ident'] if isinstance(value,dict) else value
native=[];stages=0;records_checked=0

def check(record,add_native=False):
    global stages,records_checked
    records_checked+=1
    assert set(record['knowledge_point'])=={'db_id','id','title'} and record['knowledge_point']['db_id']==17592186087845
    q=record['question'];fmt(q[':question/problem']);n,d=prompt_parts(q[':question/problem']);reduced=s.cancel(n/d);rn,rd=s.fraction(reduced)
    assert 1<=s.degree(n,X)<=2 and 3<=s.degree(d,X)<=4,'same KP degree scope'
    assert s.degree(s.gcd(n,d),X)>=1,'common factor required'
    assert s.degree(rd,X)==2,'irreducible quadratic remainder'
    a,b,c=s.Poly(rd,X).all_coeffs();delta=b*b-4*a*c;assert delta<0 and not real_roots(rd),'complex quadratic/no-pole boundary'
    metadata=record['generation']
    domain=real_roots(d);common=s.gcd(n,d);holes=real_roots(common)
    assert domain==holes and domain,'all real singularities removable'
    for key,actual in [('original_domain_excludes',domain),('holes',holes),('remaining_poles',real_roots(rd))]:
        assert simplify_rootsets(actual)==simplify_rootsets(s.sympify(v) for v in metadata[key]),(key,actual,metadata[key])
    for key,poly in [('denominator_root_multiplicities',d),('cancelled_root_multiplicities',common)]:
        actual={s.simplify(r):m for r,m in s.roots(poly,X).items()};claimed={s.sympify(r):m for r,m in metadata[key].items()}
        assert actual==claimed,(key,actual,claimed)
    sol=q.get(':question/worked-solution')
    if sol:
        fmt(sol);blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks) in (2,3)
        rows=blocks[0].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
        rhs=[]
        for row in rows:
            assert '&' in row;raw=row.split('&',1)[1].strip().lstrip('=');rhs.append(raw)
            sn,sd=fraction_parts(raw);assert s.cancel(sn/sd-reduced)==0,('displayed incorrect stage',row);stages+=1
        assert r'\cancel' in rhs[-2] and rhs[-2].count(r'\cancel')==2 and r'\cancel' not in rhs[-1]
        # Check the original rational formula before any CAS cancellation.
        pn,pd=fraction_parts(rhs[0]);assert s.expand(pn-n)==0 and s.expand(pd-d)==0
        assert s.degree(fraction_parts(rhs[-1])[1],X)==2
        eq=blocks[1].strip();left,right=eq.rstrip('.').split('=',1);assert read(right)==0
        displayed_q=read(left);assert s.degree(displayed_q,X)==2 and s.Poly(displayed_q,X).discriminant()<0
        assert s.simplify(displayed_q/rd).free_symbols==set(),'remaining denominator equation'
        if len(blocks)==3:
            drows=blocks[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
            assert re.sub(r'\s+','',drows[0].split('=',1)[1]) in ('b^2-4ac','{b}^{2}-4ac')
            expected=s.Poly(displayed_q,X).discriminant()
            for row in drows[1:]:
                v=read(row.split('=',1)[1]);assert s.simplify(v-expected)==0,('discriminant stage',row,expected);stages+=1
            assert len(drows)>=3 and '^' in drows[0]
    for f in q.get(':question/answer-fields',[]):
        assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection';choices=f[':answer-field/choices'];assert len(choices)==5
        values=[choice_roots(a[':answer/value']) for a in choices];assert len(set(values))==5,'complete bank root-set ambiguity'
        assert sum(v==frozenset() for v in values)==1
        if not metadata['evidence_only']:
            qa,qb,qc=s.Poly(rd,X).monic().all_coeffs();mult=metadata['operation_profile_multiplier']
            W=real_roots(qa*X**2+qb*X-mult*qc)
            expected={frozenset(),holes,W,holes|W,frozenset([max(W)])}
            assert set(values)==expected,('printed wrong-operation bank',values,expected)
        for a in choices:fmt(a[':answer/value'])
        if ':answer-field/correct' in f:
            correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
            ids=[a[':answer/id'] for a in choices];assert len(set(ids))==5 and correct[1] in ids
            assert values[ids.index(correct[1])]==real_roots(rd)
            if add_native:native.append({'label':metadata['template']+'/'+metadata['profile']+'/'+str(metadata['seed']),'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct[1] else 'rejected','purpose':'all owned complete-bank selections'} for a in choices]})
        else:assert metadata['evidence_only'],'missing designation only in raw evidence'


def source_presence(q):
    return {k:k in q for k in (':question/difficulty',':question/worked-solution',':question/answer-fields')}

cases=[];reviews=[];source_counts={'practice':len(g.SOURCES),'raw_prompts_exact':0,'raw_solutions_exact':0,'raw_solutions_present':0,'complete_banks_exact':0,'choices_exact':0,'correct_refs_exact':0,'correct_refs_present':0,'key_presence_parity':0}
for name,source in g.SOURCES.items():
    level=g.LEVELS[name];case={'source_id':name,'template':name,'level':level,'parameters':{'scale':1},'bank_profile':'observed:'+name};cases.append(case)
    raw=g.generate(level,template=name,parameters=case['parameters'],profile=case['bank_profile']);q=raw['question'];check(raw,True)
    assert source_presence(q)==source_presence(source);source_counts['key_presence_parity']+=1
    assert q[':question/problem']==source[':question/problem'];source_counts['raw_prompts_exact']+=1
    if ':question/worked-solution' in source:
        assert q[':question/worked-solution']==source[':question/worked-solution'];source_counts['raw_solutions_exact']+=1;source_counts['raw_solutions_present']+=1
    for of,gf in zip(source.get(':question/answer-fields',[]),q.get(':question/answer-fields',[]),strict=True):
        assert enum(of[':answer-field/type'])==gf[':answer-field/type'] and of[':answer-field/key']==gf[':answer-field/key']
        old=sorted((enum(a[':answer/type']),a[':answer/value']) for a in of[':answer-field/choices']);new=sorted((a[':answer/type'],a[':answer/value']) for a in gf[':answer-field/choices']);assert old==new
        source_counts['complete_banks_exact']+=1;source_counts['choices_exact']+=len(old)
        assert (':answer-field/correct' in of)==(':answer-field/correct' in gf)
        if ':answer-field/correct' in of:
            newanswer=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert of[':answer-field/correct'][':answer/value']==newanswer[':answer/value'];source_counts['correct_refs_exact']+=1;source_counts['correct_refs_present']+=1
    reviews.append(raw)
    for scale in (2,3):
        variant=g.generate(level,17+scale,name,parameters={'scale':scale},profile='observed:'+name);check(variant);reviews.append(variant)
    completed=g.generate(level,7,name,parameters={'scale':1},profile='completed:'+name);check(completed,True);reviews.append(completed)
    # Public markdown replay must tolerate every captured omission.
    subprocess.run([str(ROOT/'.venv/bin/python'),str(SCRIPT),'--difficulty',level,'--template',name,'--profile','observed:'+name,'--parameters','{"scale":1}'],check=True,stdout=subprocess.DEVNULL)

# Canonical example mathematics is checked separately from practice fidelity.
canonical=g.REC[':knowledge-point/canonical-example'];cn,cd=prompt_parts(canonical[':question/problem']);cc=s.gcd(cn,cd)
canonical_record={'knowledge_point':{'db_id':17592186087845,'id':g.KP_UUID,'title':g.TITLE},'question':canonical,'generation':{'evidence_only':True,'original_domain_excludes':[str(v) for v in real_roots(cd)],'holes':[str(v) for v in real_roots(cc)],'remaining_poles':[],'denominator_root_multiplicities':{str(r):int(m) for r,m in s.roots(cd,X).items()},'cancelled_root_multiplicities':{str(r):int(m) for r,m in s.roots(cc,X).items()}}}
check(canonical_record)

# Determinism, scope and meaningful authored bank tests.
variety={l:set() for l in ('easy','moderate','hard')};option_positions=set()
for name,level in g.FAMILIES.items():
    for seed in range(80):
        r=g.generate(level,seed,name);check(r,seed<3);variety[level].add(r['generation']['parameter_fingerprint'])
        if seed<2:reviews.append(r)
        replay=g.generate(level,seed+100,name,parameters=r['generation']['parameters']);assert r['question'][':question/id']==replay['question'][':question/id'];assert r['generation']['content_fingerprint']==replay['generation']['content_fingerprint']
        field=r['question'][':question/answer-fields'][0];option_positions.add(next(i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1]))
assert len(option_positions)>=4
# Authored two-pair grouping and all source layouts retain ordered workload.
for r in reviews:
    if r['generation']['template']=='grouped-numerator':assert r['generation']['parameters']['b']==0
    if r['generation']['template'] in g.SOURCES and ':question/worked-solution' in g.SOURCES[r['generation']['template']]:
        original=g.SOURCES[r['generation']['template']][':question/worked-solution']
        assert r['question'][':question/worked-solution'].count(r'\\')==original.count(r'\\')
        assert r['question'][':question/worked-solution'].count(r'\cancel')==original.count(r'\cancel')
# Enumerate narrow easy, and full bounded moderate/hard samplers to prevent inflated scalar variety.
easy_tasks={g.generate('easy',template='factored',parameters={'r':0,'b':0,'c':c,'leading':a})['generation']['parameter_fingerprint'] for a in range(1,6) for c in range(1,10) if s.gcd(a,c)==1};assert len(easy_tasks)==33
for name,p in [('factored',{'r':1,'b':0,'c':1,'leading':1}),('factored',{'r':0,'b':0,'c':2,'leading':2}),('common-power',{'r':0,'b':0,'c':2,'m':1}),('grouped',{'r':0,'b':0,'c':2}),('quadratic-numerator',{'r':0,'b':0,'c':2,'a':2}),('quartic',{'c':4}),('grouped-numerator',{'r':1,'b':1,'c':2,'a':2}),('grouped',{'r':1,'b':0,'c':1}),('grouped-numerator',{'r':1,'b':0,'c':1,'a':2})]:
    try:g.generate(g.FAMILIES[name],template=name,parameters=p)
    except ValueError:pass
    else:raise AssertionError(('missing explicit scope guard',name,p))

(P/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(P/'review.json').write_text(json.dumps(reviews,indent=2)+'\n');(P/'review.md').write_text('# Source originals and clearly labeled generated variants\n\nRaw scale=1 reproduces each captured original. Scale>1 are parameterized opaque evidence only; completed records use authored operation banks. Each authored family has two additional examples.\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in reviews)+'\n')
(P/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(P/'engine-input.json'),str(P/'engine-results.json')],check=True)
engine=json.loads((P/'engine-results.json').read_text())
report={'status':'pass','source_fidelity':source_counts,'source_completion':{'missing_correct_refs':2,'fieldless':2,'unrated_authored_level_assignments':2,'missing_solutions':2,'separate_from_raw_fidelity':True},'mathematics':{'records_checked':records_checked,'displayed_stages_checked':stages,'all_original_domain_and_multiplicities_verified':True,'all_complete_choice_rootsets_verified':True,'source_errors':[],'canonical_example_checked_separately':True},'variety':{'sampled_unique_meaningful_tasks':{l:len(v) for l,v in variety.items()},'easy_finite_domain_tasks':len(easy_tasks),'scalar_prefactors_excluded':True},'native_grading':{'accepted':engine['accepted_checks'],'rejected':engine['rejected_checks'],'unresolved':engine['documented_unresolved_checks'],'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()},'review_records':len(reviews),'database_writes':0}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

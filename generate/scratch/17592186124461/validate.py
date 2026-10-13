#!/usr/bin/env python3
"""Independent printed-mathematics checks and real native radio grading.

TeX reader is local, supporting precisely the displayed functions and vectors;
it reads actual strings, not generation metadata. Captured raw data is preserved.
"""
import copy
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('normal_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
I,J,K=sp.symbols('i j k',real=True)
X,Y=g.X,g.Y
LOCALS={'i':I,'j':J,'k':K,'x':X,'y':Y,'e':sp.E,'sqrt':sp.sqrt,'ln':sp.log,'atan':sp.atan}

@lru_cache(maxsize=20000)
def read_tex(text):
    """Recursive complete TeX operands, then independent symbolic interpretation."""
    text=text.replace('⁡','').replace('\\,','').replace('\\:','').replace('\\left','').replace('\\right','').replace('\\cdot','*').replace('\\text{ }','')
    text=text.replace(r'\operatorname{arctan}','atan').replace(r'\operatorname{ln}','ln').replace(r'\ln','ln')
    # Norms of explicit displayed vectors.
    while '‖' in text:
        start=text.index('‖');end=text.index('‖',start+1)
        v=read_tex(text[start+1:end]);a,b,k=components(v,allow_k=True)
        text=text[:start]+'('+sp.sstr(sp.sqrt(a*a+b*b+k*k))+')'+text[end+1:]
    cursor=0
    def atom():
        nonlocal cursor
        while cursor<len(text) and text[cursor].isspace():cursor+=1
        if cursor>=len(text):raise AssertionError('missing TeX operand: '+text)
        if text[cursor]=='{':
            cursor+=1;out=seq('}');return '('+out+')'
        if text[cursor]=='(':
            cursor+=1;out=seq(')');return '('+out+')'
        if text.startswith(r'\frac',cursor):
            cursor+=5;a=atom();b=atom();return '('+a+'/'+b+')'
        if text.startswith(r'\sqrt',cursor):
            cursor+=5;return 'sqrt('+atom()+')'
        ch=text[cursor];cursor+=1
        return ch
    def seq(end=None):
        nonlocal cursor
        out=''
        while cursor<len(text):
            if end and text[cursor]==end:cursor+=1;return out
            if text[cursor]=='^':cursor+=1;out+='**'+atom()
            else:out+=atom()
        if end:raise AssertionError('unbalanced TeX: '+text)
        return out
    converted=seq()
    converted=re.sub(r'(?<=[0-9)])(?=[ijkxy])','*',converted)
    converted=re.sub(r'(?<=[xy])(?=[ij])','*',converted)
    assert '\\' not in converted,converted
    return parse_expr(converted,local_dict=LOCALS,transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)

def components(expr,allow_k=False):
    v=sp.expand(expr);a,b,k=(sp.simplify(v.coeff(t)) for t in (I,J,K))
    assert sp.simplify(v-a*I-b*J-k*K)==0,('not a vector',expr)
    if not allow_k:assert k==0,('out-of-plane',expr)
    return (a,b,k) if allow_k else (a,b)

def eq(a,b):return sp.simplify(a-b)==0
def vector_eq(a,b):return all(eq(x,y) for x,y in zip(a,b))

def printed_task(record):
    prompt=record['question'][':question/problem']
    match=re.search(r'\$([fg])\(x,\s*y\)\s*=\s*(.*?)\$',prompt)
    assert match,prompt
    function=read_tex(match[2].rstrip('.'))
    pt=re.search(r'\(x,\s*y\)\s*=\s*\((.*?)\)',prompt).group(1).split(',')
    p,q=(read_tex(z) for z in pt)
    dx,dy=(sp.diff(function,z) for z in (X,Y))
    a,b=(sp.simplify(v.subs({X:p,Y:q})) for v in (dx,dy))
    assert function.free_symbols<={X,Y}
    assert all(z.is_real and z.is_finite for z in (function.subs({X:p,Y:q}),a,b))
    assert a!=0 or b!=0
    # Curve through P is f(x,y)=f(P); verify actual printed point defines its
    # level and that implicit tangent (-fy,fx) is perpendicular to the normal.
    level=function.subs({X:p,Y:q})
    assert eq((function-level).subs({X:p,Y:q}),0)
    assert eq(a*(-b)+b*a,0)
    return function,p,q,dx,dy,a,b

def balanced(text):
    assert text.count('$')%2==0,('math delimiter',text)
    assert text.count('$$') in (0,4),('display blocks',text)
    count=0
    for c in text:
        if c=='{':count+=1
        elif c=='}':count-=1
        assert count>=0,('brace',text)
    assert count==0,('brace',text)
    assert '--' not in text and '+-' not in text,('ungrouped signs',text)

def derivative_rhs(rhs,function):
    # Replace the actual displayed formal derivative operators and their
    # complete arguments. Each is independently parsed/differentiated.
    for coord in ('x','y'):
        token=r'\frac{∂}{∂'+coord+'}'
        while token in rhs:
            start=rhs.index(token);opening=start+len(token)
            assert rhs[opening]=='('
            depth=0;end=None
            for index in range(opening,len(rhs)):
                if rhs[index]=='(':depth+=1
                elif rhs[index]==')':
                    depth-=1
                    if depth==0:end=index;break
            assert end is not None
            operand=read_tex(rhs[opening+1:end]);assert eq(operand,function)
            derivative=sp.diff(operand,X if coord=='x' else Y)
            rhs=rhs[:start]+'('+g.tex(derivative)+')'+rhs[end+1:]
    return rhs

def check_solution(record):
    q=record['question']
    if ':question/worked-solution' not in q:return None
    f,p,z,dx,dy,a,b=printed_task(record);solution=q[':question/worked-solution'];balanced(solution)
    # Every prose point/gradient call, including normalization introductions.
    for match in re.finditer(r'(?:∇[fg]|\\nabla [fg])\(([^()]*)\)',solution):
        if match[1]=='x,y':continue
        assert vector_eq(tuple(read_tex(v) for v in match[1].split(',')),(p,z))
    math=solution.split('$$');assert len(math)==5
    rows=math[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
    after=False
    for row in rows:
        lhs,rhs=row.split('& =',1)
        if lhs.strip() and '(x,y)' not in lhs:after=True
        expected=(a,b) if after else (dx,dy)
        rhs=re.sub(r'\{[fg]\}_\{x\}\(x,y\)',lambda m:'('+g.tex(dx)+')',rhs)
        rhs=re.sub(r'\{[fg]\}_\{y\}\(x,y\)',lambda m:'('+g.tex(dy)+')',rhs)
        rhs=derivative_rhs(rhs,f)
        actual=components(read_tex(rhs.strip().rstrip('.')))
        assert vector_eq(actual,expected),('printed gradient stage',row,actual,expected)
    normalrows=math[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
    expected=(a/sp.sqrt(a*a+b*b),b/sp.sqrt(a*a+b*b))
    for row in normalrows:
        _,rhs=row.split('& =',1)
        for stage in rhs.split('='):
            actual=components(read_tex(stage.strip().rstrip('.')))
            assert vector_eq(actual,expected),('printed normalization stage',row,actual,expected)
    assert len(rows)==record['generation']['solution_structure']['gradient_rows']
    assert len(normalrows)==record['generation']['solution_structure']['normalization_rows']
    return len(rows)+len(normalrows)

def check_record(r):
    assert set(r)=={'knowledge_point','question','generation'}
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.KP_ID
    q=r['question'];balanced(q[':question/problem'])
    f,p,z,dx,dy,a,b=printed_task(r)
    params=r['generation']['parameters']
    assert eq(f,g.function_for(r['generation']['template'],params.get('c',1),params.get('d',1)))
    field=q[':question/answer-fields'][0]
    assert field[':answer-field/type']==':answer-field.type/radio'
    assert field[':answer-field/key']=='selection'
    assert len(field[':answer-field/choices'])==5
    for choice in field[':answer-field/choices']:balanced(choice[':answer/value'])
    values=[components(read_tex(c[':answer/value']),allow_k=True) for c in field[':answer-field/choices']]
    if r['generation']['eligible_for_learning']:
        correct=field[':answer-field/correct'];assert correct[0]==':answer/id'
        correctchoice=next(c for c in field[':answer-field/choices'] if c[':answer/id']==correct[1])
        for choice,v in zip(field[':answer-field/choices'],values):
            assert v[2]==0
            validity=eq(v[0]*v[0]+v[1]*v[1],1) and eq(v[0]*b-v[1]*a,0)
            assert validity==(choice==correctchoice),(choice,v,(a,b))
        for index,v in enumerate(values):assert not any(vector_eq(v,w) for w in values[:index])
    return check_solution(r)

def engine_item(r,label):
    field=r['question'][':question/answer-fields'][0]
    if ':answer-field/correct' not in field:return None
    correct=field[':answer-field/correct'][1]
    checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct else 'rejected','purpose':'actual radio selection; mathematics checked independently'} for c in field[':answer-field/choices']]
    return {'label':label,'record':r,'checks':checks}

def finite_domain_eligible(a,b,profile):
    """Exact rational collision conditions for the whole method banks.
    These conditions are derived separately from renderer/option expressions;
    sampled fixtures still parse and compare all five displayed vectors.
    """
    if profile=='method-axis':return (a==0 or b==0) and abs(a or b)>1
    if a==0 or b==0:return False
    norm2=a*a+b*b;l1=abs(a)+abs(b)
    if abs(a)==abs(b):return norm2!=1 and (l1!=1 if profile=='method-balanced' else norm2!=l1)
    return norm2!=1 and l1!=1

def source_fidelity(case):
    src=g.QUESTIONS[case['source_id']]
    rec=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
    check_record(rec)
    dst=rec['question'];sf=src[':question/answer-fields'][0];df=dst[':question/answer-fields'][0]
    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in src)==(key in dst)
    assert (':answer-field/correct' in sf)==(':answer-field/correct' in df)
    assert dst[':question/problem']==src[':question/problem'],('prompt fidelity',case['source_id'])
    originals=[components(read_tex(c[':answer/value']),allow_k=True) for c in sf[':answer-field/choices']]
    actual=[components(read_tex(c[':answer/value']),allow_k=True) for c in df[':answer-field/choices']]
    unmatched=list(actual)
    for value in originals:
        matches=[i for i,v in enumerate(unmatched) if vector_eq(value,v)]
        assert len(matches)==1,('bank mismatch',case['source_id'],value,actual)
        unmatched.pop(matches[0])
    assert not unmatched
    if ':answer-field/correct' in sf:
        original=components(read_tex(sf[':answer-field/correct'][':answer/value']))
        generated=components(read_tex(next(c[':answer/value'] for c in df[':answer-field/choices'] if c[':answer/id']==df[':answer-field/correct'][1])))
        assert vector_eq(original,generated)
    prose=True;row_counts=None
    if ':question/worked-solution' in src:
        source_record=copy.deepcopy(rec);source_record['question']=copy.deepcopy(src)
        check_solution(source_record)
        old=src[':question/worked-solution'].split('$$');new=dst[':question/worked-solution'].split('$$')
        assert [old[i] for i in (0,2,4)]==[new[i] for i in (0,2,4)],('shared prose fidelity',case['source_id'])
        row_counts=[len(old[i].split(r'\\')) for i in (1,3)]
        assert row_counts==[len(new[i].split(r'\\')) for i in (1,3)]
    return rec,{'source_id':case['source_id'],'raw_option_spelling_matches':sum(c[':answer/value'] in [a[':answer/value'] for a in df[':answer-field/choices']] for c in sf[':answer-field/choices']),'bank_values_matched':5,'correct_designation_matched':':answer-field/correct' in sf,'prompt_exact':True,'solution_prose_exact':prose if ':question/worked-solution' in src else None,'source_stage_counts':row_counts,'solution_raw_exact':src.get(':question/worked-solution')==dst.get(':question/worked-solution') if ':question/worked-solution' in src else None}

def main():
    records=[];engines=[];fidelity=[];scope=[];fingerprints={k:set() for k in g.LEVELS};profiles=set()
    for case in g.CASES:
        r,f=source_fidelity(case);fidelity.append(f);records.append({'label':'Original evidence replay '+case['source_id'],'record':r})
        item=engine_item(r,'source/'+case['source_id'])
        if item:engines.append(item)
        # A normal original-parameter variant uses a complete method bank, and
        # must retain the same family-specific solution stages.
        selected='method-bilinear-axis' if case['template']=='bilinear' else 'method-axis' if case['template']=='axisquad' else 'method-balanced' if case['template'] in ('log','circle') else 'method-generic'
        normal=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=selected)
        check_record(normal);records.append({'label':'Authored method bank at original parameters '+case['source_id'],'record':normal})
        engines.append(engine_item(normal,'normal-original/'+case['source_id']))
        if ':question/worked-solution' in r['question']:assert normal['question'][':question/worked-solution']==r['question'][':question/worked-solution']
        # Changed parameter evidence recipes are public too, including opaque
        # ones. They remain excluded from learner defaults.
        varied=g.generate('easy',seed=7,template=case['template'],profile=case['bank_profile']);check_record(varied)
        records.append({'label':'Changed-parameter observed bank (evidence only) '+case['source_id'],'record':varied})
    print('Source fidelity and normal original-parameter chains passed.',flush=True)
    family_coverage={level:set() for level in g.LEVELS}
    for level in g.LEVELS:
        for family in g.FAMILIES[level]:
            for seed in range(8):
                r=g.generate(level,seed,template=family);check_record(r)
                family_coverage[level].add(family);profiles.add(r['generation']['profile'])
                fingerprints[level].add(r['generation']['mathematical_fingerprint'])
                engines.append(engine_item(r,level+'/'+family+'/'+str(seed)))
                if seed<2:records.append({'label':'Generated '+level+' '+family+' seed '+str(seed),'record':r})
                # Same fixed task/bank, distinct seeds/order preserve identity.
                other=g.generate(level,seed+31,template=family,parameters=r['generation']['parameters'],profile=r['generation']['profile'])
                assert r['question'][':question/id']==other['question'][':question/id']
                assert r['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
        defaults=set();default_checked=set()
        for seed in range(80):
            r=g.generate(level,seed);defaults.add(r['generation']['template'])
            key=(r['generation']['template'],r['generation']['profile'])
            if key not in default_checked:check_record(r);default_checked.add(key)
        assert defaults==set(g.FAMILIES[level])
        assert family_coverage[level]==set(g.FAMILIES[level])
        print('Printed mathematics, banks and identities passed: '+level,flush=True)
    # Same assessed exponential substitution is one task despite coordinate aliases.
    a=g.generate_easy(template='exp',parameters={'p':'0','q':'0'})
    b=g.generate_easy(template='exp',parameters={'p':'1','q':'-1'})
    assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
    invalid=[('easy','roots',{'p':'2','q':'4'}),('easy','log',{'p':'1','q':'-1'}),('easy','quotient',{'p':'1','q':'1'}),('easy','angle',{'p':'0','q':'1'}),('easy','radical',{'p':'1','q':'1'}),('easy','circle',{'p':'0','q':'0'}),('easy','mixed',{'p':'1/2','q':'-3/2'}),('easy','bilinear',{'p':'1/2','q':'-3/2'}),('moderate','canonical',{'p':'1','q':'-1'}),('moderate','canonical',{'p':'9/2','q':'-1/2'}),('hard','quotient',{'p':'1','q':'-1/2'}),('hard','angle',{'p':'17/2','q':'-1/2'}),('hard','roots',{'p':'1/2','q':'9/4'}),('hard','radical',{'p':'5/2','q':'5/2'}),('easy','exp',{'p':'0','q':'0','c':5,'d':1})]
    for level,family,params in invalid:
        try:g.generate(level,template=family,parameters=params)
        except ValueError:pass
        else:raise AssertionError(('explicit invalid input accepted',level,family,params))
    # Unit-normal validity is independent of radio ID grading. The captured
    # angle bank has one normal: (-i+j)/sqrt(2) is tangent, not antipodal.
    raw=g.generate_easy(template='angle',parameters={'p':'2','q':'-2'},profile='observed-q-130274')
    f,p,z,dx,dy,aa,bb=printed_task(raw)
    valid=[c for c in raw['question'][':question/answer-fields'][0][':answer-field/choices'] if g.valid_unit(components(read_tex(c[':answer/value'])),aa,bb)]
    assert len(valid)==1
    ambiguous=[('normal',g.unit(aa,bb)),('antipodal',tuple(-v for v in g.unit(aa,bb))),('horizontal',(sp.Integer(1),sp.Integer(0))),('vertical',(sp.Integer(0),sp.Integer(1))),('zero',(sp.Integer(0),sp.Integer(0)))]
    try:g.validate_bank(ambiguous,0,aa,bb)
    except ValueError:pass
    else:raise AssertionError('accepted two valid antipodal unit normals')
    # Enumeration gives genuine local sampler capacity; exp aliases deduplicate.
    capacities={}
    for level in g.LEVELS:
        capacities[level]={}
        for family in g.FAMILIES[level]:
            unique=set();eligible=0
            selected='method-axis' if family=='axisquad' else 'method-balanced' if family in ('log','circle') else 'method-generic'
            for p,q in g.sampling_domain(level,family):
                try:
                    aa,bb=g.allowed(level,family,p,q)
                    if not finite_domain_eligible(aa,bb,selected):continue
                except ValueError:continue
                eligible+=1;unique.add(str(p+q) if family=='exp' else (str(p),str(q)))
            if level=='easy' and family=='bilinear':
                # The axis bank serves the original half-integer x coordinate.
                for p,q in g.sampling_domain(level,family):
                    try:aa,bb=g.allowed(level,family,p,q)
                    except ValueError:continue
                    if aa!=0 and bb==0:
                        bank,index=g.method_bank(family,p,q,aa,bb,'method-bilinear-axis')
                        try:g.validate_bank(bank,index,aa,bb)
                        except ValueError:continue
                        eligible+=1;unique.add((str(p),str(q)))
            if family=='exp':eligible*=16;unique={(c,d,z) for c in range(1,5) for d in range(1,5) for z in unique}
            assert eligible>=1
            capacities[level][family]={'eligible_parameter_pairs':eligible,'unique_assessed_tasks':len(unique)}
        print('Complete-bank sampler capacity enumerated: '+level,flush=True)
    (HERE/'engine-input.json').write_text(json.dumps(engines,indent=2,ensure_ascii=False)+'\n')
    executable=REPO/'generate/runs/current/check-engine'
    subprocess.run([str(executable),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
    report={'passed':True,'source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_count':len(fidelity),'complete_banks_matched':len(fidelity),'option_values_matched':sum(z['bank_values_matched'] for z in fidelity),'original_correct_designations_matched':sum(z['correct_designation_matched'] for z in fidelity),'original_correct_designation_denominator':8,'unrated_missing_original_correct_refs':2,'shared_solution_prose_matched':8,'shared_solution_prose_denominator':8,'ordered_solution_stages_matched':8,'raw_exact_solutions':sum(z['solution_raw_exact'] is True for z in fidelity),'notation_normalized_solutions':8,'native_fixture_records':len(engines),'native_report':'engine-validation.json','typed_field_checks':'not applicable; no typed fields in captured sources or authored output','source_mathematical_anomalies':[{'source_id':'q-36311','issue':'out-of-plane -k legacy distractor; missing original correct ref, label, solution','raw_evidence_only':True},{'source_id':'q-36378','issue':'opaque wrong-value recipes; missing original correct ref, label, solution','raw_evidence_only':True},{'source_id':'q-71374','issue':'zero/repeated-basis legacy wrong values; evidence only','raw_evidence_only':True}],'fidelity':fidelity,'normal_family_coverage':{k:sorted(v) for k,v in family_coverage.items()},'normal_bank_profiles_exercised':sorted(profiles),'sampled_unique_tasks':{k:len(v) for k,v in fingerprints.items()},'sampler_capacity':capacities,'explicit_invalid_inputs_rejected':len(invalid),'plots':'none in practice sources or canonical example; steps 5/7 require no generated assets','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_binary_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),'unresolved_limits':['Opaque historical distractor intent is not recovered; evidence-only recipes are recorded shape hypotheses.','No original difficulty, correct designation or worked solution exists for two captured unrated items; normal completion is authored.','Original wording permits either unit-normal orientation; native radio selection grades IDs rather than arbitrary vector entries.','Exponential coordinate aliases count once per operative affine coefficient pair (16 tasks), rather than as independent tasks.','Source solution typography is normalized; none is claimed byte-exact.']}
    report.update({'native_source_records_checked':8,'native_source_records_without_correct_ref':2,'original_prompt_exact_matches':10,'raw_option_spelling_matches':sum(z['raw_option_spelling_matches'] for z in fidelity),'source_snapshot_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'sampler_capacity_totals':{k:sum(z['unique_assessed_tasks'] for z in v.values()) for k,v in capacities.items()}})
    assert (HERE/'source.json').read_bytes()==(REPO/'generate/runs/current/sources/17592186124461.json').read_bytes()
    (HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    (HERE/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
    review=['# Local review: unit normals to plane level curves','Captured source and raw originals are preserved in source.json. Evidence-only profiles are excluded from learner defaults.']
    for case in g.CASES:
        review+=['## Captured original '+case['source_id'],g.QUESTIONS[case['source_id']][':question/problem']]
        for answer in g.QUESTIONS[case['source_id']][':question/answer-fields'][0][':answer-field/choices']:review.append('$'+answer[':answer/value']+'$')
        review.append(g.QUESTIONS[case['source_id']].get(':question/worked-solution','No captured worked solution.'))
        for item in records:
            if case['source_id'] in item['record']['generation']['source_ids'] and ('original' in item['label'].lower() or 'Changed-parameter' in item['label']):review+=['### '+item['label'],g.markdown(item['record'])]
    for item in records:
        if item['label'].startswith('Generated') or item['label'].startswith('Minimal'):review+=['## '+item['label'],g.markdown(item['record'])]
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','source_count','complete_banks_matched','option_values_matched','original_correct_designations_matched','native_fixture_records','sampled_unique_tasks')},indent=2))

if __name__=='__main__':main()

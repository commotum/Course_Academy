#!/usr/bin/env python3
"""Independent displayed-math, scope, fidelity, identity and native grading QA."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
WORK=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x',real=True)

def write(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def norm(text):return text.replace(g.C,'csc').replace(r'\csc','csc').replace('⁡','')

def scalar(s):return g.parse_value(s.strip().rstrip('.,'))

def calls(text):
    """Read displayed trig arguments, not generation parameters."""
    t=norm(text); result=[]
    for match in re.finditer(r'csc\s*\(',t):
        start=match.end();depth=1;i=start
        while i<len(t) and depth:
            depth+=(t[i]=='(')-(t[i]==')');i+=1
        assert depth==0,('unterminated csc',text)
        result.append((match.start(),i,t[start:i-1]))
    return result

def reduction_value(argument):
    a=scalar(argument)
    assert sp.diff(a,X)==1,('new identity branch',argument)
    shift=sp.simplify((a-X)/(2*sp.pi))
    assert shift.is_integer is True,('not a whole period',argument)
    return shift

def evaluated(text,c):
    t=norm(text)
    # Replace only complete trig components, then parse the actual scalar text.
    for i,j,argument in reversed(calls(t)):
        reduction_value(argument)
        t=t[:i]+'('+g.tex(c)+')'+t[j:]
    t=re.sub(r'csc\s*x\b',lambda _: '('+g.tex(c)+')',t)
    return scalar(t)

def formatting(text):
    assert text.count('$$')%2==0
    rest=text.replace('$$','')
    assert rest.count('$')%2==0
    balance=0
    for char in text:
        balance+=(char=='{')-(char=='}')
        assert balance>=0,('closing group',text)
    assert balance==0
    assert '\\\\frac' not in text and '\\\\sqrt' not in text
    assert '+-' not in text and '--' not in text

def displayed_check(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    q=record['question'];m=record['generation']
    for key in (':question/problem',':question/worked-solution'):
        if key in q:formatting(q[key])
    problem=q[':question/problem']; parts=re.findall(r'\$(.*?)\$',problem,re.S)
    assert len(parts)==2
    given=norm(parts[0]);assert re.match(r'csc\s*x\s*=',given)
    c=scalar(given.split('=',1)[1]);assert c>1
    expression=parts[1].rstrip('?')
    actual_angles=[reduction_value(arg) for _,_,arg in calls(expression)]
    assert len(actual_angles)==(2 if m['template']=='two_terms' else 1)
    target=evaluated(expression,c)
    field=q[':question/answer-fields'][0]
    assert len(q[':question/answer-fields'])==1 and field[':answer-field/key']=='selection'
    assert field[':answer-field/type'] in (':answer-field.type/radio',{':db/ident':':answer-field.type/radio'})
    answers=field[':answer-field/choices'];assert len(answers)==5
    parsed=[scalar(a[':answer/value']) for a in answers]
    assert len(set(a[':answer/id'] for a in answers))==5
    for i,a in enumerate(answers):
        formatting(a[':answer/value']); assert a[':answer/type'] in (':answer.type/math',{':db/ident':':answer.type/math'})
        assert parsed[i].is_real is True and parsed[i].is_finite is True
        for b in parsed[i+1:]:assert sp.simplify(parsed[i]-b)!=0,('ambiguous',record)
    hits=[i for i,v in enumerate(parsed) if sp.simplify(v-target)==0];assert len(hits)==1
    # Independently recover affine weights and offset from the ACTUAL expression,
    # then verify every authored distractor's claimed operation, not just inequality.
    if not m['evidence_only']:
        t=norm(expression);occurrences=calls(t);components=[]
        for index,(i,j,arg) in enumerate(occurrences):
            left=0 if index==0 else occurrences[index-1][1]
            between=t[left:i]
            if index==0:components.append(scalar(between) if between.strip() else sp.Integer(1))
            else:
                # Hard puts the constant between its two source-shaped terms.
                match=re.search(r'([+-])([^+-]+)$',between)
                assert match is not None
                components.append(scalar(match.group(1)+match.group(2)))
        Z=sp.Symbol('z')
        poly=t
        for i,j,arg in reversed(occurrences):poly=poly[:i]+'z'+poly[j:]
        polynomial=scalar(poly);b=polynomial.subs(Z,0)
        a=components[0];n=actual_angles[0]
        f=m['template']
        if f in ('legacy_integer','legacy_fraction','direct_radical'):
            expected=[c,1/c,-c,c+2*n*sp.pi,2*n*c]
        elif f=='scaled_integer':expected=[a*c,c,a+c,a/c,a*(c+2*n*sp.pi)]
        elif f.startswith('reciprocal'):expected=[a*c+b,c+b,a*c,b-a*c,a*c-b]
        elif f=='affine_radical':expected=[a*c+b,c+b,a*c,a*(c+b),a*c-b]
        else:
            d=components[1];expected=[(a+d)*c+b,a*c+b,d*c+b,(a-d)*c+b,(a+d)*c-b]
        assert all(sum(sp.simplify(value-e)==0 for value in parsed)==1 for e in expected),('wrong operation bank',f,parsed,expected)
    if ':answer-field/correct' in field:
        correct=field[':answer-field/correct'];cid=correct[':answer/id'] if isinstance(correct,dict) else correct[1]
        assert answers[hits[0]][':answer/id']==cid
    if ':question/worked-solution' not in q:return
    solution=q[':question/worked-solution']
    # Check displayed period, substitutions, every equality stage and final prose.
    period=re.search(r'is \$(.*?)\$',solution).group(1)
    assert scalar(period)==2*sp.pi
    indices=[int(n) for n in re.findall(r'Substituting \$n=(-?\d+)\$',solution)]
    assert indices==actual_angles
    stages=0
    for math in re.findall(r'\$\$(.*?)\$\$',solution,re.S):
        math=math.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        lhs=None
        for row in math.split(r'\\'):
            row=row.strip().replace('&','').strip()
            eq=row.split('=')
            if len(eq)<2:continue
            if eq[0].strip():lhs=evaluated(eq[0],c)
            assert lhs is not None
            for component in eq[1:]:
                right=evaluated(component,c)
                assert sp.simplify(lhs-right)==0,('invalid worked stage',row,component,lhs,right)
                lhs=right;stages+=1
    assert stages>=3
    for math in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',solution,re.S):
        if '=' not in math or math.startswith('y=') or math.startswith('n='):continue
        left,right=math.split('=',1)
        assert sp.simplify(evaluated(left,c)-evaluated(right,c))==0,('incorrect solution prose',math)
    # Verify the final displayed arithmetic answers requested expression.
    if m['template'] not in ('legacy_integer','legacy_fraction','direct_radical'):
        last=re.findall(r'\$\$(.*?)\$\$',solution,re.S)[-1].replace(r'\end{aligned}','').split('=')[-1]
        assert sp.simplify(scalar(last)-target)==0
    # Structural stages: source integer quotient has extra unevaluated row.
    aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
    # A wrong intermediate full-period offset is still numerically periodic;
    # exact angle-relation QA must detect that teaching-stage error separately.
    reduction_chains=aligned[:len(actual_angles)]
    for chain,n in zip(reduction_chains,actual_angles):
        arguments=[scalar(arg) for _,_,arg in calls(chain)]
        assert len(arguments)==2
        assert all(sp.simplify(arg-(X+2*n*sp.pi))==0 for arg in arguments),('displayed intermediate angle mismatch',chain)
    if m['template']=='reciprocal_integer':
        chain=aligned[-1];assert chain.count(r'\\')==3
        assert re.search(r'\\frac\{\d+\}\{\d+\}',chain)
    if m['template']=='reciprocal_fraction':assert aligned[-1].count(r'\\')==2
    if m['template']=='affine_radical':assert len(aligned)==1
    if m['template']=='two_terms':assert len(aligned)==3 and aligned[-1].count(r'\\')==2


def native_record(record):
    r=copy.deepcopy(record)
    for f in r['question'][':question/answer-fields']:
        if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
        for a in f[':answer-field/choices']:
            if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
        if isinstance(f.get(':answer-field/correct'),dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
    return r

def main():
    # Frozen provenance and every nested source attribute/order/ref are compared.
    frozen=WORK/'generate/runs/current/sources/17592186176054.json'
    assert (HERE/'source.json').read_bytes()==frozen.read_bytes()
    cases=[];raw_records=[];review=[];source_rows=[]
    for sid,q in g.SOURCES.items():
        f=g.FAMILY[sid];level=g.TLEVEL[f];p=g.ORIGINAL[sid]
        raw=g.generate(level,parameters=p,profile='raw:'+sid)
        assert raw['question']==q,('source fidelity',sid)
        assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']
        displayed_check(raw);raw_records.append(raw)
        normal=g.generate(level,template=f,parameters=p)
        displayed_check(normal);review.extend([raw,normal])
        if ':question/worked-solution' in q:assert normal['question'][':question/worked-solution']==q[':question/worked-solution']
        assert normal['question'][':question/problem']==q[':question/problem']
        cases.append({'source_id':sid,'template':f,'level':level,'parameters':p,'bank_profile':'raw:'+sid,'missing_observed_difficulty':':question/difficulty' not in q})
        source_rows.append({'source_id':sid,'raw_exact':True,'full_bank_values':5,'correct_ref_match':':answer-field/correct' in q[':question/answer-fields'][0],'solution_exact':':question/worked-solution' in q,'normal_prompt_exact':True,'normal_solution_exact':':question/worked-solution' in q})
        # Every evidence bank generalizes at changed parameters through PUBLIC API.
        for seed in (111,217):
            variant=g.generate(level,seed,profile='raw:'+sid)
            assert variant['generation']['parameters']!={k:str(v) for k,v in g.params(p).items()}
            displayed_check(variant);review.append(variant)
        variant=g.generate(level,891,template=f);displayed_check(variant);review.append(variant)
    for seed in (29,57):
        variant=g.generate_hard(seed);displayed_check(variant);review.append(variant)
    # Default family coverage and changed-parameter mathematics at every level.
    sample_count=0;coverage=set();tasks={level:set() for level in g.LEVELS};witnesses={level:set() for level in g.LEVELS}
    all_normal=[]
    for level in g.LEVELS:
        for seed in range(80):
            r=g.generate(level,seed);displayed_check(r);all_normal.append(r)
            coverage.add(r['generation']['template']);tasks[level].add(r['generation']['mathematical_fingerprint']);witnesses[level].add(r['generation']['content_fingerprint']);sample_count+=1
    assert coverage==set(g.TEMPLATES),coverage
    for f in g.TEMPLATES:
        r=g.generate(g.TLEVEL[f],701,template=f)
        p=r['generation']['parameters']
        a=g.generate(g.TLEVEL[f],0,template=f,parameters=p);b=g.generate(g.TLEVEL[f],93,template=f,parameters=p)
        assert a['question'][':question/id']==b['question'][':question/id']
        assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
        assert sorted(x[':answer/id'] for x in a['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(x[':answer/id'] for x in b['question'][':question/answer-fields'][0][':answer-field/choices'])
        p2=dict(p,n='1' if int(p['n'])!=1 else '2')
        if f=='two_terms' and p2['n']==p2['m']:p2['n']='3'
        c=g.generate(g.TLEVEL[f],5,template=f,parameters=p2)
        assert a['generation']['mathematical_fingerprint']==c['generation']['mathematical_fingerprint']
        assert a['question'][':question/id']!=c['question'][':question/id']
    # Task alias checks across bank/profiles and legacy/modern direct notation.
    p=dict(c='4',n=2,a='1',b='0')
    a=g.generate_easy(parameters=p,template='legacy_integer');b=g.generate_easy(parameters=p,profile='raw:q-66472')
    assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
    assert a['question'][':question/id']!=b['question'][':question/id']
    alias=g.generate_easy(parameters=dict(p,c='8/2'),template='legacy_integer',profile='operations')
    assert alias['question'][':question/id']==a['question'][':question/id']
    assert alias['generation']['mathematical_fingerprint']==a['generation']['mathematical_fingerprint']
    # Hard commutative term-order aliases share tasks, while each full displayed
    # bank/prompt/solution keeps its own identity.
    hard=g.generate_hard(912,parameters=dict(c='sqrt(2)',a='1/2',d='-1/3',b='2',n=1,m=2))
    hp=dict(hard['generation']['parameters'])
    hp['a'],hp['d']=hp['d'],hp['a'];hp['n'],hp['m']=hp['m'],hp['n']
    swapped=g.generate_hard(11,parameters=hp)
    assert swapped['generation']['mathematical_fingerprint']==hard['generation']['mathematical_fingerprint']
    assert swapped['question'][':question/id']!=hard['question'][':question/id']
    displayed_check(swapped)
    first_positions={next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in all_normal}
    assert first_positions==set(range(5))
    invalid=[('easy','legacy_integer',dict(c='1/2',a='1',b='0',n=2)),('easy','scaled_integer',dict(c='2',a='2',b='0',n=2)),('moderate','reciprocal_fraction',dict(c='4',a='1/2',b='2',n=1)),('moderate','reciprocal_integer',dict(c='3',a='1/2',b='2',n=1)),('moderate','affine_radical',dict(c='sqrt(2)',a='1',b='-1',n=1)),('hard','two_terms',dict(c='4',a='1/2',d='-1/2',b='2',n=1,m=2)),('hard','two_terms',dict(c='4',a='1',d='-1/3',b='2',n=1,m=2)),('easy','legacy_integer',dict(c='4',a='1',b='0',n='1/2'))]
    for level,f,p in invalid:
        try:g.generate(level,parameters=p,template=f)
        except ValueError:pass
        else:raise AssertionError(('guard bypass',f,p))
    # Mutation tests establish independent checks can catch bank/stage/prose/angle errors.
    mutant=copy.deepcopy(all_normal[0]);mutant['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='1/0'
    try:displayed_check(mutant)
    except (AssertionError,ValueError):pass
    else:raise AssertionError('invalid math mutation escaped')
    r=g.generate_moderate(template='reciprocal_integer',parameters=g.ORIGINAL['q-103822'])
    for old,new in [(r'\frac{6}{3}+5',r'\frac{7}{3}+5'),('Substituting $n=8$','Substituting $n=7$'),('=6.$','=7.$'),(r'2\cdot 8\cdot',r'2\cdot 7\cdot')]:
        mutant=copy.deepcopy(r);assert old in mutant['question'][':question/worked-solution'];mutant['question'][':question/worked-solution']=mutant['question'][':question/worked-solution'].replace(old,new)
        try:displayed_check(mutant)
        except (AssertionError,ValueError):pass
        else:raise AssertionError(('worked-math mutation escaped',old))
    # Real application grading all five owned choices for every native-eligible review
    # plus sample banks. Source omissions remain omissions; no invented designation.
    fixtures=[]
    for i,r in enumerate(review+all_normal[:12]+all_normal[80:92]+all_normal[160:172]):
        if ':answer-field/correct' not in r['question'][':question/answer-fields'][0]:continue
        native=native_record(r);f=native['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
        fixtures.append({'label':str(i)+':'+r['generation']['template'],'record':native,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'all original/authored owned bank choices'} for a in f[':answer-field/choices']]})
    # Meaningful typed equivalents through a private blank fixture, not a change to
    # observed radio shape: unsimplified substitution product/sum plus wrong sign.
    for f in ('scaled_integer','reciprocal_integer','affine_radical','two_terms'):
        r=g.generate(g.TLEVEL[f],703,template=f);native=native_record(r);field=native['question'][':question/answer-fields'][0]
        field[':answer-field/type']=':answer-field.type/blank';native['question'][':question/problem']+='\n\n{{selection}}'
        p=g.params(r['generation']['parameters']);equivalent='('+str(p['a'])+')*('+str(p['c'])+')+('+str(p['b'])+')'
        if f=='two_terms':equivalent+=' + ('+str(p['d'])+')*('+str(p['c'])+')'
        wrong='('+equivalent+')+1'
        fixtures.append({'label':'typed-equivalent:'+f,'record':native,'checks':[{'submitted':equivalent,'expected':'accepted','purpose':'unreduced displayed substitution expression in separate typed fixture'},{'submitted':wrong,'expected':'rejected','purpose':'unequal typed expression'}]})
    write('engine-input.json',fixtures)
    subprocess.run([str(WORK/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    native=json.loads((HERE/'engine-report.json').read_text())
    write('source-cases.json',cases);write('review.json',review)
    # Exhaustive finite numerical-task counting, with reduced rational aliases
    # removed and period indices/notation/bank profiles excluded. Hard counts the
    # union of eligible term orders, not two copies of a commutative weighted sum.
    rational={F(i) for i in range(2,13)}|{F(i,j) for j in range(2,6) for i in range(j+1,13)}
    weights={F(i,j) for j in range(2,7) for i in range(1,6) if F(i,j).denominator>1 and F(i,j)<=3}
    hard=6*len(weights)*(len(weights)-1)*12
    for c in rational:
        for a in weights:
            for d_abs in weights:
                if a==d_abs:continue
                hard+=sum(b!=0 and b not in (-d_abs*c/2,a*c/2) for b in range(-6,7))
    finite={'direct':len(rational)+6,'scaled_integer':sum(len({F(a*c),F(c),F(a+c),F(a,c)})==4 for c in range(2,13) for a in range(2,9)),
      'reciprocal_integer':sum(c%d==0 and b not in (F(c,d),2*F(c,d)) for c in range(2,13) for d in range(2,7) for b in range(1,9)),
      'reciprocal_fraction':sum(c%d!=0 and b not in (F(c,d),2*F(c,d)) for c in range(2,13) for d in range(2,7) for b in range(1,9)),
      'affine_radical':6*7*6,'hard_two_terms':hard}
    assert finite=={'direct':38,'scaled_integer':75,'reciprocal_integer':104,'reciprocal_fraction':296,'affine_radical':252,'hard_two_terms':108240}
    write('validation.json',{'passed':True,'source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'raw_exact_questions':7,'complete_banks':7,'matched_source_choices':35,'total_source_choices':35,'matched_correct_designations':5,'total_present_correct_designations':5,'missing_source_correct_designations':2,'raw_exact_solutions':5,'total_present_source_solutions':5,'normal_exact_solutions_at_source_parameters':5,'normal_exact_prompts':7,'source_checks':source_rows,'normal_math_samples':sample_count,'default_family_coverage':sorted(coverage),'conceptual_workloads':4,'finite_numeric_task_domains':finite,'deduplicated_sample_tasks':{k:len(v) for k,v in tasks.items()},'numerical_presentation_witnesses':{k:len(v) for k,v in witnesses.items()},'finite_limits':'Four conceptual workloads (direct, one product, affine, two reductions); bank/family notation and full-period shifts are excluded from task counts. Numerical samples are bounded witnesses, not proof of unlimited conceptual variety.','explicit_rejection_checks':len(invalid),'mutation_checks':5,'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':native['documented_unresolved_checks'],'engine_sha256':hashlib.sha256((WORK/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__,'plots':'none; no original assessed assets','unresolved':['Historical wrong-operation intent is underdetermined for several banks; all raw profiles evidence-only.','Two unrated originals lack correct designation/solution; normal designation and easy workload assignment are independently authored.','Hard has no observed examples; two-reduction workload is an authored same-skill design claim.']})
    print('PASS: 7/7 exact raw sources, 35/35 source choices, 5/5 normal source solutions; 240 math variants and native grading.')

if __name__=='__main__':main()

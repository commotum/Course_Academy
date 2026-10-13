#!/usr/bin/env python3
"""Independent printed-prompt, whole-bank, ordered-stage, native-grader QA."""
import hashlib, importlib.util, itertools, json, math, re, subprocess
from functools import lru_cache
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
@lru_cache(maxsize=8192)
def parse(s):
    s=s.strip().rstrip('.').replace(r'\,','').replace(r'\cdot','*')
    s=re.sub(r'\^\{(\d+)\}',r'**\1',s).replace('^','**').replace('{','').replace('}','')
    return sp.expand(parse_expr(s,transformations=standard_transformations+(implicit_multiplication_application,)))
@lru_cache(maxsize=8192)
def lcm(A,B):
    variables=sorted(A.free_symbols|B.free_symbols,key=str)
    return sp.Poly(A,*variables,domain=sp.ZZ).lcm(sp.Poly(B,*variables,domain=sp.ZZ)).as_expr()
def split_top(s):
    depth=0;pieces=[];start=0
    for i,ch in enumerate(s):
        depth+=(ch=='(');depth-=(ch==')')
        if ch==',' and depth==0:pieces.append(s[start:i]);start=i+1
    return pieces+[s[start:]]
def value(s):
    s=s.strip().rstrip('.').replace(r'\,','')
    if s.startswith(r'\text{LCM}'):
        text=s[len(r'\text{LCM}'):];assert text[0]=='(' and text[-1]==')'
        args=split_top(text[1:-1]);assert len(args)==2
        A,B=map(parse,args)
        if not A.free_symbols and not B.free_symbols:return sp.Integer(math.lcm(int(A),int(B)))
        return lcm(A,B)
    return parse(s)
def eq(x,y):return sp.expand(x-y)==0
def formatting(s):
    assert not any(ord(ch)<32 and ch!='\n' for ch in s)
    assert s.count('$')%2==0
    assert '\\\\' not in s,'adjacent decoded slashes'
    depth=0
    for ch in s:
        if ch=='{':depth+=1
        if ch=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert '--' not in s and '+-' not in s
def factored(A):
    c,terms=sp.factor_list(A);return int(c),{sp.expand(F):e for F,e in terms}

def printed_factor_order(s):
    # Complete slots are decoded from the actual first prompt polynomial.
    body=re.sub(r'^\d+','',s.strip().rstrip('.'))
    tokens=re.findall(r'(\([a-z]\s*[+-]\s*\d+\)|\{[a-z]\}|[a-z])(?:\^\{(\d+)\})?',body)
    assert len(tokens)==2,(s,tokens)
    return [(parse(base),int(exponent) if exponent else 1) for base,exponent in tokens]

def check(r,raw=False):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.KP
    q=r['question'];m=r['generation'];f=q[':question/answer-fields'][0]
    formatting(q[':question/problem']);printed=re.findall(r'\$([^$]*)\$',q[':question/problem']);assert len(printed)==2
    A,B=map(parse,printed);expected=lcm(A,B)
    assert len(A.free_symbols)==len(B.free_symbols)==2 and A.free_symbols==B.free_symbols
    ac,at=factored(A);bc,bt=factored(B)
    assert ac>=2 and bc>=2 and ac!=bc
    assert at.keys()==bt.keys() and len(at)==2
    for F in at:
        assert len(F.free_symbols)==1 and sp.Poly(F,*F.free_symbols).degree()==1
        assert sp.Poly(F,*F.free_symbols).LC()==1
    assert at!=bt
    if m['level']=='hard':
        ex=list(at.values())+list(bt.values());assert min(ex)>=2 and 7<=max(ex)<=9
        assert 12<=min(ac,bc) and max(ac,bc)<=30 and math.gcd(ac,bc)>1 and ac%bc and bc%ac and 120<math.lcm(ac,bc)<=180
    elif m['level']=='moderate':
        assert 4<=min(ac,bc) and 9<=max(ac,bc)<=20 and math.gcd(ac,bc)>1 and ac%bc and bc%ac and 3<=max(list(at.values())+list(bt.values()))<=6
    elif m['level']=='easy':
        assert max(ac,bc)<=9 and math.gcd(ac,bc)==1 and math.lcm(ac,bc)<=60 and max(list(at.values())+list(bt.values()))<=5
    if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    answers=f[':answer-field/choices'];vals=[parse(a[':answer/value']) for a in answers]
    assert len(answers)==(5 if f[':answer-field/type'].endswith('/radio') else 1)
    assert len(set(a[':answer/id'] for a in answers))==len(answers)
    for a,v in zip(answers,vals):
        formatting(a[':answer/value']);assert '$' not in a[':answer/value']
        assert v.free_symbols==A.free_symbols
    assert not any(eq(x,y) for i,x in enumerate(vals) for y in vals[i+1:])
    assert sum(eq(x,expected) for x in vals)==1
    # Verify every displayed distractor against its complete bank operation,
    # using printed factor ordering/powers and independently recovered content.
    orderedA=printed_factor_order(printed[0]);orderedB=printed_factor_order(printed[1])
    assert [x[0] for x in orderedA]==[x[0] for x in orderedB]
    F,G=[x[0] for x in orderedA];p,qx=[x[1] for x in orderedA];rr,ss=[x[1] for x in orderedB]
    E,H=max(p,rr),max(qx,ss);M,N=min(p,rr),min(qx,ss);lc=math.lcm(ac,bc)
    if len(answers)==5:
        if m['bank']=='method_bank':nodes=[(lc,E,H),(lc,M,N),(math.gcd(ac,bc),E,H),(lc,p+rr,qx+ss),(lc,H,E)]
        elif m['bank']=='product_sum_swap':nodes=[(lc,p+rr,qx+ss),(lc,E,H),(ac*bc,E,H),(ac*bc,p+rr,qx+ss),(lc,H,E)]
        elif m['bank']=='opaque_patterns':
            assert lc%2==0
            nodes=[(3*lc//2,M,H),(lc,2*p,qx+ss),(lc,E,H),(lc,M,H),(3*lc//2,M,H+1)]
        else:raise AssertionError('Unknown complete bank')
        wanted=[sp.expand(c*F**e*G**h) for c,e,h in nodes]
        assert all(sum(eq(v,w) for v in vals)==1 for w in wanted),'displayed whole bank differs from operation profile'
    if ':answer-field/correct' in f:
        correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
        selected=[i for i,a in enumerate(answers) if a[':answer/id']==correct[1]];assert len(selected)==1
        assert eq(vals[selected[0]],expected)
    else:assert raw and m['raw_missing_attributes']
    if ':question/worked-solution' not in q:
        assert raw and m['raw_missing_attributes'];return A,B,expected
    sol=q[':question/worked-solution'];formatting(sol);parts=sol.split('\n\n');assert len(parts)==12
    assert parts[0]==g.OPENING
    assert parts[1].startswith('So first, we find ')
    assert parts[2].startswith('- Multiples of ') and parts[3].startswith('- Multiples of ')
    assert parts[4].startswith('So, ')
    assert parts[5].startswith('To find ') and 'we find the largest powers for' in parts[5]
    assert parts[6].startswith('- For ') and parts[7].startswith('- For ')
    assert parts[8].startswith('Now, we raise ') and parts[8].endswith('Therefore,')
    assert parts[9].startswith('$$\n') and parts[10]=='Finally, we multiply all of our results together:' and parts[11].startswith('$$\n')
    # Numeric formal operation and complete multiples arithmetic sequence.
    formal=re.search(r'\\text\{LCM\}\((\d+),(\d+)\)',parts[1]);assert formal
    assert tuple(map(int,formal.groups()))==(ac,bc)
    for paragraph,c in zip(parts[2:4],(ac,bc)):
        label,listing=re.findall(r'\$([^$]*)\$',paragraph);assert int(label.rstrip(':'))==c
        values=[int(x) for x in re.findall(r'\d+',listing)]
        assert values==[c*i for i in range(1,math.lcm(ac,bc)//c+2)]
        assert listing.endswith(',…')
    # The actual prose's two variable products, bases and maximum comparisons.
    tokens=re.findall(r'\$([^$]*)\$',parts[5]);assert len(tokens)==5
    assert eq(parse(tokens[1]),A/ac) and eq(parse(tokens[2].rstrip(',')),B/bc)
    bases=[parse(tokens[3]),parse(tokens[4])];assert set(bases)==set(at)
    for para,F in zip(parts[6:8],bases):
        ts=re.findall(r'\$([^$]*)\$',para);assert len(ts)==3
        assert eq(parse(ts[0]),F**at[F]) and eq(parse(ts[1].rstrip(',')),F**bt[F])
        assert int(ts[2].rstrip('.'))==max(at[F],bt[F])
    ts=re.findall(r'\$([^$]*)\$',parts[8]);assert list(map(parse,ts))==bases
    # All ordered formal and reduction stages are parsed from their printed text.
    numeric=re.findall(r'\$([^$]*)\$',parts[4])[0].rstrip('.')
    varstage=parts[9][3:-3].strip().rstrip('.');finalstage=parts[11][3:-3].strip().rstrip('.')
    stages=[numeric,varstage,finalstage]
    evaluated=[]
    for stage in stages:
        components=stage.split('=');assert len(components)==2
        actual=list(map(value,components));assert eq(actual[0],actual[1]),stage
        evaluated.append(actual[1])
    assert evaluated[0]==math.lcm(ac,bc)
    primitive_expected=expected/math.lcm(ac,bc)
    assert eq(evaluated[1],primitive_expected) and eq(evaluated[2],expected)
    # Structural formal operands remain separate and in the same source order.
    varargs=split_top(varstage.split('=',1)[0][len(r'\text{LCM}('):-1].replace(r'\,',''))
    finalargs=split_top(finalstage.split('=',1)[0][len(r'\text{LCM}('):-1].replace(r'\,',''))
    assert len(varargs)==len(finalargs)==2
    assert eq(parse(varargs[0]),A/ac) and eq(parse(varargs[1]),B/bc)
    assert eq(parse(finalargs[0]),A) and eq(parse(finalargs[1]),B)
    separated=varstage.split('=',1)[1].split(r'\cdot');assert len(separated)==2
    assert all(eq(parse(s),F**max(at[F],bt[F])) for s,F in zip(separated,bases))
    return A,B,expected

def native(r,label):
    f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    choices=f[':answer-field/choices'];_,_,answer=check(r)
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete bank option'} for a in choices]
    else:
        val=choices[0][':answer/value'];expanded=str(sp.expand(answer)).replace('**','^')
        v,w=sorted(answer.free_symbols,key=str);content=int(sp.Poly(answer,v,w,domain=sp.ZZ).content())
        # Actual parser limits are a documented substantive grading restriction.
        # These entries contain only plain numbers/one-letter variables/operators,
        # so the following token count matches symbolic.rs::lex exactly.
        token_count=len(re.findall(r'\d+|[a-z]|[^\s\da-z]',expanded))
        full_limit=token_count>512 or len(expanded.encode())>4096
        F,G=[x[0] for x in printed_factor_order(re.findall(r'\$([^$]*)\$',r['question'][':question/problem'])[0])]
        _,terms=factored(answer);E,H=terms[F],terms[G]
        partial=f'{content}*('+str(sp.expand(F**E)).replace('**','^')+')*('+str(G)+')^'+str(H)
        assert eq(parse(partial),answer)
        checks=[{'submitted':val,'expected':'accepted','purpose':'canonical'},
          {'submitted':expanded,'expected':'unresolved' if full_limit else 'accepted','purpose':f'fully expanded equivalent; documented native limit4096 bytes /512 tokens; entry tokens={token_count}' if full_limit else 'fully expanded equivalent'},
          {'submitted':partial,'expected':'accepted','purpose':'partially expanded equivalent within native input limits'},
          {'submitted':'('+val+')/1','expected':'accepted','purpose':'unreduced equivalent'},
          {'submitted':'('+val+')/'+str(content),'expected':'rejected','purpose':'missing integer content'},
          {'submitted':'-('+val+')','expected':'rejected','purpose':'negative associate'},
          {'submitted':'2*('+val+')','expected':'rejected','purpose':'larger scalar multiple'},
          {'submitted':'('+val+')+1','expected':'rejected','purpose':'wrong polynomial'}]
    return {'label':label,'record':r,'checks':checks}

def main():
    cases=[];reviews=[];engine=[];matches=[];total_options=corrects=solutions=0
    for sid,cfg in g.PROFILES.items():
        p={k:cfg[k] for k in g.KEYS};original=g.QUESTIONS[sid]
        cases.append({'source_id':sid,'template':cfg['template'],'level':cfg['level'],'parameters':p,'bank_profile':'observed_'+sid,'completed_profile':'completed_'+sid,'original_rated':':question/difficulty' in original})
        r=g.generate(cfg['level'],parameters=p,template=cfg['template'],profile='observed_'+sid);check(r,True)
        q=r['question'];sf=original[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        assert q[':question/problem']==original[':question/problem'],(sid,'prompt')
        assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        for key in (':question/difficulty',':question/worked-solution'):
            assert (key in q)==(key in original),(sid,key)
        if ':question/difficulty' in original:assert q[':question/difficulty']==original[':question/difficulty'][':db/ident']
        assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
        rawvals=sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==rawvals,(sid,'entire bank')
        total_options+=len(rawvals)
        if ':answer-field/correct' in sf:
            canonical=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert canonical==sf[':answer-field/correct'][':answer/value'];corrects+=1
        if ':question/worked-solution' in original:
            assert q[':question/worked-solution']==original[':question/worked-solution'],(sid,'complete prose/math sequence');solutions+=1
        reviews.append({'label':'Original and exact parameterized replay '+sid,'original':original,'record':r})
        completed=g.generate(cfg['level'],parameters=p,profile='completed_'+sid);check(completed);engine.append(native(completed,'completed/'+sid))
        if cfg.get('missing'):reviews.append({'label':'Authored completion of missing difficulty/key/solution '+sid,'record':completed})
        # Changed parameters affect contents, exponents, and factor shifts, not only names.
        changed={**p,'h':-4 if p['h']!=-4 else 5,'k':3,'v':'u','w':'w'}
        if cfg['level']=='easy':changed.update(a=5,b=6,p=2,q=1,r=3,s=4)
        else:changed.update(a=10,b=18,p=5,q=2,r=3,s=6)
        variant=g.generate(cfg['level'],seed=33,parameters=changed,profile='completed_'+sid);check(variant)
        reviews.append({'label':'Generated changed-parameter source-profile variant '+sid,'record':variant});engine.append(native(variant,'changed/'+sid))
        matches.append({'source_id':sid,'exact_prompt':True,'exact_field_shape_presence':True,'exact_complete_bank':True,'answer_values':len(rawvals),'matched_correct_designation':':answer-field/correct' in sf,'exact_complete_solution':':question/worked-solution' in original})
    records=[];fingerprints={l:set() for l in ('easy','moderate','hard')};identities=set();correct_positions=set()
    # Every source bank is tested under substantive changed-parameter sampling.
    profile_samples=0
    for sid,cfg in g.PROFILES.items():
        for seed in range(20):
            r=g.generate(cfg['level'],seed=seed,profile='completed_'+sid);check(r);profile_samples+=1
    for level in ('easy','moderate','hard'):
        for template in g.TEMPLATES:
            for seed in range(50):
                r=g.generate(level,seed,template=template);check(r);records.append(r)
                p=r['generation']['parameters'];fingerprints[level].add(r['generation']['mathematical_fingerprint']);identities.add(r['generation']['content_identity'])
                rerun=g.generate(level,seed+101,template=template,parameters=p)
                assert r['question'][':question/id']==rerun['question'][':question/id']
                # Explicit input order reversal and swapped labels are canonicalized as whole tasks.
                swapped={**p,'a':p['b'],'b':p['a'],'p':p['r'],'q':p['s'],'r':p['p'],'s':p['q']}
                reverse=g.generate(level,seed,template=template,parameters=swapped)
                assert r['generation']['mathematical_fingerprint']==reverse['generation']['mathematical_fingerprint']
                aliases={**p,'v':'x','w':'y'}
                renamed=g.generate(level,seed,template=template,parameters=aliases)
                assert r['generation']['mathematical_fingerprint']==renamed['generation']['mathematical_fingerprint']
                if template.endswith('radio'):
                    f=r['question'][':question/answer-fields'][0];correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
                if seed<2:
                    reviews.append({'label':f'Generated {level} {template} seed {seed}','record':r});engine.append(native(r,level+'/'+template+'/'+str(seed)))
    assert correct_positions==set(range(5))
    # Profile aliases whose displayed content is equal must share identity.
    c=g.PROFILES['q-222113'];p={k:c[k] for k in g.KEYS}
    observed=g.generate('moderate',parameters=p,profile='observed_q-222113')
    completed=g.generate('moderate',parameters=p,profile='completed_q-222113')
    assert observed['question'][':question/id']==completed['question'][':question/id']
    p={k:g.PROFILES['q-111597'][k] for k in g.KEYS}
    # Authored/observed presentations with different banks share the mathematical task but differ in content identity.
    raw=g.generate('easy',parameters=p,profile='observed_q-111597')
    default=g.generate('easy',parameters=p,template='factored_radio')
    assert raw['question'][':question/id']!=default['question'][':question/id']
    assert raw['generation']['mathematical_fingerprint']==default['generation']['mathematical_fingerprint']
    invalid=[]
    for level in ('easy','moderate','hard'):
        baseline=g.generate(level,template='factored_radio')['generation']['parameters']
        for replacement in ({'a':-baseline['a']},{'b':baseline['a']},{'v':baseline['w']},{'p':0},{'h':10},{'s':10},{'h':0,'k':0}):invalid.append((level,{**baseline,**replacement}))
    easy=g.generate_easy()['generation']['parameters'];moderate=g.generate_moderate()['generation']['parameters'];hard=g.generate_hard()['generation']['parameters']
    invalid += [('moderate',{**moderate,'p':1,'q':1,'r':2,'s':2}),('moderate',{**moderate,'a':6,'b':12}),('hard',{**hard,'a':12,'b':18}),('hard',{**hard,'p':4,'q':3,'r':5,'s':6}),('hard',{**hard,'p':1}),('easy',{**easy,'a':6,'b':8}),('easy',{**easy,'a':4,'b':10})]
    for level,p in invalid:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('invalid explicit input accepted',level,p))
    # Normal observed/completed profiles use exactly the same guards as defaults.
    profile_negative_checks=0
    for sid,cfg in g.PROFILES.items():
        p={k:cfg[k] for k in g.KEYS}
        bad={**p,'a':4,'b':10} if cfg['level']=='easy' else {**p,'a':5,'b':9}
        for prefix in ('observed_','completed_'):
            try:g.generate(cfg['level'],parameters=bad,profile=prefix+sid)
            except ValueError:profile_negative_checks+=1
            else:raise AssertionError(('profile guard bypass',prefix+sid,bad))
    boundaries=[('easy',dict(a=2,b=3,v='x',w='y',h=-9,k=9,p=1,q=2,r=5,s=3)),('moderate',dict(a=12,b=20,v='u',w='w',h=0,k=-9,p=6,q=3,r=5,s=4)),('hard',dict(a=18,b=20,v='x',w='y',h=-9,k=0,p=9,q=2,r=3,s=8))]
    for level,p in boundaries:
        for t in g.TEMPLATES:
            r=g.generate(level,parameters=p,template=t);check(r);engine.append(native(r,'boundary/'+level+'/'+t))
    # Exhaust all sign/zero-shift presentations at each difficulty boundary.
    sign_checks=0
    for level,p in boundaries:
        for h,k in itertools.product((-9,0,9),repeat=2):
            if h==k==0:continue
            for t in g.TEMPLATES:check(g.generate(level,parameters={**p,'h':h,'k':k},template=t));sign_checks+=1
    write('source-cases.json',cases);write('review.json',reviews);write('engine-input.json',engine)
    binary=REPO/'generate/runs/current/check-engine'
    subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
    er=json.loads((HERE/'engine-validation.json').read_text())
    report={'status':'passed','version':g.VERSION,'source_provenance':{k:v for k,v in g.SOURCE.items() if k!='record'},'practice_sources':6,'source_prompt_exact':'6/6','field_shape_and_presence_exact':'6/6','complete_original_banks_exact':'6/6','all_original_answer_values_exact':f'{total_options}/14','original_correct_designations_exact':f'{corrects}/5','full_original_solution_sequence_exact':f'{solutions}/5','raw_missing_correct_difficulty_solution':1,'authored_missing_correct_reference':1,'authored_unrated_moderate_assignment':1,'authored_missing_solution':1,'presentation_or_mathematical_repairs':0,'raw_unmatched_values':0,'source_replay_details':matches,'normal_instances_checked':len(records),'source_profile_variants_checked':profile_samples,'signed_zero_shift_format_stage_checks':sign_checks,'unique_content_identities':len(identities),'mathematical_tasks_per_level':{l:len(x) for l,x in fingerprints.items()},'all_ordered_formal_arithmetic_and_prose_math_stages':'parsed and independently checked from actual printed output','correct_option_positions_observed':sorted(correct_positions),'invalid_explicit_inputs_rejected':len(invalid),'source_profile_negative_controls_rejected':profile_negative_checks,'native_accepted':er['accepted_checks'],'native_rejected':er['rejected_checks'],'native_unresolved':er['documented_unresolved_checks'],'plot_rating':'none','database_writes':0,'parent_qa':'pending independent review'}
    write('validation.json',report)
    markdown=['# Original and generated review','Raw missing keys are shown as absent. Generated completions and changed-parameter variants are explicitly labeled. Original bank options and full original solutions are included in review.json.']
    for e in reviews:
        markdown += ['\n## '+e['label']]
        if 'original' in e:
            o=e['original'];markdown+=['### Captured original',o[':question/problem']]
            markdown+=['- $'+a[':answer/value']+'$' for a in o[':question/answer-fields'][0][':answer-field/choices']]
            markdown += [o.get(':question/worked-solution','[Original has no worked solution, difficulty, or correct reference.]'),'### Parameterized replay']
        markdown += [g.markdown(e['record'])]
    (HERE/'review.md').write_text('\n\n'.join(markdown)+'\n')
    files=[HERE.with_suffix('.py')]+sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='frozen-manifest.json')+[binary,REPO/'generate/runs/current/check-engine.rs']+[REPO/'engine/rust'/f'{name}.rs' for name in ('learning','symbolic','schema','lib')]
    hashes={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    write('frozen-manifest.json',{'version':g.VERSION,'sympy':sp.__version__,'sha256':hashes,'database_writes':0})
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()

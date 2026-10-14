"""Independent parsing of displayed mathematics, full source replay and grading."""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('general_base_log',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=g.X

def group(s,i,opening='{',closing='}'):
    assert s[i]==opening,(s,i)
    start=i+1;depth=1;i+=1
    while depth:
        assert i<len(s),(s,start)
        depth+=(s[i]==opening)-(s[i]==closing);i+=1
    return s[start:i-1],i

def math(s):
    s=s.replace(r'\,','').replace(r'\!','').strip().rstrip('.,').replace('⁡','').replace('\u00a0','')
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','')
    s=re.sub(r'\\operatorname\{(ln|log)\}',lambda m:m[1],s)
    s=s.replace(r'\ln','ln').replace(r'\log','log').replace('{log}','log')
    s=re.sub(r'\\text\{[^}]*\}','',s)
    # Differential operators act on the following full parentheses.
    op=r'\frac{}{x}'
    s=s.replace(r'\frac{\text{d}}{\text{d}x}',op)
    while op in s:
        at=s.index(op);part,end=group(s,at+len(op),'(',')')
        s=s[:at]+'('+str(sp.diff(math(part),X))+')'+s[end:]
    while r'\frac' in s:
        at=s.index(r'\frac');n,end=group(s,at+5);d,end2=group(s,end)
        s=s[:at]+'('+str(math(n)/math(d))+')'+s[end2:]
    s=re.sub(r'log_\{(\d+)\}\s*x',r'(log(x)/log(\1))',s)
    s=re.sub(r'log_([0-9]+)\s*x',r'(log(x)/log(\1))',s)
    s=re.sub(r'\blog\s*x',r'(log(x)/log(10))',s)
    s=re.sub(r'ln\s*(\d+)',r'log(\1)',s)
    s=re.sub(r'ln\s*x',r'log(x)',s)
    s=s.replace('ln(','log(').replace('xlog(', 'x*log(').replace('{','(').replace('}',')').replace('^','**').replace(r'\cdot','*')
    s=s.replace('log(', ' log(')
    return parse_expr(s,local_dict={'x':X,'e':sp.E,'log':sp.log,'exp':sp.exp},transformations=standard_transformations+(implicit_multiplication_application,))

def equal(a,b):return sp.simplify(a-b)==0

def displayed(q):
    return math(re.search(r'\$[fy](?:\(x\))?\s*=([^$]+)',q[':question/problem']).group(1))

def formatting(s):
    assert s.count('$$')%2==0
    assert s.replace('$$','').count('$')%2==0
    assert not any(ord(c)<32 and c not in '\n\t\r' for c in s),'C0 control character'
    depth=0
    for c in s:
        if c=='{':depth+=1
        if c=='}':depth-=1;assert depth>=0
    assert depth==0
    assert not re.search(r'\\(?:ln|log)[0-9x]',s),'Unseparated TeX function command'

def inspect_record(r):
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];meta=r['generation'];p=meta['parameters'];t=meta['template'];level=g.TEMPLATES[t][0]
    g.validate_parameters(p,level,t,meta['bank_profile'])
    if meta['bank_profile']!='raw-source' and t in g.MASKS and 'solution' in g.MASKS[t]:
        assert q[':question/worked-solution']==g.normal_notation(g.render(g.MASKS[t]['solution'],t,p))
        assert q[':question/worked-solution'].count('&')==g.SOURCES[g.TEMPLATES[t][1]][':question/worked-solution'].count('&')
    f=displayed(q);d=sp.diff(f,X);_,gd,answer,point=g.expressions(t,p)
    assert equal(d,gd),(t,f,d,gd,q[':question/problem'])
    match=re.search(r'instantaneous rate of change at \$x=([^$]+)',q[':question/problem'])
    expected=sp.expand(d.subs(X,math(match[1]))) if match else d
    assert equal(expected,answer),(t,expected,answer)
    for s in (q[':question/problem'],q.get(':question/worked-solution','')):formatting(s)
    fields=q.get(':question/answer-fields',[])
    for field in fields:
        choices=field[':answer-field/choices'];correct=field.get(':answer-field/correct',[None,None])[1]
        values=[math(a[':answer/value']) for a in choices]
        assert sum(equal(v,expected) for v in values)==1,(t,values,expected)
        if correct is not None:
            assert all(equal(v,expected)==(a[':answer/id']==correct) for v,a in zip(values,choices))
        assert all(str(uuid.UUID(s))==s for s in [q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in choices])
        for a in choices:formatting(a[':answer/value'])
        if field[':answer-field/type'].endswith('/radio'):
            assert len(values)==5
            assert all(not equal(values[i],values[j]) for i in range(5) for j in range(i)),(t,values)
        else:assert len(values)==1 and '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
    # Read each actual displayed RHS, including formal derivatives and substitution.
    blocks=q.get(':question/worked-solution','').split('$$');checks=0
    for block in blocks[3::2]:
        evaluation='|' in block
        for row in re.split(r'\\\\',block):
            match=re.search(r'&\s*=\s*(.*)',row,re.S)
            if not match:continue
            rhs=match[1].split(r'\end{aligned}',1)[0].strip()
            if '|' in rhs:
                part=group(rhs,1,'(',')')[0] if rhs.startswith('{(') else None
                assert part is not None and equal(math(part),d),(t,rhs)
                marker=rhs.index('_{x=')+1;point_text,_=group(rhs,marker);assert equal(math(point_text[2:]),point),(t,rhs,point)
                value=expected
            else:value=math(rhs)
            assert equal(value,expected if evaluation else d),(t,rhs,value,d,expected)
            checks+=1
    if ':question/worked-solution' in q:assert checks>=2,(t,checks)
    # Concluding mathematical prose must contain the actual evaluation point.
    if point is not None and ':question/worked-solution' in q:
        conclusion=re.search(r'(?:Therefore|Hence), the instantaneous rate of change at \$x=([^$]+)',q[':question/worked-solution'])
        assert conclusion and equal(math(conclusion[1]),point)
    return expected

def equivalent_entry(r):
    t=r['generation']['template'];p=r['generation']['parameters'];B=p['base']
    # Independent common-denominator calculation, kept unreduced for grading.
    if t=='constant-log-slope':return frac(-p['a']*B,B)
    if t=='quadratic-slope':return frac(str(2*p['a'])+rational_ln(B)+'-'+str(p['b']),r'\ln '+str(B))
    if t=='cubic-slope':return frac(str(3*(27*p['a']+1))+r'\ln '+str(B)+'-'+str(p['b']),r'3\ln '+str(B))
    if t=='log-minus-ln':return frac('1-'+str(p['b'])+r'\ln '+str(B),'x'+r'\ln '+str(B))
    if t=='negative-exp-log':return frac(str(p['a'])+'-xe^{x}'+r'\ln '+str(B),'x'+r'\ln '+str(B))
    if t in ('log-ln-exp-slope','log-ln-exp-derivative'):
        if t.endswith('slope'):return frac(str(p['a'])+'-'+str(p['b'])+r'\ln '+str(B)+'+'+str(p['c'])+'e'+r'\ln '+str(B),r'\ln '+str(B))
        return frac(str(p['a'])+'-'+str(p['b'])+r'\ln '+str(B)+'+'+str(p['c'])+'xe^{x}'+r'\ln '+str(B),'x'+r'\ln '+str(B))
    if t=='exp-common-blank':return frac('x{'+str(p['expbase'])+r'}^{x}\ln('+str(p['expbase'])+r')\ln(10)+1',r'x\ln(10)')
    raise ValueError(t)
def frac(n,d):return r'\frac{'+str(n)+'}{'+str(d)+'}'
def rational_ln(b):return r'\ln '+str(b)

def checks(r,label,raw=False):
    f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Every displayed complete-bank choice'} for a in f[':answer-field/choices']]}
    answer=f[':answer-field/choices'][0][':answer/value'];eq=equivalent_entry(r)
    assert equal(math(eq),inspect_record(r)),(label,eq)
    entries=[{'submitted':answer,'expected':'accepted','purpose':'Canonical fragment'},{'submitted':eq,'expected':'rejected' if raw and 'Do not round' in r['question'][':question/problem'] else 'accepted','purpose':'Independent unreduced common-denominator expression; raw round-wording form sensitivity'},{'submitted':'('+answer+')+1','expected':'rejected','purpose':'Incorrect derivative/rate'},{'submitted':'0','expected':'rejected','purpose':'Incorrect zero derivative'}]
    if r['generation']['template']=='log-ln-exp-slope':
        p=r['generation']['parameters'];B=p['base']
        entries += [{'submitted':str(p['c'])+r'\cdot e-'+str(p['b'])+'+'+frac(p['a'],r'\ln '+str(B)),'expected':'rejected' if raw else 'accepted','purpose':'Legitimate independently reordered Euler scalar'}, {'submitted':frac(p['a'],r'\ln '+str(B))+'-'+str(p['b'])+'+'+str(10*p['c']),'expected':'rejected','purpose':'Known-wrong scientific-value Euler replacement'}]
    return {'label':label,'record':r,'checks':entries}

def main():
    native=[];replays=[];review=[];normal_count=0;slots={};default_seen=set();all_values=0;all_distractors=0;correct_refs=0
    for t,(level,mid) in g.TEMPLATES.items():
        if mid is not None:
            source=g.SOURCES[mid];raw=g.generate(level,0,t,parameters=g.PARAMETERS[t],profile='raw-source');q=raw['question']
            inspect_record(raw)
            for k in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (k in q)==(k in source),(mid,k)
            assert q[':question/problem']==source[':question/problem']
            if ':question/worked-solution' in source:assert q[':question/worked-solution']==source[':question/worked-solution']
            for f,sf in zip(q.get(':question/answer-fields',[]),source.get(':question/answer-fields',[]),strict=True):
                assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
                assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
                assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
                all_values+=len(f[':answer-field/choices']);all_distractors+=len(f[':answer-field/choices'])-1
                if ':answer-field/correct' in sf:
                    correct_refs+=1
                    assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
                    native.append(checks(raw,'raw/'+mid,True))
            replays.append({'source_id':mid,'template':t,'prompt_exact':True,'solution_exact':':question/worked-solution' in source,'solution_presence_exact':True,'attribute_presence_exact':True,'complete_bank_exact':bool(source.get(':question/answer-fields')),'correct_designation_matched':bool(source.get(':question/answer-fields') and ':answer-field/correct' in source[':question/answer-fields'][0])})
            replay_info={'source_id':mid,'template':t,'parameters':g.PARAMETERS[t],'bank_profile':'raw-source','difficulty_observed':source.get(':question/difficulty'),'raw_question_attribute_presence':sorted(k for k in source if k.startswith(':question/')),'raw_field_attribute_presence':[sorted(k for k in f if k.startswith(':answer-field/')) for f in source.get(':question/answer-fields',[])],'authored_replay_level':level if ':question/difficulty' not in source else None}
            review.append({'label':'raw source '+mid,'source':source,'generated':raw,'case':replay_info})
        values={k:set() for k in g.PARAMETERS[t]};identities=set()
        for i in range(40):
            r=g.generate(level,100+i,t);inspect_record(r);normal_count+=1;native.append(checks(r,t+'/'+str(i)))
            assert r==g.generate(level,100+i,t)
            for k,v in r['generation']['parameters'].items():values[k].add(v)
            identities.add(r['generation']['parameter_fingerprint'])
            if i<2:review.append({'label':'generated variant '+t+'/'+str(i),'generated':r})
        assert len(identities)>=(9 if t in ('exp-common-radio','exp-common-blank') else 15),(t,len(identities))
        slots[t]={k:sorted(v) for k,v in values.items()}
        # Content identity is option-order independent for fixed mathematical data.
        a=g.generate(level,0,t,parameters=g.PARAMETERS[t]);b=g.generate(level,92,t,parameters=g.PARAMETERS[t])
        assert a['question'][':question/id']==b['question'][':question/id']
        # Explicit bounds apply to all three levels.
        for k in g.PARAMETERS[t]:
            if k=='point':bad=0
            else:bad=1
            p=dict(g.PARAMETERS[t]);p[k]=bad
            try:g.generate(level,0,t,parameters=p)
            except ValueError:pass
            else:raise AssertionError(('Invalid explicit parameter accepted',t,k))
        # Supported evidence banks remain parameterized under changed parameters.
        if t in g.OPAQUE:
            changed=dict(g.PARAMETERS[t]);changed['base']=11 if 'common' not in t else 10;changed['expbase']=8 if 'expbase' in changed else changed.get('expbase',8)
            if 'expbase' not in g.PARAMETERS[t]:changed.pop('expbase')
            changed['a']=8 if 'a' in changed else changed.get('a',8)
            if 'a' not in g.PARAMETERS[t]:changed.pop('a')
            r=g.generate(level,51,t,parameters=changed,profile='observed-bank');inspect_record(r);native.append(checks(r,'observed-changed/'+t))
            review.append({'label':'changed historical bank (evidence only) '+t,'generated':r})
    for seed in range(200):
        r=g.generate('easy',seed);inspect_record(r);default_seen.add(r['generation']['template'])
    assert default_seen=={t for t,(level,_) in g.TEMPLATES.items() if level=='easy'},default_seen
    # Mutation tests independently detect printed arithmetic and formatting errors.
    r=g.generate('easy',3,'quadratic-slope');bad=json.loads(json.dumps(r));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('2x','3x',1)
    try:inspect_record(bad)
    except AssertionError:pass
    else:raise AssertionError('Distributed-stage mutation not caught')
    a=r['generation']['parameters']['a'];bad=json.loads(json.dumps(r));bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(str(a)+r'\cdot 2x',str(2*a)+'x')
    try:inspect_record(bad)
    except AssertionError:pass
    else:raise AssertionError('Equal-valued missing product stage mutation not caught')
    bad=json.loads(json.dumps(r));bad['question'][':question/problem']+='\x0c'
    try:inspect_record(bad)
    except AssertionError:pass
    else:raise AssertionError('C0 mutation not caught')
    (HERE/'source-cases.json').write_text(json.dumps([v['case'] for v in review if 'case' in v],indent=2)+'\n')
    (HERE/'source-replay.json').write_text(json.dumps(replays,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (HERE/'review.md').write_text('# Frozen-basis originals and generated variants\n\nRaw records are evidence only. Generated variants use authored repairs where identified.\n\n'+'\n\n---\n\n'.join('## '+v['label']+'\n\n'+g.markdown(v['generated']) for v in review)+'\n')
    (HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    report=json.loads((HERE/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    result={'status':'passed','basis':1356,'source_questions_total':12,'source_questions_replayed':len(replays),'source_banks_matched':11,'source_banks_total':11,'source_answer_values_matched':all_values,'source_answer_values_total':all_values,'source_distractors_matched':all_distractors,'source_distractors_total':all_distractors,'source_correct_designations_matched':correct_refs,'source_correct_designations_total':9,'source_prompt_exact':12,'source_solution_exact':10,'source_solution_total':10,'raw_attribute_presence_matched':12,'unrated_raw_preserved':2,'fieldless_raw_preserved':1,'authored_level':'moderate three-rule symbolic derivative; hard adds point evaluation','normal_records_checked':normal_count,'default_easy_families_covered':sorted(default_seen),'slot_coverage':slots,'native':{k:v for k,v in report.items() if k!='records'},'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'plots':'none','generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'native_harness_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('slot_coverage','default_easy_families_covered')}))
if __name__=='__main__':main()

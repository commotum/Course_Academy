#!/usr/bin/env python3
"""Independent displayed-math validation and native learner-engine fixtures."""
import importlib.util, json, re, hashlib, subprocess, sys
from functools import lru_cache
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ivp',HERE.with_suffix('.py')); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=g.x; Y=sp.Symbol('y'); D=sp.Symbol('D'); C=g.C

def clean(s):
    return s.replace('\\\\frac','\\frac').replace('\\\\operatorname','\\operatorname').replace('\\u2061','').replace('⁡','').replace('\u2061','')

def group(s,i):
    while i<len(s) and s[i].isspace():i+=1
    assert s[i]=='{',(s,i)
    start=i+1; depth=1;i+=1
    while depth:
        if s[i]=='{':depth+=1
        if s[i]=='}':depth-=1
        i+=1
    return s[start:i-1],i

def parse(s):
    s=clean(s).strip().rstrip('.').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','')
    s=re.sub(r'\\operatorname\{(sin|cos|ln)\}',lambda m:'\\'+m.group(1),s)
    s=re.sub(r'\\ln\{x\}\^\{(\d+)\}',r'\\ln(x^{\1})',s)
    s=s.replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac')
    while r'\frac' in s:
        i=s.index(r'\frac'); a,j=group(s,i+5);b,k=group(s,j);s=s[:i]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+s[k:]
    for a,b in [(r'\cdot','*'),(r'\pi','pi'),(r'\sin',' sin '),(r'\cos',' cos '),(r'\ln',' log ')]:s=s.replace(a,b)
    s=s.replace('{','(').replace('}',')').replace('^','**')
    return parse_expr(s,local_dict={'x':x,'y':Y,'D':D,'C':C,'e':sp.E,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'log':sp.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor),evaluate=True)

@lru_cache(maxsize=20000)
def equal(a,b):
    delta=sp.expand(a-b)
    if delta==0:return True
    if delta.is_zero is False:return False
    return sp.simplify(delta)==0

def displayed_problem(rec):
    prompt=clean(rec['question'][':question/problem'])
    math=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$',prompt,re.S)
    ode=next((a or b) for a,b in math if 'dy' in a+b or r'\text{d}y' in a+b)
    ode=re.sub(r'\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}|\\frac\{dy\}\{dx\}', 'D',ode)
    ode=ode.replace(r'\cdot','*').replace(r'\,','')
    initial=re.search(r'y\((.*?)\)\s*=\s*(-?\d+)',ode);assert initial,ode
    t=parse(initial.group(1));h=sp.Integer(initial.group(2))
    equation=ode[:initial.start()].rstrip(' ,').replace(r'\quad','').replace('x>0','').rstrip(' ,')
    lhs,rhs=equation.split('=',1); L=parse(lhs);Q=parse(rhs)
    coefficient=sp.expand(L).coeff(D); P=sp.expand(L).coeff(Y)/coefficient; Q=Q/coefficient
    assert equal(L,coefficient*D+coefficient*P*Y)
    return P,Q,t,h

def formatting(s):
    assert s.count('$$')%2==0
    s=s.replace('$$',''); assert s.count('$')%2==0
    depth=0
    for c in s:
        if c=='{':depth+=1
        elif c=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert not re.search(r'(?<!\\)(?:\+\-|\-\-)',s)

def stage_expr(raw,general,particular,constant,initial=False):
    raw=clean(raw).strip().rstrip('.')
    raw=re.sub(r'\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}', 'D',raw)
    marker=r'\frac{\text{d}}{\text{d}x}'
    if raw.startswith(marker):
        inner=raw[len(marker):].strip()
        assert inner.startswith('(') and inner.endswith(')'),raw
        return sp.diff(parse(inner[1:-1]).subs(Y,general),x)
    if raw=='I(x)': return None
    if raw.startswith('y(') and raw.endswith(')'):
        return general.subs(x,parse(raw[2:-1])).subs(C,constant)
    val=parse(raw).subs(Y,general).subs(D,sp.diff(general,x))
    if initial:val=val.subs(C,constant)
    return val

def check_printed_stages(solution,general,particular,m):
    checked=0
    for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S):
        previous=None
        for row in re.split(r'\\\\',block):
            if '&' not in row:continue
            left,right=row.split('&',1);left=left.strip();right=right.strip().removeprefix('=').rstrip('.')
            if left:previous=left
            else:left=previous
            if not left or r'\int' in left+right or 'P(x)' in left+right or 'Q(x)' in left+right:continue
            if left=='C':assert equal(parse(right),m['c']);checked+=1;continue
            if left=='I(x)':
                assert equal(parse(right),m['I']);checked+=1;continue
            initial=left.startswith('y(') or not ('y' in left or r'\frac{\text{d}}' in left)
            a=stage_expr(left,general,particular,m['c'],initial)
            b=stage_expr(right,general,particular,m['c'],initial)
            u=sp.Symbol('u'); b=b.subs(u,sp.integrate(m['P'],x))
            if left=='y' and not b.has(C):a=particular
            assert equal(a,b),(left,right,a,b)
            checked+=1
    return checked

def check_record(rec,allow_ambiguous=False):
    assert set(rec['knowledge_point'])=={'db_id','id','title'}
    q=rec['question'];gen=rec['generation'];fields=q[':question/answer-fields']
    formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
    P,Q,t,h=displayed_problem(rec)
    solutions=[]
    for i,f in enumerate(fields):
        assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
        choices=f[':answer-field/choices'];right=f[':answer-field/correct'][1]
        ids=[a[':answer/id'] for a in choices];assert len(ids)==len(set(ids))
        assert right in ids
        exprs=[parse(a[':answer/value']) for a in choices]
        correct=exprs[ids.index(right)]; solutions.append(correct)
        mathematically_correct=[]
        for z in exprs:
            ok=(equal(sp.diff(z,x),P*z) and z!=0) if i==0 else equal(sp.diff(z,x)+P*z,Q) and equal(z.subs(x,t),h)
            mathematically_correct.append(ok)
        assert mathematically_correct[ids.index(right)]
        assert sum(mathematically_correct)==1 or allow_ambiguous
        if not allow_ambiguous:
            assert len(set(map(sp.srepr,map(sp.simplify,exprs))))==len(exprs)
            for j,z in enumerate(exprs):
                for z2 in exprs[:j]:
                    assert not equal(z,z2)
                    if i==0:assert (ratio:=sp.simplify(z/z2)).has(x) or ratio==0
    # Verify displayed final solution and every printed algebraic y/C row.
    solution=q[':question/worked-solution']; particular=solutions[1]
    last=re.findall(r'\$\$(.*?)\$\$',solution,re.S)[-1]
    if r'\begin{aligned}' not in last:
        assert equal(parse(last.strip().removeprefix('y=').rstrip('.')),particular)
    f=gen['template']; family=g.TEMPLATES[f][1]; m=g.model(family,gen['parameters'])
    general=(sp.integrate(m['I']*Q,x)+C)/m['I']
    assert equal(sp.diff(general,x)+P*general,Q)
    # Read every explicit y=... general/particular row back from the actual text.
    rows=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
    checked=0
    for block in rows:
        for row in re.split(r'\\\\',block):
            if '&' not in row:continue
            left,right=row.split('&',1);left=left.strip();right=right.strip().removeprefix('=').rstrip('.')
            if left=='y' and not (r'\int' in right):
                val=parse(right); assert equal(val,general if val.has(C) else particular),(left,right,val,general);checked+=1
            if left=='C':assert equal(parse(right),m['c']);checked+=1
            # Product/general-solution arithmetic rows, actual printed expressions.
            if left.startswith('y') and '(' not in left and '\\frac' not in left and left!='y' and '\\text' not in left and '\\int' not in right:
                lhs=parse(left).subs(Y,general);rhs=parse(right)
                if rhs.has(sp.Symbol('u')):continue
                assert equal(lhs,rhs),(left,right,lhs,rhs);checked+=1
    return checked+check_printed_stages(solution,general,particular,m)

def prose(s):return re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?\$', '<MATH>',s,flags=re.S)

def main():
    reviews=[];cases=[];fixtures=[];counts={'questions':0,'options':0,'correct_refs':0,'available_correct_refs':0,'missing_correct_refs_derived':0,'complete_banks':0,'unambiguous_banks':0,'raw_exact_prompts':0,'raw_exact_solutions':0,'available_solutions':0,'presentation_normalized_solutions':0,'mathematical_source_solution_repairs':0,'solution_prose_sequence':0}; stages=0;matches=[]
    for qid,(level,family,p,_,_) in g.OBS.items():
        rec=g.generate(level,template=qid,parameters=p,profile='observed'); source=g.QUESTIONS[qid];amb=rec['generation']['source_ambiguous_bank']
        stages+=check_record(rec,amb);counts['questions']+=1;counts['raw_exact_prompts']+=rec['question'][':question/problem']==source[':question/problem']
        if ':question/worked-solution' in source:
            counts['available_solutions']+=1;counts['raw_exact_solutions']+=rec['question'][':question/worked-solution']==source[':question/worked-solution']
            assert prose(rec['question'][':question/worked-solution'])==prose(source[':question/worked-solution'])
            assert rec['question'][':question/worked-solution'].count(' & =')==source[':question/worked-solution'].count(' & =')
            counts['solution_prose_sequence']+=1
            counts['presentation_normalized_solutions']+=rec['question'][':question/worked-solution']!=source[':question/worked-solution']
        for original in source[':question/answer-fields']:
            f=next(f for f in rec['question'][':question/answer-fields'] if f[':answer-field/key']==original[':answer-field/key'])
            old=[parse(a[':answer/value']) for a in original[':answer-field/choices']];new=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
            assert len(old)==len(new);unused=list(new)
            for a in old:
                found=next((i for i,b in enumerate(unused) if equal(a,b)),None);assert found is not None,(qid,a,new)
                unused.pop(found);counts['options']+=1
            counts['complete_banks']+=1;counts['unambiguous_banks']+=not (amb and f[':answer-field/key']==('field-1' if qid=='q-335830' else 'field-2'))
            if ':answer-field/correct' in original:
                counts['available_correct_refs']+=1
                val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
                assert equal(parse(val),parse(original[':answer-field/correct'][':answer/value']));counts['correct_refs']+=1
            else:counts['missing_correct_refs_derived']+=1
        cases.append({'source_id':qid,'template':qid,'difficulty':level,'parameters':p,'bank_profile':'observed','ambiguous_original_bank':amb,'missing_correct_refs':':answer-field/correct' not in source[':question/answer-fields'][0]})
        reviews.append({'label':'Original replay '+qid,'record':rec,'source_id':qid})
        # Changed parameter variants for every observed presentation/bank.
        pv=dict(p)
        if family=='cosine':pv['k']=2
        else:pv['h']=p['h']+1 if p['h']+1 not in (0,1,2,6) else p['h']-1
        for prof in ('observed','authored'):
            try: v=g.generate(level,3,template=qid,parameters=pv,profile=prof)
            except ValueError:
                v=g.generate(level,5,template=qid,profile=prof)
            stages+=check_record(v,prof=='observed' and amb); reviews.append({'label':'Generated '+qid+' / '+prof,'record':v})
    source_boundary_passes=0; source_collision_rejections=0
    for template,(level,family,p,_,_) in g.OBS.items():
        for value in (-8,0,8):
            pv=dict(p)
            if family=='cosine':pv['k']=1 if value<0 else 5;pv['h']=0
            else:pv['h']=value
            for profile in ('observed','authored'):
                try:rec=g.generate(level,19,template=template,parameters=pv,profile=profile)
                except ValueError:source_collision_rejections+=1;continue
                stages+=check_record(rec,rec['generation']['source_ambiguous_bank']);source_boundary_passes+=1
    # All supported authored templates and both hard branches; vary seeded instances.
    taskcounts={};samplecounts={};identities={}
    for template,(level,family) in g.AUTH.items():
        print('Checking authored family',template,flush=True)
        ids=set();tasks=set()
        for seed in range(12):
            rec=g.generate(level,seed,template=template);stages+=check_record(rec);ids.add(rec['question'][':question/id']);tasks.add(rec['generation']['mathematical_fingerprint'])
            replay=g.generate(level,seed+200,template=template,parameters=rec['generation']['parameters'])
            assert replay['question'][':question/id']==rec['question'][':question/id'];assert replay['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
            if seed<2: reviews.append({'label':'Authored '+template+' seed '+str(seed),'record':rec})
            if seed<5:fixtures.append({'label':template+' seed '+str(seed),'record':rec,'checks':native_checks(rec)})
        samplecounts[template]=12;taskcounts[template]=len(tasks);identities[template]=len(ids)
        assert len(tasks)>=8,(template,tasks)
    for row in reviews:
        fixtures.append({'label':row['label'],'record':row['record'],'checks':native_checks(row['record'])})
    # Explicit bounds and collision guard failures, all must be rejected.
    failures=0
    for template,(level,family) in g.AUTH.items():
        base=g.generate(level,11,template=template)['generation']['parameters']
        for bad in (dict(base,h=10),dict(base,**{next(k for k in base if k!='h'):0})):
            try:g.generate(level,parameters=bad,template=template)
            except ValueError:failures+=1
            else:raise AssertionError(('invalid accepted',template,bad))
    for template in g.AUTH:
        level=g.AUTH[template][0]; p=g.generate(level,17,template=template)['generation']['parameters'];p['h']=0
        try:g.generate(level,parameters=p,template=template)
        except ValueError:failures+=1
        else:raise AssertionError('authored zero IC guard')
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
    report='# Source originals and generated variants\n\nRaw captures remain in source.json; original replay choices are presentation-normalized. Two observed banks are ambiguous evidence; normal authored banks are collision-free.\n\n'
    for qid in g.OBS:
        q=g.QUESTIONS[qid];report+='## Raw original '+qid+'\n\n'+q[':question/problem']+'\n\n'
        for field in q[':question/answer-fields']:
            report+=field[':answer-field/key']+':\n'+''.join('- `'+a[':answer/value']+'`\n' for a in field[':answer-field/choices'])+'\n'
        report+=q.get(':question/worked-solution','No captured worked solution; replay uses a separately authored derivation.')+'\n\n'
    for row in reviews:report+='## '+row['label']+'\n\n'+g.markdown(row['record'])+'\n\n'
    (HERE/'review.md').write_text(report)
    (HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
    engine=HERE.parent.parent/'runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True)
    native=json.loads((HERE/'engine.json').read_text())
    out={'status':'passed_with_documented_source_anomalies','source_fidelity':counts,'authored_sample_counts':samplecounts,'distinct_mathematical_tasks':taskcounts,'distinct_content_ids':identities,'displayed_algebra_rows_checked':stages,'source_boundary_instances_checked':source_boundary_passes,'source_boundary_collision_rejections':source_collision_rejections,'invalid_explicit_instances_rejected':failures,'native_grading':{k:v for k,v in native.items() if k!='records'},'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'grader_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'unresolved_source_findings':['q-335811 and q-335812 duplicate mathematically correct options: raw evidence profiles only','q-334916 current correct references and solution absent; two field values independently derived, no matched designation claim','q-335830 wrong IF choices -2x and 2x are redundant up to scalar; source bank evidence-only; some observed wrong-operation intent unresolved; observed profiles excluded from default bank selection'],'database_writes':0}
    (HERE/'validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

def native_checks(rec):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native designation check; evidence-only source has documented ambiguous or redundant choices' if rec['generation']['source_ambiguous_bank'] else 'owned correct/wrong choice'})
    return checks
if __name__=='__main__':main()

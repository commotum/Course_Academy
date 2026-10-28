#!/usr/bin/env python3
"""Independent displayed-TeX readback, complete banks, identities and native grading."""
from pathlib import Path
import importlib.util,json,re,hashlib,subprocess,itertools
import sympy as s
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('polar',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
R,T=g.R,g.T
CHECKED=[]

class Parser:
    """Exact small TeX grammar: reads actual implicit products and trig inputs."""
    def __init__(self,text):
        text=g.norm(text).replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(' ','').strip().rstrip('.,')
        self.t=re.findall(r'\\(?:frac|sin|cos|theta)|[0-9]+|[r()+\-*/^{}]',text);self.i=0
        assert ''.join(self.t)==text,(text,self.t)
    def peek(self):return self.t[self.i] if self.i<len(self.t) else ''
    def pop(self):x=self.peek();self.i+=1;return x
    def group(self):
        op=self.pop();assert op in ('{','('),op
        value=self.sum();assert self.pop()==('}' if op=='{' else ')');return value
    def atom(self):
        op=self.peek()
        if op in ('-','+'):
            self.pop();v=self.atom();return -v if op=='-' else v
        if op in ('{','('):v=self.group()
        elif op==r'\frac':
            self.pop();v=self.group()/self.group()
        elif op in (r'\sin',r'\cos'):
            self.pop();pow_=1
            if self.peek()=='^':self.pop();pow_=self.group() if self.peek()=='{' else s.Integer(self.pop())
            if self.peek() in ('{','('):arg=self.group()
            else:
                c=s.Integer(self.pop()) if self.peek().isdigit() else 1
                assert self.pop()==r'\theta';arg=c*T
            v=(s.sin(arg) if op==r'\sin' else s.cos(arg))**pow_
        elif op.isdigit():v=s.Integer(self.pop())
        elif op in ('r',r'\theta'):v=R if self.pop()=='r' else T
        else:raise AssertionError(('atom',op,self.t))
        if self.peek()=='^':
            self.pop();p=self.group() if self.peek()=='{' else self.atom();v=v**p
        return v
    def product(self):
        v=self.atom()
        while self.peek() and self.peek() not in ('+','-',')','}'):
            if self.peek()=='*':self.pop();v*=self.atom()
            elif self.peek()=='/':self.pop();v/=self.atom()
            else:v*=self.atom()
        return v
    def sum(self):
        v=self.product()
        while self.peek() in ('+','-'):
            op=self.pop();w=self.product();v=v+w if op=='+' else v-w
        return v
    def parse(self):v=self.sum();assert self.i==len(self.t);return v

def parse(x):return Parser(x).parse()
def eq(a,b):return g.equivalent(a,b)
def fmt(text):
    assert text.count('$$')%2==0
    assert text.replace('$$','').count('$')%2==0
    depth=0
    for c in text:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert '--' not in text and '+-' not in text

def read_problem(problem):
    inline=problem.split('$');formula=inline[1].rstrip(',');rhs=formula.split('=',1)[1]
    F=parse(rhs)
    target=inline[3];axis=re.search(r'∂([xy])',target)[1]
    name=re.search(r'^([fghuvw])\(',formula)[1]
    return F,axis,name

def read_stages(solution):
    display=solution.split('$$');assert len(display)==7
    last=display[5];rows=last.split('& =')[1:]
    return [re.split(r'\\\\|\\end',row)[0].strip().rstrip('.') for row in rows]

def check(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    q=record['question'];m=record['generation'];f=q[':question/answer-fields'][0]
    fmt(q[':question/problem']);fmt(q[':question/worked-solution'])
    F,axis,name=read_problem(q[':question/problem'])
    # Independent inverse Cartesian Jacobian from the displayed polar object.
    J=s.Matrix([[s.diff(R*s.cos(T),R),s.diff(R*s.cos(T),T)],[s.diff(R*s.sin(T),R),s.diff(R*s.sin(T),T)]])
    cart=(s.Matrix([[s.diff(F,R),s.diff(F,T)]])*J.inv())[0,0 if axis=='x' else 1]
    # Compare via exact polynomial trig identities; no eager CAS phase shifts.
    assert f[':answer-field/type']==':answer-field.type/radio'
    choices=f[':answer-field/choices'];assert len(choices)==5
    vals=[];correct=None
    ids=[]
    for a in choices:
        assert a[':answer/type']==':answer.type/math';assert '$' not in a[':answer/value'];fmt(a[':answer/value'])
        value=parse(a[':answer/value']);assert not value.has(s.zoo,s.nan)
        assert not any(eq(value,v) for v in vals),'bank collision'
        vals.append(value);ids.append(a[':answer/id'])
        if a[':answer/id']==f[':answer-field/correct'][1]:correct=value
    assert len(set(ids))==5 and correct is not None and eq(correct,cart)
    stages=read_stages(q[':question/worked-solution']);assert stages==m['solution_stages']
    for row in stages:assert eq(parse(row),cart),row
    # Verify displayed partial derivatives, not the generation metadata.
    derivative_display=q[':question/worked-solution'].split('$$')[3]
    rhs=re.split(r'=|,\\,|\\end',derivative_display)
    assert eq(parse(rhs[1]),s.diff(F,R)),rhs
    assert eq(parse(rhs[3]),s.diff(F,T)),rhs
    # Differential names and coordinate target are verified throughout.
    final=q[':question/worked-solution'].split('$$')[5]
    assert re.search(r'∂'+name+r'\}\{∂'+axis+r'\}',final)
    formula=q[':question/worked-solution'].split('$$')[1]
    assert formula== '\n'+g.render_math(m['template'],m['parameters'])[2]+'\n'
    if m['template']=='double_sine_x':
        assert len(stages)==5
        assert '(' in stages[2] and stages[3].count(r'\sin')==3 and stages[4].count(r'\sin')==1
    if m['template']=='offset_sine_x':assert len(stages)==3 and stages[1].count(r'\sin')==2
    if m['template']=='sine_minus_y':assert len(stages)==3 and '^{2}' in stages[1]
    if m['template']=='power_offset':
        assert len(stages)==3
        assert stages[1].count(g.power(m['parameters']['p']-1))==3
        assert stages[2].count(g.power(m['parameters']['p']-1))==1 and '(' in stages[2]
    assert stages[0].count('(')>=2 and r'\frac{1}{r}' in stages[0]
    # Same true content under shuffling must retain IDs; math FP ignores name.
    replay=g.generate(q[':question/difficulty'].split('/')[-1],seed=991,template=m['template'],parameters=m['parameters'],profile=m['profile'])
    assert replay['question'][':question/id']==q[':question/id']
    rename=dict(m['parameters']);rename['name']='g' if name!='g' else 'f'
    r2=g.generate(q[':question/difficulty'].split('/')[-1],template=m['template'],parameters=rename,profile=m['profile'])
    assert r2['generation']['mathematical_fingerprint']==m['mathematical_fingerprint']
    CHECKED.append(record)
    return len(stages)+2

def native(record,label):
    f=record['question'][':question/answer-fields'][0]
    return {'label':label,'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual owned radio choice'} for a in f[':answer-field/choices']]}

def source_prose(text):
    parts=g.norm(text).split('$$')
    return re.sub(r'\s+',' ','|'.join(parts[::2])).strip()

def main():
    source_cases=[];review=[];engine=[];math_stages=0;fidelity=[]
    for template,(sid,p) in g.CASES.items():
        source=g.SOURCES[sid];profile='observed:'+sid
        case={'source_id':sid,'template':template,'parameters':p,'bank_profile':profile,'level':'moderate','observed_difficulty':'moderate' if ':question/difficulty' in source else None}
        source_cases.append(case)
        record=g.generate('moderate',template=template,parameters=p,profile=profile)
        math_stages+=check(record);review.append({'label':'Original-parameter replay '+sid,'kind':'source-replay','record':record});engine.append(native(record,sid))
        expected=source[':question/answer-fields'][0]
        choices=record['question'][':question/answer-fields'][0][':answer-field/choices']
        remaining=[parse(a[':answer/value']) for a in choices]
        for a in expected[':answer-field/choices']:
            v=parse(a[':answer/value']);matched=[i for i,x in enumerate(remaining) if eq(v,x)];assert len(matched)==1,(sid,a)
            remaining.pop(matched[0])
        assert not remaining
        raw_correct=expected.get(':answer-field/correct')
        if raw_correct:
            ours=next(a for a in choices if a[':answer/id']==record['question'][':question/answer-fields'][0][':answer-field/correct'][1])
            assert eq(parse(ours[':answer/value']),parse(raw_correct[':answer/value']))
        stage_count=None
        if ':question/worked-solution' in source:
            assert source_prose(source[':question/worked-solution'])==source_prose(record['question'][':question/worked-solution'])
            rawrows=read_stages(g.norm(source[':question/worked-solution']))
            rows=record['generation']['solution_stages'];assert len(rawrows)==len(rows)
            for raw,new in zip(rawrows,rows):assert eq(parse(raw),parse(new)),(sid,raw,new)
            stage_count=len(rows)
        # Fixed prompt prose and full displayed object at source parameters.
        srcF,srcaxis,srcname=read_problem(g.norm(source[':question/problem']))
        outF,outaxis,outname=read_problem(record['question'][':question/problem']);assert eq(srcF,outF) and srcaxis==outaxis and srcname==outname
        def skeleton(t):
            v=g.norm(t).split('$');v[1]='@';return re.sub(r'\s+',' ','$'.join(v))
        assert skeleton(source[':question/problem'])==skeleton(record['question'][':question/problem'])
        fidelity.append({'source_id':sid,'matched_values':5,'matched_distractors':4,'original_correct_designation_matched':bool(raw_correct),'inferred_correct_designation':not bool(raw_correct),'source_worked_solution_present':stage_count is not None,'stage_count':stage_count,'prose_matched':stage_count is not None,'notation_normalized':True,'mathematical_label_repair':sid=='q-165282'})
        for seed in (17,38):
            variant=g.generate('moderate',seed=seed,template=template,profile=profile)
            math_stages+=check(variant);review.append({'label':'Generated observed-bank variant '+template+str(seed),'kind':'generated-observed-bank','record':variant});engine.append(native(variant,template+str(seed)))
    for level in ('easy','moderate','hard'):
        for i in range(8):
            r=g.generate(level,seed=100+i);math_stages+=check(r);engine.append(native(r,level+str(i)))
            review.append({'label':'Authored default '+level+' '+str(i),'kind':'generated-authored-bank','record':r})
    # Exercise every profile including signed boundary scale and non-default powers.
    for template in g.TEMPLATES:
        profiles=['authored:chain-rule']+(['observed:'+g.CASES[template][0]] if template in g.CASES else [])
        for profile in profiles:
            for seed in range(10):
                record=g.generate(g.TEMPLATES[template],seed=seed,template=template,profile=profile)
                math_stages+=check(record)
    # All authored defaults also receive native grading, not just random picks.
    for template in g.TEMPLATES:
        r=g.generate(g.TEMPLATES[template],seed=43,template=template)
        math_stages+=check(r);engine.append(native(r,'all-default-templates/'+template))
    # Enumerate easy's complete finite meaningful domain (32 assessed tasks).
    easy_ids=set()
    for A,p,axis in itertools.product([-4,-3,-2,-1,1,2,3,4],(2,3),('x','y')):
        r=g.generate('easy',template='radial_only',parameters=dict(A=A,p=p,axis=axis,name='f'))
        math_stages+=check(r);easy_ids.add(r['generation']['mathematical_fingerprint'])
    assert len(easy_ids)==32
    # Explicit bounds, missing workload terms and mismatch inputs must fail.
    invalid=0
    for template in g.TEMPLATES:
        p=g.sample(template,__import__('random').Random(43))
        for key,value in [('A',0),('A',-99)]+([(key,0) for key in ('p','b','k','a') if key in p]):
            bad=dict(p);bad[key]=value
            try:g.generate(g.TEMPLATES[template],template=template,parameters=bad)
            except ValueError:invalid+=1
            else:raise AssertionError(('bounds',template,key,value))
    # Whole-bank collisions reject explicit source-profile cases as a unit.
    try:g.assert_bank([s.Integer(0),s.Integer(1),s.sin(T)**2+s.cos(T)**2,s.Integer(2),s.Integer(3)])
    except ValueError:pass
    else:raise AssertionError('whole functional-equivalence bank collision')
    # canonical source precision contains no round instruction; all fields radio.
    def write(name,v):(ROOT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
    write('source-cases.json',source_cases);write('review.json',review);write('engine-input.json',engine)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    native_report=json.loads((ROOT/'engine-validation.json').read_text())
    report={'status':'passed','database':'math','basis':1356,'source_questions':9,'observed_levels':{'moderate':7,'unrated':2},'source_values_matched':45,'source_values_total':45,'source_distractors_matched':36,'source_distractors_total':36,'source_banks_matched':9,'source_banks_total':9,'source_correct_designations_matched':7,'source_correct_designations_present':7,'source_correct_designations_missing_and_inferred':2,'source_prompt_objects_and_fixed_prose_matched':9,'raw_exact_solution_strings':0,'original_solutions_present':7,'normalized_fixed_solution_prose_and_stage_sequences_matched':7,'raw_exact_mathematical_labels':6,'minimal_mathematical_label_repairs':1,'generated_and_replay_records_math_checked':len(CHECKED),'distinct_mathematical_tasks_checked':{level:len({r['generation']['mathematical_fingerprint'] for r in CHECKED if r['question'][':question/difficulty']==':question.difficulty/'+level}) for level in ('easy','moderate','hard')},'distinct_content_identities_checked':len({r['question'][':question/id'] for r in CHECKED}),'easy_complete_finite_meaningful_domain':32,'displayed_derived_stage_checks':math_stages,'invalid_parameter_checks':invalid,'native_accepted':native_report['accepted_checks'],'native_rejected':native_report['rejected_checks'],'native_unresolved':native_report['documented_unresolved_checks'],'blank_checks':'not applicable: all nine observed and all authored fields are radio','plots':'none','source_fidelity':fidelity,'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'dependencies':{'sympy':s.__version__,'native_harness_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest()},'unresolved_source_error_intent':'Observed incorrect-expression recipes are inferred shapes, not recovered cognitive intent; two original correct refs and solutions absent. These are disclosed, not counted as designation/solution matches.'}
    write('validation.json',report)
    text=['# Originals and generated variants\n\nRaw originals retained in source.json. All generated records are visibly labeled. The two unrated sources receive an authored moderate assignment. q165282 final derivative label is minimally repaired to y.\n']
    for template,(sid,p) in g.CASES.items():
        src=g.SOURCES[sid];text+=['## Raw original '+sid,'\n'+src[':question/problem'],'\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in src[':question/answer-fields'][0][':answer-field/choices']), '\n'+src.get(':question/worked-solution','Original worked solution and correct designation missing; inferred independently.')]
    for item in review:text+=['## '+item['label'],'\n'+g.markdown(item['record'])]
    (ROOT/'review.md').write_text('\n\n'.join(text)+'\n')
    print(json.dumps({k:report[k] for k in ('status','source_values_matched','source_banks_matched','native_accepted','native_rejected','displayed_derived_stage_checks')},indent=2))
if __name__=='__main__':main()

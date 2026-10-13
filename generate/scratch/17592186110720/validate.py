#!/usr/bin/env python3
"""Independent printed-math, whole-bank, source, identity and native QA."""
import hashlib
import importlib.util
import itertools
import math
import json
from fractions import Fraction
from pathlib import Path
import re
import subprocess
import sys
import uuid
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
raw=json.loads((ROOT/'generate/runs/current/sources/17592186110720.json').read_text())
source=raw['record'][':knowledge-point/questions']

def save(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def expr(text):
    text=text.strip().rstrip('.,').replace('&','')
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text)
    assert '\\' not in text, text
    return parse_expr(text,local_dict={v:sp.Symbol(v) for v in ('x','p','s','k','q','a','b')},
                      transformations=standard_transformations+(implicit_multiplication_application,))

def formatting(text):
    assert text.count('$')%2==0
    # No escaped-literal braces occur in these templates; every brace is a group.
    depth=0
    for ch in text:
        if ch=='{': depth+=1
        if ch=='}': depth-=1; assert depth>=0
    assert depth==0
    assert '+-' not in text and '--' not in text

def check(record):
    assert set(record)=={'knowledge_point','question','generation'}
    assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=record['question'];f=q[':question/answer-fields'][0]
    uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
    assert len(q[':question/answer-fields'])==1
    for text in (q[':question/problem'],q[':question/worked-solution']):formatting(text)
    if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/problem'],re.S)
    assert len(blocks)==1
    left,right=map(expr,blocks[0].split('='))
    x=sp.Symbol('x');symbols=(left.free_symbols|right.free_symbols)-{x}
    assert len(symbols)==1
    var=symbols.pop();poly=sp.Poly(left-right,x)
    # Same-KP requirement: no independent x-constant or higher-degree branch.
    assert poly.degree()==1 and poly.nth(0)==0
    actual=sp.solve(poly.nth(1),var)
    assert len(actual)==1
    correct=actual[0]
    values=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(set(values))==len(values) and all(v.is_Rational for v in values)
    designated=[i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]]
    assert len(designated)==1 and values[designated[0]]==correct
    assert sum(v==correct for v in values)==1
    assert len(values)==(1 if f[':answer-field/type'].endswith('/blank') else 5)
    opaque=record['generation']['profile'].startswith('observed_')
    assert record['generation']['evidence_only']==opaque and record['generation']['eligible_for_learning']==(not opaque)
    assert f[':answer-field/correct'][0]==':answer/id'
    for a in f[':answer-field/choices']:
        uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math'
        assert '$' not in a[':answer/value']
    # Read every mathematical stage from the fixed solution, independently of metadata.
    stages=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
    assert len(stages)==4 and stages[0]=='ax=bx'
    parts=stages[1].split(r',\,')
    assert len(parts)==2 and parts[0].startswith('a=') and parts[1].startswith('b=')
    ac=expr(parts[0][2:]);bc=expr(parts[1][2:])
    assert sp.expand(ac-left/x)==0 and sp.expand(bc-right/x)==0
    cl,cr=map(expr,stages[2].split('='))
    assert cl==ac and cr==bc and sp.solve(cl-cr,var)==[correct]
    rows=stages[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
    expected_rows=2 if record['generation']['template'] in ('affine_blank','fraction_affine_blank') else 1
    assert len(rows)==expected_rows
    for row in rows:
        l,r=map(expr,row.split('='));assert sp.simplify((l-r).subs(var,correct))==0
    if len(rows)==2:
        l,r=map(expr,rows[0].split('='))
        a=sp.diff(ac,var);b=ac.subs(var,0)
        assert l==a*var and r==bc-b
    final_l,final_r=map(expr,rows[-1].split('='));assert final_l==var and final_r==correct
    # Actual displayed objects define the mathematical-task fingerprint.
    a=sp.diff(ac,var);b=ac.subs(var,0)
    profile=record['generation']['profile']
    # Reconstruct every recipe from printed coefficients; no generation parameter lookup.
    r=correct;c=bc
    expected_banks={
        'authored_scale':lambda:[r,1/r,-r,c,a*c],
        'authored_shift':lambda:[r,c+b,c/(-b),(-b)/c,c],
        'observed_ratio':lambda:[r,1/r,-1/r,sp.Integer(1),sp.Integer(0)],
        'observed_scale':lambda:[r,sp.Integer(1),a,a/r,c],
        'observed_signed':lambda:[r,-r,1/r,sp.Integer(0),-a],
        'observed_shift':lambda:[r,c/(-b),(-b)/c,c,-b],
        'blank':lambda:[r],
    }
    assert set(values)==set(expected_banks[profile]())
    assert record['generation']['mathematical_fingerprint']==g.digest(['one-parameter-homogeneous-identity',str(b/a),str(bc/a)])
    p=record['generation']['parameters'];regenerated=g.generate(record['question'][':question/difficulty'].split('/')[-1],seed=912,
          template=record['generation']['template'],profile=record['generation']['profile'],parameters=p)
    assert regenerated['question'][':question/id']==q[':question/id']
    assert sorted(a[':answer/id'] for a in regenerated['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in f[':answer-field/choices'])
    return correct


def meaningful_counts():
    """Enumerate finite semantic domains using independent Python fractions."""
    output={};union=set()
    for template in ('scale_radio','shift_radio'):
        tasks=set();instances=0
        domain=(itertools.product([i for i in range(-8,9) if abs(i)>=2],[0],[i for i in range(-16,17) if abs(i)>=2]) if template=='scale_radio'
                else itertools.product([1],[i for i in range(-8,9) if abs(i)>=2],[i for i in range(-12,13) if abs(i)>=2]))
        for a,b,c in domain:
            r=Fraction(c-b,a)
            if r==0:continue
            wrong=[1/r,-r,Fraction(c),Fraction(a*c)] if template=='scale_radio' else [Fraction(c+b),Fraction(c,-b),Fraction(-b,c),Fraction(c)]
            if len(set([r]+wrong))!=5:continue
            instances+=1;tasks.add((Fraction(b,a),Fraction(c,a)))
        output[template]={'eligible_parameter_tuples':instances,'mathematical_tasks':len(tasks)};union|=tasks
    output['easy_union_tasks']=len(union)
    tasks=set();instances=0
    for a,b,c in itertools.product([i for i in range(-8,9) if abs(i)>=2],[i for i in range(-9,10) if i],[i for i in range(-24,25) if i]):
        r=Fraction(c-b,a)
        if 0<abs(r)<=12 and r.denominator<=4 and abs(c-b)<=48 and math.gcd(a,b,c)==1:
            tasks.add((Fraction(b,a),Fraction(c,a)));instances+=1
    output['affine_blank']={'eligible_parameter_tuples':instances,'mathematical_tasks':len(tasks)}
    coefficients=sorted({Fraction(n,d) for n in range(-12,13) if n for d in range(2,6) if Fraction(n,d).denominator>1 and abs(Fraction(n,d))<=4})
    tasks=set();instances=0
    for a,b,c in itertools.product(coefficients,repeat=3):
        diff=c-b;r=diff/a
        if b.denominator!=c.denominator and 2<=diff.denominator<=10 and abs(diff.numerator)<=24 and 2<=r.denominator<=6 and 1<=abs(r.numerator)<=12:
            tasks.add((b/a,c/a));instances+=1
    output['fraction_affine_blank']={'reduced_coefficient_catalog':len(coefficients),'eligible_parameter_tuples':instances,'mathematical_tasks':len(tasks)}
    return output


def main():
    save('source.json',raw)
    save('topic-context.json',json.loads((ROOT/'generate/runs/current/topics/17592186049310.json').read_text()))
    lesson=json.loads((ROOT/'generate/runs/current/lessons/17592186049310.json').read_text());save('lesson-context.json',lesson)
    activity=lesson['record'][0];steps={s[':db/id']:s for s in activity[':activity/steps']};route=[];node=activity[':activity/first-step'][':db/id']
    while node:
        s=steps[node];c=s[':step/content'];route.append({'step':node,'content_db_id':c[':db/id'],'title':c.get(':tutorial/title',c.get(':knowledge-point/title'))})
        node=s.get(':step/next',{}).get(':db/id')
    save('lesson-route.json',{'source':g.SOURCE,'route':route,'prerequisite_topic':{'db_id':17592186048213,'math_academy_id':343,'title':'Solving Linear Equations With Variables on Both Sides'},'scope_boundary_next_kp':17592186110721})
    cases=[];review=[];grading=[];mapping=[];total=0;wrong=0
    def add(record,label):
        value=check(record);f=record['question'][':question/answer-fields'][0]
        if f[':answer-field/type'].endswith('/radio'):
            checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if expr(a[':answer/value'])==value else 'rejected','purpose':'native owned radio selection; displayed value independently verified'} for a in f[':answer-field/choices']]
        else:
            a,b,c=(sp.Rational(record['generation']['parameters'][k]) for k in ('a','b','c'))
            # Unreduced quotient comes from displayed operations, not a simplified duplicate.
            equiv='('+str(c)+'-('+str(b)+'))/('+str(a)+')'
            checks=[{'submitted':g.tex(value),'expected':'accepted','purpose':'canonical exact parameter'},
                    {'submitted':equiv,'expected':'accepted','purpose':'unevaluated operation quotient equivalent'},
                    {'submitted':r'\frac{'+str(2*value.p)+'}{'+str(2*value.q)+'}','expected':'accepted','purpose':'unreduced rational equivalent'},
                    {'submitted':g.tex(value+1),'expected':'rejected','purpose':'wrong parameter'}]
        grading.append({'label':label,'record':record,'checks':checks})
    for q in source:
        sid=q[':question/math-academy-id'];template,profile,parameters=g.CASES[sid];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
        case={'source_id':sid,'source_db_id':q[':db/id'],'template':template,'level':level,'parameters':parameters,'bank_profile':profile};cases.append(case)
        rec=g.generate(level,template=template,profile=profile,parameters=parameters);add(rec,sid)
        for key in (':question/problem',':question/worked-solution'): assert rec['question'][key]==q[key],(sid,key)
        original=q[':question/answer-fields'][0];new=rec['question'][':question/answer-fields'][0]
        assert original[':answer-field/key']==new[':answer-field/key'] and original[':answer-field/type'][':db/ident']==new[':answer-field/type']
        original_values=[expr(a[':answer/value']) for a in original[':answer-field/choices']]
        generated_values=[expr(a[':answer/value']) for a in new[':answer-field/choices']]
        assert sorted(original_values)==sorted(generated_values)
        assert expr(original[':answer-field/correct'][':answer/value'])==check(rec)
        total+=len(original_values);wrong+=len(original_values)-1
        mapping.append({'source_id':sid,'profile':profile,'parameters':parameters,'source_field_id':original[':answer-field/id'],'source_field_key':original[':answer-field/key'],'choices':[{'recipe':(['correct']+list(g.PROFILES[profile][1]))[g.bank(template,profile,g.normalize(parameters)).index(expr(a[':answer/value']))],'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'correct':a[':answer/id']==original[':answer-field/correct'][':answer/id'],'matched_generated_id':next(b[':answer/id'] for b in new[':answer-field/choices'] if expr(b[':answer/value'])==expr(a[':answer/value']))} for a in original[':answer-field/choices']]})
        review.append({'kind':'original and parameterized replay','source_id':sid,'original':q,'record':rec})
        for seed in (107,218):
            variant=g.generate(level,seed,template=template,profile=profile);add(variant,sid+' changed parameters '+str(seed));review.append({'kind':'generated observed profile variant','source_id':sid,'record':variant})
    for level in ('easy','moderate','hard'):
        for seed in (12,33):
            rec=g.generate(level,seed);add(rec,level+' authored/default '+str(seed));review.append({'kind':'authored hard extension' if level=='hard' else 'normal default variant','record':rec})
    # Every selected profile is exercised under changed parameters and shuffled seeds.
    sampled=0
    for template,spec in g.TEMPLATES.items():
        profiles=[name for name,(owner,_,_) in g.PROFILES.items() if owner==template] if spec['field']=='radio' else ['blank']
        for profile in profiles:
            for seed in range(60):
                check(g.generate(spec['level'],seed,template=template,profile=profile));sampled+=1
    # Signed/fraction boundary cases, errors, profile guards, alias/scale identity.
    invalid=[('easy','scale_radio',{'a':1,'b':0,'c':5}),('easy','shift_radio',{'a':2,'b':3,'c':5}),
             ('moderate','affine_blank',{'a':2,'b':0,'c':8}),('moderate','affine_blank',{'a':-9,'b':3,'c':4}),('moderate','affine_blank',{'a':2,'b':2,'c':4}),
             ('hard','fraction_affine_blank',{'a':'2/2','b':'1/2','c':'1/3'}),
             ('hard','fraction_affine_blank',{'a':'3/2','b':'1/2','c':'3/2'}),
             ('hard','fraction_affine_blank',{'a':'5/3','b':'1/2','c':'3/4'}),
             ('easy','scale_radio',{'a':2,'b':0,'c':2})]
    for level,template,p in invalid:
        try:g.generate(level,template=template,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('invalid explicit input accepted',level,template,p))
    p={'a':2,'b':0,'c':3,'var':'p'}
    a=g.generate('easy',template='scale_radio',profile='observed_ratio',parameters=p)
    b=g.generate('easy',template='q-287970',profile='ratio-unit',parameters={'a':'4/2','b':'0/3','c':'6/2','var':'p'})
    assert a['question'][':question/id']==b['question'][':question/id']
    c=g.generate('easy',template='scale_radio',parameters=p)
    assert c['question'][':question/id']!=a['question'][':question/id'] and c['generation']['mathematical_fingerprint']==a['generation']['mathematical_fingerprint']
    scaled=g.generate('easy',template='scale_radio',parameters={'a':4,'b':0,'c':6,'var':'k'})
    assert scaled['generation']['mathematical_fingerprint']==c['generation']['mathematical_fingerprint'] and scaled['question'][':question/id']!=c['question'][':question/id']
    positions={next(i for i,x in enumerate(g.generate('easy',seed,template='scale_radio',parameters=p)['question'][':question/answer-fields'][0][':answer-field/choices']) if x[':answer/id']==g.generate('easy',seed,template='scale_radio',parameters=p)['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for seed in range(40)}
    assert positions==set(range(5))
    save('source-cases.json',cases);save('choice-mapping.json',mapping);save('review.json',review);save('engine-input.json',grading)
    save('source-replay.json',{'source':g.SOURCE,'all_exact':True,'records':[r for r in review if 'original' in r]})
    save('capabilities.json',{'knowledge_point':g.KP_ID,'generator_version':g.VERSION,'supported':['easy','moderate','hard'],'unsupported':{},'templates':g.TEMPLATES,'profiles':{k:{'template':v[0],'recipes':v[1],'origin':v[2]} for k,v in g.PROFILES.items()},'hard_status':'authored one-parameter rational coefficient extension; no observed hard practice','database_operations':0})
    engine=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'native-grading.json')],check=True)
    native=json.loads((HERE/'native-grading.json').read_text());assert native['documented_unresolved_checks']==0
    counts=meaningful_counts();save('variant-counts.json',counts)
    rows=['# Solving For an Unknown Parameter: source and variant review','',
          'Basis 1356. Original evidence and generator replay are separated below; hard examples are authored, not observed. Normal easy banks use mathematical-error operations; observed banks retain interpretation limits.','']
    for entry in review:
        rec=entry['record'];rows+=['## '+entry['kind']+' — '+entry.get('source_id',rec['question'][':question/difficulty'].split('/')[-1]),'']
        if 'original' in entry:
            oq=entry['original'];rows+=['Original prompt:',oq[':question/problem'],'','Original answers: '+', '.join('$'+a[':answer/value']+'$' for a in oq[':question/answer-fields'][0][':answer-field/choices']),'','Original solution:',oq[':question/worked-solution'],'','Parameterized replay (exact prompt/solution and complete bank):','']
        rows+=[g.markdown(rec),'','Parameters/profile: `'+json.dumps(rec['generation']['parameters'])+'` / `'+rec['generation']['profile']+'`.','']
    (HERE/'review.md').write_text('\n'.join(rows))
    result={'passed':True,'source':g.SOURCE,'coverage':{'practice_questions':len(source),'exact_prompts':5,'exact_complete_worked_solutions':5,'complete_banks':5,'correct_designations':5,'choices':total,'incorrect_choices':wrong,'source_errors':0,'presentation_repairs':0,'math_repairs':0},'independent_displayed_math_instances':sampled+len(grading),'explicit_guard_rejections':len(invalid),'identity_and_shuffle_checks':True,'normal_variant_counts':counts,'authored_extensions':['operation-based easy radio banks','hard fractional affine coefficient blank'],'native_grading':{k:v for k,v in native.items() if k!='records'},'known_limits':['Observed scalar distractor author intent is underdetermined; those profiles are explicit replay only, not sampled by default.','Hard difficulty is authored from the same ax=bx method and rational-coefficient prerequisite context; no observed hard label exists.','All samplers are finite; task fingerprints normalize common nonzero scale and variable aliases.'],'hashes':{'generator':sha(SCRIPT),'validator':sha(Path(__file__)),'check_engine':sha(engine),'check_engine_source':sha(ROOT/'generate/runs/current/check-engine.rs'),'raw_capture':sha(ROOT/'generate/runs/current/sources/17592186110720.json')}}
    save('validation.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        save('validation.json',{'passed':False,'failure':str(exc),'source':g.SOURCE});raise

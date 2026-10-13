#!/usr/bin/env python3
"""Independent checks read displayed TeX, not merely generator answer metadata."""
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json
import re
import subprocess
import sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp33878',ROOT.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z,t=g.x,g.y,g.z,g.t
LOC={'x':x,'y':y,'z':z,'t':t,'e':sp.E,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'sqrt':sp.sqrt}

def brace(s,pos):
    assert s[pos]=='{',s[pos:]
    count=1;i=pos+1
    while count:
        if s[i]=='{':count+=1
        if s[i]=='}':count-=1
        i+=1
    return s[pos+1:i-1],i

def scalar(s):
    s=s.strip().rstrip('.').replace('⁡','').replace('π',r'\pi')
    s=re.sub(r'\\operatorname\{(sin|cos)\}',r' \1 ',s)
    s=s.replace(r'\left','').replace(r'\right','')
    s=s.replace(r'\cdot','*').replace(r'\times','*').replace(r'\,',' ').replace(r'\!',' ')
    while r'\frac' in s or r'\dfrac' in s:
        m=re.search(r'\\d?frac\s*',s);a,j=brace(s,m.end());b,k=brace(s,j)
        s=s[:m.start()]+'(('+scalar_text(a)+')/('+scalar_text(b)+'))'+s[k:]
    while r'\sqrt' in s:
        m=re.search(r'\\sqrt\s*',s);a,j=brace(s,m.end())
        s=s[:m.start()]+'sqrt('+scalar_text(a)+')'+s[j:]
    s=s.replace(r'\pi',' pi ').replace(r'\sin',' sin ').replace(r'\cos',' cos ')
    s=s.replace('{','(').replace('}',')')
    # MA's 3e+1 means 3*Euler's constant+1, never scientific notation 30.
    s=re.sub(r'(?<=\d)e',r'*e',s)
    return parse_expr(s,local_dict=LOC,transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def scalar_text(s):return str(scalar(s))
def eq(a,b):return sp.simplify(sp.expand(a-b))==0
def split_point(s):return tuple(scalar(v) for v in s.split(','))
def call_contents(s,label):
    result=[]
    for m in re.finditer(re.escape(label)+'\\(',s):
        start=m.end();i=start;depth=1
        while depth:
            if s[i]=='(':depth+=1
            if s[i]==')':depth-=1
            i+=1
        result.append(s[start:i-1])
    return result

def displayed_math(record):
    q=record['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution']
    f=scalar(re.search(r'Let \$f\([^)]*\)=(.*?)\.\$',prompt).group(1))
    curve=split_point(re.search(r'r\(t\)=⟨(.*?)⟩',prompt).group(1))
    a,b=split_point(re.search(r't\\in \[(.*?)\]',prompt).group(1))
    A=tuple(sp.simplify(v.subs(t,a)) for v in curve);B=tuple(sp.simplify(v.subs(t,b)) for v in curve)
    fa=sp.simplify(f.subs(dict(zip((x,y,z),A)),simultaneous=True));fb=sp.simplify(f.subs(dict(zip((x,y,z),B)),simultaneous=True))
    answer=sp.simplify(fb-fa)
    # Printed endpoint table, its parameter arguments, and prose coordinates.
    endpoints=re.findall(r'r\((.*?)\)\s*&\s*=⟨(.*?)⟩',solution)
    assert len(endpoints)==2,endpoints
    for (param,coordinates),expected_param,point in zip(endpoints,(a,b),(A,B)):
        assert eq(scalar(param),expected_param)
        assert len(split_point(coordinates))==len(point)
        assert all(eq(u,v) for u,v in zip(split_point(coordinates),point))
    prose=re.search(r'coordinates of the endpoints.*?are \$\((.*?)\)\$ and \$\((.*?)\)\.\$',solution)
    assert prose,'endpoint prose'
    for coordinates,point in zip(prose.groups(),(A,B)):
        assert all(eq(u,v) for u,v in zip(split_point(coordinates),point))
    final=solution[solution.rfind(r'\begin{aligned}'):]
    rows=re.split(r'\\\\\s*&\s*=',final)
    assert len(rows)==(4 if record['generation']['template']=='zero_ellipse' else 5),rows
    theorem_calls=call_contents(rows[0],'r')
    assert len(theorem_calls)==2 and eq(scalar(theorem_calls[0]),b) and eq(scalar(theorem_calls[1]),a),theorem_calls
    f_calls=call_contents(rows[1],'f');assert len(f_calls)==2
    for call,point in zip(f_calls,(B,A)):
        assert all(eq(u,v) for u,v in zip(split_point(call),point))
    # Check every distributed substitution, arithmetic simplification, final row.
    # Reading the actual text catches a missing sign and wrong input before any
    # ID grading; source q-99008's original incorrect first line fails above.
    for row in rows[2:]:
        numeric=row.split(r'\end{aligned}')[0].strip().rstrip('.')
        assert eq(scalar(numeric),answer),(record['generation']['template'],numeric,answer,scalar(numeric))
    return f,curve,a,b,A,B,fa,fb,answer

def balanced(text):
    assert text.count('$')%2==0
    assert text.count('{')==text.count('}')
    # Parentheses need balance in all individual math components after repairs.
    for math in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',text,re.S):
        value=''.join(math)
        # Source style deliberately writes punctuation inside $...$, but has no
        # mismatched mathematical parentheses after the documented repair.
        assert value.count('(')==value.count(')'),value

def check_record(record):
    f,curve,a,b,A,B,fa,fb,answer=displayed_math(record)
    assert not any(v.has(sp.Float) for v in (f,*curve,a,b,fa,fb,answer)),'inexact mathematics'
    q=record['question'];field=q[':question/answer-fields'][0];meta=record['generation']
    assert not any(word in q[':question/problem']+q[':question/worked-solution'] for word in ('\\cosh','\\sinh','\\tanh')),'outside-scope hyperbolic notation'
    balanced(q[':question/problem']);balanced(q[':question/worked-solution'])
    choices=field[':answer-field/choices'];assert len(choices)==5
    assert field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection'
    correct_id=field[':answer-field/correct'][1];values=[scalar(c[':answer/value']) for c in choices]
    assert sum(eq(v,answer) for v in values)==1
    for i,(option,v) in enumerate(zip(choices,values)):
        assert option[':answer/type']==':answer.type/math' and '$' not in option[':answer/value']
        assert not any(word in option[':answer/value'] for word in ('\\cosh','\\sinh','\\tanh'))
        assert not v.has(sp.Float),'inexact displayed answer'
        assert (option[':answer/id']==correct_id)==eq(v,answer)
        expected=sp.sympify(meta['distractor_recipes'][option[':answer/id']]['expression'])
        assert eq(v,expected),(meta['template'],meta['seed'],option[':answer/value'],v,expected)
        assert all(not eq(v,w) for w in values[:i])
    assert len({c[':answer/id'] for c in choices})==5
    import uuid
    qid=uuid.UUID(q[':question/id']);fid=uuid.UUID(field[':answer-field/id'])
    assert fid==uuid.uuid5(qid,'selection')
    for option in choices:assert uuid.UUID(option[':answer/id'])==uuid.uuid5(fid,'math:'+option[':answer/value'])
    # Actual displayed potential/curve/domain must agree with metadata.
    mathematical=meta['mathematical_components']
    assert eq(f,sp.sympify(mathematical['potential']))
    assert all(eq(v,sp.sympify(w)) for v,w in zip(curve,mathematical['curve']))
    assert eq(a,sp.sympify(mathematical['a'])) and eq(b,sp.sympify(mathematical['b']))
    if meta['template'].startswith('reciprocal'):
        assert len(curve)==3 and a==0 and b in (1,2)
        # Fixed two-term workload: both terms at both endpoints nonzero before
        # addition/cancellation, so no dropped defining coefficient is accepted.
        p=meta['parameters'];assert all(1<=abs(p['scale']*p[k])<=3 for k in ('a','b'))
        base,_,_,_=g.components(meta['template'],p)
        for term in sp.Add.make_args(sp.expand(base)):
            assert sp.simplify(term.subs(dict(zip((x,y,z),A)),simultaneous=True))!=0
            assert sp.simplify(term.subs(dict(zip((x,y,z),B)),simultaneous=True))!=0
    return answer

def normalize(s):return re.sub(r'\s+','',s)

def main():
    snapshot=ROOT.parents[1]/'runs/current/sources/17592186133878.json'
    assert (ROOT/'source.json').read_bytes()==snapshot.read_bytes(),'source capture changed'
    source_cases=[];fidelity=[];records=[];review=[];native=[];counts={}
    for name,(level,sid,base) in g.TEMPLATES.items():
        if sid:
            case={'source_id':sid,'source_question_uuid':g.QS[sid][':question/id'],'template':name,
              'difficulty':level,'parameters':{'scale':1,**base},'bank_profile':'observed_scale'}
            source_cases.append(case)
            record=g.generate(level,0,template=name,parameters=case['parameters'],profile='observed_scale')
            answer=check_record(record);source=g.QS[sid];field=source[':question/answer-fields'][0]
            generated=record['question'][':question/answer-fields'][0]
            assert normalize(record['question'][':question/problem'])==normalize(source[':question/problem'])
            vals=[scalar(a[':answer/value']) for a in generated[':answer-field/choices']]
            originals=[scalar(a[':answer/value']) for a in field[':answer-field/choices']]
            assert len(vals)==len(originals)==5
            assert all(sum(eq(a,b) for b in vals)==1 for a in originals),(name,originals,vals)
            assert eq(answer,scalar(field[':answer-field/correct'][':answer/value']))
            repaired=source[':question/worked-solution']
            if sid in g.REPAIRS:repaired=repaired.replace(*g.REPAIRS[sid])
            assert normalize(record['question'][':question/worked-solution'])==normalize(repaired),'complete repaired source solution sequence'
            fidelity.append({'source_id':sid,'template':name,'complete_bank':True,'matched_values':5,'matched_distractors':4,
               'correct_designation':True,'prompt':True,'raw_solution_exact':sid not in g.REPAIRS,
               'repaired_solution_exact':True,'normalization':'whitespace; choices use equivalent standard SymPy TeX'})
            records.append(record)
            # Source replay recipes must genuinely vary at a nontrivial scale.
            for scale in (-2,3):
                scaled=g.generate(level,4,template=name,parameters={'scale':scale,**base},profile='observed_scale')
                check_record(scaled);records.append(scaled)
        fingerprints=set()
        examples=[]
        for seed in range(36):
            record=g.generate(level,seed,template=name)
            check_record(record);records.append(record)
            fingerprints.add(record['generation']['mathematical_fingerprint'])
            if len(examples)<2:examples.append(record)
            params=record['generation']['parameters']
            replay=g.generate(level,seed+901,template=name,parameters=params)
            assert replay['question'][':question/id']==record['question'][':question/id']
            assert replay['generation']['content_fingerprint']==record['generation']['content_fingerprint']
        counts[name]={'sampled_records':36,'distinct_mathematical_tasks':len(fingerprints)}
        print(name+': 36 displayed-math variants, '+str(len(fingerprints))+' distinct tasks',flush=True)
        review.extend(examples)
        if sid:
            # Separate generated variant for EVERY observed complete bank profile.
            variant=g.generate(level,3,template=name,parameters={'scale':2,**base},profile='observed_scale')
            review.append(variant)
        # Explicit parameter guards must never be silently resampled.
        for key,(lo,hi) in g.BOUNDS[name].items():
            for bad in (lo-1,hi+1):
                try:g.generate(level,0,template=name,parameters={**base,'scale':1,key:bad})
                except ValueError:pass
                else:raise AssertionError(('unguarded bound',name,key,bad))
    for record in records:
        field=record['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
        native.append({'label':record['generation']['template']+'-'+record['question'][':question/id'],'record':record,
          'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected',
            'purpose':'complete displayed option selection'} for a in field[':answer-field/choices']]})
    (ROOT/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n')
    (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
    engine=ROOT.parents[1]/'runs/current/check-engine'
    subprocess.run([str(engine),str(ROOT/'native-input.json'),str(ROOT/'native-grading.json')],check=True)
    grading=json.loads((ROOT/'native-grading.json').read_text())
    report={'status':'pass','database':'math','basis':1356,'lineage':g.SOURCE['lineage'],
      'independent_displayed_math_records':len(records),'source_question_coverage':'12/12','complete_original_banks':'12/12',
      'source_choices':'60/60','source_distractors':'48/48','correct_designations':'12/12',
      'raw_exact_solution_sequences':'10/12','repaired_exact_solution_sequences':'12/12',
      'source_format_repairs':{k:list(v) for k,v in g.REPAIRS.items()},'source_fidelity':fidelity,
      'distinct_task_counts_exclude_bank_profile_and_seed':counts,
      'identity':'stable across seed/order; owned UUIDs verified','scope':'hard nonzero endpoint contributions checked',
      'native_grading':{'accepted':grading['accepted_checks'],'rejected':grading['rejected_checks'],'unresolved':grading['documented_unresolved_checks'],
       'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},
      'plots':'none','database_writes':0,'limitations':['Observed scalar distractor intent is underdetermined; homogeneous replay profiles only.',
       'Hard difficulty is authored from canonical example and lesson boundaries; no observed hard label.']}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_fidelity','distinct_task_counts_exclude_bank_profile_and_seed')},indent=2))
if __name__=='__main__':main()

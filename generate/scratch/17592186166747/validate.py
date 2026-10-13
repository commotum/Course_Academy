#!/usr/bin/env python3
"""Fail on actual displayed mathematics, full raw fidelity, scope, formatting,
whole-bank ambiguity, identities and native radio grading. No engine edits."""
import copy, importlib.util, json, re, subprocess, sys, hashlib
from pathlib import Path
import sympy as sp
from texmath import read
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def equal(a,b):
    z=a-b
    if z==0:return True
    witness=z.subs({v:sp.Rational(7,3) for v in z.free_symbols}).evalf(35)
    if witness.is_finite and abs(complex(witness))>1e-20:return False
    substitutions={}
    for fun in (sp.tan,sp.cot,sp.sec,sp.csc):
        for atom in z.atoms(fun):
            u=atom.args[0];substitutions[atom]={sp.tan:sp.sin(u)/sp.cos(u),sp.cot:sp.cos(u)/sp.sin(u),sp.sec:1/sp.cos(u),sp.csc:1/sp.sin(u)}[fun]
    return sp.simplify(sp.trigsimp(sp.cancel(z.xreplace(substitutions))))==0

def definitions(prompt):
    found={}
    for chunk in re.findall(r'(?<!\$)\$([^$]+)\$(?!\$)',prompt):
        matches=list(re.finditer(r'(f\(x,\s*y\)|(?<![A-Za-z\\])[xy])\s*=',chunk))
        for i,m in enumerate(matches):
            rhs=chunk[m.end():matches[i+1].start() if i+1<len(matches) else len(chunk)]
            rhs=re.sub(r'(?:,|\\,|\s)+$','',rhs)
            found['f' if m[1].startswith('f') else m[1]]=read(rhs)
    assert set(found)=={'f','x','y'},(prompt,found)
    return found

def balanced(s):
    assert s.count('$')%2==0
    stack=0
    for i,ch in enumerate(s):
        if ch in '{}':
            # Escaped visible literal braces do not form TeX groups.
            n=0;j=i-1
            while j>=0 and s[j]=='\\':n+=1;j-=1
            if n%2:continue
            stack+=1 if ch=='{' else -1;assert stack>=0,s
    assert stack==0,s
    assert r'\u2061' not in s and '\\\\operatorname' not in s

def displayed_check(record,stages=True):
    q=record['question'];d=definitions(q[':question/problem']);v=next(z for z in d['x'].free_symbols|d['y'].free_symbols if z.name in ('s','t'))
    xx,yy=sp.symbols('x y',positive=True);F=d['f'];X=d['x'];Y=d['y'];sub={xx:X,yy:Y}
    assert F.free_symbols=={xx,yy}
    assert X.free_symbols==Y.free_symbols=={v}
    assert v.name not in ('x','y')
    fx=sp.diff(F,xx);fy=sp.diff(F,yy);sx=fx.subs(sub,simultaneous=True);sy=fy.subs(sub,simultaneous=True);dx=sp.diff(X,v);dy=sp.diff(Y,v)
    answer=sp.diff(F.subs(sub,simultaneous=True),v)
    choices=q[':question/answer-fields'][0][':answer-field/choices'];vals=[read(z[':answer/value']) for z in choices]
    assert len(vals)==5
    for i,z in enumerate(vals):
        for w in vals[:i]:assert not equal(z,w),(record['generation']['template'],'ambiguous bank',z,w)
    correct=q[':question/answer-fields'][0].get(':answer-field/correct')
    if correct:
        ix=next(i for i,z in enumerate(choices) if z[':answer/id']==correct[1]);assert equal(vals[ix],answer),(q[':question/problem'],vals[ix],answer)
        assert sum(equal(z,answer) for z in vals)==1
    else:assert sum(equal(z,answer) for z in vals)==1
    if not stages or ':question/worked-solution' not in q:return
    sol=q[':question/worked-solution'];bs=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(bs)==5
    labels={g.part('x'):'FX',g.part('y'):'FY',g.coord('x',v.name):'DX',g.coord('y',v.name):'DY',g.formal(v.name):'DF'}
    def clean(s):
        for a,b in labels.items():s=s.replace(a,b)
        return s.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').strip()
    first=clean(bs[0]).replace(' ','')
    assert first==r'DF=FX\cdotDX+FY\cdotDY',first
    # Every partial component, including unreduced quotient intermediates.
    for idx,expected in [(1,{'FX':fx,'FY':fy}),(2,{'FX':sx,'FY':sy}),(3,{'DX':dx,'DY':dy})]:
        rows=re.split(r'\\\\|,\\,',clean(bs[idx])); seen=[]
        for row in rows:
            chain=row.strip().rstrip('.,').split('=');key=chain[0].strip();seen.append(key);assert key in expected,(idx,row)
            for rhs in chain[1:]:assert equal(read(rhs),expected[key]),(idx,key,rhs,expected[key])
        assert seen==list(expected),(idx,seen)
    rows=re.split(r'\\\\',clean(bs[4]));assert rows[0].replace(' ','')==r'DF=FX\cdotDX+FY\cdotDY'
    expected_counts={'trig_product':3,'linear_cos':3,'linear_log':3,'exp_trig':3,'trig_quotient':5,'rational_power':5}
    assert len(rows)==expected_counts.get(record['generation']['template'],4),(record['generation']['template'],len(rows))
    for row in rows[1:]:
        rhs=row.split('=',1)[1].strip().rstrip('.,');assert equal(read(rhs),answer),(record['generation']['template'],rhs,answer)
    # Actual products must retain both factors before the reduction, not a final
    # expression copied into several rows. Substitution/reduction structure too.
    assert rows[1].count(r'\cdot')==2
    if record['generation']['template']=='power_exp':assert clean(bs[2]).count('=')==4
    if record['generation']['template']=='linear_log':assert clean(bs[2]).count('=')==3
    assert sol.count('First, we find the partial derivatives')==1
    if record['generation']['profile']!='observed_raw':
        for text in [q[':question/problem'],sol]+[a[':answer/value'] for a in choices]:balanced(text)


def main():
    capture=json.loads(Path('generate/runs/current/sources/17592186166747.json').read_text());assert capture==g.SNAPSHOT
    byte_rows=[]
    for source in g.SOURCES:
        for answer in source[':question/answer-fields'][0][':answer-field/choices']:
            val=answer[':answer/value'];row={'source_id':source[':db/id'],'answer_id':answer[':answer/id'],'ordinal_prefix':[ord(z) for z in val[:20]],'adjacent_ord92_pairs':sum(ord(val[j])==ord(val[j+1])==92 for j in range(len(val)-1)),'literal_six_character_u2061':val.count(chr(92)+'u2061'),'actual_U2061_count':val.count(chr(8289))};byte_rows.append(row)
    assert sum(z['adjacent_ord92_pairs']+z['literal_six_character_u2061'] for z in byte_rows)==0
    (HERE/'source-errors.json').write_text(json.dumps({'capture_private_decoded_equal':True,'escape_defects':0,'byte_inspection':byte_rows,'errors':[{'source_id':g.QMAP['exp_product'][':db/id'],'missing_attributes':[':question/difficulty',':question/worked-solution',':answer-field/correct'],'repair':'independently derive derivative; assign authored easy and formal five-block solution only in repaired/normal profiles'}]},indent=2))
    cases=[];engine=[];review=[];source_counts={'questions':0,'options':0,'correct_designations':0,'solutions':0,'raw_presence':0};checks=0
    for name,source in g.QMAP.items():
        print('Validate',name,flush=True)
        case={'source_id':source[':db/id'],'template':name,'parameters':{'h':0},'bank_profile':'observed_raw','level':'easy','authored_unrated_assignment':name=='exp_product'};cases.append(case)
        raw=g.generate_easy(template=name,parameters={'h':0},profile='observed_raw')
        q=raw['question'];assert set(q)==set(source)
        assert raw['generation']['original_refs']==source
        assert q[':question/problem']==source[':question/problem']
        assert q.get(':question/worked-solution')==source.get(':question/worked-solution')
        assert (':question/difficulty'in q)==(':question/difficulty'in source)
        for key in (':question/worked-solution',':question/answer-fields'):assert(key in q)==(key in source)
        fs=q[':question/answer-fields'][0];orig=source[':question/answer-fields'][0]
        assert set(fs)==set(orig)
        for a,b in zip(fs[':answer-field/choices'],orig[':answer-field/choices']):assert set(a)==set(b)
        assert [a[':answer/value'] for a in fs[':answer-field/choices']]==[a[':answer/value'] for a in orig[':answer-field/choices']]
        assert fs[':answer-field/type']==orig[':answer-field/type'][':db/ident']
        assert (':answer-field/correct' in fs)==(':answer-field/correct' in orig)
        if ':answer-field/correct'in orig:
            value=next(a[':answer/value'] for a in fs[':answer-field/choices'] if a[':answer/id']==fs[':answer-field/correct'][1]);assert value==orig[':answer-field/correct'][':answer/value'];source_counts['correct_designations']+=1
        source_counts['questions']+=1;source_counts['options']+=5;source_counts['solutions']+=int(':question/worked-solution'in source);source_counts['raw_presence']+=1
        displayed_check(raw,stages=name!='exp_product')
        repaired=g.generate_easy(template=name,parameters={'h':0},profile='observed_repaired');displayed_check(repaired,stages=name=='exp_product')
        translated=g.generate_easy(template=name,parameters={'h':1},profile='observed_repaired');displayed_check(translated,stages=True)
        assert not raw['generation']['eligible_for_learning'] and not repaired['generation']['eligible_for_learning']
        normal=g.generate_easy(template=name,parameters=g.ORIGINAL[name]);displayed_check(normal);checks+=1
        for j in range(4):
            variant=g.generate_easy(seed=17+j,template=name);displayed_check(variant);checks+=1
            if j<2:review.append({'label':'Generated easy '+name,'record':variant})
        review.append({'label':'Generated full historical bank evidence translation '+name,'record':translated})
        review.extend([{'label':'Original public raw '+name,'record':raw},{'label':'Minimal repaired evidence '+name,'record':repaired},{'label':'Normal at original mathematics '+name,'record':normal}])
        for rec in (normal,repaired):
            fld=rec['question'][':question/answer-fields'][0];correct=fld[':answer-field/correct'][1]
            engine.append({'label':name+' '+rec['generation']['profile'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Actual native owned radio selection'} for a in fld[':answer-field/choices']]})
    for level in ('moderate','hard'):
        print('Validate',level,flush=True)
        for seed in range(10):
            rec=g.generate(level,seed);displayed_check(rec);checks+=1
            if seed<2:review.append({'label':'Authored '+level,'record':rec})
            if seed<3:
                fld=rec['question'][':question/answer-fields'][0];engine.append({'label':level+str(seed),'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==fld[':answer-field/correct'][1] else 'rejected','purpose':'Authored level native radio selection'} for a in fld[':answer-field/choices']]})
    # Signed explicit corners, paired with the same sampler guards.
    for name in g.NAMES:
        p=g.ORIGINAL[name].copy();p.update(h=-3,k=3)
        if name in ('trig_quotient','log_trig'):p['k']=-3
        displayed_check(g.generate_easy(template=name,parameters=p));checks+=1
    for level,bad in [('moderate',dict(n=2,a=1,b=2,h=0,k=0)),('hard',dict(n=2,a=1,b=2,h=0,k=1))]:
        try:g.generate(level,parameters=bad)
        except ValueError:pass
        else:raise AssertionError('Explicit level guard bypass')
    # Identity ignores seed, choice order and method-profile aliases; content is
    # independently determined from displayed prompt, fixed solution and bank.
    r1=g.generate_easy(1,template='power_exp',parameters=g.ORIGINAL['power_exp']);r2=g.generate_easy(22,template='power_exp',parameters=g.ORIGINAL['power_exp']);assert r1['question'][':question/id']==r2['question'][':question/id']
    alias1=g.generate_hard(parameters=dict(n=2,a=2,b=1,h=2,k=1));alias2=g.generate_hard(parameters=dict(n=2,a=1,b=2,h=1,k=2))
    assert alias1['generation']['mathematical_fingerprint']==alias2['generation']['mathematical_fingerprint']
    assert alias1['question'][':question/id']!=alias2['question'][':question/id']
    assert set(r1['knowledge_point'])=={'db_id','id','title'}
    families={g.generate_easy(seed=i)['generation']['template'] for i in range(100)};assert families==set(g.NAMES),families
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2));(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False))
    (HERE/'engine-input.json').write_text(json.dumps(engine));binary=Path('generate/runs/current/check-engine')
    subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    import os
    os.environ.setdefault('MPLCONFIGDIR',str(HERE/'matplotlib-cache'))
    runtime={'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':__import__('matplotlib').__version__}
    report={'status':'passed','source_fidelity':source_counts,'normal_displayed_math_records':checks,'native_checks':sum(len(r['checks']) for r in engine),'native_typed_applicable':0,'native_limit':'All observed and normal fields are radio; typed equivalence is not a radio submission. Native ID grading is separate from mathematical choice checks. Unrated raw source missing correct ref is excluded from grading, publicly retained.','source_anomalies':{'missing_correct_ref':1,'missing_solution':1,'missing_difficulty':1,'malformed_answer_escape_options':0},'normal_source_structural_stage_cases':12,'authored_levels':['moderate','hard'],'default_family_coverage':sorted(families),'runtime':runtime,'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'limits':['Historical distractor intent is unresolved; translated full source banks and repaired opaque banks remain evidence only.','Missing moderate/hard ratings are explicit curriculum-grounded workload claims.','Source domain omission root_log, linear_log and trig_quotient repaired by normal explicit domains; source captured unchanged.','Normal mathematical typography is normalized, not raw byte-identical; exact raw replay preserves original values/strings/presence.']}
    variety=json.loads((HERE/'variety.json').read_text());assert [variety[l]['canonical_mathematical_tasks'] for l in g.LEVELS]==[375,48,636]
    report['enumerated_variety']=variety
    report['source_displayed_solution_math_checked']=11
    report['fidelity_note']='Raw prompt/solution/options are byte-exact; every source question/field/answer attribute has presence parity, with local UUIDs and schema enum/ref conversion. Original refs are retained verbatim in generation.original_refs. Normal solutions preserve mathematical stage order, with valid normalized notation.'
    (HERE/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
    md=['# Originals and generated variants\n\nRaw evidence is ineligible; all normal examples use complete method-derived banks.\n']
    for item in review:md+=['\n## '+item['label']+'\n',g.markdown(item['record'])]
    (HERE/'review.md').write_text('\n'.join(md))
if __name__=='__main__':main()

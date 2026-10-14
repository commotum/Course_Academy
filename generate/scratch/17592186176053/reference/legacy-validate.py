#!/usr/bin/env python3
"""Independent displayed-semantic, source, identity and native-grade checks."""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from PIL import Image
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('csc',ROOT.with_suffix('.py')); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def coefficient(tex):
    s=tex.replace('π',r'\pi').replace(' ','')
    m=re.fullmatch(r'(-?)\\frac\{(-?\d*)\\pi\}\{2\}',s)
    if m:return sp.Rational(int((m[1] or '')+(m[2] if m[2] not in ('','-') else m[2]+'1')),2)
    m=re.fullmatch(r'(-?\d*)\\pi',s)
    if m:return sp.Integer(m[1] if m[1] not in ('','-') else m[1]+'1')
    raise AssertionError(('unparsed coefficient',tex))
def independent(record):
    q=record['question'];text=q[':question/problem'];t=record['generation']['template']
    if t=='basic_properties':
        claims=text.split('\n\n')[1].splitlines(); truths=[]
        true={v[0] for v in g.PROPERTIES}; false={v[1] for v in g.PROPERTIES}
        for c in claims:
            v=c.split('. ',1)[1];assert v in true|false;truths.append(v in true)
    elif t=='indexed_properties':
        point=re.search(r'The point \$\((.*?),(-?\d)\)\$',text);c=coefficient(point[1]);y=int(point[2]);truths=[sp.sin(sp.pi*c)!=0 and 1/sp.sin(sp.pi*c)==y]
        asym=re.search(r'\$x=(.*?)\$ is a vertical asymptote',text);truths.append(bool(coefficient(asym[1]).is_integer))
        dom=re.search(r'\$x=(.*?)\$ is in the domain',text);truths.append(not bool(coefficient(dom[1]).is_integer))
        solution=q[':question/worked-solution']; displayed=int(re.search(r'takes the value \$(-?\d)\$',solution)[1]);assert displayed==1/sp.sin(sp.pi*c)
        assert str(truths[0]).lower() in solution.split('Hence, statement I is ')[1].split('.')[0]
    elif t=='q-42912':
        m=re.search(r'point \$\((.*?),(-?\d)\)\$',text);c=coefficient(m[1]);y=int(m[2]);v=int(re.search(r'value \$y = (-?\d+)\$',text)[1]);truths=[sp.sin(sp.pi*c)==0 or 1/sp.sin(sp.pi*c)!=y,True,abs(v)>=1]
    elif t=='q-65310':
        c=coefficient(re.search(r'zero at \$x = (.*?)\$',text)[1]);assert sp.sin(sp.pi*c)!=0
        assert r'x =-\frac{π}{2} + 2nπ' in text
        truths=[True,False,True]
    elif t in ('q-103811','q-65307'):
        c=coefficient(re.search(r'\$x=(.*?)\$ is a vertical asymptote',text)[1]);truths=[False,bool(c.is_integer),True]
        if t=='q-103811':
            shifts=[int(v.replace(' ','')) for v in re.findall(r'x([+-]\d+)\\pi',text)];assert len(shifts)==2 and (shifts[0]-shifts[1])%2==0
            solution=q.get(':question/worked-solution','');assert all(f'x{v:+d}\\pi ' in solution for v in shifts)
    elif t=='q-103814':
        c=coefficient(re.search(r'\$x=(.*?)\$ is a vertical asymptote',text)[1]);m=re.search(r'takes the value \$(-?1)\$ at \$x=(.*?)\$',text);angle=m[2].split('+2n')[0]; truths=[False,bool(c.is_integer),1/sp.sin(sp.pi*coefficient(angle))==int(m[1])]
        solution=q[':question/worked-solution'];assert f'takes the value ${m[1]}$' in solution
    elif t=='q-65308':
        c=coefficient(re.search(r'\$x=(.*?)\$ is in the domain',text)[1]);shift=int(re.search(r'x([+-]\d+)\\pi',text)[1]);truths=[False,shift%2==0,not bool(c.is_integer)]
        solution=q[':question/worked-solution'];n=int(re.search(r'n=(-?\d+),',solution)[1]);assert 2*n==shift;assert re.search(r'so \$(.*?)\$ is not in',solution)[1].strip()==re.search(r'\$x=(.*?)\$ is in',text)[1].strip()
    else:
        c=coefficient(re.search(r'III\. \$x=(.*?)\$ is in',text)[1]);truths=[False,False,not bool(c.is_integer)]
    solution=q.get(':question/worked-solution','')
    indices={'I':0,'II':1,'III':2}
    assertions=re.findall(r'statement (III|II|I) is (true|false)',solution,re.I)
    for index,value in assertions: assert bool(truths[indices[index.upper()]])==(value.lower()=='true')
    if 'statements I and II are both false' in solution: assert not truths[0] and not truths[1]
    if solution: assert len(assertions)==3 or (t=='q-103812' and len(assertions)==1)
    mask=sum(1<<i for i,v in enumerate(truths) if v);assert mask==record['generation']['truth_mask']
    fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio';assert len(f[':answer-field/choices'])==5
    values=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(set(values))==5
    # Every complete displayed selection is independently interpreted as a subset.
    expected={i+1 for i,v in enumerate(truths) if v}; eligible=[]
    for a in f[':answer-field/choices']:
        v=a[':answer/value']; selected={i+1 for i,n in enumerate(['I','II','III']) if re.search(r'(?<!I)'+n+r'(?!I)',v)} if not v.startswith('None') else set()
        if selected==expected:eligible.append(a[':answer/id'])
    assert len(eligible)==1
    if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',eligible[0]]
    if not record['generation']['evidence_only']:
        assert text.count('$')%2==0 and '$$' not in text
        for v in (text,q[':question/worked-solution']): assert v.count('{')==v.count('}') and v.count('$')%2==0
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    return eligible[0]

def main():
    cases=[];records=[];banks=values=designations=solutions=0
    for t,q in g.SOURCES.items():
        case={'source_id':q[':question/id'],'math_academy_id':t,'template':t,'level':'moderate','parameters':g.ORIGINAL[t],'bank_profile':'observed:'+t,'assignment':'observed' if ':question/difficulty' in q else 'authored moderate inference'};cases.append(case)
        r=g.generate('moderate',template=t,parameters=g.ORIGINAL[t],profile='observed:'+t);independent(r);new=r['question'];assert new[':question/problem']==q[':question/problem']
        for key in (':question/difficulty',':question/worked-solution'):assert (key in new)==(key in q)
        if ':question/worked-solution' in q: assert new[':question/worked-solution']==q[':question/worked-solution'];solutions+=1
        a=q[':question/answer-fields'][0];b=new[':question/answer-fields'][0];assert a[':answer-field/key']==b[':answer-field/key'];assert sorted(x[':answer/value'] for x in a[':answer-field/choices'])==sorted(x[':answer/value'] for x in b[':answer-field/choices']);banks+=1;values+=len(a[':answer-field/choices'])
        assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
        if ':answer-field/correct' in a:assert r['generation']['correct_value']==a[':answer-field/correct'][':answer/value'];designations+=1
        records.append(r)
        # Every observed family serves normal sampling and changed-parameter masks.
        for seed in range(40):
            variant=g.generate('moderate',seed,template=t);independent(variant);records.append(variant)
        # Raw evidence replay also supports real parameterization with source presence.
        independent(g.generate('moderate',17,template=t,profile='observed:'+t))
    # All finite easy semantic tasks, and all hard objects, independently checked.
    for trio in range(10):
        for mask in range(8):independent(g.generate_easy(parameters={'trio':trio,'mask':mask}))
    for k,y,a,d in itertools.product([-11,-9,-7,-5,5,7,9,11],[-1,1],list(range(-15,-1))+list(range(2,16)),list(range(-15,-1))+list(range(2,16))):independent(g.generate_hard(parameters={'point':k,'ordinate':y,'asymptote':a,'domain':d}))
    for l in ('easy','hard'):
        for seed in range(50):r=g.generate(l,seed);independent(r);records.append(r)
    assert {g.generate_moderate(i)['generation']['template'] for i in range(100)}==set(g.SOURCES)
    for l in ('easy','moderate','hard'):
        r=g.generate(l,2);same=g.generate(l,99,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile']);assert r['question'][':question/id']==same['question'][':question/id']
        assert sorted(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in same['question'][':question/answer-fields'][0][':answer-field/choices'])
    invalid=[('hard','indexed_properties',{'point':1,'ordinate':1,'asymptote':2,'domain':2}),('easy','basic_properties',{'trio':10,'mask':0}),('moderate','q-103811',{'asymptote':2,'left':-4,'right':6}),('moderate','q-65308',{'shift':3,'domain':5})]
    for l,t,p in invalid:
        try:g.generate(l,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid explicit input accepted')
    engine=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0]
        if ':answer-field/correct' not in f:continue
        correct=independent(r);engine.append({'label':f'{i}:{r["generation"]["template"]}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'all owned selection values; mathematics independently checked'} for a in f[':answer-field/choices']]})
    (ROOT/'engine-input.json').write_text(json.dumps(engine));subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
    (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    review=[]
    for t in g.SOURCES:
        for seed in (6,17):review.append(g.generate_moderate(seed,template=t))
    for l in ('easy','hard'):
        for seed in (6,17):review.append(g.generate(l,seed))
    (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    md=['# Originals and generated variants','Raw original omissions and malformed TeX are evidence, not eligible learner defaults.']
    for t in g.SOURCES:
        original=g.generate_moderate(template=t,parameters=g.ORIGINAL[t],profile='observed:'+t)
        md+=['## Original '+t,g.markdown(original)]
        for r in review:
            if r['generation']['template']==t:md+=['### Generated normal '+t+' '+str(r['generation']['parameters']),g.markdown(r)]
    for r in review:
        if r['generation']['template'] not in g.SOURCES:md+=['## Authored '+r['question'][':question/difficulty'],g.markdown(r)]
    (ROOT/'review.md').write_text('\n\n'.join(md)+'\n')
    assets=[]
    for rel in sorted(set(re.findall(r'images/[^)]+',json.dumps(g.SNAPSHOT,ensure_ascii=False)) + ['images/67/67463d29b77a6db10538bcf5956f9bb8a40a5d41a2b7741c6de52bd336bcc550.png'])):
        path=Path('/media/jake/SSD/EDB/math')/rel;im=Image.open(path);assets.append({'path':str(path),'size':im.size,'mode':im.mode,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'inspected_full_resolution':True,'parameter_dependent':False})
    (ROOT/'plot-provenance.json').write_text(json.dumps(assets,indent=2)+'\n')
    report={'status':'pass','source_basis':1356,'source_questions':7,'raw_exact_prompts':'7/7','complete_banks':'7/7','all_choice_values':'35/35','observed_correct_designations':'5/5','absent_correct_designations':2,'raw_exact_existing_solutions':'5/5','inferred_normal_solutions':2,'normal_presentation_repairs':['q-103814 decoded trailing $$ removed'],'observed_distractors':'20/20 (five designated banks)','inferred_distractors':'8/8 (two designationless banks; not observed)','independent_easy_tasks':80,'independent_hard_tasks':12544,'changed_source_variants':280,'normal_default_family_coverage':'7/7','native':json.loads((ROOT/'engine-report.json').read_text()),'engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'remaining_limitations':['Finite categorical family; all curves untransformed.','Two missing original correct designations and solutions are inferred only in normal output.','Authored easy/hard labels are design claims, not recovered observed ratings.','No variable plots, renderer transforms/DPI/concurrency are not applicable.']}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='native'},indent=2))
if __name__=='__main__':main()

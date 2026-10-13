#!/usr/bin/env python3
"""Independent displayed-math, source fidelity, raster and native grading QA."""
import concurrent.futures,copy,hashlib,importlib.util,json,math,re,subprocess,sys
from pathlib import Path
import sympy as sp
from PIL import Image
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def parsed(text):
    """Small independent parser for the actually displayed rational/trig masks."""
    text=text.replace('⁡','').replace(r'\operatorname{cot}','cot').replace(r'\cdot','*').replace(r'\pi','pi').replace(r'\,','').strip().rstrip('.')
    while r'\frac' in text:
        start=text.rfind(r'\frac');i=start+5
        def group(i):
            assert text[i]=='{';j=i+1;depth=1
            while depth:
                if text[j]=='{':depth+=1
                if text[j]=='}':depth-=1
                j+=1
            return text[i+1:j-1],j
        n,j=group(i);d,j=group(j);text=text[:start]+'(('+n+')/('+d+'))'+text[j:]
    from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
    return parse_expr(text,local_dict={'cot':sp.cot,'pi':sp.pi},transformations=standard_transformations+(implicit_multiplication_application,))

def scalar(v):return sp.simplify(parsed(v))

def check_format(text):
    assert text.count('$')%2==0
    depth=0
    for c in text:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert '+-' not in text and '--' not in text

def derive_plot(record):
    """Read displayed label glyphs from renderer strings; no answer metadata."""
    p=record['generation']['plots']['prompt'];meta=json.loads(Path(p).with_suffix('.json').read_text())
    labels=meta['labels'];mid=scalar(labels[0]['text'].strip('$'));end=scalar(labels[1]['text'].strip('$'));D=scalar(labels[2]['text'].strip('$'))
    B=sp.simplify(sp.pi/end)
    assert sp.simplify(mid-end/2)==0
    # Transform the ACTUAL blue PNG stroke into coordinates independently.
    image=Image.open(p).convert('RGB');pixels=image.load();W,H=image.size
    blue=[]
    for xp in range(W):
        for yp in range(H):
            r,gg,b=pixels[xp,yp]
            if b>r+50 and gg>r+20 and b>100:blue.append((xp,yp))
    assert len(blue)>500
    left,bottom,width,height=meta['axes_bounds_px'];xmin,xmax=meta['limits']['x'];ymin,ymax=meta['limits']['y']
    def xy_to_px(x,y):return (left+(x-xmin)/(xmax-xmin)*width,H-(bottom+(y-ymin)/(ymax-ymin)*height))
    lo,hi=meta['branch']['xlo'],meta['branch']['xhi'];worst=0
    # Nearest stroke point under actual axes transform; antialias tolerance.
    for i in range(1,80):
        x=lo+(hi-lo)*i/80;y=float(sp.cot(B*x)+D);xp,yp=xy_to_px(x,y)
        distance=min(math.hypot(a-xp,b-yp) for a,b in blue if abs(a-xp)<6)
        worst=max(worst,distance)
    assert worst<3,('PNG curve disagrees',p,worst)
    # Curve decreases in displayed x. Undefined y-intercept and no endpoints.
    assert meta['branch']['monotonicity']=='strictly decreasing'
    assert meta['branch']['y_intercept'] is None and 'none' in meta['branch']['endpoints']
    for box in labels:
        x,y,w,h=box['bounds'];assert 0<=x<x+w<=W and 0<=y<y+h<=H
    return B,D,{'worst_stroke_distance_px':worst,'size':[W,H]}

def check_record(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    json.loads(json.dumps(r));q=r['question'];gen=r['generation']
    check_format(q[':question/problem']);check_format(q[':question/worked-solution'])
    B,D,png=derive_plot(r)
    requested=re.search(r'What is\s*\$(B(?:[+-](?:2)?D)?)\?\$',q[':question/problem']).group(1)
    answer=scalar(requested).subs({sp.Symbol('B'):B,sp.Symbol('D'):D})
    assert answer==scalar(gen['answer'])
    # Every displayed period, reciprocal, D, arithmetic and conclusion stage.
    tokens=g.MATH.findall(q[':question/worked-solution'])
    assert scalar(tokens[7].strip('$\n ').rstrip('.'))==abs(D)
    assert ('units up' in q[':question/worked-solution'] or 'unit up' in q[':question/worked-solution'])==(D>0)
    if '=' not in tokens[1]:assert sp.simplify(scalar(tokens[1].strip('$\n ').rstrip('.'))-sp.pi/B)==0
    stages=0
    for token in tokens:
        content=token.strip('$\n ').rstrip('.')
        if '=' not in content:continue
        if content.startswith('y=A'):continue # general formal family only
        if content.startswith('y='):
            x=sp.Symbol('x');curve=parsed(content[2:]);assert sp.simplify(curve-(sp.cot(B*x)+D))==0;stages+=1;continue
        for eq in content.split('⟹'):
            sides=eq.split('=')
            parsed_sides=[parsed(s).subs({sp.Symbol('B'):B,sp.Symbol('D'):D,sp.Symbol('T'):sp.pi/B}) for s in sides]
            assert all(sp.simplify(v-parsed_sides[0])==0 for v in parsed_sides[1:]),(content,parsed_sides)
            stages+=len(sides)-1
    assert stages>=7
    for f in q[':question/answer-fields']:
        vals=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5 and len(set(vals))==5
        for a in f[':answer-field/choices']:check_format(a[':answer/value'])
        if ':answer-field/correct' in f:
            aid=f[':answer-field/correct'][1];correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==aid);assert scalar(correct[':answer/value'])==answer
    return {'id':q[':question/id'],'stages_checked':stages,'raster':png}

def source_raster(q,b,d):
    """Per-source native pixel fit with its own origin, scales, and guides."""
    rel=re.search(r'images/[^)]+',q[':question/problem']).group();path=Path('/media/jake/SSD/EDB/math')/rel
    im=Image.open(path).convert('RGB');W,H=im.size;p=im.load()
    black=lambda rgb:max(rgb)<80
    grey=lambda rgb:90<rgb[0]<210 and max(rgb)-min(rgb)<8
    x0=max(range(W),key=lambda x:sum(black(p[x,y]) for y in range(H)))
    y0=max(range(H),key=lambda y:sum(black(p[x,y]) for x in range(W)))
    right=max(range(x0+int((W-x0)*.6),W-10),key=lambda x:sum(grey(p[x,y]) for y in range(15,H)))
    yD=max([y for y in range(15,H-10) if abs(y-y0)>6],key=lambda y:sum(grey(p[x,y]) for x in range(x0+8,(x0+right)//2-8)))
    sy=(y0-yD)/float(d);assert sy>0
    blue=[]
    for x in range(W):
        ys=[y for y in range(H) if p[x,y][2]>p[x,y][0]+40 and p[x,y][1]>p[x,y][0]+15]
        if ys:blue.append((x,sum(ys)/len(ys)))
    # Fit source independently; a 3px bounded stroke allowance accommodates
    # rasterization and illustrative curve thickness, not changed geometry.
    residual=[]
    for x,y in blue:
        u=(x-x0)/(right-x0)
        if .08<u<.92:
            pred=y0-sy*(1/math.tan(math.pi*u)+float(d))
            # Perpendicular distance compensates for steep-tail x uncertainty.
            slope=sy*math.pi/(right-x0)/(math.sin(math.pi*u)**2)
            residual.append(abs(y-pred)/math.sqrt(1+slope*slope))
    worst=max(residual);assert worst<4,(q[':question/math-academy-id'],worst,x0,y0,right,yD)
    return {'source_id':q[':question/math-academy-id'],'path':str(path),'png_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'native_size':[W,H],'origin_px':[x0,y0],'period_asymptote_x_px':right,'midpoint_x_px':(x0+right)/2,'midpoint_y_px':yD,'y_pixels_per_unit':sy,'period_pi':str(1/b),'B':str(b),'D':str(d),'x_intercept_pi':str(sp.acot(-d)/(b*sp.pi)),'y_intercept':None,'monotonicity':'decreasing','endpoints':'none; unbounded tails cropped by viewport','max_curve_perpendicular_residual_px':worst}

def main():
    evidence=[];fidelity=[];records=[];sourceplots=[]
    for case,q in zip(g.CASES,g.RAW[':knowledge-point/questions']):
        r=g.generate('moderate',profile=case['bank_profile'],parameters=case['parameters']);records.append(r)
        assert r['question'][':question/problem']==q[':question/problem']
        assert r['question'][':question/worked-solution']==q[':question/worked-solution'],case['source_id']
        assert len(r['question'][':question/answer-fields'])==len(q[':question/answer-fields'])
        for src,new in zip(q[':question/answer-fields'],r['question'][':question/answer-fields']):
            assert set(map(scalar,[a[':answer/value'] for a in src[':answer-field/choices']]))==set(map(scalar,[a[':answer/value'] for a in new[':answer-field/choices']]))
            assert sorted(a[':answer/value'] for a in src[':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':answer-field/choices'])
            assert (':answer-field/correct' in src)==(':answer-field/correct' in new)
            assert src[':answer-field/key']==new[':answer-field/key']
        evidence.append(check_record(r));fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':True,'complete_banks':len(q[':question/answer-fields']),'choices':sum(len(f[':answer-field/choices']) for f in q[':question/answer-fields']),'matched_designations':sum(':answer-field/correct' in f for f in q[':question/answer-fields'])})
        sourceplots.append(source_raster(q,sp.Rational(case['parameters']['B']),sp.Rational(case['parameters']['D'])))
        # Changed-parameter source-mask and complete observed bank replay.
        p=case['parameters'].copy();p['B']=str(sp.Rational(p['B'])*sp.Rational(3,2));p['D']=str(sp.Rational(p['D'])*sp.Rational(3,2))
        # Same source number-form scope guards; supported rational ray instead.
        if sp.Rational(p['B']).q not in (1,2,4,5) or sp.Rational(p['D']).q not in (1,2,4,5) or abs(sp.Rational(p['D']))>5:p=case['parameters'].copy();p['B']=str(sp.Rational(p['B'])*2)
        variant=g.generate('moderate',seed=91,profile=case['bank_profile'],parameters=p);records.append(variant);evidence.append(check_record(variant))
    sourceplots.insert(0,source_raster(g.RAW[':knowledge-point/canonical-example'],sp.Rational(2),sp.Rational(-1)))
    (HERE/'source-geometry.json').write_text(json.dumps(sourceplots,indent=2)+'\n')
    # Select every default bank; two examples per level plus signed boundaries.
    for level in ('easy','moderate','hard'):
        for seed in range(8):
            r=g.generate(level,seed);records.append(r);evidence.append(check_record(r))
    for level,profile in [('easy','easy_period'),('moderate','method_sign_period'),('moderate','method_midpoint_offset'),('hard','method_sign_period'),('hard','method_midpoint_offset')]:
        catalog=g.eligible_domain(level,profile)
        for p in [catalog[0],catalog[-1]]:
            r=g.generate(level,profile=profile,parameters={'B':str(p[0]),'D':str(p[1]),'k':p[2]});records.append(r);evidence.append(check_record(r))
    # Invalid explicit workloads and collision cases must fail, never resample.
    invalid=[('easy',{'B':'1','D':'1','k':0}),('moderate',{'B':'5/4','D':'9/4','k':1}),('hard',{'B':'3','D':'1','k':1}),('hard',{'B':'31/4','D':'1/4','k':1})]
    for level,p in invalid:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('Bad workload accepted',level,p))
    for kwargs in ({'parameters':{}},{'template':''}):
        try:g.generate_moderate(profile='observed_q-65549',**kwargs)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit source input accepted')
    fixed={'B':'5/4','D':'-9/4','k':2}
    a=g.generate_hard(1,profile='method_sign_period',parameters=fixed);b=g.generate_hard(202,profile='method_sign_period',parameters=fixed)
    assert a['question'][':question/id']==b['question'][':question/id'];assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
    c=g.generate_hard(1,profile='method_midpoint_offset',parameters=fixed)
    assert a['question'][':question/id']!=c['question'][':question/id'];assert a['generation']['parameter_fingerprint']==c['generation']['parameter_fingerprint']
    # Fresh concurrent outputs test same and different parameter geometry.
    temp=HERE/'concurrent-plots';temp.mkdir(exist_ok=True)
    args=[{'B':'7/4','D':'-3/5','x_mid_pi':'2/7','x_asymptote_pi':'4/7','y_increment':'1/5'}, {'B':'7/4','D':'-3/5','x_mid_pi':'2/7','x_asymptote_pi':'4/7','y_increment':'1/5'}, {'B':'9/5','D':'5/4','x_mid_pi':'5/18','x_asymptote_pi':'5/9','y_increment':'1/4'}]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:outputs=list(pool.map(lambda p:g.render_plots(p,temp),args))
    assert outputs[0]['geometry']['instance']==args[0] and outputs[1]['geometry']['instance']==args[1] and outputs[2]['geometry']['instance']==args[2]
    assert outputs[0]['geometry']['png_sha256']==outputs[1]['geometry']['png_sha256']
    assert not list(temp.glob('render-input-*'))
    engine=[]
    for i,r in enumerate(records):
        fixture=copy.deepcopy(r);fixture['question'][':question/answer-fields']=[f for f in fixture['question'][':question/answer-fields'] if ':answer-field/correct' in f]
        checks=[]
        for j,f in enumerate(fixture['question'][':question/answer-fields']):
            for option in f[':answer-field/choices']:checks.append({'field_index':j,'submitted_answer_id':option[':answer/id'],'expected':'accepted' if option[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native owned radio selection'})
        engine.append({'label':str(i),'record':fixture,'checks':checks})
    (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
    process=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,capture_output=True,text=True)
    (HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n')
    review=['# Cotangent stretch and shift review','Original raw images use the frozen image references; generated image paths are absolute. Profiles marked observed are evidence-only, opaque banks. Normal defaults are explicitly authored banks.']
    for case,q,r,v in zip(g.CASES,g.RAW[':knowledge-point/questions'],records[0:24:2],records[1:24:2]):
        original_preview=re.sub(r'\]\((images/[^)]+)\)',lambda m:'](/media/jake/SSD/EDB/math/'+m[1]+')',q[':question/problem'])
        review+=['## ORIGINAL '+case['source_id'],'Image references rebased for this preview; exact frozen text is in source.json.',original_preview,q[':question/worked-solution'],'## GENERATED source-mask / complete bank variant '+case['source_id'],g.markdown(v)]
    for r in records[24:]:review+=['## GENERATED '+r['question'][':question/difficulty'].split('/')[-1],g.markdown(r)]
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    counts={l:len({(b,d,k) if k else (b,k) for profile in (('easy_period',) if l=='easy' else ('method_sign_period','method_midpoint_offset')) for b,d,k in g.eligible_domain(l,profile)}) for l in ('easy','moderate','hard')}
    report={'status':'pass','provenance':g.PROVENANCE,'source_questions':12,'source_fidelity':{'exact_prompts':12,'exact_solutions':12,'complete_banks':13,'choices':65,'matched_correct_designations':12,'missing_designations_preserved':1},'source_details':fidelity,'records_checked':len(records),'independent_checks':evidence,'native_report':'engine-report.json','native_stdout':process.stdout,'meaningful_default_tasks':counts,'default_profiles_seen':sorted({r['generation']['bank_profile'] for r in records if not r['generation']['evidence_only']}),'authored_levels':['easy','hard'],'source_rasters_individually_checked':13,'concurrent_fresh_renders':'pass','limitations':['Observed distractor intent underdetermined: complete scaling-ray replay profiles are evidence-only, not learner defaults.','q-79188 raw duplicate field lacks correct designation; fidelity preserves it. Native fixtures use authoritative single-field layout, no invented original designation.','Canonical worked solution calls cotangent a tangent; retained raw source evidence, normal wording uses cotangent.'],'python':sys.version.split()[0],'sympy':sp.__version__,'freeze':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'render.py',HERE/'validate.py',HERE/'source.json',HERE/'source-cases.json',REPO/'generate/runs/current/check-engine',REPO/'generate/runs/current/check-engine.rs']}}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('status','source_fidelity','records_checked','meaningful_default_tasks','native_stdout')},indent=2))

if __name__=='__main__':main()

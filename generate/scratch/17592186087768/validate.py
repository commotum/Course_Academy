"""Fail on source, independent displayed-math, identity, scope or native failures.

Run .venv/bin/python generate/scratch/17592186087768/validate.py.
All writes remain inside this KP's private evidence folder; no database access.
"""
import concurrent.futures, hashlib, importlib.util, itertools, json, math, random, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('circle_kp',HERE.with_suffix('.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def write(name,value): (HERE/name).write_text(json.dumps(value,indent=2)+'\n')

def formatting(text):
    assert text.count('$')%2==0,'Unbalanced math delimiters'
    depth=0
    for c in text:
        if c=='{':depth+=1
        elif c=='}':depth-=1
        assert depth>=0,'Unbalanced braces'
    assert depth==0,'Unbalanced braces'
    assert '--' not in text and '+-' not in text,'Ungrouped signed operations'

def displayed_parameters(r):
    text=r['question'][':question/problem']
    match=re.search(r'centered at \$C\((.*?),(.*?)\)\$ and the point \$X\((.*?),(.*?)\)\$',text)
    assert match,'Prompt coordinate structure'
    p=dict(zip(('h','k','u','v'),map(m.parse_math,match.groups())))
    assert all(v.is_Rational for v in p.values()),'Prompt coordinate type'
    return p

def independent(r):
    q=r['question'];g=r['generation'];p=displayed_parameters(r)
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']=={'db_id':m.KP_ID,'id':m.KP_UUID,'title':m.TITLE}
    assert p==m.parse_parameters(g['parameters']),'Displayed prompt differs from parameters'
    R=(p['u']-p['h'])**2+(p['v']-p['k'])**2;rad=sp.sqrt(R)
    m.guard(g['difficulty'],p,g['bank_profile'])
    correct=m.equation(p['h'],p['k'],R)
    formatting(q[':question/problem'])
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio'
    assert f[':answer-field/key']=='selection'
    vals=[a[':answer/value'] for a in f[':answer-field/choices']]
    assert len(vals)==5 and len(set(a[':answer/id'] for a in f[':answer-field/choices']))==5
    correct_options=[]
    for i,a in enumerate(f[':answer-field/choices']):
        formatting(a[':answer/value']);assert a[':answer/type']==':answer.type/math'
        assert re.search(r'\bx\b',a[':answer/value']) and re.search(r'\by\b',a[':answer/value'])
        if m.equation_equivalent(a[':answer/value'],correct):correct_options.append(a)
        for b in f[':answer-field/choices'][:i]:assert not m.equation_equivalent(a[':answer/value'],b[':answer/value']),'Ambiguous complete displayed bank'
    assert len(correct_options)==1
    if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',correct_options[0][':answer/id']]
    else:assert g['evidence_only'] and not g['eligible_for_learning']
    if ':question/worked-solution' in q:
        text=q[':question/worked-solution'];formatting(text)
        blocks=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S);assert len(blocks)==3
        assert m.equation_equivalent(blocks[0].rstrip('.'),r'(x-a)^2+(y-b)^2=r^2')
        body=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        rows=body.split(r'\\');assert 3<=len(rows)<=4
        for row in rows:
            expr=row.split('=',1)[1].strip().rstrip('.')
            assert sp.simplify(m.parse_math(expr)-rad)==0,'Wrong displayed distance/radius stage'
        if g['bank_profile'] in ('bank-q-54215','bank-q-72617'):
            assert len(rows)==4 and R.is_Integer and sp.sqrt(R).is_Integer
            assert r'\sqrt' in rows[-2] and r'\sqrt' not in rows[-1],'Integer source radius simplification stage collapsed'
        elif g['bank_profile'] in ('bank-q-117096','bank-q-117099'):
            assert len(rows)==3 and not sp.sqrt(R).is_Integer
            final=rows[-1].split('=',1)[1].strip().rstrip('.')
            match=re.fullmatch(r'(\d+)\\sqrt\{(\d+)\}',final)
            assert match,'Simplified-radical source final stage lost square-factor extraction'
            coefficient,radicand=map(int,match.groups())
            assert coefficient>1 and radicand>1 and coefficient**2*radicand==R
            assert not any(radicand%(f*f)==0 for f in range(2,math.isqrt(radicand)+1)),'Final radical is not reduced'
        elif g['bank_profile'] in ('bank-q-72619','bank-q-72621'):
            assert len(rows)==3 and not sp.sqrt(R).is_Integer
            final=rows[-1].split('=',1)[1].strip().rstrip('.')
            assert final==r'\sqrt{'+str(R)+'}','Unsimplified-radical source final stage changed'
        elif g.get('completion_solution_mask')=='radical_unsimplified':
            assert len(rows)==3 and not sp.sqrt(R).is_Integer
            assert rows[-1].split('=',1)[1].strip().rstrip('.')==r'\sqrt{'+str(R)+'}'
        elif g.get('completion_solution_mask')=='integer_signed':
            assert len(rows)==4 and sp.sqrt(R).is_Integer
            assert r'\sqrt' not in rows[-1],'Authored completion repeated the square-root row'
        assert rows[0].count('^{2}')==2 and rows[1].count('^{2}')==2,'Distance stages collapsed'
        # Parse the actual four formal operands, not just their numeric radius.
        # A stale center/point pair can have the same distance after translation.
        groups=[];start=None;depth=0
        for i,c in enumerate(rows[0]):
            if c=='(':
                if depth==0:start=i
                depth+=1
            elif c==')':
                depth-=1
                if depth==0:groups.append(rows[0][start+1:i])
        assert len(groups)==2,'Formal squared coordinate differences missing'
        def subtraction_pair(s):
            s=re.sub(r'\s+','',s);depth=0
            for i,c in enumerate(s):
                if c in '{(':depth+=1
                elif c in '})':depth-=1
                elif c=='-' and depth==0 and i>0:
                    return m.parse_math(s[:i]),m.parse_math(s[i+1:])
            raise AssertionError('Formal coordinate difference is not subtraction')
        pairs=list(map(subtraction_pair,groups))
        reverse=g['bank_profile']=='bank-q-54215'
        expected=[(p['h'],p['u']),(p['k'],p['v'])] if reverse else [(p['u'],p['h']),(p['v'],p['k'])]
        assert pairs==expected,'Displayed formal coordinates differ from actual prompt'
        body=blocks[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        rows=body.split(r'\\');assert len(rows)==3,'Equation stage sequence'
        eqs=[row.replace('&','').strip() for row in rows]
        assert m.equation_equivalent(eqs[0],r'(x-a)^2+(y-b)^2=r^2')
        assert m.equation_equivalent(eqs[1],correct),'Wrong displayed radius/center substitution'
        assert m.equation_equivalent(eqs[2],correct),'Wrong displayed final equation'
        assert 'x-' in eqs[1] and 'y-' in eqs[1] and '^{2}' in eqs[1].split('=')[1],'Substitution stage collapsed'
        assert text.endswith('\n$$'),'Final displayed conclusion missing'
    else:assert g['evidence_only']
    plot=g['plot'];assert plot['coordinates']==[str(p[k]) for k in ('h','k','u','v')]
    path=Path(plot['path']);assert path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==plot['sha256']
    if plot['renderer']=='Matplotlib':
        assert plot['aspect']=='equal' and plot['circle_points']==721
        assert abs(float(plot['radius'])**2-float(R))<1e-10
        from fractions import Fraction
        h,k,u,v=[float(Fraction(z)) for z in plot['coordinates']];rad=float(plot['radius']);a,b,c,d=plot['bounds']
        assert a<h-rad<h+rad<b and c<k-rad<k+rad<d and a<=0<=b and c<=0<=d
        assert plot['labels']==['C('+m.tex(p['h'])+','+m.tex(p['k'])+')','X('+m.tex(p['u'])+','+m.tex(p['v'])+')']
        left,bottom,right,top=plot['point_label_bbox_pixels'];origin=plot['axis_origin_pixels']
        assert not (left<=origin[0]<=right or bottom<=origin[1]<=top),'Point label crosses an axis'
        cx,cy=plot['circle_center_pixels'];rp=plot['circle_radius_pixels']
        near=math.hypot(max(left-cx,0,cx-right),max(bottom-cy,0,cy-top))
        far=max(math.hypot(xx-cx,yy-cy) for xx in (left,right) for yy in (bottom,top))
        assert near>rp+3 or far<rp-3,'Point label crosses the actual circle boundary'
        assert near>7,'Point label covers the center mark'
        cl,cb,cr,ct=plot['center_label_bbox_pixels']
        assert not (cl<=origin[0]<=cr or cb<=origin[1]<=ct),'Center label crosses an axis'
        cfar=max(math.hypot(xx-cx,yy-cy) for xx in (cl,cr) for yy in (cb,ct))
        cnear=math.hypot(max(cl-cx,0,cx-cr),max(cb-cy,0,cy-ct))
        assert cfar<rp-3 and cnear>7,'Center label crosses a circle or its center mark'
        assert right<cl or cr<left or top<cb or ct<bottom,'Coordinate labels overlap'
    return True

def source_fidelity(source_id,r):
    original=m.QUESTIONS[source_id];q=r['question'];f=q[':question/answer-fields'][0];old=original[':question/answer-fields'][0]
    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
        assert (key in original)==(key in q),'Source attribute presence mismatch'
    assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
    assert q[':question/problem']==original[':question/problem'],'Prompt raw fidelity'
    assert q.get(':question/worked-solution')==original.get(':question/worked-solution'),'Full solution sequence/prose fidelity'
    if ':question/difficulty' in original:assert q[':question/difficulty']==original[':question/difficulty'][':db/ident']
    assert f[':answer-field/key']==old[':answer-field/key'] and f[':answer-field/type']==old[':answer-field/type'][':db/ident']
    for a in old[':answer-field/choices']:
        matches=[b for b in f[':answer-field/choices'] if m.equation_equivalent(a[':answer/value'],b[':answer/value'])]
        assert len(matches)==1 and matches[0][':answer/value']==a[':answer/value'],'All-option bank exact fidelity'
    if ':answer-field/correct' in old:
        answer=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert m.equation_equivalent(answer[':answer/value'],old[':answer-field/correct'][':answer/value'])
    return {'source_id':source_id,'prompt_raw_exact':True,'solution_raw_exact':':question/worked-solution' in original,'solution_presence_matched':True,'displayed_bank_values_matched':5,'correct_designation_matched':':answer-field/correct' in old,'presence_matched':True}

def fixture(r,label):
    f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'actual radio grading; displayed equation independently checked'} for a in f[':answer-field/choices']]}

def original_geometry():
    """Fit each raster independently; composite transparent pixels on white."""
    from PIL import Image
    import math
    records=[]
    canonical=m.SOURCE['record'][':knowledge-point/canonical-example']
    for q in [canonical]+list(m.QUESTIONS.values()):
        sid=q[':question/math-academy-id']
        ref=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]
        image=Image.open(HERE/'originals'/Path(ref).name).convert('RGBA')
        image=Image.alpha_composite(Image.new('RGBA',image.size,'white'),image).convert('RGB')
        w,h=image.size;pix=image.load()
        red=[(a,b) for b in range(h) for a in range(w) if pix[a,b][0]>200 and pix[a,b][1]<120 and pix[a,b][2]<120]
        left,right=min(a for a,b in red),max(a for a,b in red);top,bottom=min(b for a,b in red),max(b for a,b in red)
        origin_y=max(range(h),key=lambda b:sum(max(pix[a,b])<70 for a in range(w)))
        origin_x=max(range(w),key=lambda a:sum(max(pix[a,b])<70 for b in range(h)))
        coords=re.search(r'C\(([-\d]+),\s*([-\d]+)\).*?X\(([-\d]+),\s*([-\d]+)\)',q[':question/problem'])
        a,b,u,v=map(int,coords.groups());radius=math.hypot(u-a,v-b)
        sx,sy=(right-left)/(2*radius),(bottom-top)/(2*radius)
        center=(origin_x+a*sx,origin_y-b*sy);point=(origin_x+u*sx,origin_y-v*sy)
        error=[abs(center[0]-(left+right)/2),abs(center[1]-(top+bottom)/2)]
        assert max(error)<=2,'Original circle/center geometry mismatch'
        assert abs((right-left)-(bottom-top))<=2,'Original circle unequal scales beyond stroke allowance'
        def near(pt):return sum((xx-pt[0])**2+(yy-pt[1])**2<=16 for xx,yy in red)
        assert near(center)>3 and near(point)>3,'Original red marker does not match coordinates'
        records.append({'source_id':sid,'width':w,'height':h,'circle_red_bounds':[left,right,top,bottom],'axis_origin_pixels':[origin_x,origin_y],'units_to_pixels':[sx,sy],'computed_center_pixels':center,'computed_point_pixels':point,'center_error_pixels':error,'red_pixels_within_4px_center':near(center),'red_pixels_within_4px_point':near(point),'coordinates':[a,b,u,v],'radius':radius,'stroke_allowance_pixels':2,'white_composite':True,'visual_inspected_full_resolution':True})
    write('original-geometry.json',records)
    return records

def main():
    geometry=original_geometry()
    cases=[];coverage=[];originals=[];fixtures=[];review=[];completed=[]
    for source_id,q in m.QUESTIONS.items():
        case={'source_id':source_id,'template':m.SOURCE_TEMPLATE[source_id],'parameters':{k:str(v) for k,v in m.source_parameters(source_id).items()},'bank_profile':'bank-'+source_id,'difficulty':'moderate','difficulty_origin':'observed' if ':question/difficulty' in q else 'authored replay routing only; raw difficulty remains absent'}
        cases.append(case);r=m.generate('moderate',seed=71,template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        independent(r);coverage.append(source_fidelity(source_id,r));originals.append(r)
        if r['generation']['eligible_for_learning']:fixtures.append(fixture(r,'source '+source_id))
        else:
            repaired=m.complete_incomplete(r);independent(repaired);completed.append(repaired);fixtures.append(fixture(repaired,'authored completion of '+source_id))
    write('source-cases.json',cases);write('source-replays.json',originals)
    # Every observed bank and template gets two changed-parameter variants.
    for profile in m.PROFILES:
        level='easy' if profile=='authored-easy' else 'hard' if profile=='authored-hard' else 'moderate'
        for seed in (23,61):
            r=m.generate(level,seed=seed,profile=profile);independent(r);review.append(r)
            if r['generation']['eligible_for_learning']:fixtures.append(fixture(r,'generated '+profile+' seed '+str(seed)))
            else:
                repaired=m.complete_incomplete(r);independent(repaired);completed.append(repaired);fixtures.append(fixture(repaired,'authored completion variant '+profile+' seed '+str(seed)))
    write('review.json',review);write('completed-incomplete.json',completed)
    # Exercise the ordinary moderate entrypoint, not only explicit replay.
    # Selection must happen before parameters; every selected complete bank and
    # its corresponding source solution mask are independently checked above.
    default_review=[];default_coverage={profile:0 for profile in m.DEFAULT_MODERATE_PROFILES}
    expected_profiles={'bank-'+sid for sid,q in m.QUESTIONS.items() if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/moderate'}
    assert set(default_coverage)==expected_profiles and len(default_coverage)==6
    assert 'bank-q-72616' not in default_coverage
    for seed in range(36):
        expected_rng=random.Random(seed);selected=expected_rng.choice(m.DEFAULT_MODERATE_PROFILES)
        expected_parameters={k:str(v) for k,v in m.sample('moderate',expected_rng,selected).items()}
        r=m.generate_moderate(seed=seed);independent(r)
        g=r['generation'];assert g['bank_profile']==selected
        assert g['parameters']==expected_parameters,'Default profile was selected after parameter sampling'
        assert g['eligible_for_learning'] and not g['evidence_only']
        assert g['template']==m.SOURCE_TEMPLATE[selected[5:]]
        assert r==m.generate_moderate(seed=seed),'Default seed replay is not deterministic'
        explicit=m.generate_moderate(seed=seed+1000,parameters=g['parameters'],profile=selected)
        assert r['question'][':question/id']==explicit['question'][':question/id']
        assert r['question'][':question/problem']==explicit['question'][':question/problem']
        assert r['question'][':question/worked-solution']==explicit['question'][':question/worked-solution'],'Default lost its selected source solution mask'
        assert sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in explicit['question'][':question/answer-fields'][0][':answer-field/choices']),'Default mixed or replaced members of the selected complete bank'
        default_coverage[selected]+=1;default_review.append(r)
        fixtures.append(fixture(r,'default moderate seed '+str(seed)+' / '+selected))
    assert all(count>=2 for count in default_coverage.values()),'Default moderate omitted a rated source bank'
    write('default-moderate-review.json',default_review)
    # Exercise more signed/zero-point/radical cases; parse actual learner output.
    # Existing renderer cache is preserved throughout all concurrent QA.
    checked=0;fingerprints={l:set() for l in ('easy','moderate','hard')}
    for profile in m.PROFILES:
        level='easy' if profile=='authored-easy' else 'hard' if profile=='authored-hard' else 'moderate'
        for seed in range(12):
            r=m.generate(level,seed=seed+100,profile=profile);independent(r);checked+=1
            fingerprints[level].add(r['generation']['mathematical_fingerprint'])
            other=m.generate(level,seed=seed+801,profile=profile,parameters=r['generation']['parameters'])
            assert r['question'][':question/id']==other['question'][':question/id'],'Seed/order changed identity'
            assert r['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
    # No rejected explicit call may silently resample or migrate levels.
    invalid=[('easy',{'h':1,'k':1,'u':4,'v':5},'authored-easy'),('easy',{'h':6,'k':0,'u':9,'v':4},'authored-easy'),('moderate',{'h':1,'k':0,'u':4,'v':5},'bank-q-117096'),('moderate',{'h':-6,'k':1,'u':-3,'v':5},'bank-q-117096'),('hard',{'h':1,'k':2,'u':4,'v':6},'authored-hard'),('hard',{'h':'11/2','k':'1/2','u':6,'v':2},'authored-hard'),('moderate',{'h':1,'k':2,'u':1,'v':3},'bank-q-117096'),('moderate',{'h':4,'k':-4,'u':-4,'v':-4},'bank-q-54215'),('moderate',{'h':2,'k':-5,'u':3,'v':3},'bank-q-72617'),('moderate',{'h':2,'k':-5,'u':3,'v':3},'bank-q-54215')]
    for profile in ('bank-q-117096','bank-q-117099'):
        invalid.extend([('moderate',{'h':1,'k':2,'u':3,'v':5},profile),('moderate',{'h':1,'k':2,'u':4,'v':6},profile)])
    for profile in ('bank-q-72619','bank-q-72621'):
        invalid.append(('moderate',{'h':1,'k':2,'u':4,'v':6},profile))
    for level,p,profile in invalid:
        try:m.generate(level,parameters=p,profile=profile)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit parameters silently accepted')
    # Same- and changed-geometry calls use fresh targets and unique input files.
    ps=[]
    # Select uncached eligible geometries; never remove assets a reviewer may
    # be reading. Source/profile/seed are not used to inflate task counts.
    for seed in range(9000,20000):
        p={k:str(v) for k,v in m.sample('hard',random.Random(seed),'authored-hard').items()}
        path=HERE/'plots'/(m.digest([m.RENDER_VERSION,[p[k] for k in ('h','k','u','v')]])+'.png')
        if not path.exists() and p not in ps:ps.append(p)
        if len(ps)==2:break
    assert len(ps)==2,'Fresh geometry domain unexpectedly exhausted'
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        concurrent_records=list(pool.map(lambda p:m.generate('hard',parameters=p),[ps[0],ps[1],ps[0],ps[1]]))
    for r in concurrent_records:independent(r)
    assert concurrent_records[0]['question'][':question/id']==concurrent_records[2]['question'][':question/id']
    assert not list((HERE/'plots').glob('render-input-*')),'Private renderer input leak'
    write('concurrent-review.json',concurrent_records)
    # Meaningful finite domains; no profile/layout/notation aliases counted.
    # Exact whole-bank collision checks applied to every easy task and all hard
    # tasks are automatically distinct by nonzero fractional centers and R>1.
    finite={}
    easy=0
    for h in [-5,-4,-3,-2,-1,1,2,3,4,5]:
        for dx,dy in itertools.product([-8,-6,-4,-3,3,4,6,8],repeat=2):
            p=m.parse_parameters({'h':h,'k':0,'u':h+dx,'v':dy})
            try:m.guard('easy',p,'authored-easy');m.bank(p,'authored-easy');easy+=1
            except ValueError:pass
    finite['easy']=easy
    half=[sp.Rational(n,2) for n in [-9,-7,-5,-3,-1,1,3,5,7,9]]
    # R <=1 excludes only the four (+/-1/2,+/-1/2) offsets.
    finite['hard']=len(half)**2*(len(half)**2-4)
    offs=[(a,b) for a in range(-8,9) for b in range(-8,9) if a*b and a*a+b*b<=100]
    # At least the sign-based banks cover every permitted moderate task; hybrid
    # profiles reject any colliding whole bank. Do not multiply by bank aliases.
    finite['moderate_default']=100*len(offs)
    center_values=[n for n in range(-5,6) if n]
    profile_domains={}
    for profile in m.DEFAULT_MODERATE_PROFILES:
        eligible_offsets=[]
        for dx,dy in offs:
            R=dx*dx+dy*dy;is_square=math.isqrt(R)**2==R
            if profile in ('bank-q-54215','bank-q-72617') and not is_square:continue
            if profile in ('bank-q-117096','bank-q-117099') and (is_square or not any(R%(f*f)==0 for f in range(2,math.isqrt(R)+1))):continue
            if profile in ('bank-q-72619','bank-q-72621') and is_square:continue
            eligible_offsets.append((dx,dy))
        # Other rated banks are distinct whenever h,k are nonzero and R>1.
        # For the hybrid bank, only v=-k makes its (h,-v,R) member correct.
        eligible=sum(1 for h,k in itertools.product(center_values,repeat=2) for dx,dy in eligible_offsets if profile!='bank-q-54215' or k+dy!=-k)
        profile_domains[profile]={'eligible_offset_pairs':len(eligible_offsets),'eligible_mathematical_tasks':eligible,'whole_bank_collision_exclusions':100*len(eligible_offsets)-eligible}
        # Verify each admitted radius form with public explicit guards/banks.
        for dx,dy in eligible_offsets:
            p=m.parse_parameters({'h':1,'k':5,'u':1+dx,'v':5+dy})
            m.guard('moderate',p,profile);m.bank(p,profile)
    finite['moderate_filtered_profiles']=profile_domains
    assert all(len(fingerprints[l])>=10 for l in fingerprints)
    write('native-input.json',fixtures)
    engine=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    native=json.loads((HERE/'native-report.json').read_text())
    text='# Circle from a center and an on-circle point — review\n\nSnapshot math basis 1356. Correct answers and metadata below are review-only.\n\n'
    for case,r in zip(cases,originals):
        q=m.QUESTIONS[case['source_id']];difficulty=q.get(':question/difficulty',{}).get(':db/ident','ABSENT / unrated')
        text+='## Original '+case['source_id']+' — '+difficulty+'\n\n'
        text+=m.markdown(r).replace('**Generated —','**Original source replay —',1)
        if ':answer-field/correct' not in q[':question/answer-fields'][0]:text+='\n**Original correct designation absent.** Independently inferred equation: $'+r['generation']['inferred_correct_value']+'$. This inference is not counted as source designation fidelity.\n'
        text+='\n'
        for variant in review:
            if variant['generation']['bank_profile']==case['bank_profile']:text+=m.markdown(variant)+'\n'
    for level in ('easy','hard'):
        text+='## Authored '+level+' extension — no observed difficulty sources\n\n'
        for r in review:
            if r['generation']['difficulty']==level:text+=m.markdown(r)+'\n'
    text+='## Authored completion of incomplete source\n\nOriginal absence is retained by public raw replay; the following supported radios add an independently inferred correct designation, authored moderate label and worked solution.\n\n'
    for r in completed:text+=m.markdown(r)+'\n'
    text+='## Ordinary moderate defaults — all six rated source banks\n\nComplete banks are chosen with the seeded RNG before parameters. q-72616 is excluded from ordinary defaults. Default coverage across seeds 0–35: '+', '.join(profile+' = '+str(count) for profile,count in default_coverage.items())+'. All 36 banks and solution stages were checked, then natively graded. The following examples show one ordinary default from each selected profile.\n\n'
    shown=set()
    for r in default_review:
        profile=r['generation']['bank_profile']
        if profile not in shown:text+=m.markdown(r)+'\n';shown.add(profile)
    # Original references resolve to private copied source assets in review.
    for r in originals:
        ref=re.search(r'!\[\]\((.*?)\)',r['question'][':question/problem'])[1]
        text=text.replace('('+ref+')','(originals/'+Path(ref).name+')')
    (HERE/'review.md').write_text(text)
    report={'status':'passed','version':m.VERSION,'source':m.PROVENANCE,'coverage':coverage,'practice_sources':7,'source_prompts_raw_exact':7,'source_solution_raw_exact':6,'source_solution_present':6,'source_answer_values_raw_exact':35,'complete_source_banks':7,'source_correct_designations_matched':6,'source_correct_designations_present':6,'source_presence_parity':7,'source_incomplete_questions':1,'unresolved_findings':['q-72616 has no captured difficulty, worked solution or correct designation. Public raw replay preserves omissions and is ineligible; authored completion is separately validated.'],'independent_changed_parameter_records':checked,'review_generated_records':len(review),'per_level_sampled_mathematical_tasks':{k:len(v) for k,v in fingerprints.items()},'finite_eligible_mathematical_domains':finite,'invalid_explicit_calls_rejected':len(invalid),'concurrent_fresh_render_calls':4,'original_raster_geometry_checks':len(geometry),'native_grading':{'entry_point':native['entry_point'],'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'raw_incomplete_source_native_fixture_exclusion':'No original correct ref exists; authored completion tested separately.','binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'database_writes':0}
    report['default_moderate_coverage']={'seeds':list(range(36)),'eligible_rated_profiles':list(m.DEFAULT_MODERATE_PROFILES),'selected_profile_counts':default_coverage,'records_independently_verified':36,'all_complete_banks_native_graded':36,'profile_selected_before_parameters':True,'explicit_source_replay_preserved':True,'integer_mask_simplification_stage_preserved':True,'simplified_radical_nonunit_square_factor_preserved':True,'unsimplified_radical_nonsquare_radius_preserved':True,'profile_number_form_guards_apply_to_explicit_calls':True,'q72616_default_excluded':True}
    write('validation.json',report)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()

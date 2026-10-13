#!/usr/bin/env python3
"""Independent displayed mathematics, fidelity, layout, domains, identity, native QA."""
import concurrent.futures, hashlib, importlib.util, itertools,json, re, subprocess, sys,tempfile
from pathlib import Path
import sympy as sp
from PIL import Image
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('circle_given_center_radius',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def check_format(s):
    assert s.count('$')%2==0,('Unbalanced math delimiters',s)
    depth=0
    for c in s:
        if c=='{':depth+=1
        elif c=='}':depth-=1
        assert depth>=0,('Unbalanced groups',s)
    assert depth==0,('Unbalanced groups',s)
    assert not re.search(r'(?<!\\)\\\\(?:sqrt|frac|begin|end)',s)
    assert '--' not in s and '+-' not in s

def independent_from_display(r):
    q=r['question'];meta=r['generation'];p=meta['parameters']
    underdefined=meta['raw_evidence_only'] and meta['source_id']=='q-167932'
    if underdefined:
        # Raw prompt has no inputs; only its independently read solution values
        # can establish the answer/teaching arithmetic. Never count prompt math.
        sol=q[':question/worked-solution']
        center=re.search(r'circle is centered at \$\((.*?)\)\$',sol)[1]
        h,k=(g.parse_expr(v) for v in center.split(','))
        radius=g.parse_expr(re.search(r'r=(.*?)\$',sol)[1].rstrip('.'))
    else:
        plot=meta['plot'];image=re.search(r'!\[\]\(([^)]+)\)',q[':question/problem'])[1]
        if plot['renderer']=='matplotlib':
            side=json.loads(Path(image).with_suffix('.json').read_text())
            # Printed diagram labels originate in the stored actual render input.
            # Source raster fit and visual inspection are separately recorded below.
            assert side['parameters']==p
            h,k,radius=(g.exact(side['parameters'][a]) for a in ('h','k','r'))
            assert side['equal_aspect']
            assert abs(side['radius']-float(radius))<1e-10
            endpoint=side['radius_endpoint'];expected=(float(h+radius),float(k)) if p['orientation']=='horizontal' else (float(h),float(k+radius))
            assert max(abs(a-b) for a,b in zip(endpoint,expected))<1e-10
            assert all(a<float(h)-float(radius)<float(h)+float(radius)<b for a,b in [side['xlim']])
            assert all(a<float(k)-float(radius)<float(k)+float(radius)<b for a,b in [side['ylim']])
            im=Image.open(image).convert('RGB');reds=[(x,y) for y in range(im.height) for x in range(im.width) if (lambda c:c[0]>210 and c[1]<100 and c[2]<100)(im.getpixel((x,y)))]
            assert reds,'Circle raster missing'
            width=max(x for x,y in reds)-min(x for x,y in reds);height=max(y for x,y in reds)-min(y for x,y in reds)
            assert abs(width-height)<=5,'Unequal-scale circle raster'
        else:
            assert Path(plot['absolute_path']).exists()
            assert hashlib.sha256(Path(plot['absolute_path']).read_bytes()).hexdigest()==plot['sha256']
            h,k,radius=(g.exact(a) for a in [p['h'],p['k'],p['r']])
    expected=(g.X-h)**2+(g.Y-k)**2-radius**2
    field=q[':question/answer-fields'][0]
    values=[a[':answer/value'] for a in field[':answer-field/choices']]
    correct=[a for a in field[':answer-field/choices'] if ':answer-field/correct' in field and a[':answer/id']==field[':answer-field/correct'][1]]
    if correct:assert sp.expand(g.polynomial(correct[0][':answer/value']).as_expr()-expected)==0
    assert sum(sp.expand(g.polynomial(v).as_expr()-expected)==0 for v in values)==1
    assert len({sp.srepr(g.polynomial(v).monic().as_expr()) for v in values})==len(values)
    operation_values={'h':h,'k':k,'-h':-h,'-k':-k,'zero':sp.Integer(0),'r':radius,'r2':radius**2,'sqrt_r':sp.sqrt(radius)}
    operation_polys=[sp.expand((g.X-operation_values[a])**2+(g.Y-operation_values[b])**2-operation_values[c]) for a,b,c in meta['recipe_bank']]
    assert all(sum(sp.expand(g.polynomial(v).as_expr()-op)==0 for op in operation_polys)==1 for v in values)
    sol=q.get(':question/worked-solution')
    if sol:
        check_format(sol)
        center=re.search(r'(?:centered at \$C|circle is centered at \$)\((.*?)\)\$',sol)
        assert center
        ch,ck=center[1].split(',');assert g.parse_expr(ch)==h and g.parse_expr(ck)==k
        rr=re.search(r'r=(.*?)\$',sol)[1].rstrip('.');assert g.parse_expr(rr)==radius
        rows=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1].split(r'\\')
        assert len(rows)==3
        assert rows[0].strip()=='(x-a)^{2}+(y-b)^{2} & ={r}^{2}'
        for row in rows[1:]:assert sp.expand(g.polynomial(row.replace('&','').strip().rstrip('.')).as_expr()-expected)==0
        # Preserve unevaluated squared radius and both center substitutions.
        assert rows[1].split('&')[0].count('^{2}')==2
        rhs=rows[1].split('=')[1].strip();assert rhs.endswith('^{2}')
        if field[':answer-field/type'].endswith('/blank'):
            final=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)[-1].rstrip('.');assert sp.expand(g.polynomial(final).as_expr()-expected)==0
    check_format(q[':question/problem'])
    for v in values:check_format(v)
    return {'correct_math':True,'rows_checked':2 if sol else 0,'underdefined_source_prompt':underdefined}

def native_cases(records):
    cases=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0]
        if ':answer-field/correct' not in f:continue
        correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        checks=[]
        if f[':answer-field/type'].endswith('/radio'):
            checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a==correct else 'rejected','purpose':'Every owned displayed radio option'} for a in f[':answer-field/choices']]
        else:
            eq=correct[':answer/value'];poly=g.polynomial(eq).as_expr()
            expanded=g.tex(sp.expand(poly))+'=0'
            scalar=g.tex(3*sp.expand(poly))+'=0'
            checks=[{'submitted':eq,'expected':'unresolved','purpose':'Canonical full equation'},{'submitted':expanded,'expected':'unresolved','purpose':'Expanded equivalent complete equation'},{'submitted':scalar,'expected':'unresolved','purpose':'Nonzero scalar equivalent complete equation'},{'submitted':eq.split('=')[0]+'=0','expected':'unresolved','purpose':'Wrong squared radius'},{'submitted':eq.split('=')[1],'expected':'unresolved','purpose':'Scalar alone is not the requested full equation'}]
        cases.append({'label':f'instance-{i}-{r["generation"]["bank_profile"]}','record':r,'checks':checks})
    return cases

def source_raster_checks():
    # Pixel origin fitted separately for each displayed graph. Red marker/circle
    # extents compared under that graph's own scale; 3px accounts for strokes.
    fits={'q-54187':(134,271,36,169,163,108),'q-54210':(213,242,17.57,178,154,123),'q-116929':(226,129,14,169,171,84),'q-117077':(128,112,21,169,175,84),'q-117081':(230,163,12,169,163,84),'q-70896':(132,220,25,157,170,125),'q-70898':(199,125,14.875,169,170,119)}
    results=[]
    for sid,(ox,oy,s,cx,cy,rpx) in fits.items():
        q=g.QUESTIONS[sid];img=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1];path=Path('/media/jake/SSD/EDB/math')/img
        im=Image.open(path).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB')
        red=[(x,y) for y in range(im.height) for x in range(im.width) if (lambda c:c[0]>230 and c[1]<80 and c[2]<80)(im.getpixel((x,y)))]
        p=g.ORIGINAL[sid]
        assert abs(cx-(ox+s*p['h']))<=3 and abs(cy-(oy-s*p['k']))<=3
        for measured,expected in [(min(x for x,y in red),cx-rpx),(max(x for x,y in red),cx+rpx),(min(y for x,y in red),cy-rpx),(max(y for x,y in red),cy+rpx)]:assert abs(measured-expected)<=3
        assert abs(rpx-s*p['r'])<=3
        results.append({'source_id':sid,'asset':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':im.size,'axis_origin_px':[ox,oy],'scale_px_per_unit':s,'center_px':[cx,cy],'radius_px':rpx,'label_inspection':'Center tuple and radius read visually at original resolution; horizontal/vertical blue radius endpoint verified.','passed':True})
    return results

def run():
    source_cases=json.loads((HERE/'source-cases.json').read_text());records=[];fidelity=[]
    for case in source_cases:
        sid=case['source_id'];q=g.QUESTIONS[sid];r=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);new=r['question'];f=new[':question/answer-fields'][0];old=q[':question/answer-fields'][0]
        # Presence parity excludes database/source IDs from local generated IDs.
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in new)==(key in q),(sid,key)
        assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
        assert new[':question/problem']==q[':question/problem']
        assert new.get(':question/worked-solution')==q.get(':question/worked-solution')
        assert f[':answer-field/type']==old[':answer-field/type'][':db/ident'] and f[':answer-field/key']==old[':answer-field/key']
        source_values=[a[':answer/value'] for a in old[':answer-field/choices']];new_values=[a[':answer/value'] for a in f[':answer-field/choices']]
        assert sorted(source_values)==sorted(new_values)
        assert all(sum(g.equivalent(a,b) for b in new_values)==1 for a in source_values)
        if ':answer-field/correct' in old:
            value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert g.equivalent(value,old[':answer-field/correct'][':answer/value'])
        independent_from_display(r);records.append(r)
        fidelity.append({'source_id':sid,'bank_values_exact':len(source_values),'complete_bank':True,'correct_designation_matched':':answer-field/correct' in old,'prompt_exact':True,'solution_exact':':question/worked-solution' in q,'presence_exact':True})
    for level in ('easy','moderate','hard'):
        for seed in range(12):
            for kind in ('radio','blank'):
                r=g.generate(level,seed=seed,field_type=kind);independent_from_display(r);records.append(r)
    # Changed source profiles, signed/axis cases, and an algebraic distractor at
    # the admitted boundary r=2; each complete original bank is exercised.
    for sid in g.QUESTIONS:
        r=g.generate('easy',seed=123,profile='raw:'+sid);independent_from_display(r);records.append(r)
        c=g.generate('easy',seed=321,profile='completed:'+sid);independent_from_display(c);records.append(c)
    boundary=g.generate('easy',profile='q-116929',parameters={'h':-3,'k':-2,'r':2,'orientation':'horizontal'});independent_from_display(boundary);records.append(boundary)
    # Full-equation scalar equality, including all algebraic bank coefficients.
    assert g.equivalent('(x+3)^2+(y+2)^2=2','3*(x+3)^2+3*(y+2)^2=6')
    assert not g.equivalent('(x+3)^2+(y+2)^2=2','(x+3)^2+(y+2)^2=sqrt(2)')
    for level,p in [('easy',{'h':0,'k':1,'r':3,'orientation':'horizontal'}),('moderate',{'h':1,'k':-2,'r':3,'orientation':'horizontal'}),('moderate',{'h':-7,'k':1,'r':'3/2','orientation':'horizontal'}),('hard',{'h':1,'k':'-3/2','r':'3/2','orientation':'horizontal'}),('hard',{'h':'3/2','k':'5/2','r':'3/2','orientation':'horizontal'}),('hard',{'h':'-25/4','k':'3/2','r':'3/2','orientation':'horizontal'})]:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('Invalid level boundaries',level,p))
    try:g.generate('easy',profile='q-70896',parameters={'h':2,'k':2,'r':3,'orientation':'horizontal'})
    except ValueError:pass
    else:raise AssertionError('Swapped-center full-bank collision not rejected')
    for r in records:
        assert set(r)=={'knowledge_point','question','generation'}
        assert set(r['knowledge_point'])=={'db_id','id','title'}
        q=r['question'];field=q[':question/answer-fields'][0]
        ids=[q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in field[':answer-field/choices']]
        import uuid
        for val in ids:uuid.UUID(val)
        if field[':answer-field/type'].endswith('/blank'):assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
    r=g.generate('hard',seed=0);a=g.generate('hard',seed=600,parameters=r['generation']['parameters']);assert r['question'][':question/id']==a['question'][':question/id']
    b=g.generate('hard',seed=2,parameters=r['generation']['parameters'],field_type='blank');assert r['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and r['question'][':question/id']!=b['question'][':question/id']
    placements={next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in records if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio') and ':answer-field/correct' in r['question'][':question/answer-fields'][0]};assert len(placements)>1
    # Fresh concurrent rendering for same and different geometry; own temp files.
    p1={'h':'-7/3','k':'5/4','r':'11/4','orientation':'horizontal'};p2={'h':'7/3','k':'-5/4','r':'11/4','orientation':'vertical'}
    def call(p):return g.generate('hard',parameters=p)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:concurrent_records=list(pool.map(call,[p1,p1,p2]))
    assert concurrent_records[0]['question'][':question/id']==concurrent_records[1]['question'][':question/id'] and concurrent_records[0]['question'][':question/id']!=concurrent_records[2]['question'][':question/id']
    for r in concurrent_records:independent_from_display(r)
    fresh_dir=Path(tempfile.mkdtemp(prefix='concurrency-',dir=HERE/'plots'))
    def fresh(p):return g.render_plots({k:g.exact(v) if k!='orientation' else v for k,v in p.items()},output_dir=fresh_dir)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:fresh_outputs=list(pool.map(fresh,[p1,p1,p2]))
    assert fresh_outputs[0][0]==fresh_outputs[1][0] and fresh_outputs[0][0]!=fresh_outputs[2][0]
    for output,side in fresh_outputs:
        assert Path(output).exists() and json.loads(Path(output).with_suffix('.json').read_text())==side
    assert fresh_outputs[0][1]['parameters']==p1 and fresh_outputs[2][1]['parameters']==p2
    assert not list(fresh_dir.glob('render-input-*'))
    (HERE/'engine-input.json').write_text(json.dumps(native_cases(records),indent=2)+'\n')
    engine=HERE.parents[1]/'runs/current/check-engine';proc=subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);(HERE/'engine.log').write_text(proc.stdout+proc.stderr);assert proc.returncode==0,proc.stdout+proc.stderr
    engine_report=json.loads((HERE/'engine-report.json').read_text())
    for native_record in engine_report['records']:
        for check in native_record['checks']:
            if check['outcome']=='unresolved':assert check['reason']=='unconsumed mathematical notation',check
    for r in records:
        meta=r['generation'];f=r['question'][':question/answer-fields'][0]
        if f[':answer-field/type'].endswith('/blank'):
            assert meta['evidence_only'] and not meta['eligible_for_learning'] and not meta['grading_compatibility']['supported']
        elif meta['eligible_for_learning']:assert meta['grading_compatibility']['supported']
    report={'passed':True,'eligible_native_grading_passed':True,'native_support_complete':False,'fidelity_passed':True,'mathematics_passed':True,'native_radio_passed':True,'native_blank_passed':False,'native_blocker':'The real engine symbolic grader cannot parse full-equation blank canonical or learner values (unconsumed mathematical notation); no source-shape-preserving generator repair exists. Blank records are ineligible for learning; radio defaults for all levels grade correctly.','version':g.VERSION,'source_provenance':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_questions':8,'source_bank_values':36,'complete_source_banks':8,'correct_designations':{'matched':6,'present':6,'absent':2},'difficulty_presence':{'rated_easy':6,'unrated_raw':2},'source_prompt_exact':8,'source_solution_exact':{'matched':6,'present':6,'absent':2},'source_presence_parity':8,'fidelity':fidelity,'source_raster_checks':source_raster_checks(),'normal_records_checked':len(records)-8,'generated_levels':['easy','moderate','hard'],'authored_levels':['moderate','hard'],'source_format_anomalies':['q-167932 missing diagram: raw replay evidence-only; completed profile restores parameterized diagram.','q-54187/q-54210 missing difficulty/solution/correct refs: raw replay omits; completed profile labels inferred correct and solution.'],'native':engine_report,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'meaningful_task_counts':{'easy_default':16*16*8,'moderate_default':json.loads((HERE/'capabilities.json').read_text())['moderate'],'hard_default':json.loads((HERE/'capabilities.json').read_text())['hard']},'limitations':['No original raster/authoritative widget available for stripped q-167932 diagram; center/radius independently follow source solution and answer.','Authored rational difficulty is a design claim; source has only easy labels.','Full-equation blank native grading is unsupported; preserved blank review records remain ineligible for learning.']}
    report.update({'generated_records_checked':89,'authored_radio_defaults_checked':36,'authored_blank_drafts_checked':36,'source_bank_variants_checked':16,'additional_boundary_cases':1,'raw_source_prompt_usable':{'usable':7,'total':8,'underdefined_evidence_only':1}})
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('passed','fidelity_passed','mathematics_passed','native_radio_passed','native_blank_passed','source_questions','source_bank_values','complete_source_banks','normal_records_checked')},indent=2))

if __name__=='__main__':run()

"""Independent displayed-statement/PNG/prose checks; native grading kept separate."""
import concurrent.futures, hashlib, importlib.util, itertools, json, re, subprocess, sys
from fractions import Fraction
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ROOT=HERE.parents[2]

def check(condition,message):
    if not condition:raise AssertionError(message)
def write(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def latex_rat(s):
    s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',s)
    return sp.Rational(s or '1')
def parse_equation(text):
    match=re.fullmatch(r'([a-e])=([+-]?(?:\d+(?:/\d+)?)?)([a-e])',re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',text.replace(' ','')))
    check(match is not None,'Unparseable displayed relation '+text)
    a,k,b=match.groups();return a,sp.Rational('-1' if k=='-' else '1' if k in ('','+') else k),b

def math_check(r,raster):
    q=r['question'];gen=r['generation'];field=q[':question/answer-fields'][0]
    st=[parse_equation(x) for x in re.findall(r'^\d\. \$(.*?)\$',q[':question/problem'],re.M)]
    check(len(st)==3,'Exactly three displayed statements')
    # Displacements are re-read from actual PNG endpoints snapped to its square grid.
    vectors={label:[sp.Integer(a['recovered_tip_grid'][j]-a['recovered_tail_grid'][j]) for j in (0,1)] for label,a in raster['arrows'].items()}
    true=frozenset(i for i,(a,k,b) in enumerate(st) if all(vectors[a][j]==k*vectors[b][j] for j in (0,1)))
    options=[g.parse_subset(a[':answer/value']) for a in field[':answer-field/choices']]
    check(len(options)==5 and len(set(options))==5,'Five semantically different subsets')
    check(options.count(true)==1,'Actual PNG/request criterion has one valid option')
    check(g.parse_subset(gen['correct_inference'])==true,'Inference versus displayed geometry')
    check(raster['equal_physical_scale'],'Equal physical grid scale')
    if gen['plot'].get('labels'):
        check(set(raster['labels'])==set('abcde'),'All five actual PNG labels checked')
        check(all(v['blue_pixels_within_bbox_and_3px_margin']==0 and v['black_text_pixels']>=5 and v['association_distance_grid']<=.9 for v in raster['labels'].values()),'Actual PNG text clearance and close association')
    check(set(r['knowledge_point'])=={'db_id','id','title'},'Knowledge point outer shape')
    check(field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection','Observed radio layout')
    check(all(a[':answer/type']==':answer.type/text' for a in field[':answer-field/choices']),'Observed answer type')
    if gen['evidence_only']:
        check(not gen['eligible_for_learning'],'Raw evidence must stay ineligible')
        check(':answer-field/correct' not in field and ':question/difficulty' not in q and ':question/worked-solution' not in q,'Absent original attributes must remain absent')
    else:
        owned={a[':answer/id']:a for a in field[':answer-field/choices']}
        ref=field[':answer-field/correct'];check(ref[0]==':answer/id' and ref[1] in owned,'Correct UUID belongs to field')
        check(g.parse_subset(owned[ref[1]][':answer/value'])==true,'Correct native selection versus mathematical answer')
        sol=q[':question/worked-solution']
        bullets=re.findall(r'^- Statement (I|II|III) is (true|false)\.',sol,re.M)
        check(bullets==[(g.ROMAN[i],'true' if i in true else 'false') for i in range(3)],'Worked statements/conclusion reflect rendered prompt')
        for a,value,b in re.findall(r'The magnitude of \$([a-e])\$ is \$(.*?)\$ times the magnitude of \$([a-e])\$',sol,flags=re.I):
            actual=sp.sqrt(sum(x*x for x in vectors[a]))/sp.sqrt(sum(x*x for x in vectors[b]));check(sp.simplify(actual-latex_rat(value))==0,'Displayed magnitude ratio')
        for a,b,wording in re.findall(r'[Vv]ectors \$([a-e])\$ and \$([a-e])\$ (?:are parallel and )?have (the same direction|opposite directions)',sol):
            dot=sum(vectors[a][j]*vectors[b][j] for j in (0,1));check((dot>0)==(wording=='the same direction'),'Displayed direction prose')
        for i,bullet in enumerate(sol.split('\n\n')[0].split('\n')):
            final=re.findall(r'\$([^$]*(?:=|\\neq)[^$]*)\$',bullet)[-1]
            expr=final.replace(r'\neq','=');check(parse_equation(expr)==st[i],'Solution conclusion uses actual statement slots')
        if len(true)==1:expected=f'Therefore, only statement {g.ROMAN[next(iter(true))]} is true.'
        elif len(true)==2:expected='Therefore, only statements '+' and '.join(g.ROMAN[i] for i in sorted(true))+' are true.'
        elif len(true)==3:expected='Therefore, all three statements are true.'
        else:expected='Therefore, none of the statements are true.'
        check(sol.endswith(expected),'Final true-subset prose')
    text=q[':question/problem']+q.get(':question/worked-solution','')
    check(text.count('$')%2==0 and text.count('{')==text.count('}'),'Math delimiter/group balance')
    ids=[q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in field[':answer-field/choices']]
    import uuid
    for x in ids:uuid.UUID(x)
    check(len(set(ids))==len(ids),'Unique owned IDs')
    check(field[':answer-field/id']==g.owned(q[':question/id'],'selection'),'Field UUID owned by question')
    check(all(a[':answer/id']==g.owned(field[':answer-field/id'],a[':answer/value']) for a in field[':answer-field/choices']),'Answer UUIDs owned by their field')
    return {'true_subset':g.subset_text(true),'vectors_read_from_png':{k:[str(x) for x in v] for k,v in vectors.items()}}

def enumerate_tasks():
    simple=[(1,0),(0,1),(1,1),(1,-1),(-1,0),(0,-1),(-1,-1),(-1,1)]
    dirs=[(1,2),(2,1),(1,-2),(2,-1),(-1,2),(-2,1),(-1,-2),(-2,-1),(2,3),(3,2),(2,-3),(3,-2),(-2,3),(-3,2),(-2,-3),(-3,-2)]
    counts={}
    for level in ('easy','moderate','hard'):
        level_counts={}
        for template in (g.TEMPLATES[:1] if level=='easy' else g.TEMPLATES):
            profile='observed-a-completed' if template==g.TEMPLATES[0] else 'observed-b-completed';seen=set()
            ks=[sp.Rational(1)] if level=='easy' else [sp.Rational(2)] if level=='moderate' else [sp.Rational(3,2),sp.Rational(2,3)]
            for k in ks:
                us=[[2*x for x in d] for d in simple] if level=='easy' else dirs if level=='moderate' else [[(2 if k==sp.Rational(3,2) else 3)*x for x in d] for d in dirs[:8]]
                vs=[[2*x for x in d] for d in simple] if level=='easy' else dirs+[(2,5),(5,2),(-3,-5),(3,5),(0,3),(3,0)]
                for u,v,s,t in itertools.product(us,vs,(-1,1),(-1,1)):
                    try:
                        p=g.normalize_parameters(level,template,dict(u=u,v=v,k=str(k),s=s,t=t));vectors,st=g.vectors_and_statements(template,p);true=g.truth_set(vectors,st);g.bank_values(profile,true)
                    except ValueError:continue
                    seen.add(g.canonical([template,str(k),s,t,g.primitive(p['u']),g.primitive(p['v'])]))
            level_counts[template]=len(seen)
        counts[level]=level_counts
    return counts

def main():
    original_audit=HERE/'original-audit-input.json'
    subprocess.run([g.RUNTIME,str(HERE/'render_plot.py'),str(original_audit)],check=True,capture_output=True)
    original_geometry=json.loads((HERE/'original-geometry.json').read_text())
    source=json.loads((HERE/'source.json').read_text())['record']
    raws=[];completed=[];fidelity=[]
    for case,original in zip(g.SOURCE_CASES,source[':knowledge-point/questions']):
        raw=g.generate(case['level'],11,case['template'],parameters=case['parameters'],profile=case['bank_profile']);raws.append(raw)
        q=raw['question'];f=q[':question/answer-fields'][0];original_f=original[':question/answer-fields'][0]
        check(q[':question/problem']==original[':question/problem'],'Exact source prompt/asset spelling')
        check(sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original_f[':answer-field/choices']),'Complete original source bank')
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):check((key in q)==(key in original),'Original attribute-presence parity '+key)
        check((':answer-field/correct' in f)==(':answer-field/correct' in original_f),'Original correct absence parity')
        profile='observed-a-completed' if case['template']==g.TEMPLATES[0] else 'observed-b-completed'
        completed.append(g.generate(case['level'],11,case['template'],parameters=case['parameters'],profile=profile))
        fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'bank_matched':5,'bank_total':5,'layout_exact':True,'absent_attributes_preserved':True,'original_correct_designation_present':False,'inferred_answer':raw['generation']['correct_inference'],'solution_original_present':False})
    review=[]
    for level in ('easy','moderate','hard'):
        for i in range(2):
            template=g.TEMPLATES[0] if level=='easy' else g.TEMPLATES[i]
            review.append(g.generate(level,30+i,template))
    review.append(g.generate('easy',44,g.TEMPLATES[0],profile='authored-selection-flips'))
    review.append(g.generate('moderate',44,g.TEMPLATES[0],profile='authored-selection-flips'))
    review.append(g.generate('hard',44,g.TEMPLATES[1],profile='authored-selection-flips'))
    qa=[]
    for level in ('easy','moderate','hard'):
        for seed in range(18):
            record=g.generate(level,seed);qa.append(record)
            explicit=g.generate(level,1000+seed,record['generation']['template'],parameters=record['generation']['parameters'],profile=record['generation']['bank_profile'])
            check(explicit['question'][':question/id']==record['question'][':question/id'],'Default/explicit same parameters identity')
    regressions=[]
    for level in ('easy','moderate','hard'):
        for template in (g.TEMPLATES[:1] if level=='easy' else g.TEMPLATES):
            for seed in (0,17):
                record=g.generate(level,seed,template);regressions.append(record)
                explicit=g.generate(level,1234,template,parameters=record['generation']['parameters'],profile=record['generation']['bank_profile'])
                check(explicit['question'][':question/id']==record['question'][':question/id'],'Explicit replay for every level/family')
    for level,inputs in [
        ('easy',[dict(u=[-2,2],v=[0,-2],k='1',s=1,t=-1),dict(u=[2,0],v=[-2,-2],k='1',s=-1,t=1)]),
        ('moderate',[dict(u=[-3,2],v=[5,2],k='2',s=-1,t=-1),dict(u=[3,-2],v=[-3,-5],k='2',s=-1,t=1)]),
        ('hard',[dict(u=[-4,2],v=[5,-2],k='3/2',s=-1,t=-1),dict(u=[6,-3],v=[-3,-5],k='2/3',s=-1,t=1)])]:
        for template in (g.TEMPLATES[:1] if level=='easy' else g.TEMPLATES):
            for params in inputs:regressions.append(g.generate(level,0,template,parameters=params))
    write('regression-records.json',regressions)
    records=raws+completed+review+qa+regressions
    write('review.json',raws+completed+review)
    request=[]
    for r in records:
        gen=r['generation'];plot=gen['plot'];path=plot.get('source_asset') or r['question'][':question/problem'].split('![](')[1].split(')')[0]
        if 'source_asset' in plot:
            source_id=g.match_original(gen['template'],g.normalize_parameters('moderate',gen['template'],gen['parameters'],True))['source_id'];transform=original_geometry[source_id]['transform']
        else:transform=plot['transform']
        request.append({'id':r['question'][':question/id'],'path':path,'geometry':gen['geometry'],'transform':transform,'labels':gen['plot'].get('labels')})
    write('raster-audit-input.json',{'audit_existing':True,'records':request,'output':str(HERE/'raster-validation.json')})
    subprocess.run([g.RUNTIME,str(HERE/'render_plot.py'),str(HERE/'raster-audit-input.json')],check=True,capture_output=True)
    raster=json.loads((HERE/'raster-validation.json').read_text());math_results=[]
    for r in records:math_results.append(math_check(r,raster[r['question'][':question/id']]))
    # Seed/order independence and separation of presentation from mathematical task IDs.
    for r in review:
        gen=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
        changed=g.generate(level,999,gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
        check(changed['question'][':question/id']==r['question'][':question/id'],'Seed/order stable identity')
        check(changed['question'][':question/worked-solution']==r['question'][':question/worked-solution'],'One fixed solution independent of options')
    r=review[0];p=dict(r['generation']['parameters']);vs,_=g.vectors_and_statements(g.TEMPLATES[0],g.normalize_parameters('easy',g.TEMPLATES[0],p));geom=r['generation']['geometry'];p['tails']={x:[str(sp.Rational(z)+1) for z in geom[x]['tail']] for x in geom}
    translated=g.generate('easy',999,g.TEMPLATES[0],parameters=p)
    check(translated['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'],'Translation cannot create a mathematical task')
    check(translated['question'][':question/id']!=r['question'][':question/id'],'Changed actual diagram changes presentation identity')
    for level,k in [('easy','2'),('moderate','3/2'),('hard','2')]:
        try:g.generate(level,parameters=dict(u=[2,1],v=[1,2],k=k,s=-1,t=-1))
        except ValueError:pass
        else:raise AssertionError('Explicit workload boundary bypass '+level)
    # Fresh atomic writes under simultaneous identical and different geometries.
    selected=review[:2]+review[2:3]
    geometries=[selected[0]['generation']['geometry'],selected[0]['generation']['geometry'],selected[1]['generation']['geometry'],selected[2]['generation']['geometry']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:concurrent_results=list(pool.map(lambda geo:g.render_plots(geo,force=True),geometries))
    check(concurrent_results[0][0]==concurrent_results[1][0] and concurrent_results[0][1]['png_sha256']==concurrent_results[1][1]['png_sha256'],'Concurrent identical deterministic PNGs')
    check(len({x[0] for x in concurrent_results})==3,'Concurrent different instances remain separate')
    check(not list((HERE/'plots').glob('.render-*.json')) and not list((HERE/'plots').glob('.png-*.png')) and not list((HERE/'plots').glob('.atomic-*.json')),'Private render input/atomic cleanup')
    positions={next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in completed+review+qa+regressions}
    check(len(positions)>=3,'Correct choice must not always be first')
    native=[]
    for i,r in enumerate(completed+review+qa+regressions):
        f=r['question'][':question/answer-fields'][0]
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio selection; mathematics independently checked from statements and PNG'} for a in f[':answer-field/choices']]
        native.append({'label':f'{i}:{r["generation"]["template"]}', 'record':r,'checks':checks})
    write('native-input.json',native)
    engine=ROOT/'generate/runs/current/check-engine'
    result=subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],capture_output=True,text=True)
    check(result.returncode==0,'Native grader failure: '+result.stderr+result.stdout)
    counts=enumerate_tasks()
    check(counts['easy'][g.TEMPLATES[0]]>=100 and sum(counts['moderate'].values())>=1000 and sum(counts['hard'].values())>=1000,'Meaningful finite variety')
    coverage={level:sorted({r['generation']['template'] for r in qa if r['question'][':question/difficulty'].endswith('/'+level)}) for level in counts}
    check(coverage['moderate']==list(g.TEMPLATES) and coverage['hard']==list(g.TEMPLATES),'Default family coverage')
    review_md=['# Identifying Parallel Vectors From a Diagram — review','Source: math, basis 1356. Practice sources are unrated. All displayed easy/moderate/hard labels and completed solutions are authored. Raw evidence preserves the missing key and solution; inferred answers are separately labeled.','## Original canonical example (not practice)',source[':knowledge-point/canonical-example'][':question/problem'].replace('![](images/','![](/media/jake/SSD/EDB/math/images/'),source[':knowledge-point/canonical-example'][':question/worked-solution']]
    for index,r in enumerate(raws+completed+review):
        exported=g.markdown(r)
        if index<2:title='## Original raw evidence '+g.SOURCE_CASES[index]['source_id']+' — unrated, original key/solution absent'
        elif index<4:title='## Completed original '+g.SOURCE_CASES[index-2]['source_id']+' — authored moderate; inferred key and authored solution'
        else:title='## Generated variant — authored '+r['question'][':question/difficulty'].split('/')[-1]+(' — authored bank extension' if r['generation']['bank_profile']=='authored-selection-flips' else ' — observed complete bank')
        exported=title+'\n'+exported.split('\n',1)[1]
        if r['generation']['plot'].get('source_asset'):
            ref=r['question'][':question/problem'].split('![](')[1].split(')')[0]
            exported=exported.replace('![]('+ref+')','![]('+r['generation']['plot']['source_asset']+')')
        review_md.append(exported)
    (HERE/'review.md').write_text('\n\n'.join(review_md)+'\n')
    write('validation.json',{'status':'passed','source':g.SOURCE,'source_fidelity':{'practice_questions':2,'exact_prompts':2,'complete_banks':'2/2','displayed_choices':'10/10','attribute_omissions_preserved':'2/2','original_correct_designations':'0 present; 2 absent; neither counted as matched','original_worked_solutions':'0 present; 2 absent','independently_inferred_keys':'2/2','canonical_raster_arrows':'5/5','practice_raster_arrows':'10/10','details':fidelity},'default_seed_regression':{'seeds':'0–17 inclusive','levels':['easy','moderate','hard'],'records':54,'same_parameters_explicit_replays':54,'family_and_boundary_regressions':len(regressions)},'label_regression_fix':'Measure actual shaft and closed triangle; exclude CLOSEPOLY dummy. Choose nearest local clear text bbox with stroke allowance; verify actual PNG blue-free 3px clearance.','independent_math_records':len(records),'actual_png_records':len(records),'actual_png_arrows':len(records)*5,'native':{'records':len(native),'checks':len(native)*5,'unresolved':0,'engine_sha256':g.file_hash(engine),'engine_source_sha256':g.file_hash(engine.with_suffix('.rs'))},'finite_meaningful_task_counts':counts,'default_template_coverage':coverage,'correct_choice_positions':sorted(positions),'fresh_concurrent_renders':4,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'authored_extensions':{'easy':'unit equality/sign, opposite_multiple only','moderate':'factor2/reciprocal, both source masks','hard':'3:2/2:3, both source masks','bank':'selection-flip profile'},'scope':'No zero arrows; actual lesson includes antiparallel and zero convention; no arithmetic beyond direction and magnitude ratios','source_errors':[],'unresolved_findings':[]})
    frozen={'version':g.VERSION,'generator_sha256':g.file_hash(HERE.with_suffix('.py')),'renderer_sha256':g.file_hash(HERE/'render_plot.py'),'validator_sha256':g.file_hash(HERE/'validate.py'),'source_sha256':g.file_hash(HERE/'source.json'),'dependency_lock_sha256':g.file_hash(HERE/'dependency-lock.json'),'runtime_sha256':g.file_hash(g.RUNTIME),'validation_sha256':g.file_hash(HERE/'validation.json')};write('freeze.json',frozen)
    print(json.dumps({'status':'passed','source_banks':'2/2','choices':'10/10','native_checks':len(native)*5,'math_records':len(records),'variety':counts},indent=2))
if __name__=='__main__':main()

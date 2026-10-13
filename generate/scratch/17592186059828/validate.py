"""Independent displayed-interval, raster, fidelity, catalog and native grading QA."""
import concurrent.futures,copy,hashlib,importlib.util,json,re,subprocess,tempfile
from fractions import Fraction
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def require(ok,why):
    if not ok:raise AssertionError(why)
def load(name):return json.loads((HERE/name).read_text())
def save(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def failure(fn):
    try:fn()
    except (AssertionError,ValueError):return
    raise AssertionError('Negative control did not fail')
def parse_number(s):
    s=s.strip().replace(' ','').replace('−','-')
    if s in ('-∞',r'-\infty'):return -sp.oo
    if s in ('∞',r'\infty'):return sp.oo
    s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',s)
    require(bool(re.fullmatch(r'-?\d+(?:/\d+)?',s)),'Displayed scalar malformed '+s)
    return sp.Rational(s)
def parse_interval(s):
    s=s.replace(r'x\in','x ∈').strip()
    m=re.fullmatch(r'x ∈ ([\[(])\s*(.*?)\s*,\s*(.*?)\s*([\])])',s)
    require(m is not None,'Displayed interval malformed '+s)
    a,b=parse_number(m[2]),parse_number(m[3]);require(a<b,'Displayed ordered interval')
    return sp.Interval(a,b,left_open=m[1]=='(',right_open=m[4]==')')
def decolor(s):return re.sub(r'\{\\color\{(?:red|blue)\}\{([^{}]*)\}\}',r'\1',s)
def displayed_check(record,raw=False):
    kp=record['knowledge_point'];require(set(kp)=={'db_id','id','title'} and kp['db_id']==g.KP_ID and kp['id']==g.KP_UUID and kp['title']==g.TITLE,'KP identity shape')
    q=record['question'];field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];require(len(choices)==5,'Five choices');require(field[':answer-field/type']==':answer-field.type/radio','Radio preserved')
    values=[parse_interval(a[':answer/value']) for a in choices];require(len(set(values))==5,'Whole displayed semantic bank collisions')
    for a in choices:require(a[':answer/type']==':answer.type/math','Answer type')
    for text in [q[':question/problem'],q.get(':question/worked-solution','')]:
        require(text.count('$')%2==0,'Balanced dollar delimiters')
        depth=0
        for c in text:
            depth += (c=='{')-(c=='}');require(depth>=0,'Unmatched closing TeX brace')
        require(depth==0,'Balanced TeX braces')
    if raw:
        require(':question/difficulty' not in q and ':question/worked-solution' not in q and ':answer-field/correct' not in field,'Raw missing fields preserved')
        require(record['generation']['evidence_only'],'Raw ineligible for learner use')
        return
    require(':question/difficulty' in q,'Authored rating')
    geom=record['generation']['plots']['geometry'];truth=sp.Interval(sp.Rational(str(geom['left'])),sp.Rational(str(geom['right'])),left_open=not geom['left_closed'],right_open=not geom['right_closed'])
    require(geom['left_closed']!=geom['right_closed'],'Strict half-open learner scope')
    correct=field[':answer-field/correct'];require(correct[0]==':answer/id','Correct lookup shape')
    require(sum(v==truth for v in values)==1,'Exactly one interval set equivalent to graph')
    require(next(v for a,v in zip(choices,values) if a[':answer/id']==correct[1])==truth,'Derived key matches actual displayed bank')
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
    require(len(blocks)==2,'Canonical two-stage sequence')
    require(q[':question/worked-solution'].startswith(g.OPENING),'Complete canonical shared opening')
    final=parse_interval(decolor(blocks[1]));require(final==truth,'Final solution interval read independently')
    ineq=decolor(blocks[0]).replace(r'\,','').replace(' ','')
    m=re.fullmatch(r'(.*?)(\\leq|\\lt)x(\\leq|\\lt)(.*)',ineq);require(m is not None,'Displayed inequality stage syntax')
    stage=sp.Interval(parse_number(m[1]),parse_number(m[4]),left_open=m[2]==r'\lt',right_open=m[3]==r'\lt')
    require(stage==truth,'Displayed intermediate inequality independently equals set')
    require(q[':question/worked-solution'].count('The given interval can be represented by the following inequality:')==1 and q[':question/worked-solution'].count('We can express our inequality in interval notation as follows:')==1,'Canonical complete prose sequence')

def fidelity(source,replay):
    q=replay['question'];require(q[':question/problem']==source[':question/problem'],'Raw exact prompt/path')
    expected=source[':question/answer-fields'][0][':answer-field/choices'];actual=q[':question/answer-fields'][0][':answer-field/choices']
    require(sorted(a[':answer/value'] for a in expected)==sorted(a[':answer/value'] for a in actual),'Every source bank exact value')
    require(set(parse_interval(a[':answer/value']) for a in expected)==set(parse_interval(a[':answer/value']) for a in actual),'Complete source semantic bank')
    displayed_check(replay,raw=True)

def raster(record):
    plots=record['generation']['plots'];side=json.loads(Path(plots['sidecar']).read_text());m=side['raster_readback'];fit=side['axis_pixel_fit'];geo=side['geometry']
    require(geo==plots['geometry'],'Rendered sidecar geometry matches displayed-instance geometry')
    for i,key in enumerate(('left','right')):
        actual=(m['endpoint_pixels'][i]-fit['origin_pixel'])/fit['pixels_per_unit'];require(abs(actual-geo[key])<.02,'Raster endpoint '+key)
    require(m['closed']==[geo['left_closed'],geo['right_closed']],'Raster endpoint fill')
    ticks=m['tick_pixels'];require(len(ticks)>=2,'Detected actual tick geometry')
    increments=[b-a for a,b in zip(ticks,ticks[1:])]
    require(all(abs(d/fit['pixels_per_unit']/geo['tick_step']-round(d/fit['pixels_per_unit']/geo['tick_step']))<.025 for d in increments),'Raster tick scale')
    require(side['renderer']=='Matplotlib','Authorized renderer')

def main():
    wrapper=load('source.json');sources={q[':question/math-academy-id']:q for q in wrapper['record'][':knowledge-point/questions']};cases=load('source-cases.json');raw=[];repaired=[]
    for case in cases:
        r=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);fidelity(sources[case['source_id']],r);raw.append(r)
        # Truth of original diagram is derived independently; not an observed key match.
        true=parse_interval(case['derived_original_truth']);require(sum(parse_interval(a[':answer/value'])==true for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==1,'Raw independent original truth')
        normal=g.generate('easy',parameters=case['normal_parameters'],profile=case['normal_profile']);displayed_check(normal);raster(normal);repaired.append(normal)
    # Exercise genuinely changed raw parameters; both-open legacy remains evidence only.
    changed_raw=[]
    for profile,p in [('raw_q28850',g.parameters(-2,1,False,1,1)),('raw_q31762',g.parameters(2,5,False,1,1))]:
        r=g.generate('easy',parameters=p,profile=profile);displayed_check(r,raw=True);raster(r);changed_raw.append(r)
    require(g.solution(g.parameters(-2,2,True,1,1))==wrapper['record'][':knowledge-point/canonical-example'][':question/worked-solution'],'Canonical full solution exact replay')
    # Refit EACH source axis from visible labelled anchors; read circles from actual pixels.
    media=Path('/media/jake/SSD/EDB/math');canon=wrapper['record'][':knowledge-point/canonical-example'];paths=[media/re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1] for q in [sources['q-28850'],sources['q-31762'],canon]]
    config={'output':str(HERE/'source-geometry.json'),'cases':[{'path':str(path),'fit':{'anchor_values':[1,6] if i==1 else [-3,3],'anchor_pixels':[25,271] if i==1 else [25,320],'tick_pixels':[25,74,123,172,221,271]+([] if i==1 else [320])}} for i,path in enumerate(paths)]}
    save('source-readback-input.json',config);subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE/'renderer.py'),'--readback',str(HERE/'source-readback-input.json')],check=True)
    for row,coords,fills in zip(load('source-geometry.json'),[(-1,2),(1,4),(-2,2)],[(False,True),(False,False),(True,False)]):
        m=row['measurement'];require(all(abs(a-b)<.025 for a,b in zip(m['endpoint_values'],coords)),'Independent SOURCE raster endpoint');require(m['closed']==list(fills),'Independent SOURCE circle fill')
    # Exhaust every finite mathematical domain and every complete normal bank profile.
    catalogs={};sweep=0;profile_counts={}
    for level in ('easy','moderate','hard'):
        rows=g.catalog(level);catalogs[level]=len(rows);require(len({(p['left'],p['right'],p['left_closed'],p['tick_step'],p['label_step']) for p in rows})==len(rows),'Meaningful finite catalog count')
        for profile in ('authored_left_shift','observed_left_ray','observed_right_ray','observed_negate_left'):
            count=0
            for p in rows:
                g.parse_parameters(level,p,profile)
                try:choices=g.bank(p,profile)
                except ValueError:continue
                sets=[parse_interval(v) for _,v in choices];require(len(set(sets))==5,'Exhaustive whole-bank set distinctness');a,b=sp.Rational(p['left']),sp.Rational(p['right']);truth=sp.Interval(a,b,left_open=not p['left_closed'],right_open=p['left_closed']);require(sum(v==truth for v in sets)==1,'Exhaustive bank correctness');count+=1;sweep+=1
            require(count>=8,'Adequate eligible complete observed banks');profile_counts[level+'/'+profile]=count
    review=[]
    # At least two variants per level PER complete normal bank, plus both source repairs.
    for level in catalogs:
        for profile in ('authored_left_shift','observed_left_ray','observed_right_ray','observed_negate_left'):
            eligible=[]
            for p in g.catalog(level):
                try:g.bank(p,profile);eligible.append(p)
                except ValueError:pass
            chosen=[eligible[(len(eligible)//3)//2*2],eligible[-1]]
            for n,p in enumerate(chosen):
                r=g.generate(level,seed=29+n,parameters=p,profile=profile);displayed_check(r);raster(r);review.append(r)
                other=g.generate(level,seed=99,parameters=p,profile=profile);require(r['question'][':question/id']==other['question'][':question/id'],'Seed/order invariant identity')
    # API seed samplers, guards and signed/fractional changed recipes.
    for level in catalogs:
        for seed in range(4):displayed_check(g.generate(level,seed=seed))
    negatives=0
    for level,p in [('easy',g.parameters(-1,2,False,'1/2',1)),('moderate',g.parameters(1,4,True,1,2)),('moderate',g.parameters(-4,2,True,1,2)),('hard',g.parameters(-2,1,False,'1/2',1)),('hard',g.parameters(-5,'1/2',False,'1/2',1))]:failure(lambda:g.generate(level,parameters=p));negatives+=1
    failure(lambda:g.generate('easy',parameters=g.parameters(0,2,False,1,1),profile='observed_negate_left'));negatives+=1
    bad=copy.deepcopy(review[0]);bad['question'][':question/answer-fields'][0][':answer-field/correct'][1]=bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']
    if bad['question'][':question/answer-fields'][0][':answer-field/correct']==review[0]['question'][':question/answer-fields'][0][':answer-field/correct']:bad['question'][':question/answer-fields'][0][':answer-field/correct'][1]=bad['question'][':question/answer-fields'][0][':answer-field/choices'][1][':answer/id']
    failure(lambda:displayed_check(bad));negatives+=1
    bad=copy.deepcopy(review[0]);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r'\leq',r'\lt');failure(lambda:displayed_check(bad));negatives+=1
    bad=copy.deepcopy(raw[0]);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+=' ';failure(lambda:fidelity(sources['q-28850'],bad));negatives+=1
    bad=copy.deepcopy(review[0]);bad['generation']['plots']['geometry']['left_closed']=not bad['generation']['plots']['geometry']['left_closed'];failure(lambda:raster(bad));negatives+=1
    # Fresh concurrent renders, both same and different parameter sets, scoped temp leak checks.
    with tempfile.TemporaryDirectory(prefix='concurrent-',dir=HERE) as d:
        ps=[g.catalog('hard')[0],g.catalog('hard')[-1],g.catalog('hard')[0],g.catalog('moderate')[-1]]
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:assets=list(ex.map(lambda p:g.render_plots(p,'authored_left_shift',d),ps))
        require(assets[0]['prompt']==assets[2]['prompt'],'Same concurrent identity')
        for p,asset in zip(ps,assets):
            require(json.loads(Path(asset['sidecar']).read_text())['geometry']==g.geometry(p,'authored_left_shift'),'Concurrent geometry isolation');r={'generation':{'plots':asset}};raster(r)
        require(not list(Path(d).glob('render-input-*')),'No unique input leak')
    fixtures=[]
    for i,r in enumerate(repaired+review):
        f=r['question'][':question/answer-fields'][0];fixtures.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual radio selection after independent interval-set verification'} for a in f[':answer-field/choices']]})
    save('engine-input.json',fixtures);engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    save('review.json',{'raw_original_replays':raw,'evidence_only_changed_raw':changed_raw,'normal_source_repairs':repaired,'generated_variants':review})
    sections=['# Half-open number-line review','Raw originals retain all missing fields. q-31762 is both-open and evidence only. Its normal repair closes the left endpoint. Every listed generated variant is authored.']
    for case,r,n in zip(cases,raw,repaired):sections+=['## Original '+case['source_id'],g.markdown(r),'Independent original truth: $'+case['derived_original_truth']+'$.','## Normal source repair '+case['source_id'],g.markdown(n)]
    for r in changed_raw:sections+=['## Evidence-only changed raw parameters / '+r['generation']['bank_profile'],g.markdown(r)]
    for r in review:sections+=['## Authored '+r['question'][':question/difficulty']+' / '+r['generation']['bank_profile'],g.markdown(r)]
    (HERE/'review.md').write_text('\n\n'.join(sections)+'\n')
    # Source decoded byte evidence (JSON serialization is not byte evidence).
    runs=[len(x) for x in re.findall(r'\\+',canon[':question/worked-solution'])];save('decoded-source-bytes.json',{'canonical_adjacent_backslash_run_lengths':sorted(set(runs)),'doubled_backslash_runs':sum(x>1 for x in runs),'repair_claimed':False})
    report={'passed':True,**g.SOURCE,'version':g.VERSION,'raw_exact_source_prompts':2,'raw_exact_complete_banks':2,'source_options_matched':10,'source_options_total':10,'source_semantic_banks':2,'available_correct_designations_matched':0,'available_correct_designations_total':0,'missing_correct_designations':2,'available_solutions_matched':0,'available_solutions_total':0,'missing_solutions':2,'unrated_questions':2,'normal_key_solution_authored':2,'normal_scope_plot_repairs':1,'changed_parameter_raw_replays':2,'canonical_full_solution_exact':True,'source_raster_readback':load('source-geometry.json'),'finite_task_catalogs':catalogs,'eligible_complete_banks':profile_counts,'semantic_bank_sweep':sweep,'review_variants':len(review),'negative_controls':negatives,'concurrent_fresh_renders':4,'native_grading':load('engine-report.json'),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'no_database_writes':True,'unresolved_findings':[]}
    save('validation.json',report);save('freeze.json',{'version':g.VERSION,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256((HERE/'renderer.py').read_bytes()).hexdigest(),'validation_passed':True,'parent_qa_required':True})
    print('PASS: raw 2/2 prompts/banks, 10/10 exact options; original designations/solutions absent; source scope repair 1; '+str(sweep)+' semantic banks, '+str(len(review))+' variants; native grader and concurrent raster QA')
if __name__=='__main__':main()

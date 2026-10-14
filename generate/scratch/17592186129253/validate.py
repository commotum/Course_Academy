#!/usr/bin/env python3
"""Separate source fidelity, independent displayed predicate/math, raster, native checks."""
import importlib.util,json,re,itertools,hashlib,sys,subprocess,copy,concurrent.futures,uuid,random
from pathlib import Path
import sympy as sp
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp29253',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def must(cond,msg):
    if not cond:raise AssertionError(msg)

def expect_error(fn):
    try:fn()
    except (ValueError,AssertionError):return
    raise AssertionError('Required rejection did not occur')

def parse_root(s):
    z=re.search(r'\$x\s*=\s*(.*?)\$',s).group(1).rstrip('., ')
    z=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1)/(\2)',z)
    return sp.Rational(sp.sympify(z))

def predicate(value):
    if 'simple root of even' in value:return 'impossible'
    if 'not a root' in value:return 'not'
    if 'simple root' in value:return 'simple'
    if 'even multiplicity' in value:return 'even'
    if 'odd multiplicity' in value:return 'odd'
    raise AssertionError('Unknown actual displayed predicate')

# Independently defined response sets. Incorrect choices must be unequal to
# EACH OTHER too; equal truth values for one instance do not make predicates
# synonymous. Domains distinguish nonroot, simple, parity and contradiction.
SETS={'simple':{1},'not':{0},'even':set(range(2,202,2)),'odd':set(range(3,202,2)),'impossible':set()}

def formatting(s):
    must(not any(ord(c)<32 and c not in '\n\t' for c in s),'C0 control character')
    must(s.count('$')%2==0,'Unbalanced mathematics delimiter')
    depth=0
    for c in s:
        if c=='{':depth+=1
        if c=='}':depth-=1
        must(depth>=0,'Unbalanced TeX group')
    must(depth==0,'Unbalanced TeX group')

def check_record(rec):
    must(set(rec['knowledge_point'])=={'db_id','id','title'},'Outer knowledge point keys')
    q=rec['question'];p=rec['generation']['parameters'];rs=[sp.Rational(str(x)) for x in p['roots']]
    target=rs[p['target']];f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];cat=rec['generation']['category']
    texts=[a[':answer/value'] for a in choices];cats=[predicate(v) for v in texts]
    must(len(choices)==5 and len({frozenset(SETS[c]) for c in cats})==5,'Complete bank semantic collision')
    must(all(parse_root(v)==target for v in texts),'Stale displayed target')
    for v in [q[':question/problem'],q.get(':question/worked-solution',''),*texts]:formatting(v)
    if ':answer-field/correct' in f:
        correct=next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);must(predicate(correct[':answer/value'])==cat,'Wrong displayed correct predicate')
    # Compute actual vanishing order/sign from the polynomial in the renderer
    # output (not the generator's category metadata or native answer IDs).
    data=rec['generation']['plot_data']
    if data:
        poly=sp.sympify(data['polynomial'],locals={'x':g.X})
        must(sp.Poly(poly,g.X).is_univariate,'Graph is not a polynomial')
        for r,m in zip(rs,p['multiplicities']):
            order=next(k for k in range(8) if sp.diff(poly,g.X,k).subs(g.X,r)!=0)
            must(order==m,'Actual plotted polynomial has wrong local order')
        actual=next(k for k in range(8) if sp.diff(poly,g.X,k).subs(g.X,target)!=0)
        actualcat='simple' if actual==1 else 'even' if actual%2==0 else 'odd'
        must(actualcat==cat,'Plot local classification differs from bank')
        eps=sp.Rational(1,100)
        signs=[sp.sign(poly.subs(g.X,target+e)) for e in [-eps,eps]]
        must(signs[0]*signs[1]==(1 if cat=='even' else -1),'Crossing/bouncing criterion')
        for panel in data['panels']:
            must(panel['ylim'][0]<0<panel['ylim'][1],'Zero axis outside view')
            for x,y in panel['vertices'][::157]:
                expected=float(poly.subs(g.X,sp.Float(x)))
                must(abs(y-expected)<1e-8*max(1,abs(expected)),'Plotted vertices do not evaluate same exact function')
        raster_check(data,Path(rec['generation']['plot_assets']['prompt']))
    if ':question/worked-solution' in q:
        solution=q[':question/worked-solution'];parts=solution.split('In our case,')[-1]
        occurrences=re.findall(r'\$x=(.*?)\$',parts)
        must(occurrences and all(parse_root('$x='+v+'$')==target for v in occurrences),'Stale worked-solution target')
        if cat=='simple':must('*not* tangent' in parts and '*simple* root' in parts,'Missing simple operative stage')
        else:
            must('*tangent*' in parts and '*multiple* root' in parts,'Missing multiple operative stage')
            action='touches the $x$-axis and reverses direction' if cat=='even' else 'crosses the $x$-axis'
            must(action in parts and '*'+cat+'* multiplicity' in parts,'Missing parity operative stage')

def raster_check(data,path):
    a=np.array(Image.open(path).convert('RGB'));h,w,_=a.shape
    red=(a[:,:,0]>150)&(a[:,:,1]<120)&(a[:,:,2]<120)
    black=(a[:,:,:3].max(axis=2)<120)
    for panel in data['panels']:
        bx,by,bw,bh=panel['axes_pixel_bounds'];lo,hi=panel['xlim'];yl,yh=panel['ylim']
        for x,y in panel['vertices'][100:-100:191]:
            px=int(round(bx+(x-lo)/(hi-lo)*bw));py=int(round(h-(by+(y-yl)/(yh-yl)*bh)))
            must(red[max(0,py-4):py+5,max(0,px-4):px+5].any(),'Rendered curve missing at exact plotted vertex')
        py=int(round(h-panel['zero_pixel_y']))
        # Need a genuinely horizontal black zero line, independent of the red.
        sx=int(bx);ex=int(bx+bw)
        must(black[py-2:py+3,sx:ex].any(axis=0).mean()>.1,'Raster zero axis misaligned')

SOURCE_GEOMETRY={
'q-140411':{'origin':[169,88.5],'category':'simple','signs':[-1,1],'flat':False},
'q-140414':{'origin':[169,88.5],'category':'even','signs':[-1,-1],'flat':True},
'q-141133':{'origin':[169,88.5],'category':'odd','signs':[1,-1],'flat':True},
'q-141137':{'origin':[169,88.5],'category':'odd','signs':[-1,1],'flat':True},
'q-141142':{'origin':[169,88.5],'category':'odd','signs':[1,-1],'flat':True},
'q-141144':{'origin':[169,88.5],'category':'even','signs':[-1,-1],'flat':True},
'q-141140':{'origin':[169,88.5],'category':'simple','signs':[1,-1],'flat':False}}

def source_raster(s,q):
    name=re.search(r'images/[^/]+/(.*?)\)',q[':question/problem']).group(1)
    im=Image.open(HERE/'originals'/name).convert('RGBA');canvas=Image.new('RGBA',im.size,'white');canvas.alpha_composite(im);a=np.array(canvas.convert('RGB'))
    red=(a[:,:,0]>160)&(a[:,:,1]<110)&(a[:,:,2]<110)
    geom=SOURCE_GEOMETRY[s];ox,oy=geom['origin']
    def row(x):
        ys=np.where(red[:,x])[0];must(len(ys)>0,'Original curve pixel missing');return float(np.median(ys))
    must(abs(row(ox)-oy)<=1.5,'Original exact root raster location')
    signs=[int(np.sign(row(ox+dx)-oy)) for dx in [-40,40]]
    must(signs==geom['signs'],'Original left/right local crossing orientation')
    slope=abs(row(ox+9)-row(ox-9))/18
    must((slope<.25)==geom['flat'],'Original tangent/simple raster cue')
    return {'source_id':s,'path':name,'dimensions':[a.shape[1],a.shape[0]],'root_pixel':[ox,oy],'side_signs_screen_y':signs,'local_slope_18px':slope,'classification':geom['category'],'scope':'qualitative only; no exact exponent/polynomial inferred'}

def run():
    originals=g.QUESTIONS;cases=[];fidelity=[];rasters=[];records=[];review=[]
    for s,q in originals.items():
        p=g.DEFAULT_PARAMS[s];raw=g.generate('easy',parameters=p,profile='raw-'+s);generated=raw['question'];field=generated[':question/answer-fields'][0];old=q[':question/answer-fields'][0]
        must(generated[':question/problem']==q[':question/problem'],'Prompt fidelity '+s)
        must(set(a[':answer/value'] for a in field[':answer-field/choices'])==set(a[':answer/value'] for a in old[':answer-field/choices']),'Full original bank '+s)
        for key in [':question/difficulty',':question/worked-solution']:
            must((key in generated)==(key in q),'Raw presence parity '+s+key)
        must((':answer-field/correct' in field)==(':answer-field/correct' in old),'Correct ref presence '+s)
        if ':question/worked-solution' in q:must(generated[':question/worked-solution']==q[':question/worked-solution'],'Complete operative prose fidelity '+s)
        if ':answer-field/correct' in old:
            orig=old[':answer-field/correct'][':answer/value'];new=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);must(orig==new,'Original correct designation '+s)
        check_record(raw);rasters.append(source_raster(s,q));cases.append({'source_id':s,'template':'local-identification','difficulty':'easy','parameters':p,'bank_profile':'raw-'+s,'source_difficulty':'easy' if ':question/difficulty' in q else None,'authored_replay_level':':question/difficulty' not in q})
        fidelity.append({'source_id':s,'options_matched':5,'total_options':5,'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in q else None,'correct_designation_matched':True if ':answer-field/correct' in old else None,'raw_attribute_presence':True})
        complete=g.generate('easy',parameters=p,profile='completed-'+s);check_record(complete);records.append(complete)
        p2=copy.deepcopy(p);p2['roots']=[p['roots'][0]+1 if p['roots'][0]<9 else 8]
        changed=g.generate('easy',parameters=p2,profile='completed-'+s);check_record(changed);records.append(changed)
        must(changed['question'][':question/worked-solution']==g.worked_solution(p2['roots'][0],rasters[-1]['classification']),'Changed operative source template')
        review.extend([{'label':'Original raw '+s,'record':raw},{'label':'Generated changed-parameter source-profile '+s,'record':changed}])
    for level in ['easy','moderate','hard']:
        for seed in (list(range(6))+([13] if level=='moderate' else [])):
            r=g.generate(level,seed);check_record(r);records.append(r)
            if seed in {'easy':{0,1,2},'moderate':{0,2,13},'hard':{0,1,3}}[level]:review.append({'label':'Generated '+level+' seed '+str(seed),'record':r})
            again=g.generate(level,seed);must(r==again,'Deterministic sampling')
            fixed=g.generate(level,seed+300,parameters=r['generation']['parameters'])
            must(fixed['question'][':question/id']==r['question'][':question/id'],'Seed cannot change identity with fixed parameters')
        for bad in [{'roots':[0],'multiplicities':[1],'orientation':1,'target':0},{'roots':[-2,2],'multiplicities':[1,2],'orientation':1,'target':0},{'roots':['-7/2','-1/2','5/2'],'multiplicities':[1,2,3],'orientation':1,'target':0}]:
            appropriate={1:'easy',2:'moderate',3:'hard'}[len(bad['roots'])]
            if level!=appropriate:expect_error(lambda:g.generate(level,parameters=bad))
    expect_error(lambda:g.generate('moderate',parameters={'roots':[0,1],'multiplicities':[1,2],'orientation':1,'target':0}))
    expect_error(lambda:g.generate('hard',parameters={'roots':[-5,0,5],'multiplicities':[1,2,3],'orientation':1,'target':0}))
    expect_error(lambda:g.generate('easy',parameters={**g.DEFAULT_PARAMS['q-141133'],'amplitude':4}))
    # Mutation regressions: wrong key, wrong/wrong duplicate predicate, stale
    # root, vanished operative stage, invalid displayed bytes, wrong curve.
    clean=g.generate('hard',seed=2)
    mutations=[]
    b=copy.deepcopy(clean);b['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='$x=0$ is a simple root';mutations.append(b)
    b=copy.deepcopy(clean);f=b['question'][':question/answer-fields'][0];f[':answer-field/choices'][1][':answer/value']=f[':answer-field/choices'][0][':answer/value'];mutations.append(b)
    b=copy.deepcopy(clean);b['question'][':question/worked-solution']=b['question'][':question/worked-solution'].replace('*tangent*','parallel');mutations.append(b)
    b=copy.deepcopy(clean);b['question'][':question/problem']+='\x0c';mutations.append(b)
    b=copy.deepcopy(clean);b['generation']['plot_data']['polynomial']='x';mutations.append(b)
    for b in mutations:expect_error(lambda:check_record(b))
    # No parameter spelling/ordering aliases count as different assessed tasks.
    params={'roots':['5/2','-7/2','-1/2'],'multiplicities':[2,1,3],'orientation':1,'target':0}
    alias=g.generate('hard',parameters=params);p=alias['generation']['parameters'];normal=g.generate('hard',parameters=p)
    must(alias['question'][':question/id']==normal['question'][':question/id'],'Sorting aliases alter identity')
    # Fresh concurrent renderer calls use independent temporary files and exact
    # same-function sidecars; choose parameters not in above preview/review.
    parallel=[{'roots':[-9],'multiplicities':[3],'orientation':-1,'target':0},{'roots':[9],'multiplicities':[2],'orientation':-1,'target':0}]*2
    # Matplotlib global state is not thread-safe: use separate subprocesses.
    fresh_directory=HERE/'concurrent-fresh'/str(uuid.uuid4())
    code="import importlib.util,json,sys;from pathlib import Path;s=importlib.util.spec_from_file_location('g',sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);g.HERE=Path(sys.argv[3]);print(json.dumps(g.generate('easy',parameters=json.loads(sys.argv[2]))))"
    def child(p):
        x=subprocess.run([sys.executable,'-c',code,str(HERE.with_suffix('.py')),json.dumps(p),str(fresh_directory)],check=True,text=True,capture_output=True);return json.loads(x.stdout)
    with concurrent.futures.ThreadPoolExecutor(4) as ex:outputs=list(ex.map(child,parallel))
    for r in outputs:check_record(r)
    must(outputs[0]==outputs[2] and outputs[1]==outputs[3],'Concurrent deterministic render failed')
    must(len(list((fresh_directory/'plots').glob('*.png')))==2 and len(list((fresh_directory/'plots').glob('*.json')))==2,'Concurrent temporary file leak')
    inputs=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0];checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual native radio selection'} for a in f[':answer-field/choices']]
        inputs.append({'label':str(i),'record':r,'checks':checks})
    (HERE/'native-input.json').write_text(json.dumps(inputs,indent=2))
    binary=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(binary),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    native=json.loads((HERE/'native-report.json').read_text())
    # Enumerate narrow meaningful catalogs without rendering/cosmetic aliases.
    domain_counts={}
    sampler_coverage={}
    for level in ['easy','moderate','hard']:
        pool=list(range(-9,10)) if level=='easy' else list(range(-6,7)) if level=='moderate' else [sp.Rational(k,2) for k in range(-13,14,2)]
        n={'easy':1,'moderate':2,'hard':3}[level]
        sampled=[g.canonical_parameters(g.sample(level,random.Random(i))) for i in range(200)]
        for p in sampled:g.guard(level,p)
        targets={g.category(p['multiplicities'][p['target']]) for p in sampled}
        must(targets=={'simple','even','odd'},'Default sampler misses a target category')
        must({p['orientation'] for p in sampled}=={-1,1},'Default sampler misses an orientation')
        must({p['target'] for p in sampled}==set(range(n)),'Default sampler misses a target position')
        sampler_coverage[level]={'sample_count':200,'target_categories':sorted(targets),'orientations':[-1,1],'target_indices':list(range(n)),'unique_meaningful_parameters':len({g.stable(p) for p in sampled})}
        configs=sum(1 for rs in itertools.combinations(pool,n) if n==1 or min(rs[i+1]-rs[i] for i in range(n-1))>=3)
        domain_counts[level]={'root_configurations':configs,'category_assignments':3 if n==1 else 6,'orientations':2,'targets':n,'meaningful_tasks':configs*(3 if n==1 else 6)*2*n}
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2))
    (HERE/'source-raster-checks.json').write_text(json.dumps(rasters,indent=2))
    (HERE/'review.json').write_text(json.dumps(review,indent=2))
    (HERE/'review.md').write_text('# Source and generated review\n\n'+ '\n\n---\n\n'.join('# '+item['label']+'\n\n'+g.markdown(item['record']) for item in review))
    result={'passed':True,'database_writes':0,'source_practice_count':7,'source_prompt_exact':7,'source_banks_complete':7,'source_options_matched':35,'source_options_total':35,'source_solution_exact':5,'source_solution_present_total':5,'source_correct_designations_matched':5,'source_correct_designations_present_total':5,'missing_original_correct_designations':2,'missing_original_solutions':2,'raw_presence_parity':7,'source_fidelity':fidelity,'normal_records_mathematically_checked':len(records),'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':native['documented_unresolved_checks'],'raw_missing_correct_records_not_native_graded':2,'authored_levels':['moderate','hard'],'meaningful_catalogs':domain_counts,'default_sampler_coverage':sampler_coverage,'mutation_regressions':len(mutations),'concurrent_render_records':4,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'matplotlib_version':g.matplotlib.__version__,'higher_multiplicity_exponent_recovery_claimed':False,'limitations':['Exact unseen source polynomials are underdetermined. Original raster is reused at anchors; changed representative curves preserve the assessed qualitative local behavior.','Moderate and hard are authored root-location/context workload extensions, not observed difficulty labels.','Source impossible simple-even predicate is retained as a distinct observed misconception; it denotes the empty multiplicity set.']}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':run()

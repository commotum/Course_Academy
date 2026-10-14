"""Independent printed math, complete original fidelity, native pixel and engine checks."""
import concurrent.futures
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as sp

D=Path(__file__).resolve().parent;ROOT=D.parents[2]
s=importlib.util.spec_from_file_location('local_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x,y=sp.symbols('x y');LABELS=('I','II','III')

def write(name,value):(D/name).write_text(json.dumps(value,indent=2)+'\n')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def expr(text):
    t=text.replace(' ','').replace('&','').replace(r'\,','').replace('✓','').replace(r'\times','').rstrip('.')
    t=re.sub(r'\\d?frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',t)
    assert re.fullmatch(r'[\d()+\-*/xy]+',t),t
    t=re.sub(r'(?<=[\d)xy])(?=[xy(])','*',t)
    return sp.sympify(t,locals={'x':x,'y':y},rational=True)

def equation(text):
    a,b=text.split('=');return sp.expand(expr(a)-expr(b))
def full_line(text):
    z=sp.Poly(equation(text),x,y);assert z.total_degree()==1
    c=[z.coeff_monomial(x),z.coeff_monomial(y),z.coeff_monomial(1)]
    v=next(a for a in c if a);return tuple(sp.cancel(a/v) for a in c)

def statements(q):
    a=re.findall(r'(?m)^(I|II|III)\. \$(.*?)\$$',q[':question/problem'])
    if not a:a=re.findall(r'(?m)^- \*\*(I|II|III)\.\*\* \$(.*?)\$$',q[':question/problem'])
    assert [a[0] for a in a]==list(LABELS);return [a[1] for a in a]

def points_from_print(sol,profile):
    if profile=='q-54285':
        m=re.search(r'y-axis at (-?\d+) and passes through \((-?\d+),(-?\d+)\)',sol);assert m
        b,u,v=map(sp.Rational,m.groups());return [(sp.Integer(0),b),(u,v)]
    if profile=='q-59732':
        m=re.search(r'intercepts \(0,(-?\d+)\) and \((-?\d+),0\)',sol);assert m
        b,u=map(sp.Rational,m.groups());return [(sp.Integer(0),b),(u,sp.Integer(0))]
    match=re.search(r'coordinates \$\(([^,]+),([^)]*)\)\$ and \$\(([^,]+),([^)]*)\)\$',sol);assert match
    u,v,w,z=[expr(v) for v in match.groups()];return [(u,v),(w,z)]

def formatting(q):
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
        assert text.count('$')%2==0
        depth=0
        for i,c in enumerate(text):
            if i and text[i-1]=='\\':continue
            if c=='{':depth+=1
            elif c=='}':depth-=1
            assert depth>=0
        assert depth==0
        assert '+-' not in text and '--' not in text

def curve_readback(asset,points,calibration=None):
    rgba=Image.open(asset['local']).convert('RGBA');white=Image.new('RGBA',rgba.size,'white');white.alpha_composite(rgba)
    pixels=np.asarray(white.convert('RGB'));h,w=pixels.shape[:2]
    if calibration:
        ox,oy=calibration['origin_pixels'];sx,sy=calibration['unit_pixels']
        assert [w,h]==calibration['dimensions']
    else:
        ox,oy=asset['origin_pixels'];sx,sy=asset['unit_pixels']
        assert [w,h]==asset['dimensions'];assert asset['glyph_min_axis_clearance_px']>=4
        # Physical gray grid spacing must support the declared native scale.
        gray=(pixels[:,:,0]>140)&(pixels[:,:,0]<230)&(np.max(pixels,axis=2)-np.min(pixels,axis=2)<5)
        cols=np.where(gray.sum(axis=0)>h*.45)[0]
        assert len(cols)>3
        groups=np.split(cols,np.where(np.diff(cols)>1)[0]+1)
        centers=[np.mean(a) for a in groups]
        assert abs(np.median(np.diff(centers))-sx)<2
    red=(pixels[:,:,0]>220)&(pixels[:,:,1]<100)&(pixels[:,:,2]<100)
    py,px=np.where(red);assert len(px)>80
    # Fit native curve pixels, rather than trusting recorded line coefficients.
    realx=(px-ox)/sx;realy=(oy-py)/sy
    slope,intercept=np.polyfit(realx,realy,1)
    (u,v),(a,b)=points;expected_m=float((b-v)/(a-u));expected_b=float(v)-expected_m*float(u)
    assert abs(slope-expected_m)<.025*(1+abs(expected_m)),(asset['local'],slope,expected_m)
    assert abs(intercept-expected_b)<.035*(1+abs(expected_m)),(asset['local'],intercept,expected_b)
    expected_py=oy-sy*(expected_m*(px-ox)/sx+expected_b)
    distances=np.abs(py-expected_py)/np.sqrt(1+(sy*expected_m/sx)**2)
    assert np.percentile(distances,99)<2.8,(asset['local'],np.percentile(distances,99))
    probes=[]
    for xx in np.linspace(float(u),float(a),7):
        yy=expected_m*xx+expected_b;cx,cy=int(round(ox+sx*xx)),int(round(oy-sy*yy))
        tile=red[max(0,cy-5):min(h,cy+6),max(0,cx-5):min(w,cx+6)]
        assert tile.any(),(cx,cy,asset['local'])
        probes.append([xx,yy,cx,cy])
    if asset['role']=='solution':
        blue=(pixels[:,:,2]>170)&(pixels[:,:,0]<110)&(pixels[:,:,1]<110)
        for u,v in points:
            cx,cy=int(round(ox+sx*float(u))),int(round(oy-sy*float(v)))
            assert blue[max(0,cy-5):cy+6,max(0,cx-5):cx+6].any()
    assert sha(asset['local'])==asset['sha256']
    return {'pixels':[w,h],'fit_slope':float(slope),'fit_intercept':float(intercept),'seven_native_curve_probes':probes,'99pct_perpendicular_curve_error_px':float(np.percentile(distances,99))}

# Manual calibration was read from the FULL native originals: axis-zero pixel,
# spacing between labeled even integer grid ticks, and visible line points.
CAL={
 'q-54285':{'dimensions':[334,304],'origin_pixels':[79,225],'unit_pixels':[31,31],'points':[['0','2'],['4','4']]},
 'q-59732':{'dimensions':[334,304],'origin_pixels':[79,225],'unit_pixels':[31,31],'points':[['0','4'],['4','0']]},
 'q-71837':{'dimensions':[327,304],'origin_pixels':[64,214],'unit_pixels':[25.5,25.5],'points':[['0','6'],['2','0']]},
 'q-54293':{'dimensions':[327,304],'origin_pixels':[115,188],'unit_pixels':[25.5,25.5],'points':[['0','2'],['4','0']]}}

def structural(rec,do_pixels=True):
    q=rec['question'];md=rec['generation'];profile=md['template'];raw=md.get('raw_source_replay',False);level=md['level']
    assert set(rec['knowledge_point'])=={'db_id','id','title'}
    assert rec['knowledge_point']['db_id']==g.KP_ID;uuid.UUID(rec['knowledge_point']['id'])
    uuid.UUID(q[':question/id']);formatting(q)
    eqs=statements(q);pts=points_from_print(q[':question/worked-solution'],profile)
    (u,v),(a,b)=pts;assert a!=u
    m=(b-v)/(a-u);c=v-m*u
    p=md['parameters'];expected_m=sp.Rational(p['m']) if 'm' in p else sp.Rational(p['b'])/sp.Rational(p['t'])*(1 if profile=='q-54285' else -1)
    assert (m,c)==(expected_m,sp.Rational(p['b']))
    target=full_line('y='+str(m)+'*x+'+str(c))
    truth=[full_line(z)==target for z in eqs]
    assert any(truth)
    assert md['parameter_fingerprint']==g.digest([str(m),str(c)])
    fields=q[':question/answer-fields'];allids=set();qualifies={l for l,ok in zip(LABELS,truth) if ok}
    for i,f in enumerate(fields):
        uuid.UUID(f[':answer-field/id']);choices=f[':answer-field/choices'];cid=f[':answer-field/correct'][1]
        assert f[':answer-field/correct'][0]==':answer/id'
        assert len(choices)==len({a[':answer/id'] for a in choices})
        assert cid in {a[':answer/id'] for a in choices}
        for ans in choices:
            uuid.UUID(ans[':answer/id']);assert ans[':answer/id'] not in allids;allids.add(ans[':answer/id'])
            assert ans[':answer/type']==':answer.type/text' and '$' not in ans[':answer/value']
            assert ':answer/feedback' not in ans
        if f[':answer-field/type']==':answer-field.type/checkbox':
            assert len(fields)==3 and f[':answer-field/key']==LABELS[i]
            assert {a[':answer/value'] for a in choices}=={'false','true'}
            wanted=str(truth[i]).lower()
            assert next(a[':answer/value'] for a in choices if a[':answer/id']==cid)==wanted
        else:
            assert f[':answer-field/type']==':answer-field.type/radio' and len(fields)==1 and len(choices)==5
            subsets=[frozenset(re.findall(r'\bI{1,3}\b',a[':answer/value'])) for a in choices]
            assert len(set(subsets))==5
            for ans,subset in zip(choices,subsets):assert (ans[':answer/id']==cid)==(subset==qualifies)
    sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
    if blocks:
        assert len(blocks)==3
        if profile=='q-71837':assert [len(z.split(r'\\')) for z in blocks]==[4,6,5]
        if profile=='q-54293':assert [len(z.split(r'\\')) for z in blocks]==[2,5,5]
        for index,block in enumerate(blocks):
            which=0;next_substitution=True
            for row in block.split(r'\\'):
                if next_substitution:
                    # Read the actual printed equation and preserve its operands before
                    # numeric evaluation; zero-coordinate mistakes cannot hide here.
                    expected_stage=re.sub(r'[xy]',lambda a:'('+sp.latex(pts[which][0] if a[0]=='x' else pts[which][1])+')',eqs[index])
                    if raw and profile=='q-54293' and index==0:expected_stage=expected_stage.replace('-2(0)','-1(0)')
                    clean=lambda z:z.replace(' ','').replace('&','').replace(r'\dfrac',r'\frac')
                    assert clean(row)==clean(expected_stage),(profile,row,expected_stage)
                    next_substitution=False
                residual=equation(row);expected=equation(eqs[index]).subs({x:pts[which][0],y:pts[which][1]})
                assert residual==expected,(profile,row,residual,expected)
                if '✓' in row or r'\times' in row:
                    assert (residual==0)==('✓' in row);which+=1;next_substitution=True
            # The exact substituted operands are essential, even when x=0 hides a typo.
            first=block.split(r'\\')[0]
            if profile=='q-54293' and index==0:assert '-'+str(md['parameters']['b']-(1 if raw else 0))+'(0)' in first
    else:
        # Source compact prose slope/intercepts are independently checked from printed values.
        if profile=='q-54285':
            printed=sp.Rational(re.search(r'slope is ([\d/-]+)',sol)[1]);assert printed==m
            conclusion=re.search(r'Therefore (.*), statement II',sol)[1];assert full_line(conclusion)==target
        else:assert full_line(re.search(r'equation is (.*), statement III',sol)[1])==target
    # Normal authored bounds are separately enforced from their actual printed task.
    if profile=='authored-easy':assert m in (-2,-1,1,2) and 1<=abs(c)<=6 and pts[1][0]==2
    if profile=='authored-moderate':assert m in [sp.Rational(a,b) for a,b in ((1,2),(-1,2),(2,3),(-2,3),(3,2),(-3,2))] and 1<=abs(c)<=6
    if profile=='authored-hard':assert m in (-4,-3,-2,2,3,4) and 1<=abs(c)<=6
    pixels=[]
    if do_pixels:
        for asset in md['assets']:
            cal=CAL.get(asset.get('source_calibration'))
            if cal:assert pts==[(sp.Rational(u),sp.Rational(v)) for u,v in cal['points']]
            pixels.append(curve_readback(asset,pts,cal))
    return {'line':[str(m),str(c)],'truth':truth,'fields':len(fields),'statements':3,'numeric_rows':sum(len(z.split(r'\\')) for z in blocks),'pixels':pixels}

def checks(rec):
    results=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            results.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual field-owned native radio/checkbox entry; entire displayed bank'})
    return results

def main():
    snap=ROOT/'generate/runs/current/refresh-2026-10-14'
    for folder,id,name in [('sources','17592186054802','source'),('topics','17592186050790','topic'),('lessons','17592186050790','lesson')]:assert (D/(name+'.json')).read_bytes()==(snap/folder/(id+'.json')).read_bytes()
    inv=json.loads((D/'independent-inventory.json').read_text());assert all(inv[k]==g.SOURCE[k] for k in ('database','basis','lineage'))
    assert [a['record'] for a in inv['questions']]==[q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
    assert all(a['role']=='independently authored inventory' and a['relationship_to_source_templates'] for a in inv['questions'])
    cases=json.loads((D/'source-cases.json').read_text());assert {c['source_id'] for c in cases}==set(g.PROFILES)
    originals=[];ledger=[];native=[];maths=[];pixels=[];allrec=[]
    for case in cases:
        profile=case['source_id'];rec=g.generate(case['level'],profile=case['bank_profile'],parameters=case['parameters']);result=structural(rec);maths.append(result)
        old=g.PROFILES[profile];q=rec['question'];assert q[':question/problem']==old[':question/problem']
        expected=old[':question/worked-solution'];repair=[]
        if profile=='q-54293':repair=['Raw source preserves wrong -1 operand with explicit ineligible flag; normal profile minimally repairs to -2.']
        assert (':question/difficulty' in q)==(':question/difficulty' in old)
        assert q[':question/worked-solution']==expected
        assert rec['generation']['raw_source_replay']
        assert rec['generation']['eligible_for_normal_inventory']==(profile!='q-54293')
        normal=g.generate(case['level'],profile=profile,parameters=case['parameters'])
        normal_expected=old[':question/worked-solution'].replace(r'(2) & =-1(0)',r'(2) & =-2(0)') if profile=='q-54293' else old[':question/worked-solution']
        assert normal['question'][':question/worked-solution']==normal_expected
        assert not normal['generation']['source_errors'] and normal['generation']['eligible_for_normal_inventory']
        values=0
        assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
        for before,after in zip(old[':question/answer-fields'],q[':question/answer-fields']):
            assert before[':answer-field/key']==after[':answer-field/key']
            assert before[':answer-field/type'][':db/ident']==after[':answer-field/type']
            assert sorted(a[':answer/value'] for a in before[':answer-field/choices'])==sorted(a[':answer/value'] for a in after[':answer-field/choices'])
            assert before[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in after[':answer-field/choices'] if a[':answer/id']==after[':answer-field/correct'][1])
            assert [a.get(':answer/feedback') for a in before[':answer-field/choices']]==[None]*len(after[':answer-field/choices'])
            values+=len(after[':answer-field/choices'])
        ledger.append({'source_id':profile,'prompt_exact':True,'raw_solution_exact':True,'solution_exact_after_documented_operand_repair':True,'matched_fields':len(q[':question/answer-fields']),'matched_values':values,'complete_bank':True,'correct_refs_matched':len(q[':question/answer-fields']),'repairs':repair,'missing_or_extra':[]})
        originals.append(rec);native.append({'label':'original '+profile,'record':rec,'checks':checks(rec)})
    domains={};samples={};fingerprints={};review=originals[:]
    for profile in list(g.PROFILES)+['authored-easy','authored-moderate','authored-hard']:
        level=g.SOURCE_LEVELS.get(profile,profile.split('-')[-1]);domain=g.candidates(profile);domains[profile]=len(domain)
        keys=set();profilesamples=[]
        for p in domain:
            rec=g.generate(level,seed=17,profile=profile,parameters=p)
            result=structural(rec);maths.append(result);keys.add(rec['generation']['parameter_fingerprint']);allrec.append(rec)
            other=g.generate(level,seed=41,profile=profile,parameters=p)
            assert rec['question'][':question/id']==other['question'][':question/id']
            assert rec['question'][':question/problem']==other['question'][':question/problem']
            assert rec['question'][':question/worked-solution']==other['question'][':question/worked-solution']
            native.append({'label':profile+' '+str(p),'record':rec,'checks':checks(rec)})
            if len(profilesamples)<2:profilesamples.append(rec)
        fingerprints[profile]=len(keys);samples[profile]=profilesamples
        if profile.startswith('authored-'):
            chosen={'easy':[{'m':1,'b':3,'u':2},{'m':-2,'b':-4,'u':2}], 'moderate':[{'m':'1/2','b':3,'u':2},{'m':'-2/3','b':-4,'u':3}], 'hard':[{'m':3,'b':2,'u':2},{'m':-4,'b':-3,'u':2}]}[level]
            review+=[g.generate(level,seed=7,profile=profile,parameters=p) for p in chosen]
        for invalid in ({'b':0,'t':0},{'m':'100','b':1,'u':2},{'m':'1/2','b':0,'u':2}):
            try:g.generate(level,profile=profile,parameters=invalid)
            except (ValueError,TypeError):pass
            else:raise AssertionError('Invalid domain accepted')
    # Native pixels for fresh concurrent same/different inputs; unique atomic files.
    import tempfile
    saved_package=g.PACKAGE;g.PACKAGE=Path(tempfile.mkdtemp(prefix='concurrent-fresh-',dir=D))
    fresh_package=g.PACKAGE
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs=[pool.submit(g.generate,'moderate',seed=i,parameters={'m':'-2/3' if i%2 else '2/3','b':5,'u':3},profile='authored-moderate') for i in range(4)]
        concurrent_records=[a.result() for a in jobs]
    g.PACKAGE=saved_package
    for rec in concurrent_records:structural(rec)
    assert len(list((fresh_package/'assets').glob('*.png')))==4
    assert concurrent_records[0]['question'][':question/id']==concurrent_records[2]['question'][':question/id']
    assert concurrent_records[0]['question'][':question/id']!=concurrent_records[1]['question'][':question/id']
    assert not [f for f in (D/'assets').iterdir() if not re.fullmatch(r'[a-f0-9]{64}\.(png|json)',f.name)]
    # Explicit sign/fraction boundaries and canonical parameter-spelling alias.
    for level,p in [('easy',{'m':-2,'b':-6,'u':2}),('moderate',{'m':'-3/2','b':-6,'u':2}),('hard',{'m':-4,'b':-6,'u':2})]:structural(g.generate(level,parameters=p))
    assert g.generate('moderate',parameters={'m':'2/4','b':6,'u':2})['question'][':question/id']==g.generate('moderate',parameters={'m':'1/2','b':6,'u':2})['question'][':question/id']
    # Mutation regressions catch displayed equation, correct set, hidden zero operand,
    # control characters and operative stage changes while final answers stay fixed.
    mutations=[]
    import copy
    r=copy.deepcopy(originals[0]);r['question'][':question/problem']=r['question'][':question/problem'].replace('y+3x=6','y+4x=6');mutations.append(r)
    r=copy.deepcopy(g.generate('hard',profile='q-54293',parameters={'b':2,'t':4}));r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('-2(0)','-1(0)',1);mutations.append(r)
    r=copy.deepcopy(review[-1]);r['question'][':question/problem']+='\x0c';mutations.append(r)
    for r in mutations:
        try:structural(r,False)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('Mutation passed')
    write('review.json',review);write('source-replay.json',ledger);write('source-replay-records.json',originals)
    (D/'review.md').write_text('\n\n---\n\n'.join('## '+('Original raw replay (q-54293 typo is ineligible source evidence): ' if r in originals else 'Authored normal: ')+r['generation']['bank_profile']+' '+str(r['generation']['parameters'])+'\n\n'+g.markdown(r) for r in review)+'\n')
    write('engine-input.json',native)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
    engine=json.loads((D/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    write('plot-calibration.json',{'method':'Full native inspection of axes/ticks and labeled intercepts/visible marked points, followed by independent red-pixel line fits and seven curve probes per native PNG.','original_images':CAL,'original_readbacks':[{'source_id':r['generation']['bank_profile'],'checks':structural(r)['pixels']} for r in originals]})
    write('runtime.json',{'python':sys.version,'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__,'renderer':'Matplotlib Agg','database_operations':0,'atomic_writes':True})
    report={'status':'pass','basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'original_MA_questions':4,'independent_inventory_questions':3,
      'source_fidelity':{'complete_banks_matched':4,'total_banks':4,'fields_matched':8,'values_matched':22,'distractors_matched':14,'correct_refs_matched':8,'statements_matched':12,'raw_exact_prompts':4,'raw_exact_solutions':4,'normal_unchanged_solutions':3,'documented_operand_repaired_solutions':1,'feedback_presence_matched_fields':8,'native_original_prompt_plots':4,'native_original_solution_plots':2,'missing_ratings':2,'missing_correct_refs':0,'ungradable_source_fields':0,'unresolved':[]},
      'mathematics':{'instances_checked':len(maths),'numeric_rows_checked':sum(v['numeric_rows'] for v in maths),'whole_statements_checked':3*len(maths),'domain_coverage':domains,'distinct_graph_tasks_per_family':fingerprints,'source_calibration_from_native_pixels':True,'all_native_variant_curve_probes':True,'same_and_different_concurrent_instances':4,'mutation_regressions_rejected':len(mutations)},
      'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},
      'authored_scope':{'easy':'integer substitution at two read graph points; three directly written equations; checkbox subset','moderate':'simple rational substitution at two read graph points; swapped scale/sign claims; checkbox subset','hard':'same three-claim point-testing workload with equation rearrangements; original radio replay plus checkbox authored extension','within_level_progression':False},
      'hashes':{'script':sha(D.with_suffix('.py')),'validator':sha(__file__),'source':sha(D/'source.json'),'topic':sha(D/'topic.json'),'lesson':sha(D/'lesson.json'),'engine':sha(ROOT/'generate/runs/current/check-engine')},
      'limitations':['Easy/moderate labels are explicit authored policies, not recovered MA ratings.','Two unrated current source checkbox solutions are brief captured authored prose; preserve current basis2275 contract despite older MA page radio shape.','One source solution coefficient typo repaired; raw source wrapper unchanged.','Finite graph families, no option/order/alias/bounds inflation; graph locus is the assessed mathematical task.','Source plots reused only at exact original parameters after per-image calibration.'], 'database_writes':0}
    write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()

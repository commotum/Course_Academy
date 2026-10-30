"""Author the replacement pool and independently check displayed mathematics."""
import importlib.util,json,os,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(H/'package'))
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(H/'assets')
spec=importlib.util.spec_from_file_location('parametric_fixed',H/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from generate.parametric_plot_policy import plot_plan,validate_delivery_batch

def check_math(r):
    d=r['generation'];shape=d['bank'][d['role']];q=r['question']
    # Read formulas and table values rendered in the prompt/solution rather than
    # accepting the record's precomputed table arrays as the answer.
    raw=re.search(r'\\begin\{aligned\}x&=(.*?)\\\\ y&=(.*?)\\\\ &',q[':question/problem'],re.S)
    assert raw
    for printed,axis in zip(raw.groups(),('x','y')):
        expected=g.expr(shape[axis]);tex=g.tex(expected.subs(g.T,g.sp.Symbol('theta'))) if d['label'].startswith('\\theta') else g.tex(expected)
        assert printed==tex
    times=list(map(g.expr,d['ts']));expected=[[g.sp.simplify(g.expr(shape[axis]).subs(g.T,t)) for t in times] for axis in ('x','y')]
    for axis,values in zip(('x','y'),expected):assert d['table_'+axis]==[g.tex(v) for v in values]
    arrays=re.findall(r'\\begin\{array\}.*?\\hline (.*?)\\\\ \\hline\\end\{array\}',q[':question/worked-solution'],re.S)
    assert arrays
    seen={'x':[],'y':[]}
    for body in arrays:
        rows=body.split(r' \\ \hline ');assert len(rows)==3
        for axis,row in zip(('x','y'),rows[1:]):
            cells=[c.strip() for c in row.split(' & ')];assert cells[0]==axis
            if any(cells[1:]):seen[axis].extend(cells[1:])
    assert seen['x']==[g.tex(v) for v in expected[0]]*2
    assert seen['y']==[g.tex(v) for v in expected[1]]
    assert len(set(g.valid_bank(d['bank'])))==5
    assert d['plot_plan']==plot_plan(d['bank'],d['ts'])

def main():
    pool=[]
    for index,level in enumerate(('easy','moderate','hard')):
        rows=g.batch(level,5,2026103087721+index*1009);pool+=rows
        for r in rows:check_math(r)
        print('Built',level,len(rows),flush=True)
    assert len({r['generation']['math_fingerprint'] for r in pool})==15
    # Retained used questions are not repeated under a new plot identity.
    retained=[g.shape(g.T*(g.T-2)-1,g.T*(1-g.T)-2,-2,2),g.shape(g.T**2-1,2-g.T,-1,2)]
    assert not {str(g.geometry_key(s)) for s in retained}&{str(g.geometry_key(r['generation']['bank'][r['generation']['role']])) for r in pool}
    validate_delivery_batch(pool,17592186087721)
    for name,value in [('candidate-pool',pool),('render-input',pool)]:
        (H/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
    coverage=[]
    # Preserve all imported families while rejecting oversized sampled variants.
    for template in g.SPECS:
        d=g.build_instance('easy',19,template=template,parameters={'m':1,'n':1,'h':0,'k':0});coverage.append({'template':template,'narrow_unit_pixels':d['plot_plan']['narrow_unit_pixels']})
    representative=[]
    for template in ('q-16194','q-16169','q-16192','q-16198'):
        d=g.build_instance('easy',19,template=template,parameters={'m':1,'n':1,'h':0,'k':0});r=g.make_record(d,19);check_math(r);representative.append(r)
    validate_delivery_batch(representative,17592186087721)
    (H/'representative-sources.json').write_text(json.dumps(representative,indent=2)+'\n')
    # Reported old question: prove the new rendering policy supports its exact
    # five listed checkpoints, without modifying that used question in EDB.
    old=json.loads((ROOT/'reference/edb-math/audits/2026-10-30-parametric-plot-readability/reported-generation.json').read_text());bank=old['generation']['plots'];plan=plot_plan(bank,[-2,-1,0,1,2])
    assert plan['checkpoints'][0]==[[7.,-8.],[2.,-4.],[-1.,-2.],[-2.,-2.],[-1.,-4.]]
    import subprocess
    request={'bank':bank,'ts':['-2','-1','0','1','2'],'correct':0,'output_dir':str(H/'reported-reproduction')}
    (H/'reported-reproduction.json').write_text(json.dumps(request))
    subprocess.run([sys.executable,str(H/'package/render.py'),str(H/'reported-reproduction.json')],check=True)
    result={'passed':True,'pool_questions':15,'levels':{'easy':5,'moderate':5,'hard':5},'all_source_families':coverage,'representative_source_records':4,'reported_points_verified':True,'minimum_narrow_unit_pixels':min(r['generation']['plot_plan']['narrow_unit_pixels'] for r in pool),'minimum_candidate_difference_pixels':min(p['pixels'] for r in pool for p in r['generation']['plot_plan']['pair_differences'])}
    (H/'generator-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()

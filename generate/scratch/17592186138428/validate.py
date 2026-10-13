#!/usr/bin/env python3
"""Independent displayed-equation, native grader, source and PNG verification."""
import concurrent.futures
import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
import uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('graph_kp',SCRIPT); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
X,Y=sp.symbols('x y')
TRANS=standard_transformations+(implicit_multiplication_application,)
def expr(s): return parse_expr(s,local_dict={'x':X,'y':Y},transformations=TRANS)
def displayed_rows(r):
    text=r['question'][':question/problem']
    system=re.search(r'\\begin\{array\}\{l\}(.*?)\\end\{array\}',text).group(1)
    rows=[]
    for row in system.split('\\\\'):
        lhs,rhs=row.split('='); rows.append(expr(lhs)-expr(rhs))
    return rows

def formatting(text):
    # Remove escaped literal brace and field placeholders before balancing groups.
    text=re.sub(r'\{\{field-[12]\}\}','',text)
    text=text.replace(r'\{','').replace(r'\}','')
    depth=0
    for char in text:
        depth += (char=='{')-(char=='}'); assert depth>=0
    assert depth==0
    tokens=re.findall(r'\$\$|\$',text); mode=None
    for token in tokens:
        if mode is None: mode=token
        else: assert mode==token; mode=None
    assert mode is None

def check(r):
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question']; uuid.UUID(q[':question/id']); rows=displayed_rows(r)
    sol=sp.solve(rows,(X,Y)); assert set(sol)=={X,Y}
    vals=[sol[X],sol[Y]]; ids=set()
    assert len(q[':question/answer-fields'])==2
    for i,f in enumerate(q[':question/answer-fields']):
        assert f[':answer-field/key']==f'field-{i+1}' and f[':answer-field/type']==':answer-field.type/blank'
        assert q[':question/problem'].count('{{'+f[':answer-field/key']+'}}')==1
        uuid.UUID(f[':answer-field/id']); assert len(f[':answer-field/choices'])==1
        a=f[':answer-field/choices'][0]; uuid.UUID(a[':answer/id']); assert a[':answer/id'] not in ids; ids.add(a[':answer/id'])
        assert f[':answer-field/correct']==[':answer/id',a[':answer/id']]
        assert sp.Rational(a[':answer/value'])==vals[i] and '$' not in a[':answer/value']
    for key in (':question/problem',':question/worked-solution'): formatting(q[key])
    coordinates=re.findall(r'\$\((-?\d+),(-?\d+)\)\$',q[':question/worked-solution'])
    assert len(coordinates)==2 and all([int(x),int(y)]==vals for x,y in coordinates)
    for role,path in r['generation']['plot_assets'].items():
        path=Path(path); assert path.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
        side=json.loads(path.with_suffix('.json').read_text()); assert side['role']==role and side['renderer']=='Matplotlib'
        assert side['data']==r['generation']['plot_data']; assert side['data']['intersection']==vals
        bounds=side['data']['bounds']; assert bounds[0]<vals[0]<bounds[1] and bounds[2]<vals[1]<bounds[3]
        for row,shown in zip(rows,side['plotted_equations']):
            plot=shown['a']*X+shown['b']*Y-shown['c']
            assert sp.simplify(row/plot).is_number
            for x,y in shown['samples']: assert abs(float(row.subs({X:x,Y:y})))<1e-9
        assert side['png_dimensions']==[620,540]
        step=side['data']['tick_increment']; assert all(t % step == 0 for values in side['major_ticks'].values() for t in values)
        if q[':question/difficulty'].endswith('/hard'):
            assert step==2 and all(v % 2 == 1 for v in vals)
    # Content digest independently recomputed from actual display and bank.
    actual=g.digest({'version':g.VERSION,'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],
                     'bank':[f[':answer-field/choices'][0][':answer/value'] for f in q[':question/answer-fields']]})
    assert actual==r['generation']['content_fingerprint']
    return vals

def normalize_source(raw,assets):
    s=raw
    rows=re.search(r'\$\{(.*?)\$',s).group(1).split('; ')
    system='$$\n'+r'\left\{\begin{array}{l}'+rows[0]+r'\\'+rows[1]+r'\end{array}\right.'+'\n$$'
    s=re.sub(r'\$\{.*?\$',lambda _:system,s,count=1)
    # Authoritative tuple shows exactly two entries, comma, parentheses, period.
    s=s[:s.index('The solution is')]+ 'The solution is\n$($ {{field-1}} $,$ {{field-2}} $)$.'
    s=re.sub(r'!\[\]\(.*?\)',lambda _:'![]('+assets['prompt']+')',s)
    return s

def main():
    sources=json.loads((HERE/'source.json').read_text()); cases=json.loads((HERE/'source-cases.json').read_text())
    assert (HERE/'source.json').read_bytes()==Path('generate/runs/current/sources/17592186138428.json').read_bytes()
    assert sources['database']=='math' and sources['basis']==1356 and sources['lineage']==g.SOURCE['lineage']
    questions={q[':question/math-academy-id']:q for q in sources['record'][':knowledge-point/questions']}
    records=[]; replay=[]
    for case in cases:
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        assert [str(v) for v in check(r)]==case['expected_entries']
        raw=questions[case['source_id']]
        assert normalize_source(raw[':question/problem'],r['generation']['plot_assets'])==r['question'][':question/problem']
        assert sorted(f[':answer-field/key'] for f in raw[':question/answer-fields'])==['field-1','field-2']
        assert all(f[':answer-field/type'][':db/ident']==':answer-field.type/blank' for f in raw[':question/answer-fields'])
        assert ':question/worked-solution' not in raw and all(':answer-field/correct' not in f for f in raw[':question/answer-fields'])
        replay.append({'source_id':case['source_id'],'record':r}); records.append(r)
    # Fixed solution prose comes from canonical in its complete original sequence.
    canonical=sources['record'][':knowledge-point/canonical-example'][':question/worked-solution']
    for r in records:
        expected=re.sub(r'!\[\]\(.*?\)',lambda _:'![]('+r['generation']['plot_assets']['solution']+')',canonical)
        p=r['generation']['parameters']; expected=expected.replace('(4,2)',f"({p['x']},{p['y']})")
        assert expected==r['question'][':question/worked-solution']
    review=[]
    for level in g.LEVELS:
        for template in g.TEMPLATES:
            for seed in ((17,7) if level=='hard' else (17,83)):
                r=g.generate(level,seed,template); check(r); records.append(r); review.append(r)
        # Enumerate all candidates for documented scope. No plots needed for these.
        for template in g.TEMPLATES:
            for p in g.domain(level,template):
                assert g.validate_parameters(level,template,p)==p
                a,b=g.equations(p,template)[0]
                assert a[0]*b[1]!=a[1]*b[0]
    for level,p in [('easy',{'x':0,'y':2,'m1':'-1','m2':'1'}),('moderate',{'x':5,'y':2,'m1':'-1','m2':'1'}),('moderate',{'x':2,'y':3,'m1':'-1','m2':'1'}),
                    ('hard',{'x':1,'y':2,'m1':'-3','m2':'1'}),('hard',{'x':1,'y':2,'m1':'3','m2':'3'})]:
        try: g.generate(level,parameters=p)
        except ValueError: pass
        else: raise AssertionError('Invalid explicit parameters were accepted')
    for r in records:
        args=(r['question'][':question/difficulty'].split('/')[-1],)
        identical=g.generate(*args,seed=999,template=r['generation']['template'],parameters=r['generation']['parameters'],profile='authored')
        assert identical['question'][':question/id']==r['question'][':question/id']
    # Equivalent layouts of same underlying lines have one mathematical fingerprint.
    p={'x':2,'y':3,'m1':'-1','m2':'2'}
    a=g.generate('easy',template='standard_standard',parameters=p); b=g.generate('easy',template='standard_slope',parameters=p)
    assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
    assert a['question'][':question/id']!=b['question'][':question/id']
    p={'x':-1,'y':3,'m1':'-1','m2':'2'}
    unit=g.generate('moderate',template='standard_standard',parameters=p); scaled=g.generate('hard',template='standard_standard',parameters=p)
    assert unit['generation']['mathematical_fingerprint']!=scaled['generation']['mathematical_fingerprint']
    # Fresh writes into a unique private folder: identical and different instances
    # concurrently. Never deletes/prunes normal plot caches or sibling assets.
    with tempfile.TemporaryDirectory(prefix='concurrent-',dir=HERE) as tmp:
        data=[records[0]['generation']['plot_data']]*2+[records[1]['generation']['plot_data']]*2
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            maps=list(pool.map(lambda d:g.render_plots(d,tmp),data))
        for d,paths in zip(data,maps):
            for path in paths.values(): assert json.loads(Path(path).with_suffix('.json').read_text())['data']==d
        assert not list(Path(tmp).glob('input-*')) and not list(Path(tmp).glob('atomic-*'))
    fixtures=[]
    for i,r in enumerate(records):
        checks=[]
        for j,v in enumerate(check(r)):
            equivalent=f'({int(v)*3})/3' if v else '1-1'
            checks += [{'field_index':j,'submitted':str(v),'expected':'accepted','purpose':'canonical coordinate'},
                       {'field_index':j,'submitted':equivalent,'expected':'accepted','purpose':'unreduced arithmetic equivalent coordinate'},
                       {'field_index':j,'submitted':str(v+1),'expected':'rejected','purpose':'incorrect coordinate'}]
        fixtures.append({'label':f'record-{i}','record':r,'checks':checks})
    (HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
    engine=Path('generate/runs/current/check-engine')
    subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    (HERE/'source-replays.json').write_text(json.dumps(replay,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    reviewtext=['# Graphical-system generator review','All level labels below are authored; both practice captures are unrated.']
    for case,r in zip(cases,records):
        raw=questions[case['source_id']]
        reviewtext += ['\n## Original '+case['source_id'],'Raw capture preserved verbatim (malformed TeX):','```markdown',raw[':question/problem'],'```',
                      '\n![](source-images/'+case['source_id']+'.png)','\n### Presentation-normalized replay; answers and solution independently derived',g.markdown(r)]
    for r in review:
        reviewtext += ['\n## Generated authored '+r['question'][':question/difficulty'].split('/')[-1]+' — '+r['generation']['template'],g.markdown(r)]
    (HERE/'review.md').write_text('\n\n'.join(reviewtext)+'\n')
    report={'status':'pass','database':'math','basis':1356,'source_questions':2,'source_coverage':{'replayed':2,'total':2},
            'fidelity':{'raw_exact_prompts':{'matched':0,'total':2},'presentation_normalized_prompts':{'matched':2,'total':2},
                        'field_layouts':{'matched':2,'total':2},'source_values':{'matched':0,'available':0},
                        'source_correct_designations':{'matched':0,'available':0},'missing_corrects_independently_derived':4,
                        'source_worked_solutions':{'matched':0,'available':0},'canonical_solution_prose_instantiations':2},
            'verified_records':len(records),'authored_review_records':len(review),'finite_domain_counts':{l:{t:len(g.domain(l,t)) for t in g.TEMPLATES} for l in g.LEVELS},
            'finite_unique_line_and_scale_tasks':{l:len({g.digest({'lines':sorted(g.equations(p,t)[0]),'major_tick_increment':2 if l=='hard' else 1,'minor_grid_increment':1}) for t in g.TEMPLATES for p in g.domain(l,t)}) for l in g.LEVELS},
            'finite_unique_coordinate_answers':{l:len({(p['x'],p['y']) for t in g.TEMPLATES for p in g.domain(l,t)}) for l in g.LEVELS},
            'native_grading':json.loads((HERE/'engine-report.json').read_text()),'concurrent_fresh_pngs':'passed; 4 concurrent calls, 2 identical pairs',
            'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest(),
            'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'unresolved_source_evidence':'Source difficulties, correct designations and practice solutions not supplied; derived values are not source matches.'}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 2/2 source normalized prompt/layout replays; 14 displayed systems/PNGs; 12 authored E/M/H reviews; native grading; fresh concurrent plots.')
if __name__=='__main__':main()

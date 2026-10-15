"""Independent readback of rendered surface, domain, calculus, banks and grading."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.dont_write_bytecode=True

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'surface_area_generator')
b=load(ROOT/'generate/runs/current/surface-calculus-reader.py','surface_area_reader')
u,v=s.symbols('u v',nonnegative=True)
b.u=u;b.v=v;b.p.locals_.update(u=u,v=v)

def scalar(raw):return b.math(raw)
def eq(a,c):return s.simplify(s.factor(a)-s.factor(c))==0

def vec(raw):
    return s.Matrix([scalar(x) for x in raw.strip().rstrip('.,').removeprefix('⟨').removesuffix('⟩').split(r',\,')])

def fingerprint(q):return g.fingerprint(q)

def parse_prompt(q):
    text=q[':question/problem'];m=re.search(r'r\(u,v\)=(⟨[^⟩]+⟩)',text)
    if m:coords=vec(m[1])
    else:coords=s.Matrix([scalar(re.search(r'\b'+axis+r'=(.*?)(?=,\\,|\n)',text)[1]) for axis in 'xyz'])
    disk=re.search(r'\{u\}\^\{2\}\+\{v\}\^\{2\}\\le (\d+)',text)
    if disk:bounds={'radius_squared':s.Integer(disk[1])}
    else:
        bounds={}
        for axis in ('u','v'):
            m=re.search(r'(-?\d+)\\le '+axis+r'\\le (.*?)(?=\$|,)',text)
            bounds[axis]=[scalar(m[1]),scalar(m[2].rstrip('.'))]
    return coords,bounds

def independent(rec,replay=True):
    q=rec['question'];meta=rec['generation'];assert rec['knowledge_point']['db_id']==g.KP_ID
    if replay:assert rec==g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'])
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        assert not re.search(r'[\x00-\x08\x0b-\x1f\x7f]',text),'Control character'
    coords,bounds=parse_prompt(q);ru,rv=coords.diff(u),coords.diff(v);cross=ru.cross(rv);metric=s.simplify(s.sqrt(s.factor(cross.dot(cross))))
    if 'radius_squared' in bounds:
        assert not metric.free_symbols and bounds['radius_squared']>0
        domain_area=s.pi*bounds['radius_squared'];answer=metric*domain_area
    else:
        assert all(lo<hi for lo,hi in bounds.values())
        answer=s.integrate(metric,(u,*bounds['u']),(v,*bounds['v']));domain_area=s.prod(hi-lo for lo,hi in bounds.values())
    assert answer>0
    sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
    vectorblock=next((block for block in blocks if block.startswith('r(u,v)=')),None)
    if vectorblock:assert vec(vectorblock.split('=',1)[1])==coords
    derivative=next(block for block in blocks if '{r}_{u}^{′} & =' in block)
    operands=re.findall(r'\\frac\{∂\}\{∂([uv])\}\((.*?)\)(?=,\\,|⟩)',derivative)
    assert len(operands)==6
    for i,((axis,raw),coordinate) in enumerate(zip(operands,list(coords)*2)):
        assert axis==('u' if i<3 else 'v') and eq(scalar(raw),coordinate)
    evaluated=[raw for raw in re.findall(r' & =(⟨[^⟩]+⟩)',derivative) if '∂' not in raw]
    assert len(evaluated)==2 and vec(evaluated[0])==ru and vec(evaluated[1])==rv
    product=next(block for block in blocks if '{r}_{u}^{′}\\times {r}_{v}^{′} & =' in block)
    arrays=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',product,re.S)
    mats=[s.Matrix([[scalar(x) for x in row.split('&')] for row in raw.split(r'\\')]) for raw in arrays]
    assert len(mats)==4 and mats[0][1:,:]==s.Matrix([list(ru),list(rv)])
    for M,(i,j) in zip(mats[1:],((1,2),(0,2),(0,1))):assert M==s.Matrix([[ru[i],ru[j]],[rv[i],rv[j]]])
    assert vec(re.findall(r' & =(⟨[^⟩]+⟩)',product)[-1])==cross
    norm=next(block for block in blocks if block.startswith(r'\begin{aligned}‖'))
    assert vec(re.search(r'‖(⟨[^⟩]+⟩)‖',norm)[1])==cross
    for raw in norm.split(' & =')[2:]:assert eq(scalar(raw.split(r'\\')[0].split(r'\end{aligned}')[0]),metric)
    domainblock=next(block for block in blocks if block.startswith('D='))
    if 'radius_squared' in bounds:
        assert int(re.search(r'\\le (\d+)',domainblock)[1])==bounds['radius_squared']
        radius=scalar(re.search(r'of radius \$(.*?)\.\$',sol)[1]);assert eq(radius**2,bounds['radius_squared'])
    else:
        for axis in ('u','v'):
            part=domainblock.split(r'\,:\,')[1].removesuffix('}.').split(r',\,')[0 if axis=='u' else 1]
            m=re.fullmatch(r'(-?\d+)\\le '+axis+r'\\le (.*)',part)
            assert [scalar(m[1]),scalar(m[2])]==bounds[axis]
    # Every displayed area row is an expression for the same complete area.
    finalblocks=[block for block in blocks if block.startswith(r'\begin{aligned}{∬}_{S}')]
    primitives=[];rows_checked=0
    for block in finalblocks:
        body=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
        for row in body.split(r'\\'):
            raw=re.split(r'&\s*=',row,maxsplit=1)[1].strip()
            raw=raw.replace(r'\text{Area}(D)','('+s.latex(domain_area)+')').replace('\\text{\u00a0}','1')
            if 'radius_squared' in bounds:
                # Constant metric only; use a same-area rectangle solely to
                # evaluate the printed integral over the independently read disk.
                rbounds={u:(0,domain_area),v:(0,1)}
            else:rbounds={u:tuple(bounds['u']),v:tuple(bounds['v'])}
            if 'w' in raw:
                raw=raw.replace('w','v');rbounds={u:(0,1),v:(1,4)}
            raw=raw.replace(r'{∬}_{D}\text{d}A',r'{∬}_{D}1\text{d}A')
            reader=b.Reader(1,metric,rbounds)
            val=reader.value(raw);assert eq(val,answer),(meta['template'],meta['parameters'],raw,val,answer)
            rows_checked+=1
            for primitive,var,lo,hi,printed in reader.primitives:
                if 'w' in row:expected=s.sqrt(v)
                elif var==u:expected=metric
                else:expected=s.integrate(metric,(u,*bounds['u']))
                assert eq(s.diff(primitive,var),expected),(printed,expected)
                primitives.append((primitive,var,lo,hi))
    if meta['template']=='q-109712':
        assert r'w={v}^{2}+1\,⇒\,\text{d}w=2v\,\text{d}v' in sol
        assert len(primitives)==1
    elif meta['template']=='q-109761':assert len(primitives)==2
    else:assert len(primitives)==0
    # Source prose and operative stages are kept at every nonanchor scale.
    original=g.CASES[meta['template']][':question/worked-solution']
    prose=lambda x:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','[MATH]',x,flags=re.S)).strip()
    assert prose(sol)==prose(original)
    assert len(finalblocks)==len([x for x in re.findall(r'\$\$(.*?)\$\$',original,re.S) if r'\begin{aligned}{∬}_{S}' in x])
    assert [len(x.split(r'\\')) for x in finalblocks]==[len(x.split(r'\\')) for x in re.findall(r'\$\$(.*?)\$\$',original,re.S) if r'\begin{aligned}{∬}_{S}' in x]
    f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(values)==5 and all(not eq(a,c) for a,c in itertools.combinations(values,2))
    assert [a[':answer/id'] for a,val in zip(f[':answer-field/choices'],values) if eq(val,answer)]==[f[':answer-field/correct'][1]]
    # Derive scale from the rendered domain/integral, without generator math_data.
    anchor=g.CASES[meta['template']];old_answer=scalar(anchor[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])
    scale=s.simplify(answer/old_answer)
    expected=[scalar(a[':answer/value'])*scale for a in anchor[':question/answer-fields'][0][':answer-field/choices']]
    assert all(eq(a,c) for a,c in zip(values,expected))
    assert meta['mathematical_fingerprint']==fingerprint(q)
    return {'rows':rows_checked,'choices':len(values),'area':str(answer),'fingerprint':fingerprint(q)}

check=independent
def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual learner radio grading of every bank choice'} for a in f[':answer-field/choices']]

def main():
    results=[];native=[];replays=[];recipes=[];review=[];coverage={};fps=set()
    for sid,old in g.CASES.items():
        level=g.LEVEL[sid];rec=g.generate(level,0,sid,[1]);q=rec['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
        assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
        replays.append({'source':sid,'complete_bank':True,'matched_choices':5,'matched_distractors':4,'missing':[],'extra':[],'prompt_exact':True,'solution_exact':True,'correct_designation':True})
        for a in of[':answer-field/choices']:
            recipes.append({'source':sid,'source_answer_id':a[':answer/id'],'field':'selection','profile':sid,'original_value':a[':answer/value'],'recipe':'('+a[':answer/value']+') * area_scale','observed_at_source':'area_scale=1','normal_extension':'common positive multiplier on a complete bank, derived from new/old area','interpretation':'opaque observed value pattern; psychological error unresolved','source_reproduced':True})
        for p in g.domain(sid):
            rec=g.generate(level,119888,sid,p);r=independent(rec);assert r['fingerprint'] not in fps;fps.add(r['fingerprint']);results.append(r)
            assert g.generate(level,99,sid,p)['question']==rec['question']
            native.append({'label':sid+' '+str(p),'record':rec,'checks':checks(rec)})
        coverage[sid]={'domain_slot_values':[p[0] for p in g.domain(sid)],'eligible_missing':[],'fixed_roles':'same supplied surface, same requested area, same six partials and signed cofactor work','changed_domain_test':'t=1 and t=2 hold surface fixed and independently reread prompt/domain/solution/key'}
        review.append('## '+sid+'\n\nSource\n\n'+g.markdown(g.generate(level,0,sid,[1]))+'\n\nChanged domain; identical surface\n\n'+g.markdown(g.generate(level,0,sid,[2])))
    # Mutations must fail independent rendered readback, without deterministic replay.
    base=g.generate('hard',0,'q-105922',[2]);mutations=[]
    for name,mutate in [('stale radius',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('of radius $2 \\sqrt{2}.$','of radius $2.$'))),('wrong correct',lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']])),('control',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\x0c'))]:
        r=copy.deepcopy(base);mutate(r);assert r!=base,name
        try:independent(r,False)
        except (AssertionError,ValueError):mutations.append(name)
        else:raise AssertionError('Mutation passed: '+name)
    for level in ('easy','unclassified'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported level accepted')
    for level in g.SUPPORTED_LEVELS:
        assert len({g.generate(level,i)['generation']['template'] for i in range(60)})==4
        try:g.batch(level,25,1)
        except ValueError:pass
        else:raise AssertionError('Finite count silently duplicated')
    def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
    save('source-replay.json',{'passed':True,'complete_banks_matched':8,'complete_banks_total':8,'distractors_matched':32,'distractors_total':32,'profiles':replays})
    save('choice-recipes.json',recipes);save('slot-coverage.json',coverage);save('native-input.json',native)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'status':'pass','passed':True,'instances':len(results),'distinct_tasks':len(fps),'displayed_area_rows':sum(r['rows'] for r in results),'supported_levels':list(g.SUPPORTED_LEVELS),'source_fidelity':'8/8 complete banks, 32/32 distractors, exact source prompt and solution replay','correctness':'independent rendered surface/domain reads, partial operands/results, determinants/minors, norm stages, all area rows, primitive derivatives and distinct complete banks','grading':'native application grade_field for all 240 choices','mutation_failures':mutations,'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'replenish.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine')}})
if __name__=='__main__':main()

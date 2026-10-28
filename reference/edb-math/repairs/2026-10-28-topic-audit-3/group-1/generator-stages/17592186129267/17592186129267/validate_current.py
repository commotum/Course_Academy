"""Independent displayed-prompt and whole-bank checks for current inventory."""
import copy,hashlib,importlib.util,json,re
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cylindrical_validation',D/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g

def expected(q):
    prompt=q[':question/problem'].replace(r'\geq',r'\ge').replace(r'\leq',r'\le')
    S=int(re.search(r'(?:\{y\}\^\{2\}|y\^2|y\^\{2\})\s*=\s*(\d+)',prompt)[1]);R=s.sqrt(S)
    block=prompt.split('$$')[1].replace(r'\displaystyle','').replace(r'\limits','')
    block=re.sub(r'.*?(?:\{∭\}_\{R\}|\\iiint_R)\s*','',block,flags=re.S)
    fragment=re.split(r'\\(?:,|:|;|mathrm|text)',block)[0].strip();F=v.expr(fragment) if fragment else s.Integer(1)
    heights=re.findall(r'\$z\s*=\s*(.*?)\$',prompt);assert len(heights)==2
    lo,hi=[v.expr(w.rstrip('.,')) for w in heights]
    xpos=bool(re.search(r'x\s*\\ge\s*0',prompt));xneg=bool(re.search(r'x\s*\\le\s*0',prompt));ypos=bool(re.search(r'y\s*\\ge\s*0',prompt))
    if xneg:a,b=(s.pi/2,s.pi) if ypos else (s.pi/2,3*s.pi/2)
    elif xpos:a,b=(0,s.pi/2) if ypos else (-s.pi/2,s.pi/2)
    elif ypos:a,b=0,s.pi
    else:a,b=0,2*s.pi
    subs={g.x:g.r*s.cos(g.theta),g.y:g.r*s.sin(g.theta)}
    convert=lambda x:s.refine(s.trigsimp(s.sympify(x).subs(subs,simultaneous=True)),s.Q.nonnegative(g.r))
    return (a,b,R,convert(lo),convert(hi),convert(F)*g.r)

def equal(a,b):return s.trigsimp(s.sympify(a)-s.sympify(b))==0

def task(q):
    # Bounds, integrand and radial lower define the requested setup. No IDs,
    # seed, level, bank, solution, equivalent spelling or choice order included.
    return tuple(str(s.trigsimp(s.sympify(a))) for a in expected(q))

def validate(rec,generated=True):
    q=rec['question'];want=expected(q)
    if generated:
        assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
        g.allowed(rec['generation']['template'],rec['generation']['parameters']);v.verify(rec)
    assert len(q[':question/answer-fields'])==1,'duplicate legacy answer fields'
    f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5 and f[':answer-field/correct']
    objects=[v.parse_integral(a[':answer/value']) for a in f[':answer-field/choices']]
    correct=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
    obj,rl=objects[correct];assert rl==0 and all(equal(a,b) for a,b in zip(obj,want)),'incorrect complete integral'
    assert g.whole_bank_ok([o for o,rl in objects],[rl for o,rl in objects])[0],'equivalent or nonreal complete integral options'
    sol=q[':question/worked-solution'];assert sol
    heights=re.findall(r'bounded (?:below|above) by \$z=(.*?)\$',sol);assert len(heights)==2
    for raw,bound in zip(heights,want[3:5]):
        parts=raw.rstrip('.,').split('=',1)
        converted=v.expr(parts[0]).subs({g.x:g.r*s.cos(g.theta),g.y:g.r*s.sin(g.theta)},simultaneous=True)
        assert equal(converted,bound) and equal(v.expr(parts[-1]),bound),'stale verbal height reference'
    if generated:
        original=Path(g.projection(rec['generation']['template'],rec['generation']['parameters']))
        side=json.loads(original.with_suffix('.json').read_text())
        assert side['equal_scale'] and side['S']==rec['generation']['parameters']['S']
        assert all(equal(s.sympify(a),b) for a,b in zip(side['theta'],want[:2])),'stale projection sector'
        shown=Path(re.search(r'!\[\]\((.*?)\)',sol)[1])
        if not shown.is_absolute():
            shown=Path('/media/jake/SSD/EDB/math')/shown if shown.parts[0]=='images' else D.parents[2]/shown
        assert hashlib.sha256(shown.read_bytes()).digest()==hashlib.sha256(original.read_bytes()).digest(),'stale projection asset'
    # All printed cylindrical integrand stages must agree with the prompt.
    chain=sol.split(r'\begin{aligned}')[-1].split(r'\end{aligned}')[0]
    for row in chain.split(chr(92)*2):
        if '{∭}_{Δ}' in row:rhs=row.split('{∭}_{Δ}')[1]
        elif r'\iiint_\Delta' in row:rhs=row.split(r'\iiint_\Delta')[1]
        else:continue
        rhs=re.split(r'\\,?dz|dz',rhs)[0].rstrip(' '+chr(92)+',')
        assert equal(v.expr(rhs),want[5]),'incorrect worked-solution intermediate'
    # Final integral independently read back from the actual solution.
    start=chain.find(r'{\int }_');assert start>=0
    final,rl=v.parse_integral(chain[start:]);assert rl==0 and all(equal(a,b) for a,b in zip(final,want)),'incorrect final solution bounds'
    return task(q)

def checks(rec):
    out=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            out.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'field-owned radio selection'})
    return out

"""Parent actual linear-denominator/log-absolute substitution and bank readback."""
import hashlib, importlib.util, itertools, json, re, sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064206;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
P=load(R/'qa-substitution-integrals.py','rational_integral_reader');G=load(D.with_suffix('.py'),'rational_integral_generator');originals,SC=P.FID.check(G,K,D)
x,u=P.P.x,P.P.u
def primitive(raw,inner):
    text=raw.strip().rstrip('.,').replace(r'\mid','|').replace(r'\left','').replace(r'\right','').replace('⁡','')
    text=re.sub(r'\+\s*C\s*$','',text)
    match=re.fullmatch(r'(.*?)(?:\\operatorname\{ln\}|\\ln)\s*\|([^|]+)\|',text);assert match,('Unsupported actual primitive',raw)
    coefficient=P.factor(match[1]);argument=P.scalar(match[2]);assert argument!=0
    var=u if argument.has(u) else x
    # d(log|g|)/dx = g'/g on EACH real nonzero connected interval.
    derivative=s.cancel(coefficient*s.diff(argument,var)/argument)
    if var==u:derivative=s.cancel(derivative.subs(u,inner)*s.diff(inner,x))
    return derivative
C=dict(records=0,actual_integrands=0,actual_substitutions=0,actual_differential_relations=0,operative_integral_sides=0,primitive_sides=0,choice_values=0,criterion_pairs=0,source_prose_masks=0)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for row in json.load(open(D/'review.json')):
    r=row.get('record',row)
    if 'question'in r and not r['generation'].get('evidence_only',False):records.append(r)
for r in records:
    q=r['question'];sol=q[':question/worked-solution'];F,var,_=P.integral(q[':question/problem']);assert var==x;C['actual_integrands']+=1
    definition=re.search(r'let \$u=([^$]+)\$',sol);assert definition;inner=P.scalar(definition[1]);assert s.Poly(inner,x).degree()==1
    coefficient=s.cancel(F*inner);assert coefficient.free_symbols==set() and coefficient!=0;A=s.diff(inner,x);assert A!=0;C['actual_substitutions']+=1
    derivative=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)\\,⟹',sol);assert derivative and P.equal(P.scalar(derivative[1]),A)
    inverse=re.search(r'⟹\\,\\text\{d\}x=(.*?)\\text\{d\}u',sol)
    if inverse:assert P.equal(P.factor(inverse[1])*A,1)
    else:
        direct=re.search(r'⟹\\,\\text\{d\}u=(.*?)\\text\{d\}x',sol)
        assert direct and P.equal(P.factor(direct[1]),A),(r['generation'],sol)
    C['actual_differential_relations']+=2
    blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);seen_primitive=False
    for block in blocks:
        if r'\int'not in block:continue
        block=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
        for row in block.split(chr(92)*2):
            for side in row.split('='):
                side=side.strip().rstrip('.,')
                if not side:continue
                if r'\int'in side:
                    f,v,match=P.integral(side);actual=P.factor(side[:match.start()])*f
                    if v==u:actual=actual.subs(u,inner)*A
                    else:assert v==x
                    assert P.equal(actual,F),('Wrong operative integral',side);C['operative_integral_sides']+=1
                else:assert P.equal(primitive(side,inner),F),('Wrong primitive stage',side);C['primitive_sides']+=1;seen_primitive=True
    assert seen_primitive
    def prose_mask(text):return re.sub(r'\s+',' ',re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$','<MATH>',text)).strip()
    assert prose_mask(sol) in [prose_mask(o[':question/worked-solution']) for o in originals.values() if ':question/worked-solution' in o]
    C['source_prose_masks']+=1
    for field in q[':question/answer-fields']:
        values=[primitive(a[':answer/value'],inner)for a in field[':answer-field/choices']]
        for a,v in zip(field[':answer-field/choices'],values):assert P.equal(v,F)==(a[':answer/id']==field[':answer-field/correct'][1]);C['choice_values']+=1
        for a,b in itertools.combinations(values,2):assert not P.equal(a,b),'Equivalent log-absolute choices moduloC';C['criterion_pairs']+=1
    C['records']+=1
result=dict(status='passed',source=SC,readback=C,domain_proof='real affine log arguments nonzero on connected intervals; log|k*g| has the same derivative, never an independent distractor',generator_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0)
(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

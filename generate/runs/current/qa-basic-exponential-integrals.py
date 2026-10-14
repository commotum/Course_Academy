"""Parent reads constant/general-base integral stages and all derivative-class banks."""
import hashlib, importlib.util, itertools, json, re, sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
P=load(R/'qa-substitution-integrals.py','root_elementary_integral_reader')
def mask(text): return re.sub(r'\s+',' ',re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$','<MATH>',text)).strip()
def check(K):
    D=ROOT/f'generate/scratch/{K}';G=load(D.with_suffix('.py'),'basic_exp_'+str(K));originals,S=P.FID.check(G,K,D)
    records=json.load(open(R/f'qa/{K}-sampled.json'))
    for row in json.load(open(D/'review.json')):
        r=row.get('record',row)
        if 'question'in r and not r['generation'].get('evidence_only',False):records.append(r)
    cases=json.load(open(D/'source-cases.json'));C=dict(records=0,actual_integrands=0,operative_integral_sides=0,primitive_sides=0,choice_values=0,criterion_pairs=0,source_prose_masks=0)
    for r in records:
        q=r['question'];F,x,_=P.integral(q[':question/problem']);sol=q[':question/worked-solution'];C['actual_integrands']+=1
        if K==17592186064171:
            coefficient=s.simplify(F/s.exp(x));assert coefficient.free_symbols==set()
            lev=q[':question/difficulty'].split('/')[-1]
            assert coefficient.is_Integer if lev=='easy' else coefficient.is_Rational and not coefficient.is_Integer if lev=='moderate' else coefficient.has(s.pi)
            candidates=[o for o in originals.values() if ':question/worked-solution'in o]
            assert mask(sol) in [mask(o[':question/worked-solution'])for o in candidates];C['source_prose_masks']+=1
        else:
            assert len(F.atoms(s.Pow))>=1
        primitives=0
        for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
            # Rule displays in the general-base sources use a symbolic base;
            # operative numeric chains are checked here and formal rules separately.
            if r'\int'not in block or re.search(r'(?<![A-Za-z])[ab](?:\^|\})',block):continue
            block=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
            for row in block.split(chr(92)*2):
                for side in row.split('='):
                    side=side.strip().rstrip('.,')
                    if not side:continue
                    if r'\int'in side:
                        val,var,match=P.integral(side);assert var==x
                        actual=P.factor(side[:match.start()])*val;assert P.equal(actual,F),(K,'Wrong operative integral',side);C['operative_integral_sides']+=1
                    else:
                        primitive=P.scalar(side);assert P.equal(s.diff(primitive,x),F),(K,'Wrong displayed primitive',side);primitives+=1;C['primitive_sides']+=1
        assert primitives>=1
        for f in q[':question/answer-fields']:
            vals=[s.diff(P.scalar(a[':answer/value']),x)for a in f[':answer-field/choices']]
            for a,v in zip(f[':answer-field/choices'],vals):assert P.equal(v,F)==(a[':answer/id']==f[':answer-field/correct'][1]);C['choice_values']+=1
            for a,b in itertools.combinations(vals,2):assert not P.equal(a,b),(K,'Two equivalent primitive choices');C['criterion_pairs']+=1
        C['records']+=1
    result=dict(status='passed',kp_id=K,source=S,readback=C,generator_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0)
    (R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':
    for k in map(int,sys.argv[1:]):check(k)

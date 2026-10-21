"""Independent read-only review. Run with context Python and -B; artifacts stay here."""
import ast
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import sympy as S

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
REPO = Path('/home/jake/Developer/Course_Academy')
PACKAGE = BASE/'workspace'
PYTHON = REPO/'.venv/bin/python'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True
commands = []

def save(name, data):
    (ROOT/name).parent.mkdir(parents=True, exist_ok=True)
    (ROOT/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')

def run(args, name, timeout=60, cwd=ROOT):
    p = subprocess.run([str(x) for x in args], cwd=cwd, env=ENV, text=True,
                       capture_output=True, timeout=timeout)
    d = dict(command=[str(x) for x in args], cwd=str(cwd), returncode=p.returncode,
             stdout=p.stdout, stderr=p.stderr)
    save(name, d); commands.append(d); save('commands.json', commands)
    return p

def hash_package():
    return {str(p.relative_to(PACKAGE)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(PACKAGE.rglob('*')) if p.is_file()}

def load_generator(directory):
    sys.path.insert(0,str(directory))
    spec=importlib.util.spec_from_file_location('reviewed_generator',directory/'generator.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    sys.path.pop(0)
    return module

def tex_expr(value):
    """Small independent parser for this source's rational/ln expression grammar."""
    text=value.replace('\\operatorname{ln}',r'\ln').replace('\u2061','')
    text=text.replace(r'\left','').replace(r'\right','')
    def group(t,i):
        assert t[i]=='{',t
        level=1;j=i+1
        while level:
            level+=(t[j]=='{')-(t[j]=='}');j+=1
        return t[i+1:j-1],j
    while r'\frac' in text:
        i=text.index(r'\frac');top,j=group(text,i+5);bottom,k=group(text,j)
        replacement='(('+tex_expr_text(top)+')/('+tex_expr_text(bottom)+'))'
        text=text[:i]+replacement+text[k:]
    return S.sympify(tex_expr_text(text))

def tex_expr_text(text):
    if r'\frac' in text:
        return str(tex_expr(text))
    text=text.replace(r'\ln', 'log').replace('{','(').replace('}',')')
    text=re.sub(r'(?<=\d)(?=log\(|[xyt]|\()', '*', text)
    text=re.sub(r'\)(?=log\(|[xyt]|\()', ')*', text)
    return text

def inspect_record(record):
    q=record['question'];p=q[':question/problem']
    match=re.search(r'e\^\{([^}]+)\}\s*=\s*(\d+)',p.replace('{e}','e')); assert match,p
    exp,n=match[1],int(match[2]);v=next(c for c in exp if c in 'xyt');v_symbol=S.Symbol(v)
    polynomial=S.Poly(tex_expr(exp),v_symbol)
    a,b=map(int,[polynomial.coeff_monomial(v_symbol),polynomial.coeff_monomial(1)])
    expected=(S.log(n)-b)/a
    f=q[':question/answer-fields'][0]
    assert f[':answer-field/type']==':answer-field.type/blank'
    assert f[':answer-field/key']=='field-1' and len(f[':answer-field/choices'])==1
    key=f[':answer-field/choices'][0][':answer/value']
    assert S.simplify(tex_expr(key)-expected)==0,(p,key,expected)
    sol=q[':question/worked-solution']
    # Independently check each equation in the final solve block, not metadata.
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
    rows=re.split(r'\\\\',blocks[-1]); row_results=[]
    for row in rows:
        lhs,rhs=row.replace('&','').strip().split('=',1)
        residual=S.simplify((tex_expr(lhs)-tex_expr(rhs)).subs(v_symbol,expected))
        assert residual==0,(p,row,residual)
        row_results.append(row)
    final=re.search(r'Therefore, the solution is \$[xyt]=(.*?)\.\$',sol,re.S)
    assert final and S.simplify(tex_expr(final[1])-expected)==0,(p,sol)
    assert ('\\ln(e^' in sol or '\\ln(e^' in sol.replace('{e}','e') or
            '\\operatorname{ln}' in sol or '\\ln (e^' in sol)
    return dict(a=a,b=b,n=n,variable=v,order='variable-first' if re.match(r'-?\d*[xyt]',exp) else 'constant-first',
                key=key,expected=str(expected),solution_rows=row_results,
                sign_case=('positive' if a>0 else 'negative')+'/'+('positive' if b>0 else 'negative'),
                value_sign='positive' if expected.evalf()>0 else 'negative')

def main():
    before=hash_package();save('package-before.json',before)
    gen=load_generator(PACKAGE)
    normal=gen.generate(64,791938)
    boundaries=[gen.build(a,b,n,v=('x','y','t')[i%3],order=('constant-first','variable-first')[i%2],seed='explicit-boundary')
                for i,(a,b,n) in enumerate(itertools.product((-7,-2,2,7),(-9,-1,1,9),(2,30)))]
    rhs=[gen.build(-5,4,n,seed='rhs-sweep') for n in range(2,31)]
    replay=gen.build(-5,4,21,replay=True,seed=791938)
    # Relevant changes modify one answer-bearing role at a time. Both signs included.
    pairs=[gen.build(-5,4,11,seed='controlled-base'),gen.build(5,4,11,seed='coefficient-sign'),
           gen.build(-5,-4,11,seed='offset-sign'),gen.build(-5,4,13,seed='rhs-change'),
           gen.build(-5,4,11,v='x',seed='rename'),gen.build(-5,4,11,order='variable-first',seed='reorder')]
    records=[replay]+normal+boundaries+rhs+pairs
    save('samples.json',records);save('counterfactual-samples.json',pairs)
    batch=json.loads((BASE/'samples.json').read_text());save('runner-batch.json',batch)
    analysis=[]
    for i,r in enumerate(records+batch):
        analysis.append(dict(index=i,**inspect_record(r)))
    save('math-results.json',dict(passed=True,records_checked=len(analysis),parser='prompt, keyed expression and each final worked equation independently parsed with exact SymPy arithmetic',cases=analysis))
    # Verify supported replay separately from the author's fixture.
    source=json.loads((BASE/'source/source.json').read_text())
    original=next(q for q in source['material']['kp'][':knowledge-point/questions'] if q[':question/id']==gen.SOURCE_ID)
    from math_format import normalize_prose,normalize_tex
    rq=replay['question'];comp={k:rq[k]==normalize_prose(original[k]) for k in (':question/problem',':question/worked-solution')}
    comp['complete_answer_bank']=[c[':answer/value'] for c in rq[':question/answer-fields'][0][':answer-field/choices']]==[normalize_tex(c[':answer/value']) for c in original[':question/answer-fields'][0][':answer-field/choices']]
    comp['field_type_and_key']=rq[':question/answer-fields'][0][':answer-field/key']==original[':question/answer-fields'][0][':answer-field/key'] and rq[':question/answer-fields'][0][':answer-field/type']==original[':question/answer-fields'][0][':answer-field/type'][':db/ident']
    comp['key_matches_original_choice']=rq[':question/answer-fields'][0][':answer-field/correct'][1]==rq[':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']
    assert all(comp.values()),comp
    save('source-replay-results.json',dict(source_id=gen.SOURCE_ID,comparisons=comp,original=original,replayed=replay,unsupported=['e-4103 (power RHS canonical)','q-66590 (unrated radio)','q-66595 (unrated radio)','q-100282 (easy)','q-66963 (hard root)','q-100280 (hard root radio)','q-100276 (hard root radio)'],scope='One explicitly supported moderate blank source; excluded bands and unrated radio families are not claimed as reproduced.'))
    # CLI determinism and relocation, no ambient repository helpers.
    cli=[PYTHON,'-B',PACKAGE/'generator.py','--count','8','--seed','791938']
    first=run(cli,'cli-first.json');second=run(cli,'cli-second.json');assert first.returncode==second.returncode==0 and first.stdout==second.stdout
    relocated=ROOT/'relocated-package';relocated.mkdir(exist_ok=True)
    manifest=json.loads((PACKAGE/'package.json').read_text())
    for name in manifest['files']+['package.json']:shutil.copyfile(PACKAGE/name,relocated/name)
    rp=run([PYTHON,'-B',relocated/'generator.py','--count','8','--seed','791938'],'cli-relocated.json',cwd=relocated)
    assert rp.returncode==0 and rp.stdout==first.stdout
    failures=[]
    for args in [('--difficulty','easy'),('--difficulty','hard'),('--count','-1'),('--count','6265')]:
        p=run([PYTHON,'-B',PACKAGE/'generator.py',*args],f"cli-invalid-{'-'.join(args).replace('--','')}.json")
        assert p.returncode!=0;failures.append(dict(args=args,returncode=p.returncode))
    assert gen.generate(0,791938)==[]
    for params in [(0,4,21),(-1,4,21),(-8,4,21),(-5,0,21),(-5,10,21),(-5,4,1),(-5,4,31)]:
        try:gen.build(*params)
        except ValueError:continue
        raise AssertionError(params)
    # Full finite sampler: semantic deduplication/retry must finish and preserve all roles.
    domain=gen.generate(6264,791939)
    triples={tuple(r['generation']['parameters'][k] for k in ('a','b','n')) for r in domain}
    assert len(triples)==6264
    save('sampler-domain.json',dict(seed=791939,count=len(domain),semantic_triples=len(triples),sign_cases={s:sum(r['generation']['decision_case']==s for r in domain) for s in sorted({r['generation']['decision_case'] for r in domain})},domain_sha256=hashlib.sha256(json.dumps(sorted(triples)).encode()).hexdigest(),rejection='Only repeated semantic triples are resampled; no mathematical rejection branch.'))
    strict=[dict(label='source-q-263058-wrong-zero',record=replay,checks=[dict(submitted='0',expected='rejected',purpose='Ordinary wrong real answer must produce a grading decision')])]
    save('native-strict-input.json',strict)
    strict_run=run([REPO/'generate/runs/current/check-engine',ROOT/'native-strict-input.json',ROOT/'native-strict-report.json'],'native-strict-execution.json')
    # Current executable independently rejected source wrong-zero; require strict outcomes.
    cases=[]
    for i,r in enumerate(records+batch):
        m=analysis[i];a,b,n=m['a'],m['b'],m['n'];key=m['key']
        checks=[dict(submitted=key,expected='accepted',purpose='Stored exact key'),
                dict(submitted=f'(ln({n})-({b}))/({a})',expected='accepted',purpose='Independent grouped exact equivalent'),
                dict(submitted=f'({-b})/({a})+ln({n})/({a})',expected='accepted',purpose='Independent distributed exact equivalent'),
                dict(submitted='0',expected='rejected',purpose='Ordinary wrong real answer must be rejected, including RHS>=20'),
                dict(submitted=f'(ln({n})-({b}))',expected='rejected',purpose='Omitted division misconception')]
        cases.append(dict(label=f'independent-record-{i}',record=r,checks=checks))
    base_expected='(ln(11)-4)/(-5)'
    for i,r in enumerate(pairs):
        checks=[dict(submitted=base_expected,expected='accepted' if i in (0,4,5) else 'rejected',purpose='Controlled pair: original numeric answer must track relevant evidence and survive irrelevant presentation changes')]
        cases.append(dict(label=f'controlled-pair-{i}',record=r,checks=checks))
    save('native-diagnostic-input.json',cases)
    native=run([REPO/'generate/runs/current/check-engine',ROOT/'native-diagnostic-input.json',ROOT/'native-diagnostic-report.json'],'native-diagnostic-execution.json')
    save('render-samples.json',[replay]+pairs+[boundaries[-1]])
    versions=dict(python=sys.version.split()[0],manifest=manifest['dependencies'])
    assert versions['python']==manifest['dependencies']['python'] and manifest['dependencies']['packages']=={}
    save('packaging-results.json',dict(versions=versions,deterministic=True,relocation_matches=True,invalid_cli=failures,boundary_rejections=7,empty_count=True,external_outputs='CLI JSON stdout only; no assets; filesystem writes absent in generator code',before=before,after=hash_package(),unchanged=before==hash_package()))
    (ROOT/'session-state.md').write_text('Completed independent source replay, math (all sampled prompts/keys/worked solve equations), deterministic/relocated CLI, sampler finite-domain and packaging checks. Native strict source check and diagnostic inputs/results saved. Next: resolve diagnostic expectations if needed, run shared delivery and actual UI renderer, inspect screenshots, write distribution/variation/final reports.\n')
    print(json.dumps(dict(math_records=len(analysis),source_replay=comp,strict_grader_returncode=strict_run.returncode,diagnostic_grader_returncode=native.returncode,diagnostic_stderr=native.stderr[-1000:],package_unchanged=before==hash_package())))

if __name__=='__main__':main()

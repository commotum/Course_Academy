"""Independent display-derived algebra, full-bank fidelity and native grading."""
import copy, hashlib, importlib.util, json, math, re, subprocess, sys
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,data):(D/name).write_text(json.dumps(data,indent=2)+'\n')
def matrices(text):
    pattern=r'\\begin\{(array|bmatrix)\}(?:\{[^}]*\})?(.*?)\\end\{\1\}'
    return [[[int(n.strip()) for n in row.split('&')] for row in body.split('\\\\') if row.strip()] for _,body in re.findall(pattern,text,re.S)]
def systems(text):
    blocks=[]
    for body in re.findall(r'\$\$(.*?)\$\$',text,re.S):
        body=re.sub(r'\\(?:left|right)\s*(?:\\[{}]|[.\[\]()])','',body)
        body=re.sub(r'\\(?:begin|end)\{(?:aligned|cases)\}','',body).replace('{','').replace('}','').replace('&','').strip()
        if '=' in body and r'\begin{array}' not in body:blocks.append([row.strip() for row in body.split('\\\\') if row.strip()])
    return blocks
def equation_matrix(rows):
    variables=sp.symbols('x y z')[:3 if any('z' in row for row in rows) else 2]
    result=[]
    for row in rows:
        lhs,rhs=row.split('=');expr=sp.expand(sp.sympify(re.sub(r'(\d)([xyz])',r'\1*\2',lhs))-sp.sympify(re.sub(r'(\d)([xyz])',r'\1*\2',rhs)))
        coeff=[int(expr.coeff(x)) for x in variables];constant=int(-expr.subs({x:0 for x in variables}))
        assert expr==sum(c*x for c,x in zip(coeff,variables))-constant
        result.append(coeff+[constant])
    return result
def canonical_rows(rows):
    result=[]
    for row in rows:
        gcd=math.gcd(*row);row=[n//gcd for n in row];first=next(n for n in row if n);result.append(tuple(row if first>0 else [-n for n in row]))
    return sorted(result)
def fingerprint(q):return g.digest(canonical_rows(equation_matrix(systems(q[':question/problem'])[0])))
def display_check(rec):
    q=rec['question'];f=q[':question/answer-fields'][0];expected=equation_matrix(systems(q[':question/problem'])[0]);bank=[matrices(a[':answer/value'])[0] for a in f[':answer-field/choices']]
    correct=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);assert bank[correct]==expected
    assert len(bank)==5 and len({g.digest(z) for z in bank})==5
    for i,m in enumerate(bank):
        if i!=correct:assert len(m[0])!=len(expected[0]) or canonical_rows(m)!=canonical_rows(expected),'Equivalent distractor'
    solution=q[':question/worked-solution'];ms=matrices(solution);assert ms==[[row[:-1] for row in expected],expected]
    for rows in systems(solution):assert equation_matrix(rows)==expected
    for text in [q[':question/problem'],solution]+[a[':answer/value'] for a in f[':answer-field/choices']]:
        depth=0
        for c in re.findall(r'\\[A-Za-z]+|\\.|.',text,re.S):
            depth+=(c=='{')-(c=='}');assert depth>=0
        assert depth==0 and text.count('$')%2==0
    assert q[':question/difficulty'].split('/')[-1] in g.SUPPORTED
    return fingerprint(q)
def grade(records,path):
    path=Path(path);path.mkdir(parents=True,exist_ok=True)
    inputs=[]
    for r in records:
        f=r['question'][':question/answer-fields'][0]
        inputs.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned radio choice through actual learner grader'} for a in f[':answer-field/choices']]})
    (path/'native-input.json').write_text(json.dumps(inputs,indent=2))
    subprocess.run([str(D/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    report=json.loads((path/'native-report.json').read_text());assert report['accepted_checks']==len(records) and report['rejected_checks']==4*len(records) and report['documented_unresolved_checks']==0

def main():
    deps=ROOT/'target/release/deps';subprocess.run(['cargo','build','--release','--lib','--offline'],cwd=ROOT,check=True)
    libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
    cmd=['rustc','--edition=2024','-O',str(D/'check-engine.rs')]
    for n,p in libs.items():cmd+=['--extern',n+'='+str(p)]
    subprocess.run(cmd+['-L','dependency='+str(deps),'-o',str(D/'check-engine')],check=True)
    replays=[];summary=[];variants=[];coverage={};invalid_cases=[]
    for name,src in g.PROFILES.items():
        level=src[':question/difficulty'][':db/ident'].split('/')[-1];params={str(n):n for n in g.slots(src)}
        rec=g.generate(level,0,name,parameters=params);display_check(rec);replays.append(rec)
        original=src[':question/answer-fields'][0];bank=[matrices(a[':answer/value'])[0] for a in original[':answer-field/choices']];generated=[matrices(a[':answer/value'])[0] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']];assert bank==generated
        assert rec['question']==g.generate(level,99,name,parameters=params)['question'],'Seed-dependent identity'
        summary.append({'profile':name,'source_question':src[':db/id'],'choices_matched':5,'choices_total':5,'distractors_matched':4,'correct_verified':True,'missing':[],'extra':[]})
        cases=[g.generate(level,seed,name) for seed in range(100)]
        for n in params:
            for boundary in range(2,25):
                try:cases.append(g.generate(level,0,name,parameters={**params,n:boundary}))
                except AssertionError:invalid_cases.append({'profile':name,'slot':n,'value':boundary,'reason':'Colliding magnitudes/choices rejected with other slots fixed'})
                others=iter(v for v in range(2,25) if v!=boundary)
                independent={key:boundary if key==n else next(others) for key in params}
                cases.append(g.generate(level,0,name,parameters=independent))
        seen={n:set() for n in params}
        for r in cases:
            display_check(r)
            for n,v in r['generation']['parameters'].items():seen[n].add(v)
        coverage[name]={n:sorted(vals) for n,vals in seen.items()};assert all(len(vals)==23 for vals in seen.values())
        variants+=cases
    # Corrupted rendered key must be rejected by an independent prompt read.
    mutant=copy.deepcopy(variants[0]);f=mutant['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
    try:display_check(mutant)
    except AssertionError:pass
    else:raise AssertionError('Stale key mutation accepted')
    grade(replays+variants,D/'reference/validation')
    save('source-bank-replay.json',summary);save('slot-coverage.json',{'coverage':coverage,'rejected_invalid_cases':invalid_cases})
    review=[{'source_id':src[':db/id'],'source':src,'replay':replays[i],'variants':[g.generate(src[':question/difficulty'][':db/ident'].split('/')[-1],s,name) for s in (101,102)]} for i,(name,src) in enumerate(g.PROFILES.items())]
    save('review.json',review);(D/'review.md').write_text('\n\n---\n\n'.join('Source '+x['source'][':question/math-academy-id']+'\n\n'+x['source'][':question/problem']+'\n\n'+x['source'][':question/worked-solution']+'\n\nVariants\n\n'+'\n\n'.join(g.markdown(r) for r in x['variants']) for x in review))
    save('validation.json',{'status':'passed','source_basis':g.SOURCE['basis'],'complete_banks':7,'choices_matched':35,'distractors_matched':28,'source_replays':7,'independently_validated_variants':len(variants),'actual_grader_records':len(replays+variants),'supported_levels':list(g.SUPPORTED),'unsupported_levels':['hard'],'stale_key_mutation_rejected':True,'slot_coverage':'All magnitudes 2..24 for every declared slot','fidelity':'Complete banks and source mathematical/solution backbone; captured naked braces repaired','dependencies':{'python':sys.version,'sympy':sp.__version__}})
    save('freeze-hashes.json',{'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D.with_suffix('.py'),D/'source.json',D/'validate.py',D/'check-engine.rs',D/'check-engine',D/'validation.json',ROOT/'scripts/question_capture/math_format.py']}})
    print('Validated all seven source banks and',len(variants),'variants')
if __name__=='__main__':main()

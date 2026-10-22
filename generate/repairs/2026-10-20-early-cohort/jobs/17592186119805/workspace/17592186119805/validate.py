"""Independently read rendered vector equations, banks and solution steps."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scalar(v):
    v=v.replace(' ','')
    m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',v)
    return (-1 if m[1] else 1)*sp.Rational(int(m[2]),int(m[3])) if m else sp.Rational(v)
def read(q):
    text=q[':question/problem'];v=[sp.Matrix(a) for a in g.vectors(text)];a,u=v[:2];b=v[2] if len(v)==3 else sp.zeros(len(a),1)
    c=re.search(r'if \$(\d+)',text);c=int(c[1]) if c else 1
    sign=-1 if re.search(r'\{a\}_\{1\}-[a-z]',text) else 1
    r=(b-c*a)*sign
    ratios={sp.Rational(r[i],u[i]) for i in range(len(u)) if u[i]}
    consistent=all(u[i]!=0 or r[i]==0 for i in range(len(u))) and len(ratios)==1
    correct=next(iter(ratios)) if consistent else 'No solution'
    return a,u,b,c,sign,r,correct

def fingerprint(q):return g.fingerprint(q)
def structural(rec):
    q=rec['question'];a,u,b,c,sign,r,correct=read(q);f=q[':question/answer-fields'][0];vs=[x[':answer/value'] for x in f[':answer-field/choices']]
    parsed=[v if v=='No solution' else scalar(v) for v in vs];assert len(set(parsed))==5
    cid=f[':answer-field/correct'][1];assert sum(v==correct for v in parsed)==1
    assert all((x[':answer/id']==cid)==(v==correct) for x,v in zip(f[':answer-field/choices'],parsed))
    assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    for x in f[':answer-field/choices']:assert x[':answer/type']==(':answer.type/text' if x[':answer/value']=='No solution' else ':answer.type/math')
    assert len({x[':answer/id'] for x in f[':answer-field/choices']})==5
    sol=q[':question/worked-solution'];ms=[sp.Matrix(v) for v in g.vectors(sol)]
    # Literal solution sequence: substituted equation, isolated equation, simplified residual.
    expected=[a,u,b,u,a,b,u,r] if sign==-1 else [a,u,b,u,b,a,u,r]
    if correct=='No solution':
        t=sp.Rational(r[0],u[0]);assert t*u!=r
        expected += [u,t*u,r]
        letter=re.search(r'Find \$([a-z])',q[':question/problem'])[1]
        assert str(u[0])+letter+'='+str(r[0])+r'\,⟹\,'+letter+'='+g.tex(t)+'.' in sol
        assert 'Therefore, there is no $'+letter+'$ such that' in sol
    else:
        letter=re.search(r'Find \$([a-z])',q[':question/problem'])[1]
        assert '$'+letter+'='+g.tex(correct)+'.$' in sol
    assert ms==expected,(ms,expected)
    assert sol.count('$$')==(6 if correct=='No solution' else 2)
    assert q[':question/problem'].count('$$')==2 and '![]' not in q[':question/problem']
    assert fingerprint(q)==rec['generation']['parameter_fingerprint']
    assert q[':question/difficulty']==(':question.difficulty/moderate' if correct=='No solution' else ':question.difficulty/easy')
    return correct

def checks(rec):
    f=rec['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'every source-profile field-owned option'} for a in f[':answer-field/choices']]

def main():
    ledger=[];native=[];coverage={};fps={level:set() for level in g.LEVELS};review=[]
    for level,sids in g.LEVELS.items():
        for sid in sids:
            old=g.PROFILES[sid];rec=g.generate(level,0,sid,g.CASES[sid]);structural(rec)
            oldf=old[':question/answer-fields'][0];nf=rec['question'][':question/answer-fields'][0]
            oldbank=sorted((a[':answer/value'] if a[':answer/value']=='No solution' else str(scalar(a[':answer/value']))) for a in oldf[':answer-field/choices'])
            newbank=sorted((a[':answer/value'] if a[':answer/value']=='No solution' else str(scalar(a[':answer/value']))) for a in nf[':answer-field/choices'])
            assert oldbank==newbank
            oc=oldf[':answer-field/correct'][':answer/value'];assert structural(rec)==(oc if oc=='No solution' else scalar(oc))
            assert read(old)==read(rec['question'])
            assert g.vectors(old[':question/worked-solution'])==g.vectors(rec['question'][':question/worked-solution'])
            ledger.append({'profile':sid,'complete_bank_matched':True,'matched_values':5,'matched_distractors':4,'correct_designation_matched':True,'missing_or_extra':[],'prompt_math_identical':True,'solution_matrix_sequence_identical':True,'notation_changes':'Normalized whitespace, display delimiters, conventional scalar LaTeX. Same source sentences and ordered solution stages.'})
            pool=g.domain(sid);items=[]
            for p in pool:
                rec=g.generate(level,41,sid,p);structural(rec);assert rec==g.generate(level,41,sid,p)
                assert rec['question']==g.generate(level,99,sid,p)['question']
                fps[level].add(fingerprint(rec['question']));items.append(p)
                native.append({'label':sid+'/'+str(len(items)),'record':rec,'checks':checks(rec)})
            coverage[sid]={'valid_parameter_sets':len(items),'a_coordinates':[sorted({p['a'][i] for p in items}) for i in range(len(g.CASES[sid]['a']))],'u_coordinates':[sorted({p['u'][i] for p in items}) for i in range(len(g.CASES[sid]['u']))],'c':sorted({p['c'] for p in items}),'s':sorted({p['s'] for p in items},key=str),'letter_fixed_as_cosmetic':True,'dimension_fixed_to_source_profile':len(g.CASES[sid]['a'])}
            review.extend([g.generate(level,0,sid,g.CASES[sid]),g.generate(level,0,sid,next(p for p in pool if p!=g.CASES[sid]))])
    for level in ('hard','unclassified'):
        try:g.batch(level,1)
        except ValueError:pass
        else:raise AssertionError('Unsupported level accepted')
    for name,x in [('source-replay.json',ledger),('review-records.json',review),('engine-input.json',native)]: (D/name).write_text(json.dumps(x,indent=2)+'\n')
    # Side-by-side plain Markdown for direct inspection.
    md=[]
    for sid in g.PROFILES:
        md += ['## '+sid+' — source',g.PROFILES[sid][':question/problem'],g.PROFILES[sid][':question/worked-solution']]
        rr=next(r for r in review if r['generation']['bank_profile']==sid and r['generation']['parameters']!=g.CASES[sid])
        md += ['### Variant',rr['question'][':question/problem'],rr['question'][':question/worked-solution'],str([a[':answer/value'] for a in rr['question'][':question/answer-fields'][0][':answer-field/choices']])]
    (D/'review.md').write_text('\n\n'.join(md)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
    engine=json.loads((D/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    result={'status':'pass','source_banks':len(ledger),'matched_distractors':4*len(ledger),'complete_banks':len(ledger),'finite_variant_limit':{level:len(fs) for level,fs in fps.items()},'coverage':coverage,'all_bounded_parameter_sets_checked':True,'correctness':'Rendered vector equations independently solved; every solution matrix and component contradiction checked; all five answers checked','grading':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{'generator':sha(D.with_suffix('.py')),'validator':sha(D/'validate.py'),'source':sha(D/'reference/source.json'),'grader':sha(ROOT/'generate/runs/current/check-engine')}}
    (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='coverage'},indent=2))
if __name__=='__main__':main()

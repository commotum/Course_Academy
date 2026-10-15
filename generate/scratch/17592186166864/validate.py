"""Independently parse rendered P,Q, derivatives and solution equations."""
import hashlib,importlib.util,json,re,subprocess,sys
from functools import lru_cache
from pathlib import Path
import sympy as sp
sys.path.append('/tmp/ca-conservative-parser')
from sympy.parsing.latex import parse_latex
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,a=sp.symbols('x y a')
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
@lru_cache(None)
def parse(text):
    text=text.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos')
    text=text.replace('∂',r'\partial').strip().rstrip('.')
    text=re.sub(r'([xya])(?=\()',r'\1'+r'\\cdot ',text)
    return parse_latex(text,strict=True)
def exprs(problem):
    field=problem.split('$F=')[1].split(r'\,i+')[0]
    rest=problem.split(r'\,i+')[1].split(r'\,j$')[0]
    return parse(field),parse(rest)
def fingerprint(q):
    if '$F=' not in q[':question/problem']:return g.fingerprint(q)
    p,r=exprs(q[':question/problem'])
    return hashlib.sha256(json.dumps([sp.srepr(sp.expand(p)),sp.srepr(sp.expand(r))]).encode()).hexdigest()
def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio grader checks every choice'} for v in f[':answer-field/choices']]
def independent(rec):
    q=rec['question'];meta=rec['generation'];sid=meta['template'];n=meta['parameters']
    assert rec==g.generate('easy',meta['seed'],sid,n)
    assert rec['knowledge_point']['db_id']==g.KP_ID and q[':question/difficulty']==':question.difficulty/easy'
    p,r=exprs(q[':question/problem']);py=sp.diff(p,y);rx=sp.diff(r,x);curl=sp.simplify(py-rx)
    f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection'
    vals=[parse(v[':answer/value']) for v in f[':answer-field/choices']]
    assert len(vals)==5 and all(sp.simplify(u-v)!=0 for i,u in enumerate(vals) for v in vals[i+1:])
    matches=[v[':answer/id'] for v,value in zip(f[':answer-field/choices'],vals) if sp.simplify(curl.subs(a,value))==0]
    assert matches==[f[':answer-field/correct'][1]],(sid,n,curl,matches)
    correct=next(value for v,value in zip(f[':answer-field/choices'],vals) if v[':answer/id']==matches[0])
    assert sp.diff(curl,a)!=0 and sp.diff(curl,a,2)==0
    sol=q[':question/worked-solution']
    # Read the concrete P,Q and partial derivatives from the rendered solution.
    pair=re.search(r'P=(.*?),\\,Q=(.*?)\.',sol,re.S)
    if pair is None:pair=re.search(r'P=(.*?)\$ and \$Q=(.*?)\.\$',sol,re.S)
    assert pair,(sid,'P Q absent')
    assert sp.simplify(parse(pair[1])-p)==0 and sp.simplify(parse(pair[2])-r)==0,(sid,n,'stale solution P Q')
    derivatives=re.search(r'\\frac\{∂P\}\{∂y\}=(.*?),\\,\\frac\{∂Q\}\{∂x\}=(.*?)\.',sol.split('Computing the partial derivatives, we get')[1],re.S)
    assert derivatives,(sid,'derivatives absent')
    assert sp.simplify(parse(derivatives[1])-py)==0,(sid,n,'incorrect printed P_y',derivatives[1],py)
    assert sp.simplify(parse(derivatives[2])-rx)==0,(sid,n,'incorrect printed Q_x')
    equations=sol.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
    for row in equations.split(r'\\'):
        lhs,rhs=row.replace('&','').split('=')
        assert sp.simplify((parse(lhs)-parse(rhs)).subs(a,correct))==0,(sid,n,'false solution equation',row)
    last=equations.split(r'\\')[-1].replace('&','').strip().rstrip('.')
    assert last.startswith('a') and sp.simplify(parse(last.split('=')[1])-correct)==0
    # The identity holds everywhere; cancellation is not a pointwise division at x=0 or y=0.
    assert 'everywhere' in sol and '${R}^{2}' in q[':question/problem']
    return rec
check=independent

def main():
    inputs=[];replay=[];review=[];coverage={};distinct=set();total=0;recipes=[]
    for sid,source in g.CASES.items():
        rec=independent(g.generate('easy',0,sid,g.DEFAULTS[sid]));f=rec['question'][':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
        assert rec['question'][':question/problem']==source[':question/problem'] and rec['question'][':question/worked-solution']==source[':question/worked-solution']
        assert sorted(v[':answer/value'] for v in f[':answer-field/choices'])==sorted(v[':answer/value'] for v in sf[':answer-field/choices'])
        assert next(v[':answer/value'] for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
        replay.append({'source':sid,'complete_bank':True,'matched_distractors':4,'total_distractors':4,'prompt_exact':True,'solution_exact':True,'missing':[],'extra':[]})
        for v in sf[':answer-field/choices']:recipes.append({'source':sid,'source_field':sf[':answer-field/id'],'source_answer':v[':answer/id'],'original_value':v[':answer/value'],'profile':sid,'reproduces':True})
        fps=[]
        for n in g.DOMAINS[sid]:
            rec=independent(g.generate('easy',166864,sid,n));total+=1;fp=fingerprint(rec['question']);distinct.add(fp);fps.append(fp)
            inputs.append({'label':sid+' '+str(n),'record':rec,'checks':checks(rec)})
            assert g.generate('easy',777,sid,n)['question']==rec['question'],'seed changes content identity'
        assert len(fps)==len(set(fps))
        coverage[sid]={'slot_values':g.DOMAINS[sid],'missing':[],'distinct_mathematical_fields':len(set(fps))}
        changed=next(n for n in g.DOMAINS[sid] if n!=g.DEFAULTS[sid])
        review.append('## '+sid+'\n\nSource replay\n\n'+g.markdown(g.generate('easy',0,sid,g.DEFAULTS[sid]))+'\n\nChanged coefficient/frequency\n\n'+g.markdown(g.generate('easy',0,sid,changed)))
    for level in ('moderate','hard','unclassified'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported band admitted')
    save('source-replay.json',{'passed':True,'complete_banks_matched':8,'complete_banks_total':8,'distractors_matched':32,'distractors_total':32,'profiles':replay,'excluded_sources':list(g.EXCLUDED)})
    save('choice-replay.json',recipes);save('slot-coverage.json',coverage);save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'status':'pass','passed':True,'exhaustive_instances':total,'distinct_mathematical_fields':len(distinct),'source_fidelity':'8/8 complete banks, 32/32 distractors, exact source prompt and solution replay','correctness':'Rendered P,Q independently parsed; symbolic partials match printed derivatives; all solution equations hold at sole conservative parameter; full banks mathematically distinct with one correct value','grading':'Every complete bank exercised through application grade_field','supported_levels':['easy'],'parser':'SymPy parse_latex, antlr4-python3-runtime 4.11.1','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine']}})
if __name__=='__main__':main()

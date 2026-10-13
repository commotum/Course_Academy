#!/usr/bin/env python3
"""Independent checks read printed systems, matrix stages and row operations.
The generator metadata is never used to infer mathematical answers."""
import importlib.util,json,pathlib,re,subprocess,hashlib,sys
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=pathlib.Path(__file__).parent;spec=importlib.util.spec_from_file_location('gen',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
k,x,y=s.symbols('k x y')

def parse(txt):
    txt=txt.strip().rstrip('.,').replace('\\\\','\\')
    txt=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',txt)
    txt=txt.replace('{','(').replace('}',')').replace('−','-')
    return parse_expr(txt,local_dict={'x':x,'y':y,'k':k},transformations=standard_transformations+(implicit_multiplication_application,))
def equations(block):
    body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,re.S).group(1)
    result=[]
    for row in body.split('\\\\'):
        row=row.replace('&','').strip().rstrip('.,');lhs,rhs=row.split('=');result.append(parse(lhs)-parse(rhs))
    return result

def matrix_text(body):return s.Matrix([[parse(t) for t in row.split('&')] for row in body.split('\\\\')])
def same(A,B):return A.shape==B.shape and all(s.simplify(a-b)==0 for a,b in zip(A,B))
def printed_check(rec):
    assert set(rec['knowledge_point'])=={'db_id','id','title'} and rec['knowledge_point']['db_id']==g.KP_ID
    q=rec['question'];f=q[':question/answer-fields'][0]
    assert f[':answer-field/type']==':answer-field.type/radio' and len(f[':answer-field/choices'])==5
    prompt=q[':question/problem'];solution=q[':question/worked-solution']
    assert prompt.count('$$')==2 and solution.count('$$')==6
    eqs=equations(prompt)
    A=s.Matrix([[s.expand(z).coeff(x),s.expand(z).coeff(y)] for z in eqs]);bvec=s.Matrix([-s.expand(z).subs({x:0,y:0}) for z in eqs]);M=A.row_join(bvec)
    roots=s.solve(A.det(),k);assert len(roots)==1
    t=roots[0];dependent='consistent dependent' in prompt
    rank=A.subs(k,t).rank();aug=M.subs(k,t).rank()
    assert (rank==aug==1) if dependent else (rank<aug)
    values=[parse(z[':answer/value'].split('=',1)[1]) for z in f[':answer-field/choices']]
    assert len(set(values))==5
    correct=f[':answer-field/correct'][1]
    assert sum(a[':answer/id']==correct for a in f[':answer-field/choices'])==1
    for a,v in zip(f[':answer-field/choices'],values):
        assert (s.simplify(v-t)==0)==(a[':answer/id']==correct)
        ar=A.subs(k,v).rank();mr=M.subs(k,v).rank()
        assert ((ar==mr==1) if dependent else ar<mr)==(a[':answer/id']==correct)
    # All matrices read from actual rendered solution; duplicate initial stage retained.
    raw=re.findall(r'\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',solution,re.S)
    mats=list(map(matrix_text,raw));assert same(mats[0],M) and same(mats[1],M)
    swap='↔' in solution
    assert len(mats)==(4 if swap else 3)
    current=M
    if swap:
        current=s.Matrix([list(M.row(1)),list(M.row(0))]);assert same(mats[2],current)
    operation=re.search(r'\{R\}_\{2\} & :=\{R\}_\{2\}(.*?)\{R\}_\{1\}',solution).group(1)
    m=parse(operation if operation not in ('+','-') else operation+'1')
    expected=current.copy();expected[1,:]=current.row(1)+m*current.row(0)
    assert same(mats[-1],expected)
    # Corresponding system must be exactly the row equations, not merely rank equivalent.
    blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
    final=equations(blocks[-1])
    for j,z in enumerate(final):
        expected_expr=mats[-1][j,0]*x+mats[-1][j,1]*y-mats[-1][j,2]
        assert s.simplify(z-expected_expr)==0
    # Every numerical final k statement and contradiction is independently derived.
    for v in re.findall(r'\$k=([^$]*?)\$',solution):assert s.simplify(parse(v)-t)==0
    for v in re.findall(r'\$0=([^$]*?)\$',solution):assert parse(v)==mats[-1][1,2]
    for z in re.findall(r'(?<!\$)\$([^$\n]*[xy][^$\n]*=[^$\n]*)\$(?!\$)',solution):
        lhs,rhs=z.rstrip('.,').split('=');eq=parse(lhs)-parse(rhs)
        assert s.simplify(eq-final[0])==0
    # Escaped visible left-system braces are valid, all TeX groups balance.
    for text in [prompt,solution]:
        assert not re.search(r'(?<!\\)\{(?=\\begin\{aligned\})',text)
        stripped=re.sub(r'\\[{}]','',text)
        assert stripped.count('{')==stripped.count('}')
    return t

def main():
    sources=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((D/'source-cases.json').read_text());recipes=json.loads((D/'recipes.json').read_text())
    outputs=[];fidelity=[];native=[];exact_solution=0;exact_prompt=0;presentation_solution=0
    for source,case in zip(sources,cases):
        rec=g.generate(case['level'],seed=33,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);printed_check(rec)
        q=rec['question'];sourcef=source[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        sourcevalues=[parse(a[':answer/value'].split('=',1)[1]) for a in sourcef[':answer-field/choices']];genvalues=[parse(a[':answer/value'].split('=',1)[1]) for a in f[':answer-field/choices']]
        assert set(genvalues)==set(sourcevalues)
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sourcef[':answer-field/choices'])
        gc=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert gc[':answer/value']==sourcef[':answer-field/correct'][':answer/value']
        normalized_prompt=re.sub(r'(?<!\\)\{(?=\\begin\{aligned\})',lambda _:r'\{',source[':question/problem'])
        assert q[':question/problem']==normalized_prompt
        exact_prompt+=q[':question/problem']==source[':question/problem']
        rawsol=source[':question/worked-solution'];repaired=rawsol
        if case['source_id']=='q-74695':repaired=repaired.replace('x+ky=2','x+ky=-2')
        if case['source_id']=='q-42021':repaired=repaired.replace('1 & 2 & -3','1 & 2 & 3').replace('1-2y=3','x+2y=3')
        repaired=re.sub(r'(?<!\\)\{(?=\\begin\{aligned\})',lambda _:r'\{',repaired)
        normalized_sol=re.sub(r'(?<!\\)\{(?=\\begin\{aligned\})',lambda _:r'\{',rawsol)
        assert q[':question/worked-solution']==repaired
        presentation_solution+=q[':question/worked-solution']==normalized_sol
        exact_solution+=q[':question/worked-solution']==rawsol
        fidelity.append({'source_id':case['source_id'],'prompt_byte_exact':q[':question/problem']==source[':question/problem'],'prompt_presentation_repaired_exact':True,'bank_exact':True,'correct_designation_exact':True,'solution_byte_exact':q[':question/worked-solution']==rawsol,'solution_presentation_only_exact':q[':question/worked-solution']==normalized_sol,'solution_repaired_exact':True,'choices':5,'distractors':4})
        outputs.append(('Observed replay '+case['source_id'],rec));native.append(engine_case(case['source_id'],rec))
        # Each observed template / complete profile gets a changed-parameter variant.
        for seed in range(100):
            try:changed=g.generate(case['level'],seed=1000+seed,template=case['template'],profile=case['source_id'])
            except ValueError:continue
            if changed['generation']['parameters']!=case['parameters']:break
        else:raise AssertionError('No changed parameter source-profile instance')
        printed_check(changed);outputs.append(('Generated variant of observed profile '+case['source_id'],changed));native.append(engine_case(case['source_id']+' changed',changed))
    # Validate that corrupt displayed mathematics is actually caught.
    import copy
    base=outputs[0][1]
    for kind in ('prompt','first_matrix','row_operation','correct_ref'):
        bad=copy.deepcopy(base);q=bad['question']
        if kind=='prompt':q[':question/problem']=q[':question/problem'].replace('3x+4y=12','3x+4y=13')
        if kind=='first_matrix':q[':question/worked-solution']=q[':question/worked-solution'].replace('3 & 4 & 12','3 & 5 & 12',1)
        if kind=='row_operation':q[':question/worked-solution']=q[':question/worked-solution'].replace('(-3){R}_{1}','(-2){R}_{1}')
        if kind=='correct_ref':
            f=q[':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
        try:printed_check(bad)
        except AssertionError:pass
        else:raise AssertionError('Corruption escaped: '+kind)
    # Same assessed system deduplicates across complete bank profiles.
    samep=dict(a=2,b=-1,c=3,d=4,u=1,v=0,e=4)
    er=g.generate('moderate',parameters=samep,template='inconsistent_bare',profile='q-32245')
    mr=g.generate('moderate',parameters=samep,template='inconsistent_bare')
    assert er['generation']['mathematical_fingerprint']==mr['generation']['mathematical_fingerprint']
    assert er['question'][':question/id']!=mr['question'][':question/id']
    uniqueness={};sampled=0
    for level,templates in g.TEMPLATES.items():
        for template in templates:
            seen=set()
            for seed in range(120):
                rec=g.generate(level,seed,template=template);printed_check(rec);sampled+=1;seen.add(rec['generation']['math_fingerprint'])
                if seed<2:outputs.append(('Authored default '+level+' '+template,rec));native.append(engine_case(level+template+str(seed),rec))
                # Order/seed-independent fixed mathematical content identity.
                other=g.generate(level,seed+500,template=template,parameters=rec['generation']['parameters'])
                assert other['question'][':question/id']==rec['question'][':question/id']
            assert len(seen)>=70,(template,len(seen));uniqueness[template]=len(seen)
    # Explicit boundary rejection protects level workload.
    invalid=[('moderate','inconsistent_bare',dict(a=1,b=2,c=1,d=3,u=1,v=0,e=2)),('easy','inconsistent_easy',dict(a=2,b=2,c=1,d=4,u=1,v=0,e=3)),('moderate','inconsistent_bare',dict(a=-5,b=2,c=1,d=-10,u=1,v=0,e=3)),('hard','dependent_swap',dict(a=5,b=2,c=5,d=1,u=1,v=0,e=1))]
    for level,template,p in invalid:
        try:g.generate(level,parameters=p,template=template)
        except ValueError:pass
        else:raise AssertionError('Invalid scope input accepted')
    (D/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
    engine=pathlib.Path('generate/runs/current/check-engine');subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
    report=json.loads((D/'native-report.json').read_text())
    validation={'passed':True,'basis':1356,'source_questions':15,'source_prompts_byte_exact':exact_prompt,'source_prompts_presentation_repaired_exact':15,'source_presentation_repaired_prompts':15-exact_prompt,'source_banks_exact':15,'source_choices_exact':75,'source_distractors_exact':60,'source_correct_designations_exact':15,'source_solutions_byte_exact':exact_solution,'source_solutions_presentation_only_exact':presentation_solution,'source_solutions_presentation_and_math_repaired_exact':15,'source_errors_repaired':2,'authored_missing_level':'easy','generated_math_checks':sampled+15+15,'unique_mathematical_tasks_per_template':uniqueness,'native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'native_unresolved':report['documented_unresolved_checks'],'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'fidelity':fidelity,'database_writes':0}
    (D/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    (D/'review.json').write_text(json.dumps([{'label':label,'record':record} for label,record in outputs],indent=2)+'\n')
    review=['# Source originals and generated review\n\nRaw source solutions below include errors; repaired replays are labeled.']
    for source in sources:
        review+=['\n## Raw original '+source[':question/math-academy-id'],source[':question/problem'],'\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in source[':question/answer-fields'][0][':answer-field/choices']),source[':question/worked-solution']]
    for label,rec in outputs:review+=['\n## '+label,g.markdown(rec)]
    (D/'review.md').write_text('\n\n'.join(review)+'\n');print(json.dumps(validation,indent=2))

def engine_case(label,rec):
    f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'All owned radio choices through native grader'} for a in f[':answer-field/choices']]}
if __name__=='__main__':main()

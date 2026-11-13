#!/usr/bin/env python3
"""Independent completion QA: formulas are transcribed from target problems.

Does not import any completion author build or use its recorded 'passed' flags.
"""
from pathlib import Path
import hashlib
import json
import re
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
from bs4 import BeautifulSoup

BASE=Path(__file__).resolve().parent.parent
x,y,z,w,t,m,b,a,c,w1,w2,x1,x2=S.symbols('x y z w t m b a c w1 w2 x1 x2',real=True)
loc={str(v):v for v in [x,y,z,w,t,m,b,a,c,w1,w2,x1,x2]}
loc.update(sin=S.sin,cos=S.cos,exp=S.exp,log=S.log)
def tex(v):
    v=v.strip().strip('$').replace('⁡','').replace(r'\displaystyle','').replace(r'\left','').replace(r'\right','')
    v=re.sub(r'\\operatorname\{(sin|cos|ln)\}',lambda m:'log' if m[1]=='ln' else m[1],v)
    v=re.sub(r'\\(sin|cos|ln)',lambda m:'log' if m[1]=='ln' else m[1],v)
    v=re.sub(r'e\^\{([^{}]+)\}',r'exp(\1)',v)
    while re.search(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',v):
        v=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',v)
    v=v.replace(r'\,','').replace(r'\:','').replace('^','**').replace('{','(').replace('}',')')
    assert '\\' not in v,repr(v)
    return parse_expr(v,local_dict=loc,transformations=standard_transformations+(implicit_multiplication_application,rationalize))
def equal(u,v):return S.simplify(u-v)==0
def equalmat(u,v):return u.shape==v.shape and all(equal(a,b) for a,b in zip(u,v))
def matparse(body):return S.Matrix([[tex(c) for c in row.split('&')] for row in body.split(r'\\')])

qs={q[':db/id']:q for q in json.loads((BASE/'capture/questions.json').read_text())}
layouts={q['entity']:q['after'] for q in json.loads((BASE/'proposals.json').read_text()) if q['attribute']=='question/problem'}
for record in json.loads((BASE/'final-validation/completion-records.json').read_text()):
    q=record['question'];match=next((qid for qid,old in qs.items() if old.get(':question/id')==q.get(':question/id')),None)
    if match:layouts[match]=q[':question/problem']

# Models below are independently recomputed from the actual target wording.
models={17592186129589:[S.Matrix([[1,5],[0,-2]]),S.Matrix([2*S.log(t),-t*t])],
17592186157699:[S.diag(*[S.Integer(2)**(S.Rational(d,3)) for d in [3,-12,9,21]])],
17592186204561:[S.Matrix([S.diff(w1*x1+w2*x2,k) for k in [w1,w2]]).subs({x1:2,x2:-1})],
17592186204560:[S.Matrix([S.diff(m*x+b,k) for k in [m,b]])],
17592186204562:[S.hessian(x*x*y+y*z*z,(x,y))],
17592186204565:[S.Matrix([S.diff(x*y*y+y*z*z+z*w*w,k) for k in [x,y]])],
17592186204566:[S.Matrix([S.diff(a*x+b*y+c,k) for k in [a,c]])]}
flows={17592186167247:(S.Matrix([x-x*y/2,-y/5+2*x*y]),{x:S.Rational(1,10),y:2}),
17592186167252:(S.Matrix([2*x*(1-x)-x*y,-2*y+4*x*y]),{x:1,y:0}),
17592186167253:(S.Matrix([2*x*(1-4*x)-x*y,-2*y+4*x*y]),{x:S.Rational(1,4),y:0}),
17592186221965:(S.Matrix([x*x-y,3*x+y*y]),{x:0,y:0}),
17592186221966:(S.Matrix([x*x-x+2*y-4,-3*x+y*y-4*y+7]),{x:1,y:2})}
checks={}
for qid,(flow,point) in flows.items():
    assert flow.subs(point)==S.zeros(2,1)
    J=flow.jacobian([x,y]);M=J.subs(point);models[qid]=[M]
    checks[qid]={'flow':str(flow),'equilibrium':str(point),'Jacobian':str(J),'evaluated_Jacobian':str(M),
                 'characteristic_polynomial':str(M.charpoly().as_expr()),'eigenvalues':{str(k):v for k,v in M.eigenvals().items()}}
# Independent spectral/nilpotent formulas, followed by ODE checks; no copied
# exponential answer matrices are used to construct these models.
exp_params={17592186221932:(S.Matrix([[3,-4],[2,-1]]),'complex',1,2,S.exp(t)),
17592186221933:(S.Matrix([[1,2],[-2,5]]),'repeated',3,None,S.exp(3*t)),
17592186221994:(S.Matrix([[0,6],[1,-1]]),'real',-3,2,S.Rational(1,5)),
17592186222002:(S.Matrix([[1,1],[-2,-1]]),'complex',0,1,S.Integer(1)),
17592186222003:(S.Matrix([[3,1],[-1,1]]),'repeated',2,None,S.exp(2*t))}
for qid,(A,kind,p,q,factor) in exp_params.items():
    if kind=='complex':E=S.exp(p*t)*(S.eye(2)*S.cos(q*t)+(A-p*S.eye(2))*S.sin(q*t)/q)
    elif kind=='repeated':
        N=A-p*S.eye(2);assert N*N==S.zeros(2);E=S.exp(p*t)*(S.eye(2)+t*N)
    else:E=((A-p*S.eye(2))*S.exp(q*t)-(A-q*S.eye(2))*S.exp(p*t))/(q-p)
    assert E.subs(t,0)==S.eye(2)
    assert equalmat(E.diff(t),A*E)
    models[qid]=[(E/factor).applyfunc(S.expand)]
    checks[qid]={'A':str(A),'full_exponential':str(E),'supplied_outer_factor':str(factor),
                 'required_inner_grid':str(models[qid][0]),'E0_identity':True,'Eprime_equals_AE':True}

parts=[('review-1','completion','answer-creations'),('review-1','supplemental-completion','supplemental-answer-creations'),
       ('review-2','completion','answer-creations'),('review-3','completion','answer-creations')]
creations={};correct_refs={};solutions={};artifact_hashes={};newcount=0
for directory,name,answers in parts:
    for filename in [name+'-evidence',name+'-proposals',answers]:
        path=BASE/directory/(filename+'.json');data=json.loads(path.read_text())
        artifact_hashes[str(path.relative_to(BASE))]=hashlib.sha256(path.read_bytes()).hexdigest()
        def controls(v):
            if isinstance(v,str):assert not any(ord(c)<32 and c not in '\n\r\t' for c in v)
            elif isinstance(v,dict):
                for k,u in v.items():controls(k);controls(u)
            elif isinstance(v,list):
                for u in v:controls(u)
        controls(data)
    for record in json.loads((BASE/directory/(answers+'.json')).read_text()):
        field=record['field_entity'];assert field not in creations
        creations[field]=record.get('value',record.get('answer_value'));newcount+=1
    for record in json.loads((BASE/directory/(name+'-proposals.json')).read_text()):
        if record['attribute']=='answer-field/correct':correct_refs[record['entity']]=record['after']
        elif record['attribute']=='question/worked-solution':solutions[record['entity']]=record['after']

results=[];fieldcount=0;existingcount=0
for qid,matrices in models.items():
    q=qs[qid];soup=BeautifulSoup(layouts[qid],'html.parser');tables=soup.select('.matrix-answer-brackets table')
    assert len(tables)==len(matrices),(qid,'operand count')
    mappings=[]
    for index,(table,M) in enumerate(zip(tables,matrices)):
        table_rows=table.find_all('tr');assert len(table_rows)==M.rows
        for i,tr in enumerate(table_rows):
            cells=tr.find_all('td');assert len(cells)==M.cols
            for j,cell in enumerate(cells):
                text=cell.get_text().strip();marker=re.fullmatch(r'\{\{([^{}]+)\}\}',text)
                if not marker:
                    assert equal(tex(text),M[i,j]),(qid,i,j,'supplied entry',text,M[i,j]);continue
                key=marker[1];fields=[f for f in q[':question/answer-fields'] if f[':answer-field/key']==key]
                #22003's authored duplicate cleanup retains only populated fields.
                if qid==17592186222003:fields=[f for f in fields if f.get(':answer-field/correct')]
                assert len(fields)==1,(qid,key,'field identity')
                field=fields[0];fid=field[':db/id'];fieldcount+=1
                if fid in creations:value=creations[fid];source='authored field-owned answer'
                else:
                    ref=correct_refs.get(fid,field.get(':answer-field/correct',{}).get(':db/id'))
                    matching=[choice for choice in field.get(':answer-field/choices',[]) if choice[':db/id']==ref]
                    assert len(matching)==1;value=matching[0][':answer/value'];source='existing owned answer';existingcount+=1
                    assert sum(equal(tex(choice[':answer/value']),M[i,j]) for choice in field[':answer-field/choices'])==1
                assert equal(tex(value),M[i,j]),(qid,fid,value,M[i,j])
                mappings.append({'field_entity':fid,'key':key,'operand_index_1_based':index+1,'row':i+1,'column':j+1,
                                 'answer':value,'independently_computed':str(M[i,j]),'source':source,'passed':True})
    solution=solutions.get(qid,q.get(':question/worked-solution'))
    assert solution
    solution_matrices=[matparse(v) for v in re.findall(r'\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}',solution)
                       if not re.search(r'\\partial|\\alpha|⋯|⋮|⋱|x_\{|w_\{|x\}_\{|x\}_',v)]
    for M in matrices:assert any(equalmat(M,seen) for seen in solution_matrices),(qid,'expected final matrix missing from solution')
    results.append({'question_entity':qid,'original_target_problem':q[':question/problem'],'expected_grids':[str(M) for M in matrices],
                    'independent_checks':checks.get(qid,{'differentiation_or_diagonal_evaluation':'recomputed directly from target function and requested variables'}),
                    'field_mappings':mappings,'all_supplied_entries_verified':True,'solution_contains_correct_matrix':True,'status':'pass'})

# Establish the nonlinear classical Lotka center without treating imaginary
# linear eigenvalues as sufficient for a general nonlinear system.
H=2*x+y/2-S.log(x)/5-S.log(y);F=flows[17592186167247][0]
assert S.simplify(S.diff(H,x)*F[0]+S.diff(H,y)*F[1])==0
Hess=S.hessian(H,(x,y)).subs(flows[17592186167247][1]);assert Hess==S.diag(20,S.Rational(1,4))
evidence2=json.loads((BASE/'review-2/completion-evidence.json').read_text())
wording_issue=any('KP_title_mismatch' in q for q in evidence2['questions'])
report={'basis':14371,'status':'mathematical and coordinate checks passed',
        'review_method':'Independent target transcriptions, symbolic differentiation and spectral/nilpotent recomputation; verified every proposed or retained keyed answer against its exact rendered operand/cell. No author build or passed flags were trusted.',
        'counts':{'questions':len(results),'authored_solutions':len(solutions),'authored_answers':newcount,'field_mappings':fieldcount,'existing_owned_answers':existingcount},
        'D_divisor_source_typo':{'question':17592186157699,'screenshot_independently_viewed':True,
          'screenshot':'/home/jake/Developer/MA/DATA/Lessons/2927/Source/Sections/05-question-253242.png',
          'observation':'Original screenshot explicitly requests2^(D/3) while response label says2^(D/2). The direct task wording determines the answer; diagonal entries divisible by3 provide supporting context only.',
          'result_diagonal':['2','1/16','8','128'],'final_validation_label_corrected':r'2^{D/3}' in layouts[17592186157699]},
        'Lotka_classifications':{'17592186167247':'stable nonlinear center, not asymptotically stable; first integral derivative0 and Hessian diag(20,1/4)>0 independently checked',
          '17592186167252':'unstable saddle; eigenvalues-2,+2. Stable Case KP can refer to a parameter regime; no placement defect is inferred.',
          '17592186167253':'asymptotically stable sink; eigenvalues-2,-1'},
        'issues':([{'severity':'evidence wording only','path':'review-2/completion-evidence.json','key':'KP_title_mismatch',
                   'reason':'Do not infer incorrect KP placement from the saddle at a specified boundary equilibrium; Stable Case can describe the model regime. Math and selected answers are correct.',
                   'recommended_action':'Remove or replace with a neutral target-specific classification note.'}] if wording_issue else []),
        'limits':'Root owns actual renderer/native specs/grader/transaction verification; this report does not claim a database commit or application grading result.',
        'artifact_sha256':artifact_hashes,'questions':results}
(BASE/'completion-cross-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['counts']))

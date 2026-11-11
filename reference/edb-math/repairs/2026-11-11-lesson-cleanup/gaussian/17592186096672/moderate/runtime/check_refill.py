"""Offline checks derived from displayed mathematics, never generation metadata."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import re
from fingerprint import content_fingerprint

CHECKS = ['visible-mathematics','independent-task','bank-integrity','ordinary-bank-support']

def array(text):
    match = re.search(r'\\begin\{array\}\{ccc\|c\}(.*?)\\end\{array\}',text,re.S)
    if not match:
        raise ValueError('No complete 3x4 augmented array')
    rows = [[F(x.strip()) for x in row.split('&')] for row in match[1].split(r'\\')]
    assert len(rows)==3 and all(len(row)==4 for row in rows)
    return rows

def givens(problem):
    if r'\begin{array}' in problem:
        return array(problem)
    body = re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',problem,re.S)[1]
    rows=[]
    for eq in body.split(r'\\'):
        left,right = eq.replace('&','').replace(' ','').split('=')
        right = right.rstrip('.,')
        terms = re.findall(r'([+-]?)(\d*)([xyz])',left)
        assert ''.join(sign+number+variable for sign,number,variable in terms)==left
        coefs={v:F(0) for v in 'xyz'}
        for sign,number,variable in terms:
            coefs[variable]+=(-1 if sign=='-' else 1)*F(number or '1')
        rows.append([coefs[v] for v in 'xyz']+[F(right)])
    assert len(rows)==3
    return rows

def reduced(rows):
    M=[list(row) for row in rows]
    for j in range(3):
        i=next(i for i in range(j,3) if M[i][j])
        M[i],M[j]=M[j],M[i]
        p=M[j][j];M[j]=[v/p for v in M[j]]
        for i in range(3):
            if i!=j:
                p=M[i][j];M[i]=[x-p*y for x,y in zip(M[i],M[j])]
    return M

def vector(text):
    if re.search(r'[xyz]\s*=',text):
        vals=[re.search(v+r'\s*=\s*(-?\d+)',text)[1] for v in 'xyz']
    else:
        body=text.replace(r'\langle','⟨').replace(r'\rangle','⟩')
        match=re.search(r'⟨(.*?)⟩',body)
        if not match:
            raise ValueError('No complete triple')
        vals=match[1].split(',')
    assert len(vals)==3
    return [F(v.strip()) for v in vals]

def is_ref(rows):
    return all(rows[i][i] for i in range(3)) and all(rows[i][j]==0 for i,j in ((1,0),(2,0),(2,1)))


def apply_shown_operation(current, operation):
    """Interpret the displayed elementary operation, including its target row."""
    target, rhs = operation.split(':=')
    match = re.fullmatch(r'R_([123])', target)
    assert match, 'Unsupported operation target'
    target = int(match[1])-1
    tokens = list(re.finditer(r'([+-]?)(\\frac\{\d+\}\{\d+\}|\d+)?R_([123])', rhs))
    assert tokens and ''.join(m[0] for m in tokens)==rhs, 'Incomplete operation expression'
    terms=[]
    for m in tokens:
        number=m[2] or '1'
        fraction=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',number)
        value=F(int(fraction[1]),int(fraction[2])) if fraction else F(number)
        value *= -1 if m[1]=='-' else 1
        terms.append((value,int(m[3])-1))
    if len(terms)==1:
        assert terms[0][1]==target and terms[0][0], 'Scaling must use the target row and a nonzero factor'
    else:
        assert len(terms)==2 and terms[0]==(F(1),target) and terms[1][1]!=target and terms[1][0], 'Invalid elementary row replacement'
    result=[list(row) for row in current]
    result[target]=[sum(coefficient*current[row][column] for coefficient,row in terms) for column in range(4)]
    return result

def verify_shown_transitions(initial, solution, states):
    assert states[0]==initial, 'Worked initial matrix differs from displayed givens'
    transitions=re.findall(r'Using \$(.*?)\$, we obtain\s*\$\$\s*(.*?)\$\$',solution,re.S)
    assert len(transitions)==len(states)-1, 'Every shown matrix needs its operation'
    current=initial
    for operation, display in transitions:
        current=apply_shown_operation(current,operation)
        assert current==array(display), 'Annotated operation does not produce the displayed matrix'
    assert current==states[-1]


def inspect(record):
    q=record['question'];problem=q[':question/problem'];solution=q[':question/worked-solution']
    A=givens(problem);R=reduced(A);answer=[R[i][3] for i in range(3)]
    assert all(A[i][j] for i,j in [(0,0)])
    # No row exchange needed: the first two leading principal minors are nonzero.
    assert A[0][0]*A[1][1]-A[0][1]*A[1][0]
    solve='solve the linear system' in problem
    assert 'Gaussian elimination' in problem and 'row echelon form' in problem
    assert not re.search(r'R_?\{?\d|:=|Back substitution|Using \$',problem)
    fields=q[':question/answer-fields'];assert len(fields)==1
    field=fields[0];assert str(field[':answer-field/type'].get(':db/ident') if isinstance(field[':answer-field/type'],dict) else field[':answer-field/type'])==':answer-field.type/radio'
    choices=field[':answer-field/choices'];assert len(choices)==5
    key=field[':answer-field/correct'];key=key[':answer/id'] if isinstance(key,dict) else key[1] if isinstance(key,list) else key
    valid=[];visible=[]
    for c in choices:
        value=c[':answer/value']
        if solve:
            v=vector(value);truth=all(sum(row[j]*v[j] for j in range(3))==row[3] for row in A)
            visible.append(tuple(v))
        else:
            candidate=array(value);truth=bool(is_ref(candidate) and reduced(candidate)==R)
            visible.append(tuple(tuple(row) for row in candidate))
        if truth:valid.append(c[':answer/id'])
    assert valid==[key],(valid,key)
    assert len(set(visible))==5
    # Check every displayed intermediate array as an independent row-equivalence witness.
    states=[array(x) for x in re.findall(r'\\begin\{array\}\{ccc\|c\}.*?\\end\{array\}',solution,re.S)]
    assert states and all(reduced(state)==R for state in states)
    verify_shown_transitions(A,solution,states)
    assert is_ref(states[-1])
    if solve:
        final=vector(solution[solution.rfind('Therefore'):])
        assert final==answer
    else:
        assert states[-1]==array(next(c[':answer/value'] for c in choices if c[':answer/id']==key))
    return {'solution':list(map(str,answer)),'states':len(states),'valid_choices':len(valid),'endpoint':'solve' if solve else 'ref'}

def main():
    parser=argparse.ArgumentParser()
    for name in ('records','inventory','output'):parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args()
    records=json.loads(args.records.read_text()); json.loads(args.inventory.read_text())
    details=[inspect(record) for record in records]
    # This construction regression spans fixed independent seeds, not a quota on survivors.
    from generator import generate
    from support_regression import check
    support = check(generate,givens,vector)
    fps=sorted(set(content_fingerprint(r['question']) for r in records))
    assert len(fps)==len(records)
    report={'status':'passed','checked_fingerprints':fps,
            'check_results':[{'id':name,'status':'passed','checked_fingerprints':fps} for name in CHECKS],
            'records':details,'ordinary_support_regression':support,'limitations':['Radio controls assess recognition; no method trace is collected. No population coverage quota is applied.']}
    args.output.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()

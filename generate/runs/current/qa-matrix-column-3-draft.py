"""Read complete learner operands, ordered dot-product factors and whole banks."""
import sys
sys.dont_write_bytecode = True
import copy, hashlib, importlib.util, json, re
from pathlib import Path
import sympy as s

R = Path(__file__).resolve().parent
K = 17592186100867
D = R.parents[2] / f"generate/scratch/{K}-draft"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

G = load("root_column3_generator", D.with_suffix(".py"))
F = load("root_column3_math_format", R.parents[2] / "scripts/question_capture/math_format.py")

def number(text):
    text = text.replace(r"\,", "").strip()
    if text[:1] in ("+", "-") and text[1:].lstrip().startswith("("):
        return (1 if text[0]=="+" else -1)*number(text[1:])
    while text.startswith("(") and text.endswith(")"):
        text = text[1:-1].strip()
    assert re.fullmatch(r"[+-]?\s*\d+(?:\.\d+)?", text), text
    return s.Rational(text.replace(" ", ""))

def arrays(text):
    result=[]
    for match in re.finditer(r"\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}",text,re.S):
        body=match[1]
        if r'\begin{aligned}' in body:
            body=body.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
        result.append([[cell.strip() for cell in row.split('&')] for row in body.split(chr(92)*2)])
    return result

def signed_terms(text):
    text=text.strip();depth=0;start=0;result=[]
    for i,ch in enumerate(text):
        if ch in '({[':depth+=1
        elif ch in ')}]':depth-=1
        elif ch in '+-' and depth==0 and text[start:i].strip():result.append(text[start:i]);start=i
    assert depth==0;result.append(text[start:]);return result

def numerical(matrix):
    return s.Matrix([[number(cell) for cell in row] for row in matrix])

def signature(text):
    matrices = arrays(text)
    if matrices:
        assert len(matrices) == 1
        matrix = numerical(matrices[0])
        assert matrix.shape == (3, 1)
        return tuple(matrix)
    return (number(text),)

C = dict(records=0, prompt_cells=0, printed_operand_cells=0, ordered_dot_factors=0,
         retained_or_evaluated_cells=0, complete_answer_values=0, whole_method_banks=0,
         source_prompts=0, source_solutions=0, source_fields=0, source_values=0,
         source_keys=0, source_missing_keys=0)

def check(record):
    q=record['question'];shown=arrays(q[':question/problem']);assert len(shown)==2
    A,V=map(numerical,shown);assert A.shape==(3,3) and V.shape==(3,1);target=A*V;r,t,u=list(target)
    C['prompt_cells']+=12
    for field in q[':question/answer-fields']:
        values=[signature(answer[':answer/value']) for answer in field[':answer-field/choices']];assert len(values)==len(set(values))
        expected_value=tuple(target) if field[':answer-field/type'].endswith('/radio') else (target[int(field[':answer-field/key'][-1])-1],)
        assert sum(value==expected_value for value in values)==1
        if ':answer-field/correct' in field:
            correct=next(answer for answer in field[':answer-field/choices'] if answer[':answer/id']==field[':answer-field/correct'][1]);wanted=tuple(target) if field[':answer-field/type'].endswith('/radio') else (target[int(field[':answer-field/key'][-1])-1],);assert signature(correct[':answer/value'])==wanted
        if field[':answer-field/type'].endswith('/blank'):assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
        if len(values)==5 and not record['generation']['evidence_only']:
            profile=record['generation']['bank_profile']
            banks={
             'q-127267':[(r,t,u),(r,t,-u),(r,-t,-u),(r,-t,u),(r,r,-u)],
             'q-70188':[(r,t,u),(r,-t,-u),(r,t,-u),(-r,-t,u),(r,-t,u)],
             'q-70191':[(r,t,u),(r,-t,u),(r,-t,-u),(-r,t,u),(r,t,-u)],
             'q-70190':[(r,t,u),(r,t,-u),(r,-t,u),(-r,t,u),(-r,-t,u)],
             'q-77350':[(r,t,u),(-r,-t,u),(r,u,t),(r,-t,u),(u,t,r)],
             'q-13558':[(r,t,u),(-r,-t,u),(-r,t,u),(r,-t,-u),(r,t,-u)]}
            if profile in banks:expected=banks[profile]
            else:
                assert profile=='authored-method';active=[j for j in range(3) if V[j]!=0];expected=[tuple(target)]+[tuple(target-A[:,j]*V[j]) for j in active]+[tuple(A.T*V)]+([tuple(-target)] if len(active)==2 else [])
            assert len(set(expected))==5 and set(values)==set(expected);C['whole_method_banks']+=1
        C['complete_answer_values']+=len(values)
    if ':question/worked-solution' not in q:return
    solution=q[':question/worked-solution'];ms=arrays(solution);assert len(ms)==5
    assert numerical(ms[0])==A and numerical(ms[1])==V;C['printed_operand_cells']+=12
    if all(len(row)==5 for row in ms[3]):
        assert all(row[1]==row[3]=='+' for row in ms[3])
        ms[3]=[[''.join(row)] for row in ms[3]]
    assert all(len(matrix)==3 and all(len(row)==1 for row in matrix) for matrix in ms[1:]), (record['generation']['template'],[(len(m),list(map(len,m))) for m in ms],ms[2:4])
    for row_index in range(3):
        raw=ms[2][row_index][0];match=re.fullmatch(r'(.*?)\\cdot\s*(.*?)\+(.*?)\\cdot\s*(.*?)\+(.*?)\\cdot\s*(.*?)',raw);assert match,raw
        operands=[number(part) for part in match.groups()];assert operands==[value for j in range(3) for value in (A[row_index,j],V[j])];C['ordered_dot_factors']+=6
        values=[number(part) for part in signed_terms(ms[3][row_index][0])];assert values==[A[row_index,j]*V[j] for j in range(3)],(ms[3][row_index][0],values);C['retained_or_evaluated_cells']+=3
    assert numerical(ms[4])==target;C['retained_or_evaluated_cells']+=3
    if record['generation']['template'].startswith('named'):
        label=re.search(r'\$([A-Z][a-z])(?=[=$])',q[':question/problem'])[1];assert re.search(r'\\begin\{aligned\}'+label+r'\s*&',solution)
    if not record['generation']['evidence_only']:
        level=q[':question/difficulty'].split('/')[-1]
        if level=='easy':assert sum(value==0 for value in V)==1 and all(1<=abs(value)<=4 for value in A) and all(1<=abs(value)<=3 for value in V if value)
        elif level=='moderate':assert all(value!=0 for value in V) and any(abs(value)==1 for value in V) and all(sum(abs(A[i,j])==1 for j in range(3))==1 for i in range(3))
        else:assert all(2<=abs(value)<=8 for value in [*A,*V]) and all(any(A[i,j]*V[j]<0 for j in range(3)) and any(A[i,j]*V[j]>0 for j in range(3)) for i in range(3))
    C['records']+=1

if __name__ == "__main__":
    frozen = json.loads((R/"refresh-2026-10-14/sources"/f"{K}.json").read_text())
    assert json.loads((D/"source.json").read_text()) == frozen
    originals = {q[":question/math-academy-id"]:q for q in frozen["record"][":knowledge-point/questions"]}
    for case in json.loads((D/"source-cases.json").read_text()):
        record = G.generate(case["level"], template=case["template"],
                            parameters=case["parameters"], profile=case["bank_profile"])
        check(record)
        q, old = record["question"], originals[case["source_id"]]
        assert q[":question/problem"] == F.normalize_prose(old[":question/problem"])
        C["source_prompts"] += 1
        for key in (":question/difficulty",":question/worked-solution",":question/answer-fields"):
            assert (key in q) == (key in old)
        if ":question/worked-solution" in old:
            assert q[":question/worked-solution"] == F.normalize_prose(old[":question/worked-solution"])
            C["source_solutions"] += 1
        assert len(q[":question/answer-fields"]) == len(old[":question/answer-fields"])
        for field, source_field in zip(q[":question/answer-fields"],old[":question/answer-fields"]):
            assert field[":answer-field/key"] == source_field[":answer-field/key"]
            assert field[":answer-field/type"] == source_field[":answer-field/type"][":db/ident"]
            assert sorted(signature(a[":answer/value"]) for a in field[":answer-field/choices"]) == sorted(signature(a[":answer/value"]) for a in source_field[":answer-field/choices"])
            assert (":answer-field/correct" in field) == (":answer-field/correct" in source_field)
            if ":answer-field/correct" in source_field:
                answer = next(a for a in field[":answer-field/choices"] if a[":answer/id"] == field[":answer-field/correct"][1])
                assert signature(answer[":answer/value"]) == signature(source_field[":answer-field/correct"][":answer/value"])
                C["source_keys"] += 1
            else:
                C["source_missing_keys"] += 1
            C["source_fields"] += 1
            C["source_values"] += len(source_field[":answer-field/choices"])
    records = json.loads((R/f"qa/{K}-sampled.json").read_text())
    for record in records:
        check(record)
    probe = copy.deepcopy(records[0])
    solution = probe["question"][":question/worked-solution"]
    first_dot = next(matrix[0][0] for matrix in arrays(solution) if r"\cdot" in matrix[0][0])
    bad_dot = first_dot.replace(r"\cdot", "+", 1)
    probe["question"][":question/worked-solution"] = solution.replace(r"\cdot", "+", 1)
    assert probe["question"][":question/worked-solution"] != solution
    saved = C.copy()
    try:
        check(probe)
    except AssertionError:
        pass
    else:
        raise AssertionError("Missing multiply operation survived with unchanged answer")
    C.clear();C.update(saved)
    proof = dict(status="passed", kp_id=K, readback=C,
                 missing_dot_operation_rejected=True,
                 script_sha256=hashlib.sha256(D.with_suffix(".py").read_bytes()).hexdigest())
    (R/f"qa/{K}-root-readback.json").write_text(json.dumps(proof,indent=2)+"\n")
    print(json.dumps(proof))

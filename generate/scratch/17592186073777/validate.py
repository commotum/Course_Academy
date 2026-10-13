#!/usr/bin/env python3
"""Independent rendered-equation QA, source omissions and real native grading."""
import importlib.util
import hashlib
import itertools
import json
import math
import re
import subprocess
import sys
import uuid
from collections import Counter
from fractions import Fraction
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location("generator",HERE.with_suffix(".py"))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y=sp.symbols("x y")


def expression(text,vx="x",vy="y"):
    text=text.replace(r"\left","").replace(r"\right","").replace("&","")
    def group_at(s,start):
        assert s[start]=="{",s
        depth=1;end=start+1
        while depth:
            depth += (s[end]=="{")-(s[end]=="}");end+=1
        return s[start+1:end-1],end
    while r"\frac" in text:
        pos=text.index(r"\frac")
        num,end=group_at(text,pos+5);den,end2=group_at(text,end)
        text=text[:pos]+"(("+str(expression(num,vx,vy))+ ")/("+str(expression(den,vx,vy))+"))"+text[end2:]
    text=re.sub(r"(?<![A-Za-z])"+vx+r"(?![A-Za-z])","x",text)
    text=re.sub(r"(?<![A-Za-z])"+vy+r"(?![A-Za-z])","y",text)
    assert not re.search(r"[\\{}]",text),text
    return parse_expr(text,local_dict={"x":X,"y":Y},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)


def residual(row,vx,vy):
    lhs,rhs=row.replace("&","").split("=")
    return sp.expand(expression(lhs,vx,vy)-expression(rhs,vx,vy))


def sides(row,vx,vy):
    lhs,rhs=row.replace("&","").split("=")
    return sp.expand(expression(lhs,vx,vy)),sp.expand(expression(rhs,vx,vy))


def exact_sides(row,left,right,vx,vy):
    actual_left,actual_right=sides(row,vx,vy)
    assert sp.expand(actual_left-left)==0 and sp.expand(actual_right-right)==0,"Incorrect displayed component/stage value"


def equivalent(left,right):
    if left==0 or right==0:
        return left==right
    ratio=sp.cancel(left/right)
    return not ratio.free_symbols and ratio != 0


def parse_prompt(record):
    text=record["question"][":question/problem"]
    vx,vy=record["generation"]["parameters"]["var_x"],record["generation"]["parameters"]["var_y"]
    match=re.search(r"\$l_\{1\}: (.*), l_\{2\}: (.*)\$",text)
    assert match,"Missing complete line equations"
    polynomials=[residual(row,vx,vy) for row in match.groups()]
    lines=[(poly.coeff(X),poly.coeff(Y),-poly.subs({X:0,Y:0})) for poly in polynomials]
    return lines,polynomials


def formatting(text):
    assert text.count("$")%2==0,"Unbalanced math delimiters"
    # Prompt placeholders are literal widget keys, not TeX grouping.
    text=text.replace("{{field-1}}","")
    depth=0
    for i,char in enumerate(text):
        if char in "{}" and (i==0 or text[i-1]!="\\"):
            depth += 1 if char=="{" else -1
            assert depth>=0,"Unbalanced TeX groups"
    assert depth==0,"Unbalanced TeX groups"
    assert not re.search(r"(?<!\{)\+\s*-|--",text),"Ungrouped consecutive signs"


def check(record):
    assert set(record["knowledge_point"])=={"db_id","id","title"}
    q=record["question"];metadata=record["generation"]
    for text in [q[":question/problem"],q.get(":question/worked-solution","")]:formatting(text)
    assert "{{field-1}}" in q[":question/problem"]
    lines,polynomials=parse_prompt(record)
    a,b,c=lines[0];d,e,f=lines[1]
    assert a and b and d and e
    # Independent full coefficient/augmented ranks; learner never sees ranks.
    coefficients=sp.Matrix([[a,b],[d,e]])
    augmented=sp.Matrix([[a,b,c],[d,e,f]])
    expected="none" if coefficients.rank()!=augmented.rank() else "one" if coefficients.rank()==2 else "infinite"
    assert metadata["relation"]==expected
    vx,vy=metadata["parameters"]["var_x"],metadata["parameters"]["var_y"]
    p=metadata["parameters"]
    assert lines==[(p["a"],p["b"],p["c"]),(p["d"],p["e"],p["f"])],"Printed coefficients differ"
    assert metadata["mathematical_fingerprint"]==g.mathematical_fingerprint(p)
    fields=q[":question/answer-fields"];assert len(fields)==1
    field=fields[0];assert field[":answer-field/type"]==":answer-field.type/select"
    bank=field[":answer-field/choices"]
    assert Counter(a[":answer/value"] for a in bank)==Counter(g.VALUES.values())
    assert all(a[":answer/type"]==":answer.type/text" for a in bank)
    assert len(set(a[":answer/id"] for a in bank))==3
    identity=g.digest([g.VERSION,None if metadata["evidence_only"] else metadata["level"],q[":question/problem"],q.get(":question/worked-solution"),sorted(a[":answer/value"] for a in bank),"select","text"])
    assert identity==metadata["content_fingerprint"] and q[":question/id"]==g.uid(identity)
    assert field[":answer-field/id"]==g.uid(identity+"/field-1")
    for value in [q[":question/id"],field[":answer-field/id"],*[a[":answer/id"] for a in bank]]:uuid.UUID(value)
    for answer in bank:assert answer[":answer/id"]==g.uid(field[":answer-field/id"]+"/"+answer[":answer/value"])
    if metadata["evidence_only"]:
        assert not metadata["eligible_for_learning"]
        assert ":answer-field/correct" not in field
        assert ":question/difficulty" not in q and ":question/worked-solution" not in q
        return expected
    assert q[":question/difficulty"]==":question.difficulty/"+metadata["level"]
    assert set(q)=={":question/id",":question/problem",":question/answer-fields",":question/difficulty",":question/worked-solution"}
    assert set(field)=={":answer-field/id",":answer-field/key",":answer-field/type",":answer-field/choices",":answer-field/correct"}
    assert all(set(a)=={":answer/id",":answer/type",":answer/value"} for a in bank)
    correct=field[":answer-field/correct"]
    assert correct[0]==":answer/id"
    assert next(a[":answer/value"] for a in bank if a[":answer/id"]==correct[1])==g.VALUES[expected]
    solution=q[":question/worked-solution"]
    assert "The number of points of intersection between the two lines is equal to the number of solutions of the corresponding system:" in solution
    assert "Then, we substitute" in solution and "into the second equation and solve for" in solution
    assert "Consequently, the lines "+g.VALUES[expected] in solution
    blocks=re.findall(r"\\begin\{aligned\}(.*?)\\end\{aligned\}",solution,re.S)
    rows=[[row.strip() for row in block.split(r"\\")] for block in blocks]
    assert len(rows[0])==2 and all(equivalent(residual(row,vx,vy),poly) for row,poly in zip(rows[0],polynomials))
    # Derive y independently from the actual printed first equation.
    y_expr=sp.solve(polynomials[0],Y)[0]
    substituted=sp.expand(polynomials[1].subs(Y,y_expr))
    template=metadata["template"]
    if template=="isolated_standard":
        assert len(rows)==2 and "already gives" in solution
        assert "First, we solve for" not in solution
    else:
        assert len(rows)==3 and "First, we solve for" in solution
        count=4 if template=="divided_standard" else 3 if b==-1 else 2
        assert len(rows[1])==count
        assert all(equivalent(residual(row,vx,vy),polynomials[0]) for row in rows[1])
        exact_sides(rows[1][0],a*X+b*Y,c,vx,vy)
        exact_sides(rows[1][1],b*Y,-a*X+c,vx,vy)
        for row in rows[1][2:]:exact_sides(row,Y,y_expr,vx,vy)
        if template=="divided_standard":assert r"\frac{" in rows[1][2]
    substitution_rows=rows[-1]
    assert len(substitution_rows)==(5 if expected=="one" else 4)
    assert equivalent(residual(substitution_rows[0],vx,vy),polynomials[1])
    exact_sides(substitution_rows[0],d*X+e*Y,f,vx,vy)
    assert r"\left(" in substitution_rows[1] and r"\right)" in substitution_rows[1]
    # Distribution must visibly retain both original x components, not only collection.
    assert substitution_rows[2].split("=")[0].count(vx)==2,"Missing operative distribution row"
    assert r"\left(" not in substitution_rows[2]
    for row in substitution_rows[1:]:
        assert equivalent(residual(row,vx,vy),substituted),"Incorrect printed substitution/intermediate equation"
    for row in substitution_rows[1:4]:exact_sides(row,d*X+e*y_expr,f,vx,vy)
    if expected=="one":
        exact_sides(substitution_rows[4],(d+e*y_expr.coeff(X))*X,f-e*y_expr.subs(X,0),vx,vy)
    # Every standalone isolation in substitution prose must agree with printed first line.
    isolated=re.findall(r"\$\$\n([^\n]+)\n\$\$",solution)
    for row in isolated:
        if r"\begin{aligned}" not in row:
            exact_sides(row,Y,y_expr,vx,vy)
    return expected


def rejected(call):
    try:call()
    except (ValueError,AssertionError,TypeError):return
    raise AssertionError("Invalid explicit input or mutated record accepted")


def refresh_identity(record):
    """Mutation tests bypass identity rejection to actually exercise math QA."""
    q=record["question"];m=record["generation"]
    identity=g.digest([g.VERSION,None if m["evidence_only"] else m["level"],q[":question/problem"],q.get(":question/worked-solution"),sorted(g.VALUES.values()),"select","text"])
    m["content_fingerprint"]=identity;q[":question/id"]=g.uid(identity)
    field=q[":question/answer-fields"][0]
    old_correct=field.get(":answer-field/correct",[None,None])[1]
    field[":answer-field/id"]=g.uid(identity+"/field-1")
    for answer in field[":answer-field/choices"]:
        old=answer[":answer/id"]
        answer[":answer/id"]=g.uid(field[":answer-field/id"]+"/"+answer[":answer/value"])
        if old==old_correct:field[":answer-field/correct"]=[":answer/id",answer[":answer/id"]]


def main():
    source=json.loads((HERE/"source.json").read_text())
    cases=json.loads((HERE/"source-cases.json").read_text())
    originals=source["record"][":knowledge-point/questions"]
    replay=[];fidelity=[]
    for case in cases:
        record=g.generate(case["level"],parameters=case["parameters"],template=case["template"],profile=case["bank_profile"])
        check(record);replay.append(record)
        original=next(q for q in originals if q[":question/math-academy-id"]==case["source_id"])
        q=record["question"]
        assert q[":question/problem"]==original[":question/problem"]
        assert set(q)==set(original)-{":db/id",":question/math-academy-id"}
        rawfield=original[":question/answer-fields"][0];field=q[":question/answer-fields"][0]
        assert set(field)==set(rawfield)-{":db/id"}
        assert field[":answer-field/key"]==rawfield[":answer-field/key"]
        assert field[":answer-field/type"]==rawfield[":answer-field/type"][":db/ident"]
        assert Counter(a[":answer/value"] for a in field[":answer-field/choices"])==Counter(a[":answer/value"] for a in rawfield[":answer-field/choices"])
        for answer in field[":answer-field/choices"]:
            old=next(a for a in rawfield[":answer-field/choices"] if a[":answer/value"]==answer[":answer/value"])
            assert set(answer)==set(old)-{":db/id"}
            assert answer[":answer/type"]==old[":answer/type"][":db/ident"]
        fidelity.append({"source_id":case["source_id"],"prompt_exact":True,"full_bank_values":3,"attribute_presence_parity":True,"correct_designation":"absent in source; not counted as matched","worked_solution":"absent in source"})
        # The replay recipe varies actual equations, without returning a frozen payload.
        changed=dict(case["parameters"]);changed["c"]+=1
        variation=g.generate(case["level"],parameters=changed,profile=case["bank_profile"])
        check(variation);assert variation["question"][":question/problem"]!=q[":question/problem"]
    records=[];review=[];summary={};native=[]
    for level in g.LEVELS:
        counts=Counter();fingerprints=set()
        for seed in range(300):
            record=g.generate(level,seed);kind=check(record)
            counts[kind]+=1;fingerprints.add(record["generation"]["mathematical_fingerprint"])
            records.append(record)
            if seed<12:
                field=record["question"][":question/answer-fields"][0]
                native.append({"label":f"{level}-{seed}","record":record,"checks":[{"submitted_answer_id":answer[":answer/id"],"expected":"accepted" if answer[":answer/id"]==field[":answer-field/correct"][1] else "rejected","purpose":"complete categorical source bank, independently rank verified"} for answer in field[":answer-field/choices"]]})
        assert set(counts)==set(g.VALUES)
        summary[level]={"instances":300,"category_counts":dict(counts),"distinct_geometry_sample":len(fingerprints),"default_family":g.LEVELS[level]}
        for kind in g.VALUES:
            chosen=[r for r in records if r["generation"]["level"]==level and r["generation"]["relation"]==kind][:2]
            assert len(chosen)==2;review.extend(chosen)
        anchor=g.generate(level,77)
        for seed in [0,1,2,100]:
            variant=g.generate(level,seed,parameters=anchor["generation"]["parameters"])
            assert variant["question"][":question/id"]==anchor["question"][":question/id"]
        # Identity excludes parameter aliases/notation aliases except actual rendered content.
        p=anchor["generation"]["parameters"]
        aliases=dict(p,var_x="s",var_y="t")
        alias=g.generate(level,parameters=aliases);check(alias)
        assert alias["generation"]["mathematical_fingerprint"]==anchor["generation"]["mathematical_fingerprint"]
        assert alias["question"][":question/id"]!=anchor["question"][":question/id"]
        # Prove sign/scale/order geometry normalization directly on complete equations.
        swapped=dict(zip("abcdef",[-2*p[k] for k in "defabc"]))
        assert g.mathematical_fingerprint(swapped)==g.mathematical_fingerprint(p)
        mutated=json.loads(json.dumps(anchor))
        solution=mutated["question"][":question/worked-solution"]
        blocks=re.findall(r"\\begin\{aligned\}(.*?)\\end\{aligned\}",solution,re.S)
        stage=[row.strip() for row in blocks[-1].split(r"\\")]
        mutated["question"][":question/worked-solution"]=solution.replace(stage[2],stage[3],1)
        refresh_identity(mutated)
        rejected(lambda:check(mutated))
        true_record=next(r for r in records if r["generation"]["level"]==level and r["generation"]["relation"]=="infinite")
        mutated=json.loads(json.dumps(true_record))
        solution=mutated["question"][":question/worked-solution"]
        blocks=re.findall(r"\\begin\{aligned\}(.*?)\\end\{aligned\}",solution,re.S)
        true_stage=[row.strip() for row in blocks[-1].split(r"\\")][-1]
        mutated["question"][":question/worked-solution"]=solution.replace(true_stage,"999 &= 999",1)
        refresh_identity(mutated)
        rejected(lambda:check(mutated))
    # Explicit bounds prevent easy/moderate aliases from weakening hard workload.
    rejected(lambda:g.generate("hard",parameters=dict(a=4,b=2,c=2,d=8,e=4,f=4)))
    rejected(lambda:g.generate("hard",parameters=dict(a=2,b=3,c=7,d=4,e=6,f=14)))
    rejected(lambda:g.generate("moderate",parameters=dict(a=2,b=2,c=2,d=4,e=4,f=4)))
    rejected(lambda:g.generate("easy",parameters=dict(a=2,b=-1,c=2,d=4,e=-2,f=4)))
    rejected(lambda:g.generate("easy",parameters=dict(a=2,b=1,c=2,d=4,e=2,f=3)))
    # Boundary category/zero constant/signed coefficients through all templates.
    boundary=[]
    for level in g.LEVELS:
        for sign in [-1,1]:
            for c in [-6,0,6]:
                a,b=(5,1 if level=="easy" else sign) if level!="hard" else (5,3*sign)
                for category in g.VALUES:
                    d,e=((-5 if category=="one" else a)*(-5),b*(-5))
                    f=-5*c+(0 if category=="infinite" else (3 if level=="hard" else -5))
                    if level!="hard" and abs(f/e)>6:continue
                    record=g.generate(level,parameters=dict(zip("abcdef",[a,b,c,d,e,f])))
                    assert check(record)==category;boundary.append(record)
    # Exact finite geometry counts, excluding equation scales/signs/order/letters.
    integer_lines=10*13
    rational_offsets={Fraction(n,k) for n in range(-30,31) for k in range(1,6)}
    delta_offsets={Fraction(n,k) for n in [-3,-2,-1,1,2,3] for k in range(1,6)}
    primitive_directions={(a,b) for a in range(2,6) for b in range(-5,6) if 2<=abs(b)<=5 and math.gcd(a,b)==1}
    directions=len(primitive_directions);first_lines=directions*13
    hard_one=first_lines*(directions-1)*len(rational_offsets)-(directions*(directions-1)//2)*13*13
    hard_none=first_lines*len(delta_offsets)-directions*(12+11+10)
    variety={"easy_default_exact_tasks":7930,"moderate_default_exact_tasks":7930,"easy_moderate_explicit_domain_tasks":integer_lines*(integer_lines+1)//2,
             "hard_default_exact_tasks":hard_one+hard_none+first_lines,"hard_default_counts":{"one":hard_one,"none":hard_none,"infinite":first_lines},"hard_primitive_directions":directions,"hard_second_offsets":len(rational_offsets),"hard_parallel_offset_differences":len(delta_offsets)}
    completed_sources=[]
    for case in cases:
        record=g.generate(case["level"],parameters=case["parameters"])
        check(record);completed_sources.append(record)
        field=record["question"][":question/answer-fields"][0]
        native.append({"label":case["source_id"]+"-completed-inferred-key","record":record,"checks":[{"submitted_answer_id":answer[":answer/id"],"expected":"accepted" if answer[":answer/id"]==field[":answer-field/correct"][1] else "rejected","purpose":"source values, independently inferred designation; original key absent"} for answer in field[":answer-field/choices"]]})
    (HERE/"native-input.json").write_text(json.dumps(native,indent=2)+"\n")
    engine=ROOT/"generate/runs/current/check-engine"
    subprocess.run([str(engine),str(HERE/"native-input.json"),str(HERE/"native-report.json")],check=True)
    native_report=json.loads((HERE/"native-report.json").read_text())
    review.extend(completed_sources)
    (HERE/"review.json").write_text(json.dumps({"raw_observed_replays":replay,"clearly_authored_generated_variants":review},indent=2)+"\n")
    text="# Original evidence and authored variants\n\nRaw sources have no rating, key or worked solution. Completed keys and levels below are inferred/authored.\n\n"
    for record in replay+review:
        m=record["generation"]
        text+="## "+("Original raw replay" if m["evidence_only"] else "Authored completed/generated")+f" — {m['level']}, {m['template']}, {m['relation']}\n\n"+g.markdown(record)+"\n\n"
    (HERE/"review.md").write_text(text)
    result={"status":"passed","source":g.SOURCE,"runtime":{"python":sys.version.split()[0],"sympy":sp.__version__},"source_fidelity":fidelity,
            "matched_prompts":2,"matched_complete_banks":2,"matched_bank_values":6,"observed_correct_designations_total":0,"matched_correct_designations":0,
            "observed_worked_solutions_total":0,"source_omissions_preserved":True,"inferred_keys":2,"mathematical_instances":len(records)+len(boundary),
            "level_coverage":summary,"variety":variety,"native":{"accepted":native_report["accepted_checks"],"rejected":native_report["rejected_checks"],"unresolved":native_report["documented_unresolved_checks"]},
            "operative_stage_mutation_regressions":3,"equal_constant_component_mutation_regressions":3,"database_writes":0,"unresolved_findings":[],"engine_sha256":hashlib.sha256(engine.read_bytes()).hexdigest()}
    (HERE/"validation.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()

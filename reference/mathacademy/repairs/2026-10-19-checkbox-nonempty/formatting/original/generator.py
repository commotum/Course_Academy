#!/usr/bin/env python3
"""Number of intersection points of two lines (math basis 4670).

Only this KP: infer 0, 1 or infinitely many intersections by substitution.
No intersection coordinates, graphs, ranks or general solution families are
learner methods. replay_source preserves missing difficulty, solution and
correct refs; generated records explicitly infer them. See adjacent evidence.
Each level's finite domain preserves one fixed isolation workload. Complete
categorical banks are observed, not arbitrary numerical error recipes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import random
import sys
import uuid
from pathlib import Path
import sympy as sp
from math_format import checked_math_content, normalize_prose

KP_ID = 17592186073777
KP_UUID = "5fab4792-0fe1-5a5c-8754-509af469da68"
TITLE = "Finding the Number of Intersection Points of Two Lines"
VERSION = "line-intersection-count-3"
X, Y = sp.symbols("x y", real=True)
LEVELS = {"easy": "isolated_standard", "moderate": "unit_standard", "hard": "divided_standard"}
VALUES = {"infinite": "intersect at infinitely many points", "one": "intersect at one point", "none": "do not intersect"}
RAW = {"observed-211986": ("moderate", "unit_standard", "q-211986"),
       "observed-237095": ("easy", "isolated_standard", "q-237095")}
SOURCE = {"database": "math", "basis": 4670, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}


def tex(v):
    return sp.latex(sp.Rational(v))


def linear(terms):
    """Ordered signed sum, retaining separate components even on cancellation."""
    out = ""
    for coeff, variable in terms:
        coeff = sp.Rational(coeff)
        if not coeff:
            continue
        atom = (("" if abs(coeff) == 1 else tex(abs(coeff))) + variable) if variable else tex(abs(coeff))
        out += (("-" if coeff < 0 else "") if not out else (" - " if coeff < 0 else " + ")) + atom
    return out or "0"


def eq(a, b, c, vx="x", vy="y"):
    # This observed spacing is a mask, not a replacement of source strings.
    return linear([(a, vx), (b, vy)]) + (" =" if c < 0 else " = ") + tex(c)


def iso(m, h, vx="x", vy="y"):
    return vy + " = " + linear([(m, vx), (h, "")])


def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def uid(v):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), v))


def primitive(line):
    """Canonical complete equation ax+by=c, up to sign and nonzero scale."""
    vals = [sp.Rational(v) for v in line]
    denominator = sp.ilcm(*[v.q for v in vals])
    integers = [int(v * denominator) for v in vals]
    divisor = math.gcd(*integers)
    result = [v // divisor for v in integers]
    if next(v for v in result if v) < 0:
        result = [-v for v in result]
    return tuple(result)


def mathematical_fingerprint(p):
    # Count equation pairs modulo scale, row order AND variable renaming.
    # Orientation/name changes exercise references but do not inflate variety.
    first, second = ([p[k] for k in "abc"], [p[k] for k in "def"])
    direct = sorted([primitive(first), primitive(second)])
    swapped = sorted([primitive([first[1], first[0], first[2]]),
                      primitive([second[1], second[0], second[2]])])
    return digest(min(direct, swapped))


def relation(p):
    a, b, c, d, e, f = [sp.Rational(p[k]) for k in "abcdef"]
    slope = -a / b
    intercept = c / b
    coefficient = d + e * slope
    constant = e * intercept
    kind = "one" if coefficient else ("infinite" if constant == f else "none")
    return kind, slope, intercept, coefficient, constant


def validate_parameters(level, template, parameters):
    if template != LEVELS[level]:
        raise ValueError("Template requires its documented authored level")
    p = dict(parameters)
    if set(p) - set("abcdef") - {"var_x", "var_y"} or not set("abcdef") <= set(p):
        raise ValueError("Supply exactly six line coefficients and optional variable names")
    for k in "abcdef":
        if isinstance(p[k], bool) or sp.Rational(p[k]).q != 1:
            raise ValueError("Integer displayed coefficients required")
        p[k] = int(p[k])
    p.setdefault("var_x", "x")
    p.setdefault("var_y", "y")
    if (p["var_x"], p["var_y"]) not in [("x", "y"), ("y", "x"), ("u", "v"), ("s", "t")]:
        raise ValueError("Supported variable pairs are x/y, y/x, u/v, s/t")
    a, b, c, d, e, f = [p[k] for k in "abcdef"]
    if (a,b,c) in ((d,e,f),(-d,-e,-f)):
        raise ValueError("Identical or sign-flipped equations are not eligible practice")
    if not all([a, b, d, e]) or abs(c) > 6:
        raise ValueError("Both variable terms must be present; first constant magnitude <= 6")
    if level in ("easy", "moderate"):
        if (b != 1 if level == "easy" else abs(b) != 1):
            raise ValueError("Easy is already isolated; moderate has unit dependent coefficient")
        if not (1 <= abs(a) <= 5 and 2 <= abs(e) <= 5):
            raise ValueError("Integer slope magnitude <=5 and second dependent coefficient magnitude 2..5")
        if d % e or f % e or not (1 <= abs(d // e) <= 5) or abs(f // e) > 6:
            raise ValueError("Second slope and intercept must be bounded integers")
    else:
        if not (2 <= abs(a) <= 5 and 2 <= abs(b) <= 5 and math.gcd(a, b) == 1):
            raise ValueError("Hard needs primitive nonunit coefficients and a noninteger slope")
        if not (2 <= abs(d) <= 25 and 2 <= abs(e) <= 25 and abs(f) <= 30):
            raise ValueError("Hard second coefficient/constant bounds exceeded")
        # Second line must have the same bounded primitive coefficient workload.
        g = math.gcd(d, e)
        if not (2 <= abs(d // g) <= 5 and 2 <= abs(e // g) <= 5 and 1 <= g <= 5):
            raise ValueError("Hard second line must retain nonunit primitive coefficients 2..5")
    return p


def sample(level, rng):
    kind = rng.choice(list(VALUES))
    same_intercept = kind == "infinite" or (kind == "one" and rng.choice([False, True]))
    if level in ("easy", "moderate"):
        m = rng.choice([i for i in range(-5, 6) if i])
        h = rng.randint(-6, 6)
        b = 1 if level == "easy" else rng.choice([-1, 1])
        n = m if kind != "one" else rng.choice([i for i in range(-5, 6) if i and i != m])
        j = h if same_intercept else rng.choice([i for i in range(-6, 7) if i != h])
        e = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        return dict(zip("abcdef", [-m*b, b, h*b, -n*e, e, j*e]))
    pairs = [(a, b) for a in range(-5, 6) for b in range(-5, 6)
             if 2 <= abs(a) <= 5 and 2 <= abs(b) <= 5 and math.gcd(a, b) == 1]
    a, b = rng.choice(pairs)
    c = rng.randint(-6, 6)
    d, e = (a, b) if kind != "one" else rng.choice([
        (d, e) for d, e in pairs if a*e != b*d and (not same_intercept or (c*e) % b == 0)])
    k = rng.choice([v for v in range(-5, 6) if abs(v) >= 2 and
                    (not same_intercept or abs(sp.Rational(v*e*c, b)) <= 30)])
    if kind == "infinite":
        f = k*c
    elif same_intercept:
        f = k*e*c // b
    else:
        f = rng.choice([v for v in range(-30, 31) if v*b != k*e*c])
    return dict(zip("abcdef", [a, b, c, k*d, k*e, f]))


def worked_solution(p, template):
    """Canonical shared prose; all operative isolation/substitution stages."""
    a,b,c,d,e,f = [p[k] for k in "abcdef"]
    vx,vy = p["var_x"],p["var_y"]
    kind,m,h,coefficient,constant = relation(p)
    first = iso(m,h,vx,vy) if template == "isolated_standard" else eq(a,b,c,vx,vy)
    second = eq(d,e,f,vx,vy)
    system = r"\left\{\begin{aligned}" + first.replace(" =", " &=") + r" \\ " + second.replace(" =", " &=") + r"\end{aligned}\right."
    opening = "The number of points of intersection between the two lines is equal to the number of solutions of the corresponding system:\n\n$$\n" + system + "\n$$\n\n"
    isolated = iso(m,h,vx,vy)
    if template == "isolated_standard":
        opening += f"We will solve the system using substitution. The first equation already gives ${vy}$ in terms of ${vx}$:\n\n$$\n{isolated}\n$$\n\n"
    else:
        stages = [first, linear([(b,vy)]) + " = " + linear([(-a,vx),(c,"")])]
        if abs(b) != 1:
            stages.append(vy + r" = \frac{" + linear([(-a,vx),(c,"")]) + "}{" + tex(b) + "}")
        if b != 1:
            stages.append(isolated)
        opening += f"We will solve the system using substitution. First, we solve for ${vy}$ in the first equation:\n\n$$\n" + aligned(stages) + "\n$$\n\n"
    # Render the actual substitution as a grouped signed numeric multiplier.
    substituted = linear([(d,vx)]) + (" - " if e < 0 else " + ") + tex(abs(e)) + r"\left(" + linear([(m,vx),(h,"")]) + r"\right) = " + tex(f)
    distributed = linear([(d,vx),(e*m,vx),(e*h,"")]) + " = " + tex(f)
    collected = linear([(coefficient,vx),(constant,"")]) + " = " + tex(f)
    stages = [second, substituted, distributed, collected]
    if coefficient:
        # Enough to count solutions; do not ask for or compute the point.
        stages.append(linear([(coefficient,vx)]) + " = " + tex(f-constant))
    opening += "Then, we substitute\n\n$$\n" + isolated.replace(" = ","=") + f"\n$$\n\ninto the second equation and solve for ${vx}$:\n\n$$\n" + aligned(stages) + "\n$$\n\n"
    if kind == "infinite":
        opening += "The result is a statement that's always true. Therefore, we conclude that the system has infinitely many solutions.\n\nConsequently, the lines intersect at infinitely many points (i.e., they coincide)."
    elif kind == "none":
        opening += "The result is a statement that's always false. Therefore, we conclude that the system has no solutions.\n\nConsequently, the lines do not intersect (i.e., they are parallel)."
    else:
        opening += f"The coefficient of ${vx}$ is nonzero, so this equation determines exactly one value of ${vx}$. The first equation then determines exactly one value of ${vy}$. Therefore, the system has one solution.\n\nConsequently, the lines intersect at one point."
    return opening


def aligned(rows):
    return r"\begin{aligned}" + "\n" + (" " + r"\\" + "\n").join(row.replace(" =", " &=", 1) for row in rows) + "\n" + r"\end{aligned}"


def line_definitions(first, second):
    """Give each named line its own row; align labels and equality signs."""
    rows = []
    for i, equation in enumerate((first, second), 1):
        left, right = equation.split("=")
        rows.append(f"l_{{{i}}}:\\quad & " + left.strip() + r" &{}={}& " + right.strip())
    return "$$\n" + r"\begin{alignedat}{2}" + "\n" + (r" \\[6pt]" + "\n").join(rows) + "\n" + r"\end{alignedat}" + "\n$$"


@checked_math_content
def generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None):
    if level not in LEVELS:
        raise ValueError("Difficulty must be easy, moderate or hard")
    if profile in RAW:
        raise ValueError("Use replay_source() for incomplete observed evidence")
    if profile not in [None, "categorical"]:
        raise ValueError("Unknown bank profile")
    template = template or LEVELS[level]
    if field_type not in [None, "select", ":answer-field.type/select"]:
        raise ValueError("Observed layout is one select field")
    rng = random.Random(seed)
    if parameters is None:
        parameters = sample(level, rng)
        parameters["var_x"], parameters["var_y"] = rng.choice([("x", "y"), ("y", "x")])
    p = validate_parameters(level, template, parameters)
    a,b,c,d,e,f = [p[k] for k in "abcdef"]
    vx,vy = p["var_x"],p["var_y"]
    kind,m,h,_,_ = relation(p)
    first = iso(m,h,vx,vy) if template == "isolated_standard" else eq(a,b,c,vx,vy)
    second = eq(d,e,f,vx,vy)
    prompt = "Consider the lines $l_{1}$ and $l_{2}$, defined by\n\n" + line_definitions(first, second) + "\n\nAt how many points do these lines intersect?\n\nThe lines $l_{1}$ and $l_{2}$ {{field-1}}."
    solution = worked_solution(p,template)
    prompt = normalize_prose(prompt)
    solution = normalize_prose(solution)
    identity = digest([VERSION, level, prompt, solution, sorted(VALUES.values()), "select", "text"])
    field_id = uid(identity+"/field-1")
    answers = [{":answer/id": uid(field_id+"/"+value), ":answer/type": ":answer.type/text", ":answer/value": value} for value in VALUES.values()]
    rng.shuffle(answers)
    field = {":answer-field/id": field_id, ":answer-field/key": "field-1", ":answer-field/type": ":answer-field.type/select", ":answer-field/choices": answers}
    question = {":question/id": uid(identity), ":question/problem": prompt, ":question/answer-fields": [field]}
    field[":answer-field/correct"] = [":answer/id",uid(field_id+"/"+VALUES[kind])]
    question[":question/difficulty"] = ":question.difficulty/"+level
    question[":question/worked-solution"] = solution
    return {"knowledge_point": {"db_id": KP_ID,"id":KP_UUID,"title":TITLE}, "question":question,
            "generation": {"version":VERSION,"source":SOURCE,"seed":seed,"level":level,"template":template,
                "profile":profile or "categorical","parameters":p,"mathematical_fingerprint":mathematical_fingerprint(p),
                "content_fingerprint":identity,"relation":kind,"authored_level":True,"inferred_correct":True,
                "source_ids": ["e-14011"] + (["q-237095"] if template=="isolated_standard" else ["q-211986"] if template=="unit_standard" else ["e-14370"]),
                "isolation_variable":vy,"intercept_case":"equal" if sp.Rational(c,b)==sp.Rational(f,e) else "unequal",
                "domain":{"displayed_coefficients":"integers; both variable terms nonzero", "first_constant":[-6,6],
                          "coefficient_policy":"bounded integer slopes" if level!="hard" else "primitive nonunit magnitudes 2..5, scale magnitude 2..5"},
                "evidence_only":False,"eligible_for_learning":True,"plots":"none",
                "runtime":{"python":sys.version.split()[0],"sympy":sp.__version__}}}


def replay_source(source_id):
    """Immutable complete captured evidence, including explicitly absent fields.

    This is not learner output: original practice records lack keys/solutions.
    """
    data = json.loads(Path(__file__).with_name("source_cases.json").read_text())
    for question in [*data["questions"], data["canonical"]]:
        if question[":question/math-academy-id"] == source_id:
            return question
    raise ValueError("Unknown source question")


# Easy: one already-isolated equation; bounded integer substitution/distribution.
def generate_easy(seed=0, template=None, field_type=None, parameters=None, profile=None):
    return generate("easy",seed,template,field_type,parameters,profile)


# Moderate: first unit dependent coefficient must be moved/isolated before substitution.
def generate_moderate(seed=0, template=None, field_type=None, parameters=None, profile=None):
    return generate("moderate",seed,template,field_type,parameters,profile)


# Hard: primitive nonunit coefficients require exact rational division first.
def generate_hard(seed=0, template=None, field_type=None, parameters=None, profile=None):
    return generate("hard",seed,template,field_type,parameters,profile)


def markdown(record):
    q=record["question"]
    return q[":question/problem"]+"\n\nChoices: "+"; ".join(a[":answer/value"] for a in q[":question/answer-fields"][0][":answer-field/choices"])+( "\n\n"+q[":question/worked-solution"] if ":question/worked-solution" in q else "\n\n[Raw evidence: source has no worked solution or correct reference.]")


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--difficulty",choices=[*LEVELS,"all"],default="moderate")
    parser.add_argument("--seed",type=int,default=0)
    parser.add_argument("--count",type=int,default=1)
    parser.add_argument("--format",choices=["markdown","json"],default="markdown")
    parser.add_argument("--template")
    parser.add_argument("--profile")
    parser.add_argument("--parameters",help="Explicit JSON six-coefficient mapping")
    args=parser.parse_args()
    levels=list(LEVELS) if args.difficulty=="all" else [args.difficulty]
    if args.count < 1:
        parser.error("--count must be positive")
    records=[generate(level,args.seed+i,args.template,parameters=json.loads(args.parameters) if args.parameters else None,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=="json" else "\n\n---\n\n".join(markdown(r) for r in records))

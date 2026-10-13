#!/usr/bin/env python3
"""Cartesian equations from trig parametrizations: guide-based scratch rebuild.

Source: math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.
Classification/extraction/review evidence lives beside this file in 17592186100890/.
20 practice questions -> 13 observed Markdown/value templates and 14 complete
source radio banks; moderate adds two authored cotangent templates and four
authored banks. All have plot rating none. Every source option is replay-tested.
Steps 5 and 7 therefore need no renderer. This script stops before database prep.

    .venv/bin/python generate/scratch/17592186100890.py --seed 42
    .venv/bin/python generate/scratch/17592186100890.py --difficulty easy \
        --template ellipse_cos_blank --count 2
    .venv/bin/python generate/scratch/17592186100890.py --difficulty moderate \
        --format json
    .venv/bin/python generate/scratch/17592186100890.py --difficulty easy \
        --profile sin_unit_x_shift_identity --seed 42

SymPy handles exact arithmetic and comparison; no floating-point answer checks.
Sample ranges are draft policies, not recovered source code. Moderate questions
sample positive coefficients a and b from 1 through 4 and an open quadrant from
I through IV by default. The original
unit coefficients remain valid inputs for replay, without a separate mode.
The original non-real sin/tan distractors are retained as observed source shapes.
Observed error interpretations are hypotheses; authored recipe operations are
explicit. Both remain author metadata, never option feedback.
The default moderate banks are authored extensions; observed banks remain
available by profile for source replay. Families and quadrants are unordered
variations at the same difficulty. Profiles contain exactly four recipes, chosen together before sampling; an
invalid member rejects the entire instance. Profile eligibility and formulas
generalize observed expressions, without claiming the original authoring code.

Question text and solution sentences follow the extracted sources. There is one
fixed solution, regardless of the chosen answer. Domain/branch restrictions are
retained separately in metadata, as the guide requires; author previews show them.
The canonical example's excluded-endpoint error is documented in extraction, not
copied into generated questions. Math rendering uses standard trig LaTeX instead
of the source's invisible Unicode function-application characters.

JSON is a local REVIEW RECORD, not an EDB transaction: UUID/enum strings need
typed conversion later. Questions/fields/answers have stable field-owned UUIDs;
fixed parameters and bank contents keep identity across seed/order changes;
changing the authored bank changes content identity. Existing attributes are
used, no Math Academy IDs are invented, and recipe metadata remains outside them.
Radio answers contain whole equations; blanks contain only their required LHS
or RHS. The application's real grader is checked separately in the local evidence
folder, including equivalent expanded/factored forms and radical normalization.
Never expose correct refs or author metadata before
submission. EDB many-ref banks do not guarantee persistent option ordering.

API: generate_easy / generate_moderate / generate_hard(seed, template=None,
field_type=None, parameters=None, profile=None).
Explicit parameters are validated and never silently resampled.
No database clients, transactions, or plot-generation dependencies are included.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import uuid
from dataclasses import dataclass

try:
    import sympy as sp
except ImportError as exc:
    raise SystemExit("Use the project's .venv/bin/python (SymPy is required).") from exc

KP_ID = 17592186100890
KP_UUID = "78dbecb4-68d4-53b0-b47f-f37ce92da896"
TITLE = "Finding the Cartesian Equation of a Curve Defined Parametrically With Trigonometric Functions"
VERSION = "trig-cartesian-guide-draft-4"
SOURCE = {"database": "math", "basis_t": 1356,
          "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}
X, Y, T = sp.symbols("x y t", real=True)
A, B, H, K = sp.symbols("a b h k", real=True)
S = sp.Symbol("missing_sign", real=True)
U, V = sp.symbols("u v", positive=True)
OPENING = "First, let's make the trigonometric functions the subject of each equation:"
PYTHAGOREAN = r"\sin^2 t+\cos^2 t=1"


@dataclass(frozen=True)
class Template:
    level: str
    kind: str
    family: str
    sources: tuple[str, ...]
    answer_shape: str = "equation"


TEMPLATES = {
    "ellipse_sin_radio": Template("easy", "radio", "ellipse_sin", ("q-15751", "q-102680", "q-102682", "q-15657")),
    "ellipse_cos_radio": Template("easy", "radio", "ellipse_cos", ("q-15752", "q-15679")),
    "ellipse_sin_blank": Template("easy", "blank", "ellipse_sin", ("q-320946",), "lhs"),
    "ellipse_cos_blank": Template("easy", "blank", "ellipse_cos", ("q-319828",), "lhs"),
    "tan_sec_radio": Template("easy", "radio", "tan_sec", ("q-102677",)),
    "cot_csc_radio": Template("easy", "radio", "cot_csc", ("q-15761",)),
    "cot_csc_blank": Template("easy", "blank", "cot_csc", ("q-321400",), "rhs"),
    "cos_tan_radio": Template("moderate", "radio", "cos_tan", ("q-102687",)),
    "sin_tan_radio": Template("moderate", "radio", "sin_tan", ("q-15759",)),
    "cos_cot_radio": Template("moderate", "radio", "cos_cot", ()),
    "sin_cot_radio": Template("moderate", "radio", "sin_cot", ()),
    "sin_double_factored_radio": Template("hard", "radio", "sin_double_factored", ("q-24378",)),
    "sin_double_expanded_radio": Template("hard", "radio", "sin_double_expanded", ("q-24576",)),
    "cos_double_radio": Template("hard", "radio", "cos_double", ("q-24574", "q-24575")),
    "cos_double_blank": Template("hard", "blank", "cos_double", ("q-321314", "q-321315", "q-321318"), "rhs"),
}


@dataclass(frozen=True)
class Relation:
    lhs: sp.Expr
    rhs: sp.Expr
    lhs_tex: str
    rhs_tex: str

    @property
    def latex(self) -> str:
        return self.lhs_tex + "=" + self.rhs_tex


@dataclass(frozen=True)
class Wrong:
    recipe: str
    relation: Relation


@dataclass(frozen=True)
class Recipe:
    """Parameterized choice transformation; observed error interpretations are hypotheses."""
    label: str
    lhs: sp.Expr
    rhs: sp.Expr
    squares: tuple = ()
    factor: sp.Expr | None = None

    def render(self, p: dict, missing_sign: int = 1) -> Wrong:
        values = {symbol: p[key] for symbol,key in ((A,'a'),(B,'b'),(H,'h'),(K,'k')) if key in p}
        values[S] = missing_sign
        lhs, rhs = (sp.sympify(expr).subs(values) for expr in (self.lhs,self.rhs))
        lhs_tex, rhs_tex = tex(lhs), tex(rhs)
        if self.squares:
            parts = []
            for coefficient,numerator,denominator in self.squares:
                c,n,d = (sp.sympify(expr).subs(values) for expr in (coefficient,numerator,denominator))
                part = coefficient_term(c,square(ratio(n,int(d))))
                parts.append(('+' if parts and not part.startswith('-') else '')+part)
            lhs_tex = ''.join(parts)
        if self.factor is not None:
            f = self.factor.subs(values)
            inner = sp.cancel(self.rhs/self.factor).subs(values)
            rhs_tex = tex(f)+r'\left('+tex(inner)+r'\right)'
        if lhs == Y**2:
            # Retain the source's normalized/inverted squared-ratio notation.
            a=p['a']; sx=square(ratio(X,a))
            rhs_tex={
                'reverse_identity_constant':sx+'-1',
                'invert_coordinate_ratio':square(r'\frac{'+str(a)+'}{x}')+'+1',
                'omit_scale_and_use_it_as_constant':'x^2+'+str(a),
                'reverse_squared_term':'1-'+sx,
                'omit_coordinate_scale':'1+x^2',
                'use_scale_as_coefficient_and_reverse_sign':'1-'+str(a)+'x^2',
                'use_scale_minus_one':'1+'+square(ratio(X,a-1)),
            }.get(self.label,rhs_tex)
        return Wrong(self.label,Relation(lhs,rhs,lhs_tex,rhs_tex))


def squares(label, hx=0, ky=0, ax=1, by=1, cx=1, cy=1, rhs=1, y_first=False):
    terms = ((cx,X-hx,ax),(cy,Y-ky,by))
    if y_first:
        terms = tuple(reversed(terms))
    return Recipe(label,cx*((X-hx)/ax)**2+cy*((Y-ky)/by)**2,sp.sympify(rhs),terms)


def rhs_recipe(label, value, factor=None, lhs=Y):
    return Recipe(label,lhs,sp.sympify(value),factor=factor)


@dataclass(frozen=True)
class BankProfile:
    template: str
    source: str
    recipes: tuple[Recipe, ...]
    conditions: str
    origin: str = "observed"


# Each tuple is a COMPLETE observed four-distractor bank, not a candidate pool.
# One source example cannot identify the original authoring algorithm: these
# formulas reproduce its values and define explicit, testable generalizations.
BANK_PROFILES = {
    'sin_shift_exchange': BankProfile('ellipse_sin_radio','q-15751',(
        squares('reverse_both_offsets',-H,-K,A,B),
        squares('exchange_scales_and_offsets_keep_x_sign',-K,-H,B,A),
        squares('exchange_scales_and_offsets_reverse_y_sign',-K,H,B,A),
        squares('reverse_x_offset',-H,K,A,B),
    ),'Unequal positive scales; both offsets nonzero.'),
    'sin_unit_y_shift': BankProfile('ellipse_sin_radio','q-102680',(
        squares('apply_y_offset_to_both_coordinates',K,K),
        squares('move_offset_to_x_with_reversed_sign',-K,0),
        squares('reverse_y_offset',0,-K),
        squares('replace_y_offset_with_coefficient',cy=-K),
    ),'Unit scales; h=0 and k<0.'),
    'sin_compound_scale_offset': BankProfile('ellipse_sin_radio','q-102682',(
        squares('use_y_offset_as_x_scale_and_x_scale_as_y_offset',H,-A,-K,B),
        squares('exchange_offsets',K,H,A,B),
        squares('use_y_offset_as_x_scale_and_exchange_y_scale',H,K,-K,A),
        squares('exchange_scale_offset_roles_in_both_coordinates',A,-H,H,-K),
    ),'Positive scales; both offsets nonzero; whole-bank distinctness is checked.'),
    'sin_unit_x_shift_identity': BankProfile('ellipse_sin_radio','q-15657',(
        squares('move_x_offset_to_y_with_reversed_sign',0,-H),
        squares('replace_x_offset_with_coefficient',cx=-H),
        squares('move_x_offset_to_identity_constant',rhs=-H),
        squares('reverse_and_duplicate_offset_and_change_constant',-H,-H,rhs=-H),
    ),'Unit scales; h<=-2 and k=0.'),
    'cos_identity_scale': BankProfile('ellipse_cos_radio','q-15752',(
        squares('exchange_scales_subtract_and_use_interval_constant',H,K,B,A,-1,1,2*sp.pi,True),
        squares('subtract_y_identity_term',H,K,A,B,1,-1,1,True),
        squares('omit_scales_and_use_product_as_constant',H,K,rhs=A*B),
        squares('exchange_scales_and_subtract',H,K,B,A,-1,1,1,True),
    ),'Unequal positive scales; offsets may be zero or nonzero.'),
    'cos_unit_shift_identity': BankProfile('ellipse_cos_radio','q-15679',(
        squares('omit_x_offset',0,K,y_first=True),
        squares('exchange_offsets_and_reverse_x_sign',K,-H,y_first=True),
        squares('reverse_y_offset_and_change_constant',H,-K,rhs=K,y_first=True),
        squares('omit_y_offset_shift_x_by_y_offset_and_change_constant',-K,0,rhs=K,y_first=True),
    ),'Unit scales; h<0 and k>=2.'),
    'tan_sec_source': BankProfile('tan_sec_radio','q-102677',(
        rhs_recipe('reverse_identity_constant',X**2/A**2-1,lhs=Y**2),
        rhs_recipe('invert_coordinate_ratio',1+A**2/X**2,lhs=Y**2),
        rhs_recipe('omit_scale_and_use_it_as_constant',X**2+A,lhs=Y**2),
        rhs_recipe('reverse_squared_term',1-X**2/A**2,lhs=Y**2),
    ),'a>=2; b=1.'),
    'cot_csc_source': BankProfile('cot_csc_radio','q-15761',(
        rhs_recipe('omit_coordinate_scale',1+X**2,lhs=Y**2),
        rhs_recipe('reverse_squared_term',1-X**2/A**2,lhs=Y**2),
        rhs_recipe('use_scale_as_coefficient_and_reverse_sign',1-A*X**2,lhs=Y**2),
        rhs_recipe('use_scale_minus_one',1+X**2/(A-1)**2,lhs=Y**2),
    ),'a>=3; b=1; a=2 would duplicate two options.'),
    'cos_tan_source': BankProfile('cos_tan_radio','q-102687',(
        rhs_recipe('double_denominator',B*sp.sqrt(A**2-X**2)/(2*X)),
        rhs_recipe('omit_root_and_double_denominator',B*(1-X**2/A**2)/(2*X/A)),
        rhs_recipe('omit_tangent_denominator',B*sp.sqrt(1-X**2/A**2)),
        rhs_recipe('omit_root',B*(1-X**2/A**2)/(X/A)),
    ),'Positive coefficients; sampling uses a,b in 1..4; source coefficients are both one.'),
    'sin_tan_source': BankProfile('sin_tan_radio','q-15759',(
        rhs_recipe('alter_factor_and_radical_sign',4*B*X/sp.sqrt(A**2+X**2)),
        rhs_recipe('reverse_radical_sign_and_alter_constant',B*X/sp.sqrt(X**2-4*A**2)),
        rhs_recipe('alter_factor_and_radical_constant',2*B*X/sp.sqrt(2*A**2+X**2)),
        rhs_recipe('reverse_radical_sign_and_double_factor',2*B*X/sp.sqrt(X**2-A**2)),
    ),'Positive coefficients; sampling uses a,b in 1..4; source coefficients are both one.'),
    'sin_double_factored_source': BankProfile('sin_double_factored_radio','q-24378',(
        rhs_recipe('omit_y_scale_and_double_angle_factor',1-X**2/A**2),
        rhs_recipe('reverse_sign_and_omit_double_angle_factor',B*(1+X**2/A**2),B),
        rhs_recipe('alter_outer_scale_sign_and_double_angle_factor',(B-1)*(1+X**2/A**2),B-1),
        rhs_recipe('omit_y_scale',1-2*X**2/A**2),
    ),'Positive a; b>=2.'),
    'sin_double_expanded_source': BankProfile('sin_double_expanded_radio','q-24576',(
        rhs_recipe('alter_constant_and_unsquare_scale',1-B*X**2/A),
        rhs_recipe('reverse_constant_and_omit_quadratic_scale',-B+X**2),
        rhs_recipe('exchange_constant_and_denominator_roles',-A**2/2-X**2/B),
        rhs_recipe('reciprocate_constant_and_omit_scale',-1/B-X**2),
    ),'Positive a; negative b.'),
    'cos_double_positive_source': BankProfile('cos_double_radio','q-24574',(
        rhs_recipe('alter_outer_scale_and_use_scale_plus_one',(B+1)*(X**2/(A+1)-1),B+1),
        rhs_recipe('use_unsquared_scale_and_reverse_constant',X**2/A+1),
        rhs_recipe('alter_quadratic_coefficient_and_use_scale_product_as_constant',(B+1)*X**2+A*B),
        rhs_recipe('reverse_identity_and_omit_outer_scale',1-2*X**2/A**2),
    ),'Positive a and b.'),
    'cos_double_negative_source': BankProfile('cos_double_radio','q-24575',(
        rhs_recipe('omit_outer_scale_and_double_angle_factor',X**2/A**2-1),
        rhs_recipe('use_twice_signed_scale_and_reverse_constant',1-X**2/(2*A)),
        rhs_recipe('reverse_identity_and_omit_double_angle_factor',1-X**2/A**2),
        rhs_recipe('use_scale_difference_reverse_constant_and_omit_double_angle_factor',(B-A)*(X**2/A**2+1),B-A),
    ),'Negative a; positive b.'),
}

# Authored counterparts preserve the moderate operation count, not source banks.
# S is the sign of the recovered function, determined by the given quadrant.
for family in ("cos_tan", "sin_tan", "cos_cot", "sin_cot"):
    root_denominator = family in ("sin_tan", "cos_cot")
    correct = B*S*X/sp.sqrt(A**2-X**2) if root_denominator else B*S*sp.sqrt(A**2-X**2)/X
    dropped_root = B*S*A*X/(A**2-X**2) if root_denominator else B*S*(A**2-X**2)/(A*X)
    # Omitting b is invisible at b=1; in that case use an erroneous doubled b.
    scale_error = sp.Piecewise((1/B, sp.Ne(B, 1)), (2, True))
    BANK_PROFILES[family+"_variation"] = BankProfile(family+"_radio", "", (
        rhs_recipe("wrong_square_root_branch", -correct),
        rhs_recipe("invert_trigonometric_quotient", B**2/correct),
        rhs_recipe("omit_square_root", dropped_root),
        rhs_recipe("incorrect_y_scale", correct*scale_error),
    ), "a,b in 1..4; one open quadrant; all four errors real and distinct on its x-domain.", "authored")


QUADRANTS = {1: (1,1), 2: (1,-1), 3: (-1,-1), 4: (-1,1)}  # sine, cosine signs


def quadrant_interval(q: int) -> str:
    return {1: r"0<t<\frac{\pi}{2}", 2: r"\frac{\pi}{2}<t<\pi",
            3: r"\pi<t<\frac{3\pi}{2}", 4: r"\frac{3\pi}{2}<t<2\pi"}[q]


def missing_function_sign(spec: Template, p: dict) -> int:
    sine_sign, cosine_sign = QUADRANTS[p.get("quadrant",1)]
    return sine_sign if spec.family.startswith("cos_") else cosine_sign


@dataclass(frozen=True)
class Built:
    x_t: sp.Expr
    y_t: sp.Expr
    fx: str
    fy: str
    relation: Relation
    solution: str
    period: bool
    restrictions: str
    blank_tex: str | None = None
    quadrant: int = 1


class SampleRejected(ValueError):
    """The parameters invalidate a required member of the complete bank."""


def tex(value: sp.Expr | int) -> str:
    return sp.latex(sp.sympify(value), order="lex")


def block(value: str) -> str:
    return "$$\n" + value + "\n$$"


def aligned(rows: list[tuple[str, str]]) -> str:
    return block("\\begin{aligned}\n" + " \\\\\n".join(a + " & " + b for a, b in rows) + "\n\\end{aligned}")


def trig(name: str) -> str:
    return r"\cos 2t" if name == "cos2" else "\\" + name + " t"


def function(scale: int, name: str, shift: int = 0) -> str:
    prefix = "" if scale == 1 else "-" if scale == -1 else str(scale)
    suffix = "" if shift == 0 else "+" + str(shift) if shift > 0 else str(shift)
    return prefix + trig(name) + suffix


def ratio(var: sp.Expr, scale: int, shift: int = 0) -> str:
    if scale == 1:
        return tex(var - shift)
    return ("-" if scale < 0 else "") + r"\frac{" + tex(var - shift) + "}{" + str(abs(scale)) + "}"


def square(value: str) -> str:
    return value + "^2" if value in ("x", "y") else r"\left(" + value + r"\right)^2"


def coefficient_term(coefficient: sp.Expr, value: str) -> str:
    if coefficient == 1:
        return value
    if coefficient == -1:
        return "-" + value
    return tex(coefficient) + value


def explicit(value: sp.Expr, display: str | None = None) -> Relation:
    return Relation(Y, value, "y", display or tex(value))


def ellipse(p: dict, sine_first: bool, sign: int = 1, rhs: sp.Expr | int = 1) -> Relation:
    a, b, h, k = (p[key] for key in ("a", "b", "h", "k"))
    ex, ey = ((X-h)/a)**2, ((Y-k)/b)**2
    tx, ty = square(ratio(X, a, h)), square(ratio(Y, b, k))
    display = tx + ("+" if sign == 1 else "-") + ty
    if not sine_first and sign == 1:
        display = ty + "+" + tx
    return Relation(ex + sign*ey, sp.sympify(rhs), display, tex(rhs))


def opening(p: dict, fx: str, fy: str) -> str:
    a, b, h, k = p["a"], p["b"], p.get("h", 0), p.get("k", 0)
    return OPENING + "\n\n" + aligned([
        ("x=" + function(a, fx, h), r"\Rightarrow\quad " + trig(fx) + "=" + ratio(X, a, h)),
        ("y=" + function(b, fy, k), r"\Rightarrow\quad " + trig(fy) + "=" + ratio(Y, b, k)),
    ])


def substitution(p: dict, fx: str, fy: str) -> str:
    return (f"Substituting ${trig(fx)}={ratio(X,p['a'],p.get('h',0))}$ and "
            f"${trig(fy)}={ratio(Y,p['b'],p.get('k',0))}$ into this formula, we get")


def ending(relation: Relation, comma: bool = False) -> str:
    return "\n\nSo" + (", " if comma else " ") + "the Cartesian equation of the given curve is $" + relation.latex + ".$"


def polynomial_signature(relation: Relation) -> tuple:
    polynomial = sp.Poly(sp.fraction(sp.cancel(relation.lhs-relation.rhs))[0], X, Y)
    return tuple((power, sp.cancel(c/polynomial.LC())) for power, c in polynomial.terms()) if not polynomial.is_zero else ()


def distinct(a: Relation, b: Relation, points: list[dict]) -> bool:
    if a.lhs == Y and b.lhs == Y:
        delta = sp.simplify(a.rhs-b.rhs)
        return delta != 0 and any(sp.simplify(delta.subs(point)).is_zero is False for point in points)
    return polynomial_signature(a) != polynomial_signature(b)


def verify(built: Built) -> list[dict]:
    """Independent exact curve oracle; prove radical signs on the whole quadrant."""
    s, c = 2*U/(1+U**2), (1-U**2)/(1+U**2)
    if not built.period:
        sine_sign, cosine_sign = QUADRANTS[built.quadrant]
        s, c = sine_sign*s, cosine_sign*c
    table = {sp.sin(T): s, sp.cos(T): c, sp.cos(2*T): c**2-s**2,
             sp.tan(T): s/c, sp.cot(T): c/s, sp.sec(T): 1/c, sp.csc(T): 1/s}
    xx, yy = (sp.cancel(expr.xreplace(table)) for expr in (built.x_t, built.y_t))
    relation = built.relation
    if any(abs(power.exp) == sp.Rational(1,2) for power in relation.rhs.atoms(sp.Pow)):
        # v>0 parametrizes the ENTIRE open quadrant via u=v/(1+v).
        rr = sp.factor(relation.rhs.subs(X,xx).subs(U,V/(1+V)))
        ry = sp.factor(yy.subs(U,V/(1+V)))
        if sp.cancel(rr-ry) != 0 or not (rr.is_positive is True and ry.is_positive is True
                                       or rr.is_negative is True and ry.is_negative is True):
            raise AssertionError("Selected-root answer fails the whole-quadrant parametrization")
    elif sp.cancel((relation.lhs-relation.rhs).subs({X:xx,Y:yy}, simultaneous=True)) != 0:
        raise AssertionError("Answer fails the original parametrization")
    return [{X:xx.subs(U,q), Y:yy.subs(U,q)} for q in
            (sp.Rational(1,5),sp.Rational(1,3),sp.Rational(1,2),sp.Rational(3,4))]


def validate_parameters(spec: Template, p: dict) -> None:
    required = {"a", "b", "h", "k"} if spec.family.startswith("ellipse") else {"a", "b"}
    if spec.level == "moderate" and "quadrant" in p:
        required.add("quadrant")
    if set(p) != required or any(type(value) is not int for value in p.values()):
        raise ValueError(f"Expected integer parameters {sorted(required)}")
    if spec.level == "moderate" and (p.get("quadrant",1) not in QUADRANTS or
                                     not all(1 <= p[key] <= 4 for key in ("a","b"))):
        raise ValueError("Moderate requires a,b in 1..4 and quadrant in 1..4")
    a,b = p["a"],p["b"]
    if a == 0 or b == 0:
        raise ValueError("Scales must be nonzero")
    if spec.level != "hard" and (a < 0 or b < 0):
        raise ValueError("These source families use positive scales")
    if spec.family.startswith("ellipse") and spec.kind == "blank" and (p['h'] != 0 or b != 1):
        raise ValueError("Source ellipse blanks have no x shift and unit y scale")
    if spec.family in ("tan_sec","cot_csc") and spec.kind == "radio" and b != 1:
        raise ValueError("Source hyperbola radio questions have unit y scale")
    if spec.family.startswith("sin_double") and a < 0:
        raise ValueError("Source sine/double-angle questions use positive x scale")
    if spec.family == "sin_double_factored" and b < 0 or spec.family == "sin_double_expanded" and b > 0:
        raise ValueError("Signed y scale determines this source value/solution template")
    if spec.family == "cos_double" and spec.kind == "radio" and b < 0:
        raise ValueError("Source cosine/double-angle radio questions use positive y scale")


def profile_names(spec: Template) -> list[str]:
    template = next(name for name,item in TEMPLATES.items() if item == spec)
    return [name for name,profile in BANK_PROFILES.items() if profile.template == template]


def profile_eligible(name: str, p: dict) -> bool:
    a,b,h,k = p['a'],p['b'],p.get('h',0),p.get('k',0)
    if name in ('cos_tan_source','sin_tan_source'):
        return a > 0 and b > 0 and p.get('quadrant',1) == 1
    if name == 'sin_shift_exchange':
        return a != b and h != 0 and k != 0
    if name == 'sin_compound_scale_offset':
        return h != 0 and k != 0
    if name == 'sin_unit_y_shift':
        return a == b == 1 and h == 0 and k < 0
    if name == 'sin_unit_x_shift_identity':
        return a == b == 1 and h <= -2 and k == 0
    if name == 'cos_identity_scale':
        return a != b
    if name == 'cos_unit_shift_identity':
        return a == b == 1 and h < 0 and k >= 2
    if name == 'cos_double_positive_source':
        return a > 0 and b > 0
    if name == 'cos_double_negative_source':
        return a < 0 and b > 0
    if name == 'tan_sec_source':
        return a >= 2 and b == 1
    if name == 'cot_csc_source':
        return a >= 3 and b == 1
    if name == 'sin_double_factored_source':
        return a > 0 and b >= 2
    if name == 'sin_double_expanded_source':
        return a > 0 and b < 0
    return a > 0 and b > 0


def sample(spec: Template, rng: random.Random, profile: str | None = None) -> dict:
    f = spec.family
    if f.startswith("ellipse"):
        if spec.kind == "blank":
            return {"a":rng.randint(2,6),"b":1,"h":0,"k":rng.choice((-5,-4,-3,-2,-1,1,2,3,4,5))}
        if profile == 'sin_unit_y_shift':
            return {'a':1,'b':1,'h':0,'k':rng.randint(-5,-1)}
        if profile == 'sin_unit_x_shift_identity':
            return {'a':1,'b':1,'h':rng.randint(-5,-2),'k':0}
        if profile == 'cos_unit_shift_identity':
            return {'a':1,'b':1,'h':rng.randint(-5,-1),'k':rng.randint(2,5)}
        nonzero = (-5,-4,-3,-2,-1,1,2,3,4,5)
        shifted = profile in ('sin_shift_exchange','sin_compound_scale_offset')
        return {'a':rng.randint(1,5),'b':rng.randint(1,5),
                'h':rng.choice(nonzero) if shifted else rng.randint(-5,5),
                'k':rng.choice(nonzero) if shifted else rng.randint(-5,5)}
    if spec.level == "moderate":
        return {"a":rng.randint(1,4),"b":rng.randint(1,4),
                "quadrant":1 if BANK_PROFILES[profile].origin == 'observed' else rng.randint(1,4)}
    if spec.level == "easy":
        return {"a":rng.randint(3 if profile == 'cot_csc_source' else 2,6),"b":rng.randint(2,5) if spec.kind == "blank" else 1}
    a,b = rng.randint(2,6),rng.randint(2,6)
    if f == "sin_double_expanded":
        b = -b
    if f == "cos_double":
        a *= -1 if profile == 'cos_double_negative_source' else 1 if profile == 'cos_double_positive_source' else rng.choice((-1,1))
        if spec.kind == "blank":
            b *= rng.choice((-1,1))
    return {"a":a,"b":b}


def assemble(spec: Template, name: str, p: dict, built: Built, seed: int, profile: str | None) -> dict:
    points = verify(built)
    candidates: list[Wrong] = []
    if spec.kind == "radio":
        for recipe in BANK_PROFILES[profile].recipes:
            option = recipe.render(p,missing_function_sign(spec,p) if spec.level == 'moderate' else 1)
            relation = option.relation
            if not all(distinct(relation, old, points) for old in [built.relation] + [w.relation for w in candidates]):
                raise SampleRejected(f'{profile}/{option.recipe}: equivalent or duplicate option')
            if not any(sp.simplify((relation.lhs-relation.rhs).subs(point)).is_zero is False for point in points):
                raise SampleRejected(f'{profile}/{option.recipe}: no exact witness of incorrectness')
            candidates.append(option)
        if len(candidates) != 4:
            raise SampleRejected("Fewer than four distinct, incorrect source-shaped options")
    parameter_key = hashlib.sha256(json.dumps({"template":name,"parameters":p},sort_keys=True).encode()).hexdigest()
    content_key = hashlib.sha256(json.dumps({'parameters':parameter_key,'correct':built.relation.latex if spec.kind == 'radio' else built.blank_tex,
                                           'distractors':sorted(w.relation.latex for w in candidates)},sort_keys=True).encode()).hexdigest()
    question_id = uuid.uuid5(uuid.NAMESPACE_URL, f"course-academy/generated/{KP_UUID}/{VERSION}/{content_key}")
    key = "selection" if spec.kind == "radio" else "field-1"
    field_id = uuid.uuid5(question_id,key)
    answers, recipes = [], {}
    for label, relation in [("correct",built.relation)] + [(w.recipe,w.relation) for w in candidates]:
        value = relation.latex if spec.kind == "radio" else built.blank_tex or relation.rhs_tex
        identity = str(uuid.uuid5(field_id,"math:"+value))
        answers.append({":answer/id":identity,":answer/type":":answer.type/math",":answer/value":value})
        if label == "correct":
            correct_id = identity
        else:
            recipes[identity] = {"recipe":label,"lhs":sp.srepr(relation.lhs),"rhs":sp.srepr(relation.rhs)}
    if len({a[":answer/id"] for a in answers}) != len(answers):
        raise SampleRejected("Rendered options collide")
    random.Random(seed).shuffle(answers)
    interval = r"t\in[0,2\pi)" if built.period else quadrant_interval(built.quadrant)
    prompt = ("Find the Cartesian equation of the curve defined parametrically as" if spec.kind == "radio" else "Consider the curve defined parametrically as")
    prompt += "\n\n" + block("x="+function(p['a'],built.fx,p.get('h',0))+r",\qquad y="+function(p['b'],built.fy,p.get('k',0))+r",\qquad "+interval+".")
    if spec.kind == "blank":
        prompt += "\n\nThe Cartesian equation of this curve is\n\n" + ("{{field-1}}$=1.$" if spec.answer_shape == "lhs" else "$y=$\n{{field-1}}.")
    fragment = built.relation.lhs if spec.answer_shape == "lhs" else built.relation.rhs
    return {
        "knowledge_point":{"db_id":KP_ID,"id":KP_UUID,"title":TITLE},
        "question":{":question/id":str(question_id),":question/difficulty":":question.difficulty/"+spec.level,
                    ":question/problem":prompt,":question/worked-solution":built.solution,
                    ":question/answer-fields":[{":answer-field/id":str(field_id),":answer-field/key":key,
                        ":answer-field/type":":answer-field.type/"+spec.kind,":answer-field/choices":answers,
                        ":answer-field/correct":[":answer/id",correct_id]}]},
        "generation":{"version":VERSION,"sympy_version":sp.__version__,"seed":seed,"template":name,
                      "parameters":p,"parameter_fingerprint":parameter_key,"content_fingerprint":content_key,"answer_shape":spec.answer_shape,
                      "bank_profile":profile,
                      "bank_origin":BANK_PROFILES[profile].origin if profile else "observed",
                      "authored_extension":spec.level == 'moderate' and (
                          BANK_PROFILES[profile].origin == 'authored' or built.quadrant != 1 or not spec.sources),
                      "parameter_extension":spec.level == "moderate" and (p['a'],p['b']) != (1,1),
                      "source_analysis":{**SOURCE,"question_ids":([BANK_PROFILES[profile].source]
                          if profile and BANK_PROFILES[profile].source else list(spec.sources)),
                          "method_reference_ids":['q-102687','q-15759'] if spec.level == 'moderate' else list(spec.sources)},
                      "plot_rating":"none","plot_assets":{},"curve_restrictions_latex":built.restrictions,
                      "parameter_interval": "0 <= t < 2*pi" if built.period else
                          {1:'0 < t < pi/2',2:'pi/2 < t < pi',3:'pi < t < 3*pi/2',4:'3*pi/2 < t < 2*pi'}[built.quadrant],
                      "parametrization":{"x":sp.srepr(built.x_t),"y":sp.srepr(built.y_t)},
                      "answer_math":{"lhs":sp.srepr(built.relation.lhs),"rhs":sp.srepr(built.relation.rhs),"fragment":sp.srepr(fragment)},
                      "distractor_recipes":recipes},
    }


def generate(level: str, seed: int = 0, template: str | None = None, field_type: str | None = None,
             parameters: dict | None = None, profile: str | None = None) -> dict:
    if level == 'moderate' and parameters is not None:
        # An omitted quadrant means I; canonicalize it before content hashing.
        parameters = {"quadrant":1,**parameters}
    if profile is not None:
        if profile not in BANK_PROFILES:
            raise ValueError(f'Unknown bank profile: {profile}')
        if template is not None and BANK_PROFILES[profile].template != template:
            raise ValueError('Bank profile does not belong to this template')
        template = BANK_PROFILES[profile].template
    eligible = [name for name,spec in TEMPLATES.items() if spec.level == level and (field_type is None or spec.kind == field_type)]
    if not eligible or template is not None and template not in eligible:
        raise ValueError(f"Supported {level} templates: {', '.join(eligible)}")
    rng = random.Random(seed)
    name = template or rng.choice(eligible)
    spec = TEMPLATES[name]
    if spec.kind == 'radio':
        profiles = profile_names(spec)
        if spec.level == 'moderate' and profile is None:
            profiles = [item for item in profiles if BANK_PROFILES[item].origin == 'authored']
        if parameters is not None:
            validate_parameters(spec,parameters)
            profiles = [item for item in profiles if profile_eligible(item,parameters)]
            if profile is not None and profile not in profiles:
                raise ValueError('Explicit parameters violate the bank profile conditions')
            if not profiles:
                raise SampleRejected('No eligible source bank profile for these parameters')
            # Fixed parameters keep their default bank across seed/order changes.
            stable_rng = random.Random(json.dumps(parameters,sort_keys=True))
            profile = profile or stable_rng.choice(profiles)
        else:
            profile = profile or rng.choice(profiles)
    for _ in range(64):
        p = dict(parameters) if parameters is not None else sample(spec,rng,profile)
        validate_parameters(spec,p)
        if profile and not profile_eligible(profile,p):
            continue
        built = BUILDERS[level](spec,p)
        try:
            return assemble(spec,name,p,built,seed,profile)
        except SampleRejected:
            if parameters is not None:
                raise
    raise SampleRejected("Bounded sampling did not produce an unambiguous question")


# ============================================================================
# EASY — seven extracted field/value templates using same-angle identities
# ============================================================================
def build_easy(spec: Template, p: dict) -> Built:
    """Isolate trig functions; substitute into a single Pythagorean identity.

    Sine/cosine radios retain normalized squares, sine-first substitution, and
    the source closing sentence. Their blanks show coefficient-form equivalence
    and omit that closing sentence as the originals do. Hyperbola radios derive
    their identity by division; cot/csc blanks use it directly, justify positive
    functions, and solve for the positive root. Correct-answer shape is part of
    each extracted template, not a generic conversion of a radio question.
    """
    a,b,h,k = p['a'],p['b'],p.get('h',0),p.get('k',0)
    if spec.family.startswith("ellipse"):
        sin_x = spec.family == "ellipse_sin"
        fx,fy = ("sin","cos") if sin_x else ("cos","sin")
        correct = ellipse(p,sin_x)
        solution = opening(p,fx,fy)+"\n\nUsing the Pythagorean identity $"+PYTHAGOREAN+"$, we get\n\n"
        blank = coefficient_term(sp.Rational(1,a*a),"x^2") + "+" + square(tex(Y-k))
        if spec.kind == "blank":
            solution += aligned([(correct.lhs_tex,"=1"),(blank,"=1.")])
        else:
            solution += block(correct.latex+".")+ending(correct)
        return Built(a*getattr(sp,fx)(T)+h,b*getattr(sp,fy)(T)+k,fx,fy,correct,solution,True,
                     f"{h-a}\\le x\\le {h+a},\\quad {k-b}\\le y\\le {k+b}",blank)
    fx,fy = ("tan","sec") if spec.family == "tan_sec" else ("cot","csc")
    square_x = square(ratio(X,a))
    inside = 1+X**2/a**2
    inside_tex = square_x+"+1" if fx == "tan" else "1+"+square_x
    correct = Relation(Y**2,inside,"y^2",inside_tex)
    solution = opening(p,fx,fy)
    if spec.kind == "radio":
        divisor = r"\cos" if fx == "tan" else r"\sin"
        solution += "\n\nDividing the Pythagorean identity $"+PYTHAGOREAN+"$ by $"+divisor+"^2 t$, we get\n\n"
        quotient = r"\left(\frac{\sin t}{\cos t}\right)^2+1" if fx == "tan" else r"1+\left(\frac{\cos t}{\sin t}\right)^2"
        identity = r"\tan^2 t+1" if fx == "tan" else r"1+\cot^2 t"
        solution += aligned([(r"\frac{\sin^2 t}{"+divisor+"^2 t}+\\frac{\\cos^2 t}{"+divisor+"^2 t}",r"=\frac{1}{"+divisor+"^2 t}"),
                             (quotient,r"=\left(\frac{1}{"+divisor+r" t}\right)^2"),
                             (identity,"=\\"+fy+"^2 t.")])
        solution += "\n\n"+substitution(p,fx,fy)+"\n\n"+block(inside_tex+"=y^2.")+ending(correct)
        blank = None
    else:
        value = b*sp.sqrt(inside)
        blank = str(b)+r"\sqrt{1+\frac{x^2}{"+str(a*a)+"}}"
        correct = explicit(value,blank)
        solution += "\n\nUsing the Pythagorean identity $\\csc^2 t=1+\\cot^2 t$, we get\n\n"
        solution += aligned([(r"\csc^2 t",r"=1+\cot^2 t"),
                             (r"\frac{y^2}{"+str(b*b)+"}",r"=1+\frac{x^2}{"+str(a*a)+"}.")])
        solution += "\n\nWe used here that $\\csc t>0$ and $\\cot t>0$ in the range $0<t<\\frac{\\pi}{2}.$"
        solution += "\n\nNow, solving for $y$, we obtain\n\n"+block(correct.latex+".")+ending(correct,True)
    return Built(a*getattr(sp,fx)(T),b*getattr(sp,fy)(T),fx,fy,correct,solution,False,
                 f"x>0,\\quad y>{b}",blank)


def generate_easy(seed: int = 0, template: str | None = None,
                  field_type: str | None = None, parameters: dict | None = None,
                  profile: str | None = None) -> dict:
    """Generate one of the seven easy source field/value templates."""
    return generate("easy",seed,template,field_type,parameters,profile=profile)


# ============================================================================
# MODERATE — four equivalent radio families; scales and quadrants are variations
# ============================================================================
def build_moderate(spec: Template, p: dict) -> Built:
    """Recover sine/cosine, select its sign, then use tan or cot as a quotient.

    All four families use the same source-style solution stages and positive
    integer scales 1..4. Each interval stays inside one open quadrant, so exactly
    one root branch applies. Families and quadrants have no instructional order.
    Authored banks derive four specific mistakes from this calculation; the two
    observed banks remain available for exact source replay in quadrant I.
    """
    a,b,q = p['a'],p['b'],p.get('quadrant',1)
    fx,fy = spec.family.split('_')
    missing = 'sin' if fx == 'cos' else 'cos'
    sign = missing_function_sign(spec,p)
    prefix = '' if sign == 1 else '-'
    root_denominator = spec.family in ('sin_tan','cos_cot')
    value = b*sign*X/sp.sqrt(a*a-X**2) if root_denominator else b*sign*sp.sqrt(a*a-X**2)/X
    correct = explicit(value)
    solution = opening(p,fx,fy)+"\n\nUsing the Pythagorean identity $"+PYTHAGOREAN+"$, we get\n\n"
    missing_root = prefix+r'\sqrt{1-'+trig(fx).replace(' t','^2 t')+'}'
    solution += aligned([(PYTHAGOREAN.rsplit('=',1)[0],"=1"),
                         ("\\"+missing+"^2 t","=1-\\"+fx+"^2 t"),
                         (trig(missing),"="+missing_root+".")])
    solution += f"\n\nWe used here that ${trig(missing)}{'>' if sign == 1 else '<'}0$ in the range ${quadrant_interval(q)}.$"
    sin_value = trig('sin') if fx == 'sin' else missing_root
    cos_value = trig('cos') if fx == 'cos' else missing_root
    numerator,denominator = (sin_value,cos_value) if fy == 'tan' else (cos_value,sin_value)
    identity = r'\frac{\sin t}{\cos t}' if fy == 'tan' else r'\frac{\cos t}{\sin t}'
    definition = 'a tangent' if fy == 'tan' else 'a cotangent'
    solution += "\n\nNow, using the definition of "+definition+", we obtain\n\n"+block(trig(fy)+"="+identity+r"=\frac{"+numerator+"}{"+denominator+"}.")
    solution += "\n\n"+substitution(p,fx,fy)+"\n\n"
    if (a,b) == (1,1):
        solution += block(correct.latex+".")
    else:
        radical = prefix+r"\sqrt{1-"+square(ratio(X,a))+"}"
        numerator,denominator = (ratio(X,a),radical) if root_denominator else (radical,ratio(X,a))
        solution += aligned([(ratio(Y,b),r"=\frac{"+numerator+"}{"+denominator+"}"),("y","="+correct.rhs_tex+".")])
    solution += ending(correct)
    sine_sign,cosine_sign = QUADRANTS[q]
    x_sign = cosine_sign if fx == 'cos' else sine_sign
    domain = f'0<x<{a}' if x_sign == 1 else f'-{a}<x<0'
    restrictions = domain+r'\quad '+('y>0' if sine_sign*cosine_sign == 1 else 'y<0')
    return Built(a*getattr(sp,fx)(T),b*getattr(sp,fy)(T),fx,fy,correct,solution,
                 False,restrictions,quadrant=q)


def generate_moderate(seed: int = 0, template: str | None = None,
                      field_type: str | None = None, parameters: dict | None = None,
                      profile: str | None = None) -> dict:
    """Generate equal-level tan/cot, coefficient, and single-quadrant variations."""
    return generate("moderate",seed,template,field_type,parameters,profile)


# ============================================================================
# HARD — four field/value templates using cos(2t), including expanded radio form
# ============================================================================
def build_hard(spec: Template, p: dict) -> Built:
    """Derive the appropriate double-angle form, substitute, and isolate y.

    Positive sine/y scales retain the factored source answer. Negative sine/y
    scales retain the constant-first expanded radio answer. Cosine radios retain
    factored answers and signed x scales; cosine blanks expand their RHS after
    the same intermediate factored step. Signed cosine examples omit the extra
    unsimplified-square row, as observed; this layout condition is inferred.
    All fractions use exact squared scales.
    """
    a,b = p['a'],p['b']
    sine = spec.family.startswith("sin_double")
    fx = "sin" if sine else "cos"
    inside = 1-2*X**2/a**2 if sine else 2*X**2/a**2-1
    value = sp.expand(b*inside)
    reduced = coefficient_term(sp.Rational(2,a*a),"x^2")
    inside_tex = "1-"+reduced if sine else reduced+"-1"
    factored = str(b)+r"\left("+inside_tex+r"\right)"
    constant_first = str(b)+"+"+coefficient_term(sp.Rational(-2*b,a*a),"x^2")
    display = tex(value) if spec.kind == "blank" else constant_first if spec.family == "sin_double_expanded" else factored
    correct = explicit(value,display)
    solution = opening(p,fx,"cos2")
    sentence = "Now, using the double-angle formula for cosine and the Pythagorean identity, we obtain" if spec.kind == "blank" else "Now, using double angle formula for cosine and the Pythagorean identity, we obtain"
    solution += "\n\n"+sentence+"\n\n"+aligned([
        (r"\cos 2t",r"=\cos^2 t-\sin^2 t"),
        ("",r"=(1-\sin^2 t)-\sin^2 t" if sine else r"=\cos^2 t-(1-\cos^2 t)"),
        ("",r"=1-2\sin^2 t." if sine else r"=2\cos^2 t-1."),
    ])
    solution += "\n\n"+substitution(p,fx,"cos2")+"\n\n"
    squared_ratio = square(ratio(X,a))
    unsimplified = r"\frac{x^2}{"+str(a*a)+"}"
    first = "1-2"+squared_ratio if sine else "2"+squared_ratio+"-1"
    second = "1-2\\left("+unsimplified+r"\right)" if sine else "2\\left("+unsimplified+r"\right)-1"
    rows = [(ratio(Y,b),"="+first)]
    if sine or (a > 0 and b > 0):
        rows.append((ratio(Y,b),"="+second))
    rows += [(ratio(Y,b),"="+inside_tex),
             ("y","="+(constant_first if spec.family == "sin_double_expanded" else factored))]
    if spec.kind == "blank":
        rows.append(("y","="+tex(value)+"."))
    solution += aligned(rows)+ending(correct,spec.kind == "blank")
    return Built(a*getattr(sp,fx)(T),b*sp.cos(2*T),fx,"cos2",correct,solution,True,
                 f"{-abs(a)}\\le x\\le {abs(a)}",tex(value) if spec.kind == "blank" else None)


def generate_hard(seed: int = 0, template: str | None = None,
                  field_type: str | None = None, parameters: dict | None = None,
                  profile: str | None = None) -> dict:
    """Generate a hard factored radio, expanded radio, or expanded RHS blank."""
    return generate("hard",seed,template,field_type,parameters,profile=profile)


BUILDERS = {"easy":build_easy,"moderate":build_moderate,"hard":build_hard}
GENERATORS = {"easy":generate_easy,"moderate":generate_moderate,"hard":generate_hard}


def markdown(record: dict) -> str:
    q,g = record['question'],record['generation']
    f = q[':question/answer-fields'][0]
    lines = ["## Generated — "+q[':question/difficulty'].split('/')[-1].title(),
             f"Template: `{g['template']}`; seed: `{g['seed']}`.",""]
    if g['bank_profile']:
        bank = BANK_PROFILES[g['bank_profile']]
        evidence = f'source: `{bank.source}`' if bank.origin == 'observed' else 'authored variation; method adapted from the two moderate sources'
        lines += [f"Bank profile: `{g['bank_profile']}`; {evidence}.",'']
    if g['parameter_extension']:
        lines += ["*Coefficients vary from the unit-coefficient moderate sources.*",""]
    lines += [q[':question/problem'],""]
    if f[':answer-field/type'].endswith('/radio'):
        for letter,answer in zip("ABCDE",f[':answer-field/choices'],strict=True):
            lines.append(f"- **{letter}.** ${answer[':answer/value']}$")
        letter = next(letter for letter,answer in zip("ABCDE",f[':answer-field/choices'],strict=True) if answer[':answer/id'] == f[':answer-field/correct'][1])
        lines += ["",f"**Correct: {letter}**"]
    else:
        lines += ["**Correct blank entry:** $"+f[':answer-field/choices'][0][':answer/value']+"$"]
    lines += ["","**Worked solution**","",q[':question/worked-solution'],"",
              "**Author metadata — curve restrictions:** $"+g['curve_restrictions_latex']+"$."]
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--difficulty',choices=('all',*GENERATORS),default='all')
    parser.add_argument('--template',choices=tuple(TEMPLATES))
    parser.add_argument('--field-type',choices=('radio','blank'))
    parser.add_argument('--profile',choices=tuple(BANK_PROFILES),help='Select one complete observed or authored bank; implies its template')
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=('markdown','json'),default='markdown')
    args = parser.parse_args()
    if args.count < 1 or (args.template or args.profile) and args.difficulty == 'all':
        parser.error('Use a positive --count and a specific difficulty with --template')
    levels = list(GENERATORS) if args.difficulty == 'all' else [args.difficulty]
    try:
        records = [generate(level,args.seed+i,args.template,args.field_type,None,args.profile)
                   for level in levels for i in range(args.count)]
    except ValueError as exc:
        parser.error(str(exc))
    if args.format == 'json':
        print(json.dumps(records,indent=2,ensure_ascii=False))
    else:
        print('# Cartesian-equation generator review\n\nAuthor preview; answers and solutions are included.\n')
        print('\n\n---\n\n'.join(markdown(record) for record in records))


if __name__ == '__main__':
    main()

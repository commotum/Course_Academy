"""Focused publication regressions for thirteen audited trigonometry KPs.

Inspect visible independent-practice prompts and choices, never generator claims.
This is a guard for demonstrated failures, not a mathematical grader or a general
pedagogical classifier. Source-supported numerical angle-split hints remain valid.
"""
from fractions import Fraction
import re

from scripts.question_capture.math_format import MATH, normalize_function_operators
from scripts.question_capture.math_notation import Parser, tokens

KPS = frozenset({17592186059665, 17592186059666, 17592186059821,
                 17592186059662, 17592186059663, 17592186059820,
                 17592186059671, 17592186059672, 17592186059673,
                 17592186059674, 17592186087669, 17592186087670,
                 17592186087671})
SHIFT_KPS = frozenset({17592186059665, 17592186059821,
                       17592186059662, 17592186059820})
EXACT_SUM_KPS = frozenset({17592186059666, 17592186059663})
SINGLE_DOUBLE_KPS = frozenset({17592186059671, 17592186087669, 17592186087670})
COSINE_DOUBLE_KPS = frozenset({17592186087669, 17592186087670, 17592186087671})
TRIG = frozenset({'sin', 'cos', 'tan', 'cot', 'sec', 'csc'})


def _children(node):
    if node[0] == 'fence': return [node[2]]
    if node[0] == 'group': return [node[1]]
    if node[0] in ('frac', 'root'): return list(node[1:])
    if node[0] == 'script': return [(node[1],), node[2], node[3]]
    return []


def _walk(sequence):
    for node in sequence:
        yield node
        for child in _children(node): yield from _walk(child)


def _operator(node):
    if node[0] == 'script': return _operator(node[1])
    return node[1] if node[0] == 'operator' else None


def _calls(sequence):
    """Named functions with a fenced/grouped or single-token argument."""
    for index, node in enumerate(sequence):
        if _operator(node) in TRIG and index+1 < len(sequence):
            argument = sequence[index+1]
            yield node, (argument[2] if argument[0] == 'fence' else
                         argument[1] if argument[0] == 'group' else (argument,))
        for child in _children(node): yield from _calls(child)


def _parse(tex):
    tex = re.sub(r'\\(?:begin|end)\{(?:aligned|gathered)\}', '', tex)
    tex = tex.replace('&', '').replace(r'\\', '').replace('⁡', '')
    return Parser(tokens(normalize_function_operators(tex))).sequence()


def _has_variable(sequence):
    return any((n[0] == 'char' and re.fullmatch(r'[A-Za-z]', n[1])) or
               (n[0] == 'command' and n[1] in ('theta', 'alpha', 'beta', 't', 'x'))
               for n in _walk(sequence))


def _constant(sequence):
    """Exact a+b*pi for the rational numerical angles used in these KPs.

    Unsupported expressions return None; they are not guessed or rejected.
    """
    def add(a, b): return a[0]+b[0], a[1]+b[1]
    def mul(a, b):
        if a[1] and b[1]: raise ValueError('nonlinear pi')
        return a[0]*b[0], a[0]*b[1]+a[1]*b[0]
    def atom(node):
        kind = node[0]
        if kind == 'char': return Fraction(node[1]), Fraction(0)
        if node == ('command', 'pi'): return Fraction(0), Fraction(1)
        if kind in ('group', 'fence'): return evaluate(node[1] if kind == 'group' else node[2])
        if kind == 'frac':
            top, bottom = evaluate(node[1]), evaluate(node[2])
            if bottom[1] or not bottom[0]: raise ValueError('nonrational denominator')
            return top[0]/bottom[0], top[1]/bottom[0]
        if kind == 'script' and node[3] in ((('command', 'circ'),), (('char', '°'),), (('char', '∘'),)):
            value = atom(node[1])
            if value[1]: raise ValueError('degrees of pi')
            return Fraction(0), value[0]/180
        raise ValueError('unsupported angle')
    def evaluate(parts):
        total, term, sign, divide = (Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)), 1, False
        pending = False
        for node in parts:
            if node in (('char', '+'), ('char', '-')):
                if pending:
                    total = add(total, (sign*term[0], sign*term[1])); term = (Fraction(1), Fraction(0)); pending = False
                    sign = 1
                if node == ('char', '-'): sign *= -1
            elif node in (('command', 'cdot'), ('command', 'times')): pass
            elif node in (('char', '/'), ('command', 'div')): divide = True
            else:
                value = atom(node)
                if divide:
                    if value[1] or not value[0]: raise ValueError('nonrational divisor')
                    value = (1/value[0], Fraction(0)); divide = False
                term = mul(term, value); pending = True
        if not pending: raise ValueError('empty angle')
        return add(total, (sign*term[0], sign*term[1]))
    try: return evaluate(sequence)
    except (ValueError, ZeroDivisionError, TypeError): return None


def _phase(argument):
    """Read only additive numerical terms in a symbolic shifted argument."""
    while len(argument) == 1 and argument[0][0] in ('group', 'fence'):
        argument = argument[0][1] if argument[0][0] == 'group' else argument[0][2]
    terms, current, sign = [], [], 1
    for node in argument:
        if node in (('char', '+'), ('char', '-')):
            if current: terms.append((sign, tuple(current))); current = []; sign = 1
            if node == ('char', '-'): sign *= -1
        else: current.append(node)
    if current: terms.append((sign, tuple(current)))
    phase = (Fraction(0), Fraction(0))
    for sign, term in terms:
        if _has_variable(term): continue
        value = _constant(term)
        if value is None: return None
        phase = (phase[0]+sign*value[0], phase[1]+sign*value[1])
    return phase


def _unit_product(sequence):
    for index, node in enumerate(sequence):
        one = _constant((node,)) == (Fraction(1), Fraction(0))
        # A literal 1 serving as an actual function argument is an angle,
        # not the scalar coefficient of the following function.
        if one and index and _operator(sequence[index-1]) in TRIG:
            one = False
        if one:
            following = sequence[index+1] if index+1 < len(sequence) else None
            previous = sequence[index-1] if index else None
            if following and (following in (('command', 'cdot'), ('command', 'times')) or
                              _operator(following) in TRIG or following[0] in ('fence', 'group', 'root', 'frac') or
                              following[0] == 'char' and re.fullmatch(r'[A-Za-z]', following[1])):
                return True
            if previous and (previous in (('command', 'cdot'), ('command', 'times')) or previous[0] in ('fence', 'group')):
                return True
        if any(_unit_product(child) for child in _children(node)): return True
    return False


def validate_delivery_batch(records, kp_id):
    """Raise ValueError on a known instructional regression; unrelated KPs pass."""
    kp_id = int(kp_id)
    if kp_id not in KPS: return
    for record in records:
        question = record['question']
        prompt = question.get(':question/problem', '')
        # An angle-split hint supplies numerical representation, not the trig
        # formula. Do not ban the words 'hint', 'use', or 'fact' by themselves.
        if re.search(r'\b(?:use|using|apply|recall|remember)\b[^.!?\n]{0,120}'
                     r'\b(?:formula|identity|identities|twice (?:the )?angle)\b', prompt, re.I) or re.search(
                     r'\b(?:and|use|using)\s+(?:the\s+)?(?:exact\s+)?values\b', prompt, re.I):
            raise ValueError('Trigonometry practice must leave formula recall and method selection to the learner')
        spans = [m[0].strip('$').strip() for m in MATH.finditer(prompt)]
        expressions = [_parse(span) for span in spans]
        for span, expression in zip(spans, expressions):
            if _unit_product(expression):
                raise ValueError('Trigonometry prompt/choices must omit literal unit multiplication')
            # A repeated target followed by an empty equals sign is a response
            # frame. A supplied trigonometric equality with an actual RHS is help.
            if '=' in span and list(_calls(expression)):
                rhs = span.split('=', 1)[1]
                rhs = re.sub(r'\\(?:begin|end)\{(?:aligned|gathered)\}', '', rhs).replace('&', '').strip().rstrip('.,')
                if rhs and not re.fullmatch(r'\{\{[^{}]+\}\}', rhs):
                    raise ValueError('Trigonometry practice must not supply a formula or substituted trigonometric equality')
        for field in question.get(':question/answer-fields', []):
            for answer in field.get(':answer-field/choices', []):
                value = answer.get(':answer/value', '')
                kind = answer.get(':answer/type')
                if isinstance(kind, dict): kind = kind.get(':db/ident')
                choices = [value] if kind == ':answer.type/math' else [m[0].strip('$') for m in MATH.finditer(value)]
                if any(_unit_product(_parse(choice)) for choice in choices):
                    raise ValueError('Trigonometry prompt/choices must omit literal unit multiplication')
        # Inspect the first actual trig expression, excluding later answer frames
        # and supplied numerical angle decomposition hints.
        main = next((expr for expr in expressions if list(_calls(expr))), ())
        calls = list(_calls(main))
        if kp_id == 17592186059672 and not any(_operator(node) == 'csc' for node, _ in calls):
            # In a linked product/reciprocal triple, evaluating a familiar
            # intermediate angle bypasses the second double-angle application.
            numerical = [(_operator(node), _constant(arg)) for node, arg in calls]
            for fn, mid in numerical:
                if fn not in ('cos', 'sec') or mid is None or mid[0] != 0: continue
                half = (mid[0]/2, mid[1]/2)
                if ('sin', half) not in numerical or ('cos', half) not in numerical: continue
                if (mid[1]*6).denominator == 1 or (mid[1]*4).denominator == 1:
                    raise ValueError('Repeated double-angle practice must not allow standard intermediate-angle evaluation to bypass the second application')
        if kp_id in SHIFT_KPS:
            symbolic = [(node, arg) for node, arg in calls if _has_variable(arg)]
            if len(symbolic) > 1:
                raise ValueError('Symbolic shift practice requires one shifted ratio, not a two-expansion wrapper')
            for _, argument in symbolic:
                phase = _phase(argument)
                if phase is not None and phase[0] == 0 and phase[1] % 2 == 0:
                    raise ValueError('Symbolic shift practice must avoid zero/full-turn shifts')
        if kp_id in EXACT_SUM_KPS and len(calls) > 1:
            raise ValueError('Exact sum/difference practice requires a forward single-ratio evaluation, not reverse product recognition')
        if kp_id in SINGLE_DOUBLE_KPS:
            for node in _walk(main):
                if node[0] == 'script' and _operator(node) in TRIG:
                    power = _constant(node[3])
                    if power is not None and power[1] == 0 and power[0] >= (3 if kp_id == 17592186059671 else 4):
                        raise ValueError('This double-angle KP has no source-backed quartic task')
        if kp_id in COSINE_DOUBLE_KPS:
            for _, argument in calls:
                angle = _constant(argument)
                if angle is not None and angle[0] == 0 and ((6*angle[1]).denominator == 1 or (4*angle[1]).denominator == 1):
                    raise ValueError('Original standard-angle values bypass the cosine double-angle recognition task')

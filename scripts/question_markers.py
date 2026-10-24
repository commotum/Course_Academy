"""The prompt only embeds controls for blank and select answer fields.

Radio, checkbox and free-response controls are rendered separately. Their
widget tokens must not be present in the Markdown problem statement.
"""
import re

MARKER = re.compile(r'\{\{(?:answer-field:)?([^{}]+)\}\}')
SEPARATE = {'radio', 'checkbox', 'free'}
RESPONSE_LABEL = re.compile(
    r'(?:Written response|Your response|Your selections?|List all applicable choices):\s*',
    re.IGNORECASE,
)


def misplaced_markers(problem, fields):
    kinds = {}
    for field in fields:
        kind = field[':answer-field/type']
        if isinstance(kind, dict):
            kind = kind[':db/ident']
        kinds[field[':answer-field/key']] = str(kind).rsplit('/', 1)[-1]
    return [match for match in MARKER.finditer(problem)
            if kinds.get(match[1]) in SEPARATE]


def repair_problem(problem, fields):
    """Remove redundant widget paragraphs, preserving embedded unknowns as ?.

    Only tokens bound to separately rendered fields are eligible. In particular,
    TeX double groups, unbound text, and blank/select controls are untouched.
    """
    matches = misplaced_markers(problem, fields)
    if not matches:
        return problem
    for match in reversed(matches):
        start = problem.rfind('\n\n', 0, match.start()) + 2
        if start == 1:
            start = 0
        end = problem.find('\n\n', match.end())
        if end < 0:
            end = len(problem)
        prefix, suffix = problem[start:match.start()], problem[match.end():end]
        if (not prefix.strip() or RESPONSE_LABEL.fullmatch(prefix.strip())) and not suffix.strip():
            # The whole paragraph only instructed the player to place a widget.
            problem = problem[:max(0, start - 2)] + problem[end:]
        else:
            # An unknown inside a formula remains an unknown, without a widget.
            problem = problem[:match.start()] + '?' + problem[match.end():]
    return problem.rstrip()


def validate_prompt_markers(question):
    bad = misplaced_markers(question[':question/problem'], question[':question/answer-fields'])
    if bad:
        raise ValueError('Only blank/select fields may have prompt markers: ' +
                         ', '.join(match[1] for match in bad))

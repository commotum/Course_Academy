"""Proposed common-normalizer patch; keep visible bracketed operands after aligned."""
import re

def protect_aligned_prefix(value):
    # [t], [b], [c] are genuine MathJax positioning options. Any other initial
    # bracket is visible mathematical content, e.g. the label [A | I].
    return re.sub(r'(\\begin\{aligned\})(?=\s*\[(?!\s*[tbc]\s*\]))',
                  lambda match: match[1] + '{}', str(value))


def test_protect_aligned_prefix():
    samples = [r'\begin{aligned}[A\,|\,I] &= M\end{aligned}',
               r'\begin{aligned} [B\mid b] &= M\end{aligned}']
    for value in samples:
        guarded = protect_aligned_prefix(value)
        assert r'\begin{aligned}{}' in guarded
        assert protect_aligned_prefix(guarded) == guarded
    for option in ['t', 'b', 'c']:
        value = r'\begin{aligned}[' + option + r']x&=1\end{aligned}'
        assert protect_aligned_prefix(value) == value
    assert protect_aligned_prefix(r'\begin{aligned}\left[A\mid I\right]&=M\end{aligned}') == r'\begin{aligned}\left[A\mid I\right]&=M\end{aligned}'

if __name__ == '__main__':
    test_protect_aligned_prefix()
    print('Visible-prefix, position-option, and idempotence regressions pass.')

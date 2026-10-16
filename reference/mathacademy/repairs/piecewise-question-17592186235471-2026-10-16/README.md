# Piecewise question formatting repair

Question `17592186235471` (`q-167694`) inherited its function definition from multistep `17592186235292`.

The imported setup used `f(x)={\begin{aligned}...\end{aligned}`, with an unmatched opening brace and no proper piecewise delimiter. Replaced this with a balanced `cases` environment, preserving all three expressions and domain conditions. The shared setup repair also applies wherever the same multistep is displayed.

The question problem contained a deeply indented answer placeholder surrounded by whitespace-only lines. Markdown interpreted the generated field slot as an indented code block, escaping its HTML instead of mounting an input. Replaced that whitespace with a normal inline question and the same `{{field-1}}` marker. Intentional Markdown code blocks retain their existing behavior; no renderer changes were necessary.

The native EDB preview passed before committing. Compare-and-swap forms changed only `multistep/context` and `question/problem` at basis 2962. Exact readback confirmed that all other attributes on both entities, including answer fields and the worked solution, were unchanged. Receipt datoms contain no learner activity modifications.

`check-dom.cjs` reproduces the original accidental code block and checks the repair with the actual app Markdown, MathJax, MathLive, and CSS assets. Nine repaired configurations passed (893/375/320 pixels × edit/correct/incorrect): one three-row piecewise display, no raw math delimiters or HTML, no code block, one field, and no horizontal overflow. The edit state mounts that field inline. No screenshots or image inspection were used.

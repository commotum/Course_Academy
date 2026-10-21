"""Summarize the read-only source and browser audit with exact entity references."""
import collections,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
 inv=json.loads((HERE/'inventory.json').read_text());findings=json.loads((HERE/'source-findings.json').read_text());entities=json.loads((HERE/'entities.json').read_text())
 additional=json.loads((HERE/'additional-source-review.json').read_text());signs=json.loads((HERE/'confirmed-sign-typos.json').read_text());browser=json.loads((HERE/'browser-summary.json').read_text())
 scopes={v['topic']:v for v in inv['lessons']};members={v['topic']:set(v['entities'])for v in inv['lessons']}
 operator_attrs=sorted({(v['entity'],v['attribute'])for v in additional['plain_operators']})
 bold=additional['malformed_bold']
 assert browser['cases']==318 and browser['records']==1272 and not any(browser[k]for k in ['errors','exceptions','mathErrors','overflow'])
 table_findings=[v for v in findings if v['code']=='markdown_table_review']
 assert len(table_findings)==21
 # Every flagged table has genuine x/u headings and three columns, rather than
 # the one-column fraction fragments found in some older captured lessons.
 for f in table_findings:
  rows=[line for line in entities[str(f['entity'])][f['attribute']].splitlines()if line.strip().startswith('|')]
  assert len(rows)==3 and all(line.count('|')==4 for line in rows)
  assert rows[0].startswith('| $x$ |')and rows[2].startswith('| $u$ |')

 def local_flags(topic):
  fs=[v for v in findings if topic in v['lessons']];c=collections.Counter(v['code']for v in fs);out=[]
  if c['literal_brace']:out.append(f"{c['literal_brace']} misplaced-underbrace solutions")
  if c['trailing_equals']:out.append(f"{c['trailing_equals']} content items with trailing equals signs")
  if c['legacy_command']:out.append(f"{c['legacy_command']} examples with visible row-spacing commands")
  if c['missing_separation']:out.append(f"{c['missing_separation']} prompts missing prose/equation separation")
  count=sum(e in members[topic]for e,a in operator_attrs)
  if count:out.append(f'{count} attributes with unformatted function names')
  if any(v['entity']in members[topic]for v in bold):out.append('broken bold in tutorial')
  count=sum(v['entity']in members[topic]for v in signs)
  if count:out.append(f'{count} confirmed sign typos')
  return '; '.join(out)or'No substantive formatting defect identified in these checks'
 r=['# Other Completing the Square lessons: LaTeX and Markdown audit','',
'Database: `math`. Lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Snapshot: **basis 3529**.',
'',
'No EDB transactions or content changes were made. This audit covers the ten other topic titles containing “Completing the Square”; it excludes the base lesson already repaired at basis 3520.',
'','## Coverage','',
'- 10 lesson activities; all 43 linked lesson steps; 31 knowledge points.',
'- All 12 tutorials, 31 canonical examples, 275 practice questions, and 273 available worked solutions.',
'- All 315 answer fields and 1,262 distinct answer values (1,009 math and 253 text). No answer feedback is stored on these entries.',
'- All lesson routes are connected and acyclic. No unmatched math delimiters, unbalanced TeX braces/environments, orphan field placeholders, raw rendered answer placeholders, or unexpected Markdown code blocks were found.',
'- The browser rendered all 318 items at desktop (893 px) and mobile (375 px) widths, in editable and answered states: 1,272 item renders and 4,250 math containers in desktop editable mode.',
'- No browser exceptions, MathJax error nodes, or outer card/prompt horizontal overflow were reported. Those checks do not detect the visible legacy-command and notation defects below. Long mathematical lines can still require internal scrolling.',
'- Source and geometry checks covered every item. Representative anomalies were visually inspected; the screenshots omit image elements. All three referenced diagram assets resolve in the local image library. This is a formatting audit with two incidental algebra findings, not a complete independent answer-key or mathematical audit.',
'','## Findings by lesson','',
'| Lesson | Practice questions | Findings | Missing solutions | Questions missing keys |','| --- | ---: | --- | ---: | ---: |']
 for v in inv['lessons']:
  c=collections.Counter(f['code']for f in findings if v['topic']in f['lessons'])
  r.append(f"| {v['title']} | {v['practice']} | {local_flags(v['topic'])} | {c['missing_solution']} | {c['missing_key']} |")
 r+=['','## Confirmed formatting defects','',
'### Misplaced underbraces: 63 practice solutions','',
'10 are in **Completing the Square With Odd Linear Terms**, and 53 are in **Completing the Square With Leading Coefficients**. They store `..._{⏟}` where a spanning `\\underbrace{...}` is intended. Canonical examples in these lessons already use proper underbraces.',
'','### Broken legacy equation rows: four canonical examples, five display blocks','',
'Examples `17592186068504`, `17592186068506`, `17592186166644`, and `17592186166647` use legacy `\\eqalign{...}` blocks containing single-backslash `\\[3pt]` or `\\[5pt]` row separators. These visibly render the commands instead of producing line breaks; entire derivations run across one row. Example `17592186068506` has two affected blocks. Replace the affected environments with standard `aligned` and proper `\\\\` row breaks during a repair.',
'',
'The visible failure was confirmed in [two ordinary integration examples](sample-0.png) and [two inverse reciprocal hyperbolic integration examples](sample-1.png). These are real display failures even though MathJax reports no error nodes.',
'','### Trailing equals alignment: eight content entities','',
'Both odd-linear-term tutorials, one canonical example, and five practice solutions use the same end-of-row equals-sign layout as the base lesson did. There are 15 aligned environments across those eight entities, including one harmless single-row wrapper; 14 environments contain the trailing-equals pattern. [Rendered tutorials](sample-2.png) show the result. Use conventional equation chains with the equals signs before each new expression.',
'','### Unformatted named functions: 38 attributes','',
'43 occurrences across 38 attributes use bare `arsinh`, `arcosh`, `artanh`, `arcsin`, or `arctan` in math. They render as products of italic letters, rather than named operators. The affected attributes comprise one tutorial, six worked solutions, and 31 answer values. Standard TeX commands or `\\operatorname{...}` would express the intended notation. This is visible in the [hyperbolic integration tutorial](sample-3.png), which also retains awkward slash-form fractions such as `\\int(1)/(...)dx`.',
'','### Broken Markdown emphasis: one tutorial','',
'Circle tutorial `17592186079635` contains `**Step 1. **Group...`; the space before the closing marker prevents bold formatting and leaves raw asterisks visible. It should read `**Step 1.** Group...`. See the [rendered circle tutorial](sample-3.png).',
'','### Missing prose/equation separation: three prompts','',
'Questions `17592186184553`, `17592186184554`, and `17592186184555` run the instructions directly into the answer equation. All three belong to the odd-linear-term lesson. A paragraph break before the equation would match the other prompts.',
'','## Two confirmed sign typos encountered during review','',
'These go beyond formatting and should be reviewed as mathematical content repairs:',
'']
 for v in signs:r += [f"- **`{v['entity']}`**, `{v['attribute']}`: {v['description']}"]
 r+=['',
'Both are in **Integrating Functions by Completing the Square**. The polynomial differences between the incorrect and intended expressions are respectively `12*x` and `4*x`, confirmed with exact symbolic algebra. The surrounding steps return to the intended expression; these findings do not independently establish that every final answer is correct.',
'','## Existing content gaps and optional cleanup','',
'- **33 practice questions lack worked solutions.** All 31 canonical examples have worked solutions.',
'- **36 practice questions have missing correct-answer links, affecting 39 fields.** These include all 33 questions without solutions and three additional questions. In the hyperbolic integration lesson, all eight existing practice questions lack both solutions and keys.',
'- 28 attributes retain valid but awkward grouping such as `(x+1{)}^2`; this is optional source normalization, not a rendering failure.',
'- Inline sentence punctuation inside math also remains a style cleanup. Display-equation punctuation is not automatically an error.',
'- All 21 flagged Markdown tables are genuine x-to-u limit-conversion tables with consistent columns; they are not malformed fraction captures.',
'','## Exact affected entities and attributes','']
 sections=[('Misplaced underbrace','literal_brace'),('Trailing equals alignment','trailing_equals'),('Legacy equation rows','legacy_command'),('Missing prompt separation','missing_separation'),('Missing worked solutions','missing_solution'),('Missing correct-answer links','missing_key')]
 for title,code in sections:
  r += [f'### {title}','','| Entity | Attribute | Detail |','| --- | --- | --- |']
  for v in findings:
   if v['code']==code:r.append(f"| `{v['entity']}` | `{v['attribute']}` | {', '.join(str(x)for x in v['detail'])if isinstance(v['detail'],list)else ''} |")
  r.append('')
 r += ['### Unformatted function names','','| Entity | Attribute | Names |','| --- | --- | --- |']
 for e,a in operator_attrs:
  names=sorted({v['operator']for v in additional['plain_operators']if v['entity']==e and v['attribute']==a})
  r.append(f"| `{e}` | `{a}` | {', '.join(names)} |")
 r+=['','## Lesson identities and route coverage','','| Topic | Lesson activity | Title | Steps | Tutorials | Examples | Practice |','| --- | --- | --- | ---: | ---: | ---: | ---: |']
 for v in inv['lessons']:r.append(f"| `{v['topic']}` | `{v['activity']}` | {v['title']} | {v['steps']} | {v['tutorials']} | {v['examples']} | {v['practice']} |")
 r+=['','## Supporting evidence','',
'- [Database snapshot](lessons.edn) and [read-only query](lessons-query.edn).',
'- [Inventory and routes](inventory.json), [source findings](source-findings.json), and [additional notation findings](additional-source-review.json).',
'- [Full tutorial/example/question source](source-review.txt).',
'- [Browser summary](browser-summary.json), [measurements](browser-report.json), and [visual probes](visual-probes.json).',
'- [Image asset resolution](images.json) and [confirmed sign typos](confirmed-sign-typos.json).','']
 # Independently count actual problematic aligned environments, excluding wrappers.
 affected_align=sum(sum(bool(re.search(r'&\s*=\s*\\\\',m))for m in re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',entities[str(f['entity'])][f['attribute']]))for f in findings if f['code']=='trailing_equals')
 assert affected_align==14,affected_align
 (HERE/'audit.md').write_text('\n'.join(r))
 summary={'read_only':True,'database_basis':3529,'lessons':10,'tutorials':12,'examples':31,'practice_questions':275,'answer_values':1262,'rendered_item_states':1272,'misplaced_underbrace_solutions':63,'trailing_equals_content_entities':8,'trailing_equals_environments':14,'legacy_row_examples':4,'legacy_row_display_blocks':5,'unformatted_operator_attributes':38,'broken_bold_tutorials':1,'missing_prompt_separations':3,'confirmed_sign_typos':2,'missing_solutions':33,'questions_missing_keys':36,'fields_missing_keys':39,'mathjax_error_nodes':0,'outer_card_overflow':0,'changes_made':False}
 (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()

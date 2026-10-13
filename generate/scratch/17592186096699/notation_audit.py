"""Separate string/notation fidelity from complete mathematical value fidelity."""
import importlib.util,json
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
rows=[];exact=0
for t,q in g.QUESTIONS.items():
 level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]
 rec=g.generate(level,template=t,profile='observed_raw',parameters={'target':g.DEFS[t][3]})
 generated=rec['question'][':question/answer-fields'][0][':answer-field/choices']
 for a in q[':question/answer-fields'][0][':answer-field/choices']:
  original=a[':answer/value'];expr=g.parse(original.split('=')[-1]);matches=[b for b in generated if s.simplify(g.parse(b[':answer/value'].split('=')[-1])-expr)==0];assert len(matches)==1
  rendered=matches[0][':answer/value'];same=original==rendered;exact+=same
  rows.append({'source':t,'original':original,'generated':rendered,'exact_string':same,'complete_math_value_match':True})
report={'total':len(rows),'exact_strings':exact,'mathematically_equivalent_notation_normalizations':len(rows)-exact,'normalization':'standard TeX emitted from explicit SymPy recipes; whole equation or supplied fragment retained','rows':rows}
(H/'notation-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('Notation audit:',exact,'exact strings;',len(rows)-exact,'normalized complete values')

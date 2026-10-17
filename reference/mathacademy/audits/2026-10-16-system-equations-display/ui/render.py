"""Read-only reproducer for the stored semicolon system and canonical rows."""
import copy, importlib.util, json, sys
from pathlib import Path
ROOT = Path('/home/jake/Developer/Course_Academy')
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'scripts/question_capture'))
import math_format
spec = importlib.util.spec_from_file_location('render_preview', ROOT/'generate/pipeline/render_preview.py')
renderer = importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
entity = json.loads((ROOT/'reference/mathacademy/audits/2026-10-16-mth341/entities.json').read_text())['17592186529306']
original=copy.deepcopy(entity)
field=original[':question/answer-fields'][0]
field[':answer-field/type']={':db/ident':':answer-field.type/select'}
field[':answer-field/correct'] = next(a for a in field[':answer-field/choices'] if a[':db/id']==field[':answer-field/correct'][':db/id'])
canonical=copy.deepcopy(original)
canonical[':question/problem']=original[':question/problem'].replace(r'\{-3x - y = 8; 3x + y = -6',r'\left\{\begin{aligned}-3x-y &= 8 \\ 3x+y &= -6\end{aligned}\right.')
canonical[':question/worked-solution']=original[':question/worked-solution'].replace(r'\{-3x - y = 8 \mid \mid \cdot (1); 3x + y = -6',r'\left\{\begin{aligned}-3x-y &= 8 && \mid \mid \cdot (1) \\ 3x+y &= -6\end{aligned}\right.')
records=[{'question':original},{'question':canonical}]
renderer.BROWSER_SCRIPT=renderer.BROWSER_SCRIPT.replace('mathContainers:document.querySelectorAll', '''mathTables:(()=>{const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0]?.childNodes.length,alignment:node.attributes.get('columnalign')});});return tables;})(),
        texInputs:Array.from(MathJax.startup.document.math).map(item=>item.math),
        mathContainers:document.querySelectorAll''')
checks={
 'question_entity':17592186529306,
 'source_snapshot':'reference/mathacademy/audits/2026-10-16-mth341/entities.json',
 'original_problem':original[':question/problem'],
 'normalized_problem':math_format.normalize_prose(original[':question/problem']),
 'normalizer_changes_problem':math_format.normalize_prose(original[':question/problem'])!=original[':question/problem'],
 'structural_validation_passes':math_format.validate_prose(original[':question/problem'])==original[':question/problem'],
 'literal_open_brace_normalized':math_format.normalize_tex(r'{-3x-y=8;3x+y=-6'),
 'escaped_open_brace_normalized':math_format.normalize_tex(r'\{-3x-y=8;3x+y=-6'),
 'canonical_problem':canonical[':question/problem'],
 'canonical_solution_example':canonical[':question/worked-solution'],
 'canonical_note':'Offline layout demonstration only; no database or UI source mutations.'
}
(HERE/'normalizer-findings.json').write_text(json.dumps(checks,indent=2)+'\n')
renderer.render(records, HERE/'actual-ui', [], browser='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')

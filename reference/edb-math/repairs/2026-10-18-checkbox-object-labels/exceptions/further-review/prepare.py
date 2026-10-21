"""Minimal rendering-only corrections discovered during the full checkbox replay."""
import copy,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
cases=json.loads((ROOT/'mapping-render/cases.json').read_text())['cases']
SET_IDS={17592186287770,17592186287771,17592186287772,17592186287773,17592186287782}
selected=[];changes=[]
for case in cases:
    revised=copy.deepcopy(case);qid=case['question'];dirty=False
    for attr in (':question/problem',':question/worked-solution'):
        before=case['after'].get(attr,'');after=before;reasons=[]
        if '______' in after:
            assert re.search(r'\$______[,\.]\$',after),(qid,attr)
            after=after.replace('______',r'\underline{\hspace{3em}}');reasons.append('A visible statement-completion blank was encoded as repeated TeX subscript operators.')
        if qid in SET_IDS:
            # These five reviewed Cartesian-product questions use braces only
            # as set delimiters at these precise syntactic positions.
            after=re.sub(r'(?<!\\)\{([a-zA-Z0-9]+(?:,[a-zA-Z0-9]+)+)\}',lambda m:r'\{'+m[1]+r'\}',after)
            after=re.sub(r'(?<!\\)\{((?:\([a-zA-Z0-9,]+\),?)+)\}',lambda m:r'\{'+m[1]+r'\}',after)
            after=re.sub(r'(\\begin\{aligned\}[^\n]*?=)\{( & [^\n]+)\}(\.\\end\{aligned\})',lambda m:m[1]+r'\{'+m[2]+r'\}'+m[3],after)
            after=after.replace(r'\text{\(}',r'(')
            if after!=before:reasons.append('Escape literal set delimiters; remove a spurious TeX math-opening escape inside the displayed Cartesian-product parenthesis.')
        if after!=before:
            revised['after'][attr]=after;dirty=True
            changes.append({'question_eid':qid,'attribute':attr,'before':before,'after':after,'reasons':reasons})
    if dirty:selected.append(revised)
(HERE/'cases.json').write_text(json.dumps({'cases':selected},ensure_ascii=False,indent=2)+'\n')
(HERE/'overrides.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'questions':len(selected),'changed_attributes':len(changes)}))

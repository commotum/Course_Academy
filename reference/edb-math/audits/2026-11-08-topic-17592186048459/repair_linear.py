"""Prepare the authorized source-backed repairs, preserving all owned IDs."""
import copy
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT/'scripts'))
from question_capture.math_format import MATH, normalize_prose, matrix_answer
from question_capture.edn import dumps, kw

before = json.loads((HERE/'questions.json').read_text())
questions = copy.deepcopy(before)
originals = {r['entity']: r for r in json.loads((HERE/'source-manifest.json').read_text())}
fresh = {r['entity']: r for r in json.loads((HERE/'current-extractor-results.json').read_text())}
findings = json.loads((HERE/'findings.json').read_text())
table_ids = set(findings['findings'][0]['entities'])
changes = []
templates = []

def bold_symbols(entity):
    symbols = set()
    for role in ['prompt_sources','solution_sources']:
        for source in originals[entity][role]:
            soup = BeautifulSoup(source['html'],'html.parser')
            symbols.update(n.get_text().strip() for n in soup.select('[mathvariant="bold"]')
                           if re.fullmatch(r'[A-Za-z0]',n.get_text().strip()))
    return symbols

def restore_fonts(value, symbols):
    def formula(match):
        text = match[0]
        text = re.sub(r'\\(mathbf|mathbfit|mathrm|mathit|mathbb|textbf)\s+([A-Za-z0-9])',lambda m:'\\'+m[1]+'{'+m[2]+'}',text)
        protected = []
        def protect(m):
            protected.append(m[0])
            return 'FONTGUARD'+str(len(protected)-1)+'END'
        text = re.sub(r'\\(?:mathbf|mathbfit|mathrm|mathit|mathbb|textbf|text|textrm|operatorname)\{[^{}]*\}',protect,text)
        # A numeric zero in a coordinate column remains an ordinary scalar.
        matrices = []
        def matrix(m):
            matrices.append(m[0]);return 'MATRIXGUARD'+str(len(matrices)-1)+'END'
        if '0' in symbols:
            text = re.sub(r'\\begin\{(?:bmatrix|pmatrix|matrix|array)\}.*?\\end\{(?:bmatrix|pmatrix|matrix|array)\}',matrix,text,flags=re.S)
        # Mathematical products such as kv and kT(v) contain individual
        # variables. Protect command names and environment names, then apply
        # the source font only to literal symbols, including those products.
        token = r'FONTGUARD\d+END|MATRIXGUARD\d+END|\\(?:begin|end)\{[^{}]*\}|\\[A-Za-z]+|\d+|[\s\S]'
        text = re.sub(token,lambda m:r'\mathbf{'+m[0]+'}'if m[0]in symbols else m[0],text)
        text = re.sub(r'MATRIXGUARD(\d+)END',lambda m:matrices[int(m[1])],text)
        text = re.sub(r'FONTGUARD(\d+)END',lambda m:protected[int(m[1])],text)
        return text
    return MATH.sub(formula,value)

authored_solutions = {
    17592186088152: r'''Since $\mathbf T$ is a linear transformation, it satisfies $\mathbf T(k\mathbf v)=k\mathbf T(\mathbf v).$ Noting that

$$
\begin{bmatrix}10\\14\end{bmatrix}=2\begin{bmatrix}5\\7\end{bmatrix},
$$

we have

$$
\begin{aligned}
\mathbf T\left(\begin{bmatrix}10\\14\end{bmatrix}\right)
&=\mathbf T\left(2\begin{bmatrix}5\\7\end{bmatrix}\right)\\
&=2\mathbf T\left(\begin{bmatrix}5\\7\end{bmatrix}\right)\\
&=2\begin{bmatrix}-8\\3\end{bmatrix}\\
&=\begin{bmatrix}-16\\6\end{bmatrix}.
\end{aligned}
$$''',
    17592186088150: r'''First, since $\mathbf v_1+\mathbf v_2=\mathbf 0,$ we have

$$
\begin{aligned}
15\mathbf v_1+19\mathbf v_2
&=15\mathbf v_1+15\mathbf v_2+4\mathbf v_2\\
&=15(\mathbf v_1+\mathbf v_2)+4\mathbf v_2\\
&=15\mathbf 0+4\mathbf v_2\\
&=4\mathbf v_2.
\end{aligned}
$$

Therefore, $\mathbf T(15\mathbf v_1+19\mathbf v_2)=\mathbf T(4\mathbf v_2).$ Since $\mathbf T$ is linear, it satisfies $\mathbf T(k\mathbf v)=k\mathbf T(\mathbf v).$ Thus

$$
\begin{aligned}
\mathbf T(15\mathbf v_1+19\mathbf v_2)
&=4\mathbf T(\mathbf v_2)\\
&=4\begin{bmatrix}-12\\9\\15\end{bmatrix}\\
&=\begin{bmatrix}-48\\36\\60\end{bmatrix}.
\end{aligned}
$$'''
}
expected_keys = {17592186087995:'III only',17592186088152:r'\begin{bmatrix}-16 \\ 6\end{bmatrix}',
                 17592186088150:r'\begin{bmatrix}-48 \\ 36 \\ 60\end{bmatrix}'}

for question in questions:
    entity = question[':db/id']
    if entity in table_ids:
        # Recover the label and row-to-field bindings from the saved source;
        # retain the already-repaired wording and givens before the answer.
        value = normalize_prose(fresh[entity]['prompt_sources']['problem'])
        layout = value[value.index('<div class="matrix-answer">'):]
        old = question[':question/problem']
        prefix = re.split(r'\n\n(?=\||<table)',old,maxsplit=1)[0].strip()
        question[':question/problem'] = prefix+'\n\n'+layout
        assert sorted(re.findall(r'\{\{([^{}]+)\}\}',layout)) == sorted(f[':answer-field/key']for f in question[':question/answer-fields'])
    if entity == 17592186235515:
        old = question[':question/problem']
        prefix = old[:old.index('$T(q)=')].strip()
        question[':question/problem'] = prefix+'\n\n'+r'$T(q)=\langle$ {{field-1}} $,\,$ {{field-2}} $,\,$ {{field-3}} $\rangle.$'
    if entity == 17592186087995:
        question[':question/problem'] = question[':question/problem'].replace(r'2 \cdot 1',r'2\times 1')
        question[':question/worked-solution'] = normalize_prose(fresh[entity]['solution_sources']['worked_solution'])
    if entity in authored_solutions:
        question[':question/worked-solution'] = normalize_prose(authored_solutions[entity])
        templates.append({'entity':entity,'source':'locally authored completion','canonical_example':17592186087563 if entity==17592186088152 else 17592186087565,
                          'nearby_example':17592186088151 if entity==17592186088152 else 17592186398989,
                          'pattern':'T(ku)=kT(u), target scale 2' if entity==17592186088152 else 'v1+v2=0; reduce 15v1+19v2 to 4v2; apply linearity',
                          'all_existing_choices_preserved':True})
    if entity == 17592186344982:
        old = question[':question/worked-solution']
        wrong = r'\begin{bmatrix}1 \\ 2 \\ -2\end{bmatrix}'
        assert old.count(wrong)==1
        question[':question/worked-solution'] = old.replace(wrong,r'\begin{bmatrix}1 \\ 2 \\ -1\end{bmatrix}')
    symbols = bold_symbols(entity)
    for attribute in [':question/problem',':question/worked-solution']:
        if attribute in question:
            question[attribute] = normalize_prose(restore_fonts(question[attribute],symbols))
    for field in question.get(':question/answer-fields',[]):
        if field[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
            field[':answer-field/key'] = normalize_prose(restore_fonts(field[':answer-field/key'],symbols))
        if entity in expected_keys:
            bank = field[':answer-field/choices']
            candidates = [a for a in bank if a[':answer/value']==expected_keys[entity]]
            assert len(candidates)==1,(entity,expected_keys[entity])
            field[':answer-field/correct'] = candidates[0]

def changed(old,new):
    for attribute in [':question/problem',':question/worked-solution']:
        if old.get(attribute)!=new.get(attribute):
            changes.append({'entity':old[':db/id'],'attribute':attribute[1:],'old':old.get(attribute),'new':new[attribute]})
    for previous,current in zip(old.get(':question/answer-fields',[]),new.get(':question/answer-fields',[])):
        assert previous[':db/id']==current[':db/id']
        for attribute in [':answer-field/key',':answer-field/correct']:
            a,b=previous.get(attribute),current.get(attribute)
            if attribute.endswith('/correct'):
                a=a.get(':db/id')if a else None;b=b.get(':db/id')if b else None
            if a!=b:changes.append({'entity':previous[':db/id'],'attribute':attribute[1:],'old':a,'new':b})
for old,new in zip(before,questions):changed(old,new)

forms=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['old'],c['new']]for c in changes]
owners={q[':db/id']for q in questions}
for entity in sorted({c['entity']for c in changes}):
    forms.append([kw('db/ensure'),entity,kw('question/validate'if entity in owners else 'answer-field/validate')])
out=HERE/'repair';out.mkdir(exist_ok=True)
(out/'questions-after.json').write_text(json.dumps(questions,indent=2)+'\n')
(out/'changes.json').write_text(json.dumps(changes,indent=2)+'\n')
(out/'completion-templates.json').write_text(json.dumps(templates,indent=2)+'\n')
(out/'transaction.edn').write_text(dumps(forms)+'\n')
# Produce complete renderer input, retaining every answer value and label.
fields=json.loads((HERE/'fields.json').read_text())
for change in changes:
    if change['attribute']=='answer-field/correct':continue
    field=next((f for f in fields if f['entity']==change['entity']and f['attribute']==':'+change['attribute']),None)
    if field:field['value']=change['new']
    else:fields.append({'entity':change['entity'],'attribute':':'+change['attribute'],'value':change['new']})
for question in questions:
    item=next(f for f in fields if f['entity']==question[':db/id']and f['attribute']==':question/problem')
    for f in item.get('fields',[]):
        new=next(n for n in question.get(':question/answer-fields',[])if str(n[':db/id'])==f['id'])
        f['key']=new[':answer-field/key']
(out/'fields.json').write_text(json.dumps(fields,indent=2)+'\n')
print(json.dumps({'changed_attributes':len(changes),'changed_questions':len({c['entity']for c in changes if c['entity']in owners}),
                  'correct_links_added':sum(c['attribute']=='answer-field/correct'for c in changes),'field_identities_preserved':True},indent=2))

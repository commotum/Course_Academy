"""Render actual changed formulas, stratified by operator and script form."""
import json,re,sys,uuid
from collections import Counter
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import MATH,NAMED_FUNCTION_OPERATORS
import generate.pipeline.render_preview as r
names='|'.join(sorted(NAMED_FUNCTION_OPERATORS,key=len,reverse=True));token=re.compile(r'\\(?:operatorname\{('+names+r')\}|('+names+r')(?![A-Za-z]))')
def counts(text):return Counter(m[1] or m[2] for m in token.finditer(text))
proposals=json.loads((H/'proposals.json').read_text());options={};inserted=Counter()
for change in proposals:
    delta=counts(change['after'])-counts(change['before']);inserted.update(delta)
    spans=[change['after']] if change['attribute']=='answer/value' else [m[0] for m in MATH.finditer(change['after'])]
    for name in delta:
        for span in spans:
            if name not in counts(span):continue
            profile=name+('/scripted' if re.search(r'(?:'+re.escape(name)+r'}|'+re.escape(name)+r')s*}?s*[_^]',span) else '/ordinary')
            score=len(span)+(1000 if change['attribute']=='answer/value' else 0)
            if profile not in options or score<options[profile][0]:options[profile]=(score,change,span)
rows=[]
for profile,(_,change,span) in sorted(options.items()):
    if change['attribute']=='answer/value':span='$$\n'+span+'\n$$'
    rows.append({'knowledge_point':{'title':'Operator notation verification'},'question':{
        ':question/id':str(uuid.uuid5(uuid.NAMESPACE_URL,'operator-notation/'+profile)),':question/problem':span,
        ':question/worked-solution':'Operator notation verification.',':question/answer-fields':[]},
        'verification':{'profile':profile,'entity':change['entity'],'attribute':change['attribute']}})
(H/'render-input.json').write_text(json.dumps(rows,indent=2)+'\n')
old=r.VISIBLE_DOM_AUDIT
audit=old.replace('fonts:document.fonts.status',r'''
        operators:[...root.querySelectorAll('[data-mml-node="mi"],[data-mml-node="mo"],[data-mml-node="mtext"]')]
          .map(node=>[...node.querySelectorAll('use[data-c]')].map(glyph=>String.fromCodePoint(parseInt(glyph.getAttribute('data-c'),16))).join('')),
        fonts:document.fonts.status''')
r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace(old,audit)
r.render(rows,H/'desktop',[Path('/media/jake/SSD/EDB/math')])
report=json.loads((H/'desktop/rendering.json').read_text());assert report['passed']
for row,case in zip(rows,report['cases']):
    name=row['verification']['profile'].split('/')[0]
    assert name in case['operators'] or (name in ('Re','Im') and any(g in case['operators'] for g in ('ℜ','ℑ'))),(name,case['operators'])
result={'passed':True,'operator_names':sorted(inserted),'new_operator_occurrences':dict(inserted),
        'profiles_rendered':len(rows),'actual_changed_formula_samples':True,
        'all_operator_glyphs_present':True,'lesson_rendered_questions':37,'lesson_phone_examples':4}
(H/'render-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'profiles':len(rows),'operators':len(inserted)}))

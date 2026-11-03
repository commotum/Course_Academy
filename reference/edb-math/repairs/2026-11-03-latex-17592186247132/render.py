"""Actual learner UI checks, including upright inverse-operator glyph groups."""
import copy,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
import generate.pipeline.render_preview as r

old_audit=r.VISIBLE_DOM_AUDIT
new_audit=old_audit.replace('fonts:document.fonts.status',r'''
        inverseOperators:[...root.querySelectorAll('[data-mml-node="mi"],[data-mml-node="mo"],[data-mml-node="mtext"]')]
          .map(node=>[...node.querySelectorAll('use[data-c]')].map(glyph=>String.fromCodePoint(parseInt(glyph.getAttribute('data-c'),16))).join(''))
          .filter(text=>/^(?:arcsec|arccsc|arccot)$/.test(text)),
        fonts:document.fonts.status''')
base=r.BROWSER_SCRIPT.replace(old_audit,new_audit)
rows=json.loads((H/'render-input.json').read_text());old=json.loads((H/'lesson-questions.json').read_text())
before=[]
for eid in (17592186247132,17592186115736):
    row=next(x for x in old if x['question'][':db/id']==eid);q=copy.deepcopy(row['question'])
    q[':question/answer-fields']=[f for f in q.get(':question/answer-fields',[]) if f.get(':answer-field/correct')]
    before.append({'knowledge_point':{'db_id':row['kp'],'title':row['title']},'question':q})
r.BROWSER_SCRIPT=base
try:r.render(before,H/'before-ui',[Path('/media/jake/SSD/EDB/math')])
except subprocess.CalledProcessError:pass  # The second legacy macro is deliberately broken.
report=json.loads((H/'before-ui/rendering.json').read_text())
assert report['cases'][0]['inverseOperators']==[]
assert report['cases'][1]['mathErrors']
for mode in ('desktop','phone'):
    r.BROWSER_SCRIPT=base
    selected=rows
    if mode=='phone':
        r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('width:1280,height:1000','width:390,height:844')
        ids=(17592186247132,17592186115533,17592186315057,17592186299712)
        selected=[x for x in rows if x['question'][':db/id'] in ids]
    r.render(selected,H/mode,[Path('/media/jake/SSD/EDB/math')])
    report=json.loads((H/mode/'rendering.json').read_text());assert report['passed']
    assert all(case['inverseOperators'] for case in report['cases'])
result={'passed':True,'changed_questions_rendered':len(rows),'before_reported_question_was_italic_letters':True,
        'before_legacy_macro_failed_mathjax':True,'all_repaired_questions_have_upright_operator_glyph_groups':True,
        'phone_representatives':4}
(H/'render-verification.json').write_text(json.dumps(result,indent=2)+'\n')

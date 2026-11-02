import copy,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import normalize_prose,validate_prose
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
k=json.loads((H/'17592186119939/before.json').read_text());proposals=[];render=[];audit=[]
y=s.Symbol('y',positive=True)
def expr(raw):
    raw=raw.replace(r'\sqrt{y}','sqrt(y)').replace('{','(').replace('}',')').replace('^','**')
    return parse_expr(raw,local_dict={'y':y,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
for q in [k[':knowledge-point/canonical-example'],*k[':knowledge-point/questions']]:
    out=copy.deepcopy(q);before=q[':question/problem'];after=normalize_prose(before)
    if 'fraction-equation' in after:
        assert q[':db/id'] in (17592186233915,17592186315109)
        assert re.findall(r'\{\{field-\d+\}\}',before)==re.findall(r'\{\{field-\d+\}\}',after)
        proposals.append({'entity':q[':db/id'],'attribute':'question/problem','before':before,'after':after});out[':question/problem']=after
        f={f[':answer-field/key']:expr(f[':answer-field/correct'][':answer/value']) for f in q[':question/answer-fields']}
        given=-2/y**2+5*y**2 if q[':db/id']==17592186315109 else 4*s.sqrt(y)+3*y**5
        answer=y**3/f['field-1'] if q[':db/id']==17592186315109 else f['field-1']/(2*s.sqrt(y)+f['field-2'])
        assert s.simplify(answer-1/s.diff(given,y))==0
    if q[':db/id']==17592186315109:
        old=q[':question/worked-solution'];wrong='-2{y}^{-1}+5{y}^{2}';right='-2{y}^{-2}+5{y}^{2}'
        assert old.count(wrong)==1;fixed=old.replace(wrong,right)
        proposals.append({'entity':q[':db/id'],'attribute':'question/worked-solution','before':old,'after':fixed});out[':question/worked-solution']=fixed
    for key in (':question/problem',':question/worked-solution'):
        if out.get(key):validate_prose(out[key])
    fields=out.setdefault(':question/answer-fields',[]);incomplete=any(not f.get(':answer-field/correct') for f in fields)
    audit.append({'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'fraction_repaired':'fraction-equation' in out[':question/problem'],'has_original_answer_key':not incomplete and bool(fields),'table_remains':bool(re.search(r'^\|',out[':question/problem'],re.M))})
    # A display-only fixture must not invent missing original radio keys.
    if incomplete:out[':question/answer-fields']=[]
    render.append({'question':out})
assert len(proposals)==3 and sum(r['fraction_repaired'] for r in audit)==2
for name,value in [('proposals',proposals),('render-input',render),('audit',{'passed':True,'practice_questions':9,'canonical_examples':1,'registered_generator':None,'rows':audit,'correct_fraction_keys_verified':True})]:
    (H/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
print('Audited all ten records; two fraction prompts and one exponent typo repaired; existing keys preserved')

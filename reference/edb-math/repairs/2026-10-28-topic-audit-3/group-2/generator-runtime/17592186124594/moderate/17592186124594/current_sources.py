"""Read-only audit of all current source questions, including post-freeze additions.

Original database records remain untouched. Escape normalization is for exact
mathematics comparison only, never a proposed source repair.
"""
import copy, hashlib, itertools, json, re
from pathlib import Path
import sympy as sp
import validate as v
g=v.g
HERE=Path(__file__).resolve().parent

def clean_answer(value):
    return g.normalize(value.replace('\\\\','\\'))

def formula(q):
    text=g.normalize(q[':question/problem'])
    m=re.search(r'\$([a-z])\(x\s*,\s*y\)\s*=\s*(.*?)\$',text)
    if not m:raise ValueError('Unrecognized Cartesian source prompt')
    f=g.parse_math(m[2].strip().removesuffix(','))
    d=re.search(r'find \$\\frac\{∂'+m[1]+r'\}\{∂(r|\\theta)\s*\}',text)
    if not d:raise ValueError('Unrecognized derivative target')
    variable=g.R if d[1]=='r' else g.T
    return m[1],f,variable

def fingerprint(q):
    _,f,variable=formula(q)
    return g.digest([sp.srepr(sp.cancel(sp.diff(f,g.X))),sp.srepr(sp.cancel(sp.diff(f,g.Y))),'r' if variable==g.R else 'theta'])

def canonical_fp():
    f=g.X**2/2+g.Y**2
    return g.digest([sp.srepr(sp.diff(f,g.X)),sp.srepr(sp.diff(f,g.Y)),'theta'])

def audit(q):
    sid=q[':question/math-academy-id'];name,f,variable=formula(q)
    actual=sp.diff(f.subs({g.X:g.R*sp.cos(g.T),g.Y:g.R*sp.sin(g.T)},simultaneous=True),variable)
    fields=[];errors=[]
    for field in q.get(':question/answer-fields',[]):
        values=[];fail=[]
        for a in field.get(':answer-field/choices',[]):
            try:values.append(g.parse_math(clean_answer(a[':answer/value'])))
            except (ValueError,AssertionError,IndexError,TypeError) as ex:
                values.append(None);fail.append({'answer_id':str(a[':answer/id']),'error':str(ex),'raw_value':a[':answer/value']})
        correct=field.get(':answer-field/correct');matched=[i for i,z in enumerate(values) if z is not None and v.eq(z,actual)]
        ref_matches=bool(correct and len(matched)==1 and field[':answer-field/choices'][matched[0]][':answer/id']==correct[':answer/id'])
        distinct=not fail and all(not v.eq(a,b) for a,b in itertools.combinations(values,2))
        valid=ref_matches and distinct and len(values)==5
        fields.append({'field_id':str(field[':answer-field/id']),'field_key':field[':answer-field/key'],'field_type':str(field[':answer-field/type'][':db/ident']),'value_count':len(values),'parse_failures':fail,'complete_bank_distinct':distinct,'unique_correct_value':len(matched)==1,'correct_reference_matches':ref_matches,'valid':valid})
    if len(fields)!=1:errors.append('Duplicate selection fields, one without a correct reference')
    if sid in ('q-94999','q-95113','q-95116'):errors.append('Existing source solution has documented wrong function/partial label; no database repair in this job')
    if sid=='q-95108':errors.append('Source solution says partial derivatives of n rather than p')
    if not fields or not all(x['valid'] for x in fields):errors.append('Incomplete or malformed source answer bank')
    # Independently read every printed row for the intact single-field sources.
    if not errors:
        n=copy.deepcopy(q)
        for k in (':question/problem',':question/worked-solution'):
            n[k]=g.normalize(n[k])
            if name not in 'fghw':
                n[k]=n[k].replace('∂'+name,'∂f').replace('$'+name+'(', '$f(').replace('$'+name+'$', '$f$')
        n={k:n[k] for k in (':question/problem',':question/worked-solution')}
        n[':question/id']=str(q[':question/id'])
        n[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
        n[':question/answer-fields']=[]
        for field in q[':question/answer-fields']:
            n[':question/answer-fields'].append({':answer-field/id':str(field[':answer-field/id']),':answer-field/key':field[':answer-field/key'],':answer-field/type':str(field[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(field[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':clean_answer(a[':answer/value'])} for a in field[':answer-field/choices']]})
        try:v.check_record({'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':n,'generation':{'template':'current-source'}})
        except (AssertionError,ValueError,TypeError,IndexError) as ex:errors.append('Printed source solution validation: '+str(ex))
    return {'source_id':sid,'question_id':str(q[':question/id']),'entity':q[':db/id'],'difficulty':str(q[':question/difficulty'][':db/ident']),'function':str(f),'target':'r' if variable==g.R else 'theta','mathematical_fingerprint':fingerprint(q),'fields':fields,'plot_rating':'none','validated_practice':not errors,'errors':errors}

"""Audit the captured current source bank without mutating any source entities."""
import importlib.util,json,re,sys,hashlib,copy,subprocess
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent
ROOT=D.parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import loads
spec=importlib.util.spec_from_file_location('validation',D/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
x,y,u,w=v.x,v.y,v.u,v.v

def clean(t):
    t=t.replace('\\\\','\\').replace(r'\text{d}','d').replace('{e}','e')
    t=re.sub(r'\{ln\}\^\{(\d+)\}[⁡\u2061]*(\d+)',lambda m:'(\\ln '+m[2]+')^{'+m[1]+'}',t)
    return t

def val(t):
    t=clean(t)
    return v.integral_value(t)[0] if r'\int' in t else v.math(t)

def normalize(q):
    z={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    z[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
    z[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        z[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
    return z

def task(U,V,f,bounds):
    return v.g.digest([str(s.simplify(t)) for t in (U,V,f)]+[str(z) for z in bounds])

# Supplied transformations, integrands, transformed bounds and one-to-one inverses
# independently transcribed from all 14 current prompts. sum/product is excluded.
SPECS={
 'q-38129':(x+y,y-x,y*y-x*x,(0,3,0,2),{x:(u-w)/2,y:(u+w)/2}),
 'q-160897':(y/x**2,x*y,x*y,(1,4,1,5),{x:(w/u)**s.Rational(1,3),y:u**s.Rational(1,3)*w**s.Rational(2,3)}),
 'q-38369':(2*x+y,y,2*x*y+x*x,(0,5,0,1),{x:(u-w)/2,y:w}),
 'q-82808':(y-x,x+y,8*x*y,(-1,1,0,1),{x:(w-u)/2,y:(w+u)/2}),
 'q-82827':(2*x+5*y,x+3*y,s.exp(x+y),(0,2,0,4),{x:3*u-5*w,y:2*w-u}),
 'q-83647':(x+y,y-x,3*(x+y)**2,(-1,3,-4,-1),{x:(u-w)/2,y:(u+w)/2}),
 'q-83656':(s.exp(x),s.exp(y),y,(1,2,1,4),{x:s.log(u),y:s.log(w)}),
 'q-82798':(2*y-x,y-x,x*x,(1,2,0,1),{x:u-2*w,y:u-w}),
 'q-82818':(x+1,y+(x+1)**2,x-y+1,(0,1,1,2),{x:u-1,y:w-u*u}),
 'q-160850':(x+y,x-y,(x+y)*(x-y)**s.Rational(3,2),(1,3,0,1),{x:(u+w)/2,y:(u-w)/2}),
 'q-82911':(x+y,x-y,x*x-y*y,(0,2,2,4),{x:(u+w)/2,y:(u-w)/2}),
 'q-160899':(y/x,x*y,s.exp(-x*y/2),(s.Rational(1,4),2,1,4),{x:s.sqrt(w/u),y:s.sqrt(u*w)}),
 'q-82985':(x+3*y,x+2*y,(x+3*y)/(x+2*y),(0,2,2,4),{x:3*w-2*u,y:u-w})}

def fingerprint(q):
    U,V,f,bounds,_=SPECS[q[':question/math-academy-id']]
    return task(U,V,f,bounds)

def generated_fingerprint(rec):
    p,U,V,f,_,_=v.read_prompt(rec)
    return task(U,V,f,[p[k] for k in ('ul','uh','vl','vh')])

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'field-owned radio choice'} for a in f[':answer-field/choices']]

def main():
    kp=loads((D/'reference/initial/kp.edn').read_text())[0][0]
    rows=[];inputs=[]
    for q in kp[':knowledge-point/questions']:
        mid=q[':question/math-academy-id'];row={'entity':q[':db/id'],'source_id':mid,'difficulty':q.get(':question/difficulty',{}).get(':db/ident'),'field_types':[str(f[':answer-field/type'][':db/ident']) for f in q[':question/answer-fields']], 'choice_count':len(q[':question/answer-fields'][0][':answer-field/choices']),'plots':'none','prompt':q[':question/problem'],'worked_solution':q.get(':question/worked-solution'),'eligible':False}
        if mid=='q-38371':
            row['exclusion']='Image constrained by v²>=4u; two inverse branches. Stored 9(e⁴-e) is incorrect. True value 12e⁴-16e+2sqrt(pi)(erfi(2)-erfi(1)).'
        else:
            U,V,f,b,inv=SPECS[mid]
            v.eq(U.subs(inv,simultaneous=True),u);v.eq(V.subs(inv,simultaneous=True),w)
            jac=s.det(s.Matrix([[s.diff(U,x),s.diff(U,y)],[s.diff(V,x),s.diff(V,y)]]))
            z=s.simplify((f/s.Abs(jac)).subs(inv,simultaneous=True))
            result=s.simplify(s.integrate(s.integrate(z,(u,b[0],b[1])),(w,b[2],b[3])))
            field=q[':question/answer-fields'][0];values=[val(a[':answer/value']) for a in field[':answer-field/choices']]
            key=field.get(':answer-field/correct',{}).get(':answer/value')
            row.update({'supplied_map':[str(U),str(V)],'integrand':str(f),'transformed_integrand':str(z),'bounds':[str(a) for a in b],'inverse':{str(k):str(z) for k,z in inv.items()},'jacobian':str(jac),'correct_value':str(result),'choice_values':[str(z) for z in values],'complete_bank_distinct':v.g.eligible(values),'fingerprint':fingerprint(q)})
            if key is not None:v.eq(val(key),result)
            if mid=='q-38129':row['exclusion']='Unrated, absent correct reference and worked solution.'
            elif not v.g.eligible(values):row['exclusion']='Complete definite-integral choices collide at zero.'
            elif mid=='q-160899':row['exclusion']='Solution changes dv to du while integrating a v-expression. Preserved, conservatively excluded.'
            else:
                row['eligible']=True
                rec={'knowledge_point':{'title':v.g.TITLE},'question':normalize(q),'generation':{'template':mid}}
                inputs.append({'label':mid,'record':rec,'checks':checks(rec)})
        rows.append(row)
    out=D/'reference/initial'
    (out/'source-audit.json').write_text(json.dumps({'basis':json.loads((out/'basis.json').read_text())['basis'],'rows':rows},indent=2,default=str)+'\n')
    (out/'native-input.json').write_text(json.dumps(inputs,indent=2)+'\n')
    subprocess.run([str(D/'reference/check-engine'),str(out/'native-input.json'),str(out/'native-report.json')],check=True)
    print([(r['source_id'],r['eligible'],r.get('exclusion')) for r in rows])
if __name__=='__main__':main()

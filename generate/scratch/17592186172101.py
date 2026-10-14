#!/usr/bin/env python3
"""Flux across fixed rectangles: source-faithful, finite common-scaling variants.

Normal sampling scales each source vector field by a positive integer 2..5,
expanding both components. Rectangle geometry, response shape, derivative and
iterated-integral stages stay fixed. Banks scale as complete observed banks;
no claim is made about the psychological origin of opaque source distractors.
Easy is unsupported by this bounded package. No database operations here.
"""
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186172101
NAMESPACE=uuid.UUID('f2a418f9-b4da-53b4-a39c-75d28dfa8595')
KP_UUID=str(NAMESPACE)
TITLE='Calculating Flux Across Rectangles'
GENERATOR_UUID=str(uuid.uuid5(NAMESPACE,'question-generator'))
VERSION='rectangle-flux-common-scale-v1'
DIR=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((DIR/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions']}
x,y=sp.symbols('x y',real=True)
E=sp.E
# Complete source formulas and fixed integration rectangles, not inferred from keys.
DATA={
'q-126820':(sp.exp(y)+2*x*x*y,sp.exp(x)+2*x*y*y,(-1,2,0,1)),
'q-126821':(sp.cos(sp.pi*y)-x*x,sp.sin(sp.pi*x)+2*y,(0,1,0,1)),
'q-127303':(sp.sin(y)+2*x,x**5-3*y,(-1,1,-1,1)),
'q-127308':(sp.cos(y)-3*x**3,x*sp.exp(x)-4*x*y**3,(-1,1,0,1)),
'q-127322':(y**sp.Rational(1,3)+x,sp.sin(x)-3*x*x*y*y,(0,2,0,1)),
'q-127324':(sp.sin(2*y)-y*x*x,sp.cos(2*x)+2*x*y,(0,1,-1,0)),
'q-127305':(sp.exp(y)-4*x*y,sp.cos(x)+2*x*y,(-1,1,-1,0)),
'q-127337':(y**7-x,sp.exp(3*x)+x*y*y,(-1,0,-1,1)),
'q-127326':(y*sp.exp(y)-4*x*y,sp.sin(sp.pi*x)-4*x*y**3,(0,1,-1,1)),
'q-127307':(y*y+8*x*y**3,sp.exp(x)+2*y*y,(-1,0,0,1)),
}
SUPPORTED_LEVELS=('moderate','hard')
TEMPLATES={t:q[':question/difficulty'][':db/ident'].split('/')[-1] for t,q in SOURCES.items()}
ORIGINAL={t:{'scale':1} for t in SOURCES}
EXCLUDED={'q-127322':'The cube-root component is not C1 on an open region containing y=0; the source cites the C1 form of Green\'s theorem. Retained for replay only; no generated practice from this profile.'}
SCALES=(2,3,4,5)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(NAMESPACE,v))
def value(v):
    v=v.replace('\\\\','\\').replace(' ','')
    v=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',v)
    v=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',v)
    v=re.sub(r'(?<=\d)(?=sqrt)', '*',v)
    return sp.sympify(v,locals={'e':sp.E,'sqrt':sp.sqrt})
def latex(v):return sp.latex(sp.expand(v))
def mathematical_fingerprint(t,k):
    p,q,b=DATA[t];d=sp.expand(k*(sp.diff(p,x)+sp.diff(q,y)))
    return digest([str(d),list(b)])
def source_template(q):
    for t,s in SOURCES.items():
        if str(q.get(':question/id'))==s[':question/id']:return t
    return None

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty: '+level+'; easy requires separate evidence/design')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only one source radio field is supported')
    rng=random.Random(seed)
    if profile:
        if not profile.startswith('observed:'):raise ValueError('unknown source bank profile')
        selected=profile.split(':',1)[1]
        if template and template!=selected:raise ValueError('profile/template mismatch')
        template=selected
    template=template or rng.choice([t for t in SOURCES if TEMPLATES[t]==level and t not in EXCLUDED])
    if TEMPLATES.get(template)!=level:raise ValueError('difficulty/template mismatch')
    params=copy.deepcopy(parameters) if parameters is not None else {'scale':rng.choice(SCALES)}
    if set(params)!= {'scale'} or type(params['scale']) is not int or params['scale'] not in (1,*SCALES):raise ValueError('scale must be an integer 1..5')
    k=params['scale'];raw=profile is not None
    if template in EXCLUDED and not raw:raise ValueError(EXCLUDED[template])
    s=SOURCES[template];p0,q0,b=DATA[template];p,q=sp.expand(k*p0),sp.expand(k*q0);a,z,c,d=b
    px,qy=sp.diff(p,x),sp.diff(q,y);div=sp.expand(px+qy);inner=sp.integrate(div,(x,a,z));flux=sp.integrate(inner,(y,c,d))
    source_bank=[value(v[':answer/value']) for v in s[':question/answer-fields'][0][':answer-field/choices']]
    bank=[sp.simplify(k*v) for v in source_bank]
    assert len(bank)==5 and all(sp.simplify(v-w)!=0 for i,v in enumerate(bank) for w in bank[:i]) and sum(sp.simplify(v-flux)==0 for v in bank)==1
    if raw:
        if k!=1:raise ValueError('observed replay is at source parameters only')
        problem=s[':question/problem'];solution=s[':question/worked-solution'];values=[a[':answer/value'] for a in s[':question/answer-fields'][0][':answer-field/choices']]
    else:
        problem=re.sub(r'F\(x,y\)=⟨.*?⟩',lambda _:r'F(x,y)=\left\langle '+latex(p)+r',\,'+latex(q)+r'\right\rangle',s[':question/problem'],count=1)
        prefix=s[':question/worked-solution'].split('We have that ')[0]
        solution=prefix+f'We have that $P(x,y)={latex(p)}$ and $Q(x,y)={latex(q)}.$ So,\n\n$$\n'+r'\frac{\partial P}{\partial x}='+latex(px)+r',\qquad\frac{\partial Q}{\partial y}='+latex(qy)+'.\n$$\n\nWe can express the rectangular region $D$ as follows:\n\n$$\n'+rf'D=\{{(x,y):{a}\le x\le {z},\,{c}\le y\le {d}\}}.'+'\n$$\n\nTherefore, applying Green\'s theorem in flux form, we get\n\n$$\n'+r'\begin{aligned}\oint_C F\cdot n\,\mathrm{d}s &=\oint_C P\,\mathrm{d}y-Q\,\mathrm{d}x \\ &=\iint_D\left(\frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}\right)\,\mathrm{d}A \\ &='+rf'\int_{{{c}}}^{{{d}}}\int_{{{a}}}^{{{z}}}\left({latex(div)}\right)\,\mathrm{{d}}x\,\mathrm{{d}}y'+r' \\ &='+rf'\int_{{{c}}}^{{{d}}}\left[{latex(sp.integrate(div,x))}\right]_{{x={a}}}^{{x={z}}}\,\mathrm{{d}}y'+r' \\ &='+rf'\int_{{{c}}}^{{{d}}}\left({latex(inner)}\right)\,\mathrm{{d}}y'+r' \\ &='+rf'\left[{latex(sp.integrate(inner,y))}\right]_{{{c}}}^{{{d}}}'+r' \\ &='+latex(flux)+r'.\end{aligned}'+'\n$$'
        values=[latex(v) for v in bank]
    fp=mathematical_fingerprint(template,k);qid=uid(VERSION+'/'+template+'/'+str(k));fid=uid(qid+'/selection')
    choices=[{':answer/id':uid(fid+'/'+str(i)),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
    idx=next(i for i,v in enumerate(bank) if sp.simplify(v-flux)==0)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[idx][':answer/id']]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]},'generation':{'version':VERSION,'template':template,'bank_profile':'observed:'+template if raw else 'common-scale:'+template,'seed':seed,'parameters':params,'source_basis':SNAPSHOT['basis'],'lineage':SNAPSHOT['lineage'],'source_question':s[':question/id'],'evidence_only':raw,'eligible_for_learning':template not in EXCLUDED and not raw,'mathematical_fingerprint':fp,'plot_rating':'none','fixed_rectangle':list(b),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',default='all',choices=['easy','moderate','hard','all']);a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',default='markdown',choices=['json','markdown']);a.add_argument('--template');v=a.parse_args();levels=SUPPORTED_LEVELS if v.difficulty=='all' else [v.difficulty]
    if v.count<1:a.error('positive count required')
    try:
        records=[]
        for level in levels:
            options=[generate(level,template=t,parameters={'scale':k}) for t in SOURCES if TEMPLATES[t]==level and t not in EXCLUDED and (v.template is None or t==v.template) for k in SCALES]
            if not options:raise ValueError('unsupported difficulty/template')
            random.Random(v.seed).shuffle(options)
            if v.count>len(options):raise ValueError(f'finite-limit: {len(options)} distinct {level} tasks in this bounded package')
            records.extend(options[:v.count])
    except ValueError as e:a.error(str(e))
    print(json.dumps(records,indent=2,ensure_ascii=False) if v.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()

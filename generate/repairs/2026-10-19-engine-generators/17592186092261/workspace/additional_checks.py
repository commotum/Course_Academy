"""Check actual worked-solution final stages and export complete source mapping."""
import json,pathlib,re,subprocess,sys
import sympy as sp
import generator as g
E=pathlib.Path('evidence')
def fixture(expected,tag):
    aid=g.uid([tag,expected]);return {'knowledge_point':g.KP,'question':{':question/id':g.uid(tag),':question/problem':'Check {{field-1}}',':question/answer-fields':[{':answer-field/id':g.uid([tag,'field']),':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':expected}],':answer-field/correct':[':answer/id',aid]}]},'generation':{'template':'solution-stage-equivalence'}}
def rhs(alignment):return alignment.split('\\\\')[-1].split('=',1)[1].strip().rstrip('.')
records=json.load(open(E/'test-records.json'))+json.load(open(E/'source-replay.json'));cases=[]
for i,r in enumerate(records):
    qid=r['generation']['template'];p=g.complete(qid,r['generation']['parameters'])
    # Independent function construction and differentiation, from instance data.
    f=p['c']*sp.Pow(p['b'],p['a']*g.X**p['n']+p['l']*g.X+p['d'])
    derivative=sp.diff(f,g.X);alignments=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',r['question'][':question/worked-solution'],re.S)
    assert alignments,(qid,i)
    stages=[('derivative',g.tex(derivative),rhs(alignments[0]))]
    if 'point' in p:
        t=sp.Rational(p['point']);stages.append(('slope',g.tex(derivative.subs(g.X,t)),rhs(alignments[1])))
        if p.get('equation'):
            tangent=sp.expand(derivative.subs(g.X,t)*(g.X-t)+f.subs(g.X,t))
            stages.append(('tangent equation','y-('+g.tex(tangent)+')','y-('+rhs(alignments[-1])+')'))
    for name,expected,submitted in stages:
        # The native expression checker does not prove ln(4)=2 ln(2).
        # Source hard solutions explicitly simplify that identity; compute the
        # equivalent prime-log form independently before calling the checker.
        if p['b']==4 and r'\ln(2)' in submitted:
            value=derivative.subs(g.X,t) if name=='slope' else tangent
            expected=g.tex(sp.expand_log(value,force=True))
            if name=='tangent equation':expected='y-('+expected+')'
        cases.append({'label':str(i)+' '+qid+' rendered solution '+name,'record':fixture(expected,[i,name]),'checks':[{'submitted':submitted,'expected':'accepted','purpose':'rendered solution stage vs independent calculus'}]})
(E/'solution-grader-input.json').write_text(json.dumps(cases,indent=2))
res=subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(E/'solution-grader-input.json'),str(E/'solution-grading.json')],text=True,capture_output=True)
(E/'solution-grading.log').write_text(res.stdout+res.stderr)
if res.returncode:raise RuntimeError(res.stderr)
mapping=[]
for qid,src in g.SOURCES.items():
    p=g.complete(qid,None)
    for fi,field in enumerate(src.get(':question/answer-fields',[])):
        correct=field.get(':answer-field/correct',{}).get(':answer/id')
        bank=g.original_bank(qid,p,field)
        mapping.append({'source':qid,'field_index':fi,'field_type':field[':answer-field/type'][':db/ident'],'source_key_present':correct is not None,'options':[{'captured_value':s,'mathematical_expression':str(v),'recipe':recipe,'captured_correct':a[':answer/id']==correct if correct else None,'mathematically_correct':sp.simplify(v-g.target(p))==0} for (s,v,recipe),a in zip(bank,field[':answer-field/choices'],strict=True)]})
(E/'source-choice-map.json').write_text(json.dumps(mapping,indent=2,ensure_ascii=False))
print(res.stdout.strip());print('Source choice mapping:',len(mapping),'banks;',sum(len(b['options']) for b in mapping),'options')

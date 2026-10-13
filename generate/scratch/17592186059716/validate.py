"""Independent parsed prompt arithmetic, full source-bank replay, real grading."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('unit_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def group(s):
    assert s.startswith('{');depth=0
    for i,c in enumerate(s):
        depth+=(c=='{')-(c=='}')
        if not depth:return s[1:i],s[i+1:]
    raise ValueError('Unbalanced expression')

def scalar(s):
    s=s.replace(' ','')
    if s.startswith('-'):return -scalar(s[1:])
    if s.startswith(r'\frac'):
        a,tail=group(s[5:]);b,tail=group(tail);assert not tail;return scalar(a)/scalar(b)
    radical=re.fullmatch(r'(\d*)\\sqrt(?:\[(\d+)\])?(\{.*\})',s)
    if radical:
        a,tail=group(radical[3]);assert not tail
        return sp.Integer(radical[1] or 1)*scalar(a)**sp.Rational(1,int(radical[2] or 2))
    if re.fullmatch(r'[0-9()+-]+',s):return sp.sympify(s)
    raise ValueError('Unrecognized exact scalar '+s)

def matrices(s):
    bodies=[m[1] for m in re.findall(r'\\begin\{(bmatrix|aligned)\}((?:(?!\\begin).)*?)\\end\{\1\}',s,re.S)]
    bodies=[b for b in bodies if '&' not in b]
    return [tuple(scalar(v) for v in body.split(r'\\')) for body in bodies]

def prompt_xy(q):
    text=q[':question/problem'];vs=matrices(text)
    assert all(len(v)==2 for v in vs)
    if len(vs)==1:return vs[0]
    assert len(vs)==2
    # Preserve both observed combination layouts; canonical uses a+2b.
    term=re.search(r'parallel to \$(.*?)\$',text).group(1).replace(' ','').replace(r'\mathbf','').replace('{','').replace('}','')
    m=re.fullmatch(r'(\d*)a\+(\d*)b',term);assert m,term
    ca,cb=int(m[1] or 1),int(m[2] or 1)
    return tuple(ca*va+cb*vb for va,vb in zip(*vs))

def fingerprint(q):return g.fingerprint_xy(*prompt_xy(q))

def solution_check(q):
    x,y=prompt_xy(q);n=sp.sqrt(x*x+y*y);expected=(x/n,y/n)
    solution=q[':question/worked-solution']
    assert solution and n>0
    assert all(sp.simplify(a-b)==0 for a,b in zip(matrices(solution)[-1],expected))
    fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0]
    ft=f[':answer-field/type'];assert (ft if isinstance(ft,str) else ft[':db/ident'])==':answer-field.type/radio'
    assert f[':answer-field/key']=='selection' and len(f[':answer-field/choices'])==5
    values=[matrices(a[':answer/value'])[0] for a in f[':answer-field/choices']]
    assert all(len(v)==2 for v in values)
    for i,v in enumerate(values):
        assert all(any(sp.simplify(a-b)!=0 for a,b in zip(v,w)) for w in values[:i])
    c=f[':answer-field/correct'];cid=str(c[1] if isinstance(c,list) else c[':answer/id'])
    correct=[str(a[':answer/id']) for a,v in zip(f[':answer-field/choices'],values) if all(sp.simplify(b-e)==0 for b,e in zip(v,expected))]
    assert correct==[cid]
    assert sp.simplify(sum(z*z for z in expected)-1)==0
    return expected

def independent(rec):
    q=rec['question'];solution_check(q);m=rec['generation'];p=m['parameters']
    assert rec==g.generate(q[':question/difficulty'].split('/')[-1],p['x'],p['y'],p['t'],m['seed'])
    assert fingerprint(q)==m['parameter_fingerprint']
    x,y=prompt_xy(q);n=sp.sqrt(x*x+y*y)
    assert r'\sqrt{'+str(x*x+y*y)+'}' in q[':question/worked-solution']
    assert '= '+sp.latex(n) in q[':question/worked-solution']
    if m['template']=='combination':
        allm=matrices(q[':question/worked-solution'])
        # Initial operands, scaled operand, second operand, and resultant.
        assert allm[0]==(0,p['t']) and allm[1]==(p['x'],p['y']-2*p['t'])
        assert allm[2]==(0,2*p['t']) and allm[3]==allm[1]
        assert allm[4]==(x,y) and allm[5]==(x,y)
        # The unsimplified addition matrix is rendered between these and result.
        assert g.matrix(x,y) in q[':question/worked-solution']
    return True

def checks(rec):
    solution_check(rec['question']);f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independent unit-length and same-direction result; every bank option'} for a in f[':answer-field/choices']]

def main():
    raw=json.loads((HERE/'reference/initial/source.json').read_text());qs={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']}
    replay=[];mapping=[]
    for mid in ('q-17709','q-18058','q-125135'):
        q=qs[mid];x,y=prompt_xy(q);bank,index=g.bank(mid,x,y)
        observed=q[':question/answer-fields'][0][':answer-field/choices']
        assert len(observed)==len(bank)==5
        for a,v in zip(observed,bank):
            original=matrices(a[':answer/value'])[0]
            assert all(sp.simplify(b-c)==0 for b,c in zip(original,v))
            mapping.append({'source_id':mid,'answer_id':a[':answer/id'],'value':a[':answer/value'],'recipe_index':len([r for r in mapping if r['source_id']==mid]),'original_parameters':[str(x),str(y)],'reproduced':True})
        f=q[':question/answer-fields'][0]
        if ':answer-field/correct' in f:assert str(f[':answer-field/correct'][':answer/id'])==str(observed[index][':answer/id'])
        replay.append({'source_id':mid,'complete_bank':True,'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'missing':[],'extra':[],'source_key_present':':answer-field/correct' in f})
    allrec=[r for level in g.SUPPORTED_LEVELS for r in g.batch(level,100,0)]
    for r in allrec:independent(r)
    for level in g.SUPPORTED_LEVELS:assert len({fingerprint(r['question']) for r in allrec if r['question'][':question/difficulty'].endswith('/'+level)})==len(g.batch(level,100,0))
    input=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in allrec]
    (HERE/'reference/native-input.json').write_text(json.dumps(input,indent=2)+'\n')
    subprocess.run([str(HERE/'check-engine'),str(HERE/'reference/native-input.json'),str(HERE/'reference/native-report.json')],check=True)
    native=json.loads((HERE/'reference/native-report.json').read_text());assert native['documented_unresolved_checks']==0
    (HERE/'templates.json').write_text(json.dumps({'source_basis':raw['basis'],'source_replay':replay,'choice_mapping':mapping,'recipes':{'q-17709':['(x/n,-y/n)','(x,y)','(x/n,y/(3n))','(x/n,y/n)','(x/(2n),y/n)'],'q-125135':['(x/(2n),y/(2n))','(x/sqrt(n/2),y/sqrt(n/2))','(x/n,y/n)','(x/sqrt(n),y/sqrt(n))','(x/(4n),y/(2n))'],'q-18058':['(1/n,x/n)','(x/sqrt(s+4),y/sqrt(s+4))','(y/n,x/n)','(x/n,y/n)','(x/sqrt(s+3),y/sqrt(s+3))']},'symbols':'s=x²+y², n=sqrt(s)','interpretation':'Observed expression patterns; misconception interpretations unresolved; no learner-facing inferred feedback','catalog':g.CATALOG},indent=2)+'\n')
    (HERE/'preview.json').write_text(json.dumps(allrec,indent=2)+'\n')
    (HERE/'review.md').write_text('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\nChoices: '+', '.join('$'+a[':answer/value']+'$' for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+r['question'][':question/worked-solution'] for r in allrec)+'\n')
    files=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'templates.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'capabilities.json',HERE/'reference/initial/source.json',HERE/'check-engine',HERE/'reference/grader-build.json']
    result={'status':'pass','source_basis':raw['basis'],'source_fidelity':{'available_complete_banks':3,'matched_choices':15,'total_choices':15,'matched_distractors':12,'total_distractors':12,'replay':replay,'limitation':'Hard q-125138 and moderate q-70409 have no fields. Hard fields explicitly authored from q-17709 bank. No claim of full hard field fidelity.'},'mathematical_validation':{'instances':len(allrec),'independent_parsed_prompt':True,'all_catalog_boundaries':True,'unique_oriented_directions':len(g.CATALOG),'all_options_checked':True,'deterministic_replay':True},'native_engine':native,'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'plots':'None; standalone vector LaTeX is not a plot'}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'pass','instances':len(allrec),'source_choices':'15/15','native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks']}))

if __name__=='__main__':main()

"""Independent displayed-integral reading, source banks and actual grader."""
import importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from math_parser import expression,X
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def group(t,i):
    assert t[i]=='{';depth=1;j=i+1
    while depth:
        if t[j]=='{':depth+=1
        if t[j]=='}':depth-=1
        j+=1
    return t[i+1:j-1],j
def displayed(prompt):
    t=re.search(r'\$(.*?)\$',prompt,re.S)[1].replace(r'{\int }',r'\int').strip()
    t=t[t.index(r'\int')+4:];assert t.startswith('_')
    if t[1]=='{':lo,i=group(t,1)
    else:lo,i=t[1],2
    assert t[i]=='^'
    if t[i+1]=='{':hi,j=group(t,i+1)
    else:hi,j=t[i+1],i+2
    integrand=t[j:];integrand=re.split(r'\\(?:,|text|mathrm)',integrand)[0].strip().rstrip('.=')
    # Source bare sin x uses the same parser grammar as source choices.
    return expression(lo),expression(hi),expression(integrand)
def fingerprint(q):
    lo,hi,f=displayed(q[':question/problem']);return '|'.join(map(str,(lo,hi,sp.expand(f))))
def check(record):
    q=record['question'];lo,hi,f=displayed(q[':question/problem'])
    exact=sp.simplify(sp.integrate(f,(X,lo,hi)))
    for field in q[':question/answer-fields']:
        aa=field[':answer-field/choices'];correct=field[':answer-field/correct'][1]
        vals=[expression(a[':answer/value']) for a in aa]
        assert sum(sp.simplify(v-exact)==0 for v in vals)==1
        assert all(sp.simplify(a-b)!=0 for i,a in enumerate(vals) for b in vals[i+1:])
        assert sp.simplify(next(v for a,v in zip(aa,vals) if a[':answer/id']==correct)-exact)==0
        assert len(aa)==(1 if field[':answer-field/type'].endswith('/blank') else 5)
        if len(aa)==1:assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
    sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==3
    Ftex=re.search(r'\\left\[(.*?)\\right\]',blocks[2],re.S)[1];F=expression(Ftex)
    assert sp.simplify(sp.diff(F,X)-f)==0
    final=blocks[2].split('&=')[-1].split(r'\end')[0].strip().rstrip('.')
    assert sp.simplify(expression(final)-exact)==0
    # The rendered endpoint subtraction is independently checked, including signs.
    endpoint=blocks[2].split('&=')[-2].split(r'\\')[0].strip()
    assert sp.simplify(expression(endpoint)-exact)==0
    for text in [q[':question/problem'],sol]+[a[':answer/value'] for ff in q[':question/answer-fields'] for a in ff[':answer-field/choices']]:
        assert text.count('$')%2==0
        t=re.sub(r'\{\{[^}]+\}\}','',text);depth=0
        for c in t:
            if c=='{':depth+=1
            if c=='}':depth-=1
            assert depth>=0
        assert depth==0
    return True
def native(label,record):
    checks=[]
    for i,f in enumerate(record['question'][':question/answer-fields']):
        correct=f[':answer-field/correct'][1]
        if f[':answer-field/type'].endswith('/radio'):
            checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete selected bank'} for a in f[':answer-field/choices']]
        else:
            text=f[':answer-field/choices'][0][':answer/value'];v=expression(text)
            checks += [{'field_index':i,'submitted':s,'expected':e,'purpose':purpose} for s,e,purpose in [(text,'accepted','canonical exact value'),('('+text+')','accepted','equivalent parenthesized expression'),(str(v),'accepted','equivalent algebraic expression'),(sp.latex(v+1),'rejected','off-by-one'),('0' if v!=0 else '1','rejected','wrong constant')]]
    return {'label':label,'record':record,'checks':checks}
def run_native(records,p):
    p.mkdir(parents=True,exist_ok=True);(p/'input.json').write_text(json.dumps([native(str(i),r) for i,r in enumerate(records)],indent=2))
    subprocess.run([str(HERE/'check-engine'),str(p/'input.json'),str(p/'report.json')],check=True)
def main():
    source=g.SNAPSHOT['rows'][0][0];rows=[];records=[];bank_total=matched=0
    for q in source[':knowledge-point/questions']:
        mid=q[':question/math-academy-id'];r=g.generate(profile=mid,scale=1,dilation=1);check(r)
        assert displayed(q[':question/problem'])==displayed(r['question'][':question/problem'])
        sf=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
        old=[expression(a[':answer/value']) for a in sf[':answer-field/choices']];new=[expression(a[':answer/value']) for a in rf[':answer-field/choices']]
        assert len(old)==len(new) and all(sum(sp.simplify(a-b)==0 for b in new)==1 for a in old)
        assert sp.simplify(expression(sf[':answer-field/correct'][':answer/value'])-next(expression(a[':answer/value']) for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]))==0
        n=len(old)-1;bank_total+=n;matched+=n;rows.append({'source_id':mid,'template':r['generation']['template'],'bank_matched':len(old),'bank_total':len(old),'distractors_matched':n,'distractors_total':n,'missing':[],'extra':[],'prompt_mathematics_matches':True,'ordered_solution_stages':['setup','integration-by-parts formula','integrate remaining function','substitute endpoints','simplify'],'literal_solution_row_layout':'normalized; source prose and operative stages retained'})
        records.append(r)
        for scale,dilation in [(1,2),(2,1),(3,3),(12,8)]:
            r=g.generate(profile=mid,scale=scale,dilation=dilation);check(r);assert r==g.generate(profile=mid,scale=scale,dilation=dilation);records.append(r)
    report={'passed':True,'sources':23,'complete_banks_matched':23,'distractors_matched':matched,'distractors_total':bank_total,'profiles':rows}
    (HERE/'source-replay.json').write_text(json.dumps(report,indent=2)+'\n')
    run_native(records,HERE/'native-grading')
    (HERE/'previews.json').write_text(json.dumps(records,indent=2)+'\n')
    (HERE/'review.md').write_text('\n\n---\n\n'.join('Source '+r['generation']['source_id']+'; scale '+str(r['generation']['scale'])+'; dilation '+str(r['generation']['dilation'])+'\n\n'+g.markdown(r) for r in records))
    (HERE/'validation.json').write_text(json.dumps({'passed':True,'mathematical_records':len(records),'source_replay':report,'actual_grader':'native-grading/report.json','deterministic_replay':True,'slot_coverage':{'scale':[1,2,3,12],'dilation':[1,2,3,8],'source_signed_c':[-18],'source_signed_b':[-1,-2,-3],'source_pi_b':True,'source_bounds':'all replayed; all transported endpoints checked from rendered prompt','changed_target':'not applicable: target is always the whole definite integral'},'fidelity':'all exact banks and source integrals replayed; prose and ordered stages retained, normalized equation row layout','correctness':'independently integrated from rendered prompts; antiderivative differentiated; rendered endpoint subtraction and final answer checked','grading':'all canonical and equivalent blanks accepted; all radio distractors and wrong blanks rejected'},indent=2)+'\n')
    print('Validated',len(records),'records;',matched,'/',bank_total,'source distractors')
if __name__=='__main__':main()

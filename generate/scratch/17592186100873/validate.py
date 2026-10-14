"""Independent rendered matrix-entry, complete-bank and actual-grader validation."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
from math_reader import matrices,target,fingerprint,value
spec=importlib.util.spec_from_file_location('entry',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def audit(rec):
    q=rec['question'];A,B=matrices(q);name,i,j=target(q);ans=int((sp.Matrix(A)*sp.Matrix(B))[i,j]);assert ans==value(q)
    fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];kind=f[':answer-field/type'];assert kind in (':answer-field.type/blank',':answer-field.type/radio')
    vals=[]
    for a in f[':answer-field/choices']:
        n=int(a[':answer/value']);assert (n==ans)==(a[':answer/id']==f[':answer-field/correct'][1]);assert n not in vals;vals.append(n)
    assert len(vals)==(5 if kind.endswith('/radio') else 1)
    if kind.endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    s=q[':question/worked-solution'];m=re.search(r'\$(\d)\$(?:st|nd|rd|th) row (?:in|of) \$([A-Z])\$ by the \$(\d)\$(?:st|nd|rd|th) column (?:in|of) \$([A-Z])[,]?\$',s);assert m,s
    assert (int(m[1])-1,int(m[3])-1)==(i,j)
    assert set(re.findall(r'\{'+name+r'\}_\{(\d)(\d)\}',q[':question/problem']+s))=={(str(i+1),str(j+1))}
    blocks=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)
    parsed=[[[int(x.strip()) for x in r.split('&')] for r in b.split(r'\\')] for b in blocks]
    assert parsed==[A,B,[A[i]],[[r[j]] for r in B]],parsed
    stages=s.split(r'\\  & =');assert len(stages)==5
    # Check expansion and intermediate arithmetic independently from metadata.
    expr=stages[2].strip().replace(r'\cdot','*').replace(')(',')*(')
    expr=re.sub(r'(\d)\(',r'\1*(',expr)
    assert sp.sympify(expr)==ans,(expr,ans)
    nums=[int(x) for x in re.findall(r'[+-]?\d+',stages[3].replace(' ',''))];assert nums==[a*r[j] for a,r in zip(A[i],B)]
    assert re.match(r'\s*'+re.escape(str(ans))+r'\.\\end\{aligned\}',stages[4])
    for text in (q[':question/problem'],s):assert text.count('$')%2==0 and text.count('{')==text.count('}')
    return {'fingerprint':fingerprint(q),'answer':ans}
def engine_checks(rec,label):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete field-owned bank'} for a in f[':answer-field/choices'])
        else:
            n=int(f[':answer-field/choices'][0][':answer/value'])
            checks.extend({'field_index':i,'submitted':s,'expected':e,'purpose':'integer equivalence or wrong integer'} for s,e in [(str(n),'accepted'),(str(n)+'.0','accepted'),(str(n)+'+0','accepted'),(str(n+1),'rejected'),(str(n-1),'rejected')])
    return {'label':label,'record':rec,'checks':checks}
def native(records,path):
    write(path/'native-input.json',[engine_checks(r,str(i)) for i,r in enumerate(records)])
    x=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],text=True,capture_output=True,check=True,timeout=55)
    (path/'native.log').write_text(x.stdout+x.stderr);rep=json.loads((path/'native-report.json').read_text());assert rep['documented_unresolved_checks']==0;return rep

def main():
    records=[];fidelity=[];components=[];coverage={};review=[]
    for mid,t in g.TEMPLATES.items():
        src=g.SOURCE_BY_ID[mid];rep=g.generate('easy',template=mid,replay=True);audit(rep);records.append(rep)
        sf=src[':question/answer-fields'][0];gf=rep['question'][':question/answer-fields'][0];assert rep['question'][':question/problem']==src[':question/problem'] and rep['question'][':question/worked-solution']==src[':question/worked-solution']
        matched=[]
        for a in sf[':answer-field/choices']:
            matches=[z for z in gf[':answer-field/choices'] if int(z[':answer/value'])==int(a[':answer/value'])];assert len(matches)==1
            key=a[':answer/id']==sf[':answer-field/correct'][':answer/id'];assert key==(matches[0][':answer/id']==gf[':answer-field/correct'][1])
            matched.append({'source_answer_id':a[':answer/id'],'exact_value':a[':answer/value'],'recipe':'dot product at requested target' if key else 'fixed observed integer '+a[':answer/value'],'mistake_interpretation':None if key else 'unresolved; no inference or literal variation','complete_value_reproduced':True})
        fidelity.append({'source_id':mid,'complete_bank':True,'matched_options':len(matched),'total_options':len(sf[':answer-field/choices']),'matched_distractors':len(matched)-1,'total_distractors':len(matched)-1,'missing':[],'extra':[],'source_prompt_exact':True,'source_solution_exact':True})
        components.append({'source_id':mid,'source_db_id':src[':db/id'],'field_type':t['field_type'],'profile':t['profile'],'observed_target':target(src)[1:],'matrix_shapes':[(len(M),len(M[0])) for M in matrices(src)],'original':src,'choices':matched,'domain':g.domain(mid)})
        coverage[mid]=[]
        for i,j in g.domain(mid):
            z=g.generate('easy',23,mid,{'row':i,'column':j});audit(z);records.append(z);coverage[mid].append([i,j]);assert z==g.generate('easy',23,mid,{'row':i,'column':j});assert z['question']==g.generate('easy',999,mid,{'row':i,'column':j})['question']
        oi,oj=target(src)[1:];changed=next((p for p in g.domain(mid) if p!=(oi+1,oj+1) and int((sp.Matrix(matrices(src)[0])*sp.Matrix(matrices(src)[1]))[p[0]-1,p[1]-1])!=value(src)))
        variant=g.generate('easy',template=mid,parameters=dict(zip(('row','column'),changed)));review.append({'source_id':mid,'source':src,'variant':variant})
        stale=copy.deepcopy(variant);stale['question'][':question/worked-solution']=src[':question/worked-solution']
        try:audit(stale)
        except AssertionError:pass
        else:raise AssertionError('Failed to catch stale target solution')
        stale=copy.deepcopy(variant);key=stale['question'][':question/answer-fields'][0][':answer-field/correct'][1]
        for a in stale['question'][':question/answer-fields'][0][':answer-field/choices']:
            if a[':answer/id']==key:a[':answer/value']=str(value(src))
        try:audit(stale)
        except AssertionError:pass
        else:raise AssertionError('Failed to catch stale answer')
    canonical=g.SOURCE[':knowledge-point/canonical-example'];assert fingerprint(canonical)==((1,2),(4,-2)) and value(canonical)==0
    rep=native(records,HERE/'reference/validation');write(HERE/'source-components.json',components);write(HERE/'source-fidelity.json',fidelity);write(HERE/'review.json',review)
    (HERE/'review.md').write_text('\n\n---\n\n'.join('Source '+r['source_id']+'\n\n'+r['source'][':question/problem']+'\n\n'+r['source'][':question/worked-solution']+'\n\nChanged target, same matrices\n\n'+g.markdown(r['variant']) for r in review))
    write(HERE/'validation.json',{'status':'passed','source_banks':len(fidelity),'complete_banks_matched':len(fidelity),'matched_options':sum(f['matched_options'] for f in fidelity),'total_options':sum(f['total_options'] for f in fidelity),'matched_distractors':sum(f['matched_distractors'] for f in fidelity),'total_distractors':sum(f['total_distractors'] for f in fidelity),'mathematical_checks':len(records),'distinct_finite_tasks':{'easy':len(g.candidates('easy'))},'slot_coverage':coverage,'all_eligible_cells_exhaustively_checked':True,'changed_target_stale_solution_and_key_caught_each_profile':True,'seed_does_not_create_content':True,'native':rep,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'source_exclusions':g.EXCLUDED})
    print(json.dumps({'source_banks':len(fidelity),'target_cases':len(records),'native_accepted':rep['accepted_checks'],'native_rejected':rep['rejected_checks']}))
if __name__=='__main__':main()

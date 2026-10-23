"""Fresh probes focused on the changed competing-constant answer banks."""
import sys
sys.dont_write_bytecode=True
from review_helpers import *

def probe(records):
    groups={'all':records}
    for r in records:
        groups.setdefault(r['generation']['template'],[]).append(r)
    out=[]
    for label,rs in groups.items():
        for strategy in ['second_smallest','second_largest','smallest','largest','median','unique_smallest_absolute','unique_positive','unique_negative','unique_zero','unique_integer_pair','unique_consistent_pair','first_authored']:
            hits=attempts=0
            for r in rs:
                aa=choices(r); mm=[mats(a[':answer/value'])[0] for a in aa]; yy=[m[1,2] for m in mm]
                if strategy in ['second_smallest','second_largest','smallest','largest','median']:
                    target=sorted(yy)[{'second_smallest':1,'second_largest':-2,'smallest':0,'largest':-1,'median':2}[strategy]]
                    selected=[i for i,v in enumerate(yy) if v==target]
                elif strategy=='unique_smallest_absolute': selected=[i for i,v in enumerate(yy) if abs(v)==min(map(abs,yy))]
                elif strategy=='unique_positive': selected=[i for i,v in enumerate(yy) if v>0]
                elif strategy=='unique_negative': selected=[i for i,v in enumerate(yy) if v<0]
                elif strategy=='unique_zero': selected=[i for i,v in enumerate(yy) if v==0]
                elif strategy=='first_authored': selected=[0]
                else:
                    if 'and then solve' not in r['question'][':question/problem']: continue
                    selected=[]
                    for i,a in enumerate(aa):
                        xy=re.search(r'x=([^$]+)\$ and \$y=([^$]+)',a[':answer/value']);x,y=rat(xy[1]),rat(xy[2])
                        ok=(x.q==1 and y.q==1) if strategy=='unique_integer_pair' else (mm[i][:,:2]*S.Matrix([x,y])==mm[i][:,2])
                        if ok:selected.append(i)
                # Ambiguous strategies abstain; track opportunity separately.
                if len(selected)==1:
                    attempts+=1;hits+=selected[0]==idx(r)
            out.append({'subgroup':label,'strategy':strategy,'correct':hits,'attempted':attempts,'total':len(rs),'baseline':0.2})
    return out

sets={name:json.loads((ROOT/name).read_text()) for name in ['samples.json','batch.json','control.json','delivery-batch/accepted.json','delivery-control/accepted.json']}
save('decision-probe-results.json',{name:probe(rs) for name,rs in sets.items()})
a=g.generate('easy',737837,'q-73544',[1,0]); b=g.generate('easy',737837,'q-73544',[3,1]); c=json.loads(json.dumps(a));field(c)[':answer-field/choices'].reverse()
rs=[a,b,c]
ma,mb=[prompt_matrix(r['question'][':question/problem']) for r in [a,b]]
assert ma[0,:]==mb[0,:] and ma[:,:2]==mb[:,:2] and ma[1,2]!=mb[1,2]
solutions=[m[:,:2].inv()*m[:,2] for m in [ma,mb]]
assert solutions==[S.Matrix([0,-2]),S.Matrix([2,-1])]
assert choices(a)[idx(a)][':answer/value']!=choices(b)[idx(b)][':answer/value']
assert choices(a)[idx(a)][':answer/value']==choices(c)[idx(c)][':answer/value']
extra=g.generate('moderate',737837,'q-20500',[-3,3]);rs.append(extra)
save('focused-counterfactual-records.json',rs)
cases=[]
for i,r in enumerate(rs):
    m=prompt_matrix(r['question'][':question/problem']);xy=m[:,:2].inv()*m[:,2]
    checks=[]
    for aa in choices(r):
        am=mats(aa[':answer/value'])[0]; valid=am[:,:2]*xy==am[:,2]
        match=re.search(r'x=([^$]+)\$ and \$y=([^$]+)',aa[':answer/value'])
        if match:valid=valid and S.Matrix([rat(match[1]),rat(match[2])])==xy
        checks.append({'submitted_answer_id':aa[':answer/id'],'expected':'accepted' if valid else 'rejected','purpose':'Exact equation and full response check for controlled change'})
    cases.append({'label':'focused-counterfactual-'+str(i),'record':r,'checks':checks})
save('focused-native-input.json',cases)
save('focused-counterfactual-results.json',{'seed':737837,'template':'q-73544','parameters':[[1,0],[3,1]],'before_matrix':str(ma),'after_matrix':str(mb),'before_solution':list(solutions[0]),'after_solution':list(solutions[1]),'same_first_equation_and_coefficients':True,'changed_prompt_answer_solution':all(a['question'][k]!=b['question'][k] for k in [':question/problem',':question/worked-solution']) and correct(a)!=correct(b),'irrelevant_order_preserves_content_and_answer':a['question'][':question/problem']==c['question'][':question/problem'] and a['question'][':question/worked-solution']==c['question'][':question/worked-solution'] and correct(a)==correct(c)})
print(json.dumps({'batch_probes':probe(sets['batch.json'])[:11],'focused_counterfactuals':True}))

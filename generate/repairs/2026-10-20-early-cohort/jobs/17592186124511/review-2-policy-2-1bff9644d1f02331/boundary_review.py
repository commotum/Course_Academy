import copy,json,sys
sys.dont_write_bytecode=True
from audit import E,load_generator,save,visible
g=load_generator();rows=json.load(open(E/'samples.json'));results=[]
def reject(label,t,p,expected):
    try:g.generate(template=t,parameters=p)
    except Exception as ex:
        assert expected in str(ex),(label,type(ex).__name__,str(ex))
        results.append({'case':label,'parameters':p,'template':t,'error':str(ex),'expected_error_substring':expected})
    else:raise AssertionError(label)
v=copy.deepcopy(next(r['generation']['parameters'] for r in rows if r['generation']['template']=='q-141199'));v['matrix']=[[0]]*4
reject('zero vector','q-141199',v,'Invalid nonzero independent vector data')
p={'n':5,'matrix':[[1,1]]*5,'claims':[r'\text{dim(Null}(A))=0',r'A\text{ is not invertible}',r'\text{Col}(A)\ne {R}^{5}']}
reject('dependent nullspace','q-142358',p,'Invalid nonzero independent vector data')
p={'n':4,'det':1,'claims':[r'A\text{ is not invertible}',r'\text{Null}(A)\ne \{0\}',r'\text{dim(Null}(A))\ne 0']}
reject('explicit empty checkbox subset','q-141200',p,'No correct selectable option')
for key,value,label,message in [('det',5,'det too large','Determinant outside domain'),('n',2,'dimension too small','Dimension outside domain')]:
    q=copy.deepcopy(p);q[key]=value
    reject(label,'q-141200',q,message)
p={'n':4,'claims':[r'A\text{ is invertible}',r'\text{Col}(A)={R}^{4}',r'\text{dim(Null}(A))=0']}
reject('all-true subset absent from radio bank','q-141201',p,'Subset absent from complete source bank')
# Boundary values with complete records and visible-content checks.
valid=[]
for n in (3,7):
    for det in (-4,0,4):
        p={'n':n,'det':det,'claims':[r'A\text{ is invertible}',r'\text{Null}(A)=\{0\}',r'\text{dim(Null}(A))\ne 0']}
        r=g.generate(template='q-141200',parameters=p);visible(r);valid.append(r)
for t in ('q-141199','q-142358'):
    p=copy.deepcopy(next(r['generation']['parameters'] for r in rows if r['generation']['template']==t))
    p['matrix']=[[4 if v>0 else -4 if v<0 else 0 for v in row] for row in p['matrix']]
    r=g.generate(template=t,parameters=p);visible(r);valid.append(r)
save('boundary-records.json',valid)
identities=[]
for t in g.TEMPLATES:
    p=next(r['generation']['parameters'] for r in rows if r['generation']['template']==t)
    a=g.generate(template=t,parameters=p,seed=99111);b=g.generate(template=t,parameters=p,seed=99112)
    visible(a);visible(b)
    assert a['question'][':question/id']==b['question'][':question/id']
    identities.append({'template':t,'question_id':a['question'][':question/id'],'same_under_seed_choice_order_change':True})
save('boundary-review.json',{'strict_rejections':results,'boundary_valid_records':len(valid),'stable_content_identity':identities,'nonempty_sampling':'Source-backed None gets an explicit true option for empty ordinary masks. Other checkbox templates sample nonempty masks and reject explicit empty masks; tested above.','bounded_resampling':'batch() uses max(200,50*count) deterministic seeded attempts and deduplicates its mathematical fingerprint. Policy retry budget 128 is present but normal construction already supplies nonempty selectable subsets.'})
print('Six targeted rejection cases and eight valid boundary records passed; all 15 profiles preserve content identity across seed changes.')

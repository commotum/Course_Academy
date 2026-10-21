import sys;sys.dont_write_bytecode=True
import pathlib,json,random
from audit_math import verify,tex,field,answer,equal,V
R=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent/'workspace'));import generator as G
def load(n):return json.loads((R/n).read_text())
def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
base=G.instance('R',3,1,4,'x',False,offset=-2,factors=('1/3','3/2'),omitted_row=1,omitted_col=2)
rs=[];results=[];cases=load('grader-input.json')
for name,change,kind in [('reciprocal_exponent',{'n':7},'relevant'),('reciprocal_sign',{'s':-1},'relevant'),('reciprocal_order',{'constant_first':True},'irrelevant')]:
 a=G.build(base,random.Random(7733));b=G.build(dict(base,**change),random.Random(7733));j=len(rs);rs.extend([a,b]);verify(a);verify(b)
 preserved=equal(tex(answer(a)[':answer/value']),tex(answer(b)[':answer/value']));assert preserved==(kind=='irrelevant')
 results.append({'label':name,'kind':kind,'indices':[j,j+1],'delta':change,'before_answer':answer(a)[':answer/value'],'after_answer':answer(b)[':answer/value'],'response_relationship':'preserved' if preserved else 'changed','passes':True})
 for tag,r in [('before',a),('after',b)]:cases.append({'label':name+' '+tag,'record':r,'checks':[{'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if choice[':answer/id']==answer(r)[':answer/id'] else 'rejected','purpose':'controlled R pair complete bank'} for choice in field(r)[':answer-field/choices']]})
save('reciprocal-counterfactual-records.json',rs);save('reciprocal-counterfactual-results.json',results);save('grader-input-complete.json',cases)
(R/'session-state.md').write_text('Completed independent source replay, 835 exact math checks, 618 native grading checks, package CLI/relocation, delivery 720->635 and runner5->5, and visual inspection of all24 actual UI screenshots. Added 3 reciprocal-template controlled pairs to close coverage gap; their native grading/rendering pending. Shortcut and selection script running.\n')

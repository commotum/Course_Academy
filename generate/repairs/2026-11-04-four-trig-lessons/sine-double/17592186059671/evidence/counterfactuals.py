from pathlib import Path
import copy,importlib.util,json,random,sys
HERE=Path(__file__).resolve().parent;PKG=HERE.parent
sys.path.insert(0,str(HERE));sys.path.insert(0,str(PKG))
from numeric_audit import Numeric,nodes,field_key,audit,target
spec=importlib.util.spec_from_file_location('candidate_generator',PKG/'generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def answer(r):return Numeric(nodes(field_key(r['question'][':question/answer-fields'][0])),{}).evaluate()
def check_pair(kind,desc,a,b,relation):
 for i,r in enumerate((a,b)):
  check=audit(r['question'],desc+'/'+str(i),PKG.name)
  assert check['status']=='match' and not check['choice_ambiguities'],check
 av,bv=answer(a),answer(b);assert relation(av,bv),(desc,av,bv)
 return {'kind':kind,'change':desc,'values':[av,bv],'status':'passed','before':a,'after':b}

pairs=[]
if PKG.name=='17592186059671':
 def make(k=2,sign=1,fam='direct',unit='deg',a=17):return g.make('easy' if fam=='direct' else 'moderate',fam,a,unit,k,sign,rng=random.Random(5))
 pairs += [check_pair('relevant','Double the direct-product multiplier; answer doubles',make(),make(k=4),lambda a,b:abs(2*a-b)<1e-9),
           check_pair('relevant','Reverse the square cross-term sign; the answers sum to two',make(k=1,fam='square'),make(k=1,sign=-1,fam='square'),lambda a,b:abs(a+b-2)<1e-9),
           check_pair('irrelevant','Write the same angle in degrees or radians',make(a=17),make(a=g.F(17,180),unit='rad'),lambda a,b:abs(a-b)<1e-9)]
 # Reconstruct complete source structures at their original parameters, without treating missing source fields as defects.
 source_cases=[(17592186341901,'easy','direct',g.F(3,7),'rad',2),(17592186290560,'easy','direct',g.F(1,6),'rad',4),(17592186233278,'moderate','square',g.F(1,6),'rad',1),(17592186253624,'moderate','quotient',g.F(1,10),'rad',2)]
 source={q[':db/id']:q for q in json.loads((PKG/'source-evidence.json').read_text())['imported_practice']}
 witnesses=[]
 for ident,band,fam,a,unit,k in source_cases:
  r=g.make(band,fam,a,unit,k,rng=random.Random(2));row=audit(r['question'],str(ident),PKG.name);assert row['status']=='match' and not row['choice_ambiguities']
  old=Numeric(nodes(target(source[ident])),{}).evaluate();new=answer(r);assert abs(old-new)<1e-8
  witnesses.append({'source':ident,'matched_structure':fam,'numeric_source_target':old,'current_key':new,'record':r,'status':'passed'})
 (HERE/'source-parameter-witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
elif PKG.name=='17592186059672':
 def make(end=30,c=4,unit='degrees',fam='product'):return g.construct('moderate',end,c,unit,fam,rng=random.Random(5))
 pairs += [check_pair('relevant','Double the product coefficient; answer doubles',make(),make(c=8),lambda a,b:abs(2*a-b)<1e-9),
           check_pair('relevant','Move the terminal sine from 30 to 210 degrees; answer changes sign',make(),make(end=210),lambda a,b:abs(a+b)<1e-9),
           check_pair('irrelevant','Change the valid cancellation angle; the coefficient-over-two result remains',make(end=280,fam='cancellation'),make(end=300,fam='cancellation'),lambda a,b:abs(a-b)<1e-9)]
elif PKG.name=='17592186059673':
 def make(role='sin',fam='direct',sign=1,unit='deg',angle=37):return g.make({'family':fam,'role':role,'sign':sign,'k':1,'unit':unit,'angle':angle,'bank_profile':1},'hard' if fam=='complement' else 'easy',random.Random(5))
 pairs += [check_pair('relevant','Exchange the cancellable sine/cosine denominator role; the survivor changes',make(),make(role='cos'),lambda a,b:abs(a-b)>1e-4),
           check_pair('relevant','Change the hard denominator binomial sign; complementary answers sum to four',make(fam='complement'),make(fam='complement',sign=-1),lambda a,b:abs(a+b-4)<1e-9),
           check_pair('irrelevant','Write pi/10 as 18 degrees',make(angle=18),make(angle=10,unit='rad'),lambda a,b:abs(a-b)<1e-9)]
else:
 def make(fam='product',doubled=30,sign=1,unit='degrees'):return g.instance(fam,doubled,unit,k=2,sign=sign,rng=random.Random(5))
 pairs += [check_pair('relevant','Reverse the square cross-term sign; exact values sum to two',make(fam='square'),make(fam='square',sign=-1),lambda a,b:abs(a+b-2)<1e-9),
           check_pair('relevant','Move terminal sine from 30 to 210 degrees; product value changes sign',make(),make(doubled=210),lambda a,b:abs(a+b)<1e-9),
           check_pair('irrelevant','Write the same exact-value problem in degrees or radians',make(),make(unit='radians'),lambda a,b:abs(a-b)<1e-9)]
 # Retain the sign-typo counterexample without modifying the partial imported question.
 minus=g.instance('square',330,'degrees',sign=-1,rng=random.Random(7));plus=g.instance('square',330,'degrees',sign=1,rng=random.Random(7))
 assert abs(answer(minus)-1.5)<1e-9 and abs(answer(plus)-.5)<1e-9
 pairs.append({'kind':'source-error-evidence','source_db_id':17592186233281,'minus_square_value':answer(minus),'plus_square_value':answer(plus),'status':'passed','conclusion':'The original final-line plus sign cannot be copied with the minus-square value 3/2; imported source is unchanged.'})
(HERE/'counterfactuals.json').write_text(json.dumps(pairs,indent=2)+'\n')
print(json.dumps({'kp':PKG.name,'counterfactuals':len(pairs),'status':'passed'}))

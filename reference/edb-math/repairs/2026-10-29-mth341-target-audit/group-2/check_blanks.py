import json,re,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from algebra import matrices,scalar,equations,filled,fill,symbols
S=json.loads((H/'proposed-snapshot.json').read_text());qs={q[':db/id']:q for q in S['questions']};ev=json.loads((H/'layout-evidence.json').read_text())['verified'];out=[]
for row in ev:
 q=qs[row['entity']];bank=filled(q);gs=[sp.Matrix([[scalar(fill(c,bank))for c in rr]for rr in g])for g in row['grids']]
 if len(gs)==1:
  a=matrices(q[':question/problem'])[0]['matrix'];inv=gs[0];ok=a*inv==inv*a==sp.eye(4);detail={'inverse':inv.tolist(),'both_products_identity':ok}
 else:
  rs=equations(q[':question/problem']);x,y=symbols['x'],symbols['y'];a=sp.Matrix([[sp.expand(r).coeff(x),sp.expand(r).coeff(y)]for r in rs]);b=sp.Matrix([-sp.expand(r).subs({x:0,y:0})for r in rs]);used=set(re.findall(r'\{\{([^{}]+)\}\}',str(row['grids'])));factor=scalar(bank[(set(bank)-used).pop()]);inv=factor*gs[0];ok=a*inv==inv*a==sp.eye(2)and gs[1]==b;detail={'factor':factor,'inverse':inv.tolist(),'constant':b.tolist(),'both_products_identity':a*inv==inv*a==sp.eye(2)}
 assert ok,(q[':db/id'],detail);out.append({'question':q[':db/id'],'source_cells_filled_with_preserved_answers':True,'all_field_positions_and_external_factors_verified':True,**detail})
# Named a,b,c blanks use A^-1's first row and the second constant.
for q in S['questions']:
 if 'Find the values of $a'not in q[':question/problem']:continue
 rs=equations(q[':question/problem']);x,y=symbols['x'],symbols['y'];a=sp.Matrix([[sp.expand(r).coeff(x),sp.expand(r).coeff(y)]for r in rs]);b=sp.Matrix([-sp.expand(r).subs({x:0,y:0})for r in rs]);bank=filled(q);v=list(map(scalar,[bank['field-1'],bank['field-2'],bank['field-3']]));expected=[a[1,1],-a[0,1],b[1]];assert v==expected,(q[':db/id'],v,expected);out.append({'question':q[':db/id'],'named_a_b_c_values':v,'adjugate_and_constant_match':True})
(H/'blank-algebra-verification.json').write_text(json.dumps({'passed':True,'checks':out,'database_writes':0},default=str,indent=2)+'\n');print('Verified',len(out),'complete blank questions')

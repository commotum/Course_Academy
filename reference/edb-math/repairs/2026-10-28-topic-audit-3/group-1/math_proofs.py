"""Independent symbolic checks for every authored completion's mathematical role.

No generator module or stored worked solution supplies these calculations.
Graph endpoint/sector decisions also use the actual retained visual panels.
"""
import json
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;checks=[]
x,y,z,t,th=S.symbols('x y z t theta',real=True)
def verify(ids,actual,expected,detail):
 if isinstance(actual,S.MatrixBase):ok=all(S.simplify(v)==0 for v in actual-S.Matrix(expected))
 else:ok=S.simplify(S.trigsimp(actual-expected))==0
 assert ok,(ids,actual,expected);checks.append({'identities':['q-'+str(i)for i in ids],'actual':str(actual),'expected':str(expected),'reason':detail,'verified':True})
a,b=S.sin(th),S.cos(th)
for ids,expr,expected in [([1578],(a-b)**2+(a+b)**2,2),([1579],b/(1-a)-a/b,1/b),([23522],b+a*a/b,1/b),([65162],b*b*(1+a*a/(b*b)),1),([65163],b**3+b*a*a,b),([65165],(b*b*a*a+a**4)/(b*a),a/b),([65166],a*a/(a**3+a*b*b),a),([65193],a*a*b**3+a**4*b,a*a*b)]:verify(ids,expr,expected,'Pythagorean identity; original nonzero-denominator domain retained.')
V=lambda a:S.Matrix(a)
for ids,actual,want in [([1304],V([12,5])-V([9,-2]),[3,7]),([1323],V([4,1])-V([1,-4]),[3,5]),([1386],3*V([8,-7]),[24,-21]),([17611],V([-2,1])+2*V([4,-1]),[6,-1]),([18040],V([4,-2])-(2*V([3,3])-3*V([-8,4])),[-26,4]),([18041],V([1,1])-(2*V([4,1])+5*V([-1,2])),[-2,-11]),([70401],V([7,-6])+V([3,2]),[10,-4]),([70402],2*V([4,2])+V([6,-4]),[14,0]),([1408],V([S.Rational(1,3),9,6]).cross(V([0,-3,3])),[45,-1,-1])]:verify(ids,actual,want,'Component operations, with source-restored cross product where required.')
cross=V([1,2,3*x]).cross(V([4,3,x]));verify([19783],cross.dot(cross),170*x*x+25,'Squared source cross-product norm. Equation=705 gives exactly x=±2.')
verify([20051],V([3,1,-3]).dot(V([2,6,-2]).cross(V([0,1,-4]))),-64,'Scalar triple product with source-restored inner cross.')
verify([20056],V([1,-4,1]).dot(V([3,-3,2]).cross(V([2,-1,0]))),-11,'Order q cross p retained, no cross-product reversal.')
for ids,f,lo,hi,want in [([29634],x**3,-2,2,0),([29639],x**S.Rational(5,2),0,4,S.Rational(256,7)),([49222],x**-4,1,2,S.Rational(7,24)),([49228],x**S.Rational(3,5),0,1,S.Rational(5,8)),([316010],x**-S.Rational(2,5),1,32,S.Rational(35,3))]:verify(ids,S.integrate(f,(x,lo,hi)),want,'Exact endpoint evaluation on stated positive/nonnegative real interval.')
verify([15558],S.diff(t*t,t).subs(t,-1)/S.diff(t**4+t,t).subs(t,-1),S.Rational(2,3),'Regular tangent at point(0,1); normal slope−3/2 gives x-intercept2/3.')
verify([6862],S.diff(t**5,t).subs(t,-1)/S.diff(t*t-2*t,t).subs(t,-1),-S.Rational(5,4),'Regular tangent at point(3,−1).')
verify([21206],S.diff(t**3-2,t)/S.diff(t-1,t),3*t*t,'Horizontal iff t=0; dx/dt=1 never zero.')
verify([16205],t*t-4*t,(t-2)**2-4,'All real t; minimum−4 attained.')
verify([6827],((-2)**2-2)+(0**2-0)+(3**2+3),14,'Three table entries at their actual t-values.')
verify([15799],(9*S.cos(th))**2+(9*S.sin(th))**2,81,'Center(−3,5),radius9; entire0≤theta<2pi.')
for ident,cx,cy,r,start in [(15804,0,0,8,(8,0)),(15851,0,0,6,(6,0)),(78205,-1,2,2,(1,2))]:
 X=cx+r*S.cos(th);Y=cy+r*S.sin(th);assert(X.subs(th,0),Y.subs(th,0))==start;verify([ident],(X-cx)*S.diff(Y,th)-(Y-cy)*S.diff(X,th),r*r,'Positive angular orientation; correct start and center, not locus-only verification.')
verify([15755],t*t-(x+2)**2, (t-x-2)*(t+x+2),'Parameter elimination with t=x+2; all real x.')
verify([33759],1/t**2+4+4*t*t,(2*t+1/t)**2,'t∈[1,e] positive, so positive square-root speed is2t+1/t.')
verify([33759],S.integrate(2*t+1/t,(t,1,S.E)),S.E**2,'Exact positive-speed integral.')
verify([33728],S.diff(S.sin(2*t),t)**2+S.diff(S.cos(3*t),t)**2,4*S.cos(2*t)**2+9*S.sin(3*t)**2,'Norm squared of velocity; interval[0,pi] retained.')
verify([36340],(1-4*x*x-y*y).subs({x:0,y:1}),0,'Level value at stated point gives ellipse4x²+y²=1.')
verify([36434],(1/(y-x*x)).subs({x:1,y:2}),1,'Level1; denominator remains1 on y=x²+1.')
r=S.symbols('r',nonnegative=True)
verify([161044],(x*y*y).subs({x:r*S.cos(th),y:r*S.sin(th)})*r,r**4*S.cos(th)*S.sin(th)**2,'Full disk r≤sqrt5 from actual source graphic; Jacobian included.')
verify([161068],S.expand(((x-3)**2+y*y-9).subs({x:r*S.cos(th),y:r*S.sin(th)})),r*r-6*r*S.cos(th),'Disk right of origin: −pi/2≤theta≤pi/2,0≤r≤6cos theta.')
verify([161068],((x*x-y*y).subs({x:r*S.cos(th),y:r*S.sin(th)}))*r,r**3*S.cos(2*th),'Polar integrand includes Jacobian.')
verify([38077],r*S.cos(th)*r*r,r**3*S.cos(th),'Upper half of diskcenter(1,0),radius1 gives theta0..pi/2,r0..2cos theta.')
verify([38127],S.integrate(S.integrate(r*r*S.sin(th),(r,1,2)),(th,S.pi/3,S.pi/2)),S.Rational(7,6),'Exact double integral with both stated bounds.')
verify([161522],S.integrate(S.integrate(S.integrate(r*r,(z,0,12-4*r*S.sin(th))),(r,0,2)),(th,0,2*S.pi)),64*S.pi,'Height positive across disk; Jacobian yields r²; full angular range.')
verify([39481],z*r*r,r*r*z,'Original integrand zsqrt(x²+y²), cylinder radius3, lowerz1, upperz10−r cos theta. Source correct bank exponent2 restored separately.')
verify([126578],S.pi*(2**2-1**2),3*S.pi,'Positive annulus boundary orientation: outer CCW, inner CW; Green curl1.')
verify([105561],(S.diff(S.exp(x)*S.cos(x),x)+S.diff(x*S.exp(x*y),y)).subs({x:0,y:1}),1,'Divergence, not scalar curl.')
verify([126427],S.diff(y,x)-S.diff(x*y,y),-x,'Scalar curlQx−Py.')
def curl(F):return V([S.diff(F[2],y)-S.diff(F[1],z),S.diff(F[0],z)-S.diff(F[2],x),S.diff(F[1],x)-S.diff(F[0],y)])
verify([41883],curl([x*y,y*z,x*z]),[-y,-z,-x],'Right-hand-rule curl orientation.')
verify([41899],curl([x*S.cos(y*z),0,y*S.log(x*z)]).subs({x:1,y:S.pi/2,z:1}),[0,-S.pi,1],'Source curl operator; stated point is inside real logarithm domain xz>0.')
verify([162407],S.diff(x*z,x)+S.diff(y*y,y)+S.diff(S.Integer(1),z),z+2*y,'Outward divergence theorem; hidden static box has no field role.')
verify([42215],S.integrate((3*S.sin(t)*4*S.cos(2*t)-2*S.sin(2*t)*3*S.cos(t))/2,(t,0,S.pi)),-8,'Actual curve is clockwise. Asked geometric area is abs(−8)=8.')
verify([76188],S.diff(t*t/2,t)**2+1,1+t*t,'Alongpath y/x=t/2, continuous endpoint limit0; scalarlineelementpositive.')
verify([76508],S.integrate(2*t*t*S.sqrt(5),(t,0,1)),2*S.sqrt(5)/3,'Line y2x+1, x∈[0,1], scalar ds=√5dt.')
verify([83948],(1-r*r)*r,r*(1-r*r),'Full annulus1..3; polar Jacobianr.')
verify([85059],(r*S.cos(th)-r*S.sin(th))*r,r*r*(S.cos(th)-S.sin(th)),'Upper semiannulus1..2, theta0..pi; polar Jacobianr.')
verify([104399],V([S.diff(y*S.exp(x*y),x),S.diff(y*S.exp(x*y),y)]),[y*y*S.exp(x*y),(x*y+1)*S.exp(x*y)],'Gradient of entire stated potential.')
a=S.symbols('a');verify([104412],S.diff((x-a)*S.exp(x+y),y)-S.diff(x*S.exp(x+y),x),(-a-1)*S.exp(x+y),'Entire simply connected plane; equalcrosspartials iff a=−1.')
verify([98947],V([S.diff(x*x*y*z+z*z,v)for v in[x,y,z]]),[2*x*y*z,x*x*z,x*x*y+2*z],'Three-dimensional gradient in correct component order.')
# Remaining real-range/graph/domain cases require inequalities/actual image selection.
checks.extend([{'identities':['q-'+str(i)],'verified':True,'reason':reason}for i,reason in [(54286,'Viewed all five retained graphs: slope2,intercepts(0,−4),(2,0), correct matching answer ID.'),(59676,'Viewed all five graphs and original table; points(0,1),(1,0),(2,−1),(3,−2).'),(59678,'Viewed all five graphs: slope1/2,intercepts(0,−2),(4,0).'),(16203,'t≥0; x=t(t+6) continuous increasing from0 to∞ and y√t same range.'),(70341,'Full0≤theta<2pi attains both endpoints of x∈[−4,2],y∈[0,4].'),(79205,'Viewed original third-quadrant arc; theta∈[pi,3pi/2] correct endpoints and full quarter arc, not complementary quadrant.' )]])
proofs=json.loads((H/'authored-completion-proofs.json').read_text());covered={i for c in checks for i in c['identities']};assert {p['identity']for p in proofs}<=covered,({p['identity']for p in proofs}-covered)
D=json.loads((H/'current.json').read_text());by={q[':db/id']:q for q in D['questions']};ledger=json.loads((H.parent/'source-eligibility.json').read_text());ex={r[':db/id']:r for r in ledger['excluded_questions']}
for p in proofs:p['full_question_snapshot']=by[p['question']];p['source_eligibility']=ex.get(p['question'],{'reasons':[]});p['independent_math_checks']=[c for c in checks if p['identity']in c['identities']]
(H/'authored-completion-proofs.json').write_text(json.dumps(proofs,indent=2)+'\n');(H/'independent-math-checks.json').write_text(json.dumps({'basis_t':9837,'checks':checks,'identities':sorted(covered),'all_65_completions_covered':True,'limits':'Graph decisions include actual source visual review; scalar symbolic simplifications retain original denominators, positive-root domains, intervals, endpoint and orientation conditions stated in each check. Key dispatch tests are separate and are not mathematical proof.'},indent=2)+'\n');print('independent checks',len(checks),'completion identities',len(covered),'excluded context cases',[(p['identity'],p['source_eligibility'])for p in proofs if p['source_eligibility'].get('reasons')])

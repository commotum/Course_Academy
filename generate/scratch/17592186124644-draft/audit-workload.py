"""Read actual displayed function, point and bank; independently audit arithmetic.

No generation parameters or computed arithmetic metadata are trusted. Recover
active/held factors from the two printed summands and differentiate them afresh.
"""
import sys
sys.dont_write_bytecode=True
import sympy as S
import texmath as tm
u,v=tm.SYMBOLS['u'],tm.SYMBOLS['v']
HEIGHTS={'tan-reciprocal':(9,4),'base-exponential-tan':(6,4),'sin-cos-linear':(3,1),'power-log-root':(9,4),'exp-log-power':(4,2),'polynomial':(24,1),'sec-power':(8,1),'root-reciprocal':(32,4),'cross-roots':(24,4),'cos-log-sin':(6,2),'cot-polynomial':(3,1),'log-power-exp':(30,1),'easy-polynomial':(16,1)}
def height(expression):
    parts=[z.as_coeff_Mul(rational=True)[0] for z in S.Add.make_args(S.expand_mul(expression))]
    return max(abs(int(z.p)) for z in parts),max(int(z.q) for z in parts)
def audit(q,key):
    fun,t,point=tm.prompt(q[':question/problem']);held=tm.SYMBOLS['y' if str(t)=='x' else 'x']
    U,V=point[t],point[held];role=fun.xreplace({t:u,held:v});terms=role.as_ordered_terms();assert len(terms)==2
    def first(term):
        if key=='tan-reciprocal':return term.has(S.tan(u))
        if key=='base-exponential-tan':return term.has(2**u)
        if key=='sin-cos-linear':return term.has(S.sin(u))
        if key=='power-log-root':return term.has(S.log(v))
        if key in ('exp-log-power','cos-log-sin','log-power-exp'):return term.has(S.log(u))
        if key in ('polynomial','cross-roots'):return term.as_powers_dict().get(u,0)==1
        if key=='sec-power':return term.has(S.sec(u))
        if key=='root-reciprocal':return term.as_powers_dict().get(u,0)>1
        if key=='cot-polynomial':return term.has(S.cot(u))
        if key=='easy-polynomial':return term.as_powers_dict().get(u,0)==2
        raise AssertionError(key)
    chosen=[z for z in terms if first(z)];assert len(chosen)==1;one=chosen[0];two=next(z for z in terms if z!=one)
    sign=-1 if key in ('sin-cos-linear','power-log-root','polynomial','cross-roots','cos-log-sin','cot-polynomial','log-power-exp') else 1
    h1,g1=one.as_independent(u,as_Add=False);h2,g2=(sign*two).as_independent(u,as_Add=False)
    if key in ('power-log-root','root-reciprocal'):N=g1.as_powers_dict()[u]
    elif key in ('polynomial','log-power-exp'):N=g2.as_powers_dict()[u]
    elif key=='base-exponential-tan':N=-g2.as_powers_dict()[u]
    elif key in ('exp-log-power','sec-power'):N=h2.as_powers_dict()[v]
    elif key=='cot-polynomial':N=h1.as_powers_dict()[v]
    else:N=S.Integer(2)
    M=h2.as_powers_dict()[v] if key=='cot-polynomial' else S.Integer(2)
    ah={'tan-reciprocal':v**2,'base-exponential-tan':S.tan(v),'sin-cos-linear':S.cos(v),'power-log-root':S.log(v),'exp-log-power':S.exp(v),'polynomial':v**2,'sec-power':v,'root-reciprocal':S.sqrt(v),'cross-roots':S.sqrt(v),'cos-log-sin':S.cos(v),'cot-polynomial':v**N,'log-power-exp':v,'easy-polynomial':v**2}[key]
    bh={'tan-reciprocal':v,'base-exponential-tan':v/S.pi,'sin-cos-linear':v,'power-log-root':v,'exp-log-power':v**N,'polynomial':v,'sec-power':v**N,'root-reciprocal':v,'cross-roots':v,'cos-log-sin':v,'cot-polynomial':v**M,'log-power-exp':S.exp(v),'easy-polynomial':v}[key]
    A,B=S.simplify(h1/ah),S.simplify(h2/bh);assert all(z.is_Integer and 1<=z<=4 for z in (A,B))
    d1=S.diff(g1,u);d2=S.diff(g2,u);T1=S.expand_mul((h1*d1).subs({u:U,v:V}));T2=S.expand_mul((sign*h2*d2).subs({u:U,v:V}));C=S.expand_mul(T1+T2)
    metrics={}
    def cap(name,value,limit):
        value=S.simplify(abs(value));assert value<=limit,(key,name,value,limit);metrics[name]=str(value)
    def frac(name,value,num,den):
        nn,dd=height(value);assert nn<=num and dd<=den,(key,name,value,nn,dd,num,den);metrics[name+'_numerator']=nn;metrics[name+'_denominator']=dd
    if key=='tan-reciprocal':
        cap('held_square',V**2,9);cap('term1',T1,9);cap('active_pi_square',(U/S.pi)**2,4);cap('reciprocal_numerator',B*V,8);cap('reciprocal_coefficient',T2*S.pi**2,4)
    elif key=='base-exponential-tan':
        cap('base_power',2**U,2);cap('reciprocal_power',U**(N+1),1);cap('log_coefficient',T1/S.log(2),6);cap('reciprocal_derivative_factor',N,3);cap('term2',T2,3);frac('term2',T2,6,4)
    elif key=='sin-cos-linear':cap('term1',T1,3);cap('pi_term2',T2/S.pi,3)
    elif key=='power-log-root':
        cap('active_power',U**(N-1),4);cap('power_derivative_factor',d1.subs(u,U),8);cap('log_value',S.log(V),2);cap('term1',T1,9);cap('sqrt_derivative_denominator',1/d2.subs(u,U),4);cap('root_coefficient',T2/V,2)
    elif key=='exp-log-power':
        cap('held_power',V**N,4);cap('term2',T2,4);cap('reciprocal_factor',d1.subs(u,U),2);cap('exp_coefficient',T1/S.exp(V),4);frac('exp_coefficient',T1/S.exp(V),4,2)
    elif key=='polynomial':
        cap('active_power',U**(N-1),2);cap('held_square',V**2,4);cap('derivative_factor',B*d2.subs(u,U),4);cap('term1',T1,16);cap('term2',T2,8);cap('term_arithmetic',abs(T1)+abs(T2),24)
    elif key=='sec-power':cap('held_power',V**N,4);cap('term1',T1,6);cap('term2',T2,4);cap('bank_maximum',abs(T1)+abs(T2),8)
    elif key=='root-reciprocal':
        cap('derivative_factor',d1.subs(u,U),4);cap('held_root',h1.subs(v,V),4);cap('reciprocal_numerator',h2.subs(v,V),8);cap('reciprocal_square',U**2,4);cap('term1',T1,12);cap('term2',T2,4);cap('bank_maximum',abs(T1)+abs(T2),12);frac('key',C,24,4)
    elif key=='cross-roots':
        cap('sqrt_active',S.sqrt(U),2);cap('sqrt_held',S.sqrt(V),2);cap('held_factor',h2.subs(v,V),16);cap('sqrt_derivative_denominator',1/d2.subs(u,U),4);cap('term1',T1,8);cap('term2',T2,8);cap('bank_maximum',abs(T1)+abs(T2),12);frac('key',C,24,4)
    elif key=='cos-log-sin':cap('reciprocal_pi_coefficient',T1*S.pi,6);cap('held_pi_coefficient',h2.subs(v,V)/S.pi,4);cap('term2_pi_coefficient',T2/S.pi,2)
    elif key=='cot-polynomial':cap('held_power1',V**N,1);cap('held_power2',V**M,1);cap('derivative_pi_coefficient',d2.subs(u,U)/S.pi,3);cap('term1',T1,3);cap('term2_pi_coefficient',T2/S.pi,3)
    elif key=='log-power-exp':
        cap('active_power',U**(N-1),1);cap('log_coefficient',A/U,4);cap('held_exp_factor',h2.subs(v,V),6);cap('derivative_prefactor',B*d2.subs(u,U),10);cap('term2_product',T2,30)
    elif key=='easy-polynomial':
        cap('held_square',V**2,4);cap('held_factor',h1.subs(v,V),4);cap('derivative_factor',d1.subs(u,U),6);cap('term1',T1,12);cap('term2',T2,4);cap('sum',abs(T1)+abs(T2),16)
    nh,dh=HEIGHTS[key]
    for index,answer in enumerate(q[':question/answer-fields'][0][':answer-field/choices']):frac('option'+str(index),tm.parse(answer[':answer/value']),nh,dh)
    reduced=S.expand(S.simplify(role.subs(v,V)),log=True,force=True)
    return metrics,{'role_function':S.srepr(role),'restricted_function':S.srepr(reduced),'active_coordinate':S.srepr(U)}

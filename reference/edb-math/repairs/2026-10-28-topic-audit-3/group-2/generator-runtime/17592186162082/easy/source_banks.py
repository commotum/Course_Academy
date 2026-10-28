"""Parameterized historical complete banks, used only by evidence replay."""
import sympy as s
from generator import tex
PROFILES={"q-122481":"semi","q-122843":"three_quarter","q-122828":"three_segments","q-122845":"two_segments","q-122850":"quarter_open"}
def bank(profile,t,p,L):
 r=p.get('r'); A=sum(L)
 if profile=='q-122481':return [(r*(s.pi+1),'radius_instead_diameter'),(2*r*(s.pi+2),'double_total'),(A,'correct'),(r*(2*s.pi+1),'compound_2pi_radius'),(2*r*(s.pi+1),'compound_2pi_diameter')]
 if profile=='q-122843':return [(2*r*s.pi+r/2,'empirical_4pi_1'),(A,'correct'),(3*r*s.pi/2+2*r,'double_segment'),(r*s.pi+3*r/2,'empirical_2pi_3'),(r*s.pi/2+r,'quarter_arc')]
 if profile=='q-122484':return [(r*s.pi/4+r*s.sqrt(3)/2,'empirical_pi4_sqrt3half'),(A,'correct'),(r*s.pi/2+r*s.sqrt(2)/2,'half_chord'),(r*s.pi/4+r*s.sqrt(2)/2,'half_both'),(r*s.pi+3*r*s.sqrt(2)/2,'empirical_pi_3sqrt2half')]
 if profile=='q-122828':
  a,b=p['a'],p['b'];return [(3*a,'three_vertical'),(3*b,'three_horizontal'),(A,'correct'),(2*b,'two_horizontal'),(2*L[1],'double_diagonal')]
 if profile=='q-122845':
  a,b,h=p['a'],p['b'],p['h'];return [(a+b+h,'add_coordinate_legs'),(h+L[1],'height_plus_second'),(2*a+L[1],'double_left_plus_second'),(A,'correct'),(2*L[0],'double_first')]
 if profile=='q-122850':return [(3*r*s.pi/16+r*s.sqrt(2)/4,'empirical_3pi16_sqrt2quarter'),(r*s.pi+r*s.sqrt(2)/2,'empirical_pi_halfchord'),(r*s.pi/16+r*s.sqrt(2)/4,'empirical_pi16_sqrt2quarter'),(r*s.pi/2+3*r*s.sqrt(2)/4,'three_quarter_chord'),(A,'correct')]
 # Complete authored bank chosen before any parameter sampling. No pooled fallback.
 if profile=='authored_arc':return [(A,'correct'),(L[0],'omit_segment'),(L[1],'omit_arc'),(2*L[0]+L[1],'double_arc'),(L[0]+2*L[1],'double_segment')]
 return [(A,'correct'),(L[0],'omit_rest'),(sum(L[1:]),'omit_first'),(2*L[0]+sum(L[1:]),'double_first'),(L[0]+2*sum(L[1:]),'double_rest')]
def compact_tex(x):return tex(x).replace(' ','')
def pi_term(c,unicode=False):
 c=s.Rational(c);pi='π' if unicode else r'\pi'
 if c==1:return pi
 if c.q!=1:return r'\frac{'+(str(c.p) if c.p!=1 else '')+pi+'}{'+str(c.q)+'}'
 return str(c)+pi

def radical_term(c,n):
 c=s.Rational(c);return ('' if c==1 else compact_tex(c))+r'\sqrt{'+str(n)+'}'

def raw_bank_values(qid,p,L):
 """Complete parameterized expression masks retaining observed factor/order/spacing."""
 r=p.get('r');A=sum(L)
 if qid=='q-122481':return [compact_tex(r)+r'(\pi +1)',compact_tex(2*r)+r'(\pi +2)',compact_tex(r)+r'(\pi +2)',compact_tex(r)+r'(2\pi +1)',compact_tex(2*r)+r'(\pi +1)']
 if qid=='q-122843':return [pi_term(2*r)+' +'+compact_tex(r/2),pi_term(3*r/2)+' +'+compact_tex(r),pi_term(3*r/2)+' +'+compact_tex(2*r),pi_term(r)+' +'+compact_tex(3*r/2),pi_term(r/2)+' +'+compact_tex(r)]
 if qid=='q-122484':return [pi_term(r/4,True)+' + '+radical_term(r/2,3),pi_term(r/2,True)+' + '+radical_term(r,2),pi_term(r/2,True)+' + '+radical_term(r/2,2),pi_term(r/4,True)+' + '+radical_term(r/2,2),pi_term(r,True)+' + '+radical_term(3*r/2,2)]
 if qid=='q-122828':return [compact_tex(x) for x,_ in bank(qid,PROFILES[qid],p,L)]
 if qid=='q-122845':
  coefficient,radical=s.expand(L[1]).as_coeff_Mul()
  def factor_mask(first):
   common=s.gcd(first,coefficient);return compact_tex(common)+'('+compact_tex(first/common)+'+'+compact_tex(L[1]/common)+')'
  return [compact_tex(p['a']+p['b']+p['h']),factor_mask(p['h']),factor_mask(2*p['a']),compact_tex(L[0])+'+'+compact_tex(L[1]),compact_tex(2*L[0])]
 if qid=='q-122850':return [r'\frac{'+pi_term(3*r/4)+' +'+radical_term(r,2)+'}{4}',compact_tex(r/2)+r'(2\pi +\sqrt{2})',r'\frac{'+pi_term(r/4)+' +'+radical_term(r,2)+'}{4}',pi_term(r/2)+' +'+radical_term(3*r/4,2),compact_tex(r/2)+r'(\pi +2\sqrt{2})']
 raise ValueError('Unknown raw bank')


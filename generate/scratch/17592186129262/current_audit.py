"""Read displayed current source math; preserve invalid source records unchanged."""
import copy,hashlib,json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate as v
g=v.g;s=v.sp

def scalar(text):return v.scalar(text.replace(r'\dfrac',r'\frac').replace(r'\qquad',''))
def mathtext(m):return m.group(1) if m.group(1) is not None else m.group(2)
def equations(q):
    text=mathtext(list(g.MATH.finditer(q[':question/problem']))[-1]).strip()
    pieces=re.split(r',\s*(?:\\,|\\qquad)?\s*',text)
    assert len(pieces)==4,(text,pieces)
    return [scalar(a)-scalar(b) for a,b in (piece.split('=') for piece in pieces)]
def fingerprint(q):
    out=[]
    for e in equations(q):
        n=s.factor(s.together(e).as_numer_denom()[0]);factors=s.Mul.make_args(n)
        # First-quadrant monomials and exponentials are nonzero, hence removable.
        if 'first quadrant' in q[':question/problem']:
            factors=[z for z in factors if z not in [g.X,g.Y] and z.func!=s.exp]
        n=s.expand(s.Mul(*factors));n=n.as_content_primitive()[1]
        try:n=s.Poly(n,g.X,g.Y).monic().as_expr()
        except s.PolynomialError:
            if n.could_extract_minus_sign():n=-n
        out.append(s.srepr(n))
    return hashlib.sha256(json.dumps(sorted(out)).encode()).hexdigest()

def source_math(q):
    blocks=[mathtext(m).strip() for m in g.MATH.finditer(q.get(':question/worked-solution',''))]
    assert len(blocks)==34,'missing or unfamiliar worked solution'
    substitutions=blocks[11].split(r',\,');f,h=[scalar(z.split('=')[1]) for z in substitutions]
    bounds=list(map(int,re.findall(r'(-?\d+)\\le [uv]\\le (-?\d+)',blocks[22])[0]+re.findall(r'(-?\d+)\\le [uv]\\le (-?\d+)',blocks[22])[1]));a,b,c,d=bounds
    assert a<b and c<d
    for e,trans,value in zip(equations(q),[f,f,h,h],bounds):
        ratio=s.simplify(e/(trans-value))
        assert ratio!=0 and s.simplify(ratio).is_zero is not True
        # The boundary equation differs only by a nonzero constant or denominator.
        assert all(z.is_nonzero is True for z in s.together(ratio).as_numer_denom()),(e,trans,value,ratio)
    for i,var,expected in [(18,'u',[a,b]),(20,'v',[c,d])]:
        assert list(map(int,re.findall(var+r'=(-?\d+)',blocks[i])))==expected,('wrong transformed boundary',q[':question/math-academy-id'])
    det=s.det(s.Matrix([[s.diff(f,g.X),s.diff(f,g.Y)],[s.diff(h,g.X),s.diff(h,g.Y)]]))
    printed=scalar(blocks[25].rsplit(' & =',1)[1].split(r'\end{aligned}')[0].rstrip('.'))
    assert v.equal(printed.subs({g.U:f,g.V:h}),det)
    matrices=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',blocks[25],re.S)
    if not matrices:matrices=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',blocks[25],re.S)
    assert len(matrices)==2
    entries=[z.strip() for row in matrices[1].split(r'\\') for z in row.split('&')]
    assert all(v.equal(scalar(z),value) for z,value in zip(entries,[s.diff(f,g.X),s.diff(f,g.Y),s.diff(h,g.X),s.diff(h,g.Y)]))
    inverse=scalar(blocks[28].split('=')[-1].rstrip('.'));assert v.equal(inverse.subs({g.U:f,g.V:h}),1/det)
    area=s.integrate(s.Abs(inverse),(g.U,a,b),(g.V,c,d))
    final=blocks[33];ib=re.findall(r'\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}',final);assert ib==[(str(a),str(b)),(str(c),str(d))]
    assert v.equal(scalar(final.split(' & =')[-2]),area)
    assert v.equal(scalar(final.rsplit(' & =',1)[1].split(r'\end{aligned}')[0]),area)
    fields=q[':question/answer-fields'];assert len(fields)==1
    field=fields[0];values=[scalar(z[':answer/value']) for z in field[':answer-field/choices']];assert len(values)==5
    assert all(not v.equal(x,y) for i,x in enumerate(values) for y in values[i+1:])
    correct=[z[':answer/id'] for z,value in zip(field[':answer-field/choices'],values) if v.equal(value,area)]
    assert correct==[field[':answer-field/correct'][':answer/id']]
    # Exponential source has y=v/2, x=ln(2u/v), hence first quadrant requires 2a>d.
    if f.has(s.exp(g.X)):assert 2*a>d and c>0
    return {'area':str(area),'bounds':bounds,'u':str(f),'v':str(h),'determinant':str(det),'choices_checked':len(values),'fingerprint':fingerprint(q)}

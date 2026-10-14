"""Parent reads supplied lines, point cues, equation stages, banks and native PNGs."""
import hashlib, importlib.util, itertools, json, re, sys
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as s

sys.dont_write_bytecode = True
R = Path(__file__).resolve().parent
K = 17592186175922
D = R.parents[2] / f'generate/scratch/{K}'
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
P = load(R / 'ode-scalar-parser.py', 'perpline_scalar')
G = load(D.with_suffix('.py'), 'perpline_generator')
F = load(R / 'root-source-fidelity.py', 'perpline_source')
originals, fidelity = F.check(G, K, D)
X, Y = P.x, P.y
def scalar(t): return P.scalar(t.strip().rstrip('.,'))
def equation(t):
    t = t.replace('&', '').strip().rstrip('.,')
    a, b = t.split('='); return s.expand(scalar(a) - scalar(b))
def canonical(z):
    assert s.diff(z, Y) != 0 and not s.diff(z, Y).free_symbols
    return s.expand(z / s.diff(z, Y))
def same(a,b): return s.simplify(a-b) == 0
C = dict(records=0, given_equations=0, actual_point_cues=0, actual_slope_prose=0,
         complete_equation_rows=0, actual_conclusions=0, choice_values=0,
         criterion_pairs=0, native_curve_probes=0, marked_points=0, native_label_boxes=0,
         zero_axes=0, actual_guide_probes=0)
records = json.load(open(R / f'qa/{K}-sampled.json'))
for row in json.load(open(D / 'review.json')):
    r = row.get('record', row)
    if 'question' in r and not r['generation'].get('evidence_only', False): records.append(r)
for r in records:
    q, meta = r['question'], r['generation']; prompt = q[':question/problem']; template = meta['template']
    spans = re.findall(r'\$([^$]+)\$', prompt)
    given = next(t for t in spans if re.match(r'y\s*=', t) and len(t.replace(' ',''))>2 and 'mx+b' not in t)
    line = canonical(equation(given)); A = -line.coeff(X); B = -line.subs({X:0,Y:0}); C['given_equations'] += 1
    if template.startswith('graph'):
        path = Path(meta['plots']['prompt']); side = json.load(open(meta['plots']['sidecar']))
        # Actual Matplotlib label strings, not the question's generation operands.
        texts = [item['text'] for item in side['text_boxes'] if item['text']]
        assert texts[:2] == ['$x$','$y$']
        if template.startswith('graph_intercept'): U, V = s.Integer(0), scalar(texts[2][1:-1])
        else: U, V = scalar(texts[2][1:-1]), scalar(texts[3][1:-1])
        im = np.asarray(Image.open(path).convert('RGB')); H,W = im.shape[:2]
        origin = side['origin_pixel']; scale = side['unit_pixels']; assert scale>=7
        red = (im[:,:,0]>150)&(im[:,:,1]<140)&(im[:,:,2]<140)
        blue = (im[:,:,2]>150)&(im[:,:,0]<140)&(im[:,:,1]<140)
        black = im.max(2)<100; gray = (im.max(2)-im.min(2)<15)&(im.mean(2)>60)&(im.mean(2)<210)
        def pixel(a,b): return int(round(origin[0]+float(a)*scale)), int(round(H-origin[1]-float(b)*scale))
        def near(a,b,color):
            x,y=pixel(a,b); return 4<x<W-4 and 4<y<H-4 and color[y-3:y+4,x-3:x+4].any()
        M=-1/A; intercept=V-M*U
        assert near(U,V,red); C['marked_points']+=1
        lo,hi=side['bounds']
        for slope,offset,color in [(A,B,blue),(M,intercept,red)]:
            count=0
            for t in np.linspace(lo+.8,hi-.8,49):
                yy=float(slope)*t+float(offset)
                if lo+.8<yy<hi-.8: assert near(t,yy,color); count+=1
            assert count>=4; C['native_curve_probes']+=count
        for text in side['text_boxes']:
            if not text['text']: continue
            x,y,w,h=text['bbox']; assert 0<=x<x+w<=W and 0<=y<y+h<=H
            assert im[max(0,int(H-y-h)):int(H-y)+1,int(x):int(x+w)+1].min()<180
            if text['text'] in ('$l_1$','$l_2$'):
                assert not x-4<=origin[0]<=x+w+4,('Line glyph overlaps vertical zero axis',path)
                assert not y-4<=origin[1]<=y+h+4,('Line glyph overlaps horizontal zero axis',path)
            C['native_label_boxes']+=1
        for axis in (0,1):
            hit=0
            for t in np.linspace(lo+.6,hi-.6,50): hit+=near(t,0,black) if axis==0 else near(0,t,black)
            assert hit>=35; C['zero_axes']+=1
        if U!=0:
            # Dashed reading guides need visible segments, not continuous strokes.
            for horizontal in (True,False):
                hits=sum(near(float(U)*f,V,gray) if horizontal else near(U,float(V)*f,gray) for f in np.linspace(.15,.85,15))
                assert hits>=4; C['actual_guide_probes']+=hits
        assert s.Rational(side['a'])==A and s.Rational(side['c'])==B and s.Rational(side['u'])==U and s.Rational(side['v'])==V
    else:
        point=re.search(r'\((-?\d+),(-?\d+)\)',prompt);assert point;U,V=map(s.Integer,point.groups()); M=-1/A;intercept=V-M*U
    C['actual_point_cues']+=1
    expected=Y-M*X-intercept; sol=q[':question/worked-solution']
    slope=re.search(r'must have a slope of \$([^$]+)\.\$',sol); assert slope and same(scalar(slope[1]),M); C['actual_slope_prose']+=1
    slope2=re.search(r'\$m=([^$]+)\$',sol);assert slope2 and same(scalar(slope2[1]),M)
    if template.startswith('graph_intercept'):
        stated=re.search(r'intercept of \$([^$]+)\.\$',sol);assert stated and same(scalar(stated[1]),intercept)
    else:
        stated=re.search(r'\)=(\(-?\d+,-?\d+\))',sol); assert stated and stated[1]==f'({U},{V})'
    block=sol.split('$$')[1].strip()
    if r'\begin{aligned}' in block:
        rows=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2)
        assert len(rows)==(5 if U<0 else 4)
        assert rows[0].strip()==r'y-{y}_{1} & =m(x-{x}_{1})'
        for row in rows:
            row=row.replace('{y}_{1}','('+s.latex(V)+')').replace('{x}_{1}','('+s.latex(U)+')').replace('m(', '('+s.latex(M)+')(')
            assert same(canonical(equation(row)),expected),('Wrong complete displayed equation',row)
            C['complete_equation_rows']+=1
    else: assert same(canonical(equation(block)),expected); C['complete_equation_rows']+=1
    if template.startswith('intercept'):
        final=re.search(r'Therefore, \$b=([^$]+)\.\$',sol);assert final and same(scalar(final[1]),intercept);C['actual_conclusions']+=1
    for field in q[':question/answer-fields']:
        values=[]
        for a in field[':answer-field/choices']:
            value=scalar(a[':answer/value']) if '=' not in a[':answer/value'] else canonical(equation(a[':answer/value']))
            target=intercept if template.startswith('intercept') else (M*X+intercept if field[':answer-field/type'].endswith('/blank') else expected)
            assert same(value,target)==(a[':answer/id']==field[':answer-field/correct'][1]);values.append(value);C['choice_values']+=1
        for a,b in itertools.combinations(values,2):assert not same(a,b);C['criterion_pairs']+=1
    C['records']+=1
result=dict(status='passed',source=fidelity,readback={k:int(v) for k,v in C.items()},original_assets_full_resolution=4,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0)
(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

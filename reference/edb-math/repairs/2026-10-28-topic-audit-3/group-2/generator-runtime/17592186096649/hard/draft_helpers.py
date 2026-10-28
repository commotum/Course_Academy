import hashlib,json,math,uuid
import sympy as sp

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(obj):return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(obj)))
def tex(x):return sp.latex(sp.Rational(x)).replace("- ","-")
def scalar(x):
 x=sp.Rational(x)
 return ('-' if x==-1 else '' if x==1 else tex(x))+ 'a'
def exact_vec(p):
 a=sp.pi*p['angle']/180;n=sp.Rational(p['length'])
 return (sp.simplify(n*sp.cos(a)),sp.simplify(n*sp.sin(a)))

def plot_spec(vectors,labels,allvectors):
 # Shared viewport and unit scale for prompt and EVERY choice. Translation is incidental.
 base=allvectors[0][0];norm=math.hypot(float(base[0]),float(base[1]));normal=(-float(base[1])/norm,float(base[0])/norm)
 paired=[(1.6*normal[0],1.6*normal[1]),(-1.6*normal[0],-1.6*normal[1])]
 lanes=paired if len(vectors)==2 else [(0,0)]
 tails=[(lane[0]-float(v[0])/2,lane[1]-float(v[1])/2) for lane,v in zip(lanes,vectors)]
 points=[(0,0)]
 for row in allvectors:
  lanes=paired if len(row)==2 else [(0,0)]
  ts=[(lane[0]-float(v[0])/2,lane[1]-float(v[1])/2) for lane,v in zip(lanes,row)]
  for t,v in zip(ts,row):points.extend([t,(t[0]+float(v[0]),t[1]+float(v[1]))])
 xs=[x for x,y in points];ys=[y for x,y in points];cx=(min(xs)+max(xs))/2;cy=(min(ys)+max(ys))/2
 extent=max(max(xs)-min(xs),max(ys)-min(ys))+2.0
 # Large separation of paired labels; no backgrounds/masks are used.
 return {'renderer_version':'compact-7','bounds':[[cx-extent/2,cx+extent/2],[cy-extent/2,cy+extent/2]],'label_offset':0.7,'vectors':[{'tail':list(t),'vector':[float(x) for x in v],'label':label,'color':('black' if label=='a' else '#2c72ae' if i==0 else '#e69f00')} for i,(t,v,label) in enumerate(zip(tails,vectors,labels))]}


def solution(p,images):
 s=[sp.Rational(x) for x in p['scales']];parts=[]
 if len(s)==2:parts.append('First, notice that both $'+scalar(s[0])+'$ and $'+scalar(s[1])+'$ must be parallel to $a$.')
 else:parts.append('First, notice that $'+scalar(s[0])+'$ must be parallel to $a$.')
 for i,k in enumerate(s):
  parts.append(('Now' if i==0 else 'Next')+', for the vector $'+scalar(k)+'$ we have the following:\n\n- The magnitude of $'+scalar(k)+'$ is $'+tex(abs(k))+'$ times the magnitude of $a$.\n- Vectors $a$ and $'+scalar(k)+'$ have '+('the same direction' if k>0 else 'opposite directions')+' since the factor $'+tex(k)+'$ is '+('positive' if k>0 else 'negative')+'.')
 parts.append('The required vectors are shown below.\n\n![]('+images[0]+')')
 return '\n\n'.join(parts)


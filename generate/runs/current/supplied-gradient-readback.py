"""Root derives supplied-gradient chain derivative from actual printed inputs."""
import importlib.util,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('root_supplied_chain',P/'vector-chain-readback.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
x,y,z,t=p.x,p.y,p.z,p.t

def given(prompt):
 spans=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S);gr=[];curves=[];points=[]
 for span in spans:
  span=p.clean(span)
  if re.match(r'∇[fgh]\(x,\s*y\)\s*=',span):gr.append((span[1],p.vector(span.split('=',1)[1])))
  if re.match(r'[rpq]\(t\)\s*=',span):curves.append((span[0],p.vector(span.split('=',1)[1])))
  if re.match(r't\s*=',span):points.append(p.scalar(span.split('=',1)[1]))
 assert len(gr)==len(curves)==len(points)==1
 name,G=gr[0];cn,R=curves[0];assert G[2]==R[2]==0 and p.equal(s.diff(G[0],y),s.diff(G[1],x));at=points[0];assert at.is_real is True
 composed=G.subs(dict(zip((x,y,z),R)),simultaneous=True);rd=R.diff(t);answer=composed.dot(rd);evaluated=answer.subs(t,at)
 assert not evaluated.has(s.zoo,s.nan,s.oo,-s.oo)
 return dict(name=name,curve_name=cn,G=G,R=R,composed=composed,derivative=rd,answer=answer,point=at,evaluated=evaluated)

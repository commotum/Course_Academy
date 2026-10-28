import json,re,sys,collections
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells
s=(R/'reference/edb-math/repairs/2026-10-27-lesson-1171/audit_math.py').read_text();helper=s[s.index('def scalar(s):'):s.index('def grids(t):')];helper=helper.replace("s=s.replace('⁡','')","s=re.sub(r'\\\\text\\{\\s*\\}','',s);s=re.sub(r'\\\\hspace\\{[^{}]*\\}', '',s);s=re.sub(r'([xyzkuv])_\\{(\\d+)\\}',r'\\1\\2',s);s=s.replace('⁡','')");helper=helper.replace("assert all(n in {'pi','e','E','sqrt','log','a','b','c','d'}or re.fullmatch(r'a\\d+',n)for n in names),s","assert all(re.fullmatch(r'[A-Za-z]+\\d*',n)for n in names),s").replace("if n.startswith('a')or n in {'b','c','d'}","if n not in {'pi','e','E','sqrt','log'}");exec(helper)
P=json.loads((H/'proposals.json').read_text());pm={(p['entity'],p['attribute']):p['after']for p in P};F=json.loads((H/'fields.json').read_text());out=[];flags=[]
for e,a,v,ident,bare in F:
 if a not in ['tutorial/content','question/worked-solution']:continue
 v=pm.get((e,a),v);mats=[];errors=[]
 for m in ENV.finditer(v):
  if m.groups()!=('begin','array'):continue
  span=environment(v,m.start())
  if not span:continue
  body=v[span[0]:span[1]];col=re.match(r'\{([^{}]*\|[^{}]*)\}',body)
  if not col:continue
  body=body[col.end():];body=re.sub(r'(?<=\\\\)\[[^\]]*\]','',body);gs=cells(body)
  try:M=S.Matrix([[scalar(c)for c in row]for row in gs]);rr=M.rref()[0];mats.append({'start':m.start(),'shape':list(M.shape),'matrix':str(M),'rref':str(rr),'tex':v[m.start():span[2]]})
  except Exception as ex:errors.append({'start':m.start(),'error':str(ex),'tex':v[m.start():span[2]]})
 for x,y in zip(mats,mats[1:]):
  if x['shape']==y['shape']and x['rref']!=y['rref']:flags.append({'entity':e,'attribute':a,'identity':ident,'before_matrix':x,'after_matrix':y,'between':v[x['start']:y['start']]})
 if mats or errors:out.append({'entity':e,'attribute':a,'identity':ident,'matrices':mats,'parse_errors':errors})
(H/'row-math.json').write_text(json.dumps(out,indent=2)+'\n');(H/'row-math-candidates.json').write_text(json.dumps(flags,indent=2)+'\n');print('fields',len(out),'matrices',sum(len(o['matrices'])for o in out),'parse errors',sum(len(o['parse_errors'])for o in out),'unequal consecutive rrefs',len(flags))
for f in flags:print(f['entity'],f['identity'],f['before_matrix']['matrix'],'=>',f['after_matrix']['matrix'])

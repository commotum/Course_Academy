from pathlib import Path
exec(open(Path(__file__).with_name('math.py')).read().split("if __name__")[0])
def maths(s):return re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',s,re.S)
def cleaned(s):
 s=deriv_text(s);s=re.sub(r'\\(?:begin|end)\{(?:aligned|cases)\}','',s);s=s.replace('&','').replace(r'\left\{','').replace(r'\right.','');s=s.replace('\\\x27',"'");s=re.sub(r'\\(?:bbox|boxed)(?:\[[^]]*\])?\{(.*)\}',r'\1',s)
 return s
reports=[]
for d in base.glob('175*'):
 rows=[]
 for q in json.loads((d/'questions.json').read_text()):
  prob=q[':question/problem'];sol=q.get(':question/worked-solution','');row={'eid':q[':db/id'],'mid':q[':question/math-academy-id'],'checks':[]}
  if not sol:row['missing_solution']=True;rows.append(row);continue
  try:ode=extract_ode(q)
  except:rows.append(row);continue
  var=t if 'y(t)'in prob or re.search(r't\^|\{t\}|t>',prob)else x
  coeff=[S.expand(ode).coeff(k)for k in [Ypp,Yp,Y]]
  poly=S.expand(coeff[0]/(var**2 if var in coeff[0].free_symbols else 1)*(L*(L-1)if var in coeff[0].free_symbols else L**2)+coeff[1]/(var if var in coeff[1].free_symbols else 1)*L+coeff[2]);roots=S.solve(poly,L)
  gs=[]
  for pair in maths(sol+"\n"+prob):
   for st in re.split(r'\\\\',cleaned(next(v for v in pair if v))):
    m=re.search(r'^\s*y(?:\([xt]\))?\s*=\s*(.+)',st)
    if m:
     try:
      v=tex(m[1].split('=')[0]);syms=v.free_symbols &{A,B,P,Q,C,D}
      if len(syms)==2 and L not in v.free_symbols:gs.append(v)
     except:pass
  if not gs:row['trial_only']=True
  gen=gs[0]if gs else (var**L if var in coeff[0].free_symbols else S.exp(L*var));row['general']=str(gen);row['general_residual']=str(S.simplify(sum(c*S.diff(gen,var,n)for c,n in zip(coeff,[2,1,0]))))
  params=gen.free_symbols &{A,B,P,Q,C,D};ic=[]
  prompt=re.sub(r'\{y\}\^\{′\}|y\^\{′\}|y\x27','YP',prob.replace(r'\left','').replace(r'\right',''))
  for m in re.finditer(r'(YP|y)\s*\(([^()]*(?:\{[^{}]*\}[^()]*)?)\)\s*=\s*([^,\n$]+)',prompt):
   try:arg=tex(m[2]);val=tex(re.split(r'\\(?:quad|qquad|,)|,',m[3])[0]);ic.append(S.diff(gen,var,int(m[1]=='YP')).subs(var,arg)-val)
   except:pass
  constants=S.solve(ic,list(params))if ic and params else {};row['constants']={str(k):str(v)for k,v in constants.items()};yexpr=gen.subs(constants)
  for pair in maths(sol):
   block=cleaned(next(v for v in pair if v))
   for st in re.split(r'\\\\|\\qquad|\\quad|\\,',block):
    st=st.strip().strip('.,');st=re.sub(r'\\(?:text|textrm)\{[^{}]*\}','',st)
    if '='not in st or any(z in st for z in [r'\ne',r'\Rightarrow','⇒',r'\pm',r'\overline','⟹']):continue
    parts=st.split('=')
    for aa,bb in zip(parts,parts[1:]):
     check={'equation':aa+'='+bb}
     try:
      # Evaluate y and derivatives at numeric arguments independently.
      def calls(ss):
       ss=ss.replace(r'\left','').replace(r'\right','')
       ss=re.sub(r'\{y\}\^\{′\}|y\^\{′\}|y\x27','UP',ss)
       ss=re.sub(r'\{y\}\^\{″\}|y\^\{″\}|y\x27\x27','VP',ss)
       def at(m):
        order={'y':0,'UP':1,'VP':2}[m[1]];arg=tex(m[2]);exp=S.diff(yexpr,var,order).subs(var,arg);return '('+S.sstr(exp)+')'
       # Symbolic x/t is a full function evaluation, numeric arguments are IC values.
       ss=re.sub(r'(UP|VP|y)\s*\(([^()]*)\)',at,ss);ss=ss.replace('UP',"y'").replace('VP',"y''")
       return ss
      va,vb=tex(calls(aa)),tex(calls(bb));delta=va-vb
      active=yexpr
      if L in delta.free_symbols and any(k in delta.free_symbols for k in [Y,Yp,Ypp]):active=var**L if var in coeff[0].free_symbols else S.exp(L*var)
      delta=delta.subs({Y:active,Yp:S.diff(active,var),Ypp:S.diff(active,var,2)}).subs(constants)
      checks=[S.simplify(delta.subs(L,r))for r in roots]if L in delta.free_symbols else [S.simplify(delta)]
      check['passed']=any(z==0 for z in checks);check['residuals']=list(map(str,checks))
     except Exception as e:check['parse_error']=str(e)
     row['checks'].append(check)
  rows.append(row)
 (d/'solution-chains.json').write_text(json.dumps(rows,indent=2))
 print(d.name,'general residual failures',[(r['mid'],r.get('general_residual'))for r in rows if r.get('general_residual','0')!='0'],'FAILED EQUATIONS',[(r['mid'],c)for r in rows for c in r.get('checks',[])if c.get('passed')is False])

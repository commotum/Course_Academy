"""Independent small TeX expression reader for the actual displayed source dialect.
No generation metadata is consulted. Derivative labels are handled by validator.
"""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

def read(s):
    s=s.replace('\\\\','\\').replace(r'\u2061','').replace('⁡','').replace('\u2061','')
    s=re.sub(r'\\operatorname\{(\w+)\}',r'\\\1',s)
    s=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}',r'\\\1',s)
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','').replace(' ', '').rstrip('.,')
    def grp(s,i):
        if i>=len(s):raise ValueError('Missing group in '+s)
        if s[i] in '{(':
            close='}' if s[i]=='{' else ')';n=1;j=i+1
            while j<len(s):
                if s[j]==s[i]:n+=1
                elif s[j]==close:
                    n-=1
                    if n==0:return s[i+1:j],j+1
                j+=1
            raise ValueError('Unbalanced '+s)
        return s[i],i+1
    def conv(s):
        out='';i=0
        while i<len(s):
            ch=s[i]
            if ch=='\\':
                m=re.match(r'\\(dfrac|frac|sqrt|sin|cos|tan|cot|sec|csc|ln|log|exp)',s[i:]);cmd=m[1];i+=len(m[0])
                if out and (out[-1].isalnum() or out[-1]==')'):out+='*'
                if cmd in ('frac','dfrac'):
                    a,i=grp(s,i);b,i=grp(s,i);out+='(('+conv(a)+')/('+conv(b)+'))'
                elif cmd=='sqrt':
                    a,i=grp(s,i);out+='sqrt('+conv(a)+')'
                elif cmd in ('sin','cos','tan','cot','sec','csc','ln','log','exp'):
                    power=''
                    if i<len(s) and s[i]=='^':a,i=grp(s,i+1);power='**('+conv(a)+')'
                    if i<len(s) and s[i] in '{(':a,i=grp(s,i)
                    else:
                        j=i
                        while i<len(s) and s[i] not in '+-*/\\,)':
                            if s[i] in '{(':_,i=grp(s,i)
                            else:i+=1
                        a=s[j:i]
                    if not a:raise ValueError('Missing trig argument '+s)
                    out+=('log' if cmd=='ln' else cmd)+'('+conv(a)+')'+power
                else:raise ValueError('Unsupported command '+cmd+' in '+s)
            elif ch in '{(':
                a,i=grp(s,i);out+='('+conv(a)+')'
            elif ch=='^':a,i=grp(s,i+1);out+='**('+conv(a)+')'
            else:out+=ch;i+=1
        return out
    loc={z:sp.Symbol(z,positive=True) for z in ['x','y','t','s','u']};loc.update({z:getattr(sp,z) for z in ('sin','cos','tan','cot','sec','csc','log','exp','sqrt')});loc['e']=sp.E
    return parse_expr(conv(s),local_dict=loc,transformations=standard_transformations+(convert_xor,implicit_multiplication_application))

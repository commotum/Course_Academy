"""Independently check printed prompts, keys and every authored display step."""
import re
import sympy as sp
from read import *
V={c:sp.Symbol(c,positive=True)for c in 'xyzpq'};V['e']=sp.E

def scalar(text):
 text=text.strip()
 while r'\frac'in text or r'\dfrac'in text:
  m=re.search(r'\\d?frac\{',text);start=m.start();pos=m.end()-1;parts=[]
  for _ in range(2):
   assert text[pos]=='{';depth=1;j=pos+1
   while depth:
    if text[j]=='{':depth+=1
    elif text[j]=='}':depth-=1
    j+=1
   parts.append(text[pos+1:j-1]);pos=j
  replacement='('+str(scalar(parts[0]))+')/('+str(scalar(parts[1]))+')';text=text[:start]+replacement+text[pos:]
 text=text.replace(r'\cdot','*').replace('^','**').replace('{','(').replace('}',')')
 return sp.sympify(text,locals=V)

def expr(text):
 text=text.strip().strip('.').strip();atoms={};pattern=re.compile(r'\\(ln|log)(?:_\{([^}]+)\})?\\left\(')
 while m:=pattern.search(text):
  end=text.index(r'\right)',m.end());inner=text[m.end():end];base=sp.E if m[1]=='ln'else scalar(m[2]or'10');name='L'+str(len(atoms));atoms[name]=sp.log(scalar(inner))/sp.log(base);text=text[:m.start()]+name+text[end+7:]
 return sp.sympify(text,locals={**V,**atoms})
def eq(a,b):return sp.simplify(sp.expand_log(a-b,force=True))==0
if __name__=='__main__':
 records=json.loads((HERE/'grading-records.json').read_text());questions=0;steps=0;distractors=0
 for rec in records:
  if rec.get('generation',{}).get('source_index')is not None:continue
  q=rec['question'];math=next(t for t in re.findall(r'\$(.*?)\$',q[':question/problem'],re.S)if '\\ln'in t or '\\log'in t)
  if math.endswith('='):math=math[:-1]
  target=expr(math);f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'];aid=correct.get(':answer/id')if isinstance(correct,dict)else correct[1]
  for answer in f[':answer-field/choices']:
   is_correct=str(answer[':answer/id'])==str(aid);assert eq(expr(answer[':answer/value']),target)==is_correct,(q[':question/id'],answer[':answer/value']);distractors+=not is_correct
  for display in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
   display=re.sub(r'\\(?:begin|end)\{aligned\}','',display).replace('&','')
   for line in display.split(r'\\'):
    for piece in line.split('='):
     piece=piece.strip().strip('.').strip()
     if piece:assert eq(expr(piece),target),(q[':question/id'],piece);steps+=1
  questions+=1
 save('algebra-verification.json',{'passed':True,'questions':questions,'printed_steps_checked':steps,'independently_rejected_distractors':distractors,'method':'Independent SymPy expressions parsed from printed prompts, answers and solution displays; logarithms expanded over positive variables'})
 print((HERE/'algebra-verification.json').read_text())

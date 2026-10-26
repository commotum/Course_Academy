import copy,hashlib,json,math,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import dumps,kw
from question_capture.math_format import normalize_math_boundaries,validate_prose
qs=json.loads((H/'questions.json').read_text());original=copy.deepcopy(qs);byid={q[':db/id']:q for q in qs};fields=[];forms=[];links=[]
def change(e,a,old,new):
 if old==new:return
 fields.append({'entity':e,'attribute':a,'before':old,'after':new,'before_sha256':hashlib.sha256((old or'').encode()).hexdigest(),'after_sha256':hashlib.sha256(new.encode()).hexdigest()});forms.append([kw('db/cas'),e,kw(a),old,new])
for q in qs:
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:
   old=a[':answer/value'];new=normalize_math_boundaries(old)
   if new!=old:
    assert re.fullmatch(r'\$\$\d+(?:\.\d+)?\$(?: per gallon)?',old);assert re.findall(r'\d+(?:\.\d+)?',old)==re.findall(r'\d+(?:\.\d+)?',new);validate_prose(new);change(a[':db/id'],'answer/value',old,new);a[':answer/value']=new
  if f.get(':answer-field/correct'):
   f[':answer-field/correct']=next(a for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id'])
q=byid[17592186059595];old=q[':question/worked-solution'];needle=r'&= P_{0} \mid \approx 9899';assert old.count(needle)==1;new=old.replace(needle,r'P_{0} &\approx 9899');change(q[':db/id'],'question/worked-solution',old,new);q[':question/worked-solution']=new
opening='The continuously compounded growth equation is $P=P_0e^{rt}$. '
solutions={
17592186060056:opening+r'''Here $P_0=102$, $P=10$, and $r=-0.095$ per year. Solve for $t$:

$$
\begin{aligned}
10 &= 102e^{-0.095t} \\
e^{-0.095t} &= \frac{10}{102} \\
-0.095t &= \ln\left(\frac{10}{102}\right) \\
t &= \frac{\ln(10/102)}{-0.095} \\
&\approx 24.4462.
\end{aligned}
$$

Rounding to the nearest integer gives $24$ years.''',
17592186060057:opening+r'''Here $P_0=10$, $P=781$, and $t=14$ minutes. Solve for $r$:

$$
\begin{aligned}
781 &= 10e^{14r} \\
e^{14r} &= \frac{781}{10} \\
14r &= \ln\left(\frac{781}{10}\right) \\
r &= \frac{\ln(781/10)}{14} \\
&\approx 0.311285.
\end{aligned}
$$

The percentage rate is approximately $31.1285\%$ per minute. Rounding to the nearest percent gives $31\%$ per minute.''',
17592186060058:opening+r'''Here $P_0=4120$, $r=-0.0381$ per year, and $t=2016-2009=7$ years. Substitute:

$$
\begin{aligned}
P &= 4120e^{(-0.0381)(7)} \\
&= 4120e^{-0.2667} \\
&\approx 3155.5196.
\end{aligned}
$$

Rounding to the nearest integer gives approximately $3156$ crimes in $2016$.''',
17592186060059:opening+r'''Here $P_0=9830$ and $r=-0.18$ per day. Convert $2$ weeks to $t=14$ days, then substitute:

$$
\begin{aligned}
P &= 9830e^{(-0.18)(14)} \\
&= 9830e^{-2.52} \\
&\approx 790.9179.
\end{aligned}
$$

Rounding to the nearest integer gives approximately $791$ people.''',
17592186060238:opening+r'''Here $P=16700$, $r=0.15$ per year, and $t=5$ years. Solve for the earlier profit $P_0$:

$$
\begin{aligned}
16700 &= P_0e^{(0.15)(5)} \\
P_0 &= \frac{16700}{e^{0.75}} \\
&\approx 7888.5214.
\end{aligned}
$$

Rounding to the nearest dollar, the profit five years ago was $\$7889$.''',
17592186060389:opening+r'''Here $P=3.11$, $r=-0.01$ per month, and $t=5$ months. Solve for the earlier gas price $P_0$:

$$
\begin{aligned}
3.11 &= P_0e^{(-0.01)(5)} \\
P_0 &= \frac{3.11}{e^{-0.05}} \\
&\approx 3.269453.
\end{aligned}
$$

Rounding to the nearest cent, the earlier price was $\$3.27$ per gallon.'''}
correct={17592186060056:17592186056697,17592186060057:17592186056701,17592186060058:17592186056711,17592186060059:17592186056715,17592186060238:17592186058071,17592186060389:17592186058959}
for e,new in solutions.items():
 validate_prose(new);q=byid[e];old=q.get(':question/worked-solution');assert old is None;change(e,'question/worked-solution',old,new);q[':question/worked-solution']=new
 f=q[':question/answer-fields'][0];assert not f.get(':answer-field/correct');a=next(a for a in f[':answer-field/choices']if a[':db/id']==correct[e]);f[':answer-field/correct']=a;forms.extend([[kw('db/cas'),f[':db/id'],kw('answer-field/correct'),None,a[':db/id']],[kw('db/ensure'),f[':db/id'],kw('answer-field/validate')],[kw('db/ensure'),a[':db/id'],kw('answer/validate')],[kw('db/ensure'),e,kw('question/validate')]]);links.append({'question':e,'field':f[':db/id'],'correct':a[':db/id'],'value':a[':answer/value']})
(H/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');(H/'transaction.edn').write_text(dumps(forms)+'\n');(H/'links.json').write_text(json.dumps(links,indent=2)+'\n');(H/'repaired-questions.json').write_text(json.dumps(qs,indent=2)+'\n');print('fields',len(fields),'correct links',len(links),'currency values',sum(f['attribute']=='answer/value'for f in fields))

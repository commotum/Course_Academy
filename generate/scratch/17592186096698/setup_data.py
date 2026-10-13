import json,re
from pathlib import Path
H=Path(__file__).parent;s=json.load(open(H/'source.json'));qs=s['record'][':knowledge-point/questions']
params=[dict(family='quadratic',a='1',h='1',k='1',constants=['-1','0','1']),dict(family='cubic',a='-1',h='-1',k='1',constants=['-1','0','1']),dict(family='exponential',a='-2',h='0',k='-1/4',constants=['0','3','6']),dict(family='logarithmic',a='1',h='0',k='1',constants=['-1','0','2']),dict(family='reciprocal',a='1',h='0',k='1',constants=['-1','0','1']),dict(family='linear',a='-2',h='0',k='1',constants=['-3','0','3']),dict(family='quadratic',a='1',h='0',k='1',constants=['-1','0','1']),dict(family='cubic',a='1/2',h='-2',k='1',constants=['-1','0','1']),dict(family='exponential',a='-2',h='0',k='2',constants=['-2','0','2']),dict(family='cubic',a='-1/4',h='1',k='1',constants=['-2','0','2']),dict(family='linear',a='3',h='0',k='1',constants=['-2','0','2'])]
# Explicit raw expressions denote every colored curve; empirical polynomial
# magnitudes are evidence hypotheses, not default error recipes.
bs=[['x+1','x','x-1'],['-(x-1)**2+1','-(x-1)**2','-(x-1)**2-1'],['(x-1)**2-1','(x-1)**2','(x-1)**2+1'],['x**3+1','x**3','x**3-1'],['x**2+1','x**2','x**2-1']]
banks=[bs,
[[f'{base}+{c}' for c in ['-1','0','1']] for base in ['-(x+1)**3','-(x-1)**2','(x-1)**3','-(x+1)**2','-x**3']],
[['-x**2/4','-x**2/4+2','-x**2/4+4'],['2*exp(-x/4)+1','2*exp(-x/4)-2','2*exp(-x/4)-5'],['-2*exp(x/4)-1','-2*exp(x/4)+2','-2*exp(x/4)+5'],['-2*exp(-x/4)','-2*exp(-x/4)+3','-2*exp(-x/4)+6'],['x**2/4','x**2/4+2','x**2/4+4']],
[['log(x)-1','log(x)','log(x)+2'],['1/(x-2)','1/x','1/(x-1)'],['x-2','x','x+1'],['log(x-2)','log(x)','log(x-1)'],['1/x-2','1/x','1/x+1']],
[['x-1','x','x+1'],['x**2/4','x**2/4+1','x**2/4-1'],['-1/x-1','-1/x','-1/x+1'],['1/x-1','1/x','1/x+1'],['-sqrt(3*x)','-sqrt(3*x)+1','-sqrt(3*x)-1']],
[['-2*x-3','-2*x','-2*x+3'],['-x**3/8-1','-x**3/8','-x**3/8+1'],['x**2-2','x**2','x**2+2'],['-x**2-2','-x**2','-x**2+2'],['2*x-3','2*x','2*x+3']],
[[f'{base}+{c}' for c in ['1','0','-1']] for base in ['x**2','2*x','-x**2','x**3']]+[['(x+1)**3','x**3','(x-1)**3']],
[[f'{base}+{c}' for c in ['-1','0','1']] for base in ['(x+2)**3/2','3*(x+2)**2/2']]+[['(x+3)**3/2','(x+2)**3/2','(x+1)**3/2']]+[[f'{base}+{c}' for c in ['-1','0','1']] for base in ['-3*(x+2)**2/2','-(x+2)**3/2']],
[[f'{base}+{c}' for c in ['-2','0','2']] for base in ['2*exp(2*x)','-(x+2)**2/4','-2*exp(2*x)','(x+2)**2/4','-2*exp(-2*x)']],
[[f'{base}+{c}' for c in ['-2','0','2']] for base in ['3*(x+1)**2/4','-(x-1)**3/4','-(x+1)**3/4','(x-1)**3/4','-3*(x-1)**2/4']],
[[f'{base}+{c}' for c in ['-2','0','2']] for base in ['-3*x','3*x**3','-3*x**2','3*x**2','3*x']]]
# Array entries explicitly order colors red/black/blue unless documented otherwise.
colors=[['red','blue','black'],['red','black','blue'],['red','black','blue'],['red','black','blue'],['red','black','blue'],['red','black','blue'],['red','black','blue'],['red','black','blue'],['red','black','blue'],['red','black','blue'],['red','black','blue']]
# q50195 first option black is top, blue middle, red bottom.
color_overrides={(0,0):['black','blue','red'],(0,1):['red','black','blue'],(0,2):['red','black','blue'],(0,3):['red','black','blue'],(0,4):['red','black','blue'],(2,1):['red','black','blue'],(2,2):['red','black','blue'],(3,1):['red','black','blue'],(3,3):['red','black','blue']}
records=[];cases=[]
for i,(q,p,bank) in enumerate(zip(qs,params,banks)):
 src=q[':question/math-academy-id'];f=q[':question/answer-fields'][-1];correct=f[':answer-field/correct'][':answer/value'];ci=next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/value']==correct)
 records.append({'source_id':q[':db/id'],'name':src,'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'parameters':p,'correct_index':ci,'curves':bank,'colors':[color_overrides.get((i,j),colors[i]) for j in range(5)],'uncertain_metric_options':{'q-50197':[4],'q-119139':[3],'q-79563':[2,3]}.get(src,[]),'source':q})
 cases.append({'source_id':q[':db/id'],'template':src,'level':records[-1]['level'],'parameters':p,'bank_profile':'raw-'+src})
(H/'recipes.json').write_text(json.dumps(records,indent=2));(H/'source-cases.json').write_text(json.dumps(cases,indent=2))

"""Source-tutorial row/column focus for ordinary numeric matrix products.

Presentation only. No answer fields, parameters, bank, or database operations.
"""
def matrix(rows):
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{bmatrix}'

def color(value, name):
    return r'{\color{'+name+'}{'+str(value)+'}}'

def product_solution(a,b,names,targets):
    """Keep target order and partially given result cells; emphasize each target."""
    m,n,k=len(a),len(b),len(b[0]);x,y=names;xy=x+y
    assert n==len(a[0]) and all(len(row)==n for row in a) and all(len(row)==k for row in b)
    assert len(set(map(tuple,targets)))==len(targets)
    c=[[sum(a[i][h]*b[h][j] for h in range(n)) for j in range(k)] for i in range(m)]
    dims=(r'\underset{'+str(m)+r'\times\boxed{'+color(n,'#2E8B57')+'}}{'+x+'}'
          +r'\underset{'+color(r'\checkmark','#2E8B57')+r'}{\cdot}'
          +r'\underset{\boxed{'+color(n,'#2E8B57')+r'}\times'+str(k)+'}{'+y+'}'
          +'='+r'\underset{'+str(m)+r'\times'+str(k)+'}{'+xy+'}')
    parts=[f'Here, ${x}$ is a ${m}\\times {n}$ matrix and ${y}$ is a ${n}\\times {k}$ matrix. '
           f'The matching inner dimensions show that the product is defined, and ${xy}$ is ${m}\\times {k}$:',
           '$$\n'+dims+'\n$$']
    for z,(i,j) in enumerate(targets):
        aa=[[color(v,'#4169E1' if rr==i else 'gray') for v in row] for rr,row in enumerate(a)]
        bb=[[color(v,'red' if cc==j else 'gray') for cc,v in enumerate(row)] for row in b]
        remaining=set(map(tuple,targets[z+1:]))
        progress=[[r'\ast' if (rr,cc) in remaining else str(v) for cc,v in enumerate(row)] for rr,row in enumerate(c)]
        progress[i][j]=r'\boxed{'+str(c[i][j])+'}'
        def f(v,hue):
            t=color(v,hue)
            return '('+t+')' if v<0 else t
        terms=[f(a[i][h],'#4169E1')+r'\cdot '+f(b[h][j],'red') for h in range(n)]
        dot=r' \\ &\quad +'.join('+'.join(terms[start:start+2]) for start in range(0,n,2))
        calculation=r'\begin{aligned}c_{'+str(i+1)+str(j+1)+'}&='+dot+r' \\ &='+str(c[i][j])+r'\end{aligned}'
        parts += [f'For entry $c_{{{i+1}{j+1}}}$, use row ${i+1}$ of ${x}$ (blue) and column ${j+1}$ of ${y}$ (red):',
                  '$$\n'+r'\begin{aligned}&'+matrix(aa)+matrix(bb)+r'\\ &='+matrix(progress)+r'\end{aligned}'+'\n$$',
                  '$$\n'+calculation+'\n$$']
    parts += ['Therefore,','$$\n'+xy+'='+matrix(c)+'.\n$$']
    return '\n\n'.join(parts)

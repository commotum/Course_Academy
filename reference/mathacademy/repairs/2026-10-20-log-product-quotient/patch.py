from read import *
if __name__=='__main__':
 path=HERE/'package/generator.py';text=path.read_text();text=text.replace("VERSION = '1.0.0'","VERSION = '1.1.0-source-scope'")
 start=text.index('def answer(p, signs):');end=text.index('\ndef source_bank(',start)
 text=text[:start]+'''def answer(p, signs):
    if p['template']=='combine': return log(p['base'], product_ratio(factors(p), signs))
    order=p.get('order',[0,1,2])
    order=[i for i in order if signs[i]>0]+[i for i in order if signs[i]<0]
    return signed_sum([str(p['k']),log(p['base'],str(p['c'])),log(p['base'],p['u'])],signs,order)

def validate_scope(p, source_index=None):
    """Retain observed factor roles and the source's two-positive/one-negative move."""
    s=tuple(p['signs']);order=p.get('order',[0,1,2])
    if sorted(order)!=[0,1,2]:raise ValueError('Exactly one occurrence of every factor is required')
    allowed=((1,1,-1),) if p['template']=='combine' else ((1,-1,1),(-1,1,1)) if p['template']=='expand' else ()
    if s not in allowed:raise ValueError('Outside the saved product/quotient KP source structure')
    if source_index is None and [s[i] for i in order]!=[1,1,-1]:
        raise ValueError('Present the two positive terms before the subtracted term')
    if p['base'] not in (('10','e') if p['template']=='combine' else ('2','3','5','10','e')):
        raise ValueError('Unsupported logarithm base')
    if p['u'] not in LETTERS or (p['template']=='combine' and (p['v'] not in LETTERS or p['v']==p['u'])):
        raise ValueError('Distinct source-supported variable slots required')
    if type(p['c'])is not int or not 2<=p['c']<=9:raise ValueError('Constant must be an integer from 2 to 9')
    if p['template']=='expand' and (type(p['k'])is not int or not 1<=p['k']<=3 or (p['base']=='e' and p['k']!=1)):
        raise ValueError('Unsupported known-logarithm value')

def solution(p):
    b,s=p['base'],p['signs'];fs=factors(p);order=p.get('order',[0,1,2])
    top=[fs[i]for i in order if s[i]>0];bottom=[fs[i]for i in order if s[i]<0]
    if len(top)!=2 or len(bottom)!=1:raise ValueError('Worked solution requires the saved source structure')
    quotient=log(b,r'\\cdot '.join(top))+'-'+log(b,bottom[0])
    if p['template']=='combine':
        start=signed_sum([log(b,f)for f in fs],s,order)
        return ('Using the product rule for logarithms, combine the first two terms:\\n\\n$$\\n'
                +r'\\begin{aligned}'+start+' &= '+quotient+r'.\\end{aligned}'+'\\n$$\\n\\n'
                +'Now use the quotient rule to combine the remaining difference:\\n\\n$$\\n'
                +quotient+' = '+answer(p,s)+'.\\n$$')
    ordered=[i for i in order if s[i]>0]+[i for i in order if s[i]<0]
    expanded=signed_sum([log(b,f)for f in fs],s,ordered)
    power=log(b,factors(p,False)[0])
    return ('Using the quotient rule for logarithms, separate the numerator and denominator:\\n\\n$$\\n'
            +log(b,product_ratio(fs,s,order))+' = '+quotient+'.\\n$$\\n\\n'
            +'Now use the product rule to expand the logarithm of the numerator:\\n\\n$$\\n'
            +quotient+' = '+expanded+'.\\n$$\\n\\n'
            +'Since $'+log(b,fs[0])+('='+power if power!=log(b,fs[0]) else '')+'='+str(p['k'])+'$, we obtain\\n\\n$$\\n'
            +expanded+' = '+answer(p,s)+'.\\n$$')

''' + text[end:]
 old="    if s not in SIGNS: raise ValueError('Both numerator and denominator required')"
 assert text.count(old)==1;text=text.replace(old,old+"\n    validate_scope(p,source_index)")
 text=text.replace("st=rng.choice(['combine','expand']); s=rng.choice(SIGNS)","st=rng.choice(['combine','expand'])\n    s=(1,1,-1) if st=='combine' else rng.choice(((1,-1,1),(-1,1,1)))")
 text=text.replace("c=rng.choice(cs); u,v=rng.sample(LETTERS,2); order=rng.sample(range(3),3)","c=rng.choice(cs); u,v=rng.sample(LETTERS,2)\n    top=[i for i in range(3)if s[i]>0];rng.shuffle(top)\n    order=top+[i for i in range(3)if s[i]<0]")
 text=text.replace("'choice_vectors':vectors,'source_index':source_index", "'scope':'source factor roles; two positive terms and one subtracted term',\n        'choice_vectors':vectors,'source_index':source_index")
 path.write_text(text)
 print('Patched source roles, sign structure, ordering, explicit validation and worked-solution stages')

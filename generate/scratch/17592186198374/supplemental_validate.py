#!/usr/bin/env python3
"""Correlated primitive regression: every full row stays equal, factors are wrong."""
import copy,importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('validator',D/'validate.py');z=importlib.util.module_from_spec(spec);spec.loader.exec_module(z)
rows=json.loads((D/'review.json').read_text());normal=[r for r in rows if r['generation']['eligible_for_learning']]
for r in normal:z.check_normal(r)
r=copy.deepcopy(normal[0]);ctx=z.read_context(r);g=z.g;p=g.canonical_parameters(r['generation']['parameters']);c=g.components('polynomial',p);a0,a1,b0,b1=p['bounds'];sol=r['question'][':question/worked-solution'];chain=sol.rsplit(r'\begin{aligned}',1)[1].split(r'\end{aligned}')[0];pieces=chain.split(r' \\ ');prefix='&='+g.tex(c['C'])+r'\cdot '
B=lambda P,lo,hi:r'\left['+g.tex(P)+r'\right]_{'+g.tex(lo)+'}^{'+g.tex(hi)+'}'
pieces[-5]=prefix+B(g.v**3/6,b0,b1)+r'\cdot '+B(g.u**2,a0,a1)
pieces[-4]=prefix+r'\left('+g.group(b1)+r'^{3}/6-\left('+g.group(b0)+r'^{3}/6\right)\right)\cdot \left('+g.group(a1)+r'^{2}-\left('+g.group(a0)+r'^{2}\right)\right)'
pieces[-3]=prefix+r'\left('+g.group(c['eV'][0]/2)+'-'+g.group(c['eV'][1]/2)+r'\right)\cdot \left('+g.group(2*c['eU'][0])+'-'+g.group(2*c['eU'][1])+r'\right)'
pieces[-2]=prefix+g.group(c['Iv']/2)+r'\cdot '+g.group(2*c['Iu'])
for row in pieces:
    lhs,rhs=row.split('&=')
    if lhs:z.eq(z.calculus(lhs,ctx),ctx['answer'])
    z.eq(z.calculus(rhs,ctx),ctx['answer'])
r['question'][':question/worked-solution']=sol.replace(chain,r' \\ '.join(pieces));z.expect_failure(lambda:z.check_normal(r))
(D/'supplemental-checks.json').write_text(json.dumps({'normal_review_records_checked':len(normal),'first_integrand_and_factorization_checks':'passed','individual_primitive_checks':'passed','compensating_primitive_error_regression':'all total row equalities preserved; rejected against actual separated integrands','generator_changed':False},indent=2)+'\n')
print('Supplemental display/individual-primitive QA:',len(normal),'records passed; correlated primitive mutation rejected.')

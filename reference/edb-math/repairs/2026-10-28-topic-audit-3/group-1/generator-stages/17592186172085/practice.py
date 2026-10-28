"""Same definition, varied qualifying roles; moderate/hard are authored extensions.

Easy: two independent dimension checks on familiar source forms.
Moderate: unused input coordinates, zero output coordinates and scalar outputs.
Hard: require a real planar vector at EVERY point of the explicit stated domain.
Replay of eight imported anchors remains in generator.replay.
"""
import copy
import hashlib
import json
import random
import uuid
from math_format import checked_math_content, normalize_prose

VERSION = 'vector-fields-5-three-bands-format-audit-9837-v1'
ROMANS = ('I', 'II', 'III')
MASKS = (1, 2, 3, 4, 5, 6)
BANDS = ('easy', 'moderate', 'hard')
FAMILIES = ('polynomial', 'trig', 'radical', 'reciprocal', 'log')

def uid(s):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy/' + s))

def shift(v, n):
    return v if n == 0 else '(' + v + ('-' if n > 0 else '+') + str(abs(n)) + ')'

def dimension_candidate(rng, level, qualifies, label, h, family):
    if qualifies:
        inp, out = 2, 2
    else:
        inp, out = rng.choice([(1, 2), (3, 3), (2, 3)] if level == 'easy'
                              else [(1, 2), (3, 2), (2, 3), (2, 1)])
    variables = ['t'] if inp == 1 else (['x', 'y'] if inp == 2 else ['x', 'y', 'z'])
    u, v = variables[0], variables[min(1, inp - 1)]
    a = shift(u, h)
    first = {'polynomial':a+'^2', 'trig':r'\sin '+a,
             'radical':r'\sqrt{'+a+'}', 'reciprocal':r'\frac{1}{'+a+'}',
             'log':r'\ln '+a}[family]
    second = v + ('+' if h >= 0 else '') + str(h)
    # Moderate removes the visual dependency shortcut: declared coordinates can
    # be unused and output components can be zero, without changing dimension.
    if level == 'moderate':
        second = rng.choice(['0', str(rng.randint(1, 3)), first])
    components = [first, second] + ([str(rng.randint(1, 3))] if out == 3 else [])
    notation = rng.choice(['tuple', 'basis']) if out != 1 else 'scalar'
    if out == 1:
        expression = first + '+' + second
    elif notation == 'tuple':
        expression = r'\langle '+','.join(components)+r'\rangle'
    else:
        expression = '+'.join('('+c+r')\,\mathbf '+b for c,b in zip(components,'ijk'))
    formula = label+'('+','.join(variables)+')='+expression
    condition = {'polynomial':None, 'trig':None, 'radical':a+r'\geq 0',
                 'reciprocal':a+r'\ne 0', 'log':a+'>0'}[family]
    dim = r'\mathbb R^'+str(inp)
    domain = dim if condition is None else r'\{('+','.join(variables)+r')\in '+dim+':'+condition+r'\}'
    reason = ('takes '+str(inp)+' input coordinate'+('s' if inp != 1 else '')+' and returns '+
              ('a scalar' if out == 1 else 'a vector with '+str(out)+' components')+'. ')
    if level == 'moderate':
        reason += 'The declared input list determines the input dimension, even when a coordinate is unused; a zero output coordinate still counts. '
    if condition:
        reason += 'Its natural real domain is $'+domain+'$, which is nonempty. A restricted natural domain is allowed. '
    else:
        reason += 'All components are real on $'+dim+'$. '
    reason += ('Both dimensions are two, so select this function.' if qualifies else
               'The input and output are not both two-dimensional, so do not select this function.')
    return {'formula':formula, 'domain':domain, 'reason':reason, 'correct':qualifies,
            'family':family, 'input_dim':inp, 'output_dim':out, 'notation':notation}

def domain_candidate(kind, qualifies, label, h, k, omitted=0):
    u, v = shift('x',h).strip('()'), shift('y',k).strip('()')
    if kind == 'log_sqrt':
        rad='x-y'+(('+' if k-h>0 else '')+str(k-h) if k!=h else '')
        log='x+y'+(('+' if -h-k>0 else '')+str(-h-k) if h+k!=0 else '')
        expression=r'\langle\sqrt{'+rad+r'},\ln('+log+r')\rangle'
        needs=[rad+r'\geq0',log+'>0']
        if omitted == 0:
            witness=(h,k); failure=r'\ln(0)'; why='the logarithm is undefined'
        else:
            witness=(h,k+1); failure=r'\sqrt{-1}'; why='the square root is not real'
        extra='The boundary $'+u+'='+v+'>0$ is allowed.'
    elif kind == 'recip_sqrt':
        expression=r'\langle\frac{1}{'+u+r'},\sqrt{'+v+r'}\rangle'
        needs=[u+r'\ne0',v+r'\geq0']
        if omitted == 0:
            witness=(h,k+1);failure=r'1/0';why='the reciprocal is undefined'
        else:
            witness=(h+1,k-1);failure=r'\sqrt{-1}';why='the square root is not real'
        extra='The square-root boundary $'+v+'=0$ is allowed when $'+u+r'\ne0$. '
    elif kind == 'missing_j':
        expression=r'\ln('+u+r')\,\mathbf i'
        needs=[u+'>0'];witness=(h,k);failure=r'\ln(0)';why='the logarithm is undefined'
        extra='The omitted planar component is zero: $'+expression+r'+0\,\mathbf j=\langle\ln('+u+r'),0\rangle$. Its output is still planar.'
    else:
        raise ValueError('Unknown domain profile')
    if qualifies:
        conditions=needs.copy()
        if kind == 'missing_j' and omitted:
            conditions=[u+r'\geq1']
    elif kind == 'missing_j':
        conditions=[u+(r'\geq0' if omitted == 0 else '>-1')]
    elif kind == 'log_sqrt':
        conditions=[needs[0],log+r'\geq0'] if omitted == 0 else [rad+r'\geq-1',needs[1]]
    else:
        conditions=[u+r'\geq0',needs[1]] if omitted == 0 else [needs[0],v+r'\geq-1']
    domain=r'\{(x,y)\in\mathbb R^2:'+r',\ '.join(conditions)+r'\}'
    formula=label+'(x,y)='+expression
    required='$'+r',\ '.join(needs)+'$'
    if qualifies:
        reason='The components require '+required+'. Every point in the stated domain satisfies these conditions. '
        reason+=extra+' '
        reason+='The inputs and outputs are planar, so select this function.'
    else:
        reason='The components require '+required+'. The point $('+str(witness[0])+','+str(witness[1])+')$ lies in the stated domain, but gives $'+failure+'$; '+why+'. '
        if kind=='missing_j': reason+=extra+' '
        reason+='The formula therefore fails on the entire stated domain. Do not select this function; shrinking the domain is not allowed in this question.'
    return {'formula':formula,'domain':domain,'reason':reason,'correct':qualifies,
            'family':kind,'input_dim':2,'output_dim':2,'notation':'basis' if kind=='missing_j' else 'tuple',
            'required':needs,'witness':None if qualifies else witness,'omitted':omitted}

@checked_math_content
def generate(level='easy', seed=0, template=None, parameters=None):
    if level not in BANDS:
        raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    p=copy.deepcopy(parameters) if parameters is not None else {
        'mask':rng.choice(MASKS), 'h':rng.randint(-4,4), 'k':rng.randint(-3,3),
        'labels':rng.sample(list('ABCDEFGHJKLMNPQRSTUVWXYZ'),3),
        'profiles':rng.sample(['log_sqrt','recip_sqrt','missing_j'],3), 'omitted':rng.randrange(2)}
    p.setdefault('families', [rng.choice(FAMILIES) for _ in range(3)])
    if len(p['families'])!=3 or any(f not in FAMILIES for f in p['families']):
        raise ValueError('Three permitted formula families required')
    if set(p)!={'mask','h','k','labels','profiles','omitted','families'} or p['mask'] not in MASKS:
        raise ValueError('Expected a nonempty proper selection mask and complete parameters')
    if type(p['h']) is not int or not -4<=p['h']<=4 or type(p['k']) is not int or not -3<=p['k']<=3:
        raise ValueError('Shifts out of range')
    if len(p['labels'])!=3 or len(set(p['labels']))!=3 or any(c not in 'ABCDEFGHJKLMNPQRSTUVWXYZ' for c in p['labels']):
        raise ValueError('Three distinct permitted labels required')
    if sorted(p['profiles'])!=sorted(['log_sqrt','recip_sqrt','missing_j']) or p['omitted'] not in (0,1):
        raise ValueError('Invalid profiles or omitted restriction')
    if template not in (None,'dimensions','stated-domain'):
        raise ValueError('Use generator.replay for imported anchors')
    candidates=[]
    for i,label in enumerate(p['labels']):
        qualifies=bool(p['mask'] & (1<<i))
        c=(domain_candidate(p['profiles'][i],qualifies,label,p['h'],p['k'],p['omitted']) if level=='hard'
           else dimension_candidate(rng,level,qualifies,label,p['h'],p['families'][i]))
        candidates.append(c)
    if level=='hard':
        prompt=r'Which formulas define vector fields on $\mathbb R^2$ on their **entire stated domains**? Select all that apply. Keep every stated domain unchanged. The symbols $\mathbf i,\mathbf j$ are the planar unit vectors.'
    else:
        prompt=r'Which of the following are vector fields on $\mathbb R^2$? Select all that apply.'
        if level=='easy':
            prompt+=r' A vector field maps points of a subset of $\mathbb R^2$ to vectors in $\mathbb R^2$; a restricted natural domain is allowed.'
        else:
            prompt+=' Use each function\'s declared input coordinates and its natural real domain.'
    for i,c in enumerate(candidates):
        prompt+='\n\n- **'+ROMANS[i]+'.** $'+c['formula']+'$'
        if level=='hard': prompt+=' on $'+c['domain']+'$.'
    solution=('Check the input dimension and output dimension.' if level!='hard' else
              'Check planar inputs and outputs, then test whether the formula is real and defined at every point of the stated domain.')
    for i,c in enumerate(candidates):
        solution+='\n\n- **'+ROMANS[i]+'.** $'+p['labels'][i]+'$ '+c['reason']
    selected=[ROMANS[i] for i,c in enumerate(candidates) if c['correct']]
    solution+='\n\nSelect '+', '.join(selected)+' only.'
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    ident=hashlib.sha256((VERSION+level+prompt+solution).encode()).hexdigest()
    fields=[]
    for i,c in enumerate(candidates):
        fid=uid(ident+'/'+ROMANS[i]);value=str(c['correct']).lower()
        choices=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in ('false','true')]
        fields.append({':answer-field/id':fid,':answer-field/key':ROMANS[i],':answer-field/type':':answer-field.type/checkbox',
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+'/'+value)]})
    return {'knowledge_point':{'db_id':17592186172085,'id':'019e5a17-1aab-565b-8881-447c86a9a7ec','title':'Identifying Vector Fields on Two-Dimensions'},
            'question':{':question/id':uid(ident),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,
                        ':question/worked-solution':solution,':question/answer-fields':fields},
            'generation':{'version':VERSION,'template':'stated-domain' if level=='hard' else 'dimensions','seed':seed,'parameters':p,
                          'candidates':candidates,'source':{'math_academy_ids':['q-122465','q-122656','q-122650'],
                          'tutorial':5782,'investigation_exemplars':['248652e3-f6c5-5073-aae7-554bf75b40eb','b6d5ec1a-a97b-54c7-bc35-cc60d1536152']}}}

def batch(level, count, seed):
    if level not in BANDS or type(count) is not int or count<1:
        raise ValueError('Valid band and positive count required')
    rng=random.Random(seed); records=[];seen=set(); planned=[]
    while len(planned)<count:
        masks=list(MASKS);rng.shuffle(masks)
        planned.extend(masks[:count-len(planned)])
    # Each five-item batch has at least six true and six false candidate slots.
    # Cycle every formula family through both roles, preventing "always select
    # radicals" in the delivered batch, not merely in a larger control sample.
    family_orders={}
    for outcome in (False,True):
        order=list(FAMILIES);rng.shuffle(order);family_orders[outcome]=order
    role_counts={False:0,True:0}
    for mask in planned:
        families=[]
        for i in range(3):
            role=bool(mask & (1<<i));families.append(family_orders[role][role_counts[role]%len(FAMILIES)])
            role_counts[role]+=1
        while True:
            nonce=rng.randrange(2**63)
            r=generate(level,nonce)
            p=r['generation']['parameters'];p['mask']=mask;p['families']=families
            r=generate(level,nonce,parameters=p)
            if r['question'][':question/id'] not in seen:break
        seen.add(r['question'][':question/id']);records.append(r)
    return records

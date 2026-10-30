#!/usr/bin/env python3
"""Three-matrix arithmetic: seeded, exact, source-shaped questions.

CLI: --difficulty easy|moderate|hard --count N --seed N --format json|markdown.
Hard extends grouped entrywise arithmetic to four operands. No database writes.
Local source-cases.json supports source replay; no runtime repository imports.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
from math_format import matrix_operands, matrix_answer, normalize_prose, normalize_tex, checked_math_content
import sympy as sp

KP_ID = 17592186100991
KP_UUID = '667ac53c-36b8-56a0-9699-fe27c8373c6b'
TITLE = 'Calculating the Sum or Difference of Three or More Matrices'
VERSION = 'matrix-grouping-4'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
TEMPLATES = {'easy': ('flat_sum_blank', 'flat_difference_blank', 'flat_sum_radio', 'flat_reverse_difference_blank', 'left_difference_radio'),
             'moderate': ('nested_difference_blank', 'nested_sum_blank'),
             'hard': ('paired_dd_blank','paired_ad_blank','paired_da_blank','paired_aa_blank')}
SOURCE_IDS = {'flat_reverse_difference_blank':['q-279469'],'flat_sum_blank':['q-279526'], 'flat_difference_blank':['q-275408','q-279525'],
              'flat_sum_radio':['q-69636'], 'nested_difference_blank':['q-279527'],
              'nested_sum_blank':['q-279528']}
SOURCE_IDS.update({'left_difference_radio':['q-69637'], **{t:['e-4378','tutorial-2973'] for t in TEMPLATES['hard']}})
EXPR = {'flat_reverse_difference_blank':'{a}-{b}+{c}','flat_sum_blank':'{a}+{b}+{c}', 'flat_difference_blank':'{a}+{b}-{c}',
        'flat_sum_radio':'{a}+{b}+{c}', 'nested_difference_blank':'{a}-({b}-{c})',
        'nested_sum_blank':'{a}+({b}-{c})'}

EXPR.update({'left_difference_radio':'({a}-{b})-{c}', 'paired_dd_blank':'({a}-{b})-({c}-{d})', 'paired_ad_blank':'({a}+{b})-({c}-{d})', 'paired_da_blank':'({a}-{b})-({c}+{d})', 'paired_aa_blank':'({a}+{b})-({c}+{d})'})

def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',',':')).encode()).hexdigest()

def uid(x):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), x))

def matrix(rows):
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{bmatrix}'

def parse_matrices(text):
    return [[[int(v.strip()) for v in row.split('&')] for row in m.split('\\\\')]
            for m in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]

def expression(template, names):
    return EXPR[template].format(**dict(zip('abcd',names)))

def scalar(v, following=False):
    return '('+str(v)+')' if following and v<0 else str(v)

def cell_ops(a,b,c,template):
    return str(a)+('-' if template=='flat_reverse_difference_blank' else '+')+scalar(b,True)+('+' if template.startswith('flat_sum') or template=='flat_reverse_difference_blank' else '-')+scalar(c,True)

def evaluated(template, matrices):
    a,b,c = map(sp.Matrix, matrices[:3])
    if template.startswith('paired_'):
        d=sp.Matrix(matrices[3]);return a+(b if template[7]=='a' else -b)-c+(-d if template[8]=='a' else d)
    if template=='left_difference_radio': return a-b-c
    if template.startswith('flat_sum'): return a+b+c
    if template=='flat_difference_blank': return a+b-c
    if template=='flat_reverse_difference_blank': return a-b+c
    if template=='nested_difference_blank': return a-(b-c)
    if template=='nested_sum_blank': return a+(b-c)
    raise ValueError('Unsupported template')

def radio_bank(matrices):
    """Complete observed q-69636 bank. Per-cell sign changes are explicit.

    These reproduce the observed objects; why learners make the compound
    sign mistakes is unresolved. No misconception explanations are displayed.
    """
    a,b,c=map(sp.Matrix,matrices); z=a+b+c
    first=z.copy();first[0,1]=-a[0,1]+b[0,1]+c[0,1];first[1,0]=-z[1,0]
    first[2,0]=-z[2,0];first[2,1]=a[2,1]-b[2,1]+c[2,1]
    second=z.copy();second[1,1]=a[1,1]-b[1,1]+c[1,1]
    second[2,0]=-z[2,0];second[2,1]=a[2,1]-b[2,1]+c[2,1]
    third=first.copy();third[2,0]=z[2,0];third[2,1]=z[2,1]
    fifth=z.copy();fifth[0,1]=a[0,1]-b[0,1]+c[0,1]
    fifth[1,1]=a[1,1]-b[1,1]+c[1,1];fifth[2,1]=-z[2,1]
    return [first,second,third,z,fifth]

def paired_bank(matrices,rng,key,template='flat_sum_radio'):
    """Authored bank: two values per cell, groups of 2/3, no key-only cell."""
    z=evaluated(template,matrices)
    attempts=0
    while True:
        attempts+=1; bank=[z.copy() for _ in range(5)]; details=[]
        for i in range(z.rows):
            for j in range(z.cols):
                eligible=[k for k in range(3) if matrices[k][i][j]!=0]
                k=rng.choice(eligible) if eligible else None
                signs=(1,-1,-1) if template=='left_difference_radio' else (1,1,1)
                error=rng.choice(['reverse sign','omit operand','repeat operand'])
                factor={'reverse sign':-2,'omit operand':-1,'repeat operand':1}[error]
                wrong=z[i,j]+factor*signs[k]*matrices[k][i][j] if k is not None else z[i,j]+rng.choice([-1,1])
                true_group={key,*rng.sample([x for x in range(5) if x!=key],rng.choices([1,2],weights=[2,3])[0])}
                for x in range(5):
                    if x not in true_group: bank[x][i,j]=wrong
                details.append({'cell':[i,j],'error_operand':k,'error':error,'correct_group':sorted(true_group)})
        sums=[sum(m) for m in bank];norms=[sum(abs(v) for v in m) for m in bank]
        modes=[max(set(col),key=col.count) for col in zip(*(tuple(m) for m in bank))]
        sign_patterns=[tuple((1 if v>0 else -1 if v<0 else 0) for v in m) for m in bank]
        extreme=any(sums[key]==fn(sums) and sums.count(sums[key])==1 for fn in (min,max))
        norm_cue=any(z) and norms[key]==min(norms) and norms.count(norms[key])==1
        mode_cue=tuple(bank[key])==tuple(modes) and sum(tuple(m)==tuple(modes) for m in bank)==1
        sign_cue=any(z) and sign_patterns.count(sign_patterns[key])==1
        if len({tuple(m) for m in bank})==5 and not (extreme or norm_cue or mode_cue or sign_cue):
            return bank, {'profile':'paired-errors-v2','key_position':key,'cells':details,'attempts':attempts}
        if attempts>1000: raise RuntimeError('Cannot produce distinct bank')


def prompt(template,p):
    names=p['names']; expr=expression(template,names)
    text='Calculate $'+expr+'$, where\n\n'
    text+=matrix_operands(n+'='+matrix(m) for n,m in zip(names,p['matrices']))
    if template.endswith('blank'):
        text+='\n\n'+matrix_answer(expr,[['{{field-1}}','{{field-2}}'],['{{field-3}}','{{field-4}}']])
    return text

def solution(template,p):
    a,b,c = map(sp.Matrix,p['matrices'][:3]); names=p['names'];expr=expression(template,names)
    z=evaluated(template,p['matrices']); n,m=a.shape
    if template.startswith('paired_'):
        d=sp.Matrix(p['matrices'][3]);op1='+' if template[7]=='a' else '-';op2='+' if template[8]=='a' else '-'
        left=a+b if op1=='+' else a-b;right=c+d if op2=='+' else c-d
        expanded=lambda x,y,op:matrix([[str(x[i,j])+op+scalar(y[i,j],True) for j in range(m)] for i in range(n)])
        stages=['('+matrix(a.tolist())+op1+matrix(b.tolist())+')-('+matrix(c.tolist())+op2+matrix(d.tolist())+')', expanded(a,b,op1)+'-'+expanded(c,d,op2),matrix(left.tolist())+'-'+matrix(right.tolist()),expanded(left,right,'-'),matrix(z.tolist())]
    elif template=='left_difference_radio':
        inner=a-b
        stages=['('+matrix(a.tolist())+'-'+matrix(b.tolist())+')-'+matrix(c.tolist()),matrix([[str(a[i,j])+'-'+scalar(b[i,j],True) for j in range(m)] for i in range(n)])+'-'+matrix(c.tolist()),matrix(inner.tolist())+'-'+matrix(c.tolist()),matrix([[str(inner[i,j])+'-'+scalar(c[i,j],True) for j in range(m)] for i in range(n)]),matrix(z.tolist())]
    elif template.startswith('flat'):
        stages=[matrix(a.tolist())+('-' if template=='flat_reverse_difference_blank' else '+')+matrix(b.tolist())+('+' if template.startswith('flat_sum') or template=='flat_reverse_difference_blank' else '-')+matrix(c.tolist()),
                matrix([[cell_ops(a[i,j],b[i,j],c[i,j],template) for j in range(m)] for i in range(n)]),matrix(z.tolist())]
    else:
        op='-' if template=='nested_difference_blank' else '+'
        inner=b-c
        stages=[matrix(a.tolist())+op+'('+matrix(b.tolist())+'-'+matrix(c.tolist())+')',
                matrix(a.tolist())+op+matrix([[str(b[i,j])+'-'+scalar(c[i,j],True) for j in range(m)] for i in range(n)]),
                matrix(a.tolist())+op+matrix(inner.tolist()),
                matrix([[str(a[i,j])+op+scalar(inner[i,j],True) for j in range(m)] for i in range(n)]), matrix(z.tolist())]
    def display(label, rows):
        return '$$\n'+r'\begin{aligned}'+label+' & ='+r' \\  & ='.join(rows)+r'\end{aligned}'+'\n$$'
    if template.startswith('paired_'):
        left_name=names[0]+op1+names[1];right_name=names[2]+op2+names[3]
        return ('Calculate each parenthesized result entry by entry:\n\n'+display(left_name,[expanded(a,b,op1),matrix(left.tolist())])+'\n\n'+display(right_name,[expanded(c,d,op2),matrix(right.tolist())])+'\n\nSubtract the second result from the first:\n\n'+display(expr,[matrix(left.tolist())+'-'+matrix(right.tolist()),expanded(left,right,'-'),matrix(z.tolist())]))
    if template=='left_difference_radio':
        first=names[0]+'-'+names[1]
        return ('First calculate the left-hand difference:\n\n'+display(first,[matrix([[str(a[i,j])+'-'+scalar(b[i,j],True) for j in range(m)] for i in range(n)]),matrix(inner.tolist())])+'\n\nSubtract the third matrix entry by entry:\n\n'+display(expr,[matrix([[str(inner[i,j])+'-'+scalar(c[i,j],True) for j in range(m)] for i in range(n)]),matrix(z.tolist())]))
    if template.startswith('flat'):stages=stages[1:]
    radio=template.endswith('radio')
    return ('Performing the operations on each corresponding entry, we get'+(':' if radio else '')+'\n\n$$\n'+
            r'\begin{aligned}'+expr+' & ='+r' \\  & ='.join(stages)+('' if radio else '.')+r'\end{aligned}'+'\n$$')

def task_fingerprint(template,matrices):
    # Matrix letters, seeds, option order and authored field UUIDs are irrelevant.
    if template.startswith('paired_'): return digest({'operands':matrices,'signs':(1,1 if template[7]=='a' else -1,-1,-1 if template[8]=='a' else 1)})
    if template=='left_difference_radio':return digest({'operands':matrices,'signs':(1,-1,-1)})
    signs=(1,-1,1) if template in ('nested_difference_blank','flat_reverse_difference_blank') else (1,1,-1) if template in ('flat_difference_blank','nested_sum_blank') else (1,1,1)
    return digest({'operands':matrices,'signs':signs})

def fingerprint(q):
    text=q[':question/problem'];mats=parse_matrices(text)
    if len(mats)!=3: return digest({'excluded_prompt':text})
    expr=re.search(r'Calculate \$(.*?)\$',text)[1].replace(' ','')
    template='nested_difference_blank' if '-(' in expr else 'nested_sum_blank' if '+(' in expr else 'flat_difference_blank' if '-' in expr else 'flat_sum_blank'
    return task_fingerprint(template,mats)

@checked_math_content
def generate(level,seed,template=None,parameters=None,bank_profile=None):
    if level not in TEMPLATES: raise ValueError('Unsupported difficulty: '+level)
    rng=random.Random(seed);template=template or rng.choice(TEMPLATES[level])
    if template not in TEMPLATES[level]:raise ValueError('Template/difficulty mismatch')
    radio_key=rng.randrange(5) if template.endswith('radio') else None
    if parameters is None:
        rows=3 if template=='flat_sum_radio' else 2
        cols=3 if template=='left_difference_radio' else 2
        count=4 if level=='hard' else 3
        names=rng.choice([['A','B','C'],['C','D','E'],['R','S','T'],['X','Y','Z']])
        names=names+['U'] if count==4 else names
        matrices=[[[rng.randint(-5,5) for _ in range(cols)] for _ in range(rows)] for _ in range(count)]
        # Error alternatives require a nonzero operand in each radio cell.
        if template.endswith('radio'):
            for i in range(rows):
                for j in range(cols):
                    if all(m[i][j]==0 for m in matrices): matrices[rng.randrange(3)][i][j]=rng.choice([-1,1])
        p={'matrices':matrices,'names':names}
    else:p=json.loads(json.dumps(parameters))
    count=4 if level=='hard' else 3
    assert len(p['names'])==count and len(set(p['names']))==count and all(re.fullmatch('[A-Z]',n) for n in p['names'])
    shape=(3,2) if template=='flat_sum_radio' else (2,3) if template=='left_difference_radio' else (2,2)
    assert len(p['matrices'])==count
    for m in p['matrices']:
        assert len(m)==shape[0] and all(len(r)==shape[1] for r in m)
        assert all(isinstance(v,int) and not isinstance(v,bool) for r in m for v in r)
    z=evaluated(template,p['matrices']);fp=task_fingerprint(template,p['matrices'])
    problem=normalize_prose(prompt(template,p));worked=normalize_prose(solution(template,p))
    if template.endswith('radio'):
        bank, bank_details = (radio_bank(p['matrices']), {'profile':'q-69636'}) if bank_profile=='q-69636' else paired_bank(p['matrices'],rng,radio_key,template)
        assert len({tuple(m) for m in bank})==5
        values=[normalize_tex(matrix(m.tolist())) for m in bank];correct=normalize_tex(matrix(z.tolist()))
    else:
        values=[normalize_tex(str(v)) for v in z];correct=values
    # IDs follow normalized served content, never cosmetic seed identity.
    content=digest({'problem':problem,'solution':worked,'values':values,'correct':correct,'version':VERSION})
    qid=uid('question:'+content);fields=[]
    if template.endswith('radio'):
        fid=uid(qid+':selection');choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
        fields=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+':'+correct)]}]
    else:
        for i,v in enumerate(z):
            key='field-'+str(i+1);fid=uid(qid+':'+key);aid=uid(fid+':'+str(v))
            fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':str(v)}],':answer-field/correct':[':answer/id',aid]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
            'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':worked,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},
            'generation':{'version':VERSION,'template':template,'bank_profile':bank_details['profile'] if template.endswith('radio') else 'blank','bank_details':bank_details if template.endswith('radio') else None,'seed':seed,'parameters':p,'source_ids':SOURCE_IDS[template],'sympy_version':sp.__version__,'mathematical_fingerprint':fp,'eligible_for_learning':True,'domain':'integer entries, real matrix entrywise addition/subtraction; same dimensions','sampling_policy':'2x2 blanks or rectangular paired-error radio; integer entries -5..5'}}

def replay(source_id):
    """Replay immutable source parameters; incomplete legacy fields reconstructed."""
    sources=json.loads((Path(__file__).parent/'source-cases.json').read_text())['kp']
    allq=sources[':knowledge-point/questions']+[sources[':knowledge-point/canonical-example']]
    q=next(q for q in allq if q[':question/math-academy-id']==source_id)
    text=q[':question/problem'];expr=re.search(r'Calculate \$(.*?)\$',text)[1].replace(' ','').rstrip(',')
    mats=parse_matrices(text);names=re.findall(r'([A-Z])=\\begin',text)
    template=('left_difference_radio' if expr.startswith('(') else 'nested_difference_blank' if '-(' in expr else 'nested_sum_blank' if '+(' in expr else 'flat_reverse_difference_blank' if expr[1:2]=='-' else 'flat_difference_blank' if '-' in expr else 'flat_sum_radio' if len(mats[0])==3 else 'flat_sum_blank')
    level='moderate' if template.startswith('nested') else 'easy'
    record=generate(level,0,template,{'matrices':mats,'names':names},bank_profile='q-69636' if source_id=='q-69636' else None)
    if source_id in ('q-11476','q-13542','q-69637'):
        # Banks are evidence only: do not infer offset recipes for normal sampling.
        record['question'][':question/problem']=normalize_prose(text)
        fid=uid('replay:'+source_id); choices=[]
        z=matrix(evaluated(template,mats).tolist())
        for item in q[':question/answer-fields'][0][':answer-field/choices']:
            v=normalize_tex(item[':answer/value']); choices.append({':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v})
        correct=next(a[':answer/id'] for a in choices if parse_matrices(a[':answer/value'])==parse_matrices(z))
        record['question'][':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]
        if source_id!='q-69637':record['generation']['incomplete_source']={'missing':['difficulty','worked-solution','correct-answer'],'reconstructed_difficulty':level}
    if q.get(':question/worked-solution'):record['question'][':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
    record['generation']['source_replay']=source_id
    record['generation']['original_difficulty']=q.get(':question/difficulty')
    return record


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',required=True);parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--template');parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
    if args.count<1:parser.error('Positive count required')
    if args.difficulty not in TEMPLATES:parser.error('Unsupported difficulty')
    records=[];seen=set()
    for i in range(args.count*100):
        schedule=list(TEMPLATES[args.difficulty]);random.Random(args.seed).shuffle(schedule)
        chosen=args.template or schedule[i%len(schedule)]
        r=generate(args.difficulty,args.seed+i,chosen);fp=r['generation']['mathematical_fingerprint']
        if fp in seen:continue
        records.append(r);seen.add(fp)
        if len(records)==args.count:break
    if len(records)!=args.count:raise ValueError('Finite sampling bound reached')
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        print('\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))

if __name__=='__main__':main()

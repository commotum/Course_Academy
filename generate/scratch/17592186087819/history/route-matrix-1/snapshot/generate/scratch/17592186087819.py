#!/usr/bin/env python3
"""Matrices for Route Planning, math basis 1356; local generator through step 7.

Easy: observed three entry blanks or sum, 3/4 stations, counts 0..3.
Moderate: observed three-station HTML sum with directed edges and self loops.
Hard: authored four-station sum with independent nonidentity row/column orders;
three counts, including a self loop and two directed entries, still no products,
powers or multi-stage journeys. This difficulty label is a design claim.

Source profiles retain the entire observed finite scalar windows. Their numerical
values cannot identify wrong-operation intent; normal radio uses an authored
complete omission/reversed-direction/total-route bank. Every explicit input receives level guards.
Source templates are component masks, not source-return branches. Figure reuse
requires the complete directed adjacency matrix and its original geometry.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent/'17592186087819'
KP_ID=17592186087819
KP_UUID='10ca3efc-7d23-5bc1-ab41-f785bed69986'
TITLE='Matrices for Route Planning'
VERSION='route-matrix-1'
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
SPECS=json.loads((HERE/'specs.json').read_text())
TEMPLATES={k:v['level'] for k,v in SPECS.items()}|{'sum_permuted_four':'hard'}
LABELS='ABCD'

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))

def _table_mask(text,n):
    """Replace WHOLE ordered table entry components, never numeric substrings."""
    if '<table' in text:
        # Last n rows each have n entry cells; row heading cells stay unchanged.
        rows=list(re.finditer(r'<tr>.*?</tr>',text,re.S));replacements=[]
        for r,row in enumerate(rows[-n:]):
            vals=list(re.finditer(r'<td align="center">\$(.*?)\$</td>',row.group(),re.S))
            if len(vals)!=n:raise ValueError('HTML source matrix layout')
            for c,v in enumerate(vals):replacements.append((row.start()+v.start(1),row.start()+v.end(1),'{cell_'+str(r)+'_'+str(c)+'}'))
        for a,b,value in reversed(replacements):text=text[:a]+value+text[b:]
    else:
        lines=text.splitlines();r=0
        for index,line in enumerate(lines):
            if line.startswith('| From:') or re.match(r'\| \*\*[A-D]\*\*',line):
                cells=line.split('|');start=3 if r==0 else 2
                for c in range(n):cells[start+c]=' {cell_'+str(r)+'_'+str(c)+'} '
                lines[index]='|'.join(cells);r+=1
        if r!=n:raise ValueError('Markdown source matrix layout')
        text='\n'.join(lines)
    return text

PROMPT_MASKS={name:_table_mask(SOURCES[s['source']][':question/problem'],len(s['matrix'])) for name,s in SPECS.items()}
SOLUTION_TABLE_MASKS={name:_table_mask(SOURCES[s['source']][':question/worked-solution'].split('following:\n\n',1)[1].split('\n\nTherefore,',1)[0],len(s['matrix'])) for name,s in SPECS.items() if ':question/worked-solution' in SOURCES[s['source']]}

def _fill_mask(mask,m,holes,kind):
    # Slots are entire cells, retaining source whitespace and HTML/Markdown layouts.
    for r,row in enumerate(m):
        for c,x in enumerate(row):
            slot='{cell_'+str(r)+'_'+str(c)+'}'
            if [r,c] in holes:
                i=holes.index([r,c]);value=('{{field-'+str(i+1)+'}}' if kind=='blank' else '$'+ 'abc'[i]+'$')
            else:value='$'+str(x)+'$'
            if '<table' in mask:value=value.strip('$')
            mask=mask.replace(slot,value)
    return mask

def table(m,holes=(),kind='complete',rows=None,cols=None):
    n=len(m);rows=list(range(n)) if rows is None else rows;cols=list(range(n)) if cols is None else cols
    lines=['|  |  | To: |'+ '  |'*(n-1),'|'+ ' --- |'*(n+2),'|  |  | '+' | '.join('**'+LABELS[c]+'**' for c in cols)+' |']
    for k,r in enumerate(rows):
        values=[]
        for c in cols:
            if [r,c] in holes:
                i=holes.index([r,c]);values.append('{{field-'+str(i+1)+'}}' if kind=='blank' else '$'+'abc'[i]+'$')
            else:values.append('$'+str(m[r][c])+'$')
        prefix='| From: | **'+LABELS[r]+'** | ' if k==0 else '| **'+LABELS[r]+'** | '
        lines.append(prefix+' | '.join(values)+' |'+('  |' if k else ''))
    return '\n'.join(lines)


def _bullet(v,r,c,letter=None,base=None,raw=False):
    # Preserve captured grammar verbatim only when its complete count+direction
    # component agrees; changed counts use the same three count stages.
    if base is not None:
        pattern=r'\$([0-9]+)\$ arrows? starting at Station ([A-D]) and ending at Station ([A-D])'
        match=re.search(pattern,base)
        if match and int(match[1])==v and match[2]==LABELS[r] and match[3]==LABELS[c]:return base
        if raw:return base
        if not match and v==0 and 'Station '+LABELS[r]+' and ending at Station '+LABELS[c] in base:return base
    if v==0:
        a=f'- There are no arrows starting at Station {LABELS[r]} and ending at Station {LABELS[c]}.'
        b=(f' So, there are no routes from ${LABELS[r]}$ to ${LABELS[c]},$ and so ${letter}=0.$' if letter else f' So, there are no routes from {LABELS[r]} to {LABELS[c]}.')
    elif v==1:
        a=f'- There is $1$ arrow starting at Station {LABELS[r]} and ending at Station {LABELS[c]}.'
        b=(f' So, there is only one route from ${LABELS[r]}$ to ${LABELS[c]},$ and so ${letter}=1.$' if letter else f' So, there is $1$ route from {LABELS[r]} to {LABELS[c]}.')
    else:
        a=f'- There are ${v}$ arrows starting at Station {LABELS[r]} and ending at Station {LABELS[c]}.'
        b=(f' So, there are { {2:"two",3:"three"}.get(v,str(v)) } routes from ${LABELS[r]}$ to ${LABELS[c]},$ and so ${letter}={v}.$' if letter else f' So, there are ${v}$ routes from {LABELS[r]} to {LABELS[c]}.')
    return a+b


def solution(name,m,holes,kind,rows,cols,raw=False):
    spec=SPECS.get(name);source=SOURCES[spec['source']] if spec else {}
    original=source.get(':question/worked-solution')
    orig_bullets=re.findall(r'^- .*?(?=\n\n|$)',original or '',re.M)
    values=[m[r][c] for r,c in holes]
    blocks=[_bullet(v,r,c,'abc'[i] if kind=='radio' else None,orig_bullets[i] if len(orig_bullets)==3 else None,raw) for i,((r,c),v) in enumerate(zip(holes,values))]
    label='As a result, our route matrix is the following:' if kind=='radio' else 'Therefore, our route matrix is the following:'
    complete=_fill_mask(SOLUTION_TABLE_MASKS[name],m,[], 'complete') if name in SOLUTION_TABLE_MASKS else table(m,rows=rows,cols=cols)
    result="Let's examine our diagram.\n\n"+'\n\n'.join(blocks)+'\n\n'+label+'\n\n'+complete
    if kind=='radio':
        compact=spec is None or spec['source']!='q-138940' and spec['source']!='q-139685'
        eq=('a+b+c='+ '+'.join(map(str,values))+'='+str(sum(values))+'.') if compact else ('a + b + c = '+'+'.join(map(str,values))+' = '+str(sum(values))+'.')
        result+='\n\nTherefore, \n\n$$\n'+eq+'\n$$'
    return result


def guard(level,name,p,observed=False):
    m=p['matrix'];n=len(m)
    if n not in (3,4) or any(len(row)!=n for row in m):raise ValueError('square 3/4 route matrix required')
    if any(type(x)!=int or x<0 or x>3 for row in m for x in row):raise ValueError('counts must be integers 0..3')
    if sum(map(sum,m))>16:raise ValueError('at most 16 directed routes for legibility')
    holes=p['holes'];rows=p['row_order'];cols=p['col_order']
    if len(holes)!=3 or len({tuple(x) for x in holes})!=3 or any(len(x)!=2 or any(type(y)!=int or not 0<=y<n for y in x) for x in holes):raise ValueError('three distinct valid entries')
    if sorted(rows)!=list(range(n)) or sorted(cols)!=list(range(n)):raise ValueError('row/column orders must be permutations')
    if level=='hard':
        if n!=4 or rows==list(range(n)) or cols==list(range(n)) or rows==cols:raise ValueError('hard requires independent reordered headings')
        if sum(r==c for r,c in holes)!=1 or not any(m[r][c]>=2 for r,c in holes):raise ValueError('hard requires one loop and a parallel route count')
    elif level=='moderate' and n!=3:raise ValueError('moderate observed scope: three stations')
    elif rows!=list(range(n)) or cols!=list(range(n)):raise ValueError('only hard reorders headings')
    if name in SPECS and holes!=SPECS[name]['holes']:raise ValueError('source mask fixes missing entry positions')


def sample(level,name,rng):
    if name in SPECS:
        s=SPECS[name];m=[[rng.randint(1,3) if x else 0 for x in row] for row in s['matrix']]
        holes=s['holes']
        for r,c in holes:m[r][c]=rng.randint(0,3)
        n=len(m);return {'matrix':m,'holes':holes,'row_order':list(range(n)),'col_order':list(range(n))}
    # Same route counting operation, three unknowns, altered heading order.
    m=[[0]*4 for _ in range(4)]
    for r,c in rng.sample([(r,c) for r in range(4) for c in range(4)],7):m[r][c]=rng.randint(1,3)
    d=rng.randrange(4);off=rng.sample([(r,c) for r in range(4) for c in range(4) if r!=c],2)
    holes=[[d,d],*map(list,off)];m[d][d]=rng.randint(0,2)
    for r,c in off:m[r][c]=rng.randint(1,3)
    rows=list(range(4));cols=list(range(4));rng.shuffle(rows);rng.shuffle(cols)
    return {'matrix':m,'holes':holes,'row_order':rows,'col_order':cols}


def render_plots(name,m):
    if name in SPECS and m==SPECS[name]['matrix']:
        return {'prompt':str(HERE/SPECS[name]['asset']),'source_reuse':True}
    out=HERE/'plots'/ (digest({'matrix':m,'renderer':'directed-v1'})+'.png');side=out.with_suffix('.json')
    if not(out.exists() and side.exists()):
        out.parent.mkdir(exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='route-input-',dir=HERE/'plots',delete=False) as f:
            json.dump({'matrix':m,'output':str(out)},f);tmp=Path(f.name)
        try:subprocess.run([sys.executable,str(HERE/'render_routes.py'),str(tmp)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        finally:tmp.unlink(missing_ok=True)
    return {'prompt':str(out),'source_reuse':False}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('invalid level')
    names=[k for k,v in TEMPLATES.items() if v==level]
    if field_type: names=[k for k in names if ('blank' if k.startswith('blanks') else 'radio')==field_type.split('/')[-1]]
    rng=random.Random(seed);name=template or rng.choice(names)
    if name not in names:raise ValueError('template/field type does not belong to level')
    kind='blank' if name.startswith('blanks') else 'radio'
    profile=profile or ('observed' if kind=='blank' else 'authored_omissions')
    raw=profile=='raw_solution_319429'
    allowed=('observed','raw_solution_319429') if kind=='blank' else ('authored_omissions','observed_'+SPECS[name]['source'][2:] if name in SPECS else '')
    if profile not in allowed or raw and name!='blanks_319429':raise ValueError('incompatible profile')
    explicit=parameters is not None
    for attempt in range(10000):
        p=json.loads(json.dumps(parameters)) if explicit else sample(level,name,rng)
        try:
            guard(level,name,p,profile.startswith('observed'))
            m=p['matrix'];holes=p['holes'];rows=p['row_order'];cols=p['col_order'];v=[m[r][c] for r,c in holes];correct=int(sp.Add(*v))
            if kind=='blank':banks=[[str(x)] for x in v]
            elif profile.startswith('observed_'):
                # Observed finite count windows: no inferred misconception recipe.
                source=SOURCES[SPECS[name]['source']];bank=[str(i) for i in sorted({int(a[':answer/value']) for a in source[':question/answer-fields'][0][':answer-field/choices']})]
                if str(correct) not in bank:raise ValueError('correct sum outside observed finite bank')
                banks=[bank]
            else:
                bank=[correct,v[0]+v[1],v[0]+v[2],sum(m[c][r] for r,c in holes),sum(map(sum,m))]
                if len(set(bank))!=5:raise ValueError('whole authored omission bank collision')
                banks=[list(map(str,bank))]
            break
        except (ValueError,KeyError):
            if explicit:raise
    else:raise ValueError('sampler exhausted')
    assets=render_plots(name,m)
    if name in SPECS:
        prompt=_fill_mask(PROMPT_MASKS[name],m,holes,kind)
        prompt=re.sub(r'!\[\]\(.*?\)','![]('+assets['prompt']+')',prompt,count=1)
    else:
        prompt='![]('+assets['prompt']+')\n\nThe diagram above shows train routes between four stations, where nodes represent the stations and arrows represent the directed routes between them. The (incomplete) route matrix below represents information about the number of routes between each of the four stations. Find the value of $a+b+c.$\n\n'+table(m,holes,'radio',rows,cols)
    worked=solution(name,m,holes,kind,rows,cols,raw)
    # Complete assessed diagram/order/unknown positions; profile and seed excluded.
    math_fingerprint=digest({'matrix':m,'holes':holes,'rows':rows,'cols':cols,'response':kind})
    content={'version':VERSION,'prompt':prompt,'solution':worked,'banks':banks,'field_type':kind}
    qid=uid(digest(content));fields=[]
    for i,bank in enumerate(banks):
        key='field-'+str(i+1) if kind=='blank' else 'selection';fid=uid(qid+':'+key)
        answers=[{':answer/id':uid(fid+':'+x),':answer/type':':answer.type/math',':answer/value':x} for x in bank]
        correct_value=str(v[i]) if kind=='blank' else str(correct)
        cid=next(a[':answer/id'] for a in answers if a[':answer/value']==correct_value)
        if kind=='radio':random.Random(seed).shuffle(answers)
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':fields},'generation':{'version':VERSION,'template':name,'level':level,'seed':seed,'parameters':p,'bank_profile':profile,'origin':'observed template' if name in SPECS else 'authored missing-level template','bank_origin':('authored complete omission/direction bank' if profile=='authored_omissions' else 'observed blank counts' if kind=='blank' else 'observed finite count catalog'),'bank_recipes':(['sum_three','omit_third','omit_second','reverse_three_directions','count_all_routes'] if profile=='authored_omissions' else ['required_entry']*3 if kind=='blank' else ['enumerate_complete_observed_catalog']),'domain':{'station_count':len(m),'count_range':[0,3],'max_total_routes':16},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'mathematical_fingerprint':math_fingerprint,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_ids':[SPECS[name]['source']] if name in SPECS else [],'assets':assets,'source_repairs':['B-to-B direction in second solution bullet'] if name=='blanks_319429' and not raw else []}}

# EASY: observed route count blanks and sums, fixed ordinary headings.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed HTML table with three directed/diagonal counts.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored independent row and column order, still only direct-route counts.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        for rec in records:
            q=rec['question'];print(q[':question/problem'])
            for f in q[':question/answer-fields']:print('\n'+f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']))
            print('\n'+q[':question/worked-solution']+'\n')
if __name__=='__main__':main()

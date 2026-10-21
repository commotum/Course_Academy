#!/usr/bin/env python3
"""Generate offered-entry-operation questions about row echelon form."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import checked_math_content, matrix_tex

HERE = Path(__file__).resolve().parent
KP_ID = 17592186129115
KP_UUID = uuid.UUID('fe0050b2-b5bc-54a6-aeaf-94cd5d7e5dfb')
VERSION = 'entry-removal-v4-offered-operations'

def erase(matrix, entries):
    entries = {tuple(x) for x in entries}
    return [[0 if (i,j) in entries else v for j,v in enumerate(row)] for i,row in enumerate(matrix)]

def leading(matrix):
    return [next((j for j,v in enumerate(row) if v),len(row)) for row in matrix]

def echelon(matrix):
    pivots = leading(matrix)
    nz = [p for p in pivots if p < len(matrix[0])]
    return pivots == nz + [len(matrix[0])] * (len(pivots)-len(nz)) and all(a < b for a,b in zip(nz,nz[1:]))

def entry_text(entries):
    labels = ['$a_{'+str(i+1)+str(j+1)+'}$' for i,j in entries]
    if len(labels)==1:
        return labels[0]
    if len(labels)==2:
        return ' and '.join(labels)
    return ', '.join(labels[:-1])+', and '+labels[-1]

def explanation(matrix, correct):
    corrected = erase(matrix,correct)
    pivots = [p+1 for p in leading(corrected) if p<4]
    return ('Notice that by replacing '+entry_text(correct)+' with $0$, we get a matrix in row echelon form:\n\n$$\n'+
            'A='+matrix_tex(matrix)+r'\,\longrightarrow\,'+matrix_tex(corrected)+'\n$$\n\n'+
            'The nonzero rows have leading entries in columns '+', '.join(map(str,pivots))+
            ', in strictly increasing order, and all zero rows are at the bottom. '+
            'The other options will not give us a matrix in row echelon form.')

def fingerprint_data(matrix, correct):
    return hashlib.sha256(json.dumps([leading(matrix),correct,leading(erase(matrix,correct))],sort_keys=True).encode()).hexdigest()

@checked_math_content
def generate(difficulty, seed, profile=None, parameters=None, replay=False):
    if difficulty != 'moderate':
        raise ValueError('Only moderate is supported')
    sources = json.loads((HERE/'source-banks.json').read_text())
    source = next((x for x in sources if profile in (x['source_id'], x['source_label'])), None)
    if profile not in (None, 'offered-entries', 'minimum-entries') and source is None:
        raise ValueError('Unknown source profile')
    rng = random.Random(seed)
    if replay:
        if source is None or parameters is not None:
            raise ValueError('Replay requires a source profile and no explicit parameters')
        parameters = {'matrix':source['matrix'], 'bank':source['bank']}
    elif parameters is None:
        role = rng.choice(json.loads((HERE/'catalogue.json').read_text()))
        mask = rng.choice(role['masks'])
        structure = [[int(bool(mask & (1<<(4*i+j)))) for j in range(4)] for i in range(4)]
        cells = [(i,j) for i in range(4) for j in range(4)]
        operations = [list(map(list,b)) for size in (1,2,3) for b in itertools.combinations(cells,size)]
        good = [b for b in operations if echelon(erase(structure,b))]
        wrong = [b for b in operations if not echelon(erase(structure,b))]
        # Choose the successful offered operation before incidental magnitudes.
        size = rng.choice(sorted({len(b) for b in good}))
        correct = rng.choice([b for b in good if len(b)==size])
        matrix = [[rng.choice([n for n in range(-9,10) if n]) if structure[i][j] else 0 for j in range(4)] for i in range(4)]
        # Nearby coordinate substitutions are plausible competing operations.
        # Use both sides of the coordinate ordering where mathematically
        # available, rather than mostly selecting unrelated top-row erasures.
        zero_count = sum(not structure[i][j] for i,j in correct)
        same_size = [b for b in wrong if len(b)==size and
                     sum(not structure[i][j] for i,j in b)==zero_count]
        below = [b for b in same_size if b < correct][-12:]
        above = [b for b in same_size if b > correct][:12]
        distractors = []
        for _ in range(4):
            sides = [side for side in (below,above) if side]
            side = rng.choice(sides)
            candidate = rng.choice(side)
            side.remove(candidate)
            distractors.append(candidate)
        bank = distractors+[correct]
        rng.shuffle(bank)
        parameters = {'matrix':matrix,'bank':bank}
    parameters = json.loads(json.dumps(parameters))
    matrix,bank = parameters['matrix'],parameters['bank']
    if len(matrix)!=4 or any(len(row)!=4 for row in matrix) or any(type(v) is not int for row in matrix for v in row):
        raise ValueError('Expected a 4x4 integer matrix')
    if echelon(matrix):
        raise ValueError('Expected a matrix that is not already in row echelon form')
    if len(bank)!=5 or len({tuple(sorted(map(tuple,b))) for b in bank})!=5:
        raise ValueError('Expected five distinct options')
    if any(len(b)!=len(set(map(tuple,b))) or any(i not in range(4) or j not in range(4) for i,j in b) for b in bank):
        raise ValueError('Options must identify distinct in-range matrix entries')
    good = [i for i,b in enumerate(bank) if echelon(erase(matrix,b))]
    if len(good)!=1:
        raise ValueError('Expected exactly one offered operation that produces row echelon form')
    ci = good[0]
    correct = bank[ci]
    prompt = ('Consider the matrix $A$ given below.\n'
              'Which entries of $A$ could be replaced by $0$ in order to get a matrix in row echelon form?'
              '\n\n$$\nA='+matrix_tex(matrix)+'\n$$')
    solution = explanation(matrix,correct)
    values = [entry_text(b)+' only' for b in bank]
    qid = str(uuid.uuid5(KP_UUID,json.dumps({'problem':prompt,'solution':solution,'choices':sorted(values),'correct':values[ci]},sort_keys=True)))
    fid = str(uuid.uuid5(uuid.UUID(qid),'field/selection'))
    answers = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/text',':answer/value':v} for v in values]
    question = {':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',
                ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}]}
    return {'question':question,'knowledge_point':{'db_id':KP_ID,'id':str(KP_UUID),'title':'Identifying Operations That Would Transform a Matrix To Row Echelon Form'},
            'generation':{'version':VERSION,'template':'replace-entries-4x4','profile':source['source_id'] if replay else 'offered-entries','seed':seed,'parameters':parameters,
                          'source_refs':[x['source_id'] for x in sources], 'replay':replay, 'mathematical_fingerprint':fingerprint_data(matrix,correct),'dependencies':{},'assets':[]}}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',required=True,choices=['moderate'])
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--format',choices=['json','markdown'],default='json')
    args = parser.parse_args()
    if args.count<1:
        parser.error('count must be positive')
    records=[];seen=set()
    for offset in range(max(100,20*args.count)):
        record=generate(args.difficulty,args.seed+offset)
        fp=record['generation']['mathematical_fingerprint']
        if fp not in seen:
            records.append(record);seen.add(fp)
        if len(records)==args.count:
            break
    if len(records)!=args.count:
        parser.error('finite semantic support exhausted')
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+ '\n'.join('- '+a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+r['question'][':question/worked-solution'] for r in records))

if __name__=='__main__':
    main()

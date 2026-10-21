#!/usr/bin/env python3
"""Generate 4x4 REF questions with one globally minimum correction set."""
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
VERSION = 'entry-removal-v3-minimum'

def erase(matrix, entries):
    entries = {tuple(x) for x in entries}
    return [[0 if (i,j) in entries else v for j,v in enumerate(row)] for i,row in enumerate(matrix)]

def leading(matrix):
    return [next((j for j,v in enumerate(row) if v),len(row)) for row in matrix]

def echelon(matrix):
    pivots = leading(matrix)
    nz = [p for p in pivots if p < len(matrix[0])]
    return pivots == nz + [len(matrix[0])] * (len(pivots)-len(nz)) and all(a < b for a,b in zip(nz,nz[1:]))

def minimum_sets(matrix):
    """Enumerate possible row pivots; each pivot determines necessary erasures.

    Entries to the right of a surviving pivot never need removal. Every
    minimum solution therefore occurs in this complete pivot enumeration,
    including solutions that remove entries in the first row or erase a row.
    """
    width = len(matrix[0])
    candidates = []
    def visit(i, previous, removed):
        if i == len(matrix):
            candidates.append(tuple(removed))
            return
        row = matrix[i]
        for pivot in [j for j,v in enumerate(row) if v and previous < j] + [width]:
            if previous == width and pivot != width:
                continue
            changes = [(i,j) for j,v in enumerate(row) if v and j < pivot]
            visit(i+1, pivot, removed+changes)
    visit(0, -1, [])
    size = min(map(len,candidates))
    return [list(map(list,b)) for b in sorted(set(candidates)) if len(b)==size]

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
    changes = 'this entry' if len(correct)==1 else 'these '+str(len(correct))+' entries'
    reasons = []
    for i,j in correct:
        restored = [row[:] for row in corrected]
        restored[i][j] = matrix[i][j]
        lp = leading(restored)
        conflict = next((k for k in range(1,4) if lp[k]<4 and lp[k]<=lp[k-1]),None)
        if conflict is not None:
            if lp[conflict-1]==4:
                reason='would put a nonzero row below a zero row'
            else:
                reason=('would put the leading entry of row '+str(conflict+1)+' in column '+str(lp[conflict]+1)+
                        ', which is not to the right of the leading entry in row '+str(conflict))
            reasons.append('Restoring '+entry_text([[i,j]])+' '+reason+'.')
    necessity = ('The original matrix is not in row echelon form, so at least one replacement is needed.' if len(correct)==1 else
                 'No set with fewer than '+str(len(correct))+' replacements satisfies both the leading-entry order and zero-row conditions.')
    return ('The minimum set is '+entry_text(correct)+'. Replace '+changes+
            ' with $0$:\n\n$$\n'+matrix_tex(matrix)+r'\,\longrightarrow\,'+
            matrix_tex(corrected)+'\n$$\n\nThe nonzero rows have leading entries in columns '+
            ', '.join(map(str,pivots))+', in strictly increasing order, and all zero rows are at the bottom. '+
            '\n\n'+' '.join(reasons)+' '+necessity+
            '\n\nEntries to the right of a leading entry may remain nonzero.')

def fingerprint_data(matrix, correct):
    return hashlib.sha256(json.dumps([leading(matrix),correct,leading(erase(matrix,correct))],sort_keys=True).encode()).hexdigest()

@checked_math_content
def generate(difficulty, seed, profile=None, parameters=None, replay=False):
    if difficulty != 'moderate':
        raise ValueError('Only moderate is supported')
    if replay or profile not in (None, 'minimum-entries'):
        raise ValueError('Legacy nonminimum profiles are not served')
    rng = random.Random(seed)
    if parameters is None:
        role = rng.choice(json.loads((HERE/'catalogue.json').read_text()))
        mask = rng.choice(role['masks'])
        matrix = [[rng.choice([n for n in range(-9,10) if n]) if mask & (1<<(4*i+j)) else 0 for j in range(4)] for i in range(4)]
        correct = role['targets']
        cells = [(i,j) for i in range(4) for j in range(4) if matrix[i][j]]
        wrong = [list(map(list,b)) for b in itertools.combinations(cells,len(correct)) if not echelon(erase(matrix,b))]
        bank = rng.sample(wrong,4)+[correct]
        rng.shuffle(bank)
        parameters = {'matrix':matrix,'bank':bank}
    parameters = json.loads(json.dumps(parameters))
    matrix,bank = parameters['matrix'],parameters['bank']
    if len(matrix)!=4 or any(len(row)!=4 for row in matrix) or any(type(v) is not int for row in matrix for v in row):
        raise ValueError('Expected a 4x4 integer matrix')
    minimum = minimum_sets(matrix)
    if echelon(matrix) or len(minimum)!=1 or len(minimum[0]) not in (1,2,3):
        raise ValueError('Expected one unique minimum correction of one to three entries')
    correct = minimum[0]
    if len(bank)!=5 or len({tuple(sorted(map(tuple,b))) for b in bank})!=5:
        raise ValueError('Expected five distinct options')
    if any(len(b)!=len(set(map(tuple,b))) or any(i not in range(4) or j not in range(4) or not matrix[i][j] for i,j in b) for b in bank):
        raise ValueError('Options must identify distinct nonzero matrix entries')
    good = [i for i,b in enumerate(bank) if echelon(erase(matrix,b))]
    if len(good)!=1 or sorted(bank[good[0]])!=correct:
        raise ValueError('The sole valid option must be the global minimum, without redundant removals')
    ci = good[0]
    prompt = ('Consider the matrix $A$ below. Which set of entries should be replaced by $0$ to obtain row echelon form '
              '**using the fewest replacements**? Leave all other entries unchanged.\n\n$$\nA='+matrix_tex(matrix)+'\n$$')
    solution = explanation(matrix,correct)
    values = [entry_text(b) for b in bank]
    qid = str(uuid.uuid5(KP_UUID,json.dumps({'problem':prompt,'solution':solution,'choices':sorted(values),'correct':values[ci]},sort_keys=True)))
    fid = str(uuid.uuid5(uuid.UUID(qid),'field/selection'))
    answers = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/text',':answer/value':v} for v in values]
    question = {':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',
                ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}]}
    return {'question':question,'knowledge_point':{'db_id':KP_ID,'id':str(KP_UUID),'title':'Identifying Operations That Would Transform a Matrix To Row Echelon Form'},
            'generation':{'version':VERSION,'template':'replace-entries-4x4-minimum','profile':'minimum-entries','seed':seed,'parameters':parameters,
                          'mathematical_fingerprint':fingerprint_data(matrix,correct),'dependencies':{},'assets':[]}}

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

"""Exercise the new selected-operation solution path after row relabeling."""
from pathlib import Path
import validate as t

def main():
    records = []
    for sid in t.g.CASES:
        for n, key in enumerate(t.g.eligible_keys(sid)):
            permutation = list(t.g.itertools.permutations(range(3)))[n % 5 + 1]
            p = t.g.domain(sid)[0][:4] + [permutation] + [key]
            rec = t.g.generate(parameters=p)
            t.inspect(rec)
            records.append(rec)
    out = Path(__file__).resolve().parents[1] / 'evidence'
    t.save(out / 'permuted-role-records.json', records)
    t.save(out / 'permuted-role-native-input.json', [t.v.native('permuted role ' + str(i), r) for i, r in enumerate(records)])
    print('Permuted new-role cases:', len(records))

if __name__ == '__main__':
    main()

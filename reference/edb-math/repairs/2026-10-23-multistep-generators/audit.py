"""Trace excluded-source references in runtime closures and retained live records."""
import ast
from collections import defaultdict
import json
from pathlib import Path
import sys

H=Path(__file__).resolve().parent;ROOT=H.parents[3];MATH=Path('/media/jake/SSD/EDB/math')
sys.path.insert(0,str(ROOT/'scripts'))
from generator_source_policy import source_references


def save(name,value):(H/name).write_text(json.dumps(value,indent=2)+'\n')


def main():
    excluded=json.loads((H/'excluded-sources.json').read_text())['records']
    aliases={str(r[k]):r for r in excluded for k in (':db/id',':question/id',':question/math-academy-id') if k in r}
    registrations=json.loads((H/'registrations.json').read_text())
    runtime=[]
    for row in registrations:
        reg=row[':knowledge-point/question-generator'];ref=reg[':question-generator/script']
        path=(MATH if ref.startswith('generators/') else ROOT)/ref
        paths=[path]
        if ref.startswith('generators/'):
            package=MATH/Path(*Path(ref).parts[:3])
            manifest=json.loads((package/'generator-package.json').read_text())
            paths=[package/p for p in manifest['files'] if p.endswith(('.py','.json'))]
        hits=[]
        for file in paths:
            text=file.read_text()
            if file.suffix=='.py':
                try:tree=ast.parse(text)
                except SyntaxError:continue
                literals={str(n.value) for n in ast.walk(tree) if isinstance(n,ast.Constant)}
                for literal in sorted(literals & aliases.keys()):
                    hits.append({'file':str(file),'reference':literal,'source':aliases[literal][':question/math-academy-id']})
            else:
                # JSON captures can include unused historical evidence. Retain
                # them separately rather than asserting that each is served.
                found=[key for key in aliases if key in text]
                if found:hits.append({'file':str(file),'data_references':sorted({aliases[k][':question/math-academy-id'] for k in found})})
        if hits:runtime.append({'kp':row[':db/id'],'title':row[':knowledge-point/title'],'registration':reg,'hits':hits})
    save('runtime-candidates.json',runtime)
    current={q[':question/id']:q for q in json.loads((H/'generated-questions.json').read_text())}
    proofs=defaultdict(list);affected={};errors=[];count=0
    paths=Path('/tmp/multistep-lineage-files.txt').read_text().splitlines()
    for filename in paths:
        path=ROOT/filename
        try:data=json.loads(path.read_text())
        except (OSError,ValueError) as e:errors.append({'path':filename,'error':str(e)});continue
        pending=[data]
        while pending:
            item=pending.pop()
            if isinstance(item,dict):
                question=item.get('question');generation=item.get('generation')
                if isinstance(question,dict) and isinstance(generation,dict):
                    qid=str(question.get(':question/id'))
                    if qid in current:
                        refs=source_references(item);bad=sorted(refs & aliases.keys())
                        evidence={'path':filename,'generation':generation,'source_refs':sorted(refs),'excluded_refs':bad}
                        if evidence not in proofs[qid]:proofs[qid].append(evidence)
                        if bad:affected[qid]={**current[qid],'excluded_sources':sorted({aliases[r][':question/math-academy-id'] for r in bad})}
                        count+=1
                else:pending.extend(item.values())
            elif isinstance(item,list):pending.extend(item)
    save('live-lineage.json',dict(proofs));save('affected-questions.json',list(affected.values()));save('lineage-read-errors.json',errors)
    summary={'excluded_source_questions':len(excluded),'runtime_candidate_kps':len(runtime),
             'live_questions_with_retained_generation_metadata':len(proofs),'retained_records_examined':count,
             'confirmed_affected_questions':len(affected),'already_retired':sum(q.get(':question/retired') is True for q in affected.values()),
             'lineage_files':len(paths),'file_errors':len(errors)}
    save('audit-summary.json',summary);print(json.dumps(summary))
    for row in runtime:
        code=sorted({hit['source'] for hit in row['hits'] if 'source' in hit})
        print(row['kp'],row['title'],code)


if __name__=='__main__':main()

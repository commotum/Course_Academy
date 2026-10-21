"""Review/publish only an already repaired package; never launches an author or queue."""
from pathlib import Path
import json
import sys

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from generator_pipeline import Pipeline, CodexSession, digest, read
from generator_publish import Publisher


class ReviewedManualRepair(Pipeline):
    def repair(self, feedback):
        super().repair(feedback)
        # Return actionable review feedback to the human-directed repair turn.
        # Starting another author session would duplicate the current author.
        self.persist(stage='failed', manual_revision_required=True)


if __name__ == '__main__':
    directory = Path(__file__).resolve().parent/sys.argv[1]
    publisher = Publisher.from_environment()
    state = read(directory/'job.json')
    pipeline = ReviewedManualRepair(directory,state['request'],publisher,environment=publisher.client.environment)
    if sys.argv[2] == 'sample':
        pipeline.ensure_inventory()
        pipeline.persist(attempt=pipeline.state.get('attempt',0)+1,manifest='package.json')
        candidate = pipeline.candidate_hash()
        pipeline.sample()
        pipeline.persist(stage='validate',package_hash=candidate,error=None,manual_revision_required=False)
        print(json.dumps({'stage':'validate','package_hash':candidate,'batch':str(directory/'samples.json')}))
    else:
        result = pipeline.run('validate' if sys.argv[2]=='review' else 'push')
        print(json.dumps({k:result.get(k) for k in ['stage','package_hash','registration','error']},default=str))
        if result['stage'] in {'failed','unsupported'}:sys.exit(1)

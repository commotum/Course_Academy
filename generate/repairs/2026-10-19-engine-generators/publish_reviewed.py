"""Publish this session's completed reviews via the existing guarded pipeline."""
from pathlib import Path
import json
import shutil
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from generator_pipeline import Pipeline, read
from generator_publish import Publisher
from generator_review import validate_review

class CompletedCurrentSessionReview:
    """Consume the current session's actual review; never start another agent."""
    def __init__(self, original):self.original=original
    def __call__(self, role, context, directory):
        assert role=='review','No authoring or other agents are permitted by this scoped publisher'
        validate_review(read(self.original/'result.json'),self.original)
        shutil.copytree(self.original,directory,dirs_exist_ok=True)
        return read(Path(directory)/'result.json')

class ManualRepair(Pipeline):
    def repair(self, feedback):
        super().repair(feedback)
        self.persist(stage='failed',manual_revision_required=True)

if __name__=='__main__':
    publisher=Publisher.from_environment()
    for kp in [17592186096617,17592186096618,17592186092261,17592186096842]:
        directory=Path(__file__).resolve().parent/str(kp)
        state=read(directory/'job.json')
        pipeline=ManualRepair(directory,state['request'],publisher,environment=publisher.client.environment,
            session=CompletedCurrentSessionReview(directory/'independent-review'))
        result=pipeline.run('validate' if sys.argv[1]=='review' else 'push')
        print(json.dumps({k:result.get(k) for k in ['stage','registration','error']},default=str),flush=True)
        if result['stage'] in ['failed','unsupported']:sys.exit(1)

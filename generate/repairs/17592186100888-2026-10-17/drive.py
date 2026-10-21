"""Run this repair through the existing pipeline using saved author/reviewer results."""
import argparse
import json
from pathlib import Path
import shutil
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_pipeline import Pipeline, read
from generator_publish import Publisher
from serve_graph_explorer import database_environment


def saved_session(role, context, directory):
    if role == 'author':
        return read(BASE / 'workspace/author-result.json')
    return read(Path(directory) / 'result.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('sample', 'publish'))
    args = parser.parse_args()
    env = database_environment('math')
    publisher = Publisher.from_environment(environment=env)
    manifest = read(BASE / 'workspace/package.json')
    contexts = []
    for band in ('easy', 'moderate', 'hard'):
        directory = BASE / 'bands' / band
        if not (directory / 'job.json').exists():
            (directory / 'source').mkdir(parents=True, exist_ok=True)
            for name in ('source.json', 'inventory.json'):
                shutil.copy2(BASE / 'source' / name, directory / 'source' / name)
            workspace = directory / 'workspace'
            workspace.mkdir(parents=True, exist_ok=True)
            for name in [*manifest['files'], 'package.json', 'author-result.json', 'instructional-account.md']:
                source = BASE / 'workspace' / name
                if source.is_file():
                    destination = workspace / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
        request = {'kp': 17592186100888, 'difficulty': band, 'count': 5,
                   'existing_entrypoint': str(BASE / 'workspace' / manifest['entrypoint'])}
        pipeline = Pipeline(directory, request, publisher, environment=env, session=saved_session)
        state = pipeline.run('generate' if args.phase == 'sample' else 'push')
        contexts.append(pipeline.context(pipeline.review_directory()))
        print(json.dumps({'band': band, 'stage': state['stage'], 'package_hash': state.get('package_hash'),
                          'publication': state.get('publication')}), flush=True)
        if state['stage'] not in ('validate', 'verified'):
            raise RuntimeError(f'{band}: {state.get("error")}')
    if args.phase == 'sample':
        (BASE / 'review-contexts.json').write_text(json.dumps(contexts, indent=2) + '\n')


if __name__ == '__main__':
    main()

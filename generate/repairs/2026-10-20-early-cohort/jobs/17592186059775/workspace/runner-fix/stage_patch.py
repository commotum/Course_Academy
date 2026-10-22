"""Stage a proposed runner change; never install it or change the package."""
import difflib
import hashlib
import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]
RUNNER = Path('/home/jake/Developer/Course_Academy/scripts/generator_pipeline.py')

METHOD = '''    def evidence_only_rejection(self):
        """An evidence-only revise may retain runtime bytes, never approval.

        Require the complete prior binding and a valid independent report.
        The caller still runs retained regressions, samples, and requests a
        fresh review. Historical content/grading findings remain regressions.
        """
        if self.is_refill or self.state.get('review_after_publication'):
            return False
        previous = self.state.get('previous_review') or {}
        if previous.get('binding') != self.review_binding():
            return False
        try:
            directory = inside(self.directory, previous['directory'])
            report = read(directory / 'result.json')
            validate_review(report, directory)
            findings = report.get('findings')
            return (report.get('verdict') == 'revise'
                    and isinstance(findings, list) and bool(findings)
                    and all(finding.get('kind') == 'evidence'
                            for finding in findings))
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            return False

'''


def build(source):
    anchor = '    def check_repair_regressions(self):\n'
    old = "                            and self.engine_identity() == self.state.get('last_rejected_engine')):"
    new = "                            and self.engine_identity() == self.state.get('last_rejected_engine')\n                            and not self.evidence_only_rejection()):"
    assert source.count(anchor) == source.count(old) == 1, 'Runner changed; inspect before restaging'
    return source.replace(anchor, METHOD + anchor).replace(old, new)


def main():
    source = RUNNER.read_text()
    proposed = build(source)
    compile(proposed, str(RUNNER), 'exec')
    patch = ''.join(difflib.unified_diff(
        source.splitlines(keepends=True), proposed.splitlines(keepends=True),
        fromfile='a/scripts/generator_pipeline.py', tofile='b/scripts/generator_pipeline.py'))
    target = WORKSPACE/'runner-fix/evidence-only-rejection.patch'
    target.write_text(patch)
    metadata = {
        'target': 'scripts/generator_pipeline.py',
        'base_sha256': hashlib.sha256(source.encode()).hexdigest(),
        'proposed_sha256': hashlib.sha256(proposed.encode()).hexdigest(),
        'patch_sha256': hashlib.sha256(patch.encode()).hexdigest(),
        'installed': False,
        'approval': 'Fresh independent review still required; no historical acceptance is installed.'}
    (WORKSPACE/'runner-fix/patch.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print(json.dumps(metadata))


if __name__ == '__main__':
    main()

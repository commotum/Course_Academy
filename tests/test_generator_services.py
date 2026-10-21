"""Persistent service definitions survive a successful boundary exit."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import generator_services as S


class GeneratorServiceTests(unittest.TestCase):
    def test_definition_persists_and_start_uses_a_named_unit(self):
        with tempfile.TemporaryDirectory() as t, patch.object(S, 'ROOT', Path(t)):
            run = Mock()
            directory = Path(t) / '2026-10-20-early-cohort'
            S.start_cohort(directory, runner=run)
            path = Path(t) / '.local/generator-services/course-academy-generator-cohort-20261020.service'
            self.assertTrue(path.is_file())
            body = path.read_text()
            self.assertIn('Restart=on-failure', body)
            self.assertIn('KillMode=mixed', body)
            self.assertIn('[Install]\nWantedBy=default.target', body)
            self.assertIn('generator_cohort.py', body)
            self.assertIn('"--workers" "3"', body)
            self.assertIn(str(directory), body)
            commands = [c.args[0] for c in run.call_args_list]
            self.assertEqual(commands[0], ['systemctl','--user','link','--force',str(path)])
            self.assertEqual(commands[-1], ['systemctl','--user','start',path.name])
            self.assertEqual(commands[-2], ['systemctl','--user','enable',path.name])
            self.assertFalse(any('stop' in c or 'systemd-run' in c for c in commands))
            # A second start still has the actual on-disk definition.
            S.start_cohort(directory, runner=run)
            self.assertEqual(path.read_text(), body)

    def test_unit_arguments_are_escaped_and_multiline_commands_rejected(self):
        body = S.unit_text(['/path with spaces/python','say "$HOME" 50%'], '/task path', 'test')
        self.assertIn('"/path with spaces/python"', body)
        self.assertIn('$$HOME', body)
        self.assertIn('50%%', body)
        with self.assertRaises(ValueError):
            S.unit_text(['safe\nExecStart=unsafe'], '/task', 'test')
        with self.assertRaises(ValueError):
            S.install('../../unrelated.service', ['true'])


if __name__ == '__main__':
    unittest.main()

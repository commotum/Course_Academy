import concurrent.futures
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generator_packages import (
    MANIFEST, build_manifest, check_dependencies, materialize_package, package_digest,
    publish_package, resolve_registered_script, verify_package,
)


class GeneratorPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        self.math = self.root / "math"
        self.files = ["generator.py", "support/helper.py", "support/source.json", "requirements.lock"]
        (self.source / "support").mkdir()
        (self.source / "generator.py").write_text(
            "from pathlib import Path\n"
            "import json, sys\n"
            "here = Path(__file__).resolve().parent\n"
            "sys.path.insert(0, str(here / 'support'))\n"
            "from helper import answer\n"
            "data = json.loads((here / 'support/source.json').read_text())\n"
            "(here / 'plots').mkdir(exist_ok=True)\n"
            "(here / 'plots/question.svg').write_text('<svg>' + str(answer(data['n'])) + '</svg>')\n"
            "print(json.dumps({'answer': answer(data['n'])}))\n"
        )
        (self.source / "support/helper.py").write_text("def answer(n): return n * n\n")
        (self.source / "support/source.json").write_text('{"n": 7}\n')
        (self.source / "requirements.lock").write_text("# Standard library only.\n")
        self.dependencies = {"python": "3.12.3", "packages": {}}

    def tearDown(self):
        # Published directories intentionally deny writes, including cleanup.
        for path in self.root.rglob("*"):
            if path.is_dir() and not path.is_symlink():
                path.chmod(0o755)
        self.temp.cleanup()

    def publish(self, **kwargs):
        return publish_package(self.source, "generator.py", self.files, self.math,
                               dependencies=self.dependencies, **kwargs)

    def test_hash_covers_helpers_data_and_dependencies_but_not_scratch_outputs(self):
        original = package_digest(self.source, "generator.py", self.files, dependencies=self.dependencies)
        (self.source / "review.json").write_text('{"approved": true}')
        os.utime(self.source / "generator.py", (1, 1))
        reordered = package_digest(self.source, "generator.py", reversed(self.files), dependencies=self.dependencies)
        self.assertEqual(original, reordered)
        (self.source / "support/helper.py").write_text("def answer(n): return n + n\n")
        changed = package_digest(self.source, "generator.py", self.files, dependencies=self.dependencies)
        self.assertNotEqual(original, changed)
        with self.assertRaisesRegex(ValueError, "changed after approval"):
            self.publish(expected_digest=original)
        dep_changed = package_digest(self.source, "generator.py", self.files,
                                     dependencies={"python": "3.13.1", "packages": {}})
        self.assertNotEqual(changed, dep_changed)

    def test_concurrent_publish_is_idempotent_and_runtime_plot_does_not_change_package(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as workers:
            first, second = list(workers.map(lambda _: self.publish(), range(2)))
        self.assertEqual(first.reference, second.reference)
        self.assertEqual(first.directory, self.math / "generators" / first.digest[:2] / first.digest)
        self.assertEqual(resolve_registered_script(first.reference, self.source, self.math), first.script)
        self.assertEqual(first.directory.stat().st_mode & 0o222, 0)
        self.assertEqual(first.script.stat().st_mode & 0o222, 0)
        runtime = self.root / "execution"
        script = materialize_package(first.reference, self.math, runtime)
        result = subprocess.run([sys.executable, str(script)], cwd=runtime, check=True,
                                capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout), {"answer": 49})
        self.assertEqual((runtime / "plots/question.svg").read_text(), "<svg>49</svg>")
        self.assertFalse((first.directory / "plots").exists())
        self.assertEqual(verify_package(first.directory, first.digest).digest, first.digest)
        self.assertEqual(verify_package(runtime, first.digest, allow_outputs=True).digest, first.digest)
        with self.assertRaisesRegex(ValueError, "must be new"):
            materialize_package(first.reference, self.math, runtime)
        (runtime / "support/helper.py").write_text("def answer(n): return 999\n")
        with self.assertRaisesRegex(ValueError, "file changed"):
            verify_package(runtime, first.digest, allow_outputs=True)

    def test_registration_rejects_tampering_undeclared_files_and_wrong_entrypoint(self):
        package = self.publish()
        with self.assertRaisesRegex(ValueError, "not the package entrypoint"):
            resolve_registered_script(package.reference.replace("generator.py", "support/helper.py"), self.source, self.math)
        package.directory.chmod(0o755)
        (package.directory / "injected.py").write_text("print('not approved')")
        with self.assertRaisesRegex(ValueError, "Undeclared"):
            resolve_registered_script(package.reference, self.source, self.math)
        (package.directory / "injected.py").unlink()
        package.script.chmod(0o644)
        package.script.write_text("print('tampered')\n")
        with self.assertRaisesRegex(ValueError, "file changed"):
            resolve_registered_script(package.reference, self.source, self.math)
        with self.assertRaisesRegex(ValueError, "file changed"):
            self.publish()

    def test_symlinks_and_traversal_never_enter_or_resolve_from_package(self):
        outside = self.root / "outside.py"
        outside.write_text("pass\n")
        (self.source / "link.py").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Symlinks"):
            build_manifest(self.source, "link.py", ["link.py"])
        for name in ["../outside.py", "/etc/passwd", "support/../generator.py", "./generator.py", "support//helper.py"]:
            with self.subTest(name=name), self.assertRaises(ValueError):
                build_manifest(self.source, name, [name])
        package = self.publish()
        (self.source / "legacy.py").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Symlinks"):
            resolve_registered_script("legacy.py", self.source, self.math)
        with self.assertRaises(ValueError):
            resolve_registered_script("../outside.py", self.source, self.math)
        with self.assertRaises(ValueError):
            resolve_registered_script(package.reference.replace(package.digest[:2] + "/", "xx/", 1), self.source, self.math)
        linked_math = self.root / "linked-math"
        linked_math.mkdir()
        (linked_math / "generators").symlink_to(self.math / "generators")
        with self.assertRaisesRegex(ValueError, "Symlinks"):
            resolve_registered_script(package.reference, self.source, linked_math)

    def test_legacy_paths_work_and_manifest_cannot_claim_itself(self):
        self.assertEqual(resolve_registered_script("generator.py", self.source, self.math), self.source / "generator.py")
        with self.assertRaisesRegex(ValueError, "reserved"):
            build_manifest(self.source, "generator.py", ["generator.py", MANIFEST])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            build_manifest(self.source, "generator.py", ["generator.py", "generator.py"])
        with self.assertRaisesRegex(ValueError, "entrypoint"):
            build_manifest(self.source, "generator.py", ["requirements.lock"])

    def test_dependency_check_uses_selected_python_and_detects_environment_drift(self):
        actual = platform.python_version()
        observed = check_dependencies({"python": ".".join(actual.split(".")[:2]), "packages": {}}, sys.executable)
        self.assertEqual(observed, {"python": actual, "packages": {}})
        check_dependencies({"python": actual, "packages": {}}, sys.executable)
        with self.assertRaisesRegex(ValueError, "requires Python"):
            check_dependencies({"python": "0.0", "packages": {}}, sys.executable)
        with self.assertRaisesRegex(ValueError, "not installed"):
            check_dependencies({"python": actual, "packages": {"course-academy-package-test-missing": "1.0"}}, sys.executable)
        with patch("generator_packages.subprocess.run") as run:
            run.return_value.stdout = json.dumps({"python": actual, "packages": {"sympy": "1.14.0"}})
            with self.assertRaisesRegex(ValueError, "sympy==1.13.3"):
                check_dependencies({"python": actual, "packages": {"sympy": "1.13.3"}}, sys.executable)
        with self.assertRaisesRegex(ValueError, "exact installed"):
            check_dependencies({"python": actual, "packages": {"sympy": ">=1.13"}}, sys.executable)


if __name__ == "__main__":
    unittest.main()

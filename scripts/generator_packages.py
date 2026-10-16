"""Content-addressed generator packages and disposable execution copies.

The manifest covers every explicitly declared input, including local helpers,
renderers and dependency files. Callers must declare that complete closure: this
module deliberately does not guess Python imports or copy a scratch directory.
Approvals should retain ``manifest_digest(build_manifest(...))`` and pass it as
``expected_digest`` when publishing. Review records and generated output are not
part of a package.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
from typing import Iterable, Mapping


FORMAT = "course-academy-generator-package-v1"
MANIFEST = "generator-package.json"
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class GeneratorPackage:
    digest: str
    directory: Path
    entrypoint: str
    manifest: dict

    @property
    def reference(self) -> str:
        return f"generators/{self.digest[:2]}/{self.digest}/{self.entrypoint}"

    @property
    def script(self) -> Path:
        return self.directory / self.entrypoint


def _relative(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError(f"Invalid package path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value or any(p in {".", ".."} for p in path.parts):
        raise ValueError(f"Package path must be canonical and relative: {value!r}")
    if value == ".":
        raise ValueError("Package path must name a file")
    return value


def _inside(root: Path, relative: str) -> Path:
    """Resolve a relative path without accepting any symlink components."""
    relative = _relative(relative)
    path = root
    for part in PurePosixPath(relative).parts:
        path = path / part
        if path.is_symlink():
            raise ValueError(f"Symlinks are not allowed in generator paths: {path}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Generator path escapes its root: {relative}")
    return path


def _file_record(path: Path) -> dict:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"Generator input is not a regular file: {path}")
    value = path.read_bytes()
    return {"sha256": hashlib.sha256(value).hexdigest(), "bytes": len(value),
            "executable": bool(path.stat().st_mode & 0o111)}


def _validate_dependencies(value: object) -> None:
    if isinstance(value, str):
        return
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        for child in value.values():
            _validate_dependencies(child)
        return
    raise ValueError("Dependencies must contain names, version strings and nested mappings")


def build_manifest(source_root: Path, entrypoint: str, files: Iterable[str], *,
                   dependencies: Mapping[str, object] | None = None) -> dict:
    """Describe declared package inputs deterministically, without writing."""
    source_root = Path(source_root).resolve()
    entrypoint = _relative(entrypoint)
    names = [_relative(name) for name in files]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate package input")
    if MANIFEST in names:
        raise ValueError(f"{MANIFEST} is reserved for the generated manifest")
    if entrypoint not in names:
        raise ValueError("The entrypoint must be a declared package input")
    deps = dict(dependencies or {})
    _validate_dependencies(deps)
    return {"format": FORMAT, "entrypoint": entrypoint, "dependencies": deps,
            "files": {name: _file_record(_inside(source_root, name)) for name in sorted(names)}}


def manifest_digest(manifest: dict) -> str:
    encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def package_digest(source_root: Path, entrypoint: str, files: Iterable[str], *,
                   dependencies: Mapping[str, object] | None = None) -> str:
    """Hash the candidate before review, then bind publication to this digest."""
    return manifest_digest(build_manifest(source_root, entrypoint, files, dependencies=dependencies))


def check_dependencies(dependencies: Mapping[str, object], python_executable: str, *,
                       environment: Mapping[str, str] | None = None) -> dict:
    """Check the selected interpreter and exact installed versions; never install.

    Python may be pinned to major.minor or major.minor.patch. Third-party
    distributions require exact versions. Files such as fonts and local data
    belong in the declared package rather than unverifiable dependency labels.
    The observed versions can be retained alongside the review evidence.
    """
    if not isinstance(dependencies, dict) or set(dependencies) != {"python", "packages"}:
        raise ValueError("Dependencies must explicitly declare python and packages")
    version, packages = dependencies["python"], dependencies["packages"]
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", version):
        raise ValueError("Python dependency must pin major.minor or major.minor.patch")
    if not isinstance(packages, dict) or any(
        not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name)
        or not isinstance(pin, str) or not pin or re.search(r"[\s<>=!~*]", pin)
        for name, pin in packages.items()
    ):
        raise ValueError("Package dependencies must name exact installed distribution versions")
    probe = (
        "import importlib.metadata, json, platform, sys\n"
        "versions = {}\n"
        "for name in json.load(sys.stdin):\n"
        "    try: versions[name] = importlib.metadata.version(name)\n"
        "    except importlib.metadata.PackageNotFoundError: versions[name] = None\n"
        "print(json.dumps({'python': platform.python_version(), 'packages': versions}))\n"
    )
    try:
        result = subprocess.run([str(python_executable), "-I", "-c", probe],
                                input=json.dumps(sorted(packages)), capture_output=True,
                                text=True, check=True, timeout=30,
                                env=None if environment is None else dict(environment))
        observed = json.loads(result.stdout)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise ValueError(f"Cannot inspect generator Python dependencies: {error}") from error
    actual_python = observed.get("python", "")
    if not isinstance(actual_python, str) or not (actual_python == version or actual_python.startswith(version + ".")):
        raise ValueError(f"Generator requires Python {version}; selected interpreter has {actual_python}")
    actual_packages = observed.get("packages", {})
    for name, pin in packages.items():
        if actual_packages.get(name) != pin:
            actual = actual_packages.get(name) or "not installed"
            raise ValueError(f"Generator requires {name}=={pin}; selected interpreter has {actual}")
    return observed


def _fsync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _write(path: Path, value: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(value)
        stream.flush()
        os.fchmod(stream.fileno(), mode)
        os.fsync(stream.fileno())


def _remove_staging(path: Path) -> None:
    if path.exists():
        for directory in [path, *(p for p in path.rglob("*") if p.is_dir())]:
            directory.chmod(0o755)
        shutil.rmtree(path)


def _validate_manifest(manifest: dict) -> None:
    if not isinstance(manifest, dict) or set(manifest) != {"format", "entrypoint", "dependencies", "files"}:
        raise ValueError("Invalid generator manifest fields")
    if manifest["format"] != FORMAT or not isinstance(manifest["files"], dict):
        raise ValueError("Unsupported generator manifest")
    _relative(manifest["entrypoint"])
    if manifest["entrypoint"] not in manifest["files"] or MANIFEST in manifest["files"]:
        raise ValueError("Invalid generator entrypoint or reserved file")
    if not isinstance(manifest["dependencies"], dict):
        raise ValueError("Invalid dependency specification")
    _validate_dependencies(manifest["dependencies"])
    for name, record in manifest["files"].items():
        _relative(name)
        if (not isinstance(record, dict) or set(record) != {"sha256", "bytes", "executable"}
                or not isinstance(record["sha256"], str) or not _DIGEST.fullmatch(record["sha256"])
                or type(record["bytes"]) is not int or record["bytes"] < 0
                or type(record["executable"]) is not bool):
            raise ValueError(f"Invalid manifest record: {name}")


def verify_package(directory: Path, expected_digest: str | None = None, *,
                   allow_outputs: bool = False) -> GeneratorPackage:
    """Verify declared bytes; only runtime copies may contain extra output files.

    ``allow_outputs`` permits plot files and Python caches created during a run,
    while still rejecting changed inputs and symlinks. Published packages always
    use the strict default.
    """
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"Generator package is not a directory: {directory}")
    manifest_path = _inside(directory, MANIFEST)
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, ValueError) as error:
        raise ValueError(f"Cannot read generator manifest: {directory}") from error
    _validate_manifest(manifest)
    digest = manifest_digest(manifest)
    if expected_digest is not None and digest != expected_digest:
        raise ValueError("Generator manifest does not match its approved hash")
    allowed_files = {MANIFEST, *manifest["files"]}
    allowed_directories = set()
    for name in allowed_files:
        allowed_directories.update(str(p) for p in PurePosixPath(name).parents if str(p) != ".")
    for path in directory.rglob("*"):
        name = path.relative_to(directory).as_posix()
        if path.is_symlink() or not allow_outputs and (
            (path.is_dir() and name not in allowed_directories)
            or (not path.is_dir() and name not in allowed_files)
        ):
            raise ValueError(f"Undeclared file or symlink in generator package: {name}")
    for name, expected in manifest["files"].items():
        if _file_record(_inside(directory, name)) != expected:
            raise ValueError(f"Generator package file changed: {name}")
    return GeneratorPackage(digest, directory, manifest["entrypoint"], manifest)


def publish_package(source_root: Path, entrypoint: str, files: Iterable[str], math_root: Path, *,
                    dependencies: Mapping[str, object] | None = None,
                    expected_digest: str | None = None) -> GeneratorPackage:
    """Atomically publish exact bytes; retries verify and reuse the same package."""
    source_root, math_root = Path(source_root).resolve(), Path(math_root).resolve()
    manifest = build_manifest(source_root, entrypoint, files, dependencies=dependencies)
    digest = manifest_digest(manifest)
    if expected_digest is not None and digest != expected_digest:
        raise ValueError("Generator changed after approval")
    parent = _inside(math_root, f"generators/{digest[:2]}")
    parent.mkdir(parents=True, exist_ok=True)
    destination = _inside(math_root, f"generators/{digest[:2]}/{digest}")
    if destination.exists():
        return verify_package(destination, digest)
    staging = Path(tempfile.mkdtemp(prefix=".publishing-", dir=parent))
    try:
        for name, expected in manifest["files"].items():
            source = _inside(source_root, name)
            value = source.read_bytes()
            if hashlib.sha256(value).hexdigest() != expected["sha256"] or len(value) != expected["bytes"]:
                raise ValueError(f"Generator changed during publication: {name}")
            _write(staging / name, value, 0o555 if expected["executable"] else 0o444)
        _write(staging / MANIFEST, (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode(), 0o444)
        verify_package(staging, digest)
        for directory in sorted((p for p in staging.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
            directory.chmod(0o555)
            _fsync_directory(directory)
        staging.chmod(0o555)
        _fsync_directory(staging)
        try:
            staging.rename(destination)
        except OSError:
            if not destination.exists():
                raise
            # Another publisher may have installed the same content meanwhile.
            verify_package(destination, digest)
        _fsync_directory(parent)
        _fsync_directory(parent.parent)
        _fsync_directory(math_root)
        return verify_package(destination, digest)
    finally:
        _remove_staging(staging)


def _registered_package(reference: str, math_root: Path) -> GeneratorPackage:
    _relative(reference)
    parts = PurePosixPath(reference).parts
    if (len(parts) < 4 or parts[0] != "generators" or not _DIGEST.fullmatch(parts[2])
            or parts[1] != parts[2][:2]):
        raise ValueError("Invalid content-addressed generator reference")
    directory = _inside(Path(math_root).resolve(), "/".join(parts[:3]))
    package = verify_package(directory, parts[2])
    if "/".join(parts[3:]) != package.entrypoint:
        raise ValueError("Registered script is not the package entrypoint")
    return package


def resolve_registered_script(reference: str, repo_root: Path, math_root: Path) -> Path:
    """Resolve an approved package or a legacy repository-relative script."""
    _relative(reference)
    if reference.startswith("generators/"):
        return _registered_package(reference, math_root).script
    script = _inside(Path(repo_root).resolve(), reference)
    if not script.is_file():
        raise ValueError(f"Registered generator is not a file: {reference}")
    return script


def materialize_package(reference: str, math_root: Path, destination: Path) -> Path:
    """Create a fresh writable execution copy; an existing destination fails.

    Legacy generators often write plots relative to ``__file__``. Executing the
    returned entrypoint preserves that behavior without changing approved bytes.
    Use a new destination for each attempt, and retain it until its generated
    images have been published.
    """
    package = _registered_package(reference, math_root)
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ValueError("Generator runtime destination must be new")
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{destination.name}-", dir=destination.parent))
    try:
        for name, expected in package.manifest["files"].items():
            value = _inside(package.directory, name).read_bytes()
            if hashlib.sha256(value).hexdigest() != expected["sha256"]:
                raise ValueError(f"Published generator changed during materialization: {name}")
            _write(staging / name, value, 0o755 if expected["executable"] else 0o644)
        _write(staging / MANIFEST, (json.dumps(package.manifest, indent=2, sort_keys=True) + "\n").encode(), 0o644)
        verify_package(staging, package.digest)
        # Refuse accidental reuse rather than merge old output with new code.
        if destination.exists() or destination.is_symlink():
            raise ValueError("Generator runtime destination already exists")
        staging.rename(destination)
        return destination / package.entrypoint
    finally:
        _remove_staging(staging)

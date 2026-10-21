"""Persistent user-service definitions for resumable generator workers.

Unlike systemd-run transient units, these definitions remain startable after a
successful clean boundary stop. Installing a definition never stops a live job.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def unit_text(command, directory, description):
    if '\n' in description or '\r' in description:
        raise ValueError('Service description must fit one line')
    def quote(value):
        value = str(value)
        if any(c in value for c in '\n\r\0'):
            raise ValueError('Invalid service argument')
        return '"' + value.replace('\\', '\\\\').replace('"', '\\"').replace('%', '%%').replace('$', '$$') + '"'
    quote(directory)  # Validate; WorkingDirectory is a path, not an argv list.
    return ('[Unit]\nDescription=' + description.replace('%', '%%') + '\n'
            'StartLimitIntervalSec=300\nStartLimitBurst=5\n\n'
            '[Service]\nType=simple\nWorkingDirectory=' + str(directory).replace('%', '%%') + '\n'
            'ExecStart=' + ' '.join(map(quote, command)) + '\n'
            'Restart=on-failure\nRestartPreventExitStatus=78\nRestartSec=15\nKillMode=mixed\nTimeoutStopSec=30\n\n'
            '[Install]\nWantedBy=default.target\n')


def install(name, command, *, directory=ROOT, description='Course Academy generator worker', runner=subprocess.run):
    if not re.fullmatch(r'course-academy-generator-[A-Za-z0-9_-]+\.service', name):
        raise ValueError('Invalid generator service name')
    units = ROOT / '.local/generator-services'
    units.mkdir(parents=True, exist_ok=True)
    path = units / name
    temporary = path.with_suffix('.tmp')
    temporary.write_text(unit_text(command, directory, description))
    temporary.replace(path)
    runner(['systemctl', '--user', 'link', '--force', str(path)], check=True, capture_output=True, text=True)
    runner(['systemctl', '--user', 'daemon-reload'], check=True, capture_output=True, text=True)
    return path


def start_cohort(directory, *, runner=subprocess.run):
    directory = Path(directory).resolve()
    date = directory.name[:10].replace('-', '')
    if not re.fullmatch(r'\d{8}', date):
        raise ValueError('Cohort directory must begin with its YYYY-MM-DD date')
    name = 'course-academy-generator-cohort-' + date + '.service'
    install(name, [ROOT / '.venv/bin/python', '-u', ROOT / 'scripts/generator_cohort.py',
                  'run', '--directory', directory, '--workers', '3'],
            description='Review and repair the early generator cohort with three workers', runner=runner)
    runner(['systemctl', '--user', 'enable', name], check=True, capture_output=True, text=True)
    return runner(['systemctl', '--user', 'start', name], check=True, capture_output=True, text=True)

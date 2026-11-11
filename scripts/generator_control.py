"""Generic admission and completion messages to the generation supervisor.

The supervisor owns scheduling policy. Workers only ask to start a turn and
report its raw output location; neither prompts nor workers interpret capacity.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import time

CONTROL_ENV = 'COURSE_ACADEMY_GENERATOR_CONTROL_SOCKET'
PAUSED_EXIT = 76


class GenerationPaused(SystemExit):
    """A resumable administrative pause, never a content/process failure."""
    def __init__(self, reason='Generation supervisor stopped admissions'):
        self.reason = reason
        super().__init__(PAUSED_EXIT)


def request_parent(environment, message, *, timeout=10):
    name = environment.get(CONTROL_ENV)
    if not name:
        return {'action': 'continue'}
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
            connection.settimeout(timeout)
            connection.connect(name)
            connection.sendall((json.dumps(message, separators=(',', ':')) + '\n').encode())
            chunks = bytearray()
            while b'\n' not in chunks:
                part = connection.recv(4096)
                if not part:
                    raise ValueError('Supervisor closed its response')
                chunks.extend(part)
                if len(chunks) > 65536:
                    raise ValueError('Supervisor response is too large')
            response = json.loads(chunks.split(b'\n', 1)[0])
            if not isinstance(response, dict) or response.get('action') not in {'run', 'wait', 'continue', 'halt'}:
                raise ValueError('Invalid supervisor response')
            return response
    except (OSError, ValueError) as error:
        raise GenerationPaused('Generation supervisor is unavailable: ' + str(error)) from error


def admit_turn(environment, role, directory):
    if not environment.get(CONTROL_ENV):
        return None
    message = {'event': 'admit', 'pid': os.getpid(), 'role': role,
               'directory': str(Path(directory).resolve())}
    while True:
        response = request_parent(environment, message)
        if response['action'] == 'run' and isinstance(response.get('ticket'), str) and response['ticket']:
            return response['ticket']
        if response['action'] != 'wait':
            raise GenerationPaused(response.get('reason', 'Generation supervisor stopped admissions'))
        time.sleep(1)


def completion_message(ticket, directory, events_path, events_offset, returncode):
    return {'event': 'complete', 'ticket': ticket, 'pid': os.getpid(),
            'directory': str(Path(directory).resolve()),
            'events_path': str(Path(events_path).resolve()),
            'events_offset': events_offset, 'returncode': returncode}

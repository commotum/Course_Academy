"""Canonical remote-code decoding and exact-frame CLI relay."""
import hashlib
import os
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

from edb_transport import rejection_code, replay


def response(code='postgres/stale-basis'):
    code = code.encode()
    message = b'Expected basis differs from the serialized database value'
    body = b'\x06\x01\x04'+len(code).to_bytes(4, 'big')+code+len(message).to_bytes(4, 'big')+message+b'\0'*5
    blob = b'EDBC\x0c\x00\x03\x00'+len(body).to_bytes(8, 'big')+body
    return blob+hashlib.sha256(blob).digest()


class TransportTests(unittest.TestCase):
    def test_remote_code_requires_valid_known_format_and_checksum(self):
        frame = response()
        self.assertEqual(rejection_code(frame), 'postgres/stale-basis')
        for bad in (frame[:-1], b'wrong'+frame[5:], frame[:20]+b'x'+frame[21:]):
            self.assertIsNone(rejection_code(bad))
        self.assertIsNone(rejection_code(response('untrusted\npostgres/stale-basis')))

    def test_cli_relay_preserves_request_and_response(self):
        with tempfile.TemporaryDirectory(prefix='edb-test-') as temporary:
            endpoint = str(Path(temporary)/'writer.sock')
            reply = response()
            observed = []
            with socket.socket(socket.AF_UNIX) as server:
                server.bind(endpoint)
                server.listen(1)
                server.settimeout(5)
                def writer():
                    with server.accept()[0] as stream:
                        header = stream.recv(8)
                        remaining = int.from_bytes(header, 'big')
                        payload = bytearray()
                        while len(payload) < remaining:
                            payload.extend(stream.recv(remaining-len(payload)))
                        observed.append(bytes(payload))
                        stream.sendall(len(reply).to_bytes(8, 'big')+reply)
                thread = threading.Thread(target=writer)
                thread.start()
                client = '''import socket,sys
s=socket.socket(socket.AF_UNIX);s.connect(sys.argv[sys.argv.index('--endpoint')+1])
request=b'original transaction and request key'.ljust(48,b'.')
s.sendall(len(request).to_bytes(8,'big')+request)
size=int.from_bytes(s.recv(8),'big');body=bytearray()
while len(body)<size:body.extend(s.recv(size-len(body)))
assert b'postgres/stale-basis' in body
print('ERROR category=Conflict code=transport/remote-error',file=sys.stderr)
sys.exit(1)
'''
                with self.assertRaises(subprocess.CalledProcessError) as raised:
                    replay([sys.executable, '-c', client, '--endpoint', endpoint], env=os.environ.copy(), timeout=5)
                thread.join(5)
                self.assertIn('remote_code=postgres/stale-basis', raised.exception.stderr)
                self.assertEqual(observed, [b'original transaction and request key'.ljust(48,b'.')])

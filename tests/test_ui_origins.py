"""Request protections for local and Tailscale-proxied UI access."""
from email.message import Message
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from serve_graph_explorer import handler


class RequestOrigins(unittest.TestCase):
    public_host = "eve.example.ts.net:8443"
    public_origin = f"https://{public_host}"

    def request(self, host, origin=None, site="same-origin", configured=True):
        environment = {"LEARNING_REQUEST_DIR": "/tmp/ui-origin-test"}
        if configured:
            environment["COURSE_ACADEMY_PUBLIC_ORIGIN"] = self.public_origin
        with patch("serve_graph_explorer.InventoryJobs"):
            request_class = handler(Path("/unused"), "test", "learner", environment)
        request = request_class.__new__(request_class)
        request.server = SimpleNamespace(server_port=8765)
        request.headers = Message()
        request.headers["Host"] = host
        if origin is not None:
            request.headers["Origin"] = origin
        if site is not None:
            request.headers["Sec-Fetch-Site"] = site
        request.send_bytes = Mock()
        return request

    def test_local_browsing_and_posts_remain_available(self):
        for host in ("localhost:8765", "127.0.0.1:8765"):
            for origin in (None, f"http://{host}"):
                with self.subTest(host=host, origin=origin):
                    self.assertTrue(self.request(host, origin, configured=False).trusted())

    def test_public_browsing_and_same_origin_posts_are_allowed(self):
        for origin in (None, self.public_origin):
            with self.subTest(origin=origin):
                self.assertTrue(self.request(self.public_host, origin).trusted())

    def test_unconfigured_hosts_and_cross_origin_requests_are_forbidden(self):
        cases = [
            self.request(self.public_host, configured=False),
            self.request("other.example.ts.net:8443"),
            self.request("eve.example.ts.net:443"),
            self.request(self.public_host, f"http://{self.public_host}"),
            self.request(self.public_host, "https://attacker.example"),
            self.request("localhost:8765", "https://attacker.example"),
            self.request(self.public_host, self.public_origin, "cross-site"),
            self.request("localhost:8765", "http://localhost:8765", "cross-site"),
            self.request(self.public_host, "null", site=None),
        ]
        for request in cases:
            with self.subTest(headers=str(request.headers)):
                self.assertFalse(request.trusted())
                self.assertEqual(request.send_bytes.call_args.args[0], 403)

    def test_invalid_public_origin_configuration_is_rejected(self):
        for origin in ("http://eve.example.ts.net", "https://eve.example.ts.net/home",
                       "https://user@eve.example.ts.net", "https://eve.example.ts.net?x=1",
                       "https://eve.example.ts.net#fragment", "https://eve.example.ts.net:bad"):
            with self.subTest(origin=origin), self.assertRaises(ValueError):
                handler(Path("/unused"), "test", "learner", {
                    "LEARNING_REQUEST_DIR": "/tmp/ui-origin-test",
                    "COURSE_ACADEMY_PUBLIC_ORIGIN": origin,
                })


if __name__ == "__main__":
    unittest.main()

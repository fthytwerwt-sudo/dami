from __future__ import annotations

import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures"
SITE_ROOT = FIXTURE_ROOT / "synthetic_site"


class SyntheticHandler(SimpleHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)
        if self.path.endswith("/fail"):
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"server error")
            return
        self.send_response(200)
        self.end_headers()
        if self.path.endswith("/unknown"):
            self.wfile.write(b"accepted")
        else:
            self.wfile.write(b"Thank you, message received.")

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def synthetic_server():
    handler = functools.partial(SyntheticHandler, directory=str(SITE_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)

"""测试公共夹具：只启动 localhost 合成网页，不访问外部网络。"""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest


class _QuietHandler(SimpleHTTPRequestHandler):
    """关闭测试 HTTP 服务的控制台访问日志。"""

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


@pytest.fixture()
def synthetic_site_url() -> str:
    """在随机 localhost 端口提供合成企业页，并在测试后关闭。"""

    fixture_dir = Path(__file__).parent / "fixtures"
    handler = partial(_QuietHandler, directory=str(fixture_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/synthetic_company.html"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

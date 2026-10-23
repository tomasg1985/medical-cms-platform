
import logging

from fastapi import Request

from app.main import global_exception_handler


def test_global_exception_handler_returns_generic_500(caplog):
    scope = {
        "type": "http",
        "asgi": {
            "version": "3.0",
            "spec_version": "2.3",
        },
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/test-error",
        "raw_path": b"/test-error",
        "query_string": b"",
        "root_path": "",
        "headers": [],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
        "state": {},
    }

    request = Request(scope)
    exc = RuntimeError("Detalle interno que no debe exponerse")

    with caplog.at_level(logging.ERROR):
        response = await_handler(global_exception_handler(request, exc))

    assert response.status_code == 500
    assert response.body == b'{"detail":"Error interno del servidor"}'
    assert "Detalle interno que no debe exponerse" in caplog.text


def await_handler(coroutine):
    import asyncio

    return asyncio.run(coroutine)

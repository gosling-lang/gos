import threading
import time
from typing import Optional

import portpicker
import starlette.applications
import uvicorn


class BackgroundServer:
    _app: starlette.applications.Starlette
    _port: Optional[int]
    _server_thread: Optional[threading.Thread]
    _server: Optional[uvicorn.Server]

    def __init__(self, app: starlette.applications.Starlette):
        self._app = app
        self._port = None
        self._server_thread = None
        self._server = None

    @property
    def app(self) -> starlette.applications.Starlette:
        return self._app

    @property
    def port(self) -> int:
        if self._server_thread is None or self._port is None:
            raise RuntimeError("Server not running.")
        return self._port

    def stop(self):
        if self._server_thread is None:
            return self
        assert self._server is not None

        try:
            # queue exit event and wait for thread to terminate
            self._server.should_exit = True
            self._server_thread.join()
        finally:
            self._server = None
            self._server_thread = None

        return self

    def start(
        self,
        port: Optional[int] = None,
        timeout: int = 1,
        daemon: bool = True,
        log_level: str = "warning",
    ):

        if self._server_thread is not None:
            return self

        config = uvicorn.Config(
            app=self.app,
            port=port or portpicker.pick_unused_port(),
            timeout_keep_alive=timeout,
            log_level=log_level,
        )

        self._port = config.port
        self._server = uvicorn.Server(config=config)
        self._server_thread = threading.Thread(target=self._server.run, daemon=daemon)
        self._server_thread.start()

        # wait for the server to start
        while not self._server.started:
            time.sleep(1e-3)

        return self

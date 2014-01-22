import uwsgi

from .websockets import UWebSocket, UWSMiddleware, UWSApp


class AsyncWebSocket(UWebSocket):
    def receive(self):
        while True:
            uwsgi.wait_fd_read(self.fd, self.timeout)
            uwsgi.suspend()
            fd = uwsgi.ready_fd()
            if uwsgi.ready_fd() == self.fd:
                return uwsgi.websocket_recv_nb()


class AsyncWSMiddleware(UWSMiddleware):
    client = AsyncWebSocket


class AsyncApp(UWSApp):
    middleware = AsyncWSMiddleware

import uuid
from gevent import sleep, spawn
from gevent.queue import Queue

from .websockets import UWebSocket, UWSMiddleware, UWSApp


class GeventWebSocket(UWebSocket):
    def __init__(self, queue):
        self.id = str(uuid.uuid1())
        self.queue = queue

    def send(self, message):
        self.queue.put(message)

    def receive(self):
        pass


class GeventWSMiddleware(UWSMiddleware):
    client = GeventWebSocket

    def __call__(self, environ, start_response):
        handler = self.websocket.routes.get(environ['PATH_INFO'])

        if not handler:
            return self.wsgi_app(environ, start_response)

        # do handshake
        uwsgi.websocket_handshake(environ['HTTP_SEC_WEBSOCKET_KEY'], environ.get('HTTP_ORIGIN', ''))

        queue = Queue()

        # spawn greenlet for handler
        spawn(handler, self.client(queue))

        # loop waiting for messages to send
        while True:
            message = queue.get()
            if message:
                uwsgi.websocket_send(message)
            sleep(0)

        # loop here and handle send/recieves to client in other greenlet?
        # fd = uwsgi.connection_fd()
        # while True:
        #     ready = gevent.select.select([fd], [], [], self.websocket.timeout)
        #     try:
        #         return uwsgi.websocket_recv_nb()
        #     except IOError:  # client disconnected
        #         pass


class GeventWSApp(UWSApp):
    middleware = GeventWSMiddleware

from gevent import sleep, spawn
from gevent.event import Event
from gevent.queue import Queue
from gevent.select import select
from gevent.monkey import patch_all; patch_all()
import uuid

from . import WebSocket, WebSocketClient, WebSocketMiddleware
from ._uwsgi import uwsgi


class GeventWebSocketClient(object):
    def __init__(self, fd, send_event, send_queue, recv_event, recv_queue, timeout=60):
        self.id = str(uuid.uuid1())
        self.fd = fd
        self.send_event = send_event
        self.send_queue = send_queue
        self.recv_event = recv_event
        self.recv_queue = recv_queue
        self.timeout = timeout

    def send(self, message):
        self.send_queue.put(message)
        self.send_event.set()

    def receive(self):
        self.recv_event.set()
        return self.recv_queue.get()


class GeventWebSocketMiddleware(WebSocketMiddleware):
    client = GeventWebSocketClient

    def __call__(self, environ, start_response):
        handler = self.websocket.routes.get(environ['PATH_INFO'])

        if not handler:
            return self.wsgi_app(environ, start_response)

        # do handshake
        uwsgi.websocket_handshake(environ['HTTP_SEC_WEBSOCKET_KEY'], environ.get('HTTP_ORIGIN', ''))

        # setup events
        send_event = Event()
        send_queue = Queue()

        recv_event = Event()
        recv_queue = Queue()

        client = self.client(uwsgi.connection_fd(), send_event, send_queue, recv_event, recv_queue)

        # spawn handler
        spawn(handler, client)

        # spawn recv listener
        def listener(client):
            ready = select([client.fd], [], [], client.timeout)
            recv_event.set()
        spawn(listener, client)

        while True:
            if send_event.is_set():
                send_event.clear()
                try:
                    uwsgi.websocket_send(send_queue.get())
                except IOError:  # client disconnected
                    pass

            if recv_event.is_set():
                recv_event.clear()
                try:
                    recv_queue.put(uwsgi.websocket_recv_nb())
                    spawn(listener, client)
                except IOError:  # client disconnected
                    pass

            sleep(0.1)

class GeventWebSocket(WebSocket):
    middleware = GeventWebSocketMiddleware
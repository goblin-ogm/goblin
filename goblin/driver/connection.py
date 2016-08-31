# Copyright 2016 ZEROFAIL
#
# This file is part of Goblin.
#
# Goblin is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Goblin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Goblin.  If not, see <http://www.gnu.org/licenses/>.

import abc
import asyncio
import collections
import functools
import json
import logging
import uuid

import aiohttp

from goblin import exception


logger = logging.getLogger(__name__)


Message = collections.namedtuple(
    "Message",
    ["status_code", "data", "message"])


def error_handler(fn):
    @functools.wraps(fn)
    async def wrapper(self):
        msg = await fn(self)
        if msg:
            if msg.status_code not in [200, 206]:
                self.close()
                raise exception.GremlinServerError(
                    "{0}: {1}".format(msg.status_code, msg.message))
            msg = msg.data
        return msg
    return wrapper


class Response:
    """Gremlin Server response implementated as an async iterator."""
    def __init__(self, response_queue, timeout, loop):
        self._response_queue = response_queue
        self._loop = loop
        self._timeout = timeout
        self._done = asyncio.Event(loop=self._loop)

    @property
    def done(self):
        """
        Readonly property.

        :returns: `asyncio.Event` object
        """
        return self._done

    async def __aiter__(self):
        return self

    async def __anext__(self):
        msg = await self.fetch_data()
        if msg:
            return msg
        else:
            raise StopAsyncIteration

    def close(self):
        """Close response stream by setting done flag to true."""
        self.done.set()
        self._loop = None
        self._response_queue = None

    @error_handler
    async def fetch_data(self):
        """Get a single message from the response stream"""
        if self.done.is_set():
            return None
        try:
            msg = await asyncio.wait_for(self._response_queue.get(),
                                         timeout=self._timeout,
                                         loop=self._loop)
        except asyncio.TimeoutError:
            self.close()
            raise exception.ResponseTimeoutError('Response timed out')
        if msg is None:
            self.close()
        return msg


class AbstractConnection(abc.ABC):
    """Defines the interface for a connection object."""
    @abc.abstractmethod
    async def submit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self):
        raise NotImplementedError


class Connection(AbstractConnection):
    """
    Main classd for interacting with the Gremlin Server. Encapsulates a
    websocket connection. Not instantiated directly. Instead use
    :py:meth:`Connection.open<goblin.driver.connection.Connection.open>`.

    :param str url: url for host Gremlin Server
    :param aiohttp.ClientWebSocketResponse ws: open websocket connection
    :param asyncio.BaseEventLoop loop:
    :param aiohttp.ClientSession: Client session used to establish websocket
        connections
    :param float response_timeout: (optional) `None` by default
    :param str lang: Language used to submit scripts (optional)
        `gremlin-groovy` by default
    :param str username: Username for database auth
    :param str password: Password for database auth
    :param int max_inflight: Maximum number of unprocessed requests at any
        one time on the connection
    """
    def __init__(self, url, ws, loop, client_session, *, response_timeout=None,
                 lang='gremlin-groovy', username=None, password=None,
                 max_inflight=64):
        self._url = url
        self._ws = ws
        self._loop = loop
        self._client_session = client_session
        self._response_timeout = response_timeout
        self._lang = lang
        self._username = username
        self._password = password
        self._closed = False
        self._response_queues = {}
        self._receive_task = self._loop.create_task(self._receive())
        self._semaphore = asyncio.Semaphore(value=max_inflight,
                                            loop=self._loop)

    @classmethod
    async def open(cls, url, loop, *, ssl_context=None, username='',
                   password='', lang='gremlin-groovy', max_inflight=64,
                   response_timeout=None):
        """
        **coroutine** Open a connection to the Gremlin Server.

        :param str url: url for host Gremlin Server
        :param asyncio.BaseEventLoop loop:
        :param ssl.SSLContext ssl_context:
        :param str username: Username for database auth
        :param str password: Password for database auth
        :param str lang: Language used to submit scripts (optional)
            `gremlin-groovy` by default

        :param int max_inflight: Maximum number of unprocessed requests at any
            one time on the connection
        :param float response_timeout: (optional) `None` by default

        :returns: :py:class:`Connection<goblin.driver.connection.Connection>`
        """
        connector = aiohttp.TCPConnector(ssl_context=ssl_context, loop=loop)
        client_session = aiohttp.ClientSession(loop=loop, connector=connector)
        ws = await client_session.ws_connect(url)
        return cls(url, ws, loop, client_session, lang=lang,
                   username=username, password=password,
                   response_timeout=response_timeout)

    @property
    def closed(self):
        """
        Check if connection has been closed.

        :returns: `bool`
        """
        return self._closed or self._ws.closed

    @property
    def url(self):
        """
        Readonly property.

        :returns: str The url association with this connection.
        """
        return self._url

    async def submit(self,
                     gremlin,
                     *,
                     bindings=None,
                     lang=None,
                     traversal_source=None,
                     session=None):
        """
        Submit a script and bindings to the Gremlin Server

        :param str gremlin: Gremlin script to submit to server.
        :param dict bindings: A mapping of bindings for Gremlin script.
        :param str lang: Language of scripts submitted to the server.
            "gremlin-groovy" by default
        :param dict traversal_source: ``TraversalSource`` objects to different
            variable names in the current request.
        :param str session: Session id (optional). Typically a uuid

        :returns: :py:class:`Response` object
        """
        await self._semaphore.acquire()
        if traversal_source is None:
            traversal_source = {}
        lang = lang or self._lang
        request_id = str(uuid.uuid4())
        message = self._prepare_message(gremlin,
                                        bindings,
                                        lang,
                                        traversal_source,
                                        session,
                                        request_id)
        response_queue = asyncio.Queue(loop=self._loop)
        self._response_queues[request_id] = response_queue
        if self._ws.closed:
            self._ws = await self.client_session.ws_connect(self.url)
        self._ws.send_bytes(message)
        resp = Response(response_queue, self._response_timeout, self._loop)
        self._loop.create_task(self._terminate_response(resp, request_id))
        return resp

    async def close(self):
        """**coroutine** Close underlying connection and mark as closed."""
        self._receive_task.cancel()
        await self._ws.close()
        self._closed = True
        await self._client_session.close()

    def _prepare_message(self, gremlin, bindings, lang, traversal_source, session,
                         request_id):
        message = {
            'requestId': request_id,
            'op': 'eval',
            'processor': '',
            'args': {
                'gremlin': gremlin,
                'bindings': bindings,
                'language':  lang,
                'aliases': traversal_source
            }
        }
        message = self._finalize_message(message, session)
        return message

    def _authenticate(self, username, password, session):
        auth = b''.join([b'\x00', username.encode('utf-8'),
                         b'\x00', password.encode('utf-8')])
        message = {
            'requestId': str(uuid.uuid4()),
            'op': 'authentication',
            'processor': '',
            'args': {
                'sasl': base64.b64encode(auth).decode()
            }
        }
        message = self._finalize_message(message, session)
        self._ws.submit(message, binary=True)

    def _finalize_message(self, message, session):
        if session:
            message['processor'] = 'session'
            message['args']['session'] = session
        message = json.dumps(message)
        return self._set_message_header(message, 'application/json')

    @staticmethod
    def _set_message_header(message, mime_type):
        if mime_type == 'application/json':
            mime_len = b'\x10'
            mime_type = b'application/json'
        else:
            raise ValueError('Unknown mime type.')
        return b''.join([mime_len, mime_type, message.encode('utf-8')])

    async def _terminate_response(self, resp, request_id):
        await resp.done.wait()
        del self._response_queues[request_id]
        self._semaphore.release()

    async def _receive(self):
        while True:
            data = await self._ws.receive()
            if data.tp == aiohttp.MsgType.close:
                await self._ws.close()
            elif data.tp == aiohttp.MsgType.error:
                raise data.data
            elif data.tp == aiohttp.MsgType.closed:
                pass
            else:
                if data.tp == aiohttp.MsgType.binary:
                    data = data.data.decode()
                elif data.tp == aiohttp.MsgType.text:
                    data = data.strip()
                message = json.loads(data)
                request_id = message['requestId']
                status_code = message['status']['code']
                data = message['result']['data']
                msg = message['status']['message']
                response_queue = self._response_queues[request_id]
                if status_code == 407:
                    await self._authenticate(self._username, self._password,
                                             self._processor)
                elif status_code == 204:
                    response_queue.put_nowait(None)
                else:
                    if data:
                        for result in data:
                            message = Message(status_code, result, msg)
                            response_queue.put_nowait(message)
                    else:
                        message = Message(status_code, data, msg)
                        response_queue.put_nowait(message)
                    if status_code != 206:
                        response_queue.put_nowait(None)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
        self._conn = None

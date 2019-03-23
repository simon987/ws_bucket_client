import hashlib
import hmac
import json
from email.utils import formatdate
from typing import BinaryIO
from urllib.parse import urlparse

import requests
import websocket

MAX_HTTP_RETRIES = 3
API_TIMEOUT = 10


class WsBucketApi:

    def __init__(self, url: str, secret: str, ws_scheme: str = "ws"):
        self._url = urlparse(url)
        self._secret = secret.encode("utf8")
        self._ws_scheme = ws_scheme

    def allocate(self, token: str, max_size: int, file_name: str, upload_hook: str, to_dispose_date: int):
        return self._http_post("/slot", {
            "token": token,
            "max_size": max_size,
            "file_name": file_name,
            "upload_hook": upload_hook,
            "to_dispose_date": to_dispose_date,
        })

    def read(self, token: str):
        return self._http_get("/slot", token)

    def upload(self, token: str, stream: BinaryIO, max_size: int):
        ws = websocket.WebSocket()
        ws.connect(self._ws_scheme + "://" + self._url.netloc + "/upload", header={
            "X-Upload-Token": token,
        })

        ws.send_binary(stream.read()[:max_size])

    def _http_post(self, endpoint, body):

        body = json.dumps(body)

        ts = formatdate(timeval=None, localtime=False, usegmt=True)
        signature = hmac.new(key=self._secret, msg=(body + ts).encode("utf8"),
                             digestmod=hashlib.sha256).hexdigest()
        headers = {
            "Timestamp": ts,
            "X-Signature": signature
        }

        retries = 0
        while retries < MAX_HTTP_RETRIES:
            try:
                response = requests.post(self._url.scheme + "://" + self._url.netloc + endpoint, timeout=API_TIMEOUT,
                                         headers=headers, data=body.encode("utf8"))
                return response
            except Exception as e:
                print(str(type(e)) + str(e))
                retries += 1
                pass
        return None

    def _http_get(self, endpoint, token):
        headers = {
            "X-Upload-Token": token,
        }

        retries = 0
        while retries < MAX_HTTP_RETRIES:
            try:
                response = requests.get(self._url.scheme + "://" + self._url.netloc + endpoint, timeout=API_TIMEOUT,
                                        headers=headers)
                return response
            except Exception as e:
                print(str(type(e)) + str(e))
                retries += 1
                pass
        return None

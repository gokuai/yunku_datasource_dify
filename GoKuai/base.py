import time
import base64
import hmac
import hashlib
import requests


class Base:

    timeout = 300
    connecttimeout = 10
    _user_agent = "yunku-sdk-php/6.0.0"
    _server = "http://yk3-api-ent.gokuai.com"

    def __init__(self, client_id, client_secret, server=None):
        self.client_id = client_id
        self.client_secret = client_secret
        if server:
            if "http" in server:
                self._server = "http://" + str(server)
            self._server = server

    def callApi(self, httpMethod, uri, query, body):

        httpMethod = httpMethod.upper()

        if httpMethod == "GET":
            query = self.setCommonParams(query)
        if httpMethod == "POST":
            body = self.setCommonParams(body)
        self.sendRequest(self._server + uri, httpMethod, query, body)
        return self.isOk()

    def setCommonParams(self, params):
        for k, v in list(params.items()):
            if v is None:
                del params[k]

        params["client_id"] = self.client_id
        params["dateline"] = str(int(time.time()))

        arrToSign = params
        if arrToSign['filehash'] is not None:
            del arrToSign['filehash']
        if arrToSign['filesize'] is not None:
            del arrToSign['filesize']
        params["sign"] = self._getSign(arrToSign)
        return params
    
    def _getSign(self, params):
        if params is None or len(params) == 0:
            return ""
        params = dict(sorted(params.items()))
        data = "\n".join(str(i) for i in params.values())
        signature = base64.b64encode(
            hmac.new(self.client_secret.encode(), data.encode(), hashlib.sha1).digest()
        )
        return signature

    def sendRequest(self, url, httpMethod, data, params):
        headers = {
            "User-Agent": self._user_agent,
        }
        self._response = requests.request(
            httpMethod.upper(),
            url,
            data=data,
            params=params,
            timeout=(self.timeout, self.connecttimeout),
            headers=headers,
        )
        return

    def getHttpResponse(self, return_json=False):
        if return_json:
            return self._response.json()
        else:
            return self._response.text

    def isOk(self):
        return self._response.status_code < 400

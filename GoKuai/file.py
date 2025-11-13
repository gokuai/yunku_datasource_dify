from GoKuai.base import Base
import time

class File(Base):
    # def __init__(self, client_id, client_secret, server=None):
    #     super().__init__(self, client_id, client_secret, server)
    

    def setCommonParams(self, params):
        for k, v in list(params.items()):
            if v is None:
                del params[k]

        params["org_client_id"] = self.client_id
        params["dateline"] = str(int(time.time()))

        arrToSign = params
        if 'filehash' in arrToSign.keys():
            del arrToSign['filehash']
        if 'filesize' in arrToSign.keys():
            del arrToSign['filesize']
        params["sign"] = self._getSign(arrToSign)
        return params
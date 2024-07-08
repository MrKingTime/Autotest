import sys

sys.path.append("d:\\project\\office\\interface-auto")

from tools.request import Request
from api.login import account_login
import settings


token = account_login(username=settings.QIGUAN_USER, password=settings.DEFAULT_PASSWORD)
for i in range(6):
    url = "/woPackage/savePackage"
    body = {
        "subSysId": "3586",
        "woType": "1",
        "periodId": 124,
        "contents": [{"photoRequired": 0, "standard": f"月度维保--{i}", "answerType": "1", "remark": "", "lowValue": "1", "upValue": "444"}],
    }
    res = Request.request(url=url, token=token, method="post", body=body)
    print(f"===========第{i+1}次")
    print(res)

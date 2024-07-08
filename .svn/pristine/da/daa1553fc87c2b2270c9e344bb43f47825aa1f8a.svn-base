import requests
import settings
import json
from tools.logger import get_logger


class Request:
    success_code = [200]
    _logger = get_logger()
    idempotence = None  # 幂等性校验token，但无需存储

    @classmethod
    def request(cls, url, method="GET", token=None, body=None, headers=None, full_data=False, *args, **kwargs):

        if headers is None:
            headers = {
                "X-Token": token,
                "Content-Type": "application/json",
                "project-all": "1",
                "project-id": "",
            }
        if cls.idempotence is None and url not in ["/account/token/getIdempotenceToken", "/account/login"]:
            res = Request.request("/account/token/getIdempotenceToken", method="GET", headers=headers)
            cls._logger.debug(f"idempotence：{res}")
            headers.update({"X-Idempotence": res})

        cls._logger.debug(f"接口请求，url：{url}，method：{method}，headers：{headers}，body：{json.dumps(body)}")

        res = requests.request(method=method, url=settings.BASE_URL + url, headers=headers, json=body, *args, **kwargs)

        if res.status_code != 200:
            cls._logger.error("请求失败，状态码：{}".format(res.status_code))
            cls._logger.error(res.text)
            cls._logger.error(url)
            return False

        try:
            json_data = res.json()
            if json_data is not None and json_data["code"] in cls.success_code:
                cls._logger.debug(f"接口响应，url：{url}，method：{method}，headers：{headers}，body：{json.dumps(json_data)}")
                if full_data:
                    return json_data
                return json_data["data"] if json_data["data"] != None else cls._logger.info(json_data["msg"])

            cls._logger.info(f"接口响应，url：{url}，method：{method}，headers：{headers}，MSG{json_data['msg']}")
        except Exception as e:
            cls._logger.error(url)
            cls._logger.error(e)
            return False

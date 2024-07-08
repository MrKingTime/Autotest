from typing import Union
from tools.request import Request
from tools.logger import get_logger

_logger = get_logger()


def account_login(username: str, password: str) -> Union[False, str]:
    url = "/account/login"
    body = {"username": username, "password": password}
    res = Request.request(method="POST", url=url, body=body)

    if res["token"] is not False:
        _logger.debug(f"登录成功, {username}: {res['token']}")
        return res["token"]
    else:
        _logger.error(f"登录失败, {username}")
        _logger.error(res)
        return None

from tools.request import Request
import os


def upload_file(file_path: str, token: str, *args, **kwargs):
    """创建企业

    :param str name: 企业名称
    """
    url = "/resource/upload/single"
    fileObject = {
        "sketch": (None, "", None),
        "title": (None, file_path, None),
        "file": (file_path, open(os.path.join(os.getcwd(), f"data\\{file_path}"), "rb"), "application/pdf"),
    }
    headers = {
        "X-Token": token,
        "project-all": "1",
        "project-id": "",
    }
    res = Request.request(method="POST", url=url, token=token, files=fileObject, headers=headers, *args, **kwargs)
    return res

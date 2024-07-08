from tools.request import Request
from typing import Union
import random


def create_enterprise(enterprise_name: str, token: str):
    """创建企业

    :param str name: 企业名称
    """
    url = "/company/save"
    body = {
        "name": enterprise_name,
        "adddatas": "广东省广州市黄埔区科学城地铁旁创意大厦B3",
        "contacts": "李想",
        "contactPhone": "15888888888",
        "email": "12306@qq.com",
        "ssc": "",
        "businessLicenseArr": [],
        "businessLicense": "",
        "logoImgArr": [],
        "logoImg": "",
        "sealArr": [],
        "seal": "",
        "childTitle": "",
        "permissions": [
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            20,
            21,
            39,
            244,
            24,
            25,
            38,
            246,
            27,
            28,
            29,
            30,
            242,
            31,
            32,
            35,
        ],
    }
    res = Request.request(method="POST", url=url, body=body, token=token)

    return res.split(".")[0]


def delete_enterprise(enterprise_id: str, token: str):
    """删除企业

    :param str name: 企业名称
    """
    url = f"/company/info?id={enterprise_id}"

    Request.request(method="DELETE", url=url, token=token)

    return True


def search_enterprise(name: Union[str, list], token: str):
    """搜索企业

    :param str name: 企业名称
    """
    url = f"/company/page?current=1&size=20&name={','.join(name)}"

    res = Request.request(method="GET", url=url, token=token)

    if isinstance(name, str):
        return res["records"][0].value
    elif isinstance(name, list):
        return res["records"]
    else:
        return None


def search_project(project_name: Union[str, list], token: str):
    """搜索项目

    :param str name: 项目名称
    """
    url = f"/project/options?province=&city=&region=&name={','.join(project_name) if isinstance(project_name, list) else project_name}"

    res = Request.request(method="GET", url=url, token=token)

    if isinstance(project_name, str):
        return res[0]["value"]
    elif isinstance(project_name, list):
        return res
    else:
        return None


def location_tree(project_id: str, token: str, is_random=True):
    """获取项目的建筑信息

    :param str name: 企业名称
    """
    url = f"/location/locationTree/{project_id}"
    res = Request.request(method="GET", url=url, token=token)
    if is_random:
        t_building = random.choice(res)
        building_id = t_building["id"]
        building_name = t_building["name"]

        t_childLocation = random.choice(t_building["childLocation"])
        building_floor_id = t_childLocation["id"]
        building_floor_name = t_childLocation["name"]
        return building_id, building_name, building_floor_id, building_floor_name

    return res


def get_project_info(project_id: str, token: str):
    """获取项目的详情信息

    :param str name: 企业名称
    """
    url = f"/project/detail?id={project_id}"
    res = Request.request(method="GET", url=url, token=token)

    return res

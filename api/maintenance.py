from tools.request import Request
from typing import Union


def find_sys_tree_by_pid(project_id: str, token: str):
    """获取项目的系统信息

    :param str name: 企业名称
    """
    url = f"/deviceSystem/findSysTreeByPId?projectId={project_id}"
    data = Request.request(method="GET", url=url, token=token)

    return data


def get_dict(project_id: str, type: int, token: str):
    """获取数据字典，1是设备等级，2是设备状态，3是故障等级

    :param str name: 企业名称
    """
    url = f"/dict/list?type={type}&projectId={project_id}"
    res = Request.request(method="GET", url=url, token=token)

    return res


def create_woinfo(
    project_id: str, level: str, depiction: str, location: str, building_id: str, location_id: str, token: str, device_ids=[]
):
    """创建故障维修工单

    :param str name: 企业名称
    """
    url = "/crWoInfo/add"
    body = {
        "projectId": project_id,
        "level": level,
        "depiction": depiction,
        "location": location,
        "buildingId": building_id,
        "locationId": location_id,
        "imgs": "",
        "deviceIds": device_ids,
    }
    Request.request(method="POST", url=url, body=body, token=token)


def get_operator_by_pid(woinfo_id: str, token: str, planType=0):
    """查询派发工单角色

    :param str name: 企业名称
    """
    url = f"/woInfo/findOperatorByPId?planType={planType}&id={woinfo_id}"

    res = Request.request(method="GET", url=url, token=token)

    return res["users"][0]["id"], res["users"][0]["name"]


def distribute_woinfo(woinfo_id: str, userId: str, token: str, planType=0):
    """派发工单

    :param str name: 企业名称
    """
    url = "/crWoInfo/sendTask"
    body = {"planType": planType, "id": woinfo_id, "userId": userId}

    Request.request(method="POST", url=url, body=body, token=token)


def repair_woinfo(id: str, building_id: str, location_id: str, cm_info: str, cm_desc: str, token: str, cm_imgs=""):
    """维修工单

    :param str name: 企业名称
    """
    url = "/crWoInfo/submitAudit"
    body = {
        "id": id,
        "buildingId": building_id,
        "locationId": location_id,
        "cmInfo": cm_info,
        "cmDesc": cm_desc,
        "cmImgs": cm_imgs,
    }

    Request.request(method="POST", url=url, body=body, token=token)


def check_order(id: str, plan_type: int, check_status: str, check_desc: str, token: str):
    """验收工单

    :param int plan_type: 工单类型，0 维修工单
    :param int check_status: 验收类型，1 验收通过 2 验收不通过
    """
    url = "/crWoInfo/checkOrder"
    body = {
        "planType": plan_type,
        "id": id,
        "checkStatus": check_status,
        "checkDesc": check_desc,
    }

    Request.request(method="POST", url=url, body=body, token=token)


def woinfo_list(token: str, current=1, size=10, projectIds=[], sort=None, key=""):
    """搜索工单

    :param str token: _description_
    :param int current: _description_, defaults to 1
    :param int size: _description_, defaults to 20
    :param list projectIds: _description_, defaults to []
    :param _type_ sort: _description_, defaults to None
    :param str key: 故障描述/维修编号, defaults to ""
    :return _type_: status: 0 待派发 1 待维修 2 待验收 3 已完成
    """
    url = "/crWoInfo/pageList"
    body = {
        "current": current,
        "size": size,
        "projectIds": projectIds,
        "key": key,
        "sort": sort,
    }
    res = Request.request(method="POST", url=url, body=body, token=token)

    return res["records"]


def device_list(token: str, current=1, size=10, project_ids=[], sys_id=None, sub_sys_id=None, building_id=None, location_id=None):
    """设备列表

    :param str token: _description_
    :param int current: _description_, defaults to 1
    :param int size: _description_, defaults to 20
    :param list projectIds: _description_, defaults to []
    :param _type_ sort: _description_, defaults to None
    :param str key: 故障描述/维修编号, defaults to ""
    :return _type_: status:
    """
    url = "/device/list"
    body = {
        "current": current,
        "size": size,
        "sysId": sys_id,
        "subSysId": sub_sys_id,
        "buildingId": building_id,
        "locationId": location_id,
        "projectIds": project_ids,
    }
    res = Request.request(method="POST", url=url, body=body, token=token)

    return res["records"]


def plan_list(token: str, status="", current=1, size=10, project_ids=[], sort=None, key="", plan_type=1):
    """计划列表

    :param str token: _description_
    :param int current: _description_, defaults to 1
    :param int size: _description_, defaults to 20
    :param list projectIds: _description_, defaults to []
    :param _type_ sort: _description_, defaults to None
    :param str key: 故障描述/维修编号, defaults to ""
    :return _type_: status:
    """
    url = "/woInfo/listPlanPage"
    body = {
        "current": current,
        "size": size,
        "projectIds": project_ids,
        "planType": plan_type,
        "key": key,
        "status": "",
        "sort": None,
    }
    res = Request.request(method="POST", url=url, body=body, token=token)

    return res["records"]


def increase_device(token: str, project_id, sys_id, sub_sys_id, building_id, location_id, level, state, signature_code="") -> int:
    """添加设备

    :param str name: 项目名称
    """
    url = "/device/add"
    body = {
        "projectId": project_id,
        "parentDevice": {
            "projectId": [project_id],
            "deviceCode": "",
            "sysId": sys_id,
            "subSysId": sub_sys_id,
            "buildingId": building_id,
            "locationId": location_id,
            "address": "",
            "signatureCode": signature_code,
            "brand": "",
            "serialNo": "",
            "specs": "",
            "manufacturer": "",
            "usageStatus": state,
            "priority": level,
            "acquiredDate": "",
            "introductionDate": "",
            "warrantyPeriod": "",
            "scrapDate": "",
            "director": "",
            "organization": "",
            "remark1": "",
            "img": "",
        },
        "files": [],
    }
    res = Request.request(method="POST", url=url, body=body, token=token)

    return res


def woinfo_wait_order(token: str, project_ids=[], current=1, size=10):
    """获取计划类型

    :param str token: _description_
    :param int project_id: _description_
    :param int plan_type: 类型，1为计划类型
    """
    url = "/woInfo/app/waitOrder"
    body = {"projectIds": project_ids, "current": current, "size": size}
    res = Request.request(method="POST", url=url, token=token, body=body)

    return res["records"]


def sign(token: str, build_img: str, face_img: str, order_id: list[str], gpsx: str, gpsy: str, project_id: str, project_type=1, type=1):
    """签到

    :param str token: _description_
    :param str build_img: _description_
    :param str face_img: _description_
    :param list[str] order_id: _description_
    :param str gpsx: _description_
    :param str gpsy: _description_
    :param str project_id: _description_
    :param int project_type: 1为维护保养, defaults to 1
    :param int type: 1为维护保养, defaults to 1
    :return _type_: _description_
    """
    url = "/sign/add"
    body = {
        "projectId": project_id,
        "type": type,
        "projectType": project_type,
        "gpsx": gpsx,
        "gpsy": gpsy,
        "buildImg": build_img,
        "faceImg": face_img,
        "orderId": order_id,
    }
    res = Request.request(method="POST", url=url, token=token, body=body)

    return res


def woinfo_woids_detail(token: str, plan_id: str, woIds: list[str]):
    """获取维保工单详情

    :param str token: _description_
    :param str plan_id: _description_
    :param list[str] woIds: _description_
    :return _type_: _description_
    """
    url = f"/woInfo/app/findOrderDeviceByWoIds?planId={plan_id}&woIds={woIds}"

    res = Request.request(method="GET", url=url, token=token)
    return res


def get_plan_type(token: str, project_id: int, plan_type: int):
    """获取计划类型

    :param str token: _description_
    :param int project_id: _description_
    :param int plan_type: 类型，1为计划类型
    """
    url = f"/period/listByProject?projectId={project_id}&planType={plan_type}"
    res = Request.request(method="GET", url=url, token=token)

    return res


def create_maintenance_plan(
    token: str, start_time: str, end_time: str, project_id: int, period_type_ids: list[int], business_ids: list[int]
):
    """获取计划类型

    :param str token: _description_
    :param int project_id: _description_
    :param int plan_type: 类型，1为计划类型
    """
    url = "/woInfo/add"
    body = {
        "planType": 1,
        "startTime": start_time,
        "endTime": end_time,
        "projectId": project_id,
        "periodTypeId": period_type_ids,
        "execType": 1,
        "businessIds": business_ids,
    }
    res = Request.request(method="POST", url=url, body=body, token=token)

    return res


def find_wo_device_conf(token: str, woIds: list[str], sub_sys_id: int):
    """获取设备维保任务详情

    :param str token: _description_
    :param list[str] woIds: _description_
    :param int sub_sys_id: _description_
    :return _type_: _description_
    """

    url = f"/woInfo/app/findWoDeviceConfBySubSysId?woIds={woIds}&subSysId={sub_sys_id}"

    res = Request.request(method="GET", url=url, token=token)

    return res


def add_wo_device(
    token: str,
    building_floor_id: int,
    building_floor_name: str,
    address: str,
    building_id: int,
    building_name: str,
    confVO: dict,
    device_num: int,
    sub_sys_id: int,
    woIds: list[int],
):
    """完成设备维保任务

    :param str token: _description_
    :param list[str] woIds: _description_
    :param int sub_sys_id: _description_
    :return _type_: _description_
    """

    url = "/woInfo/app/addWoDevice"
    body = {
        "address": address,
        "buildingFloorId": building_floor_id,
        "buildingFloorName": building_floor_name,
        "buildingId": building_id,
        "buildingName": building_name,
        "confVO": confVO,
        "deviceNum": device_num,
        "subSysId": sub_sys_id,
        "woIds": woIds,
    }

    res = Request.request(method="POST", url=url, token=token, body=body)

    return res


def find_order_device_by_sub_sys(token: str, woIds: str, sub_sys_id: int):
    """获取设备完成的维保任务列表

    :param str token: _description_
    :param list[str] woIds: _description_
    :param int sub_sys_id: _description_
    :return _type_: _description_
    """

    url = f"/woInfo/app/findOrderDeviceBySubSys?woIds={woIds}&subSysId={sub_sys_id}"
    res = Request.request(method="GET", url=url, token=token)

    return res

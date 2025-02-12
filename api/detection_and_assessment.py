from tools.request import Request
import uuid

from tools.yaml_util import YamlUtil


def create_detection(
        name: str, contract_file_path: str, contract_file_name: str, test_plan_file_path: str, test_plan_file_name: str,
        token: str
):
    """创建检测任务

    :param str name: 企业名称
    """
    url = "/rp/save"
    body = {
        "buildingType": 1,
        "buildingFinishDrawingExist": 1,
        "testType": 0,
        "testScope": 0,
        "itemGps": "",
        "belongArea": "44 4401 440112",
        "province": "广东省",
        "city": "广州市",
        "region": "黄埔区",
        "itemAddress": "广东省广州市黄埔区科学城地铁旁创意大厦B3",
        "entrustingParty": "李想",
        "entrustingPartyScc": "",
        "designCompany": "万达设计单位",
        "maintainCompany": "万达施工单位",
        "testCompanyId": None,
        "testArea": "23",
        "buildingFinishDate": "2024-05-16",
        "buildingTotalArea": "2312",
        "buildingFloor": 35,
        "buildingHeight": "123",
        "floorUpStorey": 32,
        "floorBelowStorey": 3,
        "testDate": "2024-05-16",
        "testFinishDate": "2024-05-16",
        "contactName": "李不想",
        "contactTel": "15888888888",
        "testPart": "检测部位(500字以内)",
        "fireProtectionApproval": "消防批文",
        "testUseFunction": "使用情况(500字以内)",
        "testBasis": "DBJT 15-110-2015广东省建筑防火及消防设施检测技术规程,",
        "testBasis1": "DBJT 15-110-2015广东省建筑防火及消防设施检测技术规程",
        "testBasis2": "",
        "testBasis1Disabled": True,
        "testContent": "14,20,22,19,21,18",
        "fieldStaff": [347],
        "projectTestUserId": None,
        "projectAuditUserId": 347,
        "projectApprovalUserId": 300,
        "contractName": "创意大厦合同",
        "contractFilePath": contract_file_path,
        "contractFileName": contract_file_name,
        "contractAmount": "8587",
        "testCompanyName": "",
        "testPlanFilePath": test_plan_file_path,
        "testPlanFileName": test_plan_file_name,
        "testIsKeyCompany": 0,
        "id": None,
        "geoScope": 300,
        "isLinkProvinceNet": 0,
        "name": name,
        "geoAddress": "23.164278 113.451206",
        "projectLeaderId": 347,
        "itemDeviceDTOS": [],
        "buildingInfoList": [],
        "editIndex": "4",
    }
    res = Request.request(method="POST", url=url, token=token, body=body)
    return res


def create_assessment(name: str, file_full_res: dict, contract_path: str, contract_name: str, token: str):
    """创建评估任务

    :param str name: 企业名称
    """
    uid = str(uuid.uuid4().int)[:13]
    url = "/sa/save"

    body = {
        "name": name,
        "isLinkProvinceNet": 0,
        "belongRegion": "44 4401 440112",
        "province": "广东省",
        "city": "广州市",
        "region": "黄埔区",
        "projectAddress": "广东省广州市黄埔区科学城地铁旁创意大厦B3",
        "geoAddress": "23.164278 113.451206",
        "geoScope": 500,
        "manageCompany": "万达管理单位",
        "maintainCompany": "万达维保单位",
        "entrustCompany": "李想",
        "buildingCompanySsc": "",
        "contactName": "李不想",
        "contactTel": "15888888888",
        "entrustCompanyAddress": "广东省广州市黄埔区科学城地铁旁创意大厦B3",
        "contractName": "合同A",
        "contractMoney": 12331,
        "contractPath": contract_path,
        "contractPathList": [
            {
                "name": contract_name,
                "percentage": 0,
                "status": "success",
                "size": 1415075,
                "raw": {"uid": uid},
                "uid": uid,
                "response": file_full_res,
            }
        ],
        "buildingCategory": 1,
        "buildingBasicInfo": "建筑基本信息",
        "buildingInfos": [],
        "projectInstruments": [],
        "existStandardIds": "121,114,117,2,7,16,59,69,81",
        "writerUserId": 347,
        "projectLeaderId": 347,
        "auditUserId": 347,
        "approvalId": 300,
        "fieldStaff": [347],
        "assessDate": "2024-05-16",
        "assessScope": "请输入请输入评估范围",
        "assessBasis": "DBJT 15-110-2015 广东省建筑防火及消防设施检测技术规程 ",
        "unitBasicInfo": "请输入请输入单位基本情况",
        "assessExplain": "",
        "highRiskProblem": "",
        "projectLogs": [],
    }
    res = Request.request(method="POST", url=url, token=token, body=body)
    return res


def search_assessment(token: str, name="", project_state="", status="", current=1, size=20, sort=None):
    """创建企业

    :param str name: 企业名称
    """
    url = "/sa/page"

    body = {
        "name": name,
        "projectState": project_state,
        "status": status,
        "current": current,
        "size": size,
        "sort": sort,
    }
    res = Request.request(method="POST", url=url, token=token, body=body)
    return res["records"]


def search_detection(token: str, name="", current=1, size=20, sort=None):
    """搜索检测任务

    :param str token: _description_
    :param str name: name和itemName好像重复了, defaults to ""
    :param int current: _description_, defaults to 1
    :param int size: total字段多余，使用size代替, defaults to 20
    :param _type_ sort: _description_, defaults to None
    :return _type_: _description_
    """
    url = "/rp/page"

    body = {
        "current": current,
        "size": size,
        "total": size,
        "itemName": name,
        "name": name,
        "sort": sort,
    }

    res = Request.request(method="POST", url=url, token=token, body=body)
    return res["records"]


def sign_detection(token: str, build_img: str, face_img: str, project_type=2, type=1):
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
        "projectId": YamlUtil().read_extract_yaml('projectId'),
        "type": type,
        "projectType": project_type,
        "gpsx": YamlUtil().read_extract_yaml('gpsx'),
        "gpsy": YamlUtil().read_extract_yaml('gpsy'),
        "buildImg": build_img,
        "faceImg": face_img,
    }
    res = Request.request(method="POST", url=url, token=token, body=body)
    return res


def search_items(IdempotenceToken: str):
    url = "/testingStandard/item/options"
    headers = {
        "X-Token": YamlUtil().read_extract_yaml('caozuoyuan_token'),
        "project-all": "1",
        "project-id": "",
        "IdempotenceToken": IdempotenceToken,
    }
    data = {'itemId': YamlUtil().read_extract_yaml('projectId')}
    res = Request.request(method="get", headers=headers, url=url, params=data)
    YamlUtil().write_extract_yaml({'parentCode': res[1]['code']})
    YamlUtil().write_extract_yaml({'individualCode': res[0]['code']})
    return res


def search_faces():
    url = "/testingStandard/level/options"
    headers = {
        "X-Token": YamlUtil().read_extract_yaml('caozuoyuan_token'),
        "project-All": "1",
        "project-id": "",
    }
    params = {
        "level": 3,
        "itemId": YamlUtil().read_extract_yaml('projectId'),
        "needCount": True,
        "parentCode": YamlUtil().read_extract_yaml('parentCode')
    }
    res = Request.request(method="get", headers=headers, url=url, params=params)
    return res


def getIdempotenceToken():
    url = "/account/token/getIdempotenceToken"
    headers = {
        "X-Token": YamlUtil().read_extract_yaml('caozuoyuan_token'),
        "project-all": "1",
        "project-id": "",
    }
    res = Request.request(method="get", headers=headers, url=url)
    return res


def point_save(testingResult: str):
    url = "/rp/point/save"
    headers = {
        "X-Token": YamlUtil().read_extract_yaml('caozuoyuan_token'),
        "project-all": "1",
        "project-id": ""
    }
    body = {
        "itemId": YamlUtil().read_extract_yaml('projectId'),
        "testingResult": testingResult,
        "individualCode": YamlUtil().read_extract_yaml('individualCode'),
        "subIndividualCode": YamlUtil().read_extract_yaml('parentCode'),
        "pointLocation": "具体位置",
        "pointFloor": "楼层",
        "remarks": "备注",
        "testingSum": 1,
        "testingPicture": ""
    }
    res = Request.request(method="POST", url=url, body=body, headers=headers)
    return res


def completeTest():
    url = "/rp/completeTest"
    headers = {
        "X-Token": YamlUtil().read_extract_yaml('caozuoyuan_token'),
        "project-all": "1",
        "project-id": "",
    }
    data = {
        'id': YamlUtil().read_extract_yaml('projectId')
    }
    res = Request.request(method="PUT", url=url, headers=headers, data=data,
                          token=YamlUtil().read_extract_yaml('caozuoyuan_token'))
    return res


def result_ser():
    url = "/rp/result/finally"
    headers = {
        "X-Token": YamlUtil().read_extract_yaml('caozuoyuan_token'),
        "project-all": "1",
        "project-id": "",
    }
    params = {'itemId': YamlUtil().read_extract_yaml('projectId')}
    res = Request.request(method="GET", url=url, headers=headers, params=params)
    print(res)
    return res


def result(testingResult: str):
    url = "/rp/result"
    headers = {
        "X-Token": YamlUtil().read_extract_yaml('caozuoyuan_token'),
        "project-all": "1",
        "project-id": "",
    }
    body = {
        "id": YamlUtil().read_extract_yaml('projectId'),
        "result": 1,
        "conclusion": "合格！！！",
        "testContentResult": testingResult
    }
    res = Request.request(method="POST", url=url, headers=headers, body=body)


def auditProject(token: str):
    url = "/rp/auditProject"
    headers = {
        "X-Token": token,
        "project-all": "1",
        "project-id": "",
    }
    params = {'id': YamlUtil().read_extract_yaml('projectId')}
    res = Request.request(method="POST", url=url, headers=headers, params=params)

from api.login import account_login
from api.systemSetting import search_project, get_project_info
from api.maintenance import (
    get_plan_type,
    create_maintenance_plan,
    plan_list,
    find_sys_tree_by_pid,
    woinfo_wait_order,
    sign,
    woinfo_woids_detail,
    find_wo_device_conf,
    add_wo_device,
    find_order_device_by_sub_sys,
)
from api.public import upload_file
from tools.logger import get_logger
from time import sleep
import settings
import pytest
import datetime
import allure
import random


@allure.epic("维护保养")
@pytest.mark.maintenance
class TestMaintenance:
    """维护保养"""

    def setup_class(self):
        self.__logger = get_logger()

        self.caozuoyuan_token = account_login(username=settings.CAOZUOYUAN_USER, password=settings.DEFAULT_PASSWORD)
        self.zhuguan_token = account_login(username=settings.ZHUGUAN_USER, password=settings.DEFAULT_PASSWORD)
        self.qiguan_token = account_login(username=settings.QIGUAN_USER, password=settings.DEFAULT_PASSWORD)
        self.gaojikehu_token = account_login(username=settings.GAOJIKEHU_USER, password=settings.DEFAULT_PASSWORD)

        self.__logger.info("故障维修用例集初始化")
        self.__logger.info(
            f"caozuoyuan_token: {self.caozuoyuan_token}，zhuguan_token: {self.zhuguan_token}，qiguan_token: {self.qiguan_token}，gaojikehu_token: {self.gaojikehu_token}"
        )
        self.date_msg = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")

        self.system_project_id = search_project(settings.PROJECT_SYSTEM_NAME, self.qiguan_token)
        self.__logger.info(f"按系统-项目名称：{settings.PROJECT_SYSTEM_NAME}，项目id：{self.system_project_id}")

        self.device_project_id = search_project(settings.PROJECT_DEVICE_NAME, self.qiguan_token)
        self.__logger.info(f"按系统-项目名称：{settings.PROJECT_DEVICE_NAME}，项目id：{self.device_project_id}")

        assert self.caozuoyuan_token and self.zhuguan_token and self.qiguan_token and self.gaojikehu_token and self.system_project_id and self.device_project_id

    def complete_task(self, task, task_key):
        task["desc"] = f"{settings.TASK_NAME_ENUM[task_key]['value']}情况OK！"  # 该字段后续会剔除
        task["result"] = random.choice([1, 2])  # 1：正常，2：异常
        task["img"] = ""
        t_contents = []
        # 遍历执行计划类型
        for i in task["contents"]:
            self.__logger.info(f"计划类型：{i['periodName']}")
            task["finishPeriods"].append(i["periodName"])

            t_deviceConfList = []
            # 遍历执行当前计划类型的所有任务
            # 修改填写deviceConfList，另一个deviceResult没啥用，不用管
            for device_conf in i["deviceConfList"]:
                self.__logger.info(f"维保任务名称：{device_conf['standard']}")

                # 数值
                if device_conf["answerType"] == 1:
                    device_conf["numValue"] = random.randint(device_conf["lowValue"], device_conf["upValue"])
                    self.__logger.info(f"数值类型：{options}，已填：{device_conf['numValue']}")

                # 单选
                elif device_conf["answerType"] == 2:
                    options = device_conf["options"].split("/")
                    device_conf["selectValue"] = random.choice(options)
                    self.__logger.info(f"单选选项类型：{options}，已选：{device_conf['selectValue']}")

                    # 异常选项需要填写原因
                    if device_conf["selectValue"] in device_conf["abnormalOption"]:
                        device_conf["desc"] = "这是异常原因！！"
                        self.__logger.info(f"异常选项填写原因：{device_conf['desc']}")

                # # 多选
                # elif device_conf["answerType"] == 3:
                #     pass

                # 文本
                elif device_conf["answerType"] == 4:
                    device_conf["strValue"] = "文本内容，文本内容"
                    self.__logger.info(f"文本类型：{device_conf['strValue']}")

                t_deviceConfList.append(device_conf)
            i["deviceConfList"] = t_deviceConfList
            t_contents.append(i)
        task["contents"] = t_contents
        return task

    @pytest.mark.run(order=1)
    @allure.title("按系统-创建下单的维保计划")
    def test_system_create_maintenance_plan(self, global_data) -> None:
        self.__logger.info(f"项目名称：{settings.PROJECT_SYSTEM_NAME}")

        with allure.step("获取计划类型"):
            plan_type_res = get_plan_type(project_id=self.system_project_id, plan_type=1, token=self.qiguan_token)
            plan_type_ids = [i["id"] for i in plan_type_res]
            self.__logger.info(f"计划类型：{plan_type_res}，计划类型id：{plan_type_ids}")

        with allure.step("获取项目的维保标准系统"):
            sys_pids = find_sys_tree_by_pid(self.system_project_id, self.qiguan_token)
            sys_ids = [i["id"] for i in sys_pids]

            self.__logger.info(f"维保标准系统列表：{sys_pids}")
            self.__logger.info(f"系统名称：{[i['name'] for i in sys_pids]}，系统id：{sys_ids}")

        with allure.step("创建维保计划"):
            now = datetime.datetime.now()
            start_time = now.strftime(r"%Y-%m-%d %H:%M:%S")
            end_time = (now + datetime.timedelta(days=60)).strftime(r"%Y-%m-%d %H:%M:%S")
            create_time = now.strftime(r"%Y-%m-%d %H:%M")

            self.__logger.info(f"计划开始时间：{start_time}，计划结束时间：{end_time}")
            self.__logger.info(f"计划类型：{plan_type_ids}")
            create_maintenance_plan(
                period_type_ids=plan_type_ids,
                project_id=self.system_project_id,
                token=self.qiguan_token,
                start_time=start_time,
                end_time=end_time,
                business_ids=sys_ids,
            )

        with allure.step("搜索断言"):
            plan_ls = plan_list(token=self.qiguan_token, project_ids=[self.system_project_id])
            pcode = plan_ls[0]["pcode"]
            plan_id = plan_ls[0]["planId"]
            global_data.set("pcode", pcode)
            global_data.set("plan_id", plan_id)

            assert create_time in plan_ls[0]["createTime"] and not self.__logger.info(f"搜索断言成功，计划编号：{pcode}")

    @pytest.mark.run(order=2)
    @allure.title("按系统-小程序签到维保任务")
    def test_system_sign_maintenance_woinfo(self, global_data) -> None:
        plan_id = global_data.get("plan_id")
        pcode = global_data.get("pcode")
        self.__logger.info(f"计划编号：{pcode}，计划id：{plan_id}")

        with allure.step("获取维保任务的工单"):
            sleep(3)  # 创建维保计划后，需要等待一段时间，否则获取不到工单
            woinfo_wait_order_res = woinfo_wait_order(project_ids=[self.system_project_id], token=self.caozuoyuan_token)
            woinfo_wait_order_info = woinfo_wait_order_res[0]

            if woinfo_wait_order_info["code"] != pcode:
                raise RuntimeError(f"维保任务工单列表：{woinfo_wait_order_res}，新创建的维保任务计划编号：{pcode}")

            woIds = woinfo_wait_order_info["woIds"].split(",")
            self.__logger.info(f"计划类型：{woinfo_wait_order_info['execContent']}，工单id：{woIds}")

        with allure.step("签到维保任务"):
            build_img_name = "测试图片A.png"
            face_img_name = "测试图片B.png"
            build_img_res = upload_file(build_img_name, token=self.caozuoyuan_token)
            face_img_res = upload_file(face_img_name, token=self.caozuoyuan_token)

            sign(
                token=self.caozuoyuan_token,
                order_id=woIds,
                build_img=build_img_res["localSavePath"],
                face_img=face_img_res["localSavePath"],
                project_type=1,
                type=1,
                gpsx=settings.GPS_X,
                gpsy=settings.GPS_Y,
                project_id=self.system_project_id,
            )
            self.__logger.info(f"build_img_name：{build_img_name}，face_img_name：{face_img_name}，gpsx：{settings.GPS_X}，gpsy：{settings.GPS_Y}")

        with allure.step("详情断言"):
            detail_res = woinfo_woids_detail(token=self.caozuoyuan_token, woIds=woinfo_wait_order_info["woIds"], plan_id=plan_id)

            assert not detail_res["isSignIn"] and not self.__logger.info(f"详情断言成功，计划编号：{pcode}")

    @pytest.mark.run(order=3)
    @allure.title("按系统-小程序执行维保任务")
    def test_system_implementation_maintenance_woinfo(self, global_data) -> None:
        plan_id = global_data.get("plan_id")
        pcode = global_data.get("pcode")

        with allure.step("获取维保任务的工单"):
            woinfo_wait_order_res = woinfo_wait_order(project_ids=[self.system_project_id], token=self.caozuoyuan_token)
            woinfo_wait_order_info = woinfo_wait_order_res[0]

            if woinfo_wait_order_info["code"] != pcode:
                raise RuntimeError(f"维保任务工单列表：{woinfo_wait_order_res}，新创建的维保任务计划编号：{pcode}")

            woIds = woinfo_wait_order_info["woIds"].split(",")
            self.__logger.info(f"计划类型：{woinfo_wait_order_info['execContent']}，工单id：{woIds}")

        with allure.step("获取项目建筑、楼层信息"):
            project_info = get_project_info(project_id=self.system_project_id, token=self.caozuoyuan_token)
            building = random.choice(project_info["buildings"])
            building_floor = random.choice(building["buildingFloors"])

            self.__logger.info(f"建筑名称：{building['name']}，建筑id：{building['id']}，楼层名称：{building_floor['name']}，楼层id：{building_floor['id']}")

        with allure.step("获取系统、子系统信息"):
            detail_res = woinfo_woids_detail(token=self.caozuoyuan_token, woIds=woinfo_wait_order_info["woIds"], plan_id=plan_id)
            sys = random.choice(detail_res["execSystems"])
            sub_sys = random.choice(sys["subSysList"])

            self.__logger.info(f"系统名称：{sys['name']}，系统id：{sys['id']}，子系统名称：{sub_sys['name']}，子系统id：{sub_sys['id']}")

        with allure.step("执行维保任务"):
            wo_device_conf_res = find_wo_device_conf(token=self.caozuoyuan_token, woIds=woinfo_wait_order_info["woIds"], sub_sys_id=sub_sys["id"])

            # 遍历执行维保任务
            for task_key, task_value in wo_device_conf_res.items():
                if task_value is None:
                    continue
                self.__logger.info(f"维保任务类型：{settings.TASK_NAME_ENUM[task_key]['description']}")
                wo_device_conf_res[task_key] = self.complete_task(task_value, task_key)

            device_num = random.randint(1, 10000)
            address = "测试地址"
            self.__logger.info(f"设备数量：{device_num}，地址：{address}")
            add_wo_device(
                token=self.caozuoyuan_token,
                address=address,
                building_floor_id=building_floor["id"],
                building_floor_name=building_floor["name"],
                building_id=building["id"],
                building_name=building["name"],
                confVO=wo_device_conf_res,
                device_num=device_num,
                sub_sys_id=sub_sys["id"],
                woIds=woIds,
            )

        with allure.step("列表断言"):
            res = find_order_device_by_sub_sys(token=self.caozuoyuan_token, woIds=woinfo_wait_order_info["woIds"], sub_sys_id=sub_sys["id"])[0]

            assert (
                res["count"] == device_num
                and res["buildingName"] == building["name"]
                and res["buildingFloor"] == building_floor["name"]
                and res["sysCode"] == sys["sysCode"]
                # and res["periodStatsList"]["finishPeriods"] == patrols["finishPeriods"]
                and not self.__logger.info(
                    f"列表断言成功，系统名称：{sys['name']}，设备名称：{sub_sys['name']}，设备数量：{res['count']}，维保任务类型：{[i['name'] for i in res['periodStatsList']]}"
                )
            )

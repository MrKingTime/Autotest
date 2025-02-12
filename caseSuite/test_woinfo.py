from api.login import account_login
from api.systemSetting import location_tree, search_project
from api.maintenance import (
    get_dict,
    create_woinfo,
    get_operator_by_pid,
    woinfo_list,
    distribute_woinfo,
    repair_woinfo,
    check_order,
    device_list,
)
from tools.logger import get_logger
from datetime import datetime
import settings
import pytest
import random
import allure


@allure.epic("故障维修")
@pytest.mark.woinfo
class TestWoinfo:
    """故障维修"""

    caozuoyuan_token = None
    zhuguan_token = None
    qiguan_token = None
    gaojikehu_token = None

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

        date_msg = datetime.now().strftime(r"%Y-%m-%d %H:%M")
        self.woinfo_depiction = f"{date_msg}-接口-故障描述"
        self.woinfo_location = f"{date_msg}-接口-故障位置"

        self.project_id = search_project(settings.PROJECT_DEVICE_NAME, self.qiguan_token)
        self.__logger.info(f"项目名称：{settings.PROJECT_DEVICE_NAME}，项目id：{self.project_id}")

        assert self.caozuoyuan_token and self.zhuguan_token and self.qiguan_token and self.gaojikehu_token

    @pytest.mark.run(order=1)
    @allure.title("创建故障维修工单")
    def test_create_woinfo(self, global_data):
        self.__logger.info(f"项目名称：{settings.PROJECT_DEVICE_NAME}")

        with allure.step("获取项目下建筑id、楼层id"):
            building_id, building_name, building_floor_id, building_floor_name = location_tree(self.project_id, self.qiguan_token)
            self.__logger.info(f"建筑名称：{building_name}，建筑id：{building_id}，楼层名称：{building_floor_name}，楼层id：{building_floor_id}")

        with allure.step("获取故障等级"):
            dicts = get_dict(self.project_id, 3, self.qiguan_token)
            level = random.choice(dicts)
            self.__logger.info(f"故障等级：{level}")

        with allure.step("获取设备列表"):
            device_ls = device_list(token=self.qiguan_token, project_ids=[self.project_id])
            device_ids = [i["id"] for i in device_ls]
            self.__logger.info(f"设备列表：{device_ls}，设备id：{device_ids}")

        with allure.step("创建故障维修工单"):
            create_woinfo(
                project_id=self.project_id,
                level=level["id"],
                depiction=self.woinfo_depiction,
                location=self.woinfo_location,
                building_id=building_id,
                location_id=building_floor_id,
                token=self.caozuoyuan_token,
                device_ids=device_ids,
            )

        with allure.step("搜索断言"):
            res = woinfo_list(key=self.woinfo_depiction, size=1, token=self.qiguan_token)

            assert (
                res[0]["name"] == self.woinfo_depiction
                and res[0]["status"] == 0
                and global_data.set("woinfo_name", res[0]["name"])
                and global_data.set("woinfo_id", res[0]["id"])
                and not self.__logger.info(f"搜索断言成功，故障描述：{self.woinfo_depiction}")
            )

    @pytest.mark.run(order=2)
    @allure.title("派发故障维修工单")
    def test_distribute_woinfo(self, global_data):
        woinfo_id = global_data.get("woinfo_id")
        woinfo_name = global_data.get("woinfo_name")
        self.__logger.info(f"派发工单名称：{woinfo_name}，工单id：{woinfo_id}")

        with allure.step("获取派发角色id"):
            user_id, user_name = get_operator_by_pid(woinfo_id, self.zhuguan_token)
            self.__logger.info(f"派发角色名称：{user_name}，派发角色id：{user_id}")

        with allure.step("派发工单"):
            distribute_woinfo(woinfo_id, user_id, self.zhuguan_token)

        with allure.step("搜索断言"):
            res = woinfo_list(key=self.woinfo_depiction, size=1, token=self.qiguan_token)

            assert (
                res[0]["name"] == self.woinfo_depiction and res[0]["status"] == 1 and not self.__logger.info(f"搜索断言成功，故障描述：{self.woinfo_depiction}")
            )

    @pytest.mark.run(order=3)
    @allure.title("维修故障维修工单")
    def test_repair_woinfo(self, global_data):
        woinfo_id = global_data.get("woinfo_id")
        woinfo_name = global_data.get("woinfo_name")
        self.__logger.info(f"维修工单名称：{woinfo_name}，工单id：{woinfo_id}")

        with allure.step("获取项目下建筑id、楼层id"):
            building_id, building_name, building_floor_id, building_floor_name = location_tree(self.project_id, self.caozuoyuan_token)
            self.__logger.info(f"建筑名称：{building_name}，建筑id：{building_id}，楼层名称：{building_floor_name}，楼层id：{building_floor_id}")

        with allure.step("维修工单"):
            cm_info = "这是维修情况"
            cm_desc = "这是耗材信息"
            repair_woinfo(
                id=woinfo_id,
                location_id=building_floor_id,
                building_id=building_id,
                cm_info=cm_info,
                cm_desc=cm_desc,
                token=self.caozuoyuan_token,
            )
            self.__logger.info(f"维修情况：{cm_info}，耗材信息：{cm_desc}")

        with allure.step("搜索断言"):
            res = woinfo_list(key=self.woinfo_depiction, size=1, token=self.qiguan_token)

            assert (
                res[0]["name"] == self.woinfo_depiction and res[0]["status"] == 2 and not self.__logger.info(f"搜索断言成功，故障描述：{self.woinfo_depiction}")
            )

    @pytest.mark.run(order=4)
    @allure.title("主管不验收通过故障维修工单")
    def test_acceptance_not_through_woinfo(self, global_data):
        woinfo_id = global_data.get("woinfo_id")
        woinfo_name = global_data.get("woinfo_name")
        self.__logger.info(f"主管不验收通过工单名称：：{woinfo_name}，工单id：{woinfo_id}")

        with allure.step("验收工单"):
            check_desc = "验收不通过！！！！"
            check_order(
                id=woinfo_id,
                check_status=2,
                plan_type=0,
                check_desc=check_desc,
                token=self.zhuguan_token,
            )
            self.__logger.info(f"验收描述：{check_desc}")

        with allure.step("搜索断言"):
            res = woinfo_list(key=self.woinfo_depiction, size=1, token=self.qiguan_token)

            assert (
                res[0]["name"] == self.woinfo_depiction and res[0]["status"] == 2 and not self.__logger.info(f"搜索断言成功，故障描述：{self.woinfo_depiction}")
            )

    @pytest.mark.run(order=5)
    @allure.title("高级客户验收通过故障维修工单")
    def test_acceptance_pass_woinfo(self, global_data):
        woinfo_id = global_data.get("woinfo_id")
        woinfo_name = global_data.get("woinfo_name")
        self.__logger.info(f"高级客户验收通过工单名称：{woinfo_name}，工单id：{woinfo_id}")

        with allure.step("验收工单"):
            check_desc = "验收通过啦！！！！"
            check_order(
                id=woinfo_id,
                check_status=1,
                plan_type=0,
                check_desc=check_desc,
                token=self.gaojikehu_token,
            )
            self.__logger.info(f"验收描述：{check_desc}")

        with allure.step("搜索断言"):
            res = woinfo_list(key=self.woinfo_depiction, size=1, token=self.qiguan_token)

            assert (
                res[0]["name"] == self.woinfo_depiction and res[0]["status"] == 3 and not self.__logger.info(f"搜索断言成功，故障描述：{self.woinfo_depiction}")
            )

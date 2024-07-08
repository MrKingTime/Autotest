from api.login import account_login
from api.systemSetting import location_tree, search_project
from api.maintenance import get_dict, find_sys_tree_by_pid, increase_device, device_list
from tools.logger import get_logger
from time import sleep
import settings
import pytest
import random
import allure


@allure.epic("设备台账")
@pytest.mark.device
class TestDevice:
    """设备台账"""

    caozuoyuan_token = None
    zhuguan_token = None
    qiguan_token = None
    gaoji_token = None

    def setup_class(self):
        self.__logger = get_logger()

        self.caozuoyuan_token = account_login(username=settings.CAOZUOYUAN_USER, password=settings.DEFAULT_PASSWORD)
        self.zhuguan_token = account_login(username=settings.ZHUGUAN_USER, password=settings.DEFAULT_PASSWORD)
        self.qiguan_token = account_login(username=settings.QIGUAN_USER, password=settings.DEFAULT_PASSWORD)
        self.gaoji_token = account_login(username=settings.GAOJIKEHU_USER, password=settings.DEFAULT_PASSWORD)

        self.__logger.info("故障维修用例集初始化")
        self.__logger.info(
            f"caozuoyuan_token: {self.caozuoyuan_token} zhuguan_token: {self.zhuguan_token} qiguan_token: {self.qiguan_token} gaoji_token: {self.gaoji_token}"
        )
        assert self.caozuoyuan_token and self.zhuguan_token and self.qiguan_token and self.gaoji_token

    @pytest.mark.run(order=1)
    @allure.title("创建设备台账")
    @pytest.mark.skip("跳过创建设备台账")
    def test_increase_device(self):
        """创建设备台账"""
        self.__logger.info("开始创建设备台账")

        with allure.step("获取项目id"):
            project_id = search_project(settings.PROJECT_DEVICE_NAME, self.qiguan_token)
            self.__logger.info(f"项目名称：{settings.PROJECT_DEVICE_NAME}，项目id：{project_id}")

        with allure.step("获取项目的建筑楼层数据"):
            building_id, building_name, building_floor_id, building_floor_name = location_tree(project_id, self.qiguan_token)
            self.__logger.info(f"建筑名称：{building_name}，建筑id：{building_id}，楼层名称：{building_floor_name}，楼层id：{building_floor_id}")

        with allure.step("获取字典数据"):
            levels = get_dict(project_id, 1, self.qiguan_token)
            states = get_dict(project_id, 2, self.qiguan_token)
            level = random.choice(levels)
            state = random.choice(states)

            self.__logger.info(f"设备等级：{level['name']}")
            self.__logger.info(f"设备状态：{state['name']}")

        with allure.step("获取项目的维保标准系统"):
            sys_pids = find_sys_tree_by_pid(project_id, self.qiguan_token)
            sys = random.choice(sys_pids)
            sub_sys = random.choice(sys["subSysList"])

            self.__logger.info(f"维保标准系统列表：{sys_pids}")
            self.__logger.info(f"系统名称：{sys['name']}，系统id：{sys['id']}")
            self.__logger.info(f"设备名称：{sub_sys['name']}，设备id：{sub_sys['id']}")

        with allure.step("创建设备台账"):

            self.__logger.debug(
                f"project_id: {project_id} building_id: {building_id} building_floor_id: {building_floor_id} d_level: {level['id']} d_state: {state['id']} sys_id: {sys['id']} sub_sys_id: {sub_sys['id']}"
            )
            device_id = increase_device(
                project_id=project_id,
                building_id=building_id,
                location_id=building_floor_id,
                token=self.qiguan_token,
                level=level["id"],
                state=state["id"],
                sys_id=sys["id"],
                sub_sys_id=sub_sys["id"],
                signature_code="123456",
            )
        with allure.step("搜索断言"):
            device_ls = device_list(token=self.qiguan_token, project_ids=[project_id])
            assert device_ls[0]["id"] == device_id and not self.__logger.info(f"搜索断言成功，设备编号：{device_ls[0]['name']}")

    @pytest.mark.run(order=1)
    # @pytest.mark.skip("跳过批量创建设备台账")
    @allure.title("批量创建设备台账")
    def test_increase_devices(self):
        """创建设备台账"""
        self.__logger.info("开始创建设备台账")

        with allure.step("获取项目id"):
            project_id = search_project(settings.PROJECT_DEVICE_NAME, self.qiguan_token)
            self.__logger.info(f"项目名称：{settings.PROJECT_DEVICE_NAME}，项目id：{project_id}")

        location_tree_res = location_tree(project_id, self.qiguan_token, is_random=False)
        levels = get_dict(project_id, 1, self.qiguan_token)
        states = get_dict(project_id, 2, self.qiguan_token)
        sys_pids = find_sys_tree_by_pid(project_id, self.qiguan_token)

        for i in range(10):
            t_building = random.choice(location_tree_res)
            building_id = t_building["id"]
            t_childLocation = random.choice(t_building["childLocation"])
            building_floor_id = t_childLocation["id"]

            sys = random.choice(sys_pids)
            sub_sys = random.choice(sys["subSysList"])

            level = random.choice(levels)
            state = random.choice(states)

            self.__logger.info(f"设备等级：{level['name']}")
            self.__logger.info(f"设备状态：{state['name']}")

            self.__logger.info(f"维保标准系统列表：{sys_pids}")
            self.__logger.info(f"系统名称：{sys['name']}，系统id：{sys['id']}")
            self.__logger.info(f"设备名称：{sub_sys['name']}，设备id：{sub_sys['id']}")

            increase_device(
                project_id=project_id,
                building_id=building_id,
                location_id=building_floor_id,
                token=self.qiguan_token,
                level=level["id"],
                state=state["id"],
                sys_id=sys["id"],
                sub_sys_id=sub_sys["id"],
                signature_code="123456",
            )
            self.__logger.debug(f"创建设备台账成功======{i}")
            sleep(1.3)

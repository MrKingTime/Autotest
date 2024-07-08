from api.login import account_login
from api.detection_and_assessment import create_detection, create_assessment, search_assessment, search_detection, \
    search_items, search_faces, getIdempotenceToken, point_save, completeTest, result_ser, result, auditProject, \
    sign_detection
from api.public import upload_file
from tools.logger import get_logger
import settings
import pytest
import datetime
import allure
from api.Search_excel import Ser_excel
from tools.yaml_util import YamlUtil

@pytest.fixture(scope="session", autouse=True)
def clear_yaml():
    YamlUtil().clear_extract_yaml()


@allure.epic("消防检测、安全评估")
@pytest.mark.detection
class TestDetection:
    """消防检测、安全评估"""

    caozuoyuan_token = None
    zhuguan_token = None
    qiguan_token = None
    gaojikehu_token = None

    date_msg = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")

    def setup_class(self):
        self.__logger = get_logger()

        self.caozuoyuan_token = account_login(username=settings.CAOZUOYUAN_USER, password=settings.DEFAULT_PASSWORD)
        self.zhuguan_token = account_login(username=settings.ZHUGUAN_USER, password=settings.DEFAULT_PASSWORD)
        self.qiguan_token = account_login(username=settings.QIGUAN_USER, password=settings.DEFAULT_PASSWORD)
        self.gaojikehu_token = account_login(username=settings.GAOJIKEHU_USER, password=settings.DEFAULT_PASSWORD)
        YamlUtil().write_extract_yaml(
            {'caozuoyuan_token': account_login(username=settings.CAOZUOYUAN_USER, password=settings.DEFAULT_PASSWORD)})

        YamlUtil().write_extract_yaml(
            {'zhuguan_token': account_login(username=settings.ZHUGUAN_USER, password=settings.DEFAULT_PASSWORD)})

        YamlUtil().write_extract_yaml(
            {'qiguan_token': account_login(username=settings.QIGUAN_USER, password=settings.DEFAULT_PASSWORD)})

        YamlUtil().write_extract_yaml(
            {'gaojikehu_token': account_login(username=settings.GAOJIKEHU_USER, password=settings.DEFAULT_PASSWORD)})
        YamlUtil().write_extract_yaml({'gpsx': '23.164495985243054'})
        YamlUtil().write_extract_yaml({'gpsy': '113.4452601453993'})

        self.__logger.info("消防检测、安全评估用例集初始化")
        self.__logger.info(
            f"caozuoyuan_token: {self.caozuoyuan_token}，zhuguan_token: {self.zhuguan_token}，qiguan_token: {self.qiguan_token}，gaojikehu_token: {self.gaojikehu_token}"
        )
        assert self.caozuoyuan_token and self.zhuguan_token and self.qiguan_token and self.gaojikehu_token

    @pytest.mark.run(order=1)
    @allure.title("创建检测任务")
    @pytest.mark.parametrize('datas', [Ser_excel().search()])
    def test_create_detection(self, datas):
        with allure.step("上传文件"):
            file_res = upload_file(datas['file_path'],
                                   token=YamlUtil().read_extract_yaml('qiguan_token'))
            print(file_res)
            self.__logger.info(f"上传文件成功，文件名：{file_res['title']}，文件内容：{file_res}")

        with allure.step("创建检测任务"):
            name = f"{datas['name']}"
            res = create_detection(
                name=name,
                # 合同文件
                contract_file_path=file_res["localSavePath"],
                contract_file_name=file_res["title"],
                # 检测方案
                test_plan_file_path=file_res["localSavePath"],
                test_plan_file_name=file_res["title"],
                token=YamlUtil().read_extract_yaml('qiguan_token'),
            )
            res = str(res)
            # self.__logger.info(f"数据：{res}还有类型：" + type(res).__name__)
            YamlUtil().write_extract_yaml({'projectId': res})
            # self.__logger.info(f"创建检测任务，项目名称：{name}")

        with allure.step("搜索断言"):
            res = search_detection(name=name, size=1, token=YamlUtil().read_extract_yaml('qiguan_token'))

            assert res[0]["name"] == name and not self.__logger.info(f"搜索断言成功，检测项目名称：{name}")

    @pytest.mark.run(order=2)
    @allure.title("签到检测任务")
    def test_sign(self):
        with allure.step("签到检测任务"):
            YamlUtil().write_extract_yaml({'file_path1': "测试图片A.png"})
            YamlUtil().write_extract_yaml({'file_path2': "测试图片B.png"})
            build_img_res = upload_file(YamlUtil().read_extract_yaml('file_path1'),
                                        token=YamlUtil().read_extract_yaml('caozuoyuan_token'))
            face_img_res = upload_file(YamlUtil().read_extract_yaml('file_path2'),
                                       token=YamlUtil().read_extract_yaml('caozuoyuan_token'))
            YamlUtil().write_extract_yaml({'build_img_name': build_img_res["localSavePath"], })
            YamlUtil().write_extract_yaml({'face_img_name': face_img_res["localSavePath"]})
            sign_detection(
                token=YamlUtil().read_extract_yaml('caozuoyuan_token'),
                build_img=build_img_res["localSavePath"],
                face_img=face_img_res["localSavePath"],
                project_type=2,
                type=1,
            )
            # self.__logger.info(
            #     f"build_img_name：{YamlUtil().read_extract_yaml('build_img_name')}，face_img_name：{YamlUtil().read_extract_yaml('face_img_name')}，gpsx：{YamlUtil().read_extract_yaml('gpsx')}，gpsy：{YamlUtil().read_extract_yaml('gpsy')}")

    @pytest.mark.run(order=3)
    @allure.title("执行检测任务")
    def test_implement(self):
        with allure.step("执行检测任务"):
            IdempotenceToken = getIdempotenceToken()
            self.__logger.info("查询检测任务")
            res = search_items(IdempotenceToken)
            self.__logger.info(f'查询检测任务结果：{res}')

            self.__logger.info("检测任务查询")
            res = search_faces()
            self.__logger.info(f"现场检测：{res}")

            list_of_ones = ['1'] * len(res)
            testingResult = ','.join(list_of_ones)
            IdempotenceToken = getIdempotenceToken()
            YamlUtil().write_extract_yaml({'IdempotenceToken': IdempotenceToken})
            point_save(testingResult)

            self.__logger.info("保存检测")
            completeTest()

            res = result_ser()
            if type(res) == bool:
                assert res ==bool and not self.__logger.debug('获取审批列表失败，请检查路径/参数')
            list_of_ones = ['1'] * len(res)
            testingResult = ','.join(list_of_ones)

            result(testingResult)
            self.__logger.info(f'填写结论说明')

            auditProject(YamlUtil().read_extract_yaml('caozuoyuan_token'))
            self.__logger.info('[审核通过]审核人操作员审核')

            auditProject(YamlUtil().read_extract_yaml('zhuguan_token'))
            self.__logger.info('[审核通过]审核人主管审核')

    @pytest.mark.run(order=2)
    @allure.title("创建评估任务")
    def test_create_assessment(self):
        with allure.step("上传文件"):
            file_full_res = upload_file("CN107415837A车载无人机和自动撑伞系统及方法.pdf", full_data=True, token=self.qiguan_token)
            self.__logger.info(f"上传文件成功，文件名：{file_full_res['data']['title']}，文件内容：{file_full_res}")

        with allure.step("创建评估任务"):
            name = f"评估任务-{self.date_msg}"
            create_assessment(
                name=name,
                file_full_res=file_full_res,
                contract_path=file_full_res["data"]["localSavePath"],
                contract_name=file_full_res["data"]["title"],
                token=self.qiguan_token,
            )
            self.__logger.info(f"创建评估任务，项目名称：{name}")

        with allure.step("搜索断言"):
            res = search_assessment(name=name, size=1, token=self.qiguan_token)

            assert res[0]["name"] == name and not self.__logger.info(f"搜索断言成功，评估项目名称：{name}")

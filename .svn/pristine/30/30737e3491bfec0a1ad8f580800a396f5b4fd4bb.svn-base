import pytest
import subprocess

if __name__ == "__main__":
    """
    -s: 显示程序中的print/logging输出
    -v: 丰富信息模式, 输出更详细的用例执行信息
    -q: 安静模式, 不输出环境信息
    -x: 出现一条测试用例失败就退出测试。调试阶段非常有用
    -k：可以使用and、not、or等逻辑运算符，区分：匹配范围（文件名、类名、函数名）
    pytest-rerunfailures --reruns n(重试次数) --reruns-delay  m(重试间隔时间，单位S)
    -s -v --reruns 1 --reruns-delay 5 --alluredir ./allure/result --clean-alluredir
    """
    args = {
        # 基础
        "base": ["-s", "-v"],
        # primary为用例标签 device woinfo maintenance detection
        "tag": ["-m", "detection"],
        # 重试
        # "reruns": ["--reruns", "10", "--reruns-delay", "5"],
        # allure
        "allure": ["--alluredir", "./allure/result", "--clean-alluredir"],
    }
    pytest.main([j for i in args.values() for j in i])

    # subprocess.Popen("allure generate allure/result/ -o allure/html --clean", shell=True) # 生成allure测试报告

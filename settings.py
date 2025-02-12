BASE_URL = "http://fas-sit.acmeict.com/api"

TITLE = "消防"

ENTERPRISE_NAME = "全量测试企业"
# ENTERPRISE_NAME = "接口测试企业"
PROJECT_SYSTEM_NAME = "全量测试-按系统"
# PROJECT_SYSTEM_NAME = "按系统"
PROJECT_DEVICE_NAME = "全量测试-按设备5"
# PROJECT_DEVICE_NAME = "按设备"

USER_PREFIX = "ql-"
CAOZUOYUAN_USER = f"{USER_PREFIX}caozuoyuan"
QIGUAN_USER = f"{USER_PREFIX}qiguan"
ZHUGUAN_USER = f"{USER_PREFIX}zhuguan"
GAOJIKEHU_USER = f"{USER_PREFIX}gaojikehu"
DEFAULT_PASSWORD = "qwe123"

# 创意大厦B3
GPS_X = "23.16446967230903"
GPS_Y = "113.45058892144097"

CASE_DATA_PATH = "case_data.xlsx"


# 枚举，可单独存为一个文件
TASK_NAME_ENUM = {
    "patrols": {
        "value": "巡查",
        "description": "巡查任务",
    },
    "maintains": {
        "value": "保养",
        "description": "保养任务",
    },
}

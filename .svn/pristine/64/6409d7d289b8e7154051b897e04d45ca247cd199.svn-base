import pytest

_global_data = {}


@pytest.fixture
def global_data():
    """设置全局变量，用于关联参数

    :return _type_: _description_
    """

    class GlobalData:
        @classmethod
        def set(cls, key, value):
            _global_data[key] = value
            return True

        @classmethod
        def get(cls, key):
            return _global_data.get(key)

    return GlobalData

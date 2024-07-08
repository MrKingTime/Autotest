import pytest


@pytest.mark.dependency()
def test_add():
    print("我是 test_add 用例")
    assert True


@pytest.mark.dependency()
def test_update():
    print("我是 test_update 用例")
    assert False


@pytest.mark.dependency(depends=["test_add", "test_update"])
def test_delete():
    print("我是 test_delete 用例")
    assert True


@pytest.mark.dependency(depends=["test_add"])
def test_select():
    print("我是 test_select 用例")
    assert True


if __name__ == "__main__":
    pytest.main(["-s", "-v"])

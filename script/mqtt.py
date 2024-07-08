from paho.mqtt import client as mqtt
from datetime import datetime
import uuid
import json
import time
import random


def on_connect(client, userdata, flags, rc):
    """
    一旦连接成功, 回调此方法
    rc的值表示成功与否：
        0:连接成功
        1:连接被拒绝-协议版本不正确
        2:连接被拒绝-客户端标识符无效
        3:连接被拒绝-服务器不可用
        4:连接被拒绝-用户名或密码不正确
        5:连接被拒绝-未经授权
        6-255:当前未使用。
    """
    rc_status = ["连接成功", "协议版本不正确", "客户端标识符无效", "服务器不可用", "用户名或密码不正确", "未经授权"]
    print("connect：", rc_status[rc])


def mqtt_connect():
    """连接MQTT服务器"""
    mqttClient = mqtt.Client(str(uuid.uuid4()))
    mqttClient.on_connect = on_connect  # 返回连接状态的回调函数
    MQTTHOST = "192.168.109.102"  # MQTT服务器地址
    MQTTPORT = 1883  # MQTT端口
    # mqttClient.username_pw_set("username", "password")  # MQTT服务器账号密码, 无密码时注释即可
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()  # 启用线程连接

    return mqttClient


def mqtt_publish():
    """发布主题为'mqtt/demo',内容为'Demo text',服务质量为2"""
    mqttClient = mqtt_connect()
    # 复位
    # data = {
    #     "params": {"aLevel": 2},
    #     "uid": "H1FYZMJYSQUF",
    #     "eui": "H1FYZMJYSQUF",
    #     "pLink": 2,
    #     "mType": 1,
    #     "atChn": 7289653804535530,
    #     "ackNum": 2,
    #     "confirm": 161,
    #     "time": 1689843311,
    # }
    # mqttClient.publish("gateway/alarm/v3/1001002128/H1FYZMJYSQUF", json.dumps(data), 2)
    # mqttClient.loop_stop()
    # return
    for i in range(3):
        timestamp = int(datetime.now().timestamp())
        data = {
            "params": {
                "action": 1,
                "aType": 1,
                "aTime": int(datetime.now().timestamp()),
                "aAddres": "广东省广州市黄埔区科学城地铁旁创意大厦B3",
                "aDevType": f"测试报警推送-{i}-{timestamp}",
                "aMsg": f"测试报警推送-{i}-{timestamp}",
                "aChnAdr": f"2-162-{i}-{timestamp}",
            },
            "uid": "H1FYZMJYSQUF",
            "eui": "H1FYZMJYSQUF",
            "pLink": 2,
            "mType": 1,
            "atChn": 7289653804535530,
            "ackNum": 2397,
            "confirm": 161,
            "time": timestamp,
        }

        mqttClient.publish("gateway/alarm/v3/1001002128/H1FYZMJYSQUF", json.dumps(data), 2)
        print(i)
        time.sleep(0.1)
    mqttClient.loop_stop()


if __name__ == "__main__":
    mqtt_publish()

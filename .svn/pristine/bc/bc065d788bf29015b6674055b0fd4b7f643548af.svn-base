import os
import yaml


class YamlUtil:

    # 读取extract.yml文件
    def read_extract_yaml(self, key):
        with open(os.getcwd() + "/extract.yaml", mode="r", encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value[key];

    # 写入extract.yml文件
    def write_extract_yaml(self, data):
        with open(os.getcwd() + "/extract.yaml", mode="a", encoding="utf-8") as f:
            yaml.dump(data=data, stream=f, allow_unicode=True)

    # 清除extract.yml文件
    def clear_extract_yaml(self):
        with open(os.getcwd() + "/extract.yaml", mode="w", encoding="utf-8") as f:
            f.truncate()

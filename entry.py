# _*_ coding: utf-8 _*_
from ivy.global_manage import global_manage
from ivy.center import Center
import yaml
import os

root_path = os.path.abspath('.')

config_path = root_path + os.path.sep + 'config' + os.path.sep

configs = list(filter(lambda x: '.yml' in x, os.listdir(config_path)))

padding_data = ''

for config in configs:
    with open(config_path + config) as f:
        padding_data += f.read()


db_config = yaml.load(padding_data, Loader=yaml.FullLoader)

print(db_config)

global_manage.set(db_config)

Center().run()

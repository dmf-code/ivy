# _*_ coding: utf-8 _*_
from ivy.manages.database import Database
from ivy.manages.context import Context
from ivy.facade import Facade
from ivy.center import Center
import yaml
import os

root_path = os.path.abspath('.')

config_path = root_path + os.path.sep + 'config' + os.path.sep

configs = list(filter(lambda x: '.yml' in x, os.listdir(config_path)))

padding_data = ''

for config in configs:
    with open(config_path + config, 'r', encoding='utf-8') as f:
        padding_data += f.read()


database_config = yaml.load(padding_data, Loader=yaml.FullLoader)

Facade().set('context', Context())

Facade().set('database', Database())

Context().set(database_config)

Center().run()

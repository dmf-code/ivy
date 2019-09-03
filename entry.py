# _*_ coding: utf-8 _*_
from ivy.global_manage import global_manage
from ivy.center import Center
import yaml
import os

root_path = os.path.abspath('.')

with open(root_path + os.path.sep + 'padding_data.yml') as f:
    padding_data = f.read()

db_config = yaml.load(padding_data, Loader=yaml.FullLoader)

global_manage.set(db_config)

Center().run()

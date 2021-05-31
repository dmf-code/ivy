### 概述

ivy是一个配置化的数据填充框架，主要解决的场景

1. 帮助你更好的去处理开发项目前无数据的尴尬
2. 摆脱手动创建数据库和数据表的繁琐工作
3. 快速生成数据后台所要的模拟数据，帮助你更快编写数据统计的逻辑开发

采用配置化的模式，使工作更加高效。配置多个主机模拟数据只要在文件配一下，就能够实现你想要的效果。

> 核心思想是解放劳动力，让你能够在不编写或最少写代码的情况下完成填充的任务

代码结构：

```text
+---config // 批量操作配置文件目录 
+---ivy 
| +---abstracts // 接口类目录 
| +---functions // 生成随机数的函数目录 
| +---manages // 具体逻辑实现管理目录
+---readme // 文档目录
```

### 要求

Python3+

Works on Linux, Windows, Mac OSX, BSD

### 文档

#### `default.yml` 配置文件（遵循 `yaml` 语法）

##### 主要做两个功能：

1. 配置实现数据库，数据表自动创建
2. 填充数据，完全支持 `faker` 库

配置文件直接写在 `config` 目录就可以了，不过要注意这里只认识 `.yml` 后缀的配置文件哦。所以只要定义了 `yml` 的文件都会被执行的哦

##### 栗子：

```yaml

- host: 127.0.0.1
  port: 3306
  username: root
  password: root
  charset: utf8mb4
  dbname: faker
  tables:
    - table: news
      flag: 1-news
      fields:
        id: INT NOT NULL AUTO_INCREMENT
        created_at: datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
        updated_at: datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间'
        deleted_at: datetime DEFAULT NULL COMMENT '删除时间'
        index:
          - PRIMARY KEY (id)
        other:
          - ENGINE=InnoDB
          - DEFAULT
          - CHARSET=utf8mb4
      rules:
        id:
          func: id_auto_increment
          database: faker
          table: news

    - table: news_content
      flag: 2-news_content
      fields:
        id: int NOT NULL AUTO_INCREMENT
        news_id: int NOT NULL COMMENT '新闻关联id'
        name: varchar(30) DEFAULT '' COMMENT '名称'
        img: varchar(256) DEFAULT '' COMMENT '文章图片'
        content: text COMMENT '文章内容'
        lang: tinyint DEFAULT '1' COMMENT '1.中文 2.英文'
        created_at: datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
        updated_at: datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间'
        deleted_at: datetime DEFAULT NULL COMMENT '删除时间'
        index:
          - PRIMARY KEY (id)
        other:
          - ENGINE=InnoDB
          - DEFAULT
          - CHARSET=utf8mb4

      rules:
        news_id:
          func: cell_conversion
          flag: 1-news
          name: id
        name:
          func: faker|name
        img:
          func: default_random
          array:
            - uploads/Ey3753aMp6lTxGZPnTMPx84xVlIPrb35RIBCV7Ny.jpg
            - uploads/Ey3753aMp6lTxGZPnTMPx84xVlIPrb35RIBCV7Ny.jpg

      lines: [ 1-news, 2-news_content ]
      number: 10
      chunk: 1
```

> 这里面使用数组的形式进行配置，每个数组对应一个服务器地址， 想要填充多个服务器上面的数据库就需要对其进行数组配置

##### `host`: 数据库 `ip`

```yaml
host: 127.0.0.1
```

##### `port`: 数据库端口

```yaml
prot: 3306
```

##### `username`: 数据库用户名

```yaml
username: root
```

##### `password`: 数据库密码

```yaml
password: 数据库密码
```

##### `charset`: 数据表编码

```yaml
charset: utf8mb4
```

##### `dbname`: 数据库库名

```yaml
dbname: faker
```

##### `tables`: 数据表配置集合

```yaml
tables: 
```

##### `table`: 数据表名称

```yaml
table: news
```

##### `flag`: 数据表唯一标识（逻辑运算需要）

```yaml
flag: 1-news
```

##### `fields`: 数据表字段

```yaml
fields:
  id: INT NOT NULL AUTO_INCREMENT
  created_at: datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
  updated_at: datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间'
  deleted_at: datetime DEFAULT NULL COMMENT '删除时间'
```

##### `index`: 数据表索引

```yaml
index:
  - PRIMARY KEY (id)
```

##### `other`: 数据表 `engine` 一些字段

```yaml
other:
  - ENGINE=InnoDB
  - DEFAULT
  - CHARSET=utf8mb4
```

##### `rules`: 数据表数据填充规则

```yaml
rules:
  id:
    func: id_auto_increment
    database: faker
    table: news
```

##### `lines`: 一组随机规则编排数组

```yaml
lines: [ 1-news, 2-news_content ]
```

##### `number` 要填充的总数

```yaml
number: 10
```

##### `chunk`: 分组插入每组的数量 （number / chunk）

```yaml
chunk: 1
```

#### 自定义填充函数

在 `functions` 目录下编写相关代码即可。

`__init__.py`

```python
# -*- coding: utf-8 -*-
from ivy.functions.id import Id
from ivy.functions.date import Date
from ivy.functions.cell import Cell
from ivy.functions.default import Default

funcs = {
    'id_auto_increment': Id().auto_increment,  # 获取自增 id
    'cell_conversion': Cell().conversion,  # pipeline 每个元素状态保存
    'date_range': Date().range,  # 日期范围随机返回
    'default': Default().default,  # 返回设置默认值
    'default_random': Default().random  # 返回配置中的随机默认值
}
```

然后编写相关类即可，可参考 `default.py` 文件

#### 填充的规则定义如下

1. 自定义的处理函数要在 `ivy/functions/__init__.py` 中定义函数名称，就是用在配置中的 `func` 哦。

##### `id_auto_increment`  获取自增 id

```yaml
func: id_auto_increment
database: faker  # 数据库
table: news  # 数据表
```

##### `cell_conversion` 跨表数据传输

```yaml
func: cell_conversion
flag: 1-news  # 数据表配置的 flag
name: id  # 跨表拿取的字段
```

##### `date_range` 日期范围随机返回

```yaml
func: date_range
start: 2021-05-01  # 开始时间
end: 2021-05-31  # 结束时间
res_format: '%Y-%m-%d'  # 生成的时间格式
step: DAY_TO_SECOND  # 控制时间间隔，具体常量DAY_TO_SECOND，HOUR_TO_SECOND，MINUTE_TO_SECOND,SECOND
```

##### `default` 返回自身设置的值

```yaml
func: default
value: test
```

##### `default_random` 随即返回配置的值

```yaml
func: default_random
array:
  - 1
  - 2
  - 3
```

2. `faker` 库的调用，这里面要直接带上 `faker` 前缀,然后用|来对其进行分割，这里面不允许使用空格。然后后面带上
   `faker` 库中的函数调用就行了。例如上面例子中，直接使用 `name` 这个函数调用。具体还可以使用什么函数参考 `faker`
   库的官网

https://faker.readthedocs.io/en/master/locales/zh_CN.html

### 安装并使用

1. 安装需要使用的库

```shell
pip install -r requirements.txt
```

2. 配置`config` 目录下的 `default.yml` 文件，这里按照 `yaml` 语法配置就可以了

3. 生成数据库并填充数据

```shell
python entry.py
```

4. 效果如下

![1567489373143](./readme/1567489373143.png)


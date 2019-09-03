### 配置化数据填充

padding_data.yml 配置文件（遵循yaml语法）

主要做两个功能：

1.配置实现数据库，数据表自动创建

2.填充数据，方便测试使用，比如数据统计需要的数据等

栗子：

```

-
  host: 192.168.3.9
  port: 9003
  username: root
  password: root
  charset: utf8mb4
  dbname: faker
  databases:
    -
      table: faker
      fields:
        id: INT NOT NULL AUTO_INCREMENT
        name: VARCHAR(20) NOT NULL
        date: timestamp NOT NULL
        index:
          - PRIMARY KEY (id)
        other:
          - ENGINE=InnoDB
          - DEFAULT
          - CHARSET=utf8mb4

      fill_rule:
        date:
          func: range_date
          start: '2019-07-20'
          end: '2019-08-20'
          res_format: '%Y-%m-%d %H-%M-%S'
          step: HOUR_TO_SECOND

        name:
          func: faker|name

      number: 5

```

tips:

- 这里面使用数组的形式进行配置，每个数组对应一个服务器地址，
想要填充多个服务器上面的数据库就需要对其进行数组配置

host: 数据库服务器ip

port: 数据库服务器端口

username: 数据库用户名

password: 数据库密码

charset: 编码

dbname: 创建的数据库名

databases: 数据库表数组

table: 数据表名

fields: 数据表字段

index: 数据表索引

other: 数据表外层engine这些

fill_rule: 数据库填充的内容设置

number: 要填充的数量


- 填充的规则定义如下

1.自定义的处理函数要在 `ivy/functions/__init__.py` 中定义函数名称，就是用在配置中的 `func` 哦。

```buildoutcfg
date: 
    start: 开始时间
    end: 结束时间
    res_format: 生成的时间格式
    step: 控制时间间隔，具体常量DAY_TO_SECOND，HOUR_TO_SECOND，MINUTE_TO_SECOND,SECOND
```

2.`faker` 库的调用，这里面要直接带上 `faker` 前缀,然后用|来对其进行分割，这里面不允许使用空格。然后后面带上
`faker` 库中的函数调用就行了。例如上面例子中，直接使用 `name` 这个函数调用。具体还可以使用什么函数参考 `faker`
库的官网

https://faker.readthedocs.io/en/master/locales/zh_CN.html


- 使用

1.安装需要使用的库
```shell
pip install -r requirements.txt
```

2.配置padding_data.yml文件，这里按照yaml语法配置就可以了

3.生成数据库并填充数据
```shell
python entry.py
```

![1567489373143](F:\Python\ivy\readme\1567489373143.png)


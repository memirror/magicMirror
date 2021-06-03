Generic single-database configuration.

```
使用：
    - 1. cd 到你的项目目录中，创建一个名叫migration<或者alembic等>的仓库
            alembic init migration
    - 2. 修改alembic.ini
            sqlalchemy.url     #注释掉
            script_location   #如果不更改默认到上一步创建位置>
    - 3. 修改env.py
            config.set_main_option("sqlalchemy.url", "mysql+pymysql://user:password@localhost:3306/databasename?charset=utf8mb4")
            target_metadata = your-project.metadata  # example: Base.metadata
    - 4. 数据库中生成对应表
            alembic revision --autogenerate -m "init<your-commit>"
    - 5. 查看并修改versions脚本中建表|删表语句
            5.1 若对应database已经存在，该初始脚本里会有已存在表的删除[upgrade]新建[downgrade]，如果不希望被更改，则删除对应语句
            5.2 如果用到sqlalchemy-utils中字段类型，需要更改脚本中语句到对应类型
    - 6. 更新到数据库
            alembic upgrade head
    - 7. 数据库字段类型等更改后
            alembic revision --autogenerate -m 'your-annotation'
    - 8. 转到#5
    - 9. 执行同步<upgrade or downgrade>
            alembic upgrade   'your-new-version'
            alembic downgrade 'your-pre-version'
```

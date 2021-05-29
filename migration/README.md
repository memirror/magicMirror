Generic single-database configuration.

```
使用：
    - 0. 在终端中，cd到你的项目目录中，然后执行命令alembic init alembic，创建一个名叫alembic的仓库。
    - 1. 修改alembic.ini 中sqlalchemy.url， script_location
    - 2. 修改env.py 中 metadata
    - 3. alembic init migration 初始化
    - 4. alembic revision --autogenerate -m "init"
    - 5. 根据versions中init生成的版本号，
         alembic upgrade 'your-init-version'
    - 6. alembic revision --autogenerate -m 'your-annotation'
    - 7. 到versions中生成的新py文件查看并调整downgrade, upgrade 函数
    - 8. 升级则 alembic upgrade   'your-new-version'
         降级   alembic downgrade 'your-pre-version'
```

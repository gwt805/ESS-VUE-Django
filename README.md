# ESS-VUE-Django

#### 介绍
ESS系统由VUE+Django+MySQL 前后端分离实现；是来记录标注人员的工作量，查看工作效率、绩效；也是来记录给供应商送标数据的详情，包含哪个项目的已使用金额及标注预算使用百分比


#### 安装&使用教程
```bash
    1. 修改 client/src/utils/axios/index.ts 的 baseURL 地址
    
    2. cd client && npm install && npm run build

    3. 修改 server/config.json 相关配置
        3.1 mysql_host 为本机真实 ip
        3.2 mysql 其他配置为 docker-compose.yml 中的配置

    4. docker-compose up -d

    5. 进入到 ess-server-django container 中 进行数据库迁移等操作
        5.1 python manage.py makemigrations
        5.2 python manage.py migrate
        5.3 python manage.py createsuperuser
    
    6. 进入到 ess-db container 中 把刚刚创建的 superuser power 改成 1

    7. ip:5173 访问

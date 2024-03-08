# ESS-VUE-Django

#### 介绍
ESS系统由VUE+Django+MySQL 前后端分离实现；是来记录标注人员的工作量，查看工作效率、绩效；也是来记录给供应商送标数据的详情，包含哪个项目的已使用金额及标注预算使用百分比


#### 安装&使用教程
```bash
# server: python>=3.6 & node:18
    npm install phantomjs-prebuilt -g

    chmod a+rw ess-vue-django

    chmod -R 777 ess-vue-django

    cd server

    # 先配置config.json 配置文件, 然后再执行下面命令

    chmod +x ess_server_auto_start.sh # 可选

    chmod +x ess_server_listen_kafka.sh # 可选

    pip install -r requirements.txt

    python manage.py collectstatic # 如果DEBUG为False时(root_stati文件夹已存在时,先删除在执行)

    python manage.py runserver 0.0.0.0:8088

    # 实时 监听 Kafka 消息，存储相关消息
    python manage.py listenkfk --start_listen_kafka


# client: node:18
    cd client

    # 先修改 utils/axios/index.ts 中的 baseURL , 如果server也在本机执行则不用修改

    chmod +x ess_client_auto_start.sh # 可选

    npm install

    npm run build

    node server.js
```

'''
脚本功能: 实时监听 kafka消息并写入数据库
项目名字和供应商映射关系放在 project_vender_snorlax_to_ess.py
'''

# from .project_vender_snorlax_to_ess import VENDER, PROJECT_NAME
from django.db import connection, OperationalError
from server.settings import CONFIG, BASE_DIR
from cachetools import cached, TTLCache
from service.mes import wb_dingtalk
from kafka import KafkaConsumer
from loguru import logger
from service import models
import time, json
import threading
import datetime
import requests
import ssl

logger.add(f"{BASE_DIR}/logs/ess-kfk.log", rotation="7 days", retention="14 days") # 7天轮转, 只保留14天内的

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

logger.info(f"kfk_topic: {CONFIG['kafka_topic']}")
logger.info(f"kfk_user: {CONFIG['kafka_user']}")
logger.info(f"kfk_pwd: {CONFIG['kafka_pwd']}")
logger.info(f"kfk_server: {CONFIG['kafka_server']}")
logger.info(f"kfk_group_id: {CONFIG['kafka_group_id']}")

def sendMsg(msg):
    nowtime = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # 东八区时间
    today = str(nowtime.year) + "-" + str(nowtime.month) + "-" + str(nowtime.day) + " " + str(nowtime.hour) + ":" + str(nowtime.minute) + ":" + str(nowtime.second)
    contents = f"现在是 {today} 来自ESS\n\r{msg}"

    def task():
        res = requests.post(
            f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={CONFIG['wecom_webhook_key']}", 
            json={
                "msgtype": "text",
                "text": {
                    "content": contents,
                    "mentioned_mobile_list":[CONFIG['wecom_at_phone']]
                }
            }
        )
        logger.info(f"企微机器人消息状态-kfk: {res.json()}")
    
    tasks = threading.Thread(target=task)
    if CONFIG["wecom_webhook_key"] == "":
        logger.info("企业微信机器人还没有配置喔!")
        if CONFIG["wecom_at_phone"] == "":
            logger.info("企业微信机器人 @ 还没有配置喔!")
    else:
        tasks.start()

try:
    consumer = KafkaConsumer(
        CONFIG["kafka_topic"],
        sasl_mechanism = "PLAIN",
        security_protocol='SASL_SSL',
        sasl_plain_username = CONFIG["kafka_user"],
        sasl_plain_password = CONFIG["kafka_pwd"],
        ssl_context = ssl_ctx,
        bootstrap_servers = CONFIG["kafka_server"], #'xxx:xxx,xxxx:xxx'
        auto_offset_reset='earliest', # 正式环境 需要
        group_id = CONFIG["kafka_group_id"] # 正式环境需要
    )
except Exception as e:
    logger.info(f"ESS kafka retry connect...\r\r{e}")
    msg = "ESS kafka 连接异常, 请及时检查!"
    sendMsg(msg)
    raise ValueError(msg)

# cache weather data for no longer than ten minutes / https://github.com/tkem/cachetools/
@cached(cache=TTLCache(maxsize=128, ttl=300))
def get_project_name(project_name):
    try:
        return models.Slesspn.objects.get(slpname=project_name).esspname.pname
    except OperationalError as e:
        logger.info("ESS kafka mysql closed and retry connect...")
        connection.close()
        return models.Slesspn.objects.get(slpname=project_name).esspname.pname

@cached(cache=TTLCache(maxsize=128, ttl=300))
def get_anno_vendor(anno_vendor):
    try:
        return models.Slessvd.objects.get(slvender=anno_vendor).essvender.name
    except OperationalError as e:
        logger.info("ESS kafka mysql closed and retry connect...")
        connection.close()
        return models.Slessvd.objects.get(slvender=anno_vendor).essvender.name

def listen_kafka():
    while True:
        for msg in consumer:
            data = json.loads(msg.value)
            logger.info(data)
            
            for item in ["creator", "creator_email", "project_name", "task_batch_desc", "send_date", "sample_cnt", "data_src", "scene_desc", "send_reason", "keyframe_extracted_method", "annotated_before", "anno_vendor", "anno_task_id"]:
                if item not in data:
                    msg = f"real_time_listen_kfk.py data[{item}] 获取出错!"
                    sendMsg(msg)
                    raise ValueError(msg)

            if len(models.User.objects.filter(email=data["creator_email"])) == 0:
                msg = f"real_time_listen_kfk.py 没有找到 {data['creator']} 的邮箱: {data['creator_email']}!"
                sendMsg(msg)
                raise ValueError(msg)

            try:
                if not models.Slesspn.objects.filter(slpname=data["project_name"]).exists():
                    msg = f"real_time_listen_kfk.py project_name: {data['project_name']} 还没有做映射!"
                    sendMsg(msg)
                    raise ValueError(msg)
            except OperationalError as e:
                logger.info("ESS kafka mysql closed and retry connect...")
                connection.close()
                if not models.Slesspn.objects.filter(slpname=data["project_name"]).exists():
                    msg = f"real_time_listen_kfk.py project_name: {data['project_name']} 还没有做映射!"
                    sendMsg(msg)
                    raise ValueError(msg)
            try:
                if not models.Slessvd.objects.filter(slvender=data["anno_vendor"]).exists():
                    msg = f"real_time_listen_kfk.py anno_vendor: {data['anno_vendor']} 还没有做映射!"
                    sendMsg(msg)
                    raise ValueError(msg)
            except OperationalError as e:
                logger.info("ESS kafka mysql closed and retry connect...")
                connection.close()
                if not models.Slessvd.objects.filter(slvender=data["anno_vendor"]).exists():
                    msg = f"real_time_listen_kfk.py anno_vendor: {data['anno_vendor']} 还没有做映射!"
                    sendMsg(msg)
                    raise ValueError(msg)

            try:
                snorlax_anno_task_id_list = models.SupplierTask.objects.filter(anno_task_id=int(data["anno_task_id"]))
            except OperationalError as e:
                logger.info("ESS kafka mysql closed and retry connect...")
                connection.close()
                snorlax_anno_task_id_list = models.SupplierTask.objects.filter(anno_task_id=int(data["anno_task_id"]))
            
            if len(snorlax_anno_task_id_list) == 0:
                info = {
                    'user': models.User.objects.get(username=models.User.objects.get(email=data["creator_email"]).username), # 邮箱映射
                    'pname': models.Project.objects.get(pname=get_project_name(data["project_name"])),# models.Project.objects.get(pname=PROJECT_NAME[data["project_name"]]),  # 手动映射
                    'send_data_batch': data["task_batch_desc"],
                    'send_data_time': data["send_date"].split("T")[0],
                    'pnums': int(data["sample_cnt"]),
                    'data_source': data["data_src"], 
                    'scene': data["scene_desc"],
                    'send_reason': data["send_reason"],
                    'key_frame_extracted_methods': data["keyframe_extracted_method"],
                    'ann_field_flag': "首次标注" if data["annotated_before"] == "false" or data["annotated_before"] == False else "返修标注",
                    'vendor': models.Supplier.objects.get(name=get_anno_vendor(data["anno_vendor"])),# models.Supplier.objects.get(name=VENDER[data["anno_vendor"]]),  # 手动映射
                    'anno_task_id': int(data["anno_task_id"]),
                    'created_time': datetime.datetime.now().strftime("%Y-%m-%d")
                }
                try:
                    models.SupplierTask.objects.create(**info)
                except OperationalError as e:
                    logger.info("ESS kafka mysql closed and retry connect...")
                    connection.close()
                    models.SupplierTask.objects.create(**info)
                except Exception as e:
                    logger.info(f"{info} \r\r{e}")
                    msg = f"添加 kafka 收到的消息出错了!"
                    sendMsg(msg)
                    raise ValueError(msg)
                wb_dingtalk(models.User.objects.get(email=data['creator_email']).username, "添加", "", info) # 这里 arg1 要拿到中文
                logger.info(info)
        time.sleep(1)
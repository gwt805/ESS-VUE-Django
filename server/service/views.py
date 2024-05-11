import json
import smtplib
import threading
from loguru import logger
from service import models
from datetime import datetime
from email.header import Header
from .utils.gsldap import ldap_auth
from django.http import JsonResponse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from server.settings import CONFIG, BASE_DIR
from service.utils.token import create_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, EmptyPage
from .mes import (
    gsdata_count_public_code,
    nupdate,
    eff_test,
    performanceq,
    search,
    waibao_search,
    gs_data_add,
    dingtalk,
    wb_dingtalk,
    budget_talk,
    budget_reaching_talk,
    get_anno_data_public,
    get_supplier_data_public
)


# Create your views here.
logger.add(f"{BASE_DIR}/logs/ess.log", rotation="7 days", retention="14 days") # 7天轮转, 只保留14天内的

def sendEmail(username: str, password: str, email: str):
    def thread_task():
        try:
            config = CONFIG
            smtp_server = "smtp.qq.com"
            message_html = "<html lang=\"en\"><head><style>#main {width: 550px;height: 400px;margin: auto;background-image: url('https://p8.itc.cn/q_70/images03/20200805/c3cde0e1121341dcbd020b8f1fa33f98.jpeg');background-repeat: no-repeat;background-size: cover;background-attachment: fixed;background-position-y: center;}#main img {width: 100px;height: 100px;display: block;margin: auto;}#main div {height: 40px;margin-top: 20px;}#main div label, #main div input {color: #fff;height: 35px;text-align: center;}#main div label {padding-left: 120px;}#main div input {width: 250px;background: transparent;border:1px solid #fff;}#main div:last-child p {margin: 0;padding: 0 20px;color: #eba565;font-weight: bold;text-align: center;line-height: 30px;}</style><body><div id=\"main\"><img src=\"https://cdn.jsdelivr.net/gh/gwt805/static/imgs/favicon.png\" alt=\"ESS\"><div><label for=\"username\" style=\"color: #fff;\">账号 :&nbsp;</label><input type=\"text\" id=\"username\" value="+username+" disabled></div><div><label for=\"username\" style=\"color: #fff;\">邮箱 :&nbsp;</label><input type=\"text\" id=\"username\" value="+ email+" disabled></div><div><label for=\"username\" style=\"color: #fff;\">密码 :&nbsp;</label><input type=\"text\" id=\"username\" value="+password+" disabled></div><div><p>尊敬的ESS用户您好 !</p><p>这是您ESS系统的最新登录配置 , 您可以使用该账号/邮箱 + 密码来登录</p><p>请一定保管好您的账号密码，切勿告知于他人！</p></div></div></body></html>"
            msg = MIMEMultipart()
            msg["From"] = Header(f"{config['send_qqEmail'].split('@')[0]} <{config['send_qqEmail']}>")
            msg["To"] = Header(f"{username} <{email}>")
            msg["Subject"] = Header("ESS 系统")
            msg.attach(MIMEText(message_html, "html"))

            server = smtplib.SMTP_SSL(smtp_server)
            server.connect(smtp_server, 465)
            server.login(config["send_qqEmail"], config["send_qqEmail_pwd"])
            server.sendmail(config["send_qqEmail"], email, msg.as_string())
            server.quit()

            logger.info(f"用户名和密码已发送到用户 {username} 邮箱")
        except Exception as e:
            logger.error(f"用户 {username} 的邮箱可能不是真的!")
            logger.warning(e)

    task = threading.Thread(target=thread_task)
    if CONFIG["send_qqEmail"] == "" or CONFIG["send_qqEmail_pwd"] == "":
        logger.warning("邮件发送相关配置您还没有操作喔!")
    else:
        task.start()

@csrf_exempt
def regist(request):
    if request.method == "POST":
        data = json.loads(request.body)

        username = data["username"]
        zhuname = data["zhuname"]
        email = data["email"]
        password = data["password"]

        user_is_exit = models.User.objects.filter(username=username).exists()
        email_is_exit = models.User.objects.filter(email=email).exists()
        zhuname_is_exit = models.User.objects.filter(zh_uname=zhuname).exists()

        if ( user_is_exit and email_is_exit and zhuname_is_exit ):
            return JsonResponse({"code": -1, "data": "用户名和邮箱和姓名都已占用!"})
        elif user_is_exit:
            return JsonResponse({"code": -1, "data": "用户名已占用!"})
        elif email_is_exit:
            return JsonResponse({"code": -1, "data": "邮箱已占用!"})
        elif zhuname_is_exit:
            return JsonResponse({"code": -1, "data": "姓名已占用"})
        else:
            user_table = models.User()
            user_table.username = username
            user_table.zh_uname = zhuname
            user_table.set_password(password)
            user_table.email = email
            user_table.save()
            logger.info(f"用户 {username}&{zhuname} 注册成功!")
            sendEmail(username, password, email)
            return JsonResponse({"code": 0, "data": "successful"})

def ldap_regist(username, password, email, zhuname, group):
    user_is_exit = models.User.objects.filter(username=username).exists()
    zhuname_is_exit = models.User.objects.filter(zh_uname=zhuname).exists()

    if ( user_is_exit and zhuname_is_exit ):
        return False, "用户名和姓名都已占用!"
    elif user_is_exit:
        return False, "用户名已占用!"
    elif zhuname_is_exit:
        return False, "姓名已占用"
    else:
        user_table = models.User()
        user_table.username = username
        user_table.zh_uname = zhuname
        user_table.set_password(password)
        user_table.email = email
        user_table.group = group
        user_table.img = "https://img1.baidu.com/it/u=1285375996,3783960243&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500"
        user_table.power = "3"
        user_table.save()
        logger.info(f"用户 {username}&{zhuname} 注册成功!")
        sendEmail(username, password, email)
        return True, "successful"

def ldap_get_user_info(email):
    user_info = models.User.objects.get(email=email)
    uname = user_info.username
    zh_uname = user_info.zh_uname
    group = user_info.group
    imgurl = user_info.img
    power = user_info.power
    return uname, zh_uname, group, imgurl, power

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("user")
        password = data.get("pwd")
        zhuname = data.get("zhuname")
        is_ldap_login = data.get("is_ldap_login")

        if is_ldap_login:
            logger.info("login with ldap......")
            ldap_flag, ldap_uname, ldap_email, ldap_group, ldap_msg = ldap_auth(username, password)
            if ldap_flag:
                email_is_exit = models.User.objects.filter(email=ldap_email).exists()
                if email_is_exit:
                    if models.User.objects.get(email=ldap_email).group != ldap_group:
                        user_model = models.User.objects.get(email=ldap_email)
                        user_model.group = ldap_group
                        user_model.save()
                    uname, zh_uname, group, imgurl, power = ldap_get_user_info(ldap_email)
                    if power == "4":
                        return JsonResponse({"code": -1, "data": "请联系管理员激活账号!"})
                    token = create_token(uname, zh_uname, power)
                    logger.info(f"用户 {username}&{zhuname} 登录成功!")
                    return JsonResponse(
                        {"code": 0, "data": "successful", "username": uname, "zhuname": zh_uname, "email": ldap_email, "level": power, "group": group, "imgurl": imgurl,"token": token}
                    )
                else:
                    if zhuname.strip() == "":
                        return JsonResponse({"code": -1, "is_zhuname": "true", "data": "请填写中文名 作为首次登录使用 !"})
                    else:
                        flag, msg = ldap_regist(ldap_uname, password, ldap_email, zhuname, ldap_group)
                        if flag:
                            uname, zh_uname, group, imgurl, power = ldap_get_user_info(ldap_email)
                            if power == "4":
                                return JsonResponse({"code": -1, "data": "请联系管理员激活账号!"})
                            token = create_token(uname, zh_uname, power)
                            logger.info(f"用户 {username}&{zhuname} 登录成功!")
                            return JsonResponse(
                                {"code": 0, "data": "successful", "username": uname, "zhuname": zh_uname, "email": ldap_email, "level": power, "group": group, "imgurl": imgurl,"token": token}
                            )
                        else:
                            return JsonResponse({"code": -1, "data": msg})
            else:
                return JsonResponse({"code": -1, "data": ldap_msg})
        else:
            logger.info("login with ess database......")
            if len(models.User.objects.filter(username=username)) == True:
                db_pwd = models.User.objects.filter(username=username).values("password")[0]["password"]
                pwd_flag = check_password(password, db_pwd)
                if pwd_flag:
                    power = models.User.objects.get(username=username).power
                    if power == "4":
                        return JsonResponse({"code": -1, "data": "请联系管理员激活账号!"})
                    else:
                        email = models.User.objects.get(username=username).email
                        zhuname = models.User.objects.get(username=username).zh_uname
                        group = models.User.objects.get(username=username).group
                        imgurl = models.User.objects.get(username=username).img
                        token = create_token(username, zhuname, power)
                        logger.info(f"用户 {username}&{zhuname} 登录成功!")
                        return JsonResponse(
                            {"code": 0, "data": "successful", "username": username, "zhuname": zhuname, "email": email, "level": power, "group": group, "imgurl": imgurl,"token": token}
                        )
                else:
                    return JsonResponse({"code": -1, "data": "账号或密码错误!"})
            elif len(models.User.objects.filter(email=username)) == True:
                db_pwd = models.User.objects.filter(email=username).values("password")[0]["password"]
                pwd_flag = check_password(password, db_pwd)
                if pwd_flag:
                    power = models.User.objects.get(username=username).power
                    if power == "4":
                        return JsonResponse({"code": -1, "data": "请联系管理员激活账号!"})
                    else:
                        user = models.User.objects.get(email=username).username
                        zhuname = models.User.objects.get(email=username).zh_uname
                        group = models.User.objects.get(email=username).group
                        imgurl = models.User.objects.get(email=username).img
                        token = create_token(username, zhuname, power)
                        logger.info(f"用户 {username}&{zhuname} 登录成功!")
                        return JsonResponse(
                            {"code": 0, "data": "successful", "username": user,"email": username, "zhuname": zhuname, "power": power, "group": group, "imgurl": imgurl, "token": token}
                        )
                else:
                    return JsonResponse({"code": -1, "data": "账号或密码错误!"})
            else:
                return JsonResponse({"code": -1, "data": "账号或密码错误!"})

@csrf_exempt
def changepwd(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username").strip()
        password = data.get("password").strip()
        user = models.User.objects.get(username=username)
        email = user.email
        user.set_password(password)
        user.save()
        sendEmail(username, password, email)
        return JsonResponse({"code": 0, "data": "successful"})

@csrf_exempt
def changeuserimg(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        imgurl = data["imgurl"].strip()
        user = models.User.objects.get(username=username)
        user.img = imgurl
        user.save()
        return JsonResponse({"code": 0, "data": "successful"})

@csrf_exempt
def get_user_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            username = data["username"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 username !"})
        try:
            info = models.User.objects.get(username=username)
            zh_uname = info.zh_uname
            email = info.email
            if info.group == None:
                group = ""
            else:
                group = info.group
            if info.img == None:
                img = ""
            else:
                img = info.img
            power = info.power
            return JsonResponse({"code": 0, "zh_uname": zh_uname, "email": email, "group": group, "img": img, "power": power})
        except:
            return JsonResponse({{"code": -1, "data": f"{username} 用户不存在 !"}})
# =================================Adamin==================================================
@csrf_exempt
def admin_get_user_info_list(request):
    if request.method == "POST":
        data = json.loads(request.body)
        currentPage = int(data["currentPage"])
        pageSize = int(data["pageSize"])
        email = data["email"]

        if len(email.strip()) != 0 and email != "@gs-robot.com":
            if email.endswith("@gs-robot.com") == False:
                return JsonResponse({"code": -1, "data": "请输入正确的邮箱地址 !"})
            user_list = models.User.objects.filter(email=email)
        else:
            user_list = models.User.objects.all()

        if user_list.count() == 0:
            return JsonResponse({"code": 0, "msg": "查询成功", "count": user_list.count(), "data": []})
        
        pageInator = Paginator(user_list, pageSize)
        try:
            context = pageInator.page(currentPage)
        except EmptyPage:
            context = pageInator.page((user_list.count()//pageSize) + 1)
        user_info_list = [{"username": item.username, "zh_uname": item.zh_uname, "email": item.email, "group": item.group, "img": item.img, "power": item.power} for item in context]
        return JsonResponse({"code": 0, "count": len(user_list), "data": user_info_list})

@csrf_exempt
def admin_get_user_info(request):
    if request.method == "POST":
        username = json.loads(request.body)["username"]
        info = models.User.objects.filter(username=username)
        user_info_list = [{"username": item.username, "zh_uname": item.zh_uname, "email": item.email, "group": item.group, "img": item.img, "power": item.power} for item in info][0]
        return JsonResponse({"code": 0, "data": user_info_list})
    
@csrf_exempt
def admin_update_user_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        auth = data["auth"]
        username = data["username"]
        zh_uname = data["zh_uname"]
        email = data["email"]
        group = data["group"]
        img = data["img"]
        power = data["power"]

        user_source = models.User.objects.filter(username=username)[0]

        if user_source.email != email and models.User.objects.filter(email=email).exists():
            return JsonResponse({"code": -1, "data": "邮箱已存在 !"})
        if user_source.zh_uname != zh_uname and models.User.objects.filter(zh_uname=zh_uname).exists():
            return JsonResponse({"code": -1, "data": "姓名已存在 !"})

        user_table = models.User.objects.get(username=username)
        user_table.username = username
        user_table.zh_uname = zh_uname
        user_table.email = email
        user_table.group = group
        user_table.img = img
        user_table.power = power
        user_table.save()
        logger.info(f"{auth} 修改了 {username} 的信息: {zh_uname} -> {email} -> {group} -> {img} -> {power}")
        return JsonResponse({"code": 0, "data": "修改成功 !"})

@csrf_exempt
def admin_update_user_pwd(request):
    if request.method == "POST":
        data = json.loads(request.body)
        auth = data["auth"]
        username = data["username"].strip()
        password = data["password"].strip()
        user = models.User.objects.get(username=username)
        email = user.email
        user.set_password(password)
        user.save()
        logger.info(f"{auth} 修改了 {username} 的密码 !")
        sendEmail(username, password, email)
        return JsonResponse({"code": 0, "data": "修改成功 !"})


# -------------------------Project----------------------------------------------------
@csrf_exempt
def admin_get_project_info_list(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            currentPage = int(data["currentPage"])
            pageSize = int(data["pageSize"])
            pname = data["pname"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 currentPage or pageSize or pname !"})

        if len(pname.strip()) != 0 or pname != "" or pname != None:
            project_list = models.Project.objects.filter(pname__contains=pname)
        else:
            project_list = models.Project.objects.all()

        if project_list.count() == 0:
            return JsonResponse({"code": -1, "msg": "没有项目名字 !", "count": project_list.count(), "data": []})
        
        pageInator = Paginator(project_list, pageSize)
        try:
            context = pageInator.page(currentPage)
        except EmptyPage:
            context = pageInator.page((project_list.count()//pageSize) + 1)
        user_info_list = [{"id": item.id, "pname": item.pname} for item in context]
        return JsonResponse({"code": 0, "msg": "查询成功 !", "count": project_list.count(), "data": user_info_list})

@csrf_exempt
def admin_add_project(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            pname = data["pname"]
            auth = data["auth"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 pname, auth !"})
        
        try:
            if models.Project.objects.filter(pname=pname).exists():
                return JsonResponse({"code": -1, "data": "项目名字已存在 !"})
            else:
                models.Project.objects.create(pname=pname).save()
                logger.info(f"{auth} 添加了项目名字: {pname}")
                return JsonResponse({"code": 0, "data": "添加成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "添加失败! !"})

@csrf_exempt
def admin_get_project_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            id = data["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 id !"})
        
        pname = models.Project.objects.get(id=id).pname
        return JsonResponse({"code": 0, "data": pname})
    
@csrf_exempt
def admin_update_project_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            auth = data["auth"]
            id = data["id"]
            pname = data["pname"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 auth, id, pname !"})
        sorce_pname = models.Project.objects.get(id=id).pname

        if pname != sorce_pname and models.Project.objects.filter(pname=pname).exists():
            return JsonResponse({"code": -1, "data": "项目名字已存在 !"})
        try:
            models.Project.objects.filter(id=id).update(pname=pname)
            logger.info(f"{auth} 修改了原项目名: {sorce_pname} 为 {pname} !")
            return JsonResponse({"code": 0, "data": "修改成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "修改失败 !"})

@csrf_exempt
def admin_delete_project(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            auth = data["auth"]
            id = data["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 auth, id !"})
        try:
            st = models.SupplierTask.objects.filter(proname=models.Project.objects.get(id=id)).exists()
            gt = models.GSTask.objects.filter(tspname=models.Project.objects.get(id=id)).exists()
            yb = models.YBudget.objects.filter(mpname=models.Project.objects.get(id=id)).exists()
            if st or gt or yb:
                return JsonResponse({"code": -1, "data": "该项目名字下有任务 , 禁止删除 !"})
            source = models.Project.objects.get(id=id)
            pname = source.pname
            source.delete()
            logger.info(f"{auth} 删除了项目 {id} -> {pname} !")
            return JsonResponse({"code": 0, "data": "删除成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "删除失败 !"})

# -------------------------Task kind---------------------------------------------------
@csrf_exempt
def admin_get_task_kind_info_list(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            currentPage = int(data["currentPage"])
            pageSize = int(data["pageSize"])
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 currentPage, pageSize !"})

        task_kind_list = models.TaskKind.objects.all()

        if task_kind_list.count() == 0:
            return JsonResponse({"code": -1, "msg": "任务类型为空 !", "count": task_kind_list.count(), "data": []})
        
        pageInator = Paginator(task_kind_list, pageSize)
        try:
            context = pageInator.page(currentPage)
        except EmptyPage:
            context = pageInator.page((task_kind_list.count()//pageSize) + 1)
        task_kind_info_list = [{"id": item.id, "kinds": item.kinds} for item in context]
        return JsonResponse({"code": 0, "msg": "查询成功 !", "count": task_kind_list.count(), "data": task_kind_info_list})

@csrf_exempt
def admin_add_task_kind(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            kinds = data["kinds"]
            auth = data["auth"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 kinds, auth !"})
        
        try:
            if models.TaskKind.objects.filter(kinds=kinds).exists():
                return JsonResponse({"code": -1, "data": "项目名字已存在 !"})
            else:
                models.TaskKind.objects.create(kinds=kinds).save()
                logger.info(f"{auth} 添加了项目名字: {kinds}")
                return JsonResponse({"code": 0, "data": "添加成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "添加失败! !"})

@csrf_exempt
def admin_get_task_kind_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            id = data["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 id !"})
        
        kinds = models.TaskKind.objects.get(id=id).kinds
        return JsonResponse({"code": 0, "data": kinds})

@csrf_exempt
def admin_update_task_kind_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            auth = data["auth"]
            id = data["id"]
            kinds = data["kinds"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 auth, id, kinds !"})
        source_kinds = models.TaskKind.objects.get(id=id).kinds

        if kinds != source_kinds and models.TaskKind.objects.filter(kinds=kinds).exists():
            return JsonResponse({"code": -1, "data": "任务类型已存在 !"})
        try:
            models.TaskKind.objects.filter(id=id).update(kinds=kinds)
            logger.info(f"{auth} 修改了原任务类型: {source_kinds} 为 {kinds} !")
            return JsonResponse({"code": 0, "data": "修改成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "修改失败 !"})

@csrf_exempt
def admin_delete_task_kind(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            auth = data["auth"]
            id = data["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 auth, id !"})
        try:
            gt = models.GSTask.objects.filter(tskind=models.TaskKind.objects.get(id=id)).exists()
            if gt:
                return JsonResponse({"code": -1, "data": "该任务类型下有任务 , 禁止删除 !"})
            source = models.TaskKind.objects.get(id=id)
            kinds = source.kinds
            source.delete()
            logger.info(f"{auth} 删除了任务类型 {id} -> {kinds} !")
            return JsonResponse({"code": 0, "data": "删除成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "删除失败 !"})

# -------------------------Supplier----------------------------------------------------
@csrf_exempt
def admin_get_supplier_info_list(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            currentPage = int(data["currentPage"])
            pageSize = int(data["pageSize"])
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 currentPage, pageSize !"})

        supplier_list = models.Supplier.objects.all()

        if supplier_list.count() == 0:
            return JsonResponse({"code": -1, "msg": "没有项目名字 !", "count": supplier_list.count(), "data": []})
        
        pageInator = Paginator(supplier_list, pageSize)
        try:
            context = pageInator.page(currentPage)
        except EmptyPage:
            context = pageInator.page((supplier_list.count()//pageSize) + 1)
        user_info_list = [{"id": item.id, "name": item.name} for item in context]
        return JsonResponse({"code": 0, "msg": "查询成功 !", "count": len(supplier_list), "data": user_info_list})

@csrf_exempt
def admin_add_supplier(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            name = data["name"]
            auth = data["auth"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 pname, auth !"})
        
        try:
            if models.Supplier.objects.filter(name=name).exists():
                return JsonResponse({"code": -1, "data": "该供应商已存在 !"})
            else:
                models.Supplier.objects.create(name=name).save()
                logger.info(f"{auth} 添加了供应商名字: {name}")
                return JsonResponse({"code": 0, "data": "添加成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "添加失败! !"})

@csrf_exempt
def admin_get_supplier_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            id = data["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 id !"})
        
        name = models.Supplier.objects.get(id=id).name
        return JsonResponse({"code": 0, "data": name})
    
@csrf_exempt
def admin_update_supplier_info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            auth = data["auth"]
            id = data["id"]
            name = data["name"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 auth, id, name !"})
        sorce_name = models.Supplier.objects.get(id=id).name

        if name != sorce_name and models.Supplier.objects.filter(name=name).exists():
            return JsonResponse({"code": -1, "data": "供应商名字已存在 !"})
        try:
            models.Supplier.objects.filter(id=id).update(name=name)
            logger.info(f"{auth} 修改了原供应商名: {sorce_name} 为 {name} !")
            return JsonResponse({"code": 0, "data": "修改成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "修改失败 !"})

@csrf_exempt
def admin_delete_supplier(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            auth = data["auth"]
            id = data["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "缺少参数 auth, id !"})
        try:
            if models.SupplierTask.objects.filter(wb_name=models.Supplier.objects.get(id=id)).exists() or models.GSTask.objects.filter(tswaibao=models.Supplier.objects.get(id=id)).exists():
                return JsonResponse({"code": -1, "data": "该供应商下有任务 , 禁止删除 !"})
            source = models.Supplier.objects.get(id=id)
            name = source.name
            source.delete()
            logger.info(f"{auth} 删除了供应商 {id} -> {name} !")
            return JsonResponse({"code": 0, "data": "删除成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "删除失败 !"})

# -------------------------Year-Budget----------------------------------------------------

# Year budget get data
@csrf_exempt
def admin_get_ybudget_data(request):
    if request.method == "POST":
        try:
            params = json.loads(request.body)
            year = int(params["year"])
            currentPage = int(params["currentPage"])
            pageSize = int(params["pageSize"])
        except KeyError:
            return JsonResponse({"code": -1, "msg": "参数错误!"})

        data = models.YBudget.objects.filter(year=year)
        if data.count() == 0:
            return JsonResponse({"code": -1, "msg": "暂无数据!", "count": 0, "data": []})
        
        pageInator = Paginator(data, pageSize)
        try:
            context = pageInator.page(currentPage)
        except EmptyPage:
            context = pageInator.page((data.count()//pageSize) + 1)
        data_list = [{"id": item.id, "year": item.year, "mpname": item.pname.pname, "pnamel": item.pnamel} for item in context]
        return JsonResponse({"code": 0, "msg": "查询成功!", "count": data.count(), "data": data_list})

# Year budget add data
@csrf_exempt
def admin_add_ybudget_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            year = int(data["year"])
            mpname = data["mpname"]
            pnamel = data["pnamel"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误 !"})
        
        if models.YBudget.objects.filter(year=year, pname=models.Project.objects.get(pname=mpname)).exists():
            return JsonResponse({"code": -1, "data": "该项目的年度预算已设置了 !"})
        
        if mpname not in pnamel:
            return JsonResponse({"code": -1, "data": "主预算项目名字 必须在 使用项目预算的项目中 填写 !"})
        
        source_pname_list = [item.pname for item in models.Project.objects.all()]
        is_not_exit = False

        for item in pnamel:
            if item not in source_pname_list:
                is_not_exit = True
        if is_not_exit:
                return JsonResponse({"code": -1, "data": f"项目名字: {item} 不存在 !"})

        try:
            models.YBudget.objects.create(year=year, pname=models.Project.objects.get(pname=mpname), pnamel=pnamel)
            logger.info(f"{username} 新增了 {year} 的年度 主项目预算: {mpname}, 使用该项目预算的有: [{pnamel}]")
            return JsonResponse({"code": 0, "data": "添加成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "添加失败 !"})

# Year budget update data
@csrf_exempt
def admin_get_ybudget_data_one(request):
    if request.method == "POST":
        try:
            id = json.loads(request.body)["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误!"})

        data = models.YBudget.objects.get(id=id)

        data_list = {"id": data.id, "year": data.year, "mpname": data.pname.pname, "pnamel": data.pnamel}
        return JsonResponse({"code": 0, "msg": "查询成功!", "data": data_list})

@csrf_exempt
def admin_update_ybudget_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            id = data["id"]
            year = int(data["year"])
            mpname = data["mpname"]
            pnamel = data["pnamel"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误!"})
        
        if mpname not in pnamel:
            return JsonResponse({"code": -1, "data": "主预算项目名字 必须在 使用项目预算的项目中 填写 !"})

        source_pname_list = [item.pname for item in models.Project.objects.all()]
        is_not_exit = False

        for item in pnamel:
            if item not in source_pname_list:
                is_not_exit = True
        if is_not_exit:
                return JsonResponse({"code": -1, "data": f"项目名字: {item} 不存在 !"})

        # 根据ID 进行修改
        ybudget_info = models.YBudget.objects.get(id=id)
        ybudget_info.year = year
        ybudget_info.mpname = models.Project.objects.get(pname=mpname)
        ybudget_info.pnamel = pnamel
        try:
            ybudget_info.save()
            logger.info(f"{username} 修改了 {year} 的年度 主项目预算: {mpname}, 使用该项目预算的有: [{pnamel}]")
            return JsonResponse({"code": 0, "data": "修改成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "修改失败 !"})

@csrf_exempt
def admin_delete_ybudget_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            id = data["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误 !"})
        # 根据ID 进行删除
        try:
            source = models.YBudget.objects.get(id=id)
            year = source.year
            mname = source.pname.pname
            pnamel = source.pnamel
            source.delete()
            logger.info(f"{username} 删除了年度标注预算管理 ID: {id} 年份: {year} 的数据, 主项目: {mname}, 使用该项目预算的有: [{pnamel}] !")
            return JsonResponse({"code": 0, "data": "删除成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "删除失败 !"})

# -------------------------Kafka Snorlax ESS Proname Vender----------------------------------------------------
@csrf_exempt
def admin_get_slesspn(request):
    if request.method == "POST":
        try:
            params = json.loads(request.body)
            currentPage = int(params["currentPage"])
            pageSize = int(params["pageSize"])
        except KeyError:
            return JsonResponse({"code": -1, "msg": "参数错误!"})

        data = models.Slesspn.objects.all()
        if data.count() == 0:
            return JsonResponse({"code": -1, "msg": "暂无数据!", "count": 0, "data": []})
        
        pageInator = Paginator(data, pageSize)
        try:
            context = pageInator.page(currentPage)
        except EmptyPage:
            context = pageInator.page((len(data)//pageSize) + 1)
        data_list = [{"id": item.id, "esspname": item.esspname.pname, "slpname": item.slpname} for item in context]
        return JsonResponse({"code": 0, "msg": "查询成功!", "count": data.count(), "data": data_list})

@csrf_exempt
def admin_add_slesspn(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            slpname = data["slpname"]
            esspname = data["esspname"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误 !"})
        
        if models.Slesspn.objects.filter(slpname=slpname).exists():
            return JsonResponse({"code": -1, "data": "该项目名字对应关系 已配置 !"})
        
        try:
            models.Slesspn.objects.create(slpname=slpname, esspname=models.Project.objects.get(pname=esspname))
            logger.info(f"{username} 新增了 ESS与Snorlax 项目名对应关系: ESS 项目名: {esspname}, Snorlax 对应项目名有: [{slpname}]")
            return JsonResponse({"code": 0, "data": "添加成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "添加失败 !"})

@csrf_exempt
def admin_get_slesspn_one(request):
    if request.method == "POST":
        try:
            id = json.loads(request.body)["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误!"})

        data = models.Slesspn.objects.get(id=id)

        data_list = {"id": data.id, "esspname": data.esspname.pname, "slpname": data.slpname}
        return JsonResponse({"code": 0, "msg": "查询成功!", "data": data_list})

@csrf_exempt
def admin_update_slesspn(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            id = data["id"]
            esspname = data["esspname"]
            slpname = data["slpname"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误!"})

        # 根据ID 进行修改
        slesspn_info = models.Slesspn.objects.get(id=id)
        slesspn_info.esspname = models.Project.objects.get(pname=esspname)
        slesspn_info.slpname = slpname
        try:
            slesspn_info.save()
            logger.info(f"{username} 修改了 ESS与Snorlax 项目名字对应关系: ESS项目名: {esspname}, Snorlax 对应的项目名有: [{slpname}]")
            return JsonResponse({"code": 0, "data": "修改成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "修改失败 !"})

@csrf_exempt
def admin_delete_slesspn(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            id = data["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误 !"})
        # 根据ID 进行删除
        try:
            source = models.Slesspn.objects.get(id=id)
            esspname = source.esspname.pname
            slpname = source.slpname
            source.delete()
            logger.info(f"{username} 删除了工具链项目名对应关系, ID: {id} 的数据, Snorlax 项目名: {slpname}, ESS 对应的项目名: {esspname} !")
            return JsonResponse({"code": 0, "data": "删除成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "删除失败 !"})
# +++++++++++++++++++++++++++++++++++++++Vender+++++++++++++++++++++++++++++++++++++++++++++++++++++
@csrf_exempt
def admin_get_slessvd(request):
    if request.method == "POST":
        try:
            params = json.loads(request.body)
            currentPage = int(params["currentPage"])
            pageSize = int(params["pageSize"])
        except KeyError:
            return JsonResponse({"code": -1, "msg": "参数错误!"})

        data = models.Slessvd.objects.all()
        if data.count() == 0:
            return JsonResponse({"code": -1, "msg": "暂无数据!", "count": 0, "data": []})
        
        pageInator = Paginator(data, pageSize)
        try:
            context = pageInator.page(currentPage)
        except EmptyPage:
            context = pageInator.page((len(data)//pageSize) + 1)
        data_list = [{"id": item.id, "essvender": item.essvender.name, "slvender": item.slvender} for item in context]
        return JsonResponse({"code": 0, "msg": "查询成功!", "count": data.count(), "data": data_list})

@csrf_exempt
def admin_add_slessvd(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            essvender = data["essvender"]
            slvender = data["slvender"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误 !"})
        
        if models.Slessvd.objects.filter(slvender=slvender).exists():
            return JsonResponse({"code": -1, "data": "该项目名字对应关系 已配置 !"})
        
        try:
            models.Slessvd.objects.create(slvender=slvender, essvender=models.Supplier.objects.get(name=essvender))
            logger.info(f"{username} 新增了 ESS与Snorlax 供应商名对应关系:  Snorlax 供应商名: {slvender}, ESS 对应的供应商名: {essvender}")
            return JsonResponse({"code": 0, "data": "添加成功 !"})
        except Exception as e:
            logger.info(e)
            return JsonResponse({"code": -1, "data": "添加失败 !"})

@csrf_exempt
def admin_get_slessvd_one(request):
    if request.method == "POST":
        try:
            id = json.loads(request.body)["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误!"})

        data = models.Slessvd.objects.get(id=id)

        data_list = {"id": data.id, "slvender": data.slvender, "essvender": data.essvender.name}
        return JsonResponse({"code": 0, "msg": "查询成功!", "data": data_list})

@csrf_exempt
def admin_update_slessvd(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            id = data["id"]
            essvender = data["essvender"]
            slvender = data["slvender"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误!"})

        # 根据ID 进行修改
        slessvd_info = models.Slessvd.objects.get(id=id)
        slessvd_info.essvender = models.Supplier.objects.get(name=essvender)
        slessvd_info.slvender = slvender
        try:
            slessvd_info.save()
            logger.info(f"{username} 修改了 ESS与Snorlax 供应商名对应关系: ESS供应商名: {essvender}, Snorlax 对应的供应商名: [{slvender}]")
            return JsonResponse({"code": 0, "data": "修改成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "修改失败 !"})

@csrf_exempt
def admin_delete_slessvd(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            id = data["id"]
        except KeyError:
            return JsonResponse({"code": -1, "data": "参数错误 !"})
        # 根据ID 进行删除
        try:
            source = models.Slessvd.objects.get(id=id)
            essvender = source.essvender.name
            slvender = source.slvender
            source.delete()
            logger.info(f"{username} 删除了工具链供应商名对应关系 ID: {id} 的数据, Snorlax 供应商名: {slvender}, ESS 对应的供应商名: {essvender} !")
            return JsonResponse({"code": 0, "data": "删除成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "删除失败 !"})


# ===============================AnnoTeams=================================================

@csrf_exempt
def get_user_list(request):
    uname_list = json.dumps([i[0] for i in models.User.objects.filter(power__range=[1, 3]).values_list("zh_uname")], ensure_ascii=False)
    return JsonResponse({"code": 0, "data": uname_list})

@csrf_exempt
def get_project_list(request):
    projects = json.dumps([i[0] for i in models.Project.objects.values_list("pname")], ensure_ascii=False)
    return JsonResponse({"code": 0, "data": projects})

@csrf_exempt
def get_supplier_list(request):
    bzf = json.dumps([i[0] for i in models.Supplier.objects.values_list("name")], ensure_ascii=False)
    return JsonResponse({"code": 0, "data": bzf})

@csrf_exempt
def get_supplier_data_jsfs(request):
    data = ["矩形框", "多边形", "线段", "视频", "3D框", "3D分割", "筛选"]
    return JsonResponse({"code": 0, "data": data})

@csrf_exempt
def get_anno_task_kind_list(request):
    tkinds = json.dumps([i[0] for i in models.TaskKind.objects.values_list("kinds")], ensure_ascii=False)
    return JsonResponse({"code": 0, "data": tkinds})


# AnnoTeamSearch
@csrf_exempt
def search_anno_team_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uname = data.get("uname")
        pname = data.get("pname")
        dtime = data.get("begin_time")
        lasttime = data.get("last_time")
        task_id = data.get("taskid")
        taskkind = data.get("taskkind")
        waibao = data.get("supplier")
        pageIndex = int(data.get("pageIndex"))
        pageSize = int(data.get("pageSize"))
        
        data = search(uname, pname, waibao, task_id, taskkind, dtime, lasttime)

        if len(data) == 0:
            return JsonResponse({"code": 0, "msg": "查询成功", "count": len(data), "data": []})
        
        pageInator = Paginator(data, pageSize)
        try:
            context = pageInator.page(pageIndex)
        except EmptyPage:
            context = pageInator.page((len(data)//pageSize) + 1)

        res = get_anno_data_public(context)
        # res.sort(key=lambda x: x["tsdtime"], reverse=True)

        return JsonResponse({"code": 0, "msg": "查询成功", "count": len(data), "data": res})

@csrf_exempt
def get_all_anno_team_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uname = data.get("uname")
        pname = data.get("pname")
        dtime = data.get("begin_time")
        lasttime = data.get("last_time")
        task_id = data.get("taskid")
        taskkind = data.get("taskkind")
        waibao = data.get("supplier")
        
        data = search(uname, pname, waibao, task_id, taskkind, dtime, lasttime)
        if len(data) == 0:
            return JsonResponse({"code": 0, "msg": "查询成功", "sources": []})
        
        res = get_anno_data_public(data)

        return JsonResponse({"code": 0, "msg": "查询成功", "sources": res})


# 添加数据
@csrf_exempt
def add_anno_task_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            auth = data["auth"]
            uname = data["tsuname"].strip()
            pname = data["tspname"].strip()
            waibao = data["tswaibao"].strip()
            task_id = data["tstask_id"].strip()
            dtime = data["tsdtime"].strip()
            kinds = data["tskind"].strip()
            pnums = int(data["tspnums"])
            knums = data["tsknums"].strip()
            ptimes = float(data["tsptimes"].strip())

            status, msg = gs_data_add(uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes)
            if status == "error":
                return JsonResponse({"code": -1, "data": msg})
            else:
                dingtalk(auth,"添加", "", uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes)
                return JsonResponse({"code": 0, "data": "添加成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "请检查填写的内容 !"})


# 修改
@csrf_exempt
def get_anno_task_data_one(request):
    if request.method == "POST":
        id = json.loads(request.body).get("id")
        res = models.GSTask.objects.filter(id=id)
        data = []
        for i in res:
            tmp_dict = {}
            tmp_dict["id"] = i.id
            tmp_dict["tsuname"] = i.tsuname.zh_uname
            tmp_dict["tspname"] = i.tspname.pname
            tmp_dict["tswaibao"] = i.tswaibao.name
            tmp_dict["tstask_id"] = i.tstask_id
            tmp_dict["tsdtime"] = i.tsdtime
            tmp_dict["tskind"] = i.tskind.kinds
            tmp_dict["tspnums"] = i.tspnums
            tmp_dict["tsknums"] = i.tsknums
            tmp_dict["tsptimes"] = i.tsptimes
            data.append(tmp_dict)
        return JsonResponse({"code": 0, "data": data})

@csrf_exempt
def update_anno_task_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        auth = data["auth"]
        id = data["id"]
        uname = data["tsuname"].strip()
        pname = data["tspname"].strip()
        waibao = data["tswaibao"].strip()
        task_id = data["tstask_id"]
        if data["tsdtime"] == None:
            dtime = ""
        else:
            dtime = data["tsdtime"].strip()
        kinds = data["tskind"].strip()
        pnums = int(data["tspnums"])
        if data["tsknums"] == None:
            knums = ""
        else:
            knums = data["tsknums"].strip()
        ptimes = float(data["tsptimes"])
        res = nupdate(id, uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes)

        if res == "error":
            return JsonResponse({"code": -1, "data": '请检查您填写的数据 !'})

        dingtalk(auth,"修改", id, uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes)
        return JsonResponse({"code": 0, "data": "successful"})

@csrf_exempt
def delete_anno_task_data(request):  # 单条数据删除
    if request.method == "POST":
        data = json.loads(request.body)
        auth = data["auth"]
        id = data["id"]
        try:
            models.GSTask.objects.get(id=id).delete()
            dingtalk(auth, "删除", id, "", "", "", "", "", "", "", "", "")
            return JsonResponse({"code": 0, "data": f"成功删除ID为 {id}的数据 !"})
        except:
            return JsonResponse({"code": -1, "data": f"ID: {id} 删除错误 !"})

@csrf_exempt
def get_anno_team_efficiency(request):  # 效率
    if request.method == "POST":
        data = json.loads(request.body)
        nbt = data.get("nbt")
        nlt = data.get("nlt")
        lbt = data.get("lbt")
        llt = data.get("llt")
        try:
            eff_team, user_list, eff_person = eff_test(nbt, nlt, lbt, llt)
            if eff_team:
                return JsonResponse({"code": 0, "eff_team": eff_team, "user_list": user_list, "eff_person": eff_person, "data": "查询成功 !"})
            else:
                return JsonResponse({"code": -1, "data": "该时间段内没有数据喔 !"})
        except:
            return JsonResponse({"code": -1, "data":"查询出错 !"})

# 绩效
@csrf_exempt
def get_anno_team_person(request):
    if request.method == "POST":
        data = json.loads(request.body)
        begin_time = data.get("begin_time")
        last_time = data.get("last_time")
        uname = data.get("uname")
        if begin_time == None and last_time == None:
            return JsonResponse({"code": -1, "msg": "请输入查询时间 !"})
        data = performanceq(begin_time, last_time, uname)
        if len(data) == 0:
            return JsonResponse({"code": -1, "msg": "很遗憾没有查询到数据 !", "data": []})
        else:
            return JsonResponse({"code": 0, "msg": "查询成功 !", "data": data})

# GS数据统计
@csrf_exempt
def get_anno_team_task_count(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = data.get("uname")
        kind = data.get("kind")
        wb_name = data.get("supplier")
        start_time = data.get("begin_time")
        end_time = data.get("last_time")
        pname_list, bar_chart_check_or_anno_list, line_chart_check_or_anno_list = gsdata_count_public_code(user, kind, wb_name, start_time, end_time)
        if len(pname_list) == 0:
            return JsonResponse({"code": -1, "msg": "该时间段内没有数据 !", "kind": kind, "pname_list": [], "bar_chart_check_or_anno_list": [], "line_chart_check_or_anno_list": []})
        return JsonResponse({"code": 0, "pname_list": pname_list, "kind": kind, "bar_chart_check_or_anno_list": bar_chart_check_or_anno_list, "line_chart_check_or_anno_list": line_chart_check_or_anno_list})

# ===============================Suppliers=================================================
# 外包数据添加
@csrf_exempt
def add_supplier_task_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        auth = data["auth"]
        try:
            int(data.get("pnums"))
        except:
            return JsonResponse({"code": -1, "data": "送标样本数量 是 <b>整数<b/>么?"})
        dataone = {
            'user': models.User.objects.get(username=models.User.objects.get(zh_uname=data.get("user")).username),
            'pname': models.Project.objects.get(pname=data.get("pname")),
            "send_data_batch": data.get("send_data_batch"),
            'send_data_time': data.get("send_data_time"),
            'pnums': int(data.get("pnums")),
            'data_source': data.get("data_source"),
            'scene': data.get("scene"),
            'send_reason': data.get("send_reason"),
            'key_frame_extracted_methods': data.get("key_frame_extracted_methods"),
            'ann_field_flag': data.get("ann_field_flag"),
            'vendor': models.Supplier.objects.get(name=data.get("wb_name")),
            'created_time': datetime.now().strftime("%Y-%m-%d")
        }
        try:
            models.SupplierTask.objects.create(**dataone)
            wb_dingtalk(auth, "添加", "", dataone)
            return JsonResponse({"code": 0, "data": "添加成功"})
        except:
            return JsonResponse({"code": -1, "data": "请检查填写的内容"})


@csrf_exempt
def get_supplier_task_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pname = data.get("pname")
        supplier = data.get("supplier")
        send_begin_time = data.get("send_begin_time")
        send_last_time = data.get("send_last_time")
        pay_begin_time = data.get("pay_begin_time")
        pay_last_time = data.get("pay_last_time")
        pageIndex = int(data.get("pageIndex"))
        pageSize = int(data.get("pageSize"))

        data = waibao_search(pname, supplier, send_begin_time, send_last_time, pay_begin_time, pay_last_time)

        if len(data) == 0:
            return JsonResponse({"code": 0, "message": "查询成功", "count": len(data), "data": []})
        
        pageInator = Paginator(data, pageSize)
        try:
            context = pageInator.page(pageIndex)
        except EmptyPage:
            context = pageInator.page((len(data)//pageSize) + 1)
        res = get_supplier_data_public(context)
        return JsonResponse({"code": 0, "message": "查询成功", "count": len(data), "data": res})

@csrf_exempt
def get_all_supplier_task_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pname = data.get("pname")
        supplier = data.get("supplier")
        send_begin_time = data.get("send_begin_time")
        send_last_time = data.get("send_last_time")
        pay_begin_time = data.get("pay_begin_time")
        pay_last_time = data.get("pay_last_time")

        data = waibao_search(pname, supplier, send_begin_time, send_last_time, pay_begin_time, pay_last_time)

        if len(data) == 0:
            return JsonResponse({"code": 0, "message": "查询成功", "count": len(data), "source": []})
        
        res = get_supplier_data_public(data)
        
        return JsonResponse({"code": 0, "message": "查询成功", "source": res})


# 外包数据 单条或批量数据删除
@csrf_exempt
def delete_supplier_task_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get("id")
        uname = data.get("uname")
        try:
            source = models.SupplierTask.objects.get(id=id)
            user = source.user.zh_uname
            proname = source.pname.pname
            send_data_batch = source.send_data_batch
            ann_field_flag = source.ann_field_flag
            send_data_time = source.send_data_time
            pnums = source.pnums
            data_source = source.data_source
            scene = source.scene
            send_reason = source.send_reason
            key_frame_extracted_methods = source.key_frame_extracted_methods
            anno_task_id = source.anno_task_id
            begin_check_data_time = source.begin_check_data_time
            last_check_data_time = source.last_check_data_time
            get_data_time = source.get_data_time
            ann_meta_data = source.ann_meta_data
            wb_name = source.vendor.name
            total_money = source.total_money
            source.delete()
            logger.info(f"{uname} 删除了 ID为 {id} 的供应商数据: [研发]: {user} [项目名字]: {proname} [送标批次]: {send_data_batch} [首次/返修标注]: {ann_field_flag} [送标时间]: {send_data_time} [送标样本数量]: {pnums} [数据来源]: {data_source} [场景分布]: {scene} [送标原因]: {send_reason} [关键帧抽取方式]: {key_frame_extracted_methods} [工具链标注任务ID]: {anno_task_id} [开始验收时间]: {begin_check_data_time} [结束验收时间]: {last_check_data_time} [收到标注结果时间]: {get_data_time} [准确率,框数,结算方式,单价]: {ann_meta_data} [供应商]: {wb_name} [总金钱]: {total_money}")
            wb_dingtalk(uname, "删除", id, '')
            return JsonResponse({"code": 0, "data": "删除成功"})
        except Exception as e:
            return JsonResponse({"code": -1, "data": "删除失败"})

# 外包数据修改
@csrf_exempt
def get_supplier_task_data_one(request):
    if request.method == "POST":
        id = json.loads(request.body)["id"]
        res = models.SupplierTask.objects.filter(id=id)

        data = []
        for i in res:
            tmp_dict = {}
            tmp_dict["id"] = i.id
            tmp_dict['user'] = i.user.zh_uname
            tmp_dict["pname"] = i.pname.pname
            tmp_dict["send_data_batch"] = i.send_data_batch
            tmp_dict['send_data_time'] = i.send_data_time
            tmp_dict["pnums"] = i.pnums
            tmp_dict['data_source'] = i.data_source
            tmp_dict['scene'] = i.scene
            tmp_dict['send_reason'] = i.send_reason
            tmp_dict['key_frame_extracted_methods'] = i.key_frame_extracted_methods
            tmp_dict['begin_check_data_time'] = i.begin_check_data_time
            tmp_dict['last_check_data_time'] = i.last_check_data_time
            tmp_dict["get_data_time"] = i.get_data_time
            tmp_dict["ann_field_flag"] = i.ann_field_flag
            tmp_dict["anno_task_id"] = i.anno_task_id
            if i.ann_meta_data == None:
                tmp_dict['ann_meta_data'] = [{"settlement_method": "", "recovery_precision": "", "knums": "", "unit_price": ""}]
            else:
                tmp_dict['ann_meta_data'] = i.ann_meta_data
            tmp_dict["wb_name"] = i.vendor.name
            tmp_dict['total_money'] = i.total_money
            data.append(tmp_dict)

        return JsonResponse({"code": 0, "data": data[0]})

@csrf_exempt
def update_supplier_task_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        auth = data["auth"]
        id = data["id"]
        data_update = {
            'user': models.User.objects.get(username=models.User.objects.get(zh_uname=data["user"]).username),
            'pname': models.Project.objects.get(pname=data["pname"]),
            'send_data_batch': data["send_data_batch"],
            'send_data_time': data["send_data_time"],
            'pnums': abs(int(data["pnums"])),
            'data_source': data["data_source"],
            'scene': data["scene"],
            'send_reason': data["send_reason"],
            'key_frame_extracted_methods': data["key_frame_extracted_methods"],
            'ann_field_flag': data["ann_field_flag"],
            'vendor': models.Supplier.objects.get(name=data["wb_name"])
        }
        if data["begin_check_data_time"]:
            data_update['begin_check_data_time'] = data["begin_check_data_time"]
        else:
            data_update['begin_check_data_time'] = None
        if data["last_check_data_time"]:
            data_update['last_check_data_time'] = data["last_check_data_time"]
        else:
            data_update['last_check_data_time'] = None
        if data["get_data_time"]:
            data_update['get_data_time'] = data["get_data_time"]
        else:
            data_update['get_data_time'] = None    
        if data["anno_task_id"]:
            data_update['anno_task_id'] = data["anno_task_id"]
        else:
            data_update['anno_task_id'] = None

        new_ann_meta_data = data["ann_meta_data"]
        new_ann_meta_remove_list = []
        is_budget_check = False
        for item in new_ann_meta_data:
            settlement_method = item["settlement_method"]
            recovery_precision = item["recovery_precision"]
            knums = item["knums"]
            unit_price = item["unit_price"]
            if settlement_method == "" and knums == "" and unit_price == "":
                new_ann_meta_remove_list.append(item)
                continue

            if settlement_method == "" or knums == "" or unit_price == "":
                return JsonResponse({"code": -1, "data": "结算方式、标注数量、单价不能为空 !"})
            else:
                if float(knums) < 0:
                    return JsonResponse({"code": -1, "data": "框数不可能能 小于0 !"})
                elif float(unit_price) < 0:
                    return JsonResponse({"code": -1, "data": "单价不可能能 小于0 !"})
                else:
                    if recovery_precision != "":
                        if settlement_method != "视频":
                            try:
                                int(knums)
                            except:
                                return JsonResponse({"code": -1, "data": "当结算方式不是视频时 , 标注数量需为整数 !"})
                        if recovery_precision != None and (float(recovery_precision) < 0 or float(recovery_precision) > 100):
                            return JsonResponse({"code": -1, "data": "准确率率不能 小于0 大于100 !"})
        for item in new_ann_meta_remove_list:
            new_ann_meta_data.remove(item)
        if new_ann_meta_data:
            is_budget_check = True
            data_update["ann_meta_data"] = new_ann_meta_data
            money_count = 0
            for idx in new_ann_meta_data:
                money_count += float(idx["knums"]) * float(idx["unit_price"])
            data_update["total_money"] = round(money_count, 3) # 根据单价位数调整
        else:
            data_update["ann_meta_data"] = None
            data_update["total_money"] = None
        try:
            models.SupplierTask.objects.filter(id=id).update(**data_update)
            wb_dingtalk(auth, "修改", id, data_update)
            if is_budget_check:
                # 触发检查是否满足 1/3,2/3,3/3
                logger.info(f"{data['pname']} {data['send_data_time']}")
                budget_check(data["pname"], data["send_data_time"])
            return JsonResponse({"code": 0, "data": "修改成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "请检查填写的信息 !"})


def wbdata_count_public_code(is_send_time_method, wb_name, start_time, end_time):
    year = datetime.now().strftime('%Y')
    if is_send_time_method == "是":
        if wb_name:
            if start_time and end_time:
                init_data = models.SupplierTask.objects.filter(send_data_time__range=[start_time, end_time], vendor=models.Supplier.objects.get(name=wb_name))
            else:
                init_data = models.SupplierTask.objects.filter(send_data_time__range=[year + '-01-01', year + "-12-31"], vendor=models.Supplier.objects.get(name=wb_name))
        else:
            if start_time and end_time:
                init_data = models.SupplierTask.objects.filter(send_data_time__range=[start_time, end_time])
            else:
                init_data = models.SupplierTask.objects.filter(send_data_time__range=[year + '-01-01', year + "-12-31"])
    else:
        if wb_name:
            if start_time and end_time:
                init_data = models.SupplierTask.objects.filter(get_data_time__range=[start_time, end_time], vendor=models.Supplier.objects.get(name=wb_name))
            else:
                init_data = models.SupplierTask.objects.filter(get_data_time__range=[year + '-01-01', year + "-12-31"], vendor=models.Supplier.objects.get(name=wb_name))
        else:
            if start_time and end_time:
                init_data = models.SupplierTask.objects.filter(get_data_time__range=[start_time, end_time])
            else:
                init_data = models.SupplierTask.objects.filter(get_data_time__range=[year + '-01-01', year + "-12-31"])

    if init_data:
        proname_list = []
        for item in init_data:
            if item.pname.pname not in proname_list:
                proname_list.append(item.pname.pname)

        pie_chart_knums_data = []
        pie_chart_money_data = []
        pie_chart_pnums_data = []
        line_chart_list = []  # [[],[],[]] time,kuang,qian [zhun]
        money_total = 0
        for proidx in proname_list:
            time_list = []
            kuang_list = []
            money_list = []
            pnums_list = []
            for modidx in init_data:
                if modidx.pname.pname == proidx:
                    time_list.append(
                        modidx.send_data_time.strftime('%Y-%m-%d'))
                    if len(pnums_list) == 0:
                        pnums_list.append(modidx.pnums)
                    else:
                        pnums_list.append(pnums_list[-1] + modidx.pnums)
                    if modidx.ann_meta_data:
                        if len(kuang_list) == 0:
                            kuang_list.append(
                                sum([float(idx["knums"]) for idx in modidx.ann_meta_data]))
                        else:
                            kuang_list.append(
                                kuang_list[-1] + sum([float(idx["knums"]) for idx in modidx.ann_meta_data]))
                        if len(money_list) == 0:
                            money_list.append(modidx.total_money)
                        else:
                            money_list.append(
                                round(money_list[-1] + modidx.total_money, 3))
                        money_total += modidx.total_money
            line_chart_list.append(
                [time_list, kuang_list, money_list, pnums_list])

            if len(kuang_list) == 0:
                pie_chart_knums_data.append({"name": proidx, "value": [0]})
            else:
                pie_chart_knums_data.append(
                    {"name": proidx, "value": kuang_list[-1]})
            if len(money_list) == 0:
                pie_chart_money_data.append({"name": proidx, "value": [0]})
            else:
                pie_chart_money_data.append(
                    {"name": proidx, "value": money_list[-1]})
            pie_chart_pnums_data.append(
                {"name": proidx, "value": pnums_list[-1]})
        char_list = [pie_chart_pnums_data,
                     pie_chart_knums_data, pie_chart_money_data]
    else:
        # 为查询到数据先返回空，后面加提示
        money_total = 0
        proname_list = []
        char_list = [[{}], [{}], [{}]]
        line_chart_list = [[[0], [0], [0]]]

    return proname_list, char_list, format(round(money_total, 3), ','), line_chart_list

# 外包数据统计 -- 图表
@csrf_exempt
def get_supplier_task_count(request):
    if request.method == "POST":
        data = json.loads(request.body)
        is_send_time_method = data.get("select_time_method")
        wb_name = data.get("supplier_name")
        start_time = data.get("start_time")
        end_time = data.get("last_time")
        proname_list, char_list, money_total, line_chart_list = wbdata_count_public_code(is_send_time_method, wb_name, start_time, end_time)

        if len(proname_list) == 0:
            return JsonResponse({"code": -1, "msg": "该时间段内没有数据 !", "proname": proname_list, "chart_pie": char_list, "chart_line": line_chart_list, "money_total": money_total})

        return JsonResponse({"code": 0, "proname": proname_list, "chart_pie": char_list, "chart_line": line_chart_list, "money_total": money_total})

# 外包数据统计 -- 表格
def budget_check(pname, time):
    def check_task():
        param_year = int(time.split("-")[0])
        ybudget_list = models.YBudget.objects.filter(year=param_year)

        is_single_project = False
        used_money = 0
        today = datetime.now().strftime('%Y-%m-%d')
        user_list = ["lihua"]
    
        for item in ybudget_list:
            if pname in item.pnamel:
                is_single_project = False
                budget_data = models.Budget.objects.filter(year_budget=param_year, pname=models.Project.objects.get(pname=item.pname))
                ann_budget = [bd.ann_budget for bd in budget_data]
                for pn in item.pnamel:
                    tmp = models.SupplierTask.objects.filter(pname=models.Project.objects.get(pname=pn),send_data_time__range=[f"{param_year}-01-01", f"{param_year}-12-31"])
                    for tmp_item in tmp:
                        if tmp_item.total_money != None:
                            used_money += tmp_item.total_money
                            if tmp_item.user.username not in user_list:
                                user_list.append(tmp_item.user.username)
                used_money = round(used_money, 3)
                if ann_budget:
                    used_ratio = float((format(used_money/ann_budget[0] * 100, '.5f')))
                    budget_data.update(used_money=used_money,used_ratio=used_ratio, updated_time=today)
                    
                    if used_ratio < float(format(1 / 3 * 100, '5f')) and used_ratio < float(format(2 / 3 * 100, '5f')) and used_ratio < float(format(3 / 3 * 100, '5f')): # < 1/3
                        budget_data.update(reaching_one_third_budget_time=None, reaching_two_third_budget_time=None, reaching_third_third_budget_time=None, updated_time=today)
                    if used_ratio >= float(format(1 / 3 * 100, '5f')) and used_ratio < float(format(2 / 3 * 100, '5f')): # >= 1/3 and < 2/3
                        one_third_time = budget_data[0].reaching_one_third_budget_time
                        if one_third_time == None:
                            budget_data.update(reaching_one_third_budget_time=today, reaching_two_third_budget_time=None, reaching_third_third_budget_time=None, updated_time=today)
                        budget_data.update(reaching_two_third_budget_time=None, reaching_third_third_budget_time=None)
                        budget_reaching_talk(pname, user_list, f"{param_year}-1/3", "ding") # 通知
                    if used_ratio >= float(format(2 / 3 * 100, '5f')) and used_ratio < float(format(3 / 3 * 100, '5f')): # >= 2/3 and < 3/3
                        one_third_time = budget_data[0].reaching_one_third_budget_time
                        two_third_time = budget_data[0].reaching_two_third_budget_time
                        if one_third_time == None:
                            budget_data.update(reaching_one_third_budget_time=today, updated_time=today)
                        if two_third_time == None:
                            budget_data.update(reaching_two_third_budget_time=today, updated_time=today)
                        budget_data.update(reaching_third_third_budget_time=None)
                        budget_reaching_talk(pname, user_list, f"{param_year}-2/3", "ding") # 通知
                    if used_ratio >= float(format(3 / 3 * 100, '5f')): # >= 3/3
                        one_third_time = budget_data[0].reaching_one_third_budget_time
                        two_third_time = budget_data[0].reaching_two_third_budget_time
                        thidr_third_time = budget_data[0].reaching_third_third_budget_time
                        if one_third_time == None:
                            budget_data.update(reaching_one_third_budget_time=today, updated_time=today)
                        if two_third_time == None:
                            budget_data.update(reaching_two_third_budget_time=today, updated_time=today)
                        if thidr_third_time == None:
                            budget_data.update(reaching_third_third_budget_time=today, updated_time=today)
                        budget_reaching_talk(pname, user_list, f"{param_year}-100%", "ding") # 通知
                else:
                    logger.warning(f"请联系管理员添加 {param_year}年 [{item.pname}] 项目的预算!")
                    budget_reaching_talk(item.pname, "", param_year, "add") # 通知
                break
            else:
                is_single_project = True
                continue
        if ybudget_list.count() == 0 or is_single_project:
            budget_data = models.Budget.objects.filter(year_budget=param_year, pname=models.Project.objects.get(pname=pname))
            ann_budget = [item.ann_budget for item in budget_data]
            tmp = models.SupplierTask.objects.filter(pname=models.Project.objects.get(pname=pname),send_data_time__range=[f"{param_year}-01-01", f"{param_year}-12-31"])
            for tmp_item in tmp:
                if tmp_item.total_money != None:
                    used_money += tmp_item.total_money
                    if tmp_item.user.username not in user_list:
                            user_list.append(tmp_item.user.username)
            used_money = round(used_money, 3)
            if ann_budget:
                used_ratio = float((format(used_money/ann_budget[0] * 100, '.5f')))
                budget_data.update(used_money=used_money,used_ratio=used_ratio, updated_time=today)

                if used_ratio < float(format(1 / 3 * 100, '5f')) and used_ratio < float(format(2 / 3 * 100, '5f')) and used_ratio < float(format(3 / 3 * 100, '5f')): # < 1/3
                    budget_data.update(reaching_one_third_budget_time=None, reaching_two_third_budget_time=None, reaching_third_third_budget_time=None, updated_time=today)
                if used_ratio >= float(format(1 / 3 * 100, '5f')) and used_ratio < float(format(2 / 3 * 100, '5f')): # >= 1/3 and < 2/3
                    one_third_time = budget_data[0].reaching_one_third_budget_time
                    if one_third_time == None:
                        budget_data.update(reaching_one_third_budget_time=today, reaching_two_third_budget_time=None, reaching_third_third_budget_time=None, updated_time=today)
                    budget_data.update(reaching_two_third_budget_time=None, reaching_third_third_budget_time=None)
                    budget_reaching_talk(pname, user_list, f"{param_year}-1/3", "ding") # 通知
                if used_ratio >= float(format(2 / 3 * 100, '5f')) and used_ratio < float(format(3 / 3 * 100, '5f')): # >= 2/3 and < 3/3
                    one_third_time = budget_data[0].reaching_one_third_budget_time
                    two_third_time = budget_data[0].reaching_two_third_budget_time
                    if one_third_time == None:
                        budget_data.update(reaching_one_third_budget_time=today, updated_time=today)
                    if two_third_time == None:
                        budget_data.update(reaching_two_third_budget_time=today, updated_time=today)
                    budget_data.update(reaching_third_third_budget_time=None)
                    budget_reaching_talk(pname, user_list, f"{param_year}-2/3", "ding") # 通知
                if used_ratio >= float(format(3 / 3 * 100, '5f')): # >= 3/3
                    one_third_time = budget_data[0].reaching_one_third_budget_time
                    two_third_time = budget_data[0].reaching_two_third_budget_time
                    thidr_third_time = budget_data[0].reaching_third_third_budget_time
                    if one_third_time == None:
                        budget_data.update(reaching_one_third_budget_time=today, updated_time=today)
                    if two_third_time == None:
                        budget_data.update(reaching_two_third_budget_time=today, updated_time=today)
                    if thidr_third_time == None:
                        budget_data.update(reaching_third_third_budget_time=today, updated_time=today)
                    budget_reaching_talk(pname, user_list, f"{param_year}-100%", "ding") # 通知
            else:
                logger.warning(f"请联系管理员添加 {param_year}年 [{pname}] 项目的预算!")
                budget_reaching_talk(pname, "", param_year, "add")
    
    task = threading.Thread(target=check_task)
    task.start()

# budget add
@csrf_exempt
def add_budget_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data["username"]
        year_budget=int(data["year"])
        pname=data["proname"]
        ann_budget=float(data["money"])
        try:
            pro_bugdet_is_exit = models.Budget.objects.filter(year_budget=year_budget, pname=models.Project.objects.get(pname=pname)).exists()
            if not pro_bugdet_is_exit:
                models.Budget.objects.create(year_budget=year_budget, pname=models.Project.objects.get(pname=pname), ann_budget=ann_budget)
                budget_talk(name, "添加", "", {"year":year_budget, "pname": pname, "ann_budget": ann_budget})
                return JsonResponse({"code": 0, "data": "添加成功 !"})
            else:
                return JsonResponse({"code": -1, "data": "已经添加过了 !"})
        except:
            return JsonResponse({"code": -1, "data": "添加失败 !"})

# bugdet show
@csrf_exempt
def get_budget_all_data(request):
    if request.method == "POST":
        data = json.loads(request.body)

        year = int(data["year"])
        currentPage = int(data["currentPage"])
        pageSize = int(data["pageSize"])

        budget_data = models.Budget.objects.filter(year_budget=year).order_by("-used_ratio")

        if len(budget_data) == 0:
            return JsonResponse({"code": -1, "msg": "该年份没有标注预算喔 !", "count": 0, "data": []})
        
        pageInator = Paginator(budget_data, pageSize)
        try:
            context = pageInator.page(currentPage)
        except EmptyPage:
            context = pageInator.page((len(data)//pageSize) + 1)

        data_list = [
        {
            "id": item.id,
            "pname": item.pname.pname,
            "ann_budget": item.ann_budget,
            "used_money": item.used_money,
            "used_ratio": item.used_ratio,
            "reaching_one_third_budget_time": item.reaching_one_third_budget_time,
            "one_third_report_time": item.one_third_report_time,
            "one_third_report_file": item.one_third_report_file,
            "reaching_two_third_budget_time": item.reaching_two_third_budget_time,
            "two_third_report_time": item.two_third_report_time,
            "two_third_report_file": item.two_third_report_file,
            "reaching_third_third_budget_time": item.reaching_third_third_budget_time,
            "third_third_report_time": item.third_third_report_time,
            "third_third_report_file": item.third_third_report_file,
         } 
        for item in context
        ]

        return JsonResponse({"code": 0, "msg": "查询成功", "count": len(budget_data), "data": data_list})

# bugdet update
@csrf_exempt
def get_budget_one_data(request):
    if request.method == "POST":
        id = json.loads(request.body)["id"]

        budget_id_data = models.Budget.objects.filter(id=id)

        data = [
            {
                "id": item.id,
                "proname": item.pname.pname,
                "ann_budget": item.ann_budget,
                "used_money": item.used_money,
                "used_ratio": item.used_ratio,
                "reaching_one_third_budget_time": item.reaching_one_third_budget_time,
                "one_third_report_time": item.one_third_report_time,
                "one_third_report_file": item.one_third_report_file,
                "reaching_two_third_budget_time": item.reaching_two_third_budget_time,
                "two_third_report_time": item.two_third_report_time,
                "two_third_report_file": item.two_third_report_file,
                "reaching_third_third_budget_time": item.reaching_third_third_budget_time,
                "third_third_report_time": item.third_third_report_time,
                "third_third_report_file": item.third_third_report_file,
            } 
            for item in budget_id_data
            ]

        return JsonResponse({"code": 0, "data": data[0]})

@csrf_exempt
def update_budget_data(request):
    if request.method == "POST":
        data = json.loads(request.body)

        name = data["username"]

        id = data["id"]
        proname = data["proname"]
        # 咦存在50-地面物体 ，修改地面物体； 不存在地面物体，修改地面物体
        temp_budget = models.Budget.objects.filter(id=id)[0]
        temp_budget_year = temp_budget.year_budget
        temp_budget_proname = temp_budget.pname.pname

        tmp_pname_list = [item[0] for item in models.Budget.objects.filter(year_budget=temp_budget_year).values_list("pname")]
        
        if temp_budget_proname != proname and proname in tmp_pname_list:
            return JsonResponse({"code": -1, "data": "该项目的标注预算已存在 !"})
        
        ann_budget = float(data["ann_budget"])
        one_third_report_time = data["one_third_report_time"]
        one_third_report_file = data["one_third_report_file"]
        two_third_report_time = data["two_third_report_time"]
        two_third_report_file = data["two_third_report_file"]
        third_third_report_time = data["third_third_report_time"]
        third_third_report_file = data["third_third_report_file"]

        req_dic = {}

        req_dic["pname"] = models.Project.objects.get(pname=proname)
        req_dic["ann_budget"] = ann_budget

        if one_third_report_time:
            req_dic["one_third_report_time"] = one_third_report_time
        else:
            req_dic["one_third_report_time"] = None
        if one_third_report_file:
            req_dic["one_third_report_file"] = one_third_report_file
        else:
            req_dic["one_third_report_file"] = None
        if two_third_report_time:
            req_dic["two_third_report_time"] = two_third_report_time
        else:
            req_dic["two_third_report_time"] = None
        if two_third_report_file:
            req_dic["two_third_report_file"] = two_third_report_file
        else:
            req_dic["two_third_report_file"] = None
        if third_third_report_time:
            req_dic["third_third_report_time"] = third_third_report_time
        else:
            req_dic["third_third_report_time"] = None
        if third_third_report_file:
            req_dic["third_third_report_file"] = third_third_report_file
        else:
            req_dic["third_third_report_file"] = None
        try:
            models.Budget.objects.filter(id=id).update(**req_dic)
            budget_talk(name, "修改", id, models.Budget.objects.get(id=id))
            return JsonResponse({"code": 0, "data": "修改成功 !"})
        except:
            return JsonResponse({"code": -1, "data": "修改失败 !"})

# bugdet delete
@csrf_exempt
def delete_budget_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data["username"]
        id = data["id"]

        try:
            models.Budget.objects.get(id=id).delete()
            budget_talk(name, "删除", data.get("id"), "")
            return JsonResponse({"code": 0, "data": "删除成功 !"})
        except:
             return JsonResponse({"code": -1, "data": "删除失败 !"})

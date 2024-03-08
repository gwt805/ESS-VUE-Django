from datetime import datetime
from time import strftime, gmtime
from server.settings import CONFIG, BASE_DIR
from loguru import logger
from service import models
import datetime as dt
import threading
import requests
import math
import json

''' 效率计算 开始 '''
def str2sec(x):
    """
  字符串时分秒转换成秒
  """
    h, m, s = x.strip().split(":")  # .split()函数将其通过':'分隔开,.strip()函数用来除去空格
    return int(h) * 3600 + int(m) * 60 + int(s)  # int()函数转换成整数运算

def eff_person_public(tdat, names, begin_time, end_time):
    ggg = []  # 二维矩阵
    for g in names:
        tps = []  # 没人一组整体效率
        k_p = []  # [(kinds1, pname1), (kinds2, pname2)]
        for kk in models.GSTask.objects.filter(tsdtime__range=[begin_time, end_time], tsuname=models.User.objects.get(username=models.User.objects.get(username=models.User.objects.get(zh_uname=g).username))):
            if (kk.tskind.kinds, kk.tspname.pname) not in k_p:
                k_p.append((kk.tskind.kinds, kk.tspname.pname))
        for i in k_p:
            pnum = 0
            knum = 0
            ptm = 0.0
            pp = []
            gg = tdat.filter(tskind=models.TaskKind.objects.get(kinds=i[0]), tspname=models.Project.objects.get(pname=i[1]), tsuname=models.User.objects.get(username=models.User.objects.get(zh_uname=g).username))
            pp.append(i[0])
            pp.append(i[1])
            if i[0] == "审核" or i[0] == "筛选":
                for j in gg:
                    pnum += j.tspnums
                    ptm += j.tsptimes
                pp.append(pnum)
                pp.append(math.floor(pnum / ptm))
            elif (
                i[0] == "2D分割标注"
                or i[0] == "2.5D点云标注"
                or i[0] == "属性标注"
                or i[0] == "2D框标注"
            ):
                for j in gg:
                    pnum += j.tspnums
                    knum += int(j.tsknums)
                    ptm += j.tsptimes
                pp.append(pnum)
                pp.append(knum)
                pp.append(math.floor(knum / ptm))
            elif i[0] == "视频标注":
                for j in gg:
                    pnum += j.tspnums
                    knum += str2sec(j.tsknums)
                    ptm += j.tsptimes
                pp.append(pnum)
                pp.append(strftime("%H时%M分%S秒", gmtime(knum)))
                pp.append(strftime("%H时%M分%S秒", gmtime(knum // ptm)))
            tps.append(pp)
        ggg.append({g: tps})
    return ggg

def data_person_compare(l_eff_res, name, nvlue):
    tmp_list = nvlue
    for item in l_eff_res:
        for k,v in item.items():
            if k == name:
                for litem in v:
                    for nitem in nvlue:
                        if litem[:2] == nitem[:2]:
                            idx = tmp_list.index(nitem)
                            tmp_list[idx].append(litem[-1])
    eff_person_list = []
    for item in tmp_list:
        tmp_dict = {}
        tmp_dict['name'] = name
        tmp_dict['kinds'] = item[0]
        tmp_dict['pname'] = item[1]
        tmp_dict['pnums'] = item[2]
        if item[0] in ["审核", "筛选"]:
            if len(item) == 4:
                tmp_dict['knums'] = None
                tmp_dict['neff'] = item[3]
                tmp_dict['leff'] = None
            else:
                tmp_dict['knums'] = None
                tmp_dict['neff'] = item[3]
                tmp_dict['leff'] = item[4]
        else:
            if len(item) == 5:
                tmp_dict['knums'] = item[3]
                tmp_dict['neff'] = item[4]
                tmp_dict['leff'] = None
            else:
                tmp_dict['knums'] = item[3]
                tmp_dict['neff'] = item[4]
                tmp_dict['leff'] = item[5]
        eff_person_list.append(tmp_dict)
    return eff_person_list

def data_team_compare(ndata, ldata):
    new_eff_list = ndata
    for litem in ldata:
        for nitem in ndata:
            if nitem[:2] == litem[:2]:
                idx = new_eff_list.index(nitem)
                new_eff_list[idx].append(litem[-1])

    eff_list_to_json = []
    for item in new_eff_list:
        tmp_dict = {}
        tmp_dict['kinds'] = item[0]
        tmp_dict['pname'] = item[1]
        tmp_dict['pnums'] = item[2]
        if item[0] in ['审核', '筛选']:
            if len(item) == 4:
                tmp_dict['knums'] = None
                tmp_dict['neff'] = item[3]
                tmp_dict['leff'] = None
            else:
                tmp_dict['knums'] = None
                tmp_dict['neff'] = item[3]
                tmp_dict['leff'] = item[4]
        else:
            if len(item) == 5:
                tmp_dict['knums'] = item[3]
                tmp_dict['neff'] = item[4]
                tmp_dict['leff'] = None
            else:
                tmp_dict['knums'] = item[3]
                tmp_dict['neff'] = item[4]
                tmp_dict['leff'] = item[5]
        eff_list_to_json.append(tmp_dict)
    return eff_list_to_json

def eff_teams(begin_time, over_time):
    tdat = models.GSTask.objects.filter(tsdtime__range=[begin_time, over_time])
    k_p = []  # [(kinds1, pname1), (kinds2, pname2)]
    for i in tdat:
        if (i.tskind.kinds, i.tspname.pname) not in k_p:
            k_p.append((i.tskind.kinds, i.tspname.pname))
    tps = []  # 团队整体效率
    for i in k_p:
        pnum = 0
        knum = 0
        ptm = 0.0
        pp = []
        gg = tdat.filter(tskind=models.TaskKind.objects.get(kinds=i[0]), tspname=models.Project.objects.get(pname=i[1]))
        # public code
        pp.append(i[0])
        pp.append(i[1])
        if i[0] == "审核" or i[0] == "筛选":
            for j in gg:
                pnum += j.tspnums
                ptm += j.tsptimes
            pp.append(pnum)
            pp.append(math.floor(pnum / ptm))
        elif (
            i[0] == "2D分割标注" or i[0] == "2.5D点云标注" or i[0] == "属性标注" or i[0] == "2D框标注"
        ):
            for j in gg:
                pnum += j.tspnums
                knum += int(j.tsknums)
                ptm += j.tsptimes
            pp.append(pnum)
            pp.append(knum)
            pp.append(math.floor(knum / ptm))
        elif i[0] == "视频标注":
            for j in gg:
                pnum += j.tspnums
                knum += str2sec(j.tsknums)
                ptm += j.tsptimes
            pp.append(pnum)
            pp.append(strftime("%H时%M分%S秒", gmtime(knum)))
            pp.append(strftime("%H时%M分%S秒", gmtime(knum // ptm)))
        tps.append(pp)
    return tps

def eff_test(nbt, nlt, lbt, llt):
    tdat_n = models.GSTask.objects.filter(tsdtime__range=[nbt, nlt])
    names_n = list(set([i.tsuname.zh_uname for i in tdat_n]))  # [name1,name2,name3]

    tdat_l = models.GSTask.objects.filter(tsdtime__range=[lbt, llt])
    names_l = list(set([i.tsuname.zh_uname for i in tdat_l]))  # [name1,name2,name3]

    n_eff_res = eff_person_public(tdat_n, names_n, nbt, nlt)
    l_eff_res = eff_person_public(tdat_l, names_l, lbt, llt)
    
    n_team_eff_res = eff_teams(nbt, nlt)
    l_team_eff_res = eff_teams(lbt, llt)
    
    eff_team = data_team_compare(n_team_eff_res, l_team_eff_res)
    eff_person = [] # 每个人效率
    user_list = []
    for item in n_eff_res:
        for k,v in item.items():
            res = data_person_compare(l_eff_res, k, v)
            user_list.append(k)
            eff_person.append(res)
    return eff_team, user_list, eff_person
''' 效率计算 结束 '''

# 绩效
def performanceq(begin_time, over_time, name):
    tdat = models.GSTask.objects.filter(
        tsdtime__range=[begin_time, over_time], tsuname=models.User.objects.get(zh_uname=name))
    k_p = (
        []
    )  # [('审核', 'S线数据'), ('其他', None), ('标注', '杂物'), ('标注', 'S线数据'), ('审核', '脏污'), ('审核', '杂物')]
    for i in tdat:
        if (i.tskind.kinds, i.tspname.pname) not in k_p:
            k_p.append((i.tskind.kinds, i.tspname.pname))
    tps = []
    for i in k_p:
        pnum = 0
        knum = 0
        ptm = 0.0
        pp = {}
        gg = tdat.filter(tskind=models.TaskKind.objects.get(kinds=i[0]), tspname=models.Project.objects.get(pname=i[1]))
        # public code
        pp['tskind'] = i[0]
        pp['tspname'] = i[1]
        if i[0] == "审核" or i[0] == "筛选":
            for j in gg:
                pnum += j.tspnums
                ptm += j.tsptimes
            pp['tspnum'] = pnum
        elif (
            i[0] == "2D框标注" or i[0] == "2.5D点云标注" or i[0] == "属性标注" or i[0] == "2D分割标注"
        ):
            for j in gg:
                pnum += j.tspnums
                knum += int(j.tsknums)
                ptm += j.tsptimes
            pp['tspnum'] = pnum
            pp['tsknum'] = knum
        elif i[0] == "视频标注":
            for j in gg:
                pnum += j.tspnums
                knum += str2sec(j.tsknums)
                ptm += j.tsptimes
            pp['tspnum'] = pnum
            pp['tsknum'] = strftime("%H时%M分%S秒", gmtime(knum))
        tps.append(pp)
    return tps


# GS 数据添加
def gs_data_add(uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes):
    import re
    new_task = models.GSTask()
    new_task.tsuname = models.User.objects.get(username=models.User.objects.get(zh_uname=uname))
    new_task.tspname = models.Project.objects.get(pname=pname)
    new_task.tswaibao = models.Supplier.objects.get(name=waibao)
    new_task.tsdtime = dtime
    new_task.tskind = models.TaskKind.objects.get(kinds=kinds)
    new_task.tspnums = pnums
    new_task.tsptimes = ptimes
    status, msg = "", ""
    if kinds == "2D分割标注" or kinds == "2.5D点云标注" or kinds == "属性标注" or kinds == "2D框标注":
        if task_id == "":
            status = "error"
            msg = "任务ID不能为空 !"
            return status, msg
        if knums == "":
            status = "error"
            msg = "标注数量不能为空 !"
            return status, msg
        new_task.tstask_id = int(task_id)
        try:
            new_task.tsknums = int(knums)
        except:
            status = "error"
            msg = "标注数量格式错误 !"
            return status, msg
    elif kinds == "视频标注":
        if knums == "":
            status = "error"
            msg = "标注数量不能为空 !"
            return status, msg
        knums_re = re.findall("[0-9]{2,}[:][0-9]{2,2}[:][0-9]{2,2}", knums)
        if len(knums_re) != 0:
            if len(knums_re[0]) != len(knums):
                status = "error"
                msg = "时间格式错误(不允许有空格) !"
                return status, msg
        else:
            status = "error"
            msg = "时间格式错误(不允许有空格) !"
            return status, msg
        new_task.tsknums = knums
    elif kinds == "审核":
        if task_id == "":
            status = "error"
            msg = "任务ID不能为空 !"
            return status, msg
        new_task.tstask_id = int(task_id)
    new_task.save()
    status = "success"
    msg = "添加成功 !"
    return status, msg

# search
def search(uname, pname, waibao, task_id, kinds, dtime, lasttime):
    filterQuery = {}
    if uname:
        filterQuery["tsuname"] = models.User.objects.get(username=models.User.objects.get(zh_uname=uname).username)
    if pname:
        filterQuery["tspname"] = models.Project.objects.get(pname=pname)
    if waibao:
        filterQuery["tswaibao"] = models.Supplier.objects.get(name=waibao)
    if task_id:
        filterQuery["id"] = int(task_id)
    if kinds:
        filterQuery["tskind"] = models.TaskKind.objects.get(kinds=kinds)
    if lasttime and dtime:
        filterQuery["tsdtime__range"] = [dtime, lasttime]
    else:
        filterQuery["tsdtime__range"] = [f"{datetime.now().year}-01-01", f"{datetime.now().year}-12-31"]

    tdat = models.GSTask.objects.filter(**filterQuery).order_by("-tsdtime")
    return tdat

def get_anno_data_public(data):
    res = []
    for i in data:
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
        res.append(tmp_dict)
    return res


# nupdate
def nupdate(id, uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes):
    import re
    now_data = models.GSTask.objects.get(id=id)
    now_data.tsuname = models.User.objects.get(username=models.User.objects.get(username=models.User.objects.get(zh_uname=uname).username))
    now_data.tspname = models.Project.objects.get(pname=pname)
    now_data.tswaibao = models.Supplier.objects.get(name=waibao)
    now_data.tsdtime = dtime
    now_data.tspnums = pnums
    now_data.tskind = models.TaskKind.objects.get(kinds=kinds)
    now_data.tsptimes = ptimes

    try:
        if kinds == "2D分割标注" or kinds == "2.5D点云标注" or kinds == "属性标注" or kinds == "2D框标注":
            now_data.tstask_id = int(task_id)
            now_data.tsknums = int(knums)
        elif kinds == "视频标注":
            knums_re = re.findall("[0-9]{2,}[:][0-9]{2,2}[:][0-9]{2,2}", knums)
            if len(knums_re) != 0:
                if len(knums_re[0]) != len(knums):
                    return "error"
                else:
                    now_data.tsknums = knums
            else:
                return "error"
            if task_id == "" or task_id == None:
                now_data.tstask_id = None
            else:
                now_data.tstask_id = int(task_id)
        elif kinds == "审核":
            now_data.tstask_id = int(task_id)
            now_data.tsknums = None
        elif kinds == "筛选":
            if task_id == "" or task_id == None:
                now_data.tstask_id = None
            else:
                now_data.tstask_id = int(task_id)
            now_data.tsknums = None
        now_data.save()
        return "successful"
    except:
        return "error"

# waibao_search
def waibao_search(pname, supplier, send_begin_time, send_last_time, pay_begin_time, pay_last_time):
    filterQuery = {}
    if pname:
        filterQuery["pname"] = models.Project.objects.get(pname=pname)
    if supplier:
        filterQuery["vendor"] = models.Supplier.objects.get(name=supplier)
    # 送标时间
    if send_begin_time and send_last_time:
        filterQuery["send_data_time__range"] = [send_begin_time, send_last_time]
    else:
        filterQuery["send_data_time__range"] = [f"{datetime.now().year}-01-01", f"{datetime.now().year}-12-31"]
    # 收到结果时间
    if pay_begin_time and pay_last_time:
        filterQuery["get_data_time__range"] = [pay_begin_time, pay_last_time]
    tdat = models.SupplierTask.objects.filter(**filterQuery).order_by("-send_data_time")
    return tdat

def get_supplier_data_public(data):
    res = []
    for i in data:
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
            tmp_dict['ann_meta_data'] = ""
        else:
            tmp_dict['ann_meta_data'] = json.dumps(i.ann_meta_data, ensure_ascii=False)

        tmp_dict["wb_name"] = i.vendor.name
        tmp_dict['total_money'] = i.total_money
        res.append(tmp_dict)
    return res


# GS 数据统计
def gsdata_count_public_code(zh_uname, kind,wb_name, start_time, end_time):
    query_filter = {}
    if zh_uname != "":
        query_filter["tsuname"] = models.User.objects.get(username=models.User.objects.get(zh_uname=zh_uname))
    if wb_name != "":
        query_filter["tswaibao"] = models.Supplier.objects.get(name=wb_name)
    if start_time and end_time:
        query_filter["tsdtime__range"] = [start_time, end_time]
    
    if zh_uname == "" and wb_name == "" and start_time == "" and end_time == "":
        init_data = models.GSTask.objects.all()
    else:
        init_data = models.GSTask.objects.filter(**query_filter)
    if init_data:
        if kind == "审核":
            # 审核-项目名字列表
            check_data_pname_list = list(set([i.tspname.pname for i in init_data.filter(tskind=models.TaskKind.objects.get(kinds="审核"))]))
            # 柱状图-审核-pname&pnums
            bar_chart_check_list = [check_data_pname_list] # [[],[]] pname, tu
            # 折线图-审核-日期&图数
            line_chart_check_list = [] # [[],[]] time, tu
            # 折线图-审核-日期&图数&框数
            check_data_pnums_bar_list = []
            for pidx in check_data_pname_list:
                tmp_time_list = []
                tmp_pnums_list = []
                for idx in init_data.filter(tspname=models.Project.objects.get(pname=pidx)):
                    if idx.tskind.kinds == "审核":
                        tmp_time_list.append(idx.tsdtime.strftime("%Y-%m-%d"))
                        if tmp_pnums_list == []:
                            tmp_pnums_list.append(idx.tspnums)
                        else:
                            tmp_pnums_list.append(idx.tspnums + tmp_pnums_list[-1])
                if tmp_time_list and tmp_pnums_list:
                    line_chart_check_list.append([tmp_time_list, tmp_pnums_list])
                    check_data_pnums_bar_list.append(tmp_pnums_list[-1])
            bar_chart_check_list.append(check_data_pnums_bar_list)
            return check_data_pname_list, bar_chart_check_list, line_chart_check_list
        else:
            # 非审核-项目名字列表
            anno_data_pname_list = list(set([i.tspname.pname for i in init_data if i.tskind.kinds != "审核"]))
            # 柱状图-标注-日期&图数&框数
            bar_chart_anno_list = [anno_data_pname_list] # [[],[]] pname, tu, kuang
            # 折线图
            line_chart_anno_list = []

            anno_data_pnums_bar_list = []
            anno_data_knums_bar_list = []
            for pidx in anno_data_pname_list:
                tmp_time_list = []
                tmp_pnums_list = []
                tmp_knums_list = []
                for idx in init_data.filter(tspname=models.Project.objects.get(pname=pidx)):
                    if idx.tskind.kinds != "审核":
                        tmp_time_list.append(idx.tsdtime.strftime("%Y-%m-%d"))
                        if tmp_pnums_list == []:
                            tmp_pnums_list.append(idx.tspnums)
                        else:
                            tmp_pnums_list.append(idx.tspnums + tmp_pnums_list[-1])

                        if idx.tskind.kinds == "视频标注":
                            if tmp_knums_list == []:
                                tmp_knums_list.append(idx.tspnums)
                            else:
                                tmp_knums_list.append(idx.tspnums + tmp_knums_list[-1])
                        else:
                            if idx.tskind.kinds == "筛选":
                                if tmp_knums_list == []:
                                    tmp_knums_list.append(0)
                                else:
                                    tmp_knums_list.append(0 + tmp_knums_list[-1])
                            else:
                                if tmp_knums_list == []:
                                    tmp_knums_list.append(int(idx.tsknums))
                                else:
                                    tmp_knums_list.append(int(idx.tsknums) + tmp_knums_list[-1])
                if tmp_time_list and tmp_pnums_list:
                    line_chart_anno_list.append([tmp_time_list, tmp_pnums_list, tmp_knums_list])
                    anno_data_pnums_bar_list.append(tmp_pnums_list[-1])
                    anno_data_knums_bar_list.append(tmp_knums_list[-1])
            bar_chart_anno_list.append(anno_data_pnums_bar_list)
            bar_chart_anno_list.append(anno_data_knums_bar_list)
            return anno_data_pname_list, bar_chart_anno_list, line_chart_anno_list
    else:
        # 没查询到数据先返回空
        return [], [], []


# 钉通知
def dingtalk(auth,kind,id,uname,pname,waibao,task_id,dtime,kinds,pnums,knums,ptimes):
    # text消息@所有人
    if kind == "删除":
        msg_text = f"@{auth} {kind} 了ID为{id}的GS数据"
    else:
        if kind == "修改":
            if task_id == "" or task_id == None:
                msg_text = f"@{auth} {kind} 了一条ID为{id}的GS数据,具体内容如下:\r\t用户名 : {uname}\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
            elif knums == "" or knums == None:
                msg_text = f"@{auth} {kind} 了一条ID为{id}的GS数据,具体内容如下:\r\t用户名 : {uname}\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
            else:
                msg_text = f"@{auth} {kind} 了一条ID为{id}的GS数据,具体内容如下:\r\t用户名 : {uname}\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t框数/属性/视频数量: {knums}\r\t工时 : {ptimes}"
        else:
            if task_id == "" or task_id == None:
                if kinds != "视频标注":
                    msg_text = f"@{auth} {kind} 了一条GS数据,具体内容如下:\r\t用户名 : {uname}\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
                msg_text = f"@{auth} {kind} 了一条GS数据,具体内容如下:\r\t用户名 : {uname}\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t框数/属性/视频数量: {knums}\r\t工时 : {ptimes}"
            elif knums == "" or task_id == None:
                msg_text = f"@{auth} {kind} 了一条GS数据,具体内容如下:\r\t用户名 : {uname}\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
            else:
                msg_text = f"@{auth} {kind} 了一条GS数据,具体内容如下:\r\t用户名 : {uname}\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t框数/属性/视频数量: {knums}\r\t工时 : {ptimes}"

    def wecom_mes():
        res = requests.post(
            f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={CONFIG['wecom_webhook_key']}", 
            json={"msgtype": "text","text": {
                "content": msg_text
            }})
        logger.info(f"企微机器人消息状态: {res.json()}")

    task_wc = threading.Thread(target=wecom_mes)

    if CONFIG['wecom_webhook_key'] == "":
        logger.warning("企业微信机器人还没有配置喔！")
    else:
        task_wc.start()

def wb_dingtalk(uname, kind, id, wbdata):
    # text消息@所有人
    if kind == "删除":
        msg_text = f"@{uname} {kind} 了ID为 {id} 的供应商数据"
    else:
        if kind == "修改":
            tmp = f"研发名字：{wbdata['user'].zh_uname}\r项目名字: {wbdata['pname'].pname}\r送标批次: {wbdata['send_data_batch']}\r送标时间: {wbdata['send_data_time']}\r送标样本数量: {wbdata['pnums']}\r数据来源: {wbdata['data_source']}\r场景分布: {wbdata['scene']}\r送标原因: {wbdata['send_reason']}\r关键帧提取方式: {wbdata['key_frame_extracted_methods']}\r是否首次标注: {wbdata['ann_field_flag']}\r供应商: {wbdata['vendor'].name}\r开始验收时间: {wbdata['begin_check_data_time']}\r结束验收时间: {wbdata['last_check_data_time']}\r标注结果返回时间: {wbdata['get_data_time']}\r"
            if wbdata['ann_meta_data']:
                ann_meta_data = wbdata['ann_meta_data']
                for k in ann_meta_data:
                    tmp += f'结算方式: {k["settlement_method"]}\r\t准确率: {k["recovery_precision"]}\r\t框数: {k["knums"]}\r\t单价: {k["unit_price"]}\r'
                tmp += f'总价: {wbdata["total_money"]}'
                msg_text = f"@{uname} {kind} 了一条ID为{id}的供应商数据,具体内容如下:\r{tmp}"
            else:
                tmp += "结算方式: 无 , 准确率: 无 , 框数: 无 , 单价: 无"
                msg_text = f"@{uname} {kind} 了一条ID为{id}的供应商数据,具体内容如下:\r{tmp}"
        else:
            tmp = f"研发名字：{wbdata['user'].zh_uname}\r项目名字: {wbdata['pname'].pname}\r送标批次: {wbdata['send_data_batch']}\r送标时间: {wbdata['send_data_time']}\r送标样本数量: {wbdata['pnums']}\r数据来源: {wbdata['data_source']}\r场景分布: {wbdata['scene']}\r送标原因: {wbdata['send_reason']}\r关键帧提取方式: {wbdata['key_frame_extracted_methods']}\r是否首次标注: {wbdata['ann_field_flag']}\r供应商:{wbdata['vendor'].name}"
            msg_text = f"@{uname} {kind} 了一条供应商数据,具体内容如下:\r{tmp}"
    
    def wecom_mes():
        res = requests.post(
            f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={CONFIG['wecom_webhook_key']}", 
            json={"msgtype": "text","text": {
                "content": msg_text
            }})
        logger.info(f"企微机器人消息状态: {res.json()}")

    task_wc = threading.Thread(target=wecom_mes)
    
    if CONFIG['wecom_webhook_key'] == "":
        logger.warning("企业微信机器人还没有配置喔！")
    else:
        task_wc.start()

def budget_talk(uname, kind, id, data):
    if kind ==  "删除":
        msg_text = f"@{uname} {kind}了一条ID为 {id} 的标注预算数据"
    if kind == "添加":
        msg_text = f"@{uname} {kind}了一条 {data['year']} 年标注预算数据:\r\t项目名字: {data['pname']}\r\t标注预算: {data['ann_budget']}"
    if kind == "修改":
        msg_text = f"@{uname} {kind}了一条ID为 {id} 的{data.year_budget}年标注预算数据, 详情如下:\r"
        msg_text += f"\t项目名字: {data.pname}\r\t标注预算: {data.ann_budget}\r\t已使用费用: {data.used_money}\r\t使用百分比: {data.used_ratio}\r\t达到1/3预算日期: {data.reaching_one_third_budget_time}\r\t1/3 汇报日期: {data.one_third_report_time}\r\t1/3 汇报文档: {data.one_third_report_file}\r\t达到2/3预算日期: {data.reaching_two_third_budget_time}\r\t2/3 汇报日期: {data.two_third_report_time}\r\t2/3 汇报文档: {data.two_third_report_file}\r\t达到 100%预算日期: {data.reaching_third_third_budget_time}\r\t100% 汇报日期: {data.third_third_report_time}\r\t100% 汇报文档: {data.third_third_report_file}"
    def wecom_mes():
        res = requests.post(
            f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={CONFIG['wecom_webhook_key']}", 
            json={"msgtype": "text","text": {
                "content": msg_text
            }})
        logger.info(f"企微机器人消息状态: {res.json()}")

    task_wc = threading.Thread(target=wecom_mes)
    
    if CONFIG['wecom_webhook_key'] == "":
        logger.warning("企业微信机器人还没有配置喔！")
    else:
        task_wc.start()

def budget_reaching_talk(pname, uname_list, ratio, flag):
    if flag == "add":
        def wecom_mes():
            res = requests.post(
                f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={CONFIG['wecom_webhook_key']}", 
                json={
                    "msgtype": "text",
                    "text": {
                        "content": f"请及时添加 {ratio} 年 项目: [{pname}] 的标注预算!",
                        "mentioned_mobile_list":[CONFIG["wecom_at_phone"]]
                        }
                    })
            logger.info(f"企微机器人消息状态: {res.json()}")

        task_wc = threading.Thread(target=wecom_mes)
        
        if CONFIG['wecom_webhook_key'] == "":
            logger.warning("企业微信机器人还没有配置喔！")
        else:
            task_wc.start()
    elif flag == "ding":
        msg_text = ""
        for item in uname_list:
            msg_text += f"@{item} "
        msg_text += f"\r请注意: {ratio.split('-')[0]}年 项目: {pname} 预算使用已达 {ratio.split('-')[-1]}"
        def wecom_mes():
            res = requests.post(
                f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={CONFIG['wecom_webhook_key']}", 
                json={"msgtype": "text","text": {
                    "content": msg_text
                }})
            logger.info(f"企微机器人消息状态: {res.json()}")

        task_wc = threading.Thread(target=wecom_mes)
        
        if CONFIG['wecom_webhook_key'] == "":
            logger.warning("企业微信机器人还没有配置喔！")
        else:
            task_wc.start()
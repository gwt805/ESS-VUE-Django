<template>
    <div id="layout">
        <div class="timeline-div">
            <el-timeline class="timeline">
                <el-timeline-item center timestamp="2024-02-24" placement="top" type="success">
                    <el-card>
                        <p>把外键指向具体字段的改为指向id</p>
                        <p>后台管理 ->用户&项目 -> 添加搜索功能</p>
                        <p>项目管理搜索功能为包含搜索</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2024-02-21" placement="top" type="success">
                    <el-card>
                        <p>后台管理 —> 添加任务类型管理</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2024-01-23" placement="top" type="success">
                    <el-card>
                        <p>动态页面样式</p>
                        <p>修复后端没有正确发出填写预算消息</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-12-13" placement="top" type="success">
                    <el-card>
                        <p>接入公司LDAP , 做用户统一账号认证</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-11-17" placement="top" type="success">
                    <el-card>
                        <p>添加工具链与ESS的项目名字和供应商对应关系管理</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-27" placement="top" type="success">
                    <el-card>
                        <p>添加年度项目预算管理 , 即哪些项目使用哪个项目的标注预算管理</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-27" placement="top" type="success">
                    <el-card>
                        <p>用户权限动态更新</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-26" placement="top" type="success">
                    <el-card>
                        <p>界面优化</p>
                        <p>更新 API 地址</p>
                        <p>添加后台管理面板及功能实现</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-25" placement="top" type="success">
                    <el-card>
                        <p>优化图表显示[默认展示当前月的数据]</p>
                        <p>鼠标默认样式修改</p>
                        <p>添加用户修改权限</p>
                        <p>菜单栏默认激活问题修复</p>
                        <p>添加修改数据前的提示</p>
                        <p>修复日期没有正常显示问题</p>
                        <p>添加开机自启shell脚本</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-24" placement="top" type="success">
                    <el-card>
                        <p>修复个人信息页面关闭后头像错误问题</p>
                        <p>修复用户注册后邮箱不能正常发送问题</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-20" placement="top" type="success">
                    <el-card>
                        <p>优化 Message 消息提示</p>
                        <p>dialog 显示优化</p>
                        <p>添加头像预览功能</p>
                        <p>添加新版本部署后通知用户刷新页面功能</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-19" placement="top" type="success">
                    <el-card>
                        <p>完成定时任务页面及添加/删除任务</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-19" placement="top" type="success">
                    <el-card>
                        <p>完成标注预算的修改功能</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-18" placement="top" type="success">
                    <el-card>
                        <p>添加标注预算展示页面</p>
                        <p>完成标注预算的添加和删除功能</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-17" placement="top" type="success">
                    <el-card>
                        <p>外部数据修改数据时的bug修复</p>
                        <p>部署时页面刷新空白bug修复</p>
                        <p>当token失效时 重新登录后可跳转至原页面</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-15" placement="top" type="success">
                    <el-card>
                        <p>添加外部数据修改功能</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-14" placement="top" type="success">
                    <el-card>
                        <p>添加注册功能</p>
                        <p>导航栏添加主题切换功能</p>
                        <p>添加头像及个人信息展示</p>
                        <p>内部和外部数据展示页面性能优化</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-10-13" placement="top" type="success">
                    <el-card>
                        <p>添加部署方式</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-09-23" placement="top" type="success">
                    <el-card>
                        <p>添加外部数据图表展示</p>
                        <p>图表页面添加重置按钮</p>
                        <p>外部数据展示页面完成添加 , 搜索 , 删除功能</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-09-22" placement="top" type="success">
                    <el-card>
                        <p>修改element-plus zh-cn plugin 错误导入 , 引发不能正常 build 问题</p>
                        <p>登录页面添加回车登录</p>
                        <p>package.json 添加相关信息</p>
                        <p>修复内部数据搜索后翻页错误问题</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-09-17" placement="top" type="success">
                    <el-card>
                        <p>完成内部数据的修改 删除 添加 功能</p>
                        <p>添加更新记录页面</p>
                        <p>添加请求错误信息提示</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-09-16" placement="top" type="success">
                    <el-card>
                        <p>完成内部的图表展示 , 添加404页面 , 添加密码修改功能</p>
                        <p>完成内部团队效率查看功能 ，添加禁止用户缩放功能 ，添加禁止用户查看源码/调试功能</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-09-12" placement="top" type="success">
                    <el-card>
                        <p>修改全局滚动条样式 , 内部图表页面完善柱状图</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-09-10" placement="top" type="success">
                    <el-card>
                        <p>完成个人绩效查询功能</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-09-09" placement="top" type="success">
                    <el-card>
                        <p>从js改成ts</p>
                        <p>更新数据库字段 , 前端首页数据展示 , 搜索及About 完善</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2023-08-28" placement="top" type="success">
                    <el-card>
                        <p>前后端搭建项目重构开始</p>
                    </el-card>
                </el-timeline-item>
                <el-timeline-item center timestamp="2022-12-12 ~ 2023-10-02" placement="top" type="success">
                    <el-card>
                        <p>老平台搭建上线 , 持续维护</p>
                    </el-card>
                </el-timeline-item>
            </el-timeline>
        </div>
    </div>
</template>

<style scoped>
.timeline-div {
    width: 100%;
    height: 100%;
    overflow: auto;
    position: absolute;
    margin-top: -20px;
}

.timeline {
    width: 55%;
    margin: auto;
    margin-top: 20px;
}

p {
    line-height: 25px;
}
</style>
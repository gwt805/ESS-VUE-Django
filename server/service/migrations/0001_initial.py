# Generated by Django 3.2.20 on 2023-10-14 12:22

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='用户名')),
                ('zh_uname', models.CharField(blank=True, max_length=20, verbose_name='姓名')),
                ('email', models.EmailField(blank=True, max_length=256, verbose_name='邮箱')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('group', models.CharField(blank=True, max_length=256, null=True, verbose_name='部门')),
                ('img', models.CharField(blank=True, max_length=1024, null=True, verbose_name='头像')),
                ('power', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default=4, max_length=1, verbose_name='权限')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': '用户信息表',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(blank=True, max_length=125, unique=True, verbose_name='项目名字')),
            ],
            options={
                'verbose_name_plural': '项目名字表',
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='外包名字')),
            ],
            options={
                'verbose_name_plural': '供应商名字表',
                'db_table': 'supplier',
            },
        ),
        migrations.CreateModel(
            name='TaskKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kinds', models.CharField(max_length=20, unique=True, verbose_name='任务类型')),
            ],
            options={
                'verbose_name_plural': '任务类型列表',
                'db_table': 'task_kind',
            },
        ),
        migrations.CreateModel(
            name='SupplierTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateField(auto_created=True)),
                ('send_data_batch', models.TextField(blank=True, default=None, verbose_name='送标批次')),
                ('ann_field_flag', models.CharField(blank=True, choices=[('首次标注', '首次标注'), ('返修标注', '返修标注')], default=None, max_length=128, verbose_name='首次/返修标注')),
                ('send_data_time', models.DateField(verbose_name='送标时间')),
                ('pnums', models.IntegerField(blank=True, verbose_name='送标样本数量')),
                ('data_source', models.CharField(choices=[('人工采集', '人工采集'), ('数据回流', '数据回流'), ('未知', '未知')], max_length=256, verbose_name='数据来源')),
                ('scene', models.TextField(default='未知', verbose_name='场景分布')),
                ('send_reason', models.TextField(default='未知', verbose_name='送标原因')),
                ('key_frame_extracted_methods', models.TextField(verbose_name='关键帧抽取方式')),
                ('anno_task_id', models.IntegerField(blank=True, null=True, unique=True, verbose_name='工具链标注任务ID')),
                ('begin_check_data_time', models.DateField(blank=True, null=True, verbose_name='开始验收时间')),
                ('last_check_data_time', models.DateField(blank=True, null=True, verbose_name='结束验收时间')),
                ('get_data_time', models.DateField(blank=True, max_length=20, null=True, verbose_name='收到标注结果时间')),
                ('ann_meta_data', models.JSONField(blank=True, null=True, verbose_name='准确率,框数,结算方式,单价')),
                ('total_money', models.FloatField(blank=True, null=True, verbose_name='总金钱')),
                ('proname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.project', to_field='pname', verbose_name='项目名字')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='研发')),
                ('wb_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.supplier', to_field='name', verbose_name='供应商')),
            ],
            options={
                'verbose_name_plural': '供应商送标统计表',
                'db_table': 'supplier_task',
            },
        ),
        migrations.CreateModel(
            name='GSTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tstask_id', models.BigIntegerField(blank=True, null=True, verbose_name='任务ID')),
                ('tsdtime', models.DateField(verbose_name='当天日期')),
                ('tspnums', models.IntegerField(verbose_name='图片数量')),
                ('tsknums', models.CharField(blank=True, max_length=128, null=True, verbose_name='框数')),
                ('tsptimes', models.FloatField(verbose_name='工时')),
                ('tskind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.taskkind', verbose_name='任务类型')),
                ('tspname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.project', verbose_name='项目类型')),
                ('tsuname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名')),
                ('tswaibao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.supplier', verbose_name='数据标注方')),
            ],
            options={
                'verbose_name_plural': 'GS任务列表',
                'db_table': 'gs_task',
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_time', models.DateField(auto_created=True, auto_now=True)),
                ('created_time', models.DateField(auto_created=True, auto_now=True)),
                ('year_budget', models.IntegerField(verbose_name='哪年的预算')),
                ('ann_budget', models.FloatField(verbose_name='标注预算')),
                ('used_money', models.FloatField(blank=True, null=True, verbose_name='已使用费用')),
                ('used_ratio', models.FloatField(blank=True, null=True, verbose_name='使用百分比')),
                ('reaching_one_third_budget_time', models.DateField(blank=True, null=True, verbose_name='达到1/3预算日期')),
                ('one_third_report_time', models.DateField(blank=True, null=True, verbose_name='1/3 汇报日期')),
                ('one_third_report_file', models.TextField(blank=True, null=True, verbose_name='1/3 汇报文档')),
                ('reaching_two_third_budget_time', models.DateField(blank=True, null=True, verbose_name='达到2/3预算日期')),
                ('two_third_report_time', models.DateField(blank=True, null=True, verbose_name='2/3 汇报日期')),
                ('two_third_report_file', models.TextField(blank=True, null=True, verbose_name='2/3 汇报文档')),
                ('reaching_third_third_budget_time', models.DateField(blank=True, null=True, verbose_name='达到 100%预算日期')),
                ('third_third_report_time', models.DateField(blank=True, null=True, verbose_name='100% 汇报日期')),
                ('third_third_report_file', models.TextField(blank=True, null=True, verbose_name='100% 汇报文档')),
                ('proname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.project', to_field='pname', verbose_name='项目名字')),
            ],
            options={
                'verbose_name_plural': '年度标注预算表',
                'db_table': 'budget',
            },
        ),
    ]
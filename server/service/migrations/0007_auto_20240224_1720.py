# Generated by Django 3.2.22 on 2024-02-24 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20240224_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='gstask',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='slesspn',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='slessvd',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='suppliertask',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='taskkind',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ybudget',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

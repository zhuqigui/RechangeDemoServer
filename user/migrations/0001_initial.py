# Generated by Django 2.2.3 on 2019-08-05 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='用户余额')),
            ],
        ),
        migrations.CreateModel(
            name='WalletRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.DateTimeField(auto_now_add=True, verbose_name='充值时间')),
                ('money', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='充值金额')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Wallet')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='手机号码')),
                ('password', models.CharField(max_length=128, verbose_name='账号密码')),
                ('city', models.CharField(default='深圳', max_length=64, verbose_name='城市')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Wallet', verbose_name='钱包')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='反馈记录')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo', verbose_name='反馈')),
            ],
        ),
    ]

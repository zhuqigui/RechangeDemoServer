# Generated by Django 2.2.3 on 2019-08-06 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='city',
            field=models.CharField(default='深圳', max_length=16, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='slots1',
            field=models.SmallIntegerField(choices=[(0, '空闲'), (1, '使用中')], default=0, verbose_name='一号插槽'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='slots2',
            field=models.SmallIntegerField(choices=[(0, '空闲'), (1, '使用中')], default=0, verbose_name='二号插槽'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='slots3',
            field=models.SmallIntegerField(choices=[(0, '空闲'), (1, '使用中')], default=0, verbose_name='三号插槽'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='slots4',
            field=models.SmallIntegerField(choices=[(0, '空闲'), (1, '使用中')], default=0, verbose_name='四号插槽'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='slots5',
            field=models.SmallIntegerField(choices=[(0, '空闲'), (1, '使用中')], default=0, verbose_name='五号插槽'),
        ),
        migrations.AlterField(
            model_name='facility',
            name='slots6',
            field=models.SmallIntegerField(choices=[(0, '空闲'), (1, '使用中')], default=0, verbose_name='六号插槽'),
        ),
    ]
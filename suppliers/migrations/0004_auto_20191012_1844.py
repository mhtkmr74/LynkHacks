# Generated by Django 2.1.13 on 2019-10-12 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0003_auto_20191012_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliers',
            name='need',
        ),
        migrations.RemoveField(
            model_name='suppliers',
            name='volunteer_type',
        ),
        migrations.AddField(
            model_name='suppliers',
            name='password',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='suppliers',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='suppliers',
            name='number',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterModelTable(
            name='suppliers',
            table='Suppliers',
        ),
    ]

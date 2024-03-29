# Generated by Django 2.1.13 on 2019-10-12 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('victims', '0004_auto_20191012_1844'),
        ('suppliers', '0004_auto_20191012_1844'),
        ('volunteers', '0003_auto_20191012_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer_Supplier_Victim',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(default=0)),
                ('requirement_id', models.ForeignKey(db_column='Need_id', on_delete=django.db.models.deletion.CASCADE, to='victims.Needs')),
                ('supplier_id', models.ForeignKey(db_column='Supplier_id', on_delete=django.db.models.deletion.CASCADE, to='suppliers.Suppliers')),
                ('victims_id', models.ForeignKey(db_column='Victim_id', on_delete=django.db.models.deletion.CASCADE, to='victims.Victims')),
            ],
        ),
        migrations.AddField(
            model_name='volunteers',
            name='password',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='volunteers',
            name='transportation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='volunteers',
            name='type',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='volunteers',
            name='number',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterModelTable(
            name='volunteers',
            table='Volunteers',
        ),
        migrations.AddField(
            model_name='volunteer_supplier_victim',
            name='volunteer_id',
            field=models.ForeignKey(db_column='Volunteer_id', on_delete=django.db.models.deletion.CASCADE, to='volunteers.Volunteers'),
        ),
    ]

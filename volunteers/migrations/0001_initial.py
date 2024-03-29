# Generated by Django 2.2.6 on 2019-10-12 10:48

from django.db import migrations, models
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('number', models.IntegerField()),
                ('email', models.EmailField(max_length=60)),
                ('area', models.CharField(max_length=255)),
                ('need', models.TextField()),
                ('location', location_field.models.plain.PlainLocationField(max_length=63)),
            ],
        ),
    ]

# Generated by Django 2.0.2 on 2022-06-01 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='mobile_no',
        ),
        migrations.AddField(
            model_name='myuser',
            name='faxNo',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='official_mobileNo',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='myuser',
            name='personal_emailID',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='personal_mobileNo',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]

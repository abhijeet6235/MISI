# Generated by Django 2.0.7 on 2022-06-09 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0004_post_master'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level_Desig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cat_id', models.IntegerField(null=True)),
                ('designation', models.CharField(max_length=100, null=True)),
                ('department', models.CharField(max_length=50, null=True)),
                ('effectdate', models.CharField(max_length=20, null=True)),
                ('un_officer_id', models.IntegerField(null=True)),
                ('level', models.CharField(max_length=2, null=True)),
                ('designation_code', models.CharField(max_length=15, null=True)),
                ('parent_desig_code', models.CharField(max_length=15, null=True)),
                ('rly_unit', models.CharField(max_length=15, null=True)),
                ('pc7_level', models.IntegerField(blank=True, null=True)),
                ('department_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myadmin.departMast')),
            ],
        ),
    ]

# Generated by Django 2.1.5 on 2019-01-22 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20190121_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useradvinfo',
            name='company_location',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='useradvinfo',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='useradvinfo',
            name='user_twitter_handle',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 2.2.16 on 2022-04-03 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220402_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='confirm_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

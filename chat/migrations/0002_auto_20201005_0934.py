# Generated by Django 2.2.13 on 2020-10-05 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='receiver',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.TextField(),
        ),
    ]
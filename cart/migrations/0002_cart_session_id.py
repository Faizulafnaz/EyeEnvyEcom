# Generated by Django 4.2.1 on 2023-06-24 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_id',
            field=models.TextField(default=None),
        ),
    ]

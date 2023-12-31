# Generated by Django 4.2.1 on 2023-07-20 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('off_percent', models.PositiveIntegerField()),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
            ],
        ),
    ]

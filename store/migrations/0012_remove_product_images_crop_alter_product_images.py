# Generated by Django 4.2.1 on 2023-06-30 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_product_image_crop_product_images_crop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images_crop',
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ImageField(upload_to='photos/categories'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-11-10 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_order_is_driver_alter_order_car_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True, help_text="Buyurtma haqida qo'shimcha izoh", null=True, verbose_name='description'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-11-02 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/orders/%Y/%m/%d/'),
        ),
    ]

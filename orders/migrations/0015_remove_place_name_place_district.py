# Generated by Django 4.1.2 on 2022-11-23 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_alter_order_to_place'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='name',
        ),
        migrations.AddField(
            model_name='place',
            name='district',
            field=models.CharField(blank=True, help_text='Tuman nomi. M: Yunusobod', max_length=50, null=True, verbose_name='Place Name'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-12-12 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_order_time_alter_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='forward_free',
            field=models.BooleanField(default=True, help_text="Mashinaning chap orqa o'rindig'i bo'shmi?", verbose_name="haydovchi yonidagi o'rindiq"),
        ),
        migrations.AddField(
            model_name='order',
            name='left_back_free',
            field=models.BooleanField(default=True, help_text="Mashinaning chap orqa o'rindig'i bo'shmi?", verbose_name="orqa chap o'rindiq"),
        ),
        migrations.AddField(
            model_name='order',
            name='middle_free',
            field=models.BooleanField(default=True, help_text="Mashinaning o'rta o'rindig'i bo'shmi?", verbose_name="orqa o'rtadagi o'rindiq"),
        ),
        migrations.AddField(
            model_name='order',
            name='right_back_free',
            field=models.BooleanField(default=True, help_text="Mashinaning o'ng orqa o'rindig'i bo'shmi?", verbose_name="orqa chap o'rindiq"),
        ),
    ]

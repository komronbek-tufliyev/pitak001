# Generated by Django 4.1.2 on 2022-11-16 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_phoneotp_count_alter_phoneotp_is_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Super adminmi?'),
        ),
    ]

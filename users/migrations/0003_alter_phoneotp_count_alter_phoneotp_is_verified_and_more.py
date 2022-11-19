# Generated by Django 4.1.2 on 2022-11-10 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_phoneotp_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneotp',
            name='count',
            field=models.IntegerField(default=0, help_text='Raqam tasdiqlanguncha yuborilgan SMSlar soni'),
        ),
        migrations.AlterField(
            model_name='phoneotp',
            name='is_verified',
            field=models.BooleanField(default=False, help_text='Tasdiqlandimi?'),
        ),
        migrations.AlterField(
            model_name='phoneotp',
            name='otp',
            field=models.CharField(help_text='Bir martalik kodd. M: 1234', max_length=6),
        ),
        migrations.AlterField(
            model_name='smslog',
            name='message',
            field=models.TextField(help_text='Telefonga yuborilgan OTP(bir martalik kodd) mavjud xabar'),
        ),
        migrations.AlterField(
            model_name='smslog',
            name='phone',
            field=models.CharField(help_text='Telefon raqam', max_length=13),
        ),
        migrations.AlterField(
            model_name='smstoken',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='..vaqtda yaratilgan'),
        ),
        migrations.AlterField(
            model_name='smstoken',
            name='expires_at',
            field=models.DateTimeField(blank=True, help_text='..vaqtgacha amal qiladi', null=True),
        ),
        migrations.AlterField(
            model_name='smstoken',
            name='name',
            field=models.CharField(blank=True, help_text='SMS token nomi', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='smstoken',
            name='token',
            field=models.CharField(blank=True, help_text='Token nomi', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='device_token',
            field=models.CharField(blank=True, help_text='Qurilmaga berilgan token(shart emas)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_login',
            field=models.BooleanField(default=True, help_text='Birinchi marta login qilib kiryaptimi?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Faolmi (hozir ham ishlatyaptimi)?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_driver',
            field=models.BooleanField(default=False, help_text='Haydovchimi'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Xodimmi?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Superadminmi?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, help_text="To'liq ism. M: Falonchiyev Pistonchi", max_length=50, null=True, verbose_name='name'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-12-16 13:57

import django.core.validators
from django.db import migrations, models
import users.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message="Faqat O'zbekiston raqamlari kiriting", regex='^998[0-9]{2}[0-9]{7}$')])),
                ('otp', models.CharField(help_text='Bir martalik kodd. M: 1234', max_length=6)),
                ('count', models.IntegerField(default=0, help_text='Raqam tasdiqlanguncha yuborilgan SMSlar soni')),
                ('is_verified', models.BooleanField(default=False, help_text='Tasdiqlandimi?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Phone OTP',
                'verbose_name_plural': 'Phone OTPS',
            },
        ),
        migrations.CreateModel(
            name='SMSLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(help_text='Telefon raqam', max_length=13)),
                ('message', models.TextField(help_text='Telefonga yuborilgan OTP(bir martalik kodd) mavjud xabar')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'SMS log',
                'verbose_name_plural': 'SMS logs',
            },
        ),
        migrations.CreateModel(
            name='SMSToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='SMS token nomi', max_length=50, null=True)),
                ('token', models.CharField(blank=True, help_text='Token nomi', max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='..vaqtda yaratilgan')),
                ('expires_at', models.DateTimeField(blank=True, help_text='..vaqtgacha amal qiladi', null=True)),
            ],
            options={
                'verbose_name': 'SMS Token',
                'verbose_name_plural': 'SMS Tokens',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(help_text='Phone number must be entered in the format: 9989XXXXXXXX', max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message="Faqat O'zbekiston raqamlari kiriting", regex='^998[0-9]{2}[0-9]{7}$')], verbose_name='phone number')),
                ('phone2', models.CharField(blank=True, help_text='Phone number must be entered in the format: 9989XXXXXXXX', max_length=13, null=True, validators=[django.core.validators.RegexValidator(message="Faqat O'zbekiston raqamlari kiriting", regex='^998[0-9]{2}[0-9]{7}$')], verbose_name='phone number2')),
                ('name', models.CharField(blank=True, help_text="To'liq ism. M: Falonchiyev Pistonchi", max_length=50, null=True, verbose_name='name')),
                ('is_driver', models.BooleanField(default=False, help_text='Haydovchimi')),
                ('image', models.ImageField(blank=True, null=True, upload_to='users/')),
                ('device_token', models.CharField(blank=True, help_text='Qurilmaga berilgan token(shart emas)', max_length=255, null=True)),
                ('first_login', models.BooleanField(default=True, help_text='Birinchi marta login qilib kiryaptimi?')),
                ('is_active', models.BooleanField(default=True, help_text='Faolmi (hozir ham ishlatyaptimi)?')),
                ('is_staff', models.BooleanField(default=False, help_text='Xodimmi?')),
                ('is_superuser', models.BooleanField(default=False, help_text='Super adminmi?')),
                ('favourite', models.ManyToManyField(related_name='favourite_order', to='orders.order')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
    ]

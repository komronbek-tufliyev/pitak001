# Generated by Django 4.1.2 on 2022-11-01 14:41

import django.core.validators
from django.db import migrations, models
import users.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(help_text='Phone number must be entered in the format: 9989XXXXXXXX', max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message="Faqat O'zbekiston raqamlari kiriting", regex='^998[0-9]{2}[0-9]{7}$')], verbose_name='phone number')),
                ('phone2', models.CharField(blank=True, help_text='Phone number must be entered in the format: 9989XXXXXXXX', max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Faqat O'zbekiston raqamlari kiriting", regex='^998[0-9]{2}[0-9]{7}$')], verbose_name='phone number2')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='name')),
                ('is_driver', models.BooleanField(default=False)),
                ('device_token', models.CharField(blank=True, max_length=255, null=True)),
                ('first_login', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=13, unique=True)),
                ('otp', models.CharField(max_length=9)),
                ('count', models.IntegerField(default=0)),
                ('is_verified', models.BooleanField(default=False)),
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
                ('phone', models.CharField(max_length=13)),
                ('message', models.TextField()),
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
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('token', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'SMS Token',
                'verbose_name_plural': 'SMS Tokens',
            },
        ),
    ]

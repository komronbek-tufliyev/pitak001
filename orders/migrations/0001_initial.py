# Generated by Django 4.1.2 on 2022-11-01 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='name')),
                ('car', models.CharField(blank=True, max_length=50, null=True, verbose_name='car')),
                ('car_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='car_number')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('date', models.DateField(blank=True, null=True, verbose_name='date')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='price')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/orders/%Y/%m/%d/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('is_finished', models.BooleanField(default=False)),
                ('is_canceled', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_driver', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Place Name')),
                ('region', models.CharField(choices=[('Toshkent', 'Toshkent'), ('Andijon', 'Andijon'), ('Buxoro', 'Buxoro'), ("Farg'ona", "Farg'ona"), ('Jizzax', 'Jizzax'), ('Namangan', 'Namangan'), ('Navoiy', 'Navoiy'), ('Qashqadaryo', 'Qashqadaryo'), ("Qoraqalpog'iston Respublikasi", "Qoraqalpog'iston Respublikasi"), ('Samarqand', 'Samarqand'), ('Sirdaryo', 'Sirdaryo'), ('Surxondaryo', 'Surxondaryo'), ('Toshkent vil', 'Toshkent vil'), ('Xorazm', 'Xorazm')], max_length=100, verbose_name='Region')),
            ],
            options={
                'verbose_name': 'Place',
                'verbose_name_plural': 'Places',
            },
        ),
        migrations.CreateModel(
            name='OrderFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='order_files')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='orders.order')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order File',
                'verbose_name_plural': 'Order Files',
            },
        ),
        migrations.CreateModel(
            name='OrderComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='comment')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='orders.order')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order Comment',
                'verbose_name_plural': 'Order Comments',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='from_place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_place', to='orders.place'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='to_place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_place', to='orders.place'),
        ),
    ]

# Generated by Django 4.1.2 on 2022-11-10 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0006_delete_orderfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_driver',
        ),
        migrations.AlterField(
            model_name='order',
            name='car',
            field=models.CharField(blank=True, help_text='Mashina nomi, M: Gentra', max_length=50, null=True, verbose_name='car'),
        ),
        migrations.AlterField(
            model_name='order',
            name='car_number',
            field=models.CharField(blank=True, help_text='Mashina raqami(shart emas), ixtiyoriy', max_length=50, null=True, verbose_name='car_number'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(blank=True, help_text='Buyurtma vaqti(ketish vaqti) YYYY-MM-DD. M: 2022-12-25', null=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='from_place',
            field=models.CharField(choices=[('Toshkent', 'Toshkent'), ('Andijon', 'Andijon'), ('Buxoro', 'Buxoro'), ("Farg'ona", "Farg'ona"), ('Jizzax', 'Jizzax'), ('Namangan', 'Namangan'), ('Navoiy', 'Navoiy'), ('Qashqadaryo', 'Qashqadaryo'), ("Qoraqalpog'iston Respublikasi", "Qoraqalpog'iston Respublikasi"), ('Samarqand', 'Samarqand'), ('Sirdaryo', 'Sirdaryo'), ('Surxondaryo', 'Surxondaryo'), ('Toshkent vil', 'Toshkent vil'), ('Xorazm', 'Xorazm')], help_text='Joy nomi, qayerdan...', max_length=100, verbose_name='From Place'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_accepted',
            field=models.BooleanField(default=False, help_text='Status: qabul qilinganmi'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_canceled',
            field=models.BooleanField(default=False, help_text='Status: rad etilganmi'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_finished',
            field=models.BooleanField(default=False, help_text='Status: bajarilganmi'),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False, help_text="Status: to'langanmi"),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(blank=True, help_text='Buyurtma nomi(kiritlishi shart emas), ixtiyoriy.', max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(help_text="Buyurtmachi id'si", on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(blank=True, help_text='Narxi', null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_place',
            field=models.CharField(choices=[('Toshkent', 'Toshkent'), ('Andijon', 'Andijon'), ('Buxoro', 'Buxoro'), ("Farg'ona", "Farg'ona"), ('Jizzax', 'Jizzax'), ('Namangan', 'Namangan'), ('Navoiy', 'Navoiy'), ('Qashqadaryo', 'Qashqadaryo'), ("Qoraqalpog'iston Respublikasi", "Qoraqalpog'iston Respublikasi"), ('Samarqand', 'Samarqand'), ('Sirdaryo', 'Sirdaryo'), ('Surxondaryo', 'Surxondaryo'), ('Toshkent vil', 'Toshkent vil'), ('Xorazm', 'Xorazm')], help_text='Joy nomi, qayerga...', max_length=100, verbose_name='To Place'),
        ),
        migrations.AlterField(
            model_name='orderimage',
            name='image',
            field=models.ImageField(help_text='Buyurtirilgan mashina rasmi', upload_to='orders/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='orderimage',
            name='order',
            field=models.ForeignKey(help_text='Buyurtma raqami(id)', on_delete=django.db.models.deletion.CASCADE, related_name='order_image', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(help_text='Joy nomi. M: Yunusobod', max_length=50, verbose_name='Place Name'),
        ),
        migrations.AlterField(
            model_name='place',
            name='region',
            field=models.CharField(choices=[('Toshkent', 'Toshkent'), ('Andijon', 'Andijon'), ('Buxoro', 'Buxoro'), ("Farg'ona", "Farg'ona"), ('Jizzax', 'Jizzax'), ('Namangan', 'Namangan'), ('Navoiy', 'Navoiy'), ('Qashqadaryo', 'Qashqadaryo'), ("Qoraqalpog'iston Respublikasi", "Qoraqalpog'iston Respublikasi"), ('Samarqand', 'Samarqand'), ('Sirdaryo', 'Sirdaryo'), ('Surxondaryo', 'Surxondaryo'), ('Toshkent vil', 'Toshkent vil'), ('Xorazm', 'Xorazm')], help_text='Viloyat nomi, 14ta tanlov bor.', max_length=100, verbose_name='Region'),
        ),
    ]

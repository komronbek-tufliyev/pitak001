# Generated by Django 4.1.2 on 2022-12-17 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0006_alter_order_forward_seat_alter_order_left_back_seat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='forward_seat',
        ),
        migrations.RemoveField(
            model_name='order',
            name='left_back_seat',
        ),
        migrations.RemoveField(
            model_name='order',
            name='middle_seat',
        ),
        migrations.RemoveField(
            model_name='order',
            name='right_back_seat',
        ),
        migrations.CreateModel(
            name='Seats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.CharField(choices=[(1, 'forward'), (2, 'right_back'), (3, 'middle'), (4, 'left_back')], max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seat_model_order', to='orders.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seat_model_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='passengers',
            field=models.ManyToManyField(blank=True, help_text="Yo'lovchilar to'plami", null=True, related_name='order_passengers', to='orders.seats'),
        ),
    ]
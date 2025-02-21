# Generated by Django 5.0.8 on 2024-10-04 06:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ma_don_hang', models.CharField(max_length=100, unique=True)),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('da_huy', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong', models.PositiveIntegerField()),
                ('don_hang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chi_tiet_don_hang', to='order.order')),
                ('san_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]

# Generated by Django 5.0.8 on 2024-09-22 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong', models.PositiveIntegerField(default=0)),
                ('ngay_cap_nhat', models.DateTimeField(auto_now=True)),
                ('san_pham', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ton_kho', to='product.product')),
            ],
            options={
                'verbose_name': 'Tồn kho',
                'verbose_name_plural': 'Tồn kho',
            },
        ),
        migrations.CreateModel(
            name='InventoryTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loai_giao_dich', models.CharField(choices=[('nhap', 'Nhập hàng'), ('xuat', 'Xuất hàng')], max_length=4)),
                ('so_luong', models.PositiveIntegerField()),
                ('ngay_giao_dich', models.DateTimeField(auto_now_add=True)),
                ('san_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='giao_dich_ton_kho', to='product.product')),
            ],
            options={
                'verbose_name': 'Giao dịch tồn kho',
                'verbose_name_plural': 'Giao dịch tồn kho',
                'ordering': ['-ngay_giao_dich'],
            },
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-04 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='name',
            field=models.CharField(db_index=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='dealerprice',
            name='product_key',
            field=models.CharField(db_index=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='dealerprice',
            name='product_name',
            field=models.CharField(db_index=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='dealerproductstauschange',
            name='status',
            field=models.CharField(choices=[('true', 'Подтвердить'), ('false', 'Отклонить'), ('none', 'Отложить')], db_index=True, default='none', max_length=5),
        ),
        migrations.AlterField(
            model_name='dealerproductstaushistory',
            name='status_type',
            field=models.CharField(choices=[('ds', 'Рекомендательная модель'), ('manual', 'Поиск в ручную'), ('none', 'Не размечена')], db_index=True, default='none', max_length=6),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_1c',
            field=models.CharField(db_index=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.PositiveIntegerField(db_index=True),
        ),
    ]
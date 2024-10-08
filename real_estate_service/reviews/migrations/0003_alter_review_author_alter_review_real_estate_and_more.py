# Generated by Django 5.0.6 on 2024-06-25 18:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0006_alter_realty_image_workschedule'),
        ('reviews', '0002_review_author_review_real_estate'),
        ('user', '0004_alter_telegramuser_tg_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.telegramuser', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='review',
            name='real_estate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='object.realty', verbose_name='Объявление'),
        ),
        migrations.AlterField(
            model_name='review',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
    ]

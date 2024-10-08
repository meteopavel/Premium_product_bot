# Generated by Django 5.0.6 on 2024-06-27 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0006_alter_realty_image_workschedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='realty',
            name='status',
            field=models.CharField(choices=[('relevant', 'Актуально'), ('not_relevant', 'Неактуально')], default='relevant', verbose_name='Статус обьявления'),
        ),
        migrations.AddField(
            model_name='realty',
            name='type',
            field=models.CharField(choices=[('rent', 'Аренда'), ('sell', 'Продажа')], default='rent', verbose_name='Тип обьявления'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-25 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0005_realty_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realty',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='realty/images/', verbose_name='Изображение'),
        ),
        migrations.CreateModel(
            name='WorkSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('mon', 'Понедельник'), ('tue', 'Вторник'), ('wed', 'Среда'), ('thu', 'Четверг'), ('fri', 'Пятница'), ('sat', 'Суббота'), ('sun', 'Воскресенье')], max_length=3, verbose_name='День недели')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='Начало работы')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='Окончание работы')),
                ('realty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_schedule', to='object.realty', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'График работы',
                'verbose_name_plural': 'Графики работы',
            },
        ),
    ]

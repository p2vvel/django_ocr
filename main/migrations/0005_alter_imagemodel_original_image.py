# Generated by Django 3.2.7 on 2021-09-21 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_imagemodel_converted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='original_image',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.imagemodel'),
        ),
    ]

# Generated by Django 3.2.7 on 2021-09-21 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_imagemodel_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodel',
            name='original_image',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.imagemodel'),
        ),
    ]
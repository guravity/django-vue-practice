# Generated by Django 3.2.12 on 2022-11-03 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiv1', '0003_auto_20221103_1121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={},
        ),
        migrations.AlterField(
            model_name='book',
            name='published_at',
            field=models.DateField(),
        ),
    ]
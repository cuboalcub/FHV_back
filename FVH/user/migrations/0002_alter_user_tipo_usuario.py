# Generated by Django 5.1.6 on 2025-03-19 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tipo_usuario',
            field=models.CharField(max_length=50),
        ),
    ]

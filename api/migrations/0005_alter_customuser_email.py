# Generated by Django 4.2.20 on 2025-04-28 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_is_verfied_otp_is_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=155, unique=True),
        ),
    ]

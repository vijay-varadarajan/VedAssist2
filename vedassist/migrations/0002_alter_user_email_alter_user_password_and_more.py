# Generated by Django 4.2.7 on 2023-12-20 17:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vedassist", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(max_length=256, unique=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-25 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]

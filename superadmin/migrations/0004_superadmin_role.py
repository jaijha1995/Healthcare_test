# Generated by Django 5.1.4 on 2024-12-18 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0003_alter_superadmin_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='superadmin',
            name='role',
            field=models.CharField(choices=[('superadmin', 'Super Admin')], default='superadmin', max_length=20),
        ),
    ]

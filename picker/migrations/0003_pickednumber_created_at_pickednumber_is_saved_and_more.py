# Generated by Django 4.2.20 on 2025-03-24 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picker', '0002_rename_pickednumbar_pickednumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickednumber',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2025-03-24 00:00:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pickednumber',
            name='is_saved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pickednumber',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

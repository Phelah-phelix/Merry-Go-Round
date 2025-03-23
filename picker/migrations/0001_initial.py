# Generated by Django 4.2.20 on 2025-03-23 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PickedNumbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('user', models.CharField(max_length=100)),
                ('is_picked', models.BooleanField(default=False)),
            ],
        ),
    ]

# Generated by Django 4.2.4 on 2023-09-17 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignalsModal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signals_text', models.TextField()),
            ],
        ),
    ]
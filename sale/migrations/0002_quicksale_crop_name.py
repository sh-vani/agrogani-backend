# Generated by Django 4.2.23 on 2025-07-18 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quicksale',
            name='crop_name',
            field=models.CharField(default='Wheat', max_length=100),
            preserve_default=False,
        ),
    ]

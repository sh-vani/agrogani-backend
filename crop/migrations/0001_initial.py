# Generated by Django 4.2.23 on 2025-07-05 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('device_limit', models.PositiveIntegerField(default=1)),
                ('allowed_crop_types', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('crop_name', models.CharField(max_length=100)),
                ('field_size', models.DecimalField(decimal_places=2, max_digits=10)),
                ('field_unit', models.CharField(max_length=20)),
                ('crop_type', models.CharField(choices=[('type1', 'Type 1'), ('type2', 'Type 2')], max_length=10)),
                ('sowing_date', models.DateField()),
                ('irrigation_source', models.CharField(choices=[('Canal', 'Canal'), ('Tubewell', 'Tubewell')], max_length=10)),
                ('additional_notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

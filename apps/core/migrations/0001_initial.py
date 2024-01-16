# Generated by Django 3.2.23 on 2024-01-16 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.TextField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField(max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_driver_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_driver_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_driver_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('brand', models.CharField(max_length=150)),
                ('model', models.CharField(max_length=150)),
                ('serial_number', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_vehicle_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_vehicle_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('driver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.driver')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_vehicle_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InsuranceApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('review_date', models.DateField(blank=True, null=True)),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('WAITING', 'Waiting for approval')], default='Waiting for approval', max_length=25)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_insuranceapplication_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='core_insuranceapplication_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('drivers', models.ManyToManyField(to='core.Driver')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_insuranceapplication_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
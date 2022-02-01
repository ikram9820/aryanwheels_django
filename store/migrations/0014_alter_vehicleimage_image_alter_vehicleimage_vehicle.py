# Generated by Django 4.0.1 on 2022-01-27 17:07

from django.db import migrations, models
import django.db.models.deletion
import store.validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_vehicleimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicleimage',
            name='image',
            field=models.ImageField(upload_to='store/images', validators=[store.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='vehicleimage',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.vehicles'),
        ),
    ]

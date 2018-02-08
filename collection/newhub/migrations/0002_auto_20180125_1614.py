# Generated by Django 2.0.1 on 2018-01-25 23:14

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('newhub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseaselink',
            name='disease',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='diseases', to='newhub.Disease'),
        ),
        migrations.AlterField(
            model_name='diseaselink',
            name='symptom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='diseases', to='newhub.Symptom'),
        ),
    ]
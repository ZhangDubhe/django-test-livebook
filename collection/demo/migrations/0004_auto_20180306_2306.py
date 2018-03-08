# Generated by Django 2.0.1 on 2018-03-07 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_auto_20180306_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='disease_link',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='demo.DiseaseLink'),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='property',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='demo.Property'),
        ),
        migrations.AlterField(
            model_name='userlog',
            name='value',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='demo.Value'),
        ),
    ]

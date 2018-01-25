# Generated by Django 2.0.1 on 2018-01-24 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symptoms', to='medicaldb.Property')),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='symptom',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symptoms', to='medicaldb.Value'),
        ),
        migrations.AddField(
            model_name='disease',
            name='symptoms',
            field=models.ManyToManyField(related_name='diseases', to='medicaldb.Symptom'),
        ),
        migrations.AlterUniqueTogether(
            name='symptom',
            unique_together={('property', 'value')},
        ),
    ]

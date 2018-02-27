# Generated by Django 2.0.1 on 2018-02-09 18:33

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
                ('content_unique_id', models.CharField(max_length=8, null=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DiseaseLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_agree', models.IntegerField()),
                ('count_disagree', models.IntegerField()),
                ('is_valid', models.BooleanField()),
                ('disease', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='diseases', to='demo.Disease')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_describe', models.CharField(max_length=250)),
                ('count_editor', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_unique_id', models.CharField(max_length=8, null=True)),
                ('symptom_name', models.TextField()),
                ('type', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='UMLS_st',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(max_length=250, unique=True)),
                ('add_at', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
            ],
        ),
        migrations.CreateModel(
            name='UMLS_tgt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(max_length=250, unique=True)),
                ('add_at', models.DateTimeField(auto_now_add=True, verbose_name='createdAt')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=250)),
                ('user_email', models.CharField(max_length=250, unique=True)),
                ('user_organization', models.CharField(max_length=250)),
                ('user_password', models.CharField(max_length=250)),
                ('is_related', models.BooleanField()),
                ('is_doctor', models.BooleanField()),
                ('add_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_at', models.DateTimeField()),
                ('DiseaseLink', models.ManyToManyField(to='demo.DiseaseLink')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.User')),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_detail', models.CharField(max_length=250)),
                ('count_editor', models.IntegerField()),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Disease')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Property')),
                ('symptom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Symptom')),
            ],
        ),
        migrations.AddField(
            model_name='userlog',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Value'),
        ),
        migrations.AddField(
            model_name='property',
            name='symptom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.Symptom'),
        ),
        migrations.AddField(
            model_name='diseaselink',
            name='symptom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='diseases', to='demo.Symptom'),
        ),
        migrations.AlterUniqueTogether(
            name='diseaselink',
            unique_together={('disease', 'symptom')},
        ),
    ]

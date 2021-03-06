# Generated by Django 2.0.1 on 2018-03-07 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0006_auto_20180307_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concept_identifier', models.CharField(max_length=8, null=True)),
                ('name', models.TextField(null=True)),
                ('semantic_type', models.TextField(null=True)),
                ('definition', models.TextField(null=True)),
                ('source', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]

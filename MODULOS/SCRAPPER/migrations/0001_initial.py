# Generated by Django 4.0.2 on 2022-02-04 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_word', models.CharField(max_length=20)),
                ('base_lang', models.CharField(choices=[('es', 'SPANISH'), ('en', 'ENGLISH'), ('ger', 'GERMAN')], max_length=3)),
                ('spanish', models.CharField(max_length=30)),
                ('english', models.CharField(max_length=30)),
                ('german', models.CharField(max_length=30)),
                ('es_definition', models.CharField(max_length=200)),
                ('en_definition', models.CharField(max_length=200)),
                ('ger_definition', models.CharField(max_length=200)),
            ],
        ),
    ]

# Generated by Django 5.0.7 on 2024-07-22 11:00

import django.db.models.deletion
import django.db.models.functions.text
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the author', max_length=100)),
                ('date_of_birth', models.DateField(blank=True, help_text='Date of birth', null=True)),
                ('date_of_death', models.DateField(blank=True, help_text='Date of death', null=True, verbose_name='Expired')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Genres for books', max_length=50, unique=True, verbose_name='GenreName')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='language in which the book is published(lower_case)', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title for the book', max_length=100)),
                ('summary', models.TextField(help_text='a small overview of the book!', max_length=500, unique=True, verbose_name='overview')),
                ('ISBN', models.CharField(help_text='ISBN(International Standard Book Number) for the book(13 digits only)', max_length=13, unique=True, verbose_name='ISBN_ID')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='books.author')),
            ],
            options={
                'db_table': 'book_data',
            },
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('unique_id', models.CharField(default=uuid.uuid4, help_text='id given to this book instance by library', max_length=50, primary_key=True, serialize=False)),
                ('return_date', models.DateField(blank=True, help_text='When to return?', null=True)),
                ('status', models.CharField(blank=True, choices=[('a', 'AVAILABLE'), ('b', 'BORROWED'), ('n', 'NOT_AVAILABLE')], default='a', max_length=1)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='books.book')),
            ],
        ),
        migrations.AddConstraint(
            model_name='genre',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name="every genre's lowercase name must be unique", violation_error_message='Genre already present'),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='select genre for the book', to='books.genre'),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(help_text='language in which the book is published', null=True, on_delete=django.db.models.deletion.CASCADE, to='books.language', verbose_name='BookLanguage'),
        ),
    ]

# Generated by Django 4.1 on 2023-05-15 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sudoku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('step', models.CharField(max_length=4)),
                ('grids', models.CharField(max_length=729)),
            ],
            options={
                'db_table': 'd_sudoku',
            },
        ),
    ]

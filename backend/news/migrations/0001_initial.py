# Generated by Django 4.2 on 2023-06-22 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(max_length=200)),
                ('date', models.DateField()),
                ('image', models.ImageField(upload_to='news/images')),
            ],
        ),
    ]
# Generated by Django 3.0.4 on 2020-05-06 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('bio', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, unique=True)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='event_image')),
                ('link', models.URLField(blank=True)),
                ('day', models.DateTimeField(blank=True)),
                ('speakers', models.ManyToManyField(to='events.Speaker')),
            ],
        ),
    ]

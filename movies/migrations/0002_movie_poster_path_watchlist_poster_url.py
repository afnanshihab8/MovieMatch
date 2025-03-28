# Generated by Django 4.2.17 on 2025-03-20 10:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='poster_url',
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

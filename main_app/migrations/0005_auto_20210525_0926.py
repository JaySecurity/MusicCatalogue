# Generated by Django 3.2.3 on 2021-05-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20210524_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='album_art_3d',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='album_back_art',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
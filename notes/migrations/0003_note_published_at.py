# Generated by Django 4.0.4 on 2022-05-14 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_note_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='published_at',
            field=models.DateTimeField(null=True),
        ),
    ]

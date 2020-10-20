# Generated by Django 3.1.2 on 2020-10-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='Markdown',
        ),
        migrations.DeleteModel(
            name='Text',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='extra_attributes',
            field=models.JSONField(blank=True, default={}),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]

# Generated by Django 3.2.3 on 2021-06-15 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.2.9 on 2022-01-31 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20220131_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='ratings_sum',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='user_ratings_counter',
            field=models.IntegerField(default=0),
        ),
    ]
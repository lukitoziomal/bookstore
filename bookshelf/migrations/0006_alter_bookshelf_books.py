# Generated by Django 3.2.9 on 2022-01-29 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0005_shelfbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookshelf',
            name='books',
            field=models.ManyToManyField(to='bookshelf.ShelfBook'),
        ),
    ]

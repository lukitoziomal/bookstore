# Generated by Django 3.2.9 on 2022-01-29 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0006_alter_bookshelf_books'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shelfbook',
            old_name='book',
            new_name='mother_book',
        ),
    ]
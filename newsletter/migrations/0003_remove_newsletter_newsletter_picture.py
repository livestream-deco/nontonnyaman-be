# Generated by Django 4.2.5 on 2023-10-03 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_remove_newsletter_newsletter_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='newsletter_picture',
        ),
    ]
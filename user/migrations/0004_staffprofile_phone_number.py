# Generated by Django 4.1.1 on 2023-10-13 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_staffassistant_account_has_chose_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='phone_number',
            field=models.CharField(default=1515, max_length=10),
            preserve_default=False,
        ),
    ]
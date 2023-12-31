# Generated by Django 4.1.1 on 2023-10-13 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_account_role_users_account_stadium_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffAssistant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.staffprofile')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='has_chose',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='AssistanceRequest',
        ),
        migrations.AddField(
            model_name='staffassistant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='account',
            name='staff_assistant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.staffassistant'),
        ),
    ]

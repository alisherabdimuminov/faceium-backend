# Generated by Django 5.1.5 on 2025-02-02 11:41

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_gender_alter_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=100),
        ),
    ]

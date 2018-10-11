# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20181009_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_content',
            field=models.TextField(default='no-content'),
            preserve_default=False,
        ),
    ]

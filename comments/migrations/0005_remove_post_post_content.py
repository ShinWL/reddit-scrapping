# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_post_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_content',
        ),
    ]

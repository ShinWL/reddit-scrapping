# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20181008_2238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_title',
            new_name='post',
        ),
    ]

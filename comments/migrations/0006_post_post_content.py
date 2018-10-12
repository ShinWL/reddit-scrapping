# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_remove_post_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

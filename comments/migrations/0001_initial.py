# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=30)),
                ('comment_content', models.TextField()),
                ('time_fetched', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_title', models.TextField()),
                ('post_url', models.URLField()),
                ('time_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post_title',
            field=models.ForeignKey(to='comments.Post'),
        ),
    ]

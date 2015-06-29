# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogposts', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='allow_comments',
            field=models.BooleanField(verbose_name='allow comments', default=True),
        ),
    ]

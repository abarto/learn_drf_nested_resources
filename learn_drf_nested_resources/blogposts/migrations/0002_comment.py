# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
from django.conf import settings
import uuid
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogposts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, blank=True, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, blank=True, verbose_name='modified', default=django.utils.timezone.now)),
                ('id', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('content', models.TextField(max_length=255, verbose_name='content')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='author', related_name='blogposts_comment_author')),
                ('blogpost', models.ForeignKey(to='blogposts.Blogpost', editable=False, verbose_name='blogpost', related_name='comments')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

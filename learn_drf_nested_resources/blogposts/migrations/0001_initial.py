# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import uuid
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blogpost',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(verbose_name='created', editable=False, blank=True, default=django.utils.timezone.now)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(verbose_name='modified', editable=False, blank=True, default=django.utils.timezone.now)),
                ('title', models.CharField(verbose_name='title', max_length=255)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(verbose_name='slug', editable=False, blank=True, populate_from='title')),
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True, editable=False)),
                ('content', models.TextField(null=True, verbose_name='content', blank=True)),
                ('author', models.ForeignKey(verbose_name='author', editable=False, related_name='blogposts_blogpost_author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

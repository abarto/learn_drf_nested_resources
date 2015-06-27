import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel


class UUIDIdMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class AuthorMixin(models.Model):
    class Meta:
        abstract = True

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, verbose_name=_('author'),
        related_name='%(app_label)s_%(class)s_author'
    )


class Blogpost(UUIDIdMixin, TimeStampedModel, TitleSlugDescriptionModel, AuthorMixin):
    content = models.TextField(_('content'), blank=True, null=True)

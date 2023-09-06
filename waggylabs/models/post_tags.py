from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey

from taggit.models import Tag, TaggedItemBase


class PostPageTag(TaggedItemBase):
    """Class for post tags"""
    
    content_object = ParentalKey(
        'waggylabs.PostPage',
        on_delete=models.CASCADE,
        related_name='post_page_tags',
    )


class TagProxy(Tag):
    """Proxy for tags for Wagtail admin."""

    class Meta:
        proxy = True
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
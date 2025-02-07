from django.db import models

# Create your models here.

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image

from datetime import date


class BlogPage(Page):
    blog_title = models.CharField(max_length=100)
    body = RichTextField(blank=True)
    date = models.DateField("Post date", default=date.today)
    blog_banner_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("blog_title"),
        FieldPanel("body", classname="full"),
        FieldPanel("date"),
        FieldPanel("blog_banner_image"),
    ]

    class Meta:
        verbose_name = "Blog Page"
        verbose_name_plural = "Blog Pages"
        ordering = ["-date"]

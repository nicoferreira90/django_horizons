from django.db import models

# Create your models here.

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from datetime import date


class BlogPage(Page):
    blog_title = models.CharField(max_length=100)
    body = RichTextField(blank=True)
    date = models.DateField("Post date", default=date.today)

    content_panels = Page.content_panels + [
        FieldPanel("blog_title"),
        FieldPanel("body", classname="full"),
    ]

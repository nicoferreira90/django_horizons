from django.db import models

# Create your models here.

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from blog.blocks import RichTextBlock
from wagtail.images.blocks import ImageBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from datetime import date


class BlogPage(Page):
    blog_title = models.CharField(max_length=100)
    body = StreamField(
        [
            ("image", ImageBlock()),
            ("full_richtext", RichTextBlock()),
        ],
        null=True,
        blank=True,
    )
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


class BlogListingPage(RoutablePageMixin, Page):
    """Listing Page lists all blog detail pages"""

    template = "blog/blog_listing_page.html"

    max_count_per_parent = 1

    custom_title = models.CharField(
        max_length=100, blank=False, null=False, help_text="Page title"
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogPage.objects.live().public()
        return context

from django.db import models

from wagtail.models import Page

from blog.models import BlogPage, BlogListingPage

from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image
from blog.blocks import RichTextBlock
from wagtail.images.blocks import ImageBlock


class HomePage(Page):
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogPage.objects.live().public().order_by("-date")
        context["about_url"] = AboutPage.objects.first().url
        context["blog_listing_page_url"] = BlogListingPage.objects.first().url
        return context


class AboutPage(Page):
    max_count = 1

    body = StreamField(
        [
            ("image", ImageBlock()),
            ("full_richtext", RichTextBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["home_url"] = HomePage.objects.first().url
        return context

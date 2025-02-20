from django.db import models

from wagtail.models import Page

from blog.models import BlogPage


class HomePage(Page):
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogPage.objects.live().public().order_by("-date")
        return context

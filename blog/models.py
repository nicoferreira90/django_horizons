from django.db import models

from django import forms

from django.shortcuts import render, redirect

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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["blog_listing_page_url"] = BlogListingPage.objects.first().url

        # Get all the active comments for this post
        comments = BlogComment.objects.filter(post=self, active=True)
        context["comments"] = comments

        # Initialize the form (so it's available in the template, even if no comment is submitted)
        form = CommentForm()
        context["form"] = form

        return context

    def serve(self, request, *args, **kwargs):
        # Handle comment form submission
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = self
                comment.save()

                # After the comment is saved, redirect to the same page to avoid re-posting on refresh
                return redirect(self.get_url())

        # Get the context with the comment form and comments already
        context = self.get_context(request, *args, **kwargs)
        return render(request, "blog/blog_page.html", context)


class BlogListingPage(RoutablePageMixin, Page):
    """Listing Page lists all blog detail pages"""

    template = "blog/blog_listing_page.html"

    max_count = 1

    custom_title = models.CharField(
        max_length=100, blank=False, null=False, help_text="Page title"
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogPage.objects.live().public().order_by("-date")
        return context


class BlogComment(models.Model):
    post = models.ForeignKey(
        BlogPage, on_delete=models.CASCADE, related_name="comments"
    )
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    body = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ["name", "email", "body"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required")
        return email

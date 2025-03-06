from django.contrib.syndication.views import Feed
from .models import BlogPage
from django.urls import reverse


class LatestBlogPostsFeed(Feed):
    title = "Latest Blog Posts"
    link = "/rss/"  # This is the URL where your feed will be available
    description = "Updates on the latest blog posts."

    def items(self):
        # Retrieve the latest 10 blog posts (you can adjust this limit)
        return BlogPage.objects.live().order_by("-date")[
            :10
        ]  # Adjust the limit or ordering if needed

    def item_title(self, item):
        return item.blog_title  # Title of the blog post

    def item_link(self, item):
        return item.url  # Link to the blog post detail page

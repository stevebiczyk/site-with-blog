from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from datetime import date


class BlogIndexPage(Page):
    """
    A page that lists all blog posts.
    """
    descripton = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]
    
class BlogPostPage(Page):
    """
    A page that represents a single blog post.
    """
    date = models.DateField("Post date", default=date.today)
    intro =  RichTextField(blank=True)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('title'),
        FieldPanel('body'),
    ]
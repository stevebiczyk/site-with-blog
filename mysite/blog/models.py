from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from datetime import date
from modelcluster.fields import ParentalKey


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
    
    content_panels = Page.content_panels + [InlinePanel('image_gallery', label="Image Gallery"),
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('author'),
        FieldPanel('title'),
        FieldPanel('body'),
    ]
    
class BlogPageImageGallery(Orderable):
    page = ParentalKey(
        BlogPostPage,
        on_delete=models.CASCADE,
        related_name='image_gallery',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+',
    )
    caption = models.CharField(max_length=255, blank=True)
    panels = [FieldPanel('image'), FieldPanel('caption')]
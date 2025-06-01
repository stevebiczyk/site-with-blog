from datetime import date

from django import forms
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet


class BlogIndexPage(Page):
    """
    A page that lists all blog posts.
    """
    description = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [FieldPanel("description")]
    def get_context(self, request):
        context = super().get_context(request)
        blogposts = self.get.children().live().order_by('-first_published_at')
        context["blogposts"] = blogposts
        
        return context
    
class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey("BlogPostPage", related_name="tagged_items", on_delete=models.CASCADE)

    
class BlogPostPage(Page):
    """
    A page that represents a single blog post.
    """
    date = models.DateField("Post date", default=date.today)
    intro =  RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    
    content_panels = Page.content_panels + [InlinePanel('image_gallery', label="Image Gallery"),
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
        FieldPanel('title'),
        FieldPanel('body'),
        FieldPanel('tags'),
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
    
@register_snippet
class Author(models.Model):
    """
    A model that represents an author.
    """
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+',
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]
    def __str__(self):
        return self.name
    
class TagIndexPage(Page):
    """
    A page that lists all tags.
    """
    def get_context(self, request):
        tag = request.GET.get("tag")
        blogposts = BlogPostPage.objects.filter(tags__name=tag)
        
        context = super().get_context(request)
        context["blogposts"] = blogposts
        return context
    
    description = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]
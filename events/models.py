from django import forms
from django.db import models

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class EventsIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super(EventsIndexPage, self).get_context(request)

        # Get the full unpaginated listing of resource pages as a queryset -
        # replace this with your own query as appropriate
        pages = EventsPage.objects.live().order_by('event_date')

        context['events'] = pages

        return context


class EventsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'EventsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class EventsPage(Page):
    date = models.DateField("Post date")
    event_date = models.DateTimeField("Event start date")
    event_date_end = models.DateTimeField("Event end date", blank=True, null=True)
    location = models.CharField(max_length=300, blank=True)
    intro = models.CharField(max_length=300)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=EventsPageTag, blank=True)
    categories = ParentalManyToManyField('events.EventsCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Story info"),
        FieldPanel('event_date'),
        FieldPanel('event_date_end'),
        FieldPanel('location'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class EventsPageGalleryImage(Orderable):
    page = ParentalKey(EventsPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=300)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class EventsTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        pages = EventsPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['pages'] = pages
        return context


@register_snippet
class EventsCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'event categories'

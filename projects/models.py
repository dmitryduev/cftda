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


class ProjectsIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super(ProjectsIndexPage, self).get_context(request)

        # Get the full unpaginated listing of resource pages as a queryset -
        # replace this with your own query as appropriate
        # docpages = self.get_children().live().order_by('first_published_at')
        docpages = ProjectsPage.objects.live().order_by('-date')

        paginator = Paginator(docpages, 4)  # Show 9 resources per page

        page = request.GET.get('page')
        try:
            # print(page, paginator.num_pages)
            resources = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            resources = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            resources = paginator.page(paginator.num_pages)

        # make the variable 'resources' available on the template
        context['projects'] = resources

        return context


class ProjectsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProjectsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ProjectsPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=300)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ProjectsPageTag, blank=True)
    categories = ParentalManyToManyField('projects.ProjectsCategory', blank=True)

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
        ], heading="Project info"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class ProjectsPageGalleryImage(Orderable):
    page = ParentalKey(ProjectsPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=300)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class ProjectsTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        pages = ProjectsPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['pages'] = pages
        return context


@register_snippet
class ProjectsCategory(models.Model):
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
        verbose_name_plural = 'project categories'

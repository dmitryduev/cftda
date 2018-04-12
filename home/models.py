from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from stories.models import StoriesPage


class HomePage(Page):
    mission = RichTextField(blank=True)

    def carousel_stories(self):
        # Get list of live stories pages
        stories = StoriesPage.objects.all()

        # Order by most recent date first
        stories = stories.live().order_by('-date')

        # return only 3 most recent entries
        return [s for s in stories if 'carousel' in [c.name for c in s.categories.all()]][:3]

    def featured_stories(self):
        # Get list of live stories pages
        stories = StoriesPage.objects.all()

        # Order by most recent date first
        stories = stories.live().order_by('-date')

        # return only 6 most recent entries
        return [s for s in stories if 'featured' in [c.name for c in s.categories.all()]][:6]

    content_panels = Page.content_panels + [
        FieldPanel('mission', classname="full"),
    ]

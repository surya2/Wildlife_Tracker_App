import json
from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from .models import User, Wildlife, Post, Comment, Like, UploadImage, SavedPost
# Register your models here.

# changed the class name to WildlifeAdmin as a placeholder.
#   RentalAdmin, from the tutorial, referred to a location as Rental, aka property rentals

# from: https://pypi.org/project/django-google-maps/
class WildlifeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {
            'widget': map_widgets.GoogleMapsAddressWidget(attrs={
                'data-autocomplete-options': json.dumps({
                    'types': ['geocode', 'establishment'],
                    'componentRestrictions': {
                        'country': 'us'
                    }
                })
            })
        },
    }
    # from https://djangocentral.com/creating-comments-system-with-django/
    # i'm pretty sure the CommentAdmin class can be merged with this one since we only have one admin
    # changed 'created_on' to 'created_at', 'name' and 'email' to include 'user.'
    list_display = ('user.name', 'body', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('user.name', 'user.email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(User)
admin.site.register(Wildlife)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(UploadImage)
admin.site.register(SavedPost)


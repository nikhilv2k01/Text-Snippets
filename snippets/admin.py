from django.contrib import admin
from .models import Snippet, Tag

# Register models with the Django admin site
admin.site.register(Snippet)  # Register Snippet model
admin.site.register(Tag)  # Register Tag model

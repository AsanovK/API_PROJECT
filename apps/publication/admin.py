from django.contrib import admin

from .models import Publication, PublicationImage

class PublicationImageAdmin(admin.TabularInline):
    model = PublicationImage
    extra = 1

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    model = Publication
    list_display = ('author', 'title', 'slug', 'created_at', 'updated_at', 'views_count', 'category')
    # list_display = ("__str__", )
    prepopulated_fields = {'slug': ('title', )}
    inlines = [PublicationImageAdmin]
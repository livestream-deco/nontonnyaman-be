from django.contrib import admin

from newsletter.models import Newsletter

class NewsletterAdmin(admin.ModelAdmin):
    readonly_fields = ('id')
# Register your models here.
admin.site.register(Newsletter)
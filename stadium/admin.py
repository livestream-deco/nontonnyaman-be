from django.contrib import admin

from stadium.models import Stadium

class StadiumAdmin(admin.ModelAdmin):
    readonly_fields = ('id')
# Register your models here.
admin.site.register(Stadium)
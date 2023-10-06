from django.contrib import admin

# Register your models here.
from accomodationsuggestion.models import Accomodation

class AccomodationAdmin(admin.ModelAdmin):
    readonly_fields = ('id')
# Register your models here.
admin.site.register(Accomodation)
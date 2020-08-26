from django.contrib import admin
from test2api.models import users

# Register your models here.
class userAdmin(admin.ModelAdmin):
    list_display = ('uid', 'habbit')

admin.site.register(users)
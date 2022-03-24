from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(bananas)
admin.site.register(hashtag)
admin.site.site_header = 'Admistration'

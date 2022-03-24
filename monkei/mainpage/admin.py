from django.contrib import admin
from .models import Profile, Post
# Register your models here.
admin.site.register(Profile)
admin.site.site_header = 'Admistration'
admin.site.register(Post)
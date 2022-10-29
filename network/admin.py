from django.contrib import admin
from .models import User, Profil, Post, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Profil)
admin.site.register(Post)
admin.site.register(Comment)
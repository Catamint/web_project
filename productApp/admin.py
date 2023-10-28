from django.contrib import admin
from .models import *

# Register your models here.
from django.contrib.auth.models import User

class session_inline(admin.StackedInline):
    model=session_base
    extra=0

class pic_inline(admin.StackedInline):
    model=picture_base
    extra=0

class movie_admin(admin.ModelAdmin):
    list_display = ['name', 'inform', 'time_publish', 'photo']
    inlines=[pic_inline, session_inline]

class hall_admin(admin.ModelAdmin):
    list_display = ['name', 'total_seats']
    inlines=[session_inline]

# admin.site.register(product_data)
admin.site.register(movie_base, movie_admin)
admin.site.register(hall_base, hall_admin)
admin.site.register(session_base)
admin.site.register(ticket_base)
admin.site.register(kind_base)
admin.site.register(picture_base)
admin.site.register(review_base)
admin.site.register(jumbotron_base)
admin.site.register(user_exp)
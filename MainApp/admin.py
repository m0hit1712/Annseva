from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(FoodModel)
admin.site.register(RequestLocation)
admin.site.register(PostModel)
admin.site.register(CommentModel)

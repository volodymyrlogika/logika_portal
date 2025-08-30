from django.contrib import admin
from forum.models import Post,Thread,Category
# Register your models here.

admin.site.register(Post)
admin.site.register(Thread)
admin.site.register(Category)
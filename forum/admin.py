from django.contrib import admin
from forum.models import Post,Thread,Category,ReplyPost
# Register your models here.

admin.site.register(Post)
admin.site.register(Thread)
admin.site.register(Category)
admin.site.register(ReplyPost)
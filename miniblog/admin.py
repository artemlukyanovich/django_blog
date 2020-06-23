from django.contrib import admin

# Register your models here.
from .models import Blog, Comment, User, Profile
from django_admin_listfilter_dropdown.filters import \
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pub_date', 'last_comment_date')
    # fields = ['author', 'name', 'pub_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commented_blog', 'display_description', 'author', 'pub_date', )
    fields = ['commented_blog', 'description', 'author', 'pub_date', ]


@admin.register(Profile)
class BloggerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.get_fields()
                    if field.name not in ['id', 'bio']]




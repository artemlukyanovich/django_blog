from django.contrib import admin

# Register your models here.
from .models import Blog, Comment, User, Profile
from django_admin_listfilter_dropdown.filters import \
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter


# class CommentInline(admin.StackedInline):
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'pub_date', 'last_comment_date')
    list_filter = (('author', RelatedDropdownFilter), 'pub_date', )
    search_fields = ['name']
    # inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commented_blog', 'display_description', 'author', 'pub_date', )
    fields = ['commented_blog', 'description', 'author', 'pub_date', ]
    list_filter = (('author', RelatedDropdownFilter), 'pub_date', )
    search_fields = ['description']


@admin.register(Profile)
class BloggerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.get_fields()
                    if field.name not in ['id', 'bio']]
    # Некорректное отображение:
    list_filter = (('user', RelatedDropdownFilter), )






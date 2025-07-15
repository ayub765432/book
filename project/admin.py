from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from project.models import CustomUser, Profile, Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'user', 'is_read', 'publish_year')
    search_fields = ('title', 'author')

admin.site.register([Profile])

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name' ,'email', 'is_staff', 'is_superuser')
    add_fieldsets = (
        ('CreateUser', {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
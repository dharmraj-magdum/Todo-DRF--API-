from django.contrib import admin
# from .models.todo import Todo
from .models import User

# //---------------usermodelAdmin--------------------
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# create as class to customize how the admin pannel work with userModel


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'name', 'is_admin')
    list_filter = ('is_admin',)
    # this is just section of user data
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    # searching or order if needed
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)


# //---------------todomodelAdmin--------------------
# @admin.register(Todo)
# class TodoAdmin(admin.ModelAdmin):
#     list_display = ["id", "author", "text", "date"]

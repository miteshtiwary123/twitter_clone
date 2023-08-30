from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

# Unregister Group
admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    models = User
    fields = ["username"]
    inlines = [ProfileInline]

# Unregister User
admin.site.unregister(User)

# Reregister User and profile
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)